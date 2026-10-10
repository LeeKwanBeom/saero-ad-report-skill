#!/usr/bin/env python3
"""플레이스 화면·소재 손보기(설계안 C — 매출 작업, 2026-10-10) 시험 — scripts/place.py · compute.py place_effect · compare "12 플레이스 행".

임시 폴더 스크래치 체크리스트·합성 키워드 표만 쓴다(SAERO_PLACE 를 늘 임시 경로로 — 저장소 audit/place-checklist.csv 를 만들지 않는다). 네트워크 0.
- 쓰기 규칙(11·25): 첫 set 은 P1~P9 전부 · id·상태 밖 · 바꾼 날 미래 · 다시 볼 날 오늘 이하 · 같은 상태 · 바꾼 날이 지금 기록보다 앞 → [FAIL] 쓰기 0 ·
  줄 추가만(앞 바이트 그대로) · dry-run 파일 쓰기 0 · 상태 넷(✓ ✗ 안 함 미룸) · in12_since(✗ 행 = todo 중 config 순서 위 items_in_12 개, 빠지면 다음 todo 가 그날로).
- 효과 판정(26 · C-1·C-2 — 손으로 센 기대값과 대조 = 독립 계산): 플레이스 **검색 지면만**(콘텐츠 행·파워링크 행 뺌) · **달력 일수** 분모(행 빠진 날 0) ·
  둘 다 띠 위 좋아짐 / 둘 다 아래 나빠짐 / 하나만 밖 구별 안 됨 · 앞뒤 14일 안 다른 바꿈 = 겹침(한 번에 한 항목) · 자료 부족 = 비교 불가 · 덜 찬 창 = 측정 중(n/14일).
- 12번 목록(13): ✗ 행 ≤ items_in_12 · 판정 뒤 final_show_days 일까지 남기고 빠지는 회차에 "빠짐" · 안 함·미룸은 12번·3주 셈 밖, 지난 배포본 뒤에 적힌 것만
  이월 줄에 한 번 · ✗ 가 chat_after_days 일 넘게 그대로면 채팅 질문 신호 · 미룸 다시 볼 날 지나면 채팅 질문 신호.
- compare: 12번 플레이스 행(id·상태/판정) ≠ compute → DIFF.
실행: "$PY" tests/test_place.py
"""
import contextlib
import datetime as dt
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import compute as C  # noqa: E402
import place as P  # noqa: E402
from reportlib import load_config  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

PLACE = os.path.join(ROOT, "scripts", "place.py")
CFG = load_config()
PC = CFG["place_checklist"]
ALL9 = ["P1=done", "P2=todo", "P3=todo", "P4=done", "P5=no", "P6=later:2026-11-01", "P7=todo", "P8=done", "P9=done"]


def rb(p):
    with open(p, "rb") as f:
        return f.read()


def run(args, path, today="2026-10-12"):
    env = dict(os.environ, SAERO_PLACE=path, PYTHONUTF8="1")
    extra = ["--today", today] if args and args[0] in ("set", "done") else []
    r = subprocess.run([sys.executable, PLACE] + args + extra, capture_output=True, text=True, encoding="utf-8", env=env, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


class Write(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()
        self.p = os.path.join(self.td, "audit", "place-checklist.csv")

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def test_first_set_rules_and_dry_run(self):
        rc, out = run(["set", "P1=done", "P2=todo"], self.p)
        self.assertEqual(rc, 1)
        self.assertIn("첫 set 은 P1~P9 전부", out)
        rc, out = run(["done", "P2", "--date", "2026-10-10"], self.p)
        self.assertEqual(rc, 1)
        self.assertIn("아직 없음", out)
        rc, out = run(["set"] + ALL9 + ["--dry-run"], self.p)
        self.assertEqual(rc, 0, out)
        self.assertFalse(os.path.exists(self.p))
        rc, out = run(["set"] + ALL9, self.p)
        self.assertEqual(rc, 0, out)
        rows = P.parse_checklist(rb(self.p).decode())
        cur = P.current(rows)
        self.assertEqual({i: r["state"] for i, r in cur.items()},
                         {"P1": "done", "P2": "todo", "P3": "todo", "P4": "done", "P5": "no", "P6": "later", "P7": "todo", "P8": "done", "P9": "done"})
        self.assertEqual(P.in12_ids(cur, CFG), ["P2", "P3"])                       # todo 중 config 순서 위 items_in_12(2)
        self.assertEqual((cur["P2"]["in12_since"], cur["P7"]["in12_since"]), (dt.date(2026, 10, 12), None))
        self.assertEqual((cur["P5"]["state_date"], cur["P6"]["revisit"]), (dt.date(2026, 10, 12), dt.date(2026, 11, 1)))
        h = hashlib.md5(rb(self.p)).hexdigest()
        rc, out = run(["done", "P2", "--date", "2026-10-11", "--dry-run"], self.p)
        self.assertEqual((rc, hashlib.md5(rb(self.p)).hexdigest()), (0, h))

    def test_write_guards_and_append_only(self):
        self.assertEqual(run(["set"] + ALL9, self.p)[0], 0)
        before = rb(self.p)
        bad = ((["set", "P10=todo"], "config"), (["set", "PX=todo"], "P<n>=done"), (["set", "P1=gone"], "P<n>=done"),
               (["done", "P2", "--date", "2026-10-13"], "미래"), (["done", "P2", "--date", "2026-08-01"], "개업일"),
               (["set", "P6=later:2026-10-12"], "오늘"), (["set", "P2=todo"], "같은 상태"), (["set", "P5=no"], "같은 상태"),
               (["set", "P6=later:2026-11-01"], "같은 상태"), (["set", "P2=no:2026-10-01"], "날짜를 붙이지"), (["done", "P2", "--date", "10/11"], "YYYY"))
        for args, frag in bad:
            with self.subTest(args=args):
                rc, out = run(args, self.p)
                self.assertNotEqual(rc, 0, out)
                self.assertIn(frag, out)
                self.assertEqual(rb(self.p), before)
        rc, out = run(["done", "P2", "--date", "2026-10-11"], self.p)
        self.assertEqual(rc, 0, out)
        after = rb(self.p)
        self.assertTrue(after.startswith(before))                                 # 줄 추가만
        cur = P.current(P.parse_checklist(after.decode()))
        self.assertEqual(P.in12_ids(cur, CFG), ["P3", "P7"])                      # P2 가 빠지자 P7 이 그날로
        self.assertEqual(cur["P7"]["in12_since"], dt.date(2026, 10, 12))
        self.assertEqual(cur["P3"]["in12_since"], dt.date(2026, 10, 12))         # 계속 있던 P3 는 그대로(새 줄 없음)
        self.assertEqual(sum(1 for r in P.parse_checklist(after.decode()) if r["id"] == "P3"), 1)
        for args, frag in ((["done", "P2", "--date", "2026-10-10"], "앞이거나 같음"), (["done", "P2", "--date", "2026-10-11"], "앞이거나 같음"),
                           (["set", "P2=done"], "이미")):
            with self.subTest(args=args):
                rc, out = run(args, self.p)
                self.assertEqual(rc, 1, out)
                self.assertIn(frag, out)
        self.assertEqual(run(["done", "P2", "--date", "2026-10-12"], self.p)[0], 0)   # 다시 바꾼 날(뒤)은 된다
        self.assertEqual(run(["set", "P6=todo"], self.p)[0], 0)                      # 미룸 → ✗: config 순서가 P7 보다 앞이라 12번 자리를 받는다
        rows = P.parse_checklist(rb(self.p).decode())
        cur = P.current(rows)
        self.assertEqual((cur["P6"]["state"], cur["P6"]["in12_since"]), ("todo", dt.date(2026, 10, 12)))
        self.assertEqual((cur["P7"]["state"], cur["P7"]["in12_since"]), ("todo", None))   # 밀린 P7 은 in12_since 빈 줄이 덧붙음
        self.assertEqual(P.in12_ids(cur, CFG), ["P3", "P6"])

    def test_broken_file_no_write(self):
        self.assertEqual(run(["set"] + ALL9, self.p)[0], 0)
        with open(self.p, "a", encoding="utf-8") as f:
            f.write("2026-10-12,P2,done,2026-10-11,,메모\n")
        before = rb(self.p)
        rc, out = run(["done", "P3", "--date", "2026-10-11"], self.p)
        self.assertEqual(rc, 1)
        self.assertIn("꼴 다름", out)
        self.assertEqual(rb(self.p), before)


# ------------------------------------------------------------- 효과 판정(합성 표 — 손으로 센 기대값)
def frame(rows):
    return pd.DataFrame([{"일별": f"{d:%Y.%m.%d}.", "캠페인": c, "검색/콘텐츠 매체": m, "노출수": i, "클릭수": k} for d, c, m, i, k in rows])


D0 = dt.date(2026, 9, 1)


def series(start, n, imp, clk, skip=()):
    """날마다 플레이스 검색 행 하나(skip 날은 행 없음) + 콘텐츠 행(클릭 0, 노출 큼) + 파워링크 검색 행 — 콘텐츠·파워링크는 판정에 안 들어가야 한다."""
    out = []
    for k in range(n):
        d = start + dt.timedelta(days=k)
        if d in skip:
            continue
        i, c = (imp(d), clk(d))
        out += [(d, "플레이스#1", "검색", i, c), (d, "플레이스#1", "콘텐츠", 999, 0), (d, "파워링크#1", "검색", 50, 9)]
    return out


def checklist(td, lines):
    p = os.path.join(td, "c.csv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(P.HEADER_LINE + "\n" + "".join(l + "\n" for l in lines))
    return p


BASE9 = ["2026-09-01,P1,done,,,", "2026-09-01,P2,todo,,,2026-09-01", "2026-09-01,P3,todo,,,2026-09-01", "2026-09-01,P4,done,,,",
         "2026-09-01,P5,done,,,", "2026-09-01,P6,done,,,", "2026-09-01,P7,todo,,,", "2026-09-01,P8,done,,,", "2026-09-01,P9,done,,,"]


class Effect(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def eff(self, rows, lines, end, prev_end=None, prev12=""):
        inc = frame(rows)
        p = checklist(self.td, lines)
        with contextlib.redirect_stderr(io.StringIO()):
            return C.place_effect(inc, D0, end, p, CFG, prev_end, prev12, "판정 전(3/8주)")

    def test_search_only_calendar_days_and_verdicts(self):
        Dd = dt.date(2026, 9, 20)
        before_days = {Dd - dt.timedelta(days=k) for k in range(1, 15)}
        # 바꾸기 전: 하루 노출 100·클릭 5(9/10 행 빠짐 = 0) / 바꾼 뒤: 하루 노출 100·클릭 8(9/25·9/26 행 빠짐)
        rows = series(D0, 40, lambda d: 100, lambda d: 5 if d < Dd else 8, skip={dt.date(2026, 9, 10), dt.date(2026, 9, 25), dt.date(2026, 9, 26)})
        lines = BASE9 + ["2026-09-20,P2,done,2026-09-20,,", "2026-09-20,P7,todo,,,2026-09-20"]
        r = self.eff(rows, lines, dt.date(2026, 10, 9))
        m = r["측정"][0]
        # 손으로 센 값 — 앞 14일(9/6~9/19) 중 9/10 빠짐: 노출 13×100 · 클릭 13×5 / 뒤 14일(9/21~10/4) 중 9/25·9/26 빠짐: 노출 12×100 · 클릭 12×8
        self.assertEqual((m["전"]["노출"], m["전"]["클릭"], m["후"]["노출"], m["후"]["클릭"]), (1300, 65, 1200, 96))
        self.assertEqual((m["전"]["하루클릭"], m["후"]["하루클릭"]), (round(65 / 14, 1), round(96 / 14, 1)))   # 달력 14일 분모(행 있는 날 수 아님)
        self.assertAlmostEqual(m["변화%"]["하루클릭"], round((96 / 65 - 1) * 100, 1))
        self.assertAlmostEqual(m["변화%"]["CTR"], round(((96 / 1200) / (65 / 1300) - 1) * 100, 1))
        self.assertEqual(m["판정"], "좋아짐")                                       # 클릭 +47.7% > 37 · CTR +60% > 34
        self.assertTrue(before_days)
        # 콘텐츠 행(클릭 0·노출 999)이 섞였으면 CTR 이 크게 달라진다 — 검색 지면만 본 값인지
        self.assertEqual(m["전"]["CTR"], 5.0)

    def test_band_needs_both_and_down(self):
        Dd = dt.date(2026, 9, 20)
        cases = (("클릭만 위", lambda d: 100 if d < Dd else 140, lambda d: 5 if d < Dd else 7, "구별 안 됨"),   # 클릭 +40% · CTR 0%
                 ("둘 다 아래", lambda d: 100, lambda d: 10 if d < Dd else 6, "나빠짐"),                        # 클릭 −40% · CTR −40%
                 ("둘 다 띠 안", lambda d: 100, lambda d: 10 if d < Dd else 12, "구별 안 됨"))                   # +20%
        for label, imp, clk, want in cases:
            with self.subTest(label=label):
                r = self.eff(series(D0, 40, imp, clk), BASE9 + ["2026-09-20,P2,done,2026-09-20,,"], dt.date(2026, 10, 9))
                self.assertEqual(r["측정"][0]["판정"], want, r["측정"][0])

    def test_measuring_overlap_short(self):
        rows = series(D0, 40, lambda d: 100, lambda d: 5)
        r = self.eff(rows, BASE9 + ["2026-10-01,P2,done,2026-10-01,,"], dt.date(2026, 10, 9))
        self.assertEqual(r["측정"][0]["판정"], "측정 중(8/14일)")
        r = self.eff(rows, BASE9 + ["2026-09-20,P2,done,2026-09-20,,", "2026-09-25,P3,done,2026-09-25,,"], dt.date(2026, 10, 9))
        self.assertEqual([m["판정"] for m in r["측정"]], ["겹침(따로 못 잼)", "겹침(따로 못 잼)"])          # 한 번에 한 항목
        r = self.eff(rows, BASE9 + ["2026-09-10,P2,done,2026-09-10,,"], dt.date(2026, 10, 9))
        self.assertEqual(r["측정"][0]["판정"], "비교 불가(자료 부족)")                                  # 9/10 − 14일 < 첫날 9/1
        r = self.eff(rows, BASE9 + ["2026-09-01,P2,done,2026-09-01,,", "2026-09-20,P2,done,2026-09-20,,"], dt.date(2026, 10, 9))
        self.assertEqual(r["측정"][0]["판정"], "구별 안 됨")                                         # 지난 바꿈 9/1 은 14일 밖(19일 앞) — 겹침 아님, 앞 창 9/6~ 은 자료 안
        r = self.eff(rows, BASE9 + ["2026-09-10,P2,done,2026-09-10,,", "2026-09-22,P2,done,2026-09-22,,"], dt.date(2026, 10, 9))
        self.assertEqual(r["측정"][0]["판정"], "겹침(따로 못 잼)")                                       # 같은 항목의 지난 바꿈도 겹침

    def test_rows_12_keep_drop_carry_chat(self):
        rows = series(D0, 70, lambda d: 100, lambda d: 5)
        # 10/11 회차(집계 끝 10/10 · 지난 배포본 끝 10/9)에 적힌 결정 — 그 회차 이월 줄에 한 번, 다음 회차(끝 10/11)엔 없음
        lines = BASE9 + ["2026-09-20,P2,done,2026-09-20,,", "2026-09-20,P7,todo,,,2026-09-20",
                         "2026-10-11,P5,no,2026-10-11,,", "2026-10-11,P6,later,2026-10-11,2026-10-20,"]
        # 판정 날 = 9/20 + 14 = 10/4 · 남김 7일 → 10/10 까지 12번, 10/11 회차에 빠짐
        r = self.eff(rows, lines, dt.date(2026, 10, 10), prev_end=dt.date(2026, 10, 9))
        self.assertEqual([(x["id"], x["종류"]) for x in r["12번"]], [("P2", "판정"), ("P3", "상태"), ("P7", "상태")])
        self.assertLessEqual(len([x for x in r["12번"] if x["종류"] == "상태"]), PC["items_in_12"])
        self.assertEqual(r["빠짐"], [])
        self.assertEqual(r["이월줄"], ["P5 안 함(10/11 결정)", "P6 미룸(10/20 다시 봄)"])        # 지난 배포본(10/9 끝) 뒤에 적힘 → 한 번
        r = self.eff(rows, lines, dt.date(2026, 10, 11), prev_end=dt.date(2026, 10, 10))
        self.assertEqual([x["id"] for x in r["12번"]], ["P3", "P7"])
        self.assertEqual(r["빠짐"], ["P2 구별 안 됨"])
        self.assertEqual(r["이월줄"], [])                                                       # 다음 회차엔 다시 안 나옴
        self.assertEqual(r["채팅질문"], ["P3 12번 9/1부터 40일 그대로", "P7 12번 9/20부터 21일 그대로"])   # 21일(3주) 이상 ✗ — 안 함·미룸은 셈 밖
        # 순서에 밀려 12번에서 내려간 ✗ 도 이월 줄에 한 번
        r = self.eff(rows, lines + ["2026-10-12,P6,todo,,,2026-10-12", "2026-10-12,P7,todo,,,"], dt.date(2026, 10, 11), prev_end=dt.date(2026, 10, 10))
        self.assertEqual(([x["id"] for x in r["12번"]], r["이월줄"]), (["P3", "P6"], ["P7 ✗(12번 자리 순서로 내림)"]))
        # 같은 기간 다시 계산(2-1 같음 — 지난 배포본 끝 날 = 이번 끝 날 10/10): 이번 회차 날(10/11) 결정은 지난 배포본 12번에 그 줄이 없으면 싣고, 있으면 다시 안 씀
        r = self.eff(rows, lines, dt.date(2026, 10, 10), prev_end=dt.date(2026, 10, 10), prev12="<td>· 이월 판정: 없음</td>")
        self.assertEqual(r["이월줄"], ["P5 안 함(10/11 결정)", "P6 미룸(10/20 다시 봄)"])
        r = self.eff(rows, lines, dt.date(2026, 10, 10), prev_end=dt.date(2026, 10, 10), prev12="· 이월 판정: P5 안 함(10/11 결정) · P6 미룸(10/20 다시 봄)")
        self.assertEqual(r["이월줄"], [])
        r = self.eff(rows, lines, dt.date(2026, 10, 21), prev_end=dt.date(2026, 10, 20))
        self.assertIn("P6 미룸 다시 볼 날(10/20) 지남", r["채팅질문"])
        self.assertIn("P7 12번 9/20부터 31일 그대로", r["채팅질문"])

    def test_missing_or_broken(self):
        inc = frame(series(D0, 20, lambda d: 100, lambda d: 5))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            r = C.place_effect(inc, D0, dt.date(2026, 9, 20), os.path.join(self.td, "없음.csv"), CFG, None, "", "확인 못 함")
        self.assertEqual((r["상태"], r["12번"]), ("체크리스트 없음", []))
        self.assertIn("[주의]", err.getvalue())
        p = checklist(self.td, ["2026-09-01,P1,done,,,메모"])
        with contextlib.redirect_stderr(io.StringIO()):
            r = C.place_effect(inc, D0, dt.date(2026, 9, 20), p, CFG, None, "", "확인 못 함")
        self.assertEqual((r["상태"], r["12번"]), ("꼴 다름", []))


class Report(unittest.TestCase):
    def test_rows_html_and_compare(self):
        rows = series(D0, 40, lambda d: 100, lambda d: 5)
        td = tempfile.mkdtemp()
        try:
            p = checklist(td, BASE9 + ["2026-10-01,P2,done,2026-10-01,,", "2026-10-01,P7,todo,,,2026-10-01"])
            with contextlib.redirect_stderr(io.StringIO()):
                eff = C.place_effect(frame(rows), D0, dt.date(2026, 10, 9), p, CFG, None, "", "판정 전(2/8주)")
            R = {"성과장부": {"판정": "판정 전(2/8주)", "기준": "10/9까지", "상태": "ok", "입력주수": 2, "창주": 4, "최소주": 8}, "플레이스전후": eff}
            hs = P.rows_html(R)
            self.assertEqual(len(hs), 3)
            self.assertIn("플레이스 P2 소개글에 체험·가격 — 10/1 바꿈 · 10/9까지 판정 = 측정 중(8/14일)</b>", hs[0])
            self.assertIn("장부 판정 = 판정 전(2/8주)", hs[0])
            self.assertIn("플레이스 P3 네이버 예약 체험 상품 — 10/9까지 상태 = ✗</b>", hs[1])
            import leads as L
            for h in hs:
                t = __import__("re").sub(r"<[^>]+>", "", h)
                self.assertEqual(L.label_hits(t, CFG["leads"]["public_labels"]), [], t)
                for bad in ["필요", "시점", "할 것", "검토", "주째", "확인 요청", "판단 요청", "기다림", "확인 중", "대기"]:
                    self.assertNotIn(bad, t)
            body = "\n".join(f"<tr><td><!-- n:12-{i}:매회차 -->{h}<!-- /n --></td></tr>" for i, h in enumerate([L.row_html(R)] + hs, 2))
            html = f"<!-- Section 12: x -->\n<table><tbody>{body}</tbody></table>\n<script>\n</script>"
            h, j = os.path.join(td, "i.html"), os.path.join(td, "c.json")
            with open(h, "w", encoding="utf-8") as f:
                f.write(html)
            for mutate, diff in ((None, False), ("✗", True)):
                R2 = json.loads(json.dumps(R, ensure_ascii=False, default=str))
                if mutate:
                    R2["플레이스전후"]["12번"][1]["값"] = "✓"                        # compute 는 P3 ✓ 인데 화면은 ✗ — 낡은 행
                with open(j, "w", encoding="utf-8") as f:
                    json.dump(R2, f, ensure_ascii=False)
                r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "compare.py"), h, j], capture_output=True, text=True, encoding="utf-8")
                line = [x for x in r.stdout.splitlines() if "12 플레이스 행" in x and x.startswith("  [")]
                self.assertEqual(len(line), 1, r.stdout[-400:])
                self.assertEqual("[DIFF]" in line[0], diff, line[0])
                self.assertIn("[OK]", [x for x in r.stdout.splitlines() if "12 장부 기준 판정" in x and x.startswith("  [")][0])
        finally:
            shutil.rmtree(td, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=1)
