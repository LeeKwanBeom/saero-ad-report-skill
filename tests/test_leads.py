#!/usr/bin/env python3
"""주간 성과 장부(설계안 A — 매출 작업, 2026-10-10) 시험 — scripts/leads.py · compute.py leads_card · validate.py 새 검사 25·26 · compare "12 장부·플레이스" ·
narrative_check(같은 주 이틀 연속 회차).

임시 폴더의 스크래치 장부·합성 합본(키워드.csv 일별만)·임시 git 저장소만 쓴다 — 실제 ~/saero-leads·운영 작업 폴더·네트워크에 닿지 않는다(SAERO_LEADS 를 늘 임시 경로로).
- 주(A-F8): add 는 --week 를 받지 않고 합본 집계 끝 기준 다 찬 주만 · 월요일 01~09시(합본이 아직 토요일까지)면 그 전 주 · 정정 --replace --week 는 월요일·≤ 집계 끝·장부에 있는 주만.
- 입력 검사(완료 기준 10): 숫자 아님·음수·소수·상한 초과·모순 셋 → [FAIL] 쓰기 0 · 장부 칸에 글자 칸 없음.
- 덮어쓰기 0(11): 줄 추가만(앞 바이트 그대로) · 같은 주 FAIL · 정정은 .bak-<시각>(옛 바이트 그대로) · dry-run 파일 쓰기 0(2).
- skip(A-F6 · 23): 숫자 없는 줄 · status 는 skip 이 있으면 묻지 않음 · 판정에서 skip 주 = 미입력(구멍)(0 으로 더하지 않음).
- 판정(9): 8주 미만 판정 전(N/8주) · 구멍 · 직전 0 비교 불가 · 포아송 2σ 경계(12 대 4 = 구별 안 됨, 13 대 4 = 좋아짐) · 장부 없음·꼴 다름 확인 못 함(12).
- 공개 범위(7): compute 성과장부에 건수 0 · publish ≠ verdict FAIL · guard(현실 값 초안·커밋 메시지 FAIL, 기록 꼴 PASS, 장부 파일 staged FAIL, 최근 매출 값 FAIL) ·
  validate "장부 라벨+숫자 0" — 제외 검색어 문구('등록 31개' 등)는 PASS.
- compare(8): 12번 판정 낱말 ≠ compute → DIFF · 같으면 OK. narrative(6): 같은 주 이틀 연속 회차의 장부 행은 'M/D까지' 가 달라 PASS.
실행: "$PY" tests/test_leads.py
"""
import contextlib
import datetime as dt
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import leads as L  # noqa: E402
import narrative_check as N  # noqa: E402
from reportlib import load_config  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

LEADS = os.path.join(ROOT, "scripts", "leads.py")
CFG = load_config()
FORBIDDEN = ["필요", "시점", "할 것", "검토", "주째"]          # validate.py 와 같은 목록(report-structure.md 11번)
RESIDUAL = ["확인 요청", "판단 요청", "기다림", "확인 중", "대기"]


def md5(p):
    return hashlib.md5(rb(p)).hexdigest()


def rb(p):
    with open(p, "rb") as f:
        return f.read()


def rt(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def combined(td, end):
    """합성 합본 — 키워드.csv 의 일별만(집계 끝 = end)."""
    d = os.path.join(td, "combined")
    os.makedirs(d, exist_ok=True)
    days = [end - dt.timedelta(days=i) for i in range(3)]
    with open(os.path.join(d, "키워드.csv"), "w", encoding="utf-8") as f:
        f.write("필라테스 보고서(2026.08.01.~2026.10.31.),2580077\n일별,노출수\n")
        for x in days:
            f.write(f"{x:%Y.%m.%d}.,1\n")
    return d


def run(args, ledger, comb=None, extra_env=None):
    env = dict(os.environ, SAERO_LEADS=ledger, PYTHONUTF8="1")
    env.update(extra_env or {})
    cmd = [sys.executable, LEADS] + args + (["--combined", comb] if comb else [])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def ledger_text(rows):
    """rows = [(월요일 date, 'ok'|'skip', signup)] — 다른 칸은 맞는 값으로."""
    out = [L.HEADER_LINE]
    for w, st, s in rows:
        nums = {k: None for k in L.FIELDS}
        if st == "ok":
            nums.update(inquiry=s + 2, trial=s, signup=s, naver=0)
        out.append(L.row_line(w, st, nums, dt.datetime(2026, 10, 10, 12, 0, tzinfo=L.KST)).rstrip("\n"))
    return "\n".join(out) + "\n"


MON = dt.date(2026, 10, 5)  # 10/5(월)


def weeks_back(n, last=MON):
    return [last - dt.timedelta(weeks=i) for i in range(n)][::-1]


class Weeks(unittest.TestCase):
    def test_last_full_week(self):
        self.assertEqual(L.last_full_week(dt.date(2026, 10, 11)), dt.date(2026, 10, 5))   # 일요일까지 → 그 주
        self.assertEqual(L.last_full_week(dt.date(2026, 10, 10)), dt.date(2026, 9, 28))   # 토요일까지 → 그 전 주
        self.assertEqual(L.last_full_week(dt.date(2026, 10, 12)), dt.date(2026, 10, 5))   # 월요일까지 → 지난 월~일
        self.assertEqual(L.last_full_week(dt.date(2026, 10, 4)), dt.date(2026, 9, 28))
        self.assertEqual(L.week_label(dt.date(2026, 10, 5)), "10/5(월)~10/11(일)")

    def test_monday_morning_boundary_uses_combined_not_clock(self):
        """월요일 01~09시 KST: 합본이 일요일까지면 그 주, 아직 토요일까지(수집 전·2-1 같음)면 그 전 주 — 벽시계가 아니라 집계 끝."""
        td = tempfile.mkdtemp()
        try:
            led = os.path.join(td, "l.csv")
            rc, out = run(["status"], led, combined(os.path.join(td, "a"), dt.date(2026, 10, 11)))
            self.assertIn("week=2026-10-05", out)
            rc, out = run(["status"], led, combined(os.path.join(td, "b"), dt.date(2026, 10, 10)))
            self.assertIn("week=2026-09-28", out)
        finally:
            shutil.rmtree(td, ignore_errors=True)


class AddSkip(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()
        self.led = os.path.join(self.td, "sub", "leads.csv")
        self.comb = combined(self.td, dt.date(2026, 10, 11))

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def add(self, *kv, extra=()):
        args = ["add"]
        for k, v in zip(("--inquiry", "--trial", "--signup", "--naver"), kv):
            args += [k, str(v)]
        return run(args + list(extra), self.led, self.comb)

    def test_dry_run_writes_nothing(self):
        rc, out = self.add(3, 2, 1, 1, extra=["--dry-run"])
        self.assertEqual(rc, 0, out)
        self.assertIn("파일 쓰기 0", out)
        self.assertFalse(os.path.exists(self.led))
        self.assertEqual(self.add(3, 2, 1, 1)[0], 0)
        h = md5(self.led)
        rc, out = run(["skip", "--dry-run"], self.led, self.comb)          # 같은 주라 FAIL — 그래도 쓰기 0
        self.assertEqual(md5(self.led), h)

    def test_append_only_and_same_week_fail(self):
        rc, out = self.add(3, 2, 1, 1)
        self.assertEqual(rc, 0, out)
        with open(self.led, encoding="utf-8") as f:
            text = f.read()
        self.assertTrue(text.startswith(L.HEADER_LINE + "\n2026-10-05,ok,3,2,1,1,,,,,,"), text)
        before = rb(self.led)
        rc, out = self.add(5, 4, 2, 2)
        self.assertEqual(rc, 1)
        self.assertIn("같은 주", out)
        self.assertEqual(rb(self.led), before)               # 덮어쓰기 0
        rc, out = run(["skip"], self.led, self.comb)
        self.assertEqual(rc, 1)
        self.assertIn("같은 주", out)
        # 다음 주(합본 집계 끝이 한 주 뒤) — 줄 추가만, 앞 바이트 그대로
        comb2 = combined(os.path.join(self.td, "n"), dt.date(2026, 10, 18))
        rc, out = run(["skip"], self.led, comb2)
        self.assertEqual(rc, 0, out)
        after = rb(self.led)
        self.assertTrue(after.startswith(before))
        self.assertRegex(after[len(before):].decode(), r"^2026-10-12,skip,,,,,,,,,,2026-")

    def test_week_only_with_replace(self):
        rc, out = self.add(3, 2, 1, 1, extra=["--week", "2026-09-28"])
        self.assertEqual(rc, 2)
        self.assertIn("--replace", out)
        self.assertFalse(os.path.exists(self.led))

    def test_replace_backup_and_checks(self):
        self.assertEqual(self.add(3, 2, 1, 1)[0], 0)
        old = rb(self.led)
        for wk, frag in (("2026-10-06", "월요일이 아님"), ("2026-10-12", "다 찬 주만"), ("2026-09-28", "장부에 없음")):
            with self.subTest(wk=wk):
                rc, out = self.add(4, 2, 2, 1, extra=["--replace", "--week", wk])
                self.assertEqual(rc, 1, out)
                self.assertIn(frag, out)
                self.assertEqual(rb(self.led), old)
        self.assertEqual(glob.glob(self.led + ".bak-*"), [])
        rc, out = self.add(4, 2, 2, 1, extra=["--replace", "--week", "2026-10-05", "--dry-run"])
        self.assertEqual((rc, rb(self.led)), (0, old))
        rc, out = self.add(4, 2, 2, 1, extra=["--replace", "--week", "2026-10-05"])
        self.assertEqual(rc, 0, out)
        baks = glob.glob(self.led + ".bak-*")
        self.assertEqual(len(baks), 1)
        self.assertEqual(rb(baks[0]), old)                  # 옛 바이트 그대로
        self.assertIn("2026-10-05,ok,4,2,2,1,", rt(self.led))

    def test_input_checks(self):
        cap = CFG["leads"]["max_per_week"]["signup"]
        bad = (("글자", ("3", "2", "한명", "1"), "10진 숫자"), ("음수", ("3", "2", "-1", "0"), "10진 숫자"), ("소수", ("3", "2", "1.5", "1"), "10진 숫자"),
               ("상한 초과", ("200", "100", str(cap + 1), "0"), "상한"), ("체험 > 문의", ("2", "3", "1", "0"), "모순"),
               ("등록 > 문의 + 체험", ("1", "1", "3", "0"), "모순"), ("네이버 경유 > 등록", ("3", "2", "1", "2"), "모순"))
        for label, kv, frag in bad:
            with self.subTest(label=label):
                rc, out = self.add(*kv)
                self.assertEqual(rc, 1, out)
                self.assertIn(frag, out)
                self.assertIn("쓰기 0", out)
                self.assertFalse(os.path.exists(self.led))
        rc, out = self.add("200", "100", str(cap), "0", extra=["--revenue", str(CFG["leads"]["max_per_week"]["revenue"] + 1)])
        self.assertEqual(rc, 1)
        self.assertIn("매출", out)
        rc, out = self.add("200", "100", str(cap), "0", extra=["--dry-run"])                 # 상한 그대로는 통과
        self.assertEqual(rc, 0, out)
        rc, out = run(["add", "--inquiry", "3", "--trial", "2", "--signup", "1"], self.led, self.comb)   # 필수 칸 빠짐
        self.assertEqual(rc, 1)
        self.assertIn("필수", out)
        # 장부 칸 = 숫자 칸만 — 글자 칸이 없다
        self.assertEqual(L.HEADER, ["week", "status", "inquiry", "trial", "signup", "naver", "revenue", "place_visit", "call", "direction", "save", "entered_at"])

    def test_status_skip_not_asked_and_broken_ledger(self):
        rc, out = run(["status"], self.led, self.comb)
        self.assertIn("ask5=yes", out)
        self.assertIn("(5) 질문: 지난주 10/5(월)~10/11(일): 새 문의", out)
        self.assertEqual(run(["skip"], self.led, self.comb)[0], 0)
        rc, out = run(["status"], self.led, self.comb)
        self.assertIn("ask5=no", out)
        self.assertIn("건너뜀", out)
        with open(self.led, "a", encoding="utf-8") as f:
            f.write("2026-10-12,ok,메모,,,,,,,,,2026-10-10T00:00:00+09:00\n")       # 손으로 고친 글자 칸
        before = rb(self.led)
        rc, out = run(["status"], self.led, self.comb)
        self.assertEqual(rc, 0)
        self.assertIn("[주의] 꼴 다름", out)
        self.assertIn("verdict=확인 못 함", out)
        rc, out = self.add(3, 2, 1, 1)
        self.assertEqual(rc, 1)
        self.assertEqual(rb(self.led), before)


class Verdict(unittest.TestCase):
    def v(self, rows, end=dt.date(2026, 10, 11)):
        return L.verdict(L.parse_ledger(ledger_text(rows)), end, CFG)[0]

    def test_rules(self):
        w8 = weeks_back(8)
        self.assertEqual(L.verdict(None, dt.date(2026, 10, 11), CFG)[0], "확인 못 함")
        self.assertEqual(self.v([(w8[-1], "ok", 1)]), "판정 전(1/8주)")
        self.assertEqual(self.v([(w, "ok", 1) for w in w8[1:]]), "판정 전(7/8주)")
        self.assertEqual(self.v([(w, "ok", 1) for w in weeks_back(9)[:-1]]), "미입력(구멍)")          # 8줄이지만 지난주가 없음
        self.assertEqual(self.v([(w, "ok", 1) for w in weeks_back(9) if w != weeks_back(9)[4]]), "미입력(구멍)")
        # 건너뜀 주 = 구멍(0 으로 더하면 직전 4주 합이 줄어 '나빠짐'이 될 자리)
        rows = [(w, "ok", 6 if i < 4 else 1) for i, w in enumerate(w8)]
        self.assertEqual(self.v(rows), "나빠짐")                                    # 직전 24 대 최근 4
        rows[5] = (w8[5], "skip", 0)
        self.assertEqual(self.v(rows), "미입력(구멍)")
        self.assertEqual(self.v([(w, "ok", 0 if i < 4 else 3) for i, w in enumerate(w8)]), "비교 불가")   # 직전 합 0
        # 포아송 2σ 경계 — 최근 12 대 직전 4: 차이 8 = 2√16 → 구별 안 됨 / 13 대 4: 9 > 2√17 → 좋아짐 / 4 대 13 → 나빠짐
        def split(recent, prev):
            r = [prev // 4 + (1 if i < prev % 4 else 0) for i in range(4)] + [recent // 4 + (1 if i < recent % 4 else 0) for i in range(4)]
            return [(w, "ok", s) for w, s in zip(w8, r)]
        self.assertEqual(self.v(split(12, 4)), "구별 안 됨")
        self.assertEqual(self.v(split(13, 4)), "좋아짐")
        self.assertEqual(self.v(split(4, 13)), "나빠짐")
        self.assertEqual(self.v(split(6, 5)), "구별 안 됨")
        # 집계 끝 뒤의 주는 세지 않는다(다 찬 주만)
        self.assertEqual(self.v([(w8[-1], "ok", 1)], end=dt.date(2026, 10, 10)), "판정 전(0/8주)")

    def test_words_safe_for_report(self):
        words, before, mn = L.verdict_words_all(CFG)
        allw = words + [f"{before}({n}/{mn}주)" for n in range(mn)] + list(CFG["place_checklist"]["verdict_words"].values()) \
            + list(CFG["place_checklist"]["state_words"].values())
        for w in allw:
            for bad in FORBIDDEN + RESIDUAL:
                self.assertNotIn(bad, w, w)


class Public(unittest.TestCase):
    def test_compute_card_has_no_counts(self):
        import compute as C
        td = tempfile.mkdtemp()
        try:
            led = os.path.join(td, "l.csv")
            with open(led, "w", encoding="utf-8", newline="") as f:
                f.write(L.HEADER_LINE + "\n" + L.row_line(MON, "ok", {"inquiry": 7, "trial": 5, "signup": 3, "naver": 2, "revenue": 1200000,
                                                                       "place_visit": 345, "call": 6, "direction": 8, "save": 9},
                                                          dt.datetime(2026, 10, 12, 1, 0, tzinfo=L.KST)))
            g = C.leads_card(led, dt.date(2026, 10, 11), CFG)
            self.assertEqual(set(g), {"판정", "기준", "상태", "입력주수", "창주", "최소주"})
            self.assertEqual((g["판정"], g["기준"], g["상태"], g["입력주수"]), ("판정 전(1/8주)", "10/11까지", "ok", 1))
            text = json.dumps(g, ensure_ascii=False)
            for v in ("1200000", "1,200,000", "345"):
                self.assertNotIn(v, text)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                g = C.leads_card(os.path.join(td, "없음.csv"), dt.date(2026, 10, 11), CFG)
            self.assertEqual((g["판정"], g["상태"]), ("확인 못 함", "장부 없음"))
            self.assertIn("[주의]", err.getvalue())
            bad = json.loads(json.dumps(CFG))
            bad["leads"]["publish"] = "counts"
            with self.assertRaises(C.LeadsPublishError):
                C.leads_card(led, dt.date(2026, 10, 11), bad)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def test_label_hits(self):
        labs = CFG["leads"]["public_labels"]
        leak = ["(5) 답: 문의 3 · 체험 2 · 등록 1 · 네이버 경유 1 · 매출 1,200,000", "사장님 답 '등록 1명, 매출 120만'",
                "사용자에게 요청한 값: 승인 묶음 (4) · (5) 등록 1", "제외 검색어 등록 31개 · 장부 등록 2명", "상담 4건", "문의: 3"]
        for s in leak:
            with self.subTest(s=s):
                self.assertTrue(L.label_hits(s, labs), s)
        ok = ["10/10 등록 31개 · 확인 93/93 · 실패 0(10/11부터 판정) · 10/9 등록 44개는 10/10부터 판정",
              "제외 검색어: 10/10 등록 31개 · 확인 93/93 · 실패 0", "후보 33 − 뺌 2 → 승인 31 → 등록 31 · verified 31(93/93) · 실패 0",
              "제외 검색어(5-0단계): 재노출 판정 0건 / 후보 0 → 등록 0 / registry 968행(변경 없음)", "등록 승인 31개", "(9/18 등록, 23일차)",
              "9/2 등록 · 9/17 OFF", "톡톡상담 2026-06-04", "(5) 장부 입력됨(로컬)", "성과 장부(광고비 → 문의 → 등록) — 10/9까지 장부 기준 판정 = 판정 전(1/8주)",
              "'노원필라테스체험' 8회"]
        for s in ok:
            with self.subTest(s=s):
                self.assertEqual(L.label_hits(s, labs), [], s)

    def test_rows_safe(self):
        R = {"성과장부": {"판정": "판정 전(1/8주)", "기준": "10/9까지", "상태": "ok", "입력주수": 1, "창주": 4, "최소주": 8}}
        h = L.row_html(R)
        t = re.sub(r"<[^>]+>", "", h)
        self.assertEqual(L.label_hits(t, CFG["leads"]["public_labels"]), [])
        for bad in FORBIDDEN + RESIDUAL:
            self.assertNotIn(bad, t)
        self.assertIn("10/9까지 장부 기준 판정 = 판정 전(1/8주)</b>", h)


def git(cwd, *a):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.path.join(cwd, "..", "gitcfg"), GIT_CEILING_DIRECTORIES=os.path.dirname(cwd))
    r = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"] + list(a), cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout


class Guard(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()
        open(os.path.join(self.td, "gitcfg"), "w").close()
        self.repo = os.path.join(self.td, "repo")
        os.makedirs(os.path.join(self.repo, "audit"))
        with open(os.path.join(self.repo, "audit", "last-audit.md"), "w", encoding="utf-8") as f:
            f.write("# 기록\n")
        git(self.repo, "init", "-q")
        git(self.repo, "add", "audit/last-audit.md")
        git(self.repo, "commit", "-qm", "init")
        self.led = os.path.join(self.td, "leads.csv")
        with open(self.led, "w", encoding="utf-8", newline="") as f:
            f.write(L.HEADER_LINE + "\n" + L.row_line(MON, "ok", {"inquiry": 3, "trial": 2, "signup": 1, "naver": 1, "revenue": 1200000},
                                                      dt.datetime(2026, 10, 12, 1, 0, tzinfo=L.KST)))

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def stage(self, rel, text, mode="a"):
        p = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, mode, encoding="utf-8", newline="") as f:
            f.write(text)
        git(self.repo, "add", rel)

    def guard(self, msg=None):
        args = ["guard", "--staged", "--repo", self.repo, "--ledger", self.led]
        if msg is not None:
            mf = os.path.join(self.td, "msg.txt")
            with open(mf, "w", encoding="utf-8") as f:
                f.write(msg)
            args += ["--message-file", mf]
        return run(args, self.led)

    def test_record_form_passes(self):
        here = rt(os.path.join(ROOT, "audit", "last-audit.md"))
        a = here.index("## 갱신 회차 (2026-10-10 02:19")
        sect = here[a:here.index("\n---\n", a)]                          # 브랜치 last-audit 10/10 갱신 회차 절 그대로
        self.stage("audit/last-audit.md", "\n" + sect + "\n사용자에게 요청한 값: 승인 묶음 (4) · (5) 장부 입력됨(로컬)\n")
        rc, out = self.guard("audit: 2026-10-10 갱신 회차 — 배포 59c5313 · (5) 장부 입력됨(로컬)")
        self.assertEqual(rc, 0, out)
        self.assertIn("[PASS] guard", out)

    def test_realistic_draft_fails(self):
        self.stage("audit/last-audit.md", "\n사용자 답 해석: (5) 답 \"문의 3 · 체험 2 · 등록 1 · 네이버 1 · 매출 1,200,000\" 그대로 장부에\n")
        rc, out = self.guard("audit: 갱신 회차")
        self.assertEqual(rc, 1, out)
        self.assertIn("장부 라벨+숫자", out)
        self.assertIn("최근 매출 값", out)

    def test_message_and_value_only(self):
        self.stage("audit/last-audit.md", "\n이번 주 1,200,000\n")              # 라벨 없이 값만 — 장부 최근 매출과 같은 숫자
        rc, out = self.guard()
        self.assertEqual(rc, 1, out)
        git(self.repo, "reset", "-q")
        self.stage("audit/last-audit.md", "\n평범한 기록\n", mode="w")
        rc, out = self.guard("audit: 장부 등록 1명 · 120만")
        self.assertEqual(rc, 1, out)
        self.assertIn("커밋 메시지", out)

    def test_ledger_file_staged_fails_and_scope(self):
        self.stage("audit/leads.csv", rt(self.led), mode="w")
        rc, out = self.guard()
        self.assertEqual(rc, 1, out)
        self.assertIn("장부 머리줄", out)
        git(self.repo, "reset", "-q")
        self.stage("tests/test_x.py", "s = '문의 3 · 등록 1'\n", mode="w")      # 시험·스크립트는 범위 밖
        rc, out = self.guard()
        self.assertEqual(rc, 0, out)


class ConfigOnly(unittest.TestCase):
    """완료 기준 3 — 새 값은 config leads·place_checklist 에만: 새 코드(leads.py·place.py 전부 · compute leads_card·place_effect · validate 새 검사 둘)의
    숫자 토큰(주석·문자열 뺌 — tokenize)에 config 의 선택 값(창·최소 주·자리 수·일수·띠·상한·하한·12번 상한)이 없다. 7(요일)·100(백분율)·10000(수 단위 '만')·0·1·2(포아송 2σ·반복)는 구조 상수."""

    def test_no_config_values_in_new_code(self):
        import inspect
        import tokenize
        import compute
        sys.argv = ["validate.py"]
        import validate
        lc, pc = CFG["leads"], CFG["place_checklist"]
        vals = {lc["window_weeks"], lc["min_weeks"], lc["guard_value_min"], pc["window_days"], pc["chat_after_days"], pc["max_open_rows_12"],
                pc["final_show_days"], *pc["band_pct"]["clicks"], *pc["band_pct"]["ctr"], *lc["max_per_week"].values()}
        vals = {abs(int(v)) for v in vals} - {0, 1, 2, 7, 100, 10000}   # 10000 = 수 단위 '만'(leads.value_forms) — 길찾기·저장 상한과 숫자만 같다
        srcs = {"leads.py": rt(os.path.join(ROOT, "scripts", "leads.py")), "place.py": rt(os.path.join(ROOT, "scripts", "place.py"))}
        for name, fn in (("compute.leads_card", compute.leads_card), ("compute.place_effect", compute.place_effect),
                         ("validate.check_leads_public", validate.check_leads_public), ("validate.check_12_growth", validate.check_12_growth)):
            srcs[name] = inspect.getsource(fn)
        for name, src in srcs.items():
            nums = {int(t.string) for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type == tokenize.NUMBER and t.string.isdigit()}
            with self.subTest(name=name):
                self.assertEqual(sorted(nums & vals), [], f"{name} 에 config 값 숫자 {sorted(nums & vals)}")


class ValidateCompareNarrative(unittest.TestCase):
    def page(self, end_md, verdict, place_rows=(), extra12="", period="2026.08.26 — 10.13 (49일)"):
        rows = [f'<tr><td><span class="tag tag-mint">1</span></td><td><!-- n:12-1:매회차 --><span class="tag tag-mint">상시</span> '
                f'<b>제외 검색어 정기 점검 — 10/10 등록 31개 · 확인 93/93 · 실패 0</b><!-- /n --></td></tr>',
                f'<tr><td><span class="tag tag-mint">2</span></td><td><!-- n:12-2:매회차 -->'
                + L.row_html({"성과장부": {"판정": verdict, "기준": f"{end_md}까지", "상태": "ok", "입력주수": 1, "창주": 4, "최소주": 8}})
                + "<!-- /n --></td></tr>"]
        for i, h in enumerate(place_rows, 3):
            rows.append(f'<tr><td><span class="tag tag-mint">{i}</span></td><td><!-- n:12-{i}:매회차 -->{h}<!-- /n --></td></tr>')
        return (f'<div>집계 기간<b>{period}</b></div>\n<!-- Section 1: x -->\n<div class="section-desc">01 글</div>\n<!-- Section 2: x -->\n'
                f'<!-- Section 11: x -->\n<ul><li>관찰</li></ul>\n<!-- Section 12: x -->\n<table><tbody>\n' + "\n".join(rows)
                + f"\n</tbody></table>\n<div class=\"note\">{extra12}</div>\n<script>\nconst x = 1;\n</script>")

    def test_validate_checks(self):
        sys.argv = ["validate.py"]
        import validate as V
        dmax = dt.datetime(2026, 10, 13)
        V.results.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            V.check_leads_public(self.page("10/13", "판정 전(1/8주)"))
            V.check_12_growth(self.page("10/13", "판정 전(1/8주)"), dmax)
            V.check_leads_public(self.page("10/13", "판정 전(1/8주)", extra12="· 장부: 등록 1명"))
            V.check_12_growth(self.page("10/12", "판정 전(1/8주)"), dmax)                 # M/D까지 ≠ 집계 끝
            V.check_12_growth(self.page("10/13", "좋아질 듯"), dmax)                    # 낱말 밖
            x = '<span class="tag tag-mint">화면 손보기</span> <b>플레이스 P{} 문구 — 10/13까지 상태 = ✗</b>'
            V.check_12_growth(self.page("10/13", "구별 안 됨", [x.format(1), x.format(2), x.format(3)]), dmax)   # ✗ 3 > items_in_12 2
            V.check_12_growth(self.page("10/13", "구별 안 됨", [x.format(i) for i in (1, 2)] + ["<b>기타</b>"] * 4), dmax)   # ✓ 아닌 행 8 > 7
            V.check_12_growth(self.page("10/13", "구별 안 됨", [x.format(1), x.format(2)]), dmax)
        got = [ok for _, ok, _ in V.results]
        self.assertEqual(got, [True, True, False, False, False, False, False, True], V.results)

    def test_compare_diff_on_stale_verdict(self):
        td = tempfile.mkdtemp()
        try:
            h, j = os.path.join(td, "i.html"), os.path.join(td, "c.json")
            with open(h, "w", encoding="utf-8") as f:
                f.write(self.page("10/13", "판정 전(2/8주)"))
            for want, diff in (("판정 전(2/8주)", False), ("판정 전(3/8주)", True)):
                with open(j, "w", encoding="utf-8") as f:
                    json.dump({"성과장부": {"판정": want}, "플레이스전후": {"12번": []}}, f, ensure_ascii=False)
                r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "compare.py"), h, j], capture_output=True, text=True, encoding="utf-8")
                line = [x for x in r.stdout.splitlines() if "12 장부 기준 판정" in x and x.startswith("  [")]
                self.assertEqual(len(line), 1, r.stdout[-500:])
                self.assertEqual("[DIFF]" in line[0], diff, line[0])
                self.assertEqual("[OK]" in [x for x in r.stdout.splitlines() if "12 플레이스 행" in x and x.startswith("  [")][0], True)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def test_narrative_same_week_two_days(self):
        """같은 주 화·수 회차 — 장부 판정·주가 같아도 'M/D까지'(합본 마지막 날)가 달라 서술 미교체 FAIL 이 나지 않는다. 같은 글이면 FAIL."""
        a = self.page("10/13", "판정 전(1/8주)", period="2026.08.26 — 10.13 (49일)")
        b = self.page("10/14", "판정 전(1/8주)", period="2026.08.26 — 10.14 (50일)")
        # 12-1 은 이 시험 밖 — 회차마다 다시 쓰는 글이라 바꿔 둔다
        b = b.replace("10/10 등록 31개", "10/11 등록 5개")
        rc, out = N.check(b, a)
        self.assertEqual(rc, 0, out)
        stale = b.replace("10/14까지 장부 기준", "10/13까지 장부 기준")
        rc, out = N.check(stale, a)
        self.assertEqual(rc, 1)
        self.assertIn("12-2", "\n".join(out))


if __name__ == "__main__":
    unittest.main(verbosity=1)
