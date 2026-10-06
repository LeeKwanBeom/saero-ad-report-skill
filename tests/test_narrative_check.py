#!/usr/bin/env python3
"""scripts/narrative_check.py 시험 — 합성 HTML(외부·파일 의존 없음).

한 블록 미교체 → FAIL · 전부 교체 → PASS · 작업본 표지 0 → FAIL · 직전에 표지 없음 → [주의] exit 0 · 같은 기간 → [주의] exit 0 ·
고정 블록은 같아도 통과 · 표지 짝 어긋남·이름 중복 → FAIL · CLI 종료 코드.
실행: "$PY" tests/test_narrative_check.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
import narrative_check as nc  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def page(period, blocks, plain=""):
    """blocks = [(자리, 종류, 글)]."""
    body = "".join(f'<div class="note"><!-- n:{n}:{k} -->{t}<!-- /n --></div>\n' for n, k, t in blocks)
    return f'<div class="period">집계 기간<b>{period}</b></div>\n<!-- Section 1: x -->\n{body}{plain}'


PREV = page("2026.08.26 — 10.04 (40일)", [("01-desc", "매회차", "10/4(일) 노출 200회"), ("07-notes", "매회차", "② 제외 검색어: 10/5 등록 10개"),
                                          ("12-basis", "고정", "· 집계 기간: 개업일부터 누적")])


class NarrativeCheck(unittest.TestCase):
    def test_all_replaced_pass(self):
        work = page("2026.08.26 — 10.05 (41일)", [("01-desc", "매회차", "10/5(월) 노출 219회"), ("07-notes", "매회차", "② 제외 검색어: 10/6 등록 10개"),
                                                  ("12-basis", "고정", "· 집계 기간: 개업일부터 누적")])  # 고정은 같아도 통과
        rc, out = nc.check(work, PREV)
        self.assertEqual(rc, 0, out)
        self.assertTrue(out[-1].startswith("[PASS] 서술 표지 3개 · 매회차 2개"), out)

    def test_one_block_stale_fail(self):
        work = page("2026.08.26 — 10.05 (41일)", [("01-desc", "매회차", "10/5(월) 노출 219회"), ("07-notes", "매회차", "② 제외 검색어: 10/5 등록 10개"),
                                                  ("12-basis", "고정", "· 집계 기간: 개업일부터 누적")])
        rc, out = nc.check(work, PREV)
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] 서술 미교체 07-notes", "\n".join(out))
        self.assertNotIn("01-desc", "\n".join(x for x in out if x.startswith("[FAIL]")))

    def test_zero_markers_fail(self):
        work = '<div>집계 기간<b>2026.08.26 — 10.05 (41일)</b></div><div class="note">옛 글</div>'
        rc, out = nc.check(work, PREV)
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] 작업본에 서술 표지 0개", out[0])
        rc, out = nc.check(work, work)  # 같은 기간이어도 표지 0은 FAIL(0건 가드가 먼저)
        self.assertEqual(rc, 1, out)

    def test_prev_without_markers_notice(self):
        work = page("2026.08.26 — 10.05 (41일)", [("01-desc", "매회차", "10/5(월) 노출 219회")])
        old = '<div>집계 기간<b>2026.08.26 — 10.04 (40일)</b></div><div class="note">10/4(일) 노출 200회</div>'
        rc, out = nc.check(work, old)
        self.assertEqual(rc, 0, out)
        self.assertTrue(out[0].startswith("[주의] 직전 배포본에 표지 없음 — 대조 생략"), out)

    def test_same_period_notice(self):
        work = page("2026.08.26 — 10.04 (40일)", [("01-desc", "매회차", "10/4(일) 노출 200회"), ("07-notes", "매회차", "② 제외 검색어: 10/5 등록 10개"),
                                                  ("12-basis", "고정", "· 집계 기간: 개업일부터 누적")])
        rc, out = nc.check(work, PREV)  # 블록이 전부 같아도 같은 기간이면 대조 생략
        self.assertEqual(rc, 0, out)
        self.assertTrue(out[0].startswith("[주의] 같은 기간 — 대조 생략"), out)

    def test_broken_or_duplicate_markers_fail(self):
        dup = page("2026.08.26 — 10.05 (41일)", [("01-desc", "매회차", "a"), ("01-desc", "매회차", "b")])
        rc, out = nc.check(dup, PREV)
        self.assertEqual(rc, 1, out)
        self.assertIn("중복 이름", out[0])
        broken = page("2026.08.26 — 10.05 (41일)", [("01-desc", "매회차", "a")]) + "<!-- n:07-notes:매회차 -->닫는 표지 없음"
        rc, out = nc.check(broken, PREV)
        self.assertEqual(rc, 1, out)
        self.assertIn("짝", out[0])

    def test_cli_exit_codes(self):
        td = tempfile.mkdtemp()
        w, p = os.path.join(td, "w.html"), os.path.join(td, "p.html")
        stale = page("2026.08.26 — 10.05 (41일)", [("01-desc", "매회차", "10/4(일) 노출 200회")])
        for path, text in ((w, stale), (p, PREV)):
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(HERE), "scripts", "narrative_check.py"), w, p],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("[FAIL] 서술 미교체 01-desc", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
