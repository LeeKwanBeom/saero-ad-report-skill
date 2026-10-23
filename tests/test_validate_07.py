#!/usr/bin/env python3
"""validate.py "07 각주 세 자리(경쟁사 판정·제외 검색어·클릭 0 전체)" · 28 "화면 글 구역 번호"(판 I — 2026-10-23) · 30 "판 J 뺀 글 0" · 19 판정 줄 'M/D까지'(판 J — 2026-10-23 오후)
시험 — 합성 구역(배포본·CSV 의존 없음).

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


J_SEC = {1: '<span class="section-desc"><!-- n:01-desc:매회차 -->1/7(수) 노출 10회·클릭 1건·CTR 10.00% — 전날보다 늘었음<!-- /n --></span>'
            '<div class="note"><!-- n:01-rank:매회차 -->1/7까지 누적 가중평균은 2.10 → 2.11위(작을수록 상단)<!-- /n --></div>',
         3: "<!-- n:03-desc:고정 -->최고치 1/2(금) 9,000원<!-- /n -->",
         4: '<!-- n:04-mint:매회차 -->→ 1/7까지 격차 기준 = 파워링크 총비용 1위 "가짜" CPC 500원 vs 플레이스 1,000원<!-- /n -->'
            "<!-- n:04-note:매회차 -->두 광고는 성격이 달라 … 1/7까지 파워링크 비중은 8.0 → 8.1%. 예산은 현행 유지(사용자 결정).<!-- /n -->",
         6: "<!-- n:06-arrow:매회차 -->→ 자동매칭이 노출·클릭 모두 앞섬(첫 리포트부터 같음) — 1/7 직접 1·자동 2회<!-- /n -->",
         7: '<div class="note"><!-- n:07-notes:매회차 -->② 제외 검색어: 1/7 등록 1개 · 확인 3/3 · 실패 0.<br>③ 클릭 0인 검색어 전체는 10개·노출 20회(경쟁사 포함 · 클릭이 없어 비용 0원).<!-- /n --></div>',
         8: '<!-- n:08-note:고정 -->이 외 클릭 0인 2개 지역에서 노출 3회 발생.<br>※ …<!-- /n --><!-- n:08-mint:매회차 -->→ 1/7까지 노원구 단독으로 전체 노출의 45%·클릭의 48% 차지 · "국내 - 상세 위치 확인불가" 비용 비중 8.8%.<!-- /n -->',
         9: "<!-- n:09-desc:고정 -->20시대 클릭 최다(46건)<!-- /n --><!-- n:09-call:고정 -->→ 심야(22시~09시) 노출 1회(22%)·클릭 1건(22%)·비용 1원 — 낮 시간대와 비슷한 효율. 2위는 13시 41건.<!-- /n -->",
         10: ("<!-- n:11-list:매회차 --><ul><li><b>지난 회차 관찰이 뒤집힘 — 가짜</b>(하루치라 아직 알 수 없음, 01번 참고)</li>"
              "<li><b>1/7까지 변화 없음</b> — 모바일 비중·최다 클릭 시간대(20시)·파워링크 총비용 1위 그룹(04·05·06·08·09번)</li></ul><!-- /n -->"
              "<div><!-- n:11-verdict:매회차 -->1/7까지 지난 회차 10번 2개 항목 판정: 유지 1 · 뒤집힘 1 · 근거 소멸 0<!-- /n --></div>"),
         11: ('<!-- n:12-1:매회차 --><span class="tag tag-mint">상시</span> <b>제외 검색어 정기 점검 — 1/7 등록 1개</b><div class="note">다음 회차 판정: 1/7 등록분이 다시 노출되는지</div><!-- /n -->'
              "<!-- n:12-note:매회차 -->· 1/7까지 지난 항목 3개 모두 이어감<br>· 신규 없음<!-- /n -->")}


def j_page(over=None):
    sec = dict(J_SEC) | (over or {})
    return "".join(f"<!-- Section {n}: x -->\n{sec.get(n, '<div>빈 구역 글</div>')}\n" for n in range(1, 12)) + "<script></script>"


class TrimGoneJ(unittest.TestCase):
    """validate 30 "판 J 뺀 글 0"(2026-10-23 오후 — 결정 10~14·19~24·37): 판 J 꼴 → PASS · 옛 꼴 하나라도 다시 나오면 FAIL · 구역 0자 FAIL(0건 가드) ·
    10 제외 검색어 항목은 07 ② 에 실패·재노출·미확인이 있는 날만."""
    def run_(self, html):
        V.results.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            V.check_trim_gone(html)
        (name, ok, detail), = V.results
        self.assertTrue(name.startswith("판 J 뺀 글 0"), name)
        return ok, detail

    def test_j_forms_pass(self):
        ok, d = self.run_(j_page())
        self.assertTrue(ok, d)

    def test_old_forms_fail(self):
        S = J_SEC
        cases = ((1, S[1].replace("전날보다 늘었음", "전날보다 늘었음, 누적 CTR 3.34 → 3.34%"), "01 머리 줄 누적 CTR"),
                 (1, S[1].replace("1/7까지 누적", "닷새 2.82 → 3.99 → 3.66위(작을수록 상단) · 누적"), "01 ② 닷새 나열"),
                 (3, S[3].replace("9,000원", "9,000원 그대로 — 1/7(수)은 5,000원(플레이스 4,000원 + 파워링크 1,000원)"), "03 머리 줄"),
                 (4, S[4].replace("1,000원<!-- /n -->", "1,000원 — 격차 2.50 → <b>2.49배</b> 줄어듦<!-- /n -->"), "04 민트 줄 격차 되풀이"),
                 (6, S[6].replace("모두 앞섬(첫 리포트부터 같음)", "우위 42회차 연속"), "06 '회차 연속'"),
                 (7, S[7].replace("클릭이 없어 비용 0원", "지난 회차 9개·19회"), "07 ③ 지난 회차"),
                 (8, S[8].replace("발생.<br>", "발생. TOP 10 + 위 목록으로 1/7까지 전체 클릭 5건이 모두 표시됨.<br>"), "08 '모두 표시됨'"),
                 (9, S[9].replace("(46건)", "(46회, 11회차 연속) — 상시 문의 대응 전략과 부합"), "09 '회차 연속'"),
                 (9, S[9].replace("2위는 13시 41건", "최다 클릭 시간대는 20시 46회, 2위는 13시 41회"), "09 '최다 클릭 시간대는'"),
                 (10, S[10].replace("</ul>", "<li><b>(참고)</b> 경쟁사 — 가짜(07번 ①)</li></ul>"), "10 (참고) 경쟁사"),
                 (10, S[10].replace("근거 소멸 0", "근거 소멸 0 — 이번 요약은 2개 + (참고) 0개."), "10 판정 줄 되풀이"),
                 (10, S[10].replace("모바일 비중·", "모바일 비중 79.6%·"), "10 변화 없음 줄에 숫자"),
                 (10, S[10].replace("</ul>", "<li><b>제외 검색어 — 1/7 등록 1개</b>(07번 ②)</li></ul>"), "10 제외 검색어 항목"),
                 (11, S[11].replace("</b><div", "</b> — 등록 여부는 스킬이 등록 목록(registry)으로 판정(사장님께 다시 묻지 않음)<div"), "11 registry 구"),
                 (11, S[11].replace("· 신규 없음", "· <b>신규 없음</b>: 플레이스 상향 뒤 CPC 1,421원"), "11 note 신규 없음 사유"),
                 (11, S[11].replace("<!-- n:12-note:매회차 -->", "<!-- n:12-note:매회차 -->· <b>정렬</b>: 1번은 맨 위<br>"), "11 note 정렬·경쟁사"))
        for n, body, frag in cases:
            with self.subTest(frag=frag):
                self.assertNotEqual(body, J_SEC[n])
                ok, d = self.run_(j_page({n: body}))
                self.assertFalse(ok, d)
                self.assertIn(frag, d)

    def test_excl_item_allowed_on_event_day(self):
        ev = J_SEC[7].replace("실패 0.", "실패 0 · 등록돼 있는데도 노출: 가짜이름(등록 1/2·노출 1/6 1회).")
        ok, d = self.run_(j_page({7: ev, 10: J_SEC[10].replace("</ul>", "<li><b>제외 검색어 — 등록돼 있는데도 노출 1개</b>(07번 ②)</li></ul>")}))
        self.assertTrue(ok, d)

    def test_empty_section_guard(self):
        html = j_page().replace("<!-- Section 3: x -->", "<!-- Sect 3: x -->", 1)
        ok, d = self.run_(html)
        self.assertFalse(ok)
        self.assertIn("0자", d)


class VerdictDateJ(unittest.TestCase):
    """validate 19 "10번 항목 수·판정 줄"(판 J): 판정 줄 앞 'M/D까지' = 집계 끝(없거나 다르면 FAIL — G1·낡은 날짜)."""
    def run_(self, verdict, dmax):
        import datetime as dt
        sec10 = "<ul><li><b>1/7까지 변화 없음</b> — 모바일 비중(05번)</li></ul><div>" + verdict + "</div>"
        html = "<!-- Section 7: x -->\n<div class=\"note\">각주</div>\n<!-- Section 10: x -->\n" + sec10 + "\n<!-- Section 11: x -->\n<div>다음 액션</div>\n<script></script>"
        V.results.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            V.check_11_12(html, False, dt.date(2026, *dmax))
        return [r for r in V.results if r[0] == "10번 항목 수·판정 줄"][0]

    def test_date(self):
        self.assertTrue(self.run_("1/7까지 지난 회차 10번 2개 항목 판정: 유지 2 · 뒤집힘 0 · 근거 소멸 0", (1, 7))[1])
        for v, frag in (("지난 회차 10번 2개 항목 판정: 유지 2 · 뒤집힘 0 · 근거 소멸 0", "없음"), ("1/6까지 지난 회차 10번 2개 항목 판정: 유지 2 · 뒤집힘 0 · 근거 소멸 0", "1/6")):
            with self.subTest(v=v):
                name, ok, d = self.run_(v, (1, 7))
                self.assertFalse(ok)
                self.assertIn(frag, d)


if __name__ == "__main__":
    unittest.main(verbosity=1)
