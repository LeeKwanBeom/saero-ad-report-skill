#!/usr/bin/env python3
"""validate.py "07 각주 세 자리(경쟁사 판정·제외 검색어·클릭 0 전체)" · 28 "화면 글 구역 번호"(판 I — 2026-10-23) 시험 — 합성 구역(배포본·CSV 의존 없음).

평상 회차 · exclusion-ui.md 9절 예외 회차 고정 문구(등록 0 · "등록은 나중에" · 부분 실패 a/b · 재노출 · 등록 누락) → PASS /
a > b · b ≠ 등록 × 대상 그룹 수 · ①②③ 하나라도 없음 · 클릭 0 목록 0건 → FAIL.
실행: "$PY" tests/test_validate_07.py   (config/report-config.json 의 exclusions.targets 수를 읽는다)
"""
import contextlib
import io
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
with contextlib.redirect_stdout(io.StringIO()):
    import validate as V  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

NT = V.N_TARGETS
ONE = '① 경쟁사 판정(1/7): 새 판정 없음 — 표 40행 그대로.<br>경쟁사·타 스튜디오 브랜드명으로 추정되는 검색어.'
THREE = "③ 클릭 0인 검색어 전체는 743개·노출 2,236회(경쟁사 포함)."
LIST0 = ('<div>노출은 있으나 클릭 0건인 검색어</div>\n'
         '<div style="font-size:12.5px;color:var(--ink);line-height:1.9;">\n  가짜검색어가(150회) · 가짜검색어나(61회)\n</div>\n')


def s7(two, one=ONE, three=THREE, list0=LIST0):
    return ('<!-- Section 7: x -->\n<div class="note" style="margin-bottom:12px;">표 설명.</div>\n' + list0 +
            f'<div class="note" style="margin-top:8px;"><!-- n:07-notes:매회차 -->{two}<br>{three}<!-- /n --></div>\n'
            f'<div class="note" style="margin-top:12px;"><!-- n:07-comp:매회차 -->{one}<!-- /n --></div>\n')


def run(sec):
    V.results.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        V.check_07_footnotes(sec)
    (name, ok, detail), = V.results
    return ok, detail


class Footnotes07(unittest.TestCase):
    def test_normal_round(self):
        ok, d = run(s7(f"② 제외 검색어: 1/7 등록 10개 · 확인 {10 * NT}/{10 * NT} · 실패 0(1/8부터 판정) · 1/6 등록분은 1/7부터 판정."))
        self.assertTrue(ok, d)

    def test_exception_phrases_pass(self):  # exclusion-ui.md 9절 고정 문구 — 전부 ② 정규식을 만족하는 꼴
        for two in ("② 제외 검색어: 등록 0개 · 확인 0/0 · 실패 0 — 새 후보 없음 · 등록분은 1/6까지 재노출 0.",
                    "② 제외 검색어: 등록 0개 · 확인 0/0 · 실패 0 — 제안 7개는 등록은 다음에(사용자 결정).",
                    f"② 제외 검색어: 1/7 등록 10개 · 확인 {10 * NT - 2}/{10 * NT} · 실패 2(가짜이름 그룹 1곳 — 다음 회차 재등록 후보).",
                    f"② 제외 검색어: 1/7 등록 3개 · 확인 {3 * NT}/{3 * NT} · 실패 0 · 등록돼 있는데도 노출: 가짜이름(등록 1/2·노출 1/6 1회).",
                    "② 제외 검색어: 등록 0개 · 확인 0/0 · 실패 0 · 등록 누락 → 후보: 가짜이름(registry unregistered).",
                    "② 제외 검색어: 등록 0개 · 확인 0/0 · 실패 0 — registry를 못 읽어 재노출 판정 미확인."):
            with self.subTest(two=two):
                ok, d = run(s7(two))
                self.assertTrue(ok, d)

    def test_a_greater_than_b_fail(self):
        ok, d = run(s7(f"② 제외 검색어: 1/7 등록 10개 · 확인 {10 * NT + 1}/{10 * NT} · 실패 0."))
        self.assertFalse(ok)
        self.assertIn("a > b", d)

    def test_b_not_registered_times_targets_fail(self):
        ok, d = run(s7(f"② 제외 검색어: 1/7 등록 10개 · 확인 10/10 · 실패 0." if NT != 1 else "② 제외 검색어: 1/7 등록 10개 · 확인 9/9 · 실패 0."))
        self.assertFalse(ok)
        self.assertIn("≠ 등록", d)

    def test_each_missing_place_fails(self):
        two = f"② 제외 검색어: 1/7 등록 10개 · 확인 {10 * NT}/{10 * NT} · 실패 0."
        for kw, sec, frag in (("①", s7(two, one="경쟁사·타 스튜디오 브랜드명으로 추정되는 검색어."), "① 경쟁사 판정"),
                              ("②", s7("② 제외검색어: 1/7 등록 10개 · 확인 30/30 · 실패 0."), "② 제외 검색어"),
                              ("③", s7(two, three="③ 클릭 0 검색어 743개."), "③ 클릭 0인"),
                              ("클릭0 목록", s7(two, list0=""), "클릭 0 목록 항목 0건")):
            with self.subTest(kw=kw):
                ok, d = run(sec)
                self.assertFalse(ok, d)
                self.assertIn(frag, d)

    def test_no_note_at_all_fail(self):
        ok, d = run("<!-- Section 7: x -->\n<div>각주 없음</div>\n" + LIST0)
        self.assertFalse(ok)
        self.assertIn('class="note" 0개', d)


class SectionRefs(unittest.TestCase):
    """validate 28 "화면 글 구역 번호"(판 I — 2026-10-23 콘텐츠 지면 빼기): 서술 표지 안 'NN번' 이 1~11 · 지면 가리키는 10번 0 · 옛 지면 글 0.
    검색어 속 숫자('노원역10번출구' · '노원역 12번 출구')·'N번째' 는 안 센다 · 기계 자리(표지 밖) 글은 안 본다 · 표지 0개 FAIL."""
    def check(self, *bodies, outside=""):
        V.results.clear()
        html = "".join(f"<div><!-- n:x{i}:매회차 -->{b}<!-- /n --></div>\n" for i, b in enumerate(bodies)) + outside
        with contextlib.redirect_stdout(io.StringIO()):
            V.check_section_refs(html)
        (name, ok, detail), = V.results
        self.assertTrue(name.startswith("화면 글 구역 번호"), name)
        return ok, detail

    def test_pass_forms(self):
        ok, d = self.check("<li>제외 검색어 — 등록 5개(07번 ②·11번 1번)</li>", "카드 유지(11번 2번)", "지난 회차 10번 8개 항목 판정: 유지 6",
                           "KPI·01~07번에서 제외 — 08·09번은 포함", '"노원역10번출구"(5회) · 노원역 12번 출구 · 3번째 날 · 01·04번 참고',
                           outside="<td>노원역 12번 출구(3회)</td> 12번 · 콘텐츠 지면 47일 연속 0")
        self.assertTrue(ok, d)

    def test_fail_forms(self):
        for body, frag in (("(12번 2번)", "'12번'(없는 구역"), ("07번 ②·12번 1번", "없는 구역"),
                           ("지난 회차 12번 3개 항목", "없는 구역"), ("(12번 행 없음)", "없는 구역"),
                           ("KPI·01~07·10번에서 제외", "지면 구역을 가리키는 10번"), ("콘텐츠 지면 노출 1,746회는 10번 참고", "지면 구역을 가리키는 10번"),
                           ("· 콘텐츠 지면 47일 연속 0 ·", "옛 지면 구역 글"), ("검색 지면 vs 콘텐츠 지면", "옛 지면 구역 글")):
            with self.subTest(body=body):
                ok, d = self.check("정상 글(11번 1번)", body)
                self.assertFalse(ok, d)
                self.assertIn(frag, d)

    def test_zero_markers_guard(self):
        V.results.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            V.check_section_refs("<div>표지 없음 12번</div>")
        self.assertFalse(V.results[0][1])
        self.assertIn("서술 표지 0개", V.results[0][2])


if __name__ == "__main__":
    unittest.main(verbosity=1)
