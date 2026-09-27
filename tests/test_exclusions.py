#!/usr/bin/env python3
"""scripts/exclusions.py 오프라인 검사(네트워크 0, 실제 registry 불변).

실행: python3 tests/test_exclusions.py   (unittest, 저장소 루트에서)
가짜 API(FakeSender)로 pull/push/verify/test-roundtrip 경로를 돌리고, dry-run이 HTTP를 0회 호출하는지,
금지 패턴이 승인 목록에 있어도 거부되는지, 등록 응답은 성공인데 다시 읽으면 없는 경우(verified:false)가 실패로
보고되는지를 확인한다. 끝에 실제 audit/exclusions.csv md5가 그대로인지 출력한다.
"""
import base64
import hashlib
import hmac
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import exclusions as X  # noqa: E402

REAL_REG = os.path.join(ROOT, "audit", "exclusions.csv")


def md5f(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


REAL_MD5 = md5f(REAL_REG) if os.path.exists(REAL_REG) else None
GIDS = X.target_ids()
NAMES = {GIDS[0]: "그룹A", GIDS[1]: "그룹B", GIDS[2]: "그룹C"}


class FakeSender:
    """api.searchad.naver.com 흉내 — 광고그룹 3개, 제외 검색어 메모리 저장."""

    def __init__(self, fail_keywords=(), drop_after_post=False, blocked=False, advoost=None, auth_fail=False):
        self.kws = {g: {} for g in GIDS}
        self.seq = 0
        self.calls = []
        self.fail_keywords = set(fail_keywords)
        self.drop_after_post = drop_after_post
        self.blocked = blocked
        self.advoost = advoost
        self.auth_fail = auth_fail

    def __call__(self, method, url, headers, data):
        if self.blocked:
            raise urllib.error.URLError("Tunnel connection failed: 403 Forbidden")
        if self.auth_fail:
            return 401, {"code": 1002, "message": "Invalid signature"}
        u = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(u.query)
        self.calls.append((method, u.path, dict(q), headers))
        parts = u.path.split("/")
        gid = parts[3]
        if u.path.endswith("/restricted-keywords"):
            if method == "GET":
                assert q.get("type") == ["EXP_SEARCH"], "확장 검색 칸은 type=EXP_SEARCH 로 읽어야 한다"
                return 200, [dict(keyword=k, type="EXP_SEARCH", nccAdgroupRestrictKwdId=i, regTm="2026-09-27T01:00:00.000Z")
                             for k, i in self.kws[gid].items()]
            if method == "POST":
                body = json.loads(data.decode("utf-8"))
                out = []
                for it in body:
                    k = it["keyword"]
                    if k in self.fail_keywords:
                        out.append(dict(keyword=k, resultStatus={"code": 3723, "message": "등록할 수 없는 문자"}))
                        continue
                    self.seq += 1
                    rid = f"rk-{self.seq}"
                    if not self.drop_after_post:
                        self.kws[gid][k] = rid
                    out.append(dict(keyword=k, type="EXP_SEARCH", nccAdgroupRestrictKwdId=rid, regTm="2026-09-27T02:00:00.000Z"))
                return 200, out
            if method == "DELETE":
                ids = set(q.get("ids", [""])[0].split(","))
                self.kws[gid] = {k: i for k, i in self.kws[gid].items() if i not in ids}
                return 204, None
        if method == "GET" and len(parts) == 4:  # /ncc/adgroups/{gid}
            ag = dict(nccAdgroupId=gid, name=NAMES[gid], userLock=False, useExpSearch=True)
            if self.advoost is not None:
                ag["useAdvoost"] = self.advoost
            return 200, ag
        return 404, {"message": "no route"}


def api_with(sender):
    return X.NaverApi("KEY", "SECRET", 4480035, sender=sender)


def rows_of(*specs):
    rows = []
    for kw, gname, status, regdate in specs:
        rows.append(dict(keyword=kw, group_id="", group_name=gname, type="EXP_SEARCH", status=status, source="ui",
                         registered_at=regdate, restrict_kwd_id="", verified_at="", note=""))
    return rows


class TestSignatureAndBlocked(unittest.TestCase):
    def test_signature_reference(self):
        api = api_with(FakeSender())
        ts, method, uri = "1700000000000", "GET", "/ncc/adgroups/grp-x/restricted-keywords"
        want = base64.b64encode(hmac.new(b"SECRET", f"{ts}.{method}.{uri}".encode(), hashlib.sha256).digest()).decode()
        self.assertEqual(api.sign(ts, method, uri), want)

    def test_headers_uri_without_query(self):
        s = FakeSender(); api = api_with(s)
        api.restricted(GIDS[0])
        method, path, q, h = s.calls[-1]
        self.assertEqual(h["X-Customer"], "4480035")
        self.assertEqual(h["X-Signature"], api.sign(h["X-Timestamp"], "GET", path))  # 서명은 쿼리 제외 경로로
        self.assertEqual(q, {"type": ["EXP_SEARCH"]})

    def test_blocked_reason(self):
        self.assertIn("운동", X.blocked_reason("노원역운동"))
        self.assertIn("산전", X.blocked_reason("근처산전필라테스"))
        self.assertIn("임산부", X.blocked_reason("노원임산부체험"))
        self.assertIn("경쟁사명", X.blocked_reason("노원필라테스정원내돈내산"))
        self.assertIsNone(X.blocked_reason("노원역맛집출구"))


class TestStatusAndJudgement(unittest.TestCase):
    def test_registration_status(self):
        rows = rows_of(("a", "그룹A", "registered", "2026-09-20"), ("b", "그룹A", "registered", "2026-09-20"),
                       ("b", "그룹B", "unregistered", ""), ("c", "그룹B", "unregistered", ""), ("d", "*", "keep", ""))
        self.assertEqual(X.registration_status(rows, "a")[0], "registered")
        self.assertEqual(X.registration_status(rows, "b")[0], "partial")
        self.assertEqual(X.registration_status(rows, "c")[0], "unregistered")
        self.assertEqual(X.registration_status(rows, "d")[0], "keep")
        self.assertEqual(X.registration_status(rows, "zzz")[0], "unknown")

    def test_reexposure(self):
        import datetime as dt
        d = lambda s: dt.date.fromisoformat(s)
        rows = rows_of(("a", "그룹A", "registered", "2026-09-20"), ("c", "그룹B", "unregistered", ""))
        self.assertEqual(X.reexposure_judgement(rows, "a", [d("2026-09-22")])[0], "등록돼 있는데도 노출")
        self.assertEqual(X.reexposure_judgement(rows, "a", [d("2026-09-20")])[0], "등록 당일(판정 안 함)")
        self.assertEqual(X.reexposure_judgement(rows, "a", [d("2026-09-19")])[0], "등록 전 노출(정상)")
        self.assertEqual(X.reexposure_judgement(rows, "c", [d("2026-09-22")])[0], "등록 누락 → 후보")
        self.assertEqual(X.reexposure_judgement(rows, "zzz", [d("2026-09-22")])[0], "이력 없음(registry에 없는 이름)")


class TestProposal(unittest.TestCase):
    def test_build_proposal(self):
        import pandas as pd
        rows = rows_of(("노원역카페", "그룹A", "registered", "2026-09-10"), ("노원역세", "그룹A", "unregistered", ""))
        data = [  # 검색어, 유형, 일별, 노출, 클릭
            ("노원역맛집출구", "확장", "2026.09.26.", 1, 0), ("노원역맛집출구", "확장", "2026.09.26.", 1, 0),
            ("노원구운동", "확장", "2026.09.26.", 2, 0), ("노원역필라테스정원", "확장", "2026.09.26.", 1, 0),
            ("노원필라테스주말", "확장", "2026.09.26.", 1, 0), ("노원역카페", "확장", "2026.09.26.", 3, 0),
            ("노원역세", "확장", "2026.09.26.", 2, 0), ("예전이름", "확장", "2026.09.20.", 1, 0), ("예전이름", "확장", "2026.09.26.", 1, 0),
            ("클릭있음", "확장", "2026.09.26.", 5, 1), ("일치만", "일치", "2026.09.26.", 9, 0),
        ]
        sr = pd.DataFrame(data, columns=["검색어", "검색 유형", "일별", "노출수", "클릭수"])
        sr["d"] = sr["일별"].str.rstrip(".").map(lambda s: __import__("datetime").date(*[int(x) for x in s.split(".")]))
        p = X.build_proposal(rows, sr, day="2026-09-26")
        self.assertEqual([k for k, _, _ in p["new"]], ["노원역맛집출구"])          # 첫 등장·클릭0·금지 아님
        self.assertEqual([k for k, _, _ in p["industry"]], ["노원필라테스주말"])   # 업종어 → 별도 묶음
        self.assertEqual({k for k, _, _ in p["blocked"]}, {"노원구운동", "노원역필라테스정원"})
        self.assertEqual([k for k, _, _ in p["rereg"]], ["노원역세"])
        judged = {k: j for k, _, j, _ in p["reexposed"]}
        self.assertEqual(judged["노원역카페"], "등록돼 있는데도 노출")
        self.assertEqual(judged["노원역세"], "등록 누락 → 후보")
        self.assertEqual(p["candidates"], ["노원역맛집출구", "노원역세"])
        self.assertIn("건수: 2", p["approval_text"])
        self.assertIn("이미 등록 1 · 노출 유지(사용자 결정) 0", p["approval_text"])   # 노원역카페(등록됨)가 "이미 등록"으로 셈(검증 판단 3)
        self.assertEqual(p["n_registered"], 1)
        self.assertNotIn("클릭있음", json.dumps(p, ensure_ascii=False, default=str))
        self.assertNotIn("일치만", json.dumps(p, ensure_ascii=False, default=str))
        p2 = X.build_proposal(rows, sr, day="2026-09-26", first_seen_only=False)
        self.assertIn("예전이름", [k for k, _, _ in p2["new"]])


class TestApiFlows(unittest.TestCase):
    def test_pull_updates_and_marks_missing(self):
        s = FakeSender(); s.kws[GIDS[0]] = {"노원역카페": "rk-1"}; s.kws[GIDS[1]] = {"노원역카페": "rk-2"}; s.kws[GIDS[2]] = {"노원역카페": "rk-3"}
        rows = rows_of(("노원역카페", "*", "registered", "2026-09-10"), ("사라진이름", "그룹A", "registered", "2026-09-10"))
        out = X.do_pull(api_with(s), rows, log=lambda *a: None)
        self.assertEqual(set(out), set(GIDS))
        st = {(r["keyword"], r["group_id"]): r["status"] for r in rows}
        self.assertEqual(st[("노원역카페", GIDS[0])], "registered")
        self.assertNotIn(("노원역카페", "*"), st)                       # 3그룹 API 행이 있으니 기록 행 제거
        self.assertEqual(st[("사라진이름", GIDS[0])], "missing")         # 그룹A 이름은 group_id로 연결되고 missing

    def test_pull_merges_ui_rows_by_normalized_name_and_warns_stray(self):
        s = FakeSender(); s.kws[GIDS[0]] = {"노원역카페": "rk-1"}
        rows = rows_of(("노원역카페", "그룹 A", "unregistered", ""),        # UI 전사: 공백 있는 이름, 미등록으로 적혀 있었음
                       ("노원역카페", "옛그룹", "registered", "2026-09-10"))  # API에 없는 그룹명
        logs = []
        X.do_pull(api_with(s), rows, log=logs.append)
        a = X.find_row(rows, "노원역카페", group_id=GIDS[0])
        self.assertEqual((a["group_name"], a["status"], a["restrict_kwd_id"]), ("그룹A", "registered", "rk-1"))  # 공백 무시 병합·API 이름으로
        self.assertEqual(len([r for r in rows if r["keyword"] == "노원역카페" and r["group_id"] == GIDS[0]]), 1)  # 중복 행 없음
        self.assertTrue(any("[주의] registry 그룹명 옛그룹" in m for m in logs))               # 안 맞는 그룹명 경고
        self.assertEqual(X.find_row(rows, "노원역카페", group_name="옛그룹")["status"], "registered")  # 남의 그룹 행은 건드리지 않음

    def test_push_partial_failure_then_verify(self):
        s = FakeSender(fail_keywords={"나쁜문자"}); s.kws[GIDS[2]] = {"이미있음": "rk-0"}
        rows = []
        res = X.do_push(api_with(s), rows, ["새이름", "나쁜문자", "이미있음"], "desc", log=lambda *a: None)
        self.assertEqual(res[GIDS[0]]["added"], ["새이름", "이미있음"])
        self.assertEqual([k for k, _ in res[GIDS[0]]["failed"]], ["나쁜문자"])
        self.assertEqual(res[GIDS[2]]["skipped"], ["이미있음"])
        st = {(r["keyword"], r["group_id"]): r["status"] for r in rows}
        self.assertEqual(st[("새이름", GIDS[0])], "pending")
        self.assertEqual(st[("나쁜문자", GIDS[0])], "failed")
        miss = X.do_verify(api_with(s), rows, ["새이름", "이미있음"], log=lambda *a: None)
        self.assertEqual(sum(len(m) for m in miss.values()), 0)
        st = {(r["keyword"], r["group_id"]): r for r in rows}
        self.assertEqual(st[("새이름", GIDS[1])]["status"], "registered")
        self.assertTrue(st[("새이름", GIDS[1])]["verified_at"])

    def test_verified_false_is_failure(self):
        s = FakeSender(drop_after_post=True)
        rows = []
        X.do_push(api_with(s), rows, ["유령"], "desc", log=lambda *a: None)
        miss = X.do_verify(api_with(s), rows, ["유령"], log=lambda *a: None)
        self.assertEqual({g: m for g, m in miss.items()}, {g: ["유령"] for g in GIDS})
        self.assertTrue(all(r["status"] == "failed" for r in rows if r["keyword"] == "유령"))
        with self.assertRaises(X.ApiError) as cm:
            X.do_test_roundtrip(api_with(FakeSender(drop_after_post=True)), [], "시험", GIDS[0], log=lambda *a: None)
        self.assertIn("verified:false", str(cm.exception))

    def test_test_roundtrip_success_restores(self):
        s = FakeSender(); rows = []
        X.do_test_roundtrip(api_with(s), rows, "saero제외테스트", GIDS[0], log=lambda *a: None)
        self.assertEqual([c[0] for c in s.calls], ["GET", "GET", "POST", "GET", "DELETE", "GET"])
        self.assertEqual(s.kws[GIDS[0]], {})                                   # 원상복구
        self.assertEqual(rows[0]["status"], "deleted")

    def test_network_blocked_returns_2(self):
        with tempfile.TemporaryDirectory() as td:
            kf = os.path.join(td, "k.keys.json"); reg = os.path.join(td, "r.csv")
            write_text(kf, json.dumps({"api_key": "K", "secret_key": "S"}))
            orig = X._default_sender
            X._default_sender = FakeSender(blocked=True)
            try:
                with redirect_stdout(io.StringIO()) as buf:
                    rc = X.main(["--registry", reg, "pull", "--key-file", kf])
            finally:
                X._default_sender = orig
            self.assertEqual(rc, 2)
            self.assertIn("네트워크 차단", buf.getvalue())


class TestCliSafety(unittest.TestCase):
    def test_runs_without_pandas_for_pc_commands(self):
        """첫 실사용 2026-09-27: 사용자 PC에는 pandas가 없다 — report(=pull/push/verify와 같은 import 경로)가 pandas 없이 돌아야 한다."""
        import subprocess
        script = os.path.join(ROOT, "scripts", "exclusions.py")
        code = ("import sys, runpy; sys.modules['pandas'] = None; sys.path.insert(0, %r); sys.argv = ['exclusions.py', 'report']; "
                "runpy.run_path(%r, run_name='__main__')" % (os.path.dirname(script), script))  # python scripts\\exclusions.py 와 같은 조건
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        self.assertIn("registry", r.stdout)
        self.assertNotIn("pandas", r.stderr)

    def test_missing_registry_stops_judging_commands_but_pull_creates(self):
        """검증 판단 1: registry가 없으면 propose/push/verify/delete/test-roundtrip/report는 [FAIL] … 미확인 exit 1, pull은 새로 만든다."""
        with tempfile.TemporaryDirectory() as td:
            reg = os.path.join(td, "없는.csv"); ap = os.path.join(td, "a.txt"); kf = os.path.join(td, "k.keys.json")
            write_text(ap, "노원역맛집출구\n"); write_text(kf, json.dumps({"api_key": "K", "secret_key": "S"}))
            cases = [["report"], ["push", "--approved", ap, "--dry-run"], ["verify", "--key-file", kf],
                     ["delete", "--group", GIDS[0], "--ids", "rk-1", "--key-file", kf, "--confirm"],
                     ["test-roundtrip", "--keyword", "x", "--group", GIDS[0], "--key-file", kf, "--confirm"]]
            for argv in cases:
                with redirect_stdout(io.StringIO()) as buf:
                    rc = X.main(["--registry", reg] + argv)
                self.assertEqual(rc, 1, argv)
                self.assertIn("registry 없음", buf.getvalue(), argv)
                self.assertIn("미확인", buf.getvalue(), argv)
                self.assertFalse(os.path.exists(reg), argv)                        # 아무것도 만들지 않는다
            orig, orig_root = X._default_sender, X.ROOT
            X._default_sender = FakeSender(); X.ROOT = td                           # 스냅샷은 임시 폴더의 work/ 에
            try:
                with redirect_stdout(io.StringIO()) as buf:
                    rc = X.main(["--registry", reg, "pull", "--key-file", kf])
            finally:
                X._default_sender, X.ROOT = orig, orig_root
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(reg))                                    # pull만 새로 만든다
            self.assertIn("스냅샷", buf.getvalue())
            self.assertTrue(os.path.exists(os.path.join(td, "work", f"exclusions_pull_{X.today()}.json")))
        with self.assertRaises(X.RegistryUnavailable):                              # 형식이 다른 파일도 멈춤
            with tempfile.TemporaryDirectory() as td:
                bad = os.path.join(td, "bad.csv"); write_text(bad, "a,b\n1,2\n")
                X.load_registry(bad)

    def test_failed_names_come_back_as_candidates_with_reason(self):
        """검증 판단 2: 등록 실패(failed) 이름은 재노출이 없어도 다음 propose 재등록 후보·report에 사유와 함께 오른다."""
        import pandas as pd
        rows = rows_of(("실패이름", "그룹A", "failed", ""))
        rows[0]["note"] = "2026-09-27 등록 실패: 3723 등록할 수 없는 문자"
        sr = pd.DataFrame([("다른이름", "확장", "2026.09.26.", 1, 0)], columns=["검색어", "검색 유형", "일별", "노출수", "클릭수"])
        sr["d"] = sr["일별"].str.rstrip(".").map(lambda s: __import__("datetime").date(*[int(x) for x in s.split(".")]))
        p = X.build_proposal(rows, sr, day="2026-09-26")
        self.assertEqual([(k, why) for k, _, why in p["rereg"]], [("실패이름", "2026-09-27 등록 실패: 3723 등록할 수 없는 문자")])
        self.assertIn("실패이름", p["candidates"])
        md = X.render_proposal(p)
        self.assertIn("**직전 실패**: 2026-09-27 등록 실패: 3723", md)
        rows[0]["status"] = "keep"                                                  # 사용자가 제외하면 사라진다
        self.assertEqual(X.build_proposal(rows, sr, day="2026-09-26")["rereg"], [])
        with tempfile.TemporaryDirectory() as td:
            reg = os.path.join(td, "r.csv"); rows[0]["status"] = "failed"; X.save_registry(reg, rows)
            with redirect_stdout(io.StringIO()) as buf:
                X.main(["--registry", reg, "report"])
            self.assertIn("등록·확인 실패 1개", buf.getvalue())
            self.assertIn("실패이름", buf.getvalue())

    def test_push_logs_capacity_and_warns_over_limit(self):
        """검증 판단 4: push는 그룹별 현재+예정을 찍고 max_per_group 초과 예상이면 [주의]; 차단은 하지 않는다."""
        s = FakeSender(); s.kws[GIDS[0]] = {f"기존{i}": f"rk-{i}" for i in range(3)}
        logs = []
        old = X.EX.get("max_per_group")
        X.EX["max_per_group"] = 4
        try:
            res = X.do_push(api_with(s), [], ["새1", "새2"], "desc", log=logs.append)
        finally:
            if old is None:
                X.EX.pop("max_per_group", None)
            else:
                X.EX["max_per_group"] = old
        line = next(m for m in logs if m.startswith("[push] 그룹A: 현재"))
        self.assertIn("현재 3 + 등록 예정 2 = 5 (한도 추정 4 — [주의] 초과 예상", line)
        self.assertEqual(res[GIDS[0]]["added"], ["새1", "새2"])                    # 경고만, 등록은 진행(3716은 항목별 실패로 남는다)
        self.assertTrue(any(m.startswith("[push] 그룹B: 현재 0 + 등록 예정 2 = 2 (한도 추정 4)") for m in logs))

    def test_delete_requires_confirm_and_verify_writes_snapshot(self):
        """참고 2: delete는 --confirm 없이는 돌지 않는다(dry-run 제외). 참고 1: verify/push도 스냅샷을 쓴다."""
        with tempfile.TemporaryDirectory() as td:
            reg = os.path.join(td, "r.csv"); kf = os.path.join(td, "k.keys.json")
            write_text(kf, json.dumps({"api_key": "K", "secret_key": "S"}))
            X.save_registry(reg, rows_of(("대기", "그룹A", "pending", "2026-09-27")))
            with self.assertRaises(SystemExit):
                X.main(["--registry", reg, "delete", "--group", GIDS[0], "--ids", "rk-1", "--key-file", kf])
            with redirect_stdout(io.StringIO()) as buf:
                rc = X.main(["--registry", reg, "delete", "--group", GIDS[0], "--ids", "rk-1", "--dry-run"])
            self.assertEqual(rc, 0); self.assertIn("호출 0", buf.getvalue())
            orig_sender, orig_root = X._default_sender, X.ROOT
            fake = FakeSender(); fake.kws[GIDS[0]] = {"대기": "rk-1"}; fake.kws[GIDS[1]] = {"대기": "rk-2"}; fake.kws[GIDS[2]] = {"대기": "rk-3"}
            X._default_sender = fake; X.ROOT = td                                  # 스냅샷은 임시 폴더의 work/ 에
            try:
                with redirect_stdout(io.StringIO()) as buf:
                    rc = X.main(["--registry", reg, "verify", "--key-file", kf])
            finally:
                X._default_sender, X.ROOT = orig_sender, orig_root
            self.assertEqual(rc, 0)
            snap = os.path.join(td, "work", f"exclusions_pull_{X.today()}.json")
            self.assertTrue(os.path.exists(snap))
            with open(snap, encoding="utf-8") as f:
                self.assertEqual(json.load(f)[GIDS[0]]["keywords"], ["대기"])

    def test_pull_auth_error_returns_1_and_keeps_registry(self):
        with tempfile.TemporaryDirectory() as td:
            kf = os.path.join(td, "k.keys.json"); reg = os.path.join(td, "r.csv"); shutil.copy(REAL_REG, reg)
            write_text(kf, json.dumps({"api_key": "K", "secret_key": "S"}))
            before = md5f(reg)
            orig = X._default_sender
            X._default_sender = FakeSender(auth_fail=True)
            try:
                with redirect_stdout(io.StringIO()) as buf:
                    rc = X.main(["--registry", reg, "pull", "--key-file", kf])
            finally:
                X._default_sender = orig
            self.assertEqual(rc, 1)
            self.assertIn("401 인증/권한 오류", buf.getvalue())
            self.assertEqual(md5f(reg), before)                             # 인증 실패 때 registry 불변

    def test_dry_run_plan_after_pull_uses_group_ids(self):
        rows = rows_of(("있음", "그룹A", "registered", ""), ("있음", "그룹B", "registered", ""), ("있음", "그룹C", "unregistered", ""))
        for r, gid in zip(rows, GIDS):
            r["group_id"] = gid                                              # pull 뒤 상태: 그룹 ID가 채워져 있다
        plan = X.dry_run_plan(rows, ["있음", "없음"])
        self.assertEqual([lab for lab, _, _, _ in plan], [f"그룹A({GIDS[0]})", f"그룹B({GIDS[1]})", f"그룹C({GIDS[2]})"])
        self.assertEqual([todo for _, todo, _, _ in plan], [["없음"], ["없음"], ["있음", "없음"]])  # 그룹C는 미등록이라 다시 등록 예정
        self.assertEqual([skip for _, _, skip, _ in plan], [["있음"], ["있음"], []])
        self.assertEqual([n for _, _, _, n in plan], [1, 1, 0])                       # 현재 registry 등록 수(용량 표시용)
        self.assertEqual(X.dry_run_plan([], ["x"]), [("(registry 비어 있음 — 3그룹 전부 등록 예정)", ["x"], [], 0)])

    def test_push_dry_run_zero_http_and_no_file_change(self):
        with tempfile.TemporaryDirectory() as td:
            reg = os.path.join(td, "r.csv"); shutil.copy(REAL_REG, reg)
            before = md5f(reg)
            ap = os.path.join(td, "approved.txt")
            write_text(ap, "노원역맛집출구\n노원역운동\n노원역맛집출구\n새로오픈\n#주석\n")  # 새로오픈 = registry에 3그룹 등록 확인된 이름
            orig = X._default_sender

            def boom(*a, **k):
                raise AssertionError("dry-run에서 HTTP 호출 발생")
            X._default_sender = boom
            try:
                with redirect_stdout(io.StringIO()) as buf:
                    rc = X.main(["--registry", reg, "push", "--approved", ap, "--dry-run"])
            finally:
                X._default_sender = orig
            out = buf.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("[거부] 노원역운동", out)                     # 금지 패턴은 승인 목록에 있어도 거부
            self.assertIn("승인 2개", out)                                # 중복 제거 + 거부 제외
            self.assertEqual(out.count("등록 예정 1 · registry에 이미 등록 1"), 3)  # 그룹별: 노원역맛집출구 등록, 새로오픈 건너뜀
            self.assertIn("건너뜀: 새로오픈", out)
            self.assertNotIn("등록: 노원역맛집출구 · 새로오픈", out)
            self.assertEqual(md5f(reg), before)
            self.assertFalse(os.path.exists(os.path.join(ROOT, "work", "should_not_exist")))

    def test_import_ui_parse_and_apply(self):
        parsed = X.parse_ui_lines("# 주석\n1|이미등록|노원역카페|확장|35|0|0\n1|+추가|노원역맛집출구|확장|1|0|0\n1|+추가|노원구근처필라테스|일치(유사검색어)|27|0|0\n이미등록|짧은형식|확장\n")
        self.assertEqual(parsed, [("이미등록", "노원역카페", "확장"), ("+추가", "노원역맛집출구", "확장"),
                                  ("+추가", "노원구근처필라테스", "일치(유사검색어)"), ("이미등록", "짧은형식", "확장")])
        rows = rows_of(("노원역맛집출구", "*", "unregistered", ""))
        n_reg, n_unreg = X.do_import_ui(rows, parsed, "그룹A", "2026-09-27")
        self.assertEqual((n_reg, n_unreg), (2, 1))                       # 일치(유사검색어) 행은 무시
        st = {(r["keyword"], r["group_name"]): r["status"] for r in rows}
        self.assertEqual(st[("노원역카페", "그룹A")], "registered")
        self.assertEqual(st[("노원역맛집출구", "그룹A")], "unregistered")
        self.assertNotIn(("노원구근처필라테스", "그룹A"), st)


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1)
    after = md5f(REAL_REG) if os.path.exists(REAL_REG) else None
    print(f"실제 registry md5 전/후 동일: {REAL_MD5 == after} ({(after or '')[:8]})")
    sys.exit(0 if r.result.wasSuccessful() and REAL_MD5 == after else 1)
