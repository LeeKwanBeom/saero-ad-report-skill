#!/usr/bin/env python3
"""scripts/exclusions.py 오프라인 검사(네트워크 0, 실제 registry 불변).

실행: "$PY" tests/test_exclusions.py   (unittest, 저장소 루트에서 Git Bash — $PY = 저장소 밖 venv 파이썬, references/code-tab.md 1절)
가짜 API(FakeSender)로 pull/push/verify/test-roundtrip 경로를 돌리고, dry-run이 HTTP를 0회 호출하는지,
금지 패턴·경쟁사명이 승인 목록에 있어도 거부되는지, 등록 응답은 성공인데 다시 읽으면 없는 경우(verified:false)가 실패로
보고되는지(함수 결과와 CLI 종료 코드 둘 다), 승인 목록 참조 선택 모드의 쓰기 전 가드(합계 ≠ N·범위 밖·빈·못 읽는 원천·중복·
출처 md5·고른 이름 하나하나의 이미 registered·keep·금지 패턴·경쟁사명 FAIL·쌍둥이 [주의]·dry-run 파일 0·실제 push의 --approved 거부·
실제 push의 pull 뒤 재검사 — 고른 이름 중 하나라도 3그룹 전부에 있으면 POST 0)와 요청 도중 끊김·응답 못 읽음(요청 결과 모름)·키 가림을 확인한다. 끝에 실제 audit/exclusions.csv md5가 그대로인지 출력한다.
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

    def __init__(self, fail_keywords=(), drop_after_post=False, blocked=False, advoost=None, auth_fail=False, desc_max=None,
                 raise_on_post=None, apply_then_raise=False, echo_key_status=None):
        self.kws = {g: {} for g in GIDS}
        self.seq = 0
        self.calls = []
        self.fail_keywords = set(fail_keywords)
        self.drop_after_post = drop_after_post
        self.blocked = blocked
        self.advoost = advoost
        self.auth_fail = auth_fail
        self.desc_max = desc_max  # description 글자 수 한도 흉내(실서버 한도는 미공개, 29자에서 3721 실측)
        self.descriptions = []    # 등록에 실제로 쓰인 description
        self.raise_on_post = raise_on_post        # POST 때 이 예외를 올린다(TimeoutError 등 — 요청 도중 끊김 흉내)
        self.apply_then_raise = apply_then_raise  # True면 저장까지 한 뒤 올린다(서버엔 반영됐는데 응답만 잃은 경우)
        self.echo_key_status = echo_key_status    # POST에 이 상태 코드로 요청 헤더(X-API-KEY)를 되돌려 준다(가림 시험)

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
                if self.echo_key_status:
                    return self.echo_key_status, {"code": 9999, "message": f"bad request; X-API-KEY={headers['X-API-KEY']}"}
                if self.raise_on_post is not None:
                    if self.apply_then_raise:
                        for it in body:
                            self.seq += 1
                            self.kws[gid][it["keyword"].upper()] = f"rk-{self.seq}"
                    raise self.raise_on_post
                if self.desc_max is not None and any(len(it.get("description", "")) > self.desc_max for it in body):
                    return 400, {"code": 3721, "status": 400, "title": "The description of the negative search terms has reached its maximum length."}
                self.descriptions += [it.get("description") for it in body]
                out = []
                for it in body:
                    k = it["keyword"].upper()  # 네이버는 영문을 대문자로 저장·응답한다(첫 실사용 실측)
                    if k in {f.upper() for f in self.fail_keywords}:
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
        for r, gid in zip(rows, [GIDS[0], GIDS[0], GIDS[1], GIDS[1], ""]):
            r["group_id"] = gid                                                  # pull 뒤: ID가 있어도 표시는 그룹명(검증 2 참고 ①)
        self.assertEqual(X.registration_status(rows, "b")[1:], ({"그룹A"}, {"그룹B"}))
        self.assertIn("미등록 그룹B", X.reexposure_judgement(rows, "b", [])[1])

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
        self.assertIn("목록(번호 = 후보 파일 줄): 1 노원역맛집출구 · 2 노원역세", p["approval_text"])   # X5: 답의 번호 = _candidates.txt 줄
        self.assertIn('"3 빼고"', p["approval_text"])
        self.assertIn('N은 숫자로 씁니다(예 "등록 승인 12개", 이 목록 그대로면 "등록 승인 2개")', p["approval_text"])   # 2026-09-29 후속 3: N 미기입 답
        self.assertIn('"위 2가지만"처럼 둘 이상으로 읽히면 글자 그대로 읽은 dry-run 목록을 보이고 다시 묻습니다', p["approval_text"])
        self.assertIn("- 1 노원필라테스주말 — 노출", X.render_proposal(p))                               # 업종어 절 번호 = _industry.txt 줄
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

    def test_pull_resolves_star_rows_into_group_rows(self):
        """첫 실사용 2026-09-27: 3그룹을 다 읽으면 기록 행(*)은 그룹별 행으로 풀린다 — 미등록 기록 → 없는 그룹마다 unregistered, 등록 기록인데 없는 그룹 → missing."""
        s = FakeSender(); s.kws[GIDS[0]] = {"반만": "rk-1"}; s.kws[GIDS[1]] = {"반만": "rk-2"}   # 그룹C에는 없음
        rows = rows_of(("미등록기록", "*", "unregistered", ""), ("반만", "*", "registered", "2026-09-23"), ("유지", "*", "keep", ""))
        X.do_pull(api_with(s), rows, log=lambda *a: None)
        self.assertEqual([r for r in rows if r["group_name"] == "*"], [])                       # * 행 0
        st = {(r["keyword"], r["group_name"]): r["status"] for r in rows}
        self.assertEqual([st[("미등록기록", n)] for n in ("그룹A", "그룹B", "그룹C")], ["unregistered"] * 3)
        self.assertEqual((st[("반만", "그룹A")], st[("반만", "그룹B")], st[("반만", "그룹C")]), ("registered", "registered", "missing"))
        self.assertEqual([st[("유지", n)] for n in ("그룹A", "그룹B", "그룹C")], ["keep"] * 3)
        self.assertEqual(X.registration_status(rows, "미등록기록"), ("unregistered", set(), {"그룹A", "그룹B", "그룹C"}))
        self.assertEqual(X.registration_status(rows, "반만")[0], "partial")
        self.assertEqual(X.registration_status(rows, "유지")[0], "keep")
        note = X.find_row(rows, "반만", group_id=GIDS[2])["note"]
        self.assertIn("API 확인: 이 그룹에 없음", note)

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


class TestDescriptionFallback(unittest.TestCase):
    """첫 실사용 2026-09-27: 'saero-ad-report 시험 2026-09-27'(29자)가 3721로 거부됨 → 짧은 설명 → 설명 없음 순 폴백."""

    def test_fallback_to_prefix_then_none(self):
        s = FakeSender(desc_max=8)                                   # 'saero 09-27'(11자) 거부, 'saero'(5자) 허용
        api = api_with(s)
        api.add_restricted(GIDS[0], ["x"], X.default_description())
        self.assertEqual(api.last_description, "saero")
        self.assertEqual(s.descriptions, ["saero"])
        self.assertEqual([c[0] for c in s.calls], ["POST", "POST"])  # 2번째 시도에서 성공
        s2 = FakeSender(desc_max=3)                                  # 어떤 설명도 안 됨 → 설명 없이
        api2 = api_with(s2)
        api2.add_restricted(GIDS[0], ["x"], X.default_description())
        self.assertEqual(api2.last_description, "")
        self.assertEqual(s2.descriptions, [None])                    # description 키 자체를 안 보냄
        self.assertEqual(len(s2.calls), 3)

    def test_other_400_is_not_retried(self):
        s = FakeSender(fail_keywords={"x"})                          # 항목별 실패는 200 응답 안의 resultStatus — 폴백 대상 아님
        api = api_with(s)
        resp = api.add_restricted(GIDS[0], ["x"], X.default_description())
        self.assertEqual(resp[0]["resultStatus"]["code"], 3723)
        self.assertEqual(api.last_description, X.default_description())
        s3 = FakeSender(auth_fail=True)                               # 401은 즉시 ApiError, 재시도 없음
        with self.assertRaises(X.ApiError):
            api_with(s3).add_restricted(GIDS[0], ["x"], "saero 09-27")

    def test_roundtrip_logs_fallback(self):
        s = FakeSender(desc_max=8); logs = []
        X.do_test_roundtrip(api_with(s), [], "시험", GIDS[0], log=logs.append)
        self.assertTrue(any("3721(길이 초과)라 'saero'으로 등록" in m for m in logs))
        self.assertEqual(s.kws[GIDS[0]], {})                          # 원상복구는 그대로
        self.assertEqual(X.default_description("test"), f"saero test {X.today()[5:]}")


class TestCaseInsensitive(unittest.TestCase):
    """첫 실사용 2026-09-27 2차 시험: 'saero제외테스트0927' 등록 응답이 'SAERO제외테스트0927' — 대소문자 구분 대조가 성공을 실패로 판정해 삭제 전에 멈췄다."""

    def test_roundtrip_with_latin_letters_passes(self):
        s = FakeSender(); rows = []
        X.do_test_roundtrip(api_with(s), rows, "saero제외테스트0927", GIDS[2], log=lambda *a: None)
        self.assertEqual([c[0] for c in s.calls], ["GET", "GET", "POST", "GET", "DELETE", "GET"])
        self.assertEqual(s.kws[GIDS[2]], {})
        self.assertEqual(rows[0]["status"], "deleted")

    def test_push_verify_with_latin_letters(self):
        s = FakeSender(); rows = []
        res = X.do_push(api_with(s), rows, ["saero제외test", "노원구godtk"], "saero 09-27", log=lambda *a: None)
        self.assertEqual([len(v["failed"]) for v in res.values()], [0, 0, 0])
        self.assertEqual(res[GIDS[0]]["added"], ["saero제외test", "노원구godtk"])
        miss = X.do_verify(api_with(s), rows, ["saero제외test", "노원구godtk"], log=lambda *a: None)
        self.assertEqual(sum(len(m) for m in miss.values()), 0)
        st = {(K, r["group_id"]): r["status"] for r in rows for K in [X.K(r["keyword"])]}
        self.assertEqual(st[("SAERO제외TEST", GIDS[0])], "registered")
        self.assertEqual(len([r for r in rows if X.K(r["keyword"]) == "SAERO제외TEST"]), 3)   # 그룹당 1행, 중복 없음
        res2 = X.do_push(api_with(s), rows, ["SAERO제외TEST"], "saero 09-27", log=lambda *a: None)
        self.assertEqual(res2[GIDS[0]]["skipped"], ["SAERO제외TEST"])                            # 이미 있음 → 건너뜀

    def test_pull_merges_case_variants_and_blocked_is_case_insensitive(self):
        s = FakeSender(); s.kws[GIDS[0]] = {"노원구GODTK": "rk-1"}
        rows = rows_of(("노원구godtk", "그룹A", "unregistered", ""))
        X.do_pull(api_with(s), rows, log=lambda *a: None)
        same = [r for r in rows if X.K(r["keyword"]) == "노원구GODTK"]
        self.assertEqual([(r["group_name"], r["status"]) for r in same], [("그룹A", "registered")])  # 한 행으로 병합
        self.assertEqual(X.registration_status(rows, "노원구GODTK")[0], "registered")
        self.assertEqual(X.registration_status(rows, "노원구godtk")[0], "registered")
        old = list(X.CFG.get("competitors", [])); X.CFG["competitors"] = old + ["AbcPilates"]
        try:
            self.assertIn("경쟁사명", X.blocked_reason("노원ABCPILATES점"))
        finally:
            X.CFG["competitors"] = old
        with tempfile.TemporaryDirectory() as td:
            ap = os.path.join(td, "a.txt"); write_text(ap, "saero제외test\nSAERO제외TEST\n노원역세\n")
            self.assertEqual(X.read_approved(ap), ["saero제외test", "노원역세"])                 # 승인 목록 중복도 대소문자 무시


class TestRegTm(unittest.TestCase):
    def test_regtm_utc_to_kst_date(self):
        """첫 실사용 2026-09-27: regTm은 UTC — 09:00 KST 전 등록분은 UTC 날짜가 하루 이르다."""
        self.assertEqual(X.regtm_to_date("2026-09-16T23:40:12.000Z"), "2026-09-17")   # 09-17 08:40 KST
        self.assertEqual(X.regtm_to_date("2026-09-17T00:10:00.000Z"), "2026-09-17")   # 09-17 09:10 KST
        self.assertEqual(X.regtm_to_date("2026-09-26T04:18:00.000Z"), "2026-09-26")   # 09-26 13:18 KST(UI 등록시각과 일치)
        self.assertEqual(X.regtm_to_date("2026-09-26T15:30:00.000Z"), "2026-09-27")   # 09-27 00:30 KST
        self.assertEqual(X.regtm_to_date("2026-09-26"), "2026-09-26")                 # 날짜만 오면 그대로
        self.assertEqual(X.regtm_to_date(None), "")


class TestCliSafety(unittest.TestCase):
    def test_runs_without_pandas_for_pc_commands(self):
        """첫 실사용 2026-09-27: 사용자 PC에는 pandas가 없다 — report(=pull/push/verify와 같은 import 경로)가 pandas 없이 돌아야 한다."""
        import subprocess
        script = os.path.join(ROOT, "scripts", "exclusions.py")
        code = ("import sys, runpy; sys.modules['pandas'] = None; sys.path.insert(0, %r); sys.argv = ['exclusions.py', 'report']; "
                "runpy.run_path(%r, run_name='__main__')" % (os.path.dirname(script), script))  # pandas 없는 파이썬으로 scripts/exclusions.py report를 부른 것과 같은 조건
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
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
        p0 = X.build_proposal(rows, sr.assign(클릭수=1), day="2026-09-26")           # 후보 0 — "이 목록 그대로면 … 0개" 없이 숫자 예만
        self.assertEqual(p0["candidates"], [])
        self.assertIn('N은 숫자로 씁니다(예 "등록 승인 12개")', p0["approval_text"])
        self.assertNotIn("이 목록 그대로면", p0["approval_text"])
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
            # 실제 registry 대신 고정 fixture(이월 ③ — 실제 registry는 회차마다 바뀌어 기대값이 깨진다):
            # 새로오픈 = 3그룹 등록 확인, 노원역맛집출구 = registry에 없음
            reg = os.path.join(td, "r.csv")
            fx = rows_of(*[("새로오픈", NAMES[g], "registered", "2026-09-10") for g in GIDS])
            for r, g in zip(fx, GIDS):
                r["group_id"] = g
            X.save_registry(reg, fx)
            before = md5f(reg)
            ap = os.path.join(td, "approved.txt")
            write_text(ap, "노원역맛집출구\n노원역운동\n노원역맛집출구\n새로오픈\n#주석\n젠필라테스노원점\n")  # 새로오픈 = registry에 3그룹 등록 확인된 이름
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
            self.assertIn("[거부] 젠필라테스노원점: 경쟁사명 '젠필라테스'", out)   # config 경쟁사명도 push 경로에서 거부(검증 1 결론 8)
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


def boom(*a, **k):
    raise AssertionError("HTTP 호출 발생 — 이 경로는 네트워크를 쓰면 안 된다")


class TestApprovedReference(unittest.TestCase):
    """2026-09-28 수정 회차 2·3(검증 1 결론 1·7, 조정 W1·W3·W4·W5·W9·W12): 승인 목록 참조 선택 모드 — push가 원천 파일에서 이름을 직접 읽고, 쓰기 전에 멈춘다.
    9/28 사고: 사용자가 승인한 '노원힐링장소.'가 마침표 없이 들어가 이미 등록된 쌍둥이 '노원힐링장소'로 "건너뜀" → 원문은 미등록."""
    CSV = ('"검색어 보고서(2026.08.26.~2026.09.27.)",2580077\n'
           "검색어,검색 유형,일별,노출수,클릭수\n"
           "노원역카페,확장,2026.09.26.,1,0\n"            # 3
           "노원힐링장소,확장,2026.09.17.,1,0\n"           # 4 — registry 3그룹 registered(마침표 없음)
           "노원힐링장소.,확장,2026.09.27.,1,0\n"          # 5 — 사용자가 승인한 원문(마침표)
           "ABC,확장,2026.09.27.,1,0\n")                   # 6

    def setUp(self):
        self.td = tempfile.mkdtemp()
        p = lambda n: os.path.join(self.td, n)
        self.w = p("work")                                                     # 원천은 저장소(ROOT=td) work/ 밑만 받는다(X4)
        self.reg, self.kf = p("r.csv"), p("k.keys.json")
        self.cand, self.ind = os.path.join(self.w, "x_candidates.txt"), os.path.join(self.w, "x_industry.txt")
        self.csv = os.path.join(self.w, "combined", "검색어.csv")              # 출처 검사: 저장소 work/combined/검색어.csv만 받는다
        os.makedirs(os.path.dirname(self.csv))
        write_text(self.csv, self.CSV)
        fx = rows_of(*[("노원힐링장소", NAMES[g], "registered", "2026-09-17") for g in GIDS],
                     *[("필테등록됨", NAMES[g], "registered", "2026-09-20") for g in GIDS],
                     ("별기록", "*", "registered", "2026-09-10"))          # 그룹 미확인 기록 — propose 기준으로는 registered
        for r, g in zip(fx, GIDS + GIDS):
            r["group_id"] = g
        X.save_registry(self.reg, fx)
        self.reg_md5 = md5f(self.reg)
        with open(self.cand, "w", encoding="utf-8", newline="\r\n") as f:   # propose는 Windows에서 CRLF로 쓴다
            f.write("새이름1\n뺄이름\nabc\n")
        write_text(self.ind, "노원필라테스주말\n필테등록됨\n")
        self.stamp()
        write_text(self.kf, json.dumps({"api_key": "K", "secret_key": "S"}))
        self.orig = (X._default_sender, X.ROOT)
        X._default_sender, X.ROOT = boom, self.td          # 승인 파일·스냅샷은 임시 폴더 work/에, 기본은 HTTP 금지

    def tearDown(self):
        X._default_sender, X.ROOT = self.orig
        shutil.rmtree(self.td)

    def stamp(self, base="x", folder=None):
        """propose가 쓰는 출처 기록(<창 이름>.md5)과 같은 형식 — 후보·업종어 파일 md5 + 지금 합본(combined)·registry md5."""
        folder = folder or self.w
        lines = []
        for suffix in ("_candidates.txt", "_industry.txt"):
            f = os.path.join(folder, base + suffix)
            if os.path.exists(f):
                lines.append(f"{md5f(f)}  {base + suffix}\n")
        lines += [f"{md5f(self.csv)}  combined\n", f"{md5f(self.reg)}  registry\n"]
        write_text(os.path.join(folder, base + ".md5"), "".join(lines))

    def write_cand(self, text, name="x_candidates.txt", crlf=True, folder=None):
        path = os.path.join(folder or self.w, name)
        with open(path, "w", encoding="utf-8", newline="\r\n" if crlf else "\n") as f:
            f.write(text)
        return path

    def push(self, *argv):
        with redirect_stdout(io.StringIO()) as buf:
            rc = X.main(["--registry", self.reg, "push", *argv])
        return rc, buf.getvalue()

    def approved_files(self):
        w = os.path.join(self.td, "work")
        return sorted(os.path.join(w, n) for n in (os.listdir(w) if os.path.isdir(w) else []) if n.startswith("approved_"))

    def read_bytes(self, path):
        with open(path, "rb") as f:
            return f.read()

    def assert_nothing_written(self, rc, out):
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] 승인 목록을 만들지 않았다 — 쓰기 0", out)
        self.assertEqual(self.approved_files(), [])                          # 승인 파일 0
        self.assertEqual(md5f(self.reg), self.reg_md5)                        # registry 불변(HTTP는 boom이 막는다)

    def test_builds_list_from_sources_with_sources_printed(self):
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2,3", "--industry", self.ind, "--industry-lines", "1",
                            "--extra-csv", self.csv, "--extra-rows", "5", "--expect", "3", "--dry-run")
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.approved_files(), [])                          # W3: dry-run은 파일을 쓰지 않는다(화면만)
        self.assertIn("[승인 목록] 3개 = --expect 3 (원천 원문 그대로) — dry-run: 파일 안 씀", out)
        self.assertIn(f"'새이름1' ← {self.cand}:1", out)
        self.assertIn(f"'노원필라테스주말' ← {self.ind}:1 (추가 — 후보 밖)", out)
        self.assertIn(f"'노원힐링장소.' ← {self.csv}:5 (추가 — 후보 밖)", out)
        self.assertIn(f"뺀 것: '뺄이름' ← {self.cand}:2 · 'abc' ← {self.cand}:3 (--drop)", out)
        self.assertIn("승인 3개", out)
        # 쌍둥이 [주의]: 고른 '노원힐링장소.'(5행)와 합본 4행·registry 3행의 '노원힐링장소'를 나란히
        self.assertIn("[주의] 쌍둥이", out)
        self.assertIn(f"고른 것 '노원힐링장소.' ← {self.csv}:5", out)
        self.assertIn(f"쌍둥이  '노원힐링장소' ← {self.csv}:4·registry 3·5·7행(registered 3)", out)

    def test_real_push_writes_raw_names_to_new_timestamped_file(self):
        """W3·W12: 실제 push만 승인 파일을 쓰고(시각 이름, 덮어쓰기 없음), 끝 마침표·앞뒤 공백까지 원문 그대로.
        X12: 시계를 고정해 두 번째 파일이 반드시 `_2.txt`."""
        import datetime as _dt
        orig_now = X.NOW
        X.NOW = lambda: _dt.datetime(2026, 9, 28, 12, 0, 0)
        self.addCleanup(setattr, X, "NOW", orig_now)
        self.write_cand(" 앞뒤공백 \n끝마침표.\n")
        write_text(self.ind, "업종필테끝.\n 업종 필테 \n")
        self.stamp()
        X._default_sender = FakeSender()
        argv = ("--from-candidates", self.cand, "--industry", self.ind, "--industry-lines", "1,2", "--expect", "4", "--key-file", self.kf)
        rc, out = self.push(*argv)
        self.assertEqual(rc, 0, out)
        self.assertIn("' 앞뒤공백 ' ←", out)
        self.assertIn("' 업종 필테 ' ←", out)
        files = self.approved_files()
        self.assertEqual(len(files), 1)
        self.assertRegex(os.path.basename(files[0]), r"^approved_\d{4}-\d\d-\d\d_\d{6}(_\d+)?\.txt$")
        self.assertEqual(self.read_bytes(files[0]), " 앞뒤공백 \n끝마침표.\n업종필테끝.\n 업종 필테 \n".encode())
        self.write_cand("둘째이름\n")
        self.stamp()
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)   # 두 번째 실제 push — 앞 파일을 덮지 않는다
        self.assertEqual(rc, 0, out)
        self.assertEqual([os.path.basename(f) for f in self.approved_files()],
                         ["approved_2026-09-28_120000.txt", "approved_2026-09-28_120000_2.txt"])   # 시계 고정 — 같은 초면 반드시 _2
        self.assertEqual(self.read_bytes(files[0]), " 앞뒤공백 \n끝마침표.\n업종필테끝.\n 업종 필테 \n".encode())

    def test_9_28_type_extra_row_already_registered_everywhere_fails(self):
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2,3", "--extra-csv", self.csv, "--extra-rows", "4",
                            "--expect", "2", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("[FAIL] 이름 '노원힐링장소' ← ", out)
        self.assertIn("이미 registered", out)
        self.assertIn(f"쌍둥이  '노원힐링장소.' ← {self.csv}:5", out)            # 맞는 행을 나란히 보인다

    def test_every_name_checked_registered_and_blocked(self):
        """W1(a)(c): 후보·업종어 이름도 — 이미 registered(모든 그룹·`*` 기록) · 금지 패턴·경쟁사면 FAIL(승인 파일에 들어가지 않는다)."""
        cases = {"노원힐링장소": "이미 registered", "별기록": "이미 registered", "노원역운동": "금지 패턴 '운동'",
                 "젠필라테스노원점": "경쟁사명 '젠필라테스'"}
        for name, want in cases.items():
            self.write_cand(f"{name}\n")
            self.stamp()
            for dry in (["--dry-run"], ["--key-file", self.kf]):
                rc, out = self.push("--from-candidates", self.cand, "--expect", "1", *dry)
                self.assert_nothing_written(rc, out)
                self.assertIn(f"[FAIL] 이름 '{name}' ← {self.cand}:1", out)
                self.assertIn(want, out, name)
                self.assertNotIn("[거부]", out)
        rc, out = self.push("--industry", self.ind, "--industry-lines", "2", "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn(f"[FAIL] 이름 '필테등록됨' ← {self.ind}:2", out)

    def test_provenance_hand_written_changed_or_swapped_fails(self):
        """W1(b): propose 산출물(이름 접미사 + 같은 폴더 .md5 기록)만 받는다."""
        outside = self.write_cand("새이름1\n", name="o_candidates.txt", folder=self.td)   # work/ 밖(출처 기록까지 있어도)
        self.stamp(base="o", folder=self.td)
        rc, out = self.push("--from-candidates", outside, "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("저장소 work/ 밑 파일만 받는다", out)
        hand = self.write_cand("노원힐링장소.\n", name="hand_candidates.txt")   # 손으로 쓴 후보 파일 — 출처 기록 없음
        rc, out = self.push("--from-candidates", hand, "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("후보 파일이 propose 산출물이 아님·propose 뒤 바뀜", out)
        self.assertIn("hand.md5", out)
        with open(self.cand, "a", encoding="utf-8") as f:                    # propose 뒤 바뀜 — md5 불일치
            f.write("덧붙임\n")
        rc, out = self.push("--from-candidates", self.cand, "--expect", "4", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("후보 파일이 propose 산출물이 아님·propose 뒤 바뀜", out)
        self.assertIn("출처 기록", out)
        self.stamp()
        rc, out = self.push("--from-candidates", self.ind, "--expect", "2", "--dry-run")       # 업종어 파일을 후보 자리에
        self.assert_nothing_written(rc, out)
        self.assertIn("_candidates.txt로 끝나야 한다", out)
        rc, out = self.push("--industry", self.cand, "--industry-lines", "1", "--expect", "1", "--dry-run")  # 후보 파일을 업종어 자리에
        self.assert_nothing_written(rc, out)
        self.assertIn("_industry.txt로 끝나야 한다", out)
        o_ind = os.path.join(self.td, "o_industry.txt")                        # 업종어 파일도 work/ 밖이면(출처 기록까지 있어도) FAIL
        write_text(o_ind, "노원필라테스주말\n")
        self.stamp(base="o", folder=self.td)
        rc, out = self.push("--industry", o_ind, "--industry-lines", "1", "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn(f"{o_ind}: 저장소 work/ 밑 파일만 받는다", out)
        hand_csv = os.path.join(self.td, "mine.csv")                           # 손으로 쓴 CSV — --extra-csv 하나만으로도 막는다(리뷰 반영)
        write_text(hand_csv, "검색어\n손으로쓴이름.\n")
        X._default_sender = FakeSender()
        for dry in (["--dry-run"], ["--key-file", self.kf]):
            rc, out = self.push("--extra-csv", hand_csv, "--extra-rows", "2", "--expect", "1", *dry)
            self.assert_nothing_written(rc, out)
            self.assertIn("합본 CSV가 저장소 work/combined/검색어.csv가 아님", out)
        self.assertEqual(X._default_sender.calls, [])                       # POST 0
        X._default_sender = boom
        rc, out = self.push("--industry", self.cand, "--industry-lines", "1", "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("_industry.txt로 끝나야 한다", out)
        os.remove(os.path.join(self.w, "x.md5"))                              # 출처 기록을 지우면
        rc, out = self.push("--from-candidates", self.cand, "--expect", "4", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("x.md5을(를) 읽을 수 없음", out)

    def test_twins_case_only_and_inside_candidate_file(self):
        """W12: 대소문자만 다른 쌍둥이(합본 칸) · 후보 파일 안 쌍둥이(끝 마침표) — 멈추지 않고 [주의]로 나란히."""
        self.write_cand("노원X\n노원x.\nabc\n")
        self.stamp()
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2", "--extra-csv", self.csv, "--extra-rows", "3",
                            "--expect", "3", "--dry-run")
        self.assertEqual(rc, 0, out)
        self.assertIn(f"고른 것 '노원X' ← {self.cand}:1", out)
        self.assertIn(f"쌍둥이  '노원x.' ← {self.cand}:2", out)                 # 후보 파일 안 쌍둥이
        self.assertIn(f"고른 것 'abc' ← {self.cand}:3", out)
        self.assertIn(f"쌍둥이  'ABC' ← {self.csv}:6", out)                     # 대소문자만 다름

    def test_sum_range_empty_missing_duplicate_fail_before_writing(self):
        cases = {
            "합계 2 ≠ --expect 3": ["--from-candidates", self.cand, "--drop", "3", "--expect", "3"],
            "--drop 9:": ["--from-candidates", self.cand, "--drop", "9", "--expect", "3"],
            "--extra-rows 2:": ["--from-candidates", self.cand, "--drop", "2,3", "--extra-csv", self.csv, "--extra-rows", "2", "--expect", "2"],
            "--extra-rows 7:": ["--from-candidates", self.cand, "--drop", "2,3", "--extra-csv", self.csv, "--extra-rows", "7", "--expect", "2"],
            "--industry-lines 3:": ["--industry", self.ind, "--industry-lines", "3", "--expect", "1"],
            "같은 이름을 두 번 고름(K() 중복)": ["--from-candidates", self.cand, "--drop", "1,2", "--extra-csv", self.csv, "--extra-rows", "6", "--expect", "2"],
            "--expect N이 없음": ["--from-candidates", self.cand],
            "--extra-csv와 --extra-rows는 함께": ["--from-candidates", self.cand, "--extra-csv", self.csv, "--expect", "3"],
            "파일 없음": ["--from-candidates", os.path.join(self.td, "없음_candidates.txt"), "--expect", "1"],
            "--drop 값 '²'": ["--from-candidates", self.cand, "--drop", "²", "--expect", "3"],   # W4: isdigit은 참, int()는 실패
        }
        for want, argv in cases.items():
            for dry in ([], ["--dry-run"]):
                rc, out = self.push(*argv, *dry)
                self.assert_nothing_written(rc, out)
                self.assertIn(want, out, (argv, dry))
        write_text(self.cand, "")
        self.stamp()
        rc, out = self.push("--from-candidates", self.cand, "--expect", "0", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("비어 있음", out)
        write_text(self.cand, "\n\n")
        rc, out = self.push("--from-candidates", self.cand, "--expect", "0", "--key-file", self.kf)
        self.assert_nothing_written(rc, out)
        with open(self.cand, "wb") as f:                                    # W4: UTF-16(PowerShell 5.1 `>`) — Traceback 대신 [FAIL]
            f.write(b"\xff\xfe" + "새이름1\r\n".encode("utf-16-le"))
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("파일을 읽을 수 없음(UnicodeDecodeError", out)
        write_text(self.csv, self.CSV + '"줄\n바꿈",확장,2026.09.27.,1,0\n')   # W4: 칸 안 줄바꿈 → 행 번호가 파일 줄과 어긋남
        self.stamp()
        for row in ("7", "8"):                                                   # 줄바꿈 든 행(7~8 두 파일 줄) — 고르면 FAIL
            rc, out = self.push("--extra-csv", self.csv, "--extra-rows", row, "--expect", "1", "--dry-run")
            self.assert_nothing_written(rc, out)
            self.assertIn(f"--extra-rows {row}: 합본 CSV {self.csv}:{row}은 칸 안에 줄바꿈이 든 행", out)
        rc, out = self.push("--extra-csv", self.csv, "--extra-rows", "3", "--expect", "1", "--dry-run")   # 다른 행은 줄 번호 그대로 고를 수 있다
        self.assertEqual(rc, 0, out)
        self.assertIn(f"'노원역카페' ← {self.csv}:3", out)
        write_text(self.csv, self.CSV + '"다\r라",확장,2026.09.27.,1,0\n마바,확장,2026.09.27.,1,0\n')   # 칸 안 CR만(따옴표 칸) — grep -n은 CR을 줄로 안 센다
        self.stamp()
        rc, out = self.push("--extra-csv", self.csv, "--extra-rows", "8", "--expect", "1", "--dry-run")   # grep -n 8행 = 마바(이웃 행이 아님)
        self.assertEqual(rc, 0, out)
        self.assertIn(f"'마바' ← {self.csv}:8", out)
        rc, out = self.push("--extra-csv", self.csv, "--extra-rows", "7", "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn(f"--extra-rows 7: 합본 CSV {self.csv}:7은 칸 안에 줄바꿈이 든 행", out)

    def test_approved_file_only_for_dry_run(self):
        ap = os.path.join(self.td, "a.txt"); write_text(ap, "새이름1\n")
        rc, out = self.push("--approved", ap, "--key-file", self.kf)            # 실제 push에 --approved → 쓰기 전 FAIL(HTTP는 boom)
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] --approved는 dry-run·시험 전용", out)
        self.assertEqual(md5f(self.reg), self.reg_md5)
        rc, out = self.push("--approved", ap, "--from-candidates", self.cand, "--expect", "3", "--dry-run")
        self.assertEqual(rc, 1, out)
        self.assertIn("함께 쓸 수 없음", out)
        rc, out = self.push("--key-file", self.kf)
        self.assertEqual(rc, 1, out)
        self.assertIn("원천이 없음", out)
        rc, out = self.push("--approved", ap, "--dry-run")                      # dry-run은 그대로 된다(승인 파일 안 씀)
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.approved_files(), [])

    def test_cli_push_and_verify_exit_1_when_not_verified(self):
        """검증 1 결론 7: 등록 응답은 성공인데 다시 읽으면 없음 → CLI push·verify 둘 다 exit 1(함수 결과만이 아니라 종료 코드)."""
        fake = FakeSender(drop_after_post=True)
        X._default_sender = fake
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2,3", "--expect", "1", "--key-file", self.kf)
        self.assertEqual(rc, 1, out)
        self.assertIn("실패/미확인 3", out)
        files = self.approved_files()
        self.assertEqual([self.read_bytes(p) for p in files], ["새이름1\n".encode()])
        self.assertEqual([c[0] for c in fake.calls].count("POST"), 3)
        with redirect_stdout(io.StringIO()) as buf:
            rc = X.main(["--registry", self.reg, "verify", "--key-file", self.kf, "--approved", files[0]])
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("3건 없음 → failed로 기록", buf.getvalue())
        fake.drop_after_post = False                                            # 대조: 정상 등록이면 둘 다 0
        self.write_cand("새이름2\n")
        self.stamp()
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)
        self.assertEqual(rc, 0, out)
        self.assertIn("실패/미확인 0", out)

    def test_propose_writes_md5_record_and_warns_empty_window(self):
        """W1(b)·W5: propose는 후보·업종어 파일의 출처 기록(.md5)을 쓰고, 창에 행이 없으면(--day가 데이터 끝 뒤) [주의] 빈 창.
        그 산출물은 push 출처 검사를 그대로 통과한다(propose → push 끝까지)."""
        out_md = os.path.join(self.w, "p.md")
        with redirect_stdout(io.StringIO()) as buf:
            rc = X.main(["--registry", self.reg, "propose", os.path.dirname(self.csv), "--day", "2026-09-30", "--out", out_md])
        self.assertEqual(rc, 0)
        self.assertIn("[주의] 빈 창(창 2026-09-30~2026-09-30 안 검색어 행 0", buf.getvalue())
        with redirect_stdout(io.StringIO()) as buf:
            rc = X.main(["--registry", self.reg, "propose", os.path.dirname(self.csv), "--since", "2026-09-27", "--out", out_md])
        self.assertEqual(rc, 0)
        self.assertNotIn("[주의] 빈 창", buf.getvalue())
        rec = os.path.join(self.w, "p.md5")
        with open(rec, encoding="utf-8") as f:
            got = dict(ln.split()[::-1] for ln in f)
        self.assertEqual(got, {"p_candidates.txt": md5f(os.path.join(self.w, "p_candidates.txt")),
                               "p_industry.txt": md5f(os.path.join(self.w, "p_industry.txt")),
                               "combined": md5f(self.csv), "registry": md5f(self.reg)})         # X4(b): 합본·registry md5도
        rc, out = self.push("--from-candidates", os.path.join(self.w, "p_candidates.txt"), "--expect", "2", "--dry-run")
        self.assertEqual(rc, 0, out)
        self.assertIn("'노원힐링장소.' ← ", out)

    def test_propose_rereg_skips_names_registered_in_every_target(self):
        """리뷰 반영: 대상 그룹 전부 등록 확인(group_id 행)인데 `*` missing 기록만 남은 이름은 propose 재등록 후보가 아니다
        — push가 "이미 registered"로 막는 이름을 propose가 내면 서로 어긋난다. 한 그룹이라도 미등록이면 그대로 후보."""
        import pandas as pd
        rows = rows_of(*[("다등록", NAMES[g], "registered", "2026-09-10") for g in GIDS], ("다등록", "*", "missing", ""),
                       *[("반등록", NAMES[g], "registered", "2026-09-10") for g in GIDS[:2]], ("반등록", NAMES[GIDS[2]], "unregistered", ""))
        for r, g in zip(rows[:3] + rows[4:7], GIDS + GIDS):
            r["group_id"] = g
        sr = pd.DataFrame([("다른이름", "확장", "2026.09.26.", 1, 0)], columns=["검색어", "검색 유형", "일별", "노출수", "클릭수"])
        sr["d"] = sr["일별"].str.rstrip(".").map(lambda s: __import__("datetime").date(*[int(x) for x in s.split(".")]))
        sr = pd.concat([sr, pd.DataFrame([("노원\n힐링", "확장", "2026.09.26.", 1, 0)], columns=["검색어", "검색 유형", "일별", "노출수", "클릭수"])], ignore_index=True)
        sr["d"] = sr["일별"].str.rstrip(".").map(lambda s: __import__("datetime").date(*[int(x) for x in s.split(".")]))
        self.assertEqual(X.registration_status(rows, "다등록")[0], "partial")
        p = X.build_proposal(rows, sr, day="2026-09-26")
        self.assertEqual([k for k, _, _ in p["rereg"]], ["반등록"])
        self.assertNotIn("다등록", p["candidates"])
        self.assertNotIn("노원\n힐링", p["candidates"])                        # 줄바꿈이 든 이름은 후보 파일에 쓸 수 없어 "뺀 것"으로(리뷰 반영)
        self.assertEqual(p["newline"], [("노원\n힐링", 1)])                       # "줄바꿈 이름 n"으로 따로 센다(X13)
        self.assertIn("줄바꿈 이름 1", p["approval_text"])
        self.assertIn("- '노원\\n힐링' — 노출 1", X.render_proposal(p))


    def registry_rows(self):
        with open(self.reg, encoding="utf-8-sig", newline="") as f:
            return list(__import__("csv").DictReader(f))

    def test_post_timeout_saves_registry_marks_failed_and_exit_1(self):
        """X1: POST 도중 TimeoutError → "요청 결과 모름" — 그 묶음은 failed, verify가 실제 상태를 다시 읽고, registry는 저장, exit 1.
        서버엔 반영됐는데 응답만 잃은 경우(apply_then_raise)는 verify가 registered로 바로잡는다. 재개 판정은 verify --approved <승인 파일>."""
        self.write_cand("새이름1\n")
        self.stamp()
        X._default_sender = FakeSender(raise_on_post=TimeoutError("timed out"))
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)
        self.assertEqual(rc, 1, out)
        self.assertIn("요청 결과 모름(TimeoutError) — 반영됐을 수 있다, verify로 확인", out)
        st = {(r["keyword"], r["group_id"]): r["status"] for r in self.registry_rows()}
        self.assertEqual([st[("새이름1", g)] for g in GIDS], ["failed"] * 3)            # registry 저장됨(verify도 없음 확인)
        self.write_cand("새이름2\n")
        self.stamp()
        fake = FakeSender(raise_on_post=TimeoutError("timed out"), apply_then_raise=True)
        X._default_sender = fake
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)
        self.assertEqual(rc, 1, out)                                                    # 요청은 실패로 센다
        st = {(r["keyword"], r["group_id"]): r["status"] for r in self.registry_rows()}
        self.assertEqual([st[("새이름2", g)] for g in GIDS], ["registered"] * 3)        # verify가 실제 상태(반영됨)로 바로잡음
        fake.raise_on_post = None
        with redirect_stdout(io.StringIO()) as buf:                                     # 재개 판정: verify --approved <이번 회차의 가장 최근 승인 파일>
            rc = X.main(["--registry", self.reg, "verify", "--key-file", self.kf, "--approved", self.approved_files()[-1]])
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("전부 확인", buf.getvalue())
        with redirect_stdout(io.StringIO()) as buf:                                     # --approved 없이 pending 0이면 판정이 아님을 말한다
            rc = X.main(["--registry", self.reg, "verify", "--key-file", self.kf])
        self.assertIn("registry에 pending 0 — 등록 여부 판정 아님(--approved <승인 파일>로 확인)", buf.getvalue())

    def test_unexpected_error_still_saves_registry(self):
        """X1: 예상 못 한 예외에도(try/finally) pull 결과가 registry에 남는다."""
        self.write_cand("새이름1\n")
        self.stamp()
        fake = FakeSender(raise_on_post=RuntimeError("뜻밖의 오류"))
        for g in GIDS:
            fake.kws[g]["서버에만있음"] = f"rk-{g}"
        X._default_sender = fake
        with self.assertRaises(RuntimeError):
            with redirect_stdout(io.StringIO()):
                X.main(["--registry", self.reg, "push", "--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf])
        self.assertIn("서버에만있음", {r["keyword"] for r in self.registry_rows()})       # pull 결과 저장됨

    def test_industry_file_twins_shown(self):
        """X3: 쌍둥이 [주의]가 _industry.txt 줄도 본다."""
        write_text(self.ind, "업종필테X\n업종필테x.\n")
        self.stamp()
        rc, out = self.push("--industry", self.ind, "--industry-lines", "1", "--expect", "1", "--dry-run")
        self.assertEqual(rc, 0, out)
        self.assertIn(f"고른 것 '업종필테X' ← {self.ind}:1", out)
        self.assertIn(f"쌍둥이  '업종필테x.' ← {self.ind}:2", out)

    def test_sources_must_be_one_run_and_unchanged_since_propose(self):
        """X4: 후보·업종어는 같은 propose 실행 · propose 뒤 합본·registry가 바뀌면 FAIL."""
        other_ind = os.path.join(self.w, "y_industry.txt")
        write_text(other_ind, "노원필라테스주말\n")
        self.stamp(base="y")
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2,3", "--industry", other_ind, "--industry-lines", "1",
                            "--expect", "2", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("--from-candidates와 --industry가 같은 propose 실행이 아님", out)
        with open(self.csv, "a", encoding="utf-8") as f:                                # propose 뒤 합본이 바뀜(ingest 다시 등)
            f.write("새검색어,확장,2026.09.27.,1,0\n")
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2,3", "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("propose 뒤 합본·registry가 바뀜 — propose부터 다시·재승인(combined", out)
        self.stamp()
        X.save_registry(self.reg, self.registry_rows() + [dict(keyword="새행", group_id="", group_name="*", type="EXP_SEARCH",
                                                                status="unregistered", source="ui", registered_at="",
                                                                restrict_kwd_id="", verified_at="", note="")])
        self.reg_md5 = md5f(self.reg)
        rc, out = self.push("--from-candidates", self.cand, "--drop", "2,3", "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("propose 뒤 합본·registry가 바뀜 — propose부터 다시·재승인(registry", out)

    def test_real_push_stops_when_pull_shows_all_present(self):
        """X6: 실제 push는 pull 직후 고른 이름이 대상 그룹 전부에 이미 있으면(registry가 낡음) POST 0으로 FAIL — pull 결과는 저장."""
        self.write_cand("새이름1\n새이름2\n")
        self.stamp()
        fake = FakeSender()
        for g in GIDS:
            fake.kws[g]["새이름1"] = f"rk-{g}"
        X._default_sender = fake
        rc, out = self.push("--from-candidates", self.cand, "--expect", "2", "--key-file", self.kf)
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] 고른 이름 중 1개가 방금 읽은(pull) 대상 그룹 전부에 이미 있음: '새이름1'", out)
        self.assertEqual([c[0] for c in fake.calls].count("POST"), 0)                   # 새이름2도 보내지 않는다
        st = {(r["keyword"], r["group_id"]): r["status"] for r in self.registry_rows()}
        self.assertEqual([st[("새이름1", g)] for g in GIDS], ["registered"] * 3)        # pull 결과 저장
        self.assertEqual(self.approved_files(), [])                                     # POST 0이면 승인 파일도 없다(재개 판정이 헷갈리지 않게)
        self.stamp()                                                                    # (pull 결과 저장으로 registry md5가 바뀜)
        self.write_cand("새이름2\n")
        self.stamp()
        X._default_sender = FakeSender(auth_fail=True)                                  # 첫 pull부터 실패 — POST 0
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)
        self.assertEqual(rc, 1, out)
        self.assertIn("POST 전에 멈춤(POST 0 — 승인 파일 안 씀)", out)
        self.assertEqual(self.approved_files(), [])

    def test_post_cut_mid_response_or_unreadable_body_is_result_unknown(self):
        """X1(리뷰 반영): 응답 도중 끊김(http.client.IncompleteRead — OSError 아님)·응답 본문을 못 읽음(JSONDecodeError)도 "요청 결과 모름" —
        그 묶음은 failed, 나머지 그룹도 시도, verify가 실제 상태를 다시 읽고, registry 저장·exit 1(Traceback 아님)."""
        import http.client
        for n, (exc, applied) in enumerate(((http.client.IncompleteRead(b""), False),
                                            (json.JSONDecodeError("Expecting value", "<html>OK</html>", 0), True)), 1):
            self.write_cand(f"새끊김{n}\n")
            self.stamp()
            fake = FakeSender(raise_on_post=exc, apply_then_raise=applied)
            X._default_sender = fake
            rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)
            self.assertEqual(rc, 1, out)
            self.assertIn(f"요청 결과 모름({type(exc).__name__}) — 반영됐을 수 있다, verify로 확인", out)
            self.assertEqual([c[0] for c in fake.calls].count("POST"), 3)               # 나머지 그룹도 시도
            st = {(r["keyword"], r["group_id"]): r["status"] for r in self.registry_rows()}
            self.assertEqual([st[(f"새끊김{n}", g)] for g in GIDS], ["registered" if applied else "failed"] * 3)
        real = self.orig[0]                                                             # 기본 sender: 200인데 JSON이 아닌 본문
        orig_open = X.urllib.request.urlopen
        self.addCleanup(setattr, X.urllib.request, "urlopen", orig_open)

        class Resp:
            status = 200

            def read(self):
                return b"<html>OK</html>"

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False
        X.urllib.request.urlopen = lambda req, timeout=None: Resp()
        with self.assertRaises(X.ApiError) as cm:
            X.NaverApi("K", "S", 1, sender=real).request("POST", "/ncc/restricted-keywords", body=[{"keyword": "새이름"}])
        self.assertIn("요청 결과 모름(JSONDecodeError)", str(cm.exception))

    def test_keep_name_fails(self):
        """X7: registry keep(사용자 결정 '노출 유지') 이름은 참조 모드에서 FAIL."""
        rows = self.registry_rows() + [dict(keyword="유지이름", group_id="", group_name="*", type="EXP_SEARCH", status="keep",
                                            source="ui", registered_at="", restrict_kwd_id="", verified_at="", note="")]
        X.save_registry(self.reg, rows)
        self.reg_md5 = md5f(self.reg)
        self.write_cand("유지이름\n")
        self.stamp()
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--dry-run")
        self.assert_nothing_written(rc, out)
        self.assertIn("[FAIL] 이름 '유지이름' ← ", out)
        self.assertIn("registry에 keep(사용자 결정 '노출 유지')", out)

    def test_api_key_masked_in_error_output_and_registry(self):
        """X10: 서버가 요청 헤더(X-API-KEY)를 되돌려 줘도 출력·registry note에 키 값이 없다(***)."""
        key = "FAKEKEY0928echo"
        write_text(self.kf, json.dumps({"api_key": key, "secret_key": "S3CRETecho"}))
        self.write_cand("새이름1\n")
        self.stamp()
        X._default_sender = FakeSender(echo_key_status=400)
        rc, out = self.push("--from-candidates", self.cand, "--expect", "1", "--key-file", self.kf)
        self.assertEqual(rc, 1, out)
        self.assertIn("X-API-KEY=***", out)
        self.assertNotIn(key, out)
        with open(self.reg, encoding="utf-8-sig") as f:
            self.assertNotIn(key, f.read())
        api = X.NaverApi(key, "S3CRETecho", 1, sender=lambda m, u, h, d: (401, {"message": f"denied {h['X-API-KEY']}"}))
        with self.assertRaises(X.ApiError) as cm:
            api.adgroup(GIDS[0])
        self.assertIn("denied ***", str(cm.exception))
        self.assertNotIn(key, str(cm.exception))
        long_key = "0100000000" + "ab12cd34" * 8                                       # JSON 아닌 오류 본문 500자 경계에 걸친 키 — 가린 뒤에 자른다
        orig_open = X.urllib.request.urlopen
        self.addCleanup(setattr, X.urllib.request, "urlopen", orig_open)

        def raise_400(req, timeout=None):
            raise urllib.error.HTTPError(req.full_url, 400, "bad", {}, io.BytesIO(("x" * 440 + "X-API-KEY: " + long_key).encode()))
        X.urllib.request.urlopen = raise_400
        st, resp = X.NaverApi(long_key, "S3CRETecho", 1, sender=self.orig[0]).request("POST", "/ncc/restricted-keywords", body=[])
        self.assertEqual(st, 400)
        self.assertIn("X-API-KEY: ***", resp["message"])
        self.assertNotIn(long_key[:20], resp["message"])
        self.assertLessEqual(len(resp["message"]), 500)

    def test_load_keys_rejects_values_not_usable_as_header(self):
        """W9: 키 값이 한 줄·ASCII·공백 없음이 아니면 SystemExit — 값은 출력하지 않는다(deploy.usable보다 넓다 — 비밀키엔 +/= 같은 글자가 있을 수 있다)."""
        for bad in ("K Y", "키값", "K\nY"):
            write_text(self.kf, json.dumps({"api_key": bad, "secret_key": "S"}))
            with self.assertRaises(SystemExit) as cm:
                X.load_keys(self.kf)
            self.assertIn("api_key 값 형식이 다릅니다", str(cm.exception))
            self.assertNotIn(bad, str(cm.exception))


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1)
    after = md5f(REAL_REG) if os.path.exists(REAL_REG) else None
    print(f"실제 registry md5 전/후 동일: {REAL_MD5 == after} ({(after or '')[:8]})")
    sys.exit(0 if r.result.wasSuccessful() and REAL_MD5 == after else 1)
