#!/usr/bin/env python3
"""scripts/apply.py 시험(E2 저장소화 2026-10-06 + 레이아웃 판 r2026-10-B 회차 2 + 판 r2026-10-C 01 차트 회차 1) + compute.py 직전 경쟁사표 0행 가드.

fixture = tests/fixtures/layout_old.html(배포본 앵커 마크업 발췌 — 숫자·검색어·경쟁사·그룹 이름 가짜, 서술 표지·레이아웃 meta 없는 옛 판) +
          tests/fixtures/layout_old.compute.json(같은 가짜 값의 compute 출력 꼴 — 03.rows 만 10일(12/29~1/7)이라 "최근 7 + 접힌 3" 분배가 보인다).
- 판 고르기: meta 없음 + --layout 없음 → `[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout …`(옛 배치로 쓰지 않음, 작업본 그대로) ·
  meta 다름·details 수 다름 → FAIL · --layout 변환 = 사슬(옛 → r2026-10-B: meta + details 5 + 접기 CSS·스크립트 → r2026-10-C: 분기 표지 2 ·
  01·06 템플릿 · 분기 도우미 · 왼쪽 페이드 · 안내 4줄), 두 번째(변환 건너뜀)는 바이트 같음.
- 판 C(ApplyLayoutC): meta r2026-10-B 판 + --layout 없음 → `레이아웃 판 meta r2026-10-B ≠ config r2026-10-C — --layout …` · + --layout → 사슬과 같은 바이트 ·
  분기 표지 하나 지운 C 판 → FAIL "분기 표지" · 묵은 M 줄 → config 값으로 다시 씀 · 변환이 섹션 HTML·서술 표지·min-width 를 건드리지 않음 · 판 C 앵커 없음 → FAIL.
- 멱등: 같은 compute.json 으로 두 번 돌리면 바이트 같음(--layout 있음·없음, 서술 표지를 넣은 fixture 도 — 표지 안쪽 바이트 불변·details 밖).
- 앵커·행 수: masthead·og·KPI·차트·01 표 5행·순위 5칸(오름차순 그대로)·03 = 합계 맨 위 + 최근 7일 최신 위 + 접힌 표 나머지 최신 위 ·
  04·06·07 정식표/목록/경쟁사표·08·10 이 compute 값과 같음. 동률은 직전 순서(클릭 1건 목록) · 신규 변형 행 = config competitor_defaults.
- summary 기계 자리(막음 M2): 03 "이전 N일(M/D~M/D)"·07 "(N개 · 펼치기)"·경쟁사 "표 N행"·08 "(N개 지역·클릭 M건)" — 옛 값으로 바꿔 둔 판도 다시 쓰고,
  일수 ≤ recent_days 면 접힌 표 0행 + "이전 0일 펼치기"(details 5 그대로).
- 시끄러운 실패: 앵커가 없거나 둘이면·새 04 그룹·직전/후보 밖 경쟁사 → `[FAIL] apply:` exit 1, 작업본 바이트 그대로.
- compute.py: --competitors-html 의 경쟁사표 0행(소제목만 바꾼 사본 — 탐색 프로브 r10 유형) → `[FAIL]` exit 1(합본을 읽기 전) · 접힌 경쟁사표도 그대로 읽음.
- 리허설 산출(work/R3/index.html + compute.json, 서술 표지·레이아웃 판 r2026-10-C 있음)이 있으면 그것도 멱등(없으면 건너뜀) — A.apply() 직접(meta 로 판 선택).
실행: "$PY" tests/test_apply.py
"""
import hashlib
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
import apply as A  # noqa: E402
from reportlib import load_config, section  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

FIX = os.path.join(HERE, "fixtures", "layout_old.html")
FIXJ = os.path.join(HERE, "fixtures", "layout_old.compute.json")
APPLY = os.path.join(ROOT, "scripts", "apply.py")
COMPUTE = os.path.join(ROOT, "scripts", "compute.py")


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def jread(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def rows(s):
    return re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S)


def cells(tr):
    return [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]


def listtext(h, anchor):
    a = h.index('line-height:1.9;">', h.index(anchor)) + len('line-height:1.9;">')
    return [x.strip() for x in h[a:h.index("</div>", a)].strip().split(" · ")]


def tbodies(sec):
    return [[cells(t) for t in rows(b) if "<td" in t] for b in re.findall(r"<tbody>(.*?)</tbody>", sec, re.S)]


def unfold_one(h, n):
    """n 번 구역의 첫 details/summary 를 걷어 낸 판(details 수 하나 줄이기)."""
    sec = section(h, n)
    return h.replace(sec, re.sub(r"</details>", "", re.sub(r"<details[^>]*>\s*<summary[^>]*>.*?</summary>", "", sec, count=1, flags=re.S), count=1), 1)


class ApplyFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)

    def test_idempotent_and_changed(self):
        self.assertNotEqual(self.out, self.H)                      # 빈 시험이 아님 — 값이 실제로 바뀐다
        self.assertEqual(A.apply(self.out, self.R, self.cfg), self.out)                # meta 있음 → 변환 없이 값만(--layout 없이도)
        self.assertEqual(A.apply(self.out, self.R, self.cfg, layout=True), self.out)   # --layout 이어도 변환 건너뜀

    def test_layout_conversion_skeleton(self):
        o, lay = self.out, self.cfg["report_layout"]
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), [lay["layout_id"]])
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", o)), lay["markers"]["details"])
        self.assertEqual(len(re.findall(r"<details[^>]*>\s*<summary", o)), lay["markers"]["details"])     # details 마다 바로 안 summary
        self.assertEqual(o.count("</details>"), lay["markers"]["details"])
        self.assertEqual(o.count('line-height:1.9;">'), 3)                                              # 기준점 셋 그대로
        for anchor in ("클릭 1건 검색어", "노출은 있으나 클릭 0건인", "TOP 10 외"):                          # 앵커 뒤 첫 line-height:1.9 = 목록 div(summary 아님)
            i = o.index(anchor)
            self.assertLess(o.index("</summary>", i), o.index('line-height:1.9;">', i))
            self.assertNotIn("line-height:1.9", o[o.rindex("<summary", 0, i):o.index("</summary>", i)])
        self.assertIn(".fold > summary{cursor:pointer;}", o)
        self.assertIn("addEventListener('toggle', sync)", o)
        self.assertIn("'beforeprint'", o)
        self.assertIn("'afterprint'", o)
        self.assertIn("경쟁사 브랜드명 검색어</div>", o)                                                 # 경쟁사 머리글 리터럴 그대로(details 밖)
        s8 = section(o, 8)
        self.assertLess(s8.index("</details>"), s8.index('<div class="note"'))                          # 08 각주 note 는 details 밖
        s7 = section(o, 7)
        self.assertLess(s7.rindex("</details>", 0, s7.index("가짜 각주")), s7.index("가짜 각주"))            # 07 클릭 0 각주도 details 밖

    def test_idempotent_with_narrative_markers(self):
        """서술 표지가 있는 판(새 글) — 표지는 apply 가 건드리지 않고, 01 순위 5칸 끝 앵커(표지 무관)도 그대로 맞는다."""
        H2 = self.H.replace('<div class="note">닷새 동안 가짜 순위 서술.</div>',
                            '<div class="note"><!-- n:01-rank:매회차 -->닷새 가짜 순위 서술.<!-- /n --></div>', 1)
        H2 = H2.replace("        4일차. 가짜 카드 서술.", "        <!-- n:06-card-가짜그룹B:매회차 -->4일차. 가짜 카드 서술.<!-- /n -->", 1)
        H2 = H2.replace("이 검색어들은 비용이 발생하지 않았지만(클릭 0), 가짜 각주.", "<!-- n:07-notes:매회차 -->이 검색어들은 비용이 발생하지 않았지만(클릭 0), 가짜 각주.<!-- /n -->", 1)
        H2 = H2.replace("이 외 클릭 0인 가짜 지역. 가짜 08 각주.", "<!-- n:08-note:매회차 -->이 외 클릭 0인 가짜 지역. 가짜 08 각주.<!-- /n -->", 1)
        self.assertEqual(H2.count("<!-- n:"), 4)
        o1 = A.apply(H2, self.R, self.cfg, layout=True)
        self.assertEqual(A.apply(o1, self.R, self.cfg), o1)
        blk = r"<!-- n:[^>]+-->.*?<!-- /n -->"
        self.assertEqual(re.findall(blk, o1, re.S), re.findall(blk, H2, re.S))   # 변환·값 교체 모두 표지 안쪽 바이트 불변
        for m in re.finditer(blk, o1, re.S):                                     # 표지는 접기 밖(항상 보임)
            self.assertEqual(o1.count("<details", 0, m.start()), o1.count("</details>", 0, m.start()), m.group(0)[:40])
        self.assertEqual(o1.count("위</div>"), self.out.count("위</div>"))  # 순위 5칸이 그대로 생성됨

    def test_values_and_row_counts(self):
        o, R = self.out, self.R
        self.assertIn(f"집계 기간<b>{R['masthead']}</b>", o)
        self.assertIn(f'og:description" content="{R["og"]}"', o)
        self.assertIn(f'<div class="value">{R["KPI"]["노출"]:,}<span class="unit">회', o)
        self.assertIn(f"일 평균 {R['KPI']['일평균노출']}회", o)
        self.assertIn(f"클릭당 평균 {R['KPI']['클릭당']:,}원", o)
        self.assertIn(f"광고비 비중 (총 {R['KPI']['광고비']:,}원)", o)
        self.assertEqual(len(re.findall(rf'min-width:{R["minwidth"]}px;">\s*<canvas id="(?:dailyChart|rankChart)"', o)), 2)
        self.assertIn("labels: [" + ",".join(f"'{x}'" for x in R["01"]["labels"]) + "]", o)
        self.assertIn("data: [" + ", ".join(map(str, R["01"]["노출"])) + "]", o)
        s1, s3, s4, s6, s7, s8, s10 = (section(o, n) for n in (1, 3, 4, 6, 7, 8, 10))
        self.assertEqual([cells(t)[0] for t in rows(s1)], [r["날짜"] for r in R["01"]["표5"]])
        self.assertEqual(re.findall(r'margin-bottom:2px;">([^<]+)</div>', s1), [g["날짜"] for g in R["01"]["플레이스순위5"]])
        self.assertEqual(len(re.findall(r'font-weight:800;color:var\(--mint-dark\);">[\d.]+위', s1)), 1)   # 민트 칸 하나
        r3 = [cells(t) for t in rows(s3) if "<td" in t]
        self.assertEqual(len(r3), len(R["03"]["rows"]) + 1)
        dates = [r["날짜"] for r in R["03"]["rows"]]
        self.assertEqual([r[0] for r in r3], ["합계"] + dates[::-1])                                     # 합계 맨 위 + DOM 전체 최신 위
        k = self.cfg["report_layout"]["recent_days"]
        self.assertGreater(len(dates), k + 1)                                                           # fixture 가 분배를 볼 만큼 길다(10일)
        top, fold = tbodies(s3)
        self.assertEqual([r[0] for r in top], ["합계"] + dates[-k:][::-1])                               # 위 표 = 합계 + 최근 7일 최신 위
        self.assertEqual([r[0] for r in fold], dates[:-k][::-1])                                         # 접힌 표 = 나머지 최신 위
        self.assertEqual(top[0][1:], ["27,000원", "27", "1,000원", "4,000원", "4", "1,000원", "31,000원"])
        self.assertLess(s3.index("</tbody>"), s3.index("<details"))                                     # 위 표는 접기 밖
        self.assertIn('<summary class="fold-more">이전 3일(12/29~12/31) 펼치기</summary>', s3)
        self.assertEqual([cells(t)[0] for t in rows(s1)], [r["날짜"] for r in R["01"]["표5"]])           # 01 은 오름차순 그대로(결정 4 (가))
        self.assertEqual([cells(t)[1].split("(")[0].strip() for t in rows(s4)], [r["그룹"] for r in R["04"]["rows"]])
        self.assertIn("(1/2 신규)", s4)                                                                  # 이름 칸 메모는 직전 행 그대로
        self.assertIn("(1/2 등록, 6일차)", s6)
        self.assertIn('font-weight:800;color:var(--mint-dark);">1.55위', s6)
        main7 = [cells(t) for t in rows(s7[:s7.index("클릭 1건 검색어")])]
        self.assertEqual([r[0] for r in main7], [r["검색어"] for r in R["07"]["정식표"]])
        self.assertEqual(main7[1][1], "확장")                                                            # *동률 표시는 지움
        self.assertEqual(listtext(o, "클릭 1건 검색어"), ["가짜한건가(12회/700원)", "가짜한건나(10회/500원)", "가짜한건다(10회/900원)"])  # 동률 = 직전 순서
        self.assertEqual(listtext(o, "노출은 있으나 클릭 0건인"), [f"{x['검색어']}({x['노출']}회)" for x in R["07"]["클릭0목록"]])
        comp = [cells(t) for t in rows(s7[s7.index("경쟁사 브랜드명 검색어"):])]
        self.assertEqual([r[0] for r in comp], [r["검색어"] for r in R["07"]["경쟁사표"]])
        d = self.cfg["competitor_defaults"]
        self.assertEqual(comp[1][1:3], [d["district"], d["match"]])                                      # 신규 변형 = config 기본값
        self.assertEqual(comp[0][1:3], ["가짜구", "일치"])                                                 # 직전 행 그대로
        self.assertEqual(len([t for t in rows(s8) if "<td" in t]), 10)
        self.assertEqual(listtext(o, "TOP 10 외"), ["가짜동(노출6·클릭1)", "가짜읍(노출5·클릭1)"])
        self.assertIn(f"({R['08']['컴팩트수']}개 지역·클릭 {R['08']['컴팩트클릭']}건)</span> · 펼치기</summary>", s8)
        self.assertIn(f"클릭 1건 검색어 <span style=\"font-weight:400;\">({len(R['07']['클릭1'])}개 · 펼치기)</span></summary>", s7)
        self.assertIn(f"(노출 5회 이상 {len(R['07']['클릭0목록'])}개 · 펼치기)</span></summary>", s7)
        self.assertIn(f'<summary class="fold-more">표 {len(R["07"]["경쟁사표"])}행 · 펼치기</summary>', s7)
        self.assertEqual([[c.replace(",", "").replace("원", "") for c in cells(t)[2:5]] for t in rows(s10)],
                         [[str(v) for v in R["10"][k]] for k in "ABCD"])


class ApplyLayoutSelect(unittest.TestCase):
    """판 고르기·summary 기계 자리(M2)·짧은 기간."""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)

    def test_old_layout_without_flag_fails(self):
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta 없음 — --layout"):
            A.apply(self.H, self.R, self.cfg)

    def test_meta_mismatch_or_details_count_fails(self):
        lid = self.cfg["report_layout"]["layout_id"]
        other = self.out.replace(f'content="{lid}"', 'content="r2099-01-Z"', 1)
        for flag in (False, True):
            with self.assertRaisesRegex(A.ApplyError, "≠ config"):
                A.apply(other, self.R, self.cfg, layout=flag)
        with self.assertRaisesRegex(A.ApplyError, "details 4개"):
            A.apply(unfold_one(self.out, 3), self.R, self.cfg, layout=True)
        with self.assertRaisesRegex(A.ApplyError, "<details> 가"):                     # meta 없는데 접기가 있는 판 — 변환 안 함
            A.apply(re.sub(r'<meta name="report-layout"[^>]*>\n', "", self.out), self.R, self.cfg, layout=True)

    def test_summaries_rewritten_every_run(self):
        """막음 M2 — 변환을 건너뛴 회차에도 summary 개수·날짜를 compute.json 으로 다시 쓴다."""
        stale = (self.out.replace("이전 3일(12/29~12/31) 펼치기", "이전 2일(12/30~12/31) 펼치기", 1)
                 .replace(f"({len(self.R['07']['클릭1'])}개 · 펼치기)", "(99개 · 펼치기)", 1)
                 .replace(f"노출 5회 이상 {len(self.R['07']['클릭0목록'])}개", "노출 5회 이상 98개", 1)
                 .replace(f"표 {len(self.R['07']['경쟁사표'])}행 · 펼치기", "표 97행 · 펼치기", 1)
                 .replace(f"({self.R['08']['컴팩트수']}개 지역·클릭 {self.R['08']['컴팩트클릭']}건)", "(96개 지역·클릭 95건)", 1))
        self.assertEqual(len([x for x in ("이전 2일", "99개", "98개", "97행", "96개 지역") if x in stale]), 5)
        self.assertEqual(A.apply(stale, self.R, self.cfg), self.out)

    def test_short_period_has_empty_fold(self):
        R = jread(FIXJ)
        R["03"]["rows"] = R["03"]["rows"][-5:]                                           # 5일 ≤ recent_days 7
        o = A.apply(self.H, R, self.cfg, layout=True)
        s3 = section(o, 3)
        top, fold = tbodies(s3)
        self.assertEqual([r[0] for r in top], ["합계"] + [r["날짜"] for r in R["03"]["rows"]][::-1])
        self.assertEqual(fold, [])
        self.assertIn(">이전 0일 펼치기</summary>", s3)
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", o)), self.cfg["report_layout"]["markers"]["details"])
        self.assertEqual(A.apply(o, R, self.cfg), o)
        R2 = jread(FIXJ)                                                                  # 다음 회차에 날짜가 늘면 접힌 표가 채워진다
        self.assertEqual(A.apply(o, R2, self.cfg), self.out)


class ApplyLayoutC(unittest.TestCase):
    """판 r2026-10-C(01·06 모바일 가로 막대) — 사슬·B → C·멱등·손 수정 FAIL·M 줄 기계 자리·변환 범위."""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)
        cls.B = A.convert_layout(cls.H, A.LAYOUT_B)                          # meta r2026-10-B 판(배포본 014472d 꼴 — 값은 fixture 옛 값)

    def block(self, h, cid):
        i = h.index(f"getElementById('{cid}')")
        return h[i:h.index("new Chart", i + 10)]

    def test_chain_old_to_c(self):
        o, R = self.out, self.R
        self.assertEqual(self.lay["layout_id"], "r2026-10-C")
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), ["r2026-10-C"])
        self.assertEqual(o.count("/* saero:mobile-branch 01 */"), 1)
        self.assertEqual(o.count("/* saero:mobile-branch 06 */"), 1)
        self.assertEqual(len(A.BRANCH.findall(o)), self.lay["markers"]["mobile_branch"])
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", o)), self.lay["markers"]["details"])
        self.assertEqual(A.M_LINE.findall(o), [A.m_line(self.lay)])
        self.assertIn('var M = {maxPx: 640, printMaxH: 1000, row: {"01": 26, "06": 22}, pad: {"01": 90, "06": 70}};', o)
        self.assertEqual(o.count("matchMedia("), 1)
        self.assertEqual(o.count(".scroll-fade.at-start::before{opacity:0;}"), 1)
        self.assertEqual(o.count("wrapper.classList.toggle('at-start', box.scrollLeft <= 2);"), 1)
        self.assertEqual(o.count("box.parentNode.classList.add('at-end', 'at-start'); // 페이드 둘 다 숨김"), 1)
        self.assertEqual(o.count("window.__saeroSync = sync;"), 1)
        self.assertEqual(o.count("window.__saeroMobile.scrollEnd(); }, 0); });"), 1)
        d1, d6 = self.block(o, "dailyChart"), self.block(o, "rankChart")       # 블록 안 첫 new Chart 앞에 배열이 하나씩 채워짐(apply·compare 첫 일치 앵커)
        self.assertEqual(d1.count("labels: ["), 1)
        self.assertEqual(d6.count("labels: ["), 1)
        self.assertIn("labels: [" + ",".join(f"'{x}'" for x in R["01"]["labels"]) + "]", d1)
        self.assertIn("labels: [" + ",".join(f"'{x}'" for x in R["01"]["labels"]) + "]", d6)
        self.assertIn("data: [" + ", ".join(map(str, R["01"]["노출"])) + "]", d1)
        self.assertIn("data: [" + ", ".join(map(str, R["01"]["총비용"])) + "]", d1)
        self.assertIn("data: [" + ", ".join(f"{x:.2f}" for x in R["06"]["rankChart"]) + "]", d6)
        self.assertEqual(o.count("getElementById('dailyChart')"), 1)            # 도우미는 id 리터럴을 쓰지 않는다
        self.assertEqual(o.count("getElementById('rankChart')"), 1)
        self.assertEqual(len(re.findall(r"labels:\s*\[((?:'\d+/\d+\(.\)',?)+)\]", o)), 2)   # compare "01/06 labels" 정확히 2개
        self.assertEqual(len(re.findall(rf'min-width:{R["minwidth"]}px;">\s*<canvas id="(?:dailyChart|rankChart)"', o)), 2)
        self.assertNotIn("<details", o[o.index("<script>"):])                   # 스크립트·주석에 태그 꺾쇠 없음(details 수·태그 짝)
        self.assertEqual(A.apply(o, R, self.cfg), o)                            # 값만(멱등)
        self.assertEqual(A.apply(o, R, self.cfg, layout=True), o)

    def test_b_to_c(self):
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.B), ["r2026-10-B"])
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-B ≠ config r2026-10-C — --layout 을 붙여 r2026-10-B → r2026-10-C"):
            A.apply(self.B, self.R, self.cfg)
        self.assertEqual(A.apply(self.B, self.R, self.cfg, layout=True), self.out)   # B → C 만 = 옛 → B → C 사슬과 같은 바이트

    def test_hand_edited_c_fails(self):
        for k in ("01", "06"):
            bad = self.out.replace(f"/* saero:mobile-branch {k} */", "", 1)
            for flag in (False, True):
                with self.assertRaisesRegex(A.ApplyError, "분기 표지 1개"):
                    A.apply(bad, self.R, self.cfg, layout=flag)
        dup = self.out.replace("/* saero:mobile-branch 06 */", "/* saero:mobile-branch 06 */ /* saero:mobile-branch 06 */", 1)
        with self.assertRaisesRegex(A.ApplyError, "분기 표지"):
            A.apply(dup, self.R, self.cfg)
        with self.assertRaisesRegex(A.ApplyError, "앵커가 정확히 하나가 아님"):            # M 줄이 없어진 판
            A.apply(self.out.replace("var M = {", "var MX = {", 1), self.R, self.cfg)

    def test_stale_m_line_rewritten(self):
        stale = self.out.replace("var M = {maxPx: 640, printMaxH: 1000,", "var M = {maxPx: 641, printMaxH: 999,", 1)
        self.assertNotEqual(stale, self.out)
        self.assertEqual(A.apply(stale, self.R, self.cfg), self.out)                # M 줄은 compute 가 아니라 config 에서 온다

    def test_conversion_scope(self):
        """B → C 변환은 섹션 HTML(서술 표지 포함)·min-width 텍스트를 건드리지 않는다 — 바뀌는 곳은 meta·style 끝·스크립트뿐."""
        H2 = self.H.replace('<div class="note">닷새 동안 가짜 순위 서술.</div>',
                            '<div class="note"><!-- n:01-rank:매회차 -->닷새 가짜 순위 서술.<!-- /n --></div>', 1)
        H2 = H2.replace("        4일차. 가짜 카드 서술.", "        <!-- n:06-card-가짜그룹B:매회차 -->4일차. 가짜 카드 서술.<!-- /n -->", 1)
        b2 = A.convert_layout(H2, A.LAYOUT_B)
        c2 = A.convert_b_to_c(b2, self.lay)
        blk = r"<!-- n:[^>]+-->.*?<!-- /n -->"
        self.assertEqual(len(re.findall(blk, c2, re.S)), 2)
        self.assertEqual(re.findall(blk, c2, re.S), re.findall(blk, b2, re.S))
        for n in range(1, 13):
            self.assertEqual(section(c2, n), section(b2, n), n)
        self.assertEqual(re.findall(r"min-width:\s*\d+px", c2[c2.index("<body>"):]), re.findall(r"min-width:\s*\d+px", b2[b2.index("<body>"):]))
        head_c, head_b = c2[:c2.index("<body>")], b2[:b2.index("<body>")]
        self.assertEqual(head_c.replace(A.MOBILE_CSS.rstrip("\n") + "\n", "", 1).replace('content="r2026-10-C"', 'content="r2026-10-B"', 1), head_b)
        self.assertEqual(c2[c2.index("<body>"):c2.index("<script>")], b2[b2.index("<body>"):b2.index("<script>")])


class ApplyFailsLoudly(unittest.TestCase):
    def run_cli(self, html_text, R=None, layout=True):
        td = tempfile.mkdtemp()
        try:
            h, j = os.path.join(td, "index.html"), os.path.join(td, "compute.json")
            with open(h, "w", encoding="utf-8", newline="") as f:
                f.write(html_text)
            if R is None:
                shutil.copy(FIXJ, j)
            else:
                with open(j, "w", encoding="utf-8") as f:
                    json.dump(R, f, ensure_ascii=False)
            before = md5(h)
            r = subprocess.run([sys.executable, APPLY, "--html", h, "--compute", j] + (["--layout"] if layout else []),
                               capture_output=True, text=True, encoding="utf-8")
            return r.returncode, r.stdout + r.stderr, before == md5(h)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def test_cli_ok(self):
        rc, out, same = self.run_cli(read(FIX))
        self.assertEqual(rc, 0, out)
        self.assertFalse(same)
        self.assertIn("[apply]", out)
        self.assertIn("레이아웃 판 변환(meta 없음 → r2026-10-B → r2026-10-C, details 5 · 분기 2)", out)

    def test_cli_twice_same_bytes_and_flag_required(self):
        td = tempfile.mkdtemp()
        try:
            h = os.path.join(td, "index.html")
            with open(h, "w", encoding="utf-8", newline="") as f:
                f.write(read(FIX))
            run = lambda *extra: subprocess.run([sys.executable, APPLY, "--html", h, "--compute", FIXJ, *extra], capture_output=True, text=True, encoding="utf-8")
            r = run()                                                                     # 옛 판 + --layout 없음 → FAIL, 그대로
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout", r.stdout)
            self.assertEqual(read(h), read(FIX))
            self.assertEqual(run("--layout").returncode, 0)
            m1 = md5(h)
            r = run("--layout")                                                           # 두 번째: 변환 건너뜀 · 바이트 같음
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("(변환 건너뜀) (변경 없음)", r.stdout)
            self.assertEqual(md5(h), m1)
            self.assertEqual(run().returncode, 0)                                         # 새 판이면 --layout 없이도 값만(멱등)
            self.assertEqual(md5(h), m1)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def test_missing_or_duplicate_anchor(self):
        H = read(FIX)
        for label, text in (("TOP 10 외 없음", H.replace("TOP 10 외 지역", "TOP10 밖 지역", 1)),
                            ("클릭당 평균 둘", H.replace("</body>", "<p>클릭당 평균 1원</p></body>", 1)),
                            ("집계 기간 없음", H.replace("집계 기간<b>", "집계기간<b>", 1)),
                            ("경쟁사 머리글 소제목 변경", H.replace("경쟁사 브랜드명 검색어</div>", "경쟁사 검색어 (2개)</div>", 1)),
                            ("10 표 행 3개", H.replace('<td class="name-cell">추천·콘텐츠 지면 › 가짜 D</td>\n            <td>가짜 매체</td>\n            <td class="num">40</td>', '<td class="name-cell">D</td>', 1)),
                            ("접기 CSS 자리(</style>) 없음", H.replace("</style>", "</styl>", 1)),
                            ("접기 스크립트 자리(resize 줄) 없음", H.replace("t = setTimeout(sync, 200);", "t = setTimeout(sync, 300);", 1)),
                            ("03 표 둘", H.replace("<!-- Section 4:", "<table></table>\n  <!-- Section 4:", 1)),
                            ("판 C 안내 앵커(updateEnd 의 at-end 줄) 없음", H.replace("wrapper.classList.toggle('at-end', atEnd);", "wrapper.classList.toggle('at-end', !!atEnd);", 1)),
                            ("판 C 안내 앵커(페이드 숨김 줄) 없음", H.replace("// 페이드 숨김", "// 숨김", 1)),
                            ("판 C 차트 스크립트 끝 앵커 없음", H.replace("\n});\n</script>\n", "\n}); \n</script>\n", 1)),
                            ("판 C 01 블록 시작 없음", H.replace("new Chart(document.getElementById('dailyChart'), {", "new Chart(document.getElementById('dailyChart'),{", 1))):
            with self.subTest(label=label):
                rc, out, same = self.run_cli(text)
                self.assertEqual(rc, 1, out)
                self.assertIn("[FAIL] apply:", out)
                self.assertTrue(same, "실패했는데 작업본이 바뀜")

    def test_new_group_and_unknown_competitor(self):
        R = jread(FIXJ)
        R["04"]["rows"].append(dict(R["04"]["rows"][-1], 그룹="가짜새그룹"))
        rc, out, same = self.run_cli(read(FIX), R)
        self.assertEqual(rc, 1, out)
        self.assertIn("새 그룹", out)
        self.assertTrue(same)
        R = jread(FIXJ)
        R["07"]["신규변형후보"] = []                                   # 직전 표에도 후보에도 없는 이름 → 멈춤
        rc, out, same = self.run_cli(read(FIX), R)
        self.assertEqual(rc, 1, out)
        self.assertIn("신규 변형 후보도 아닌", out)
        self.assertTrue(same)


class ComputeCompetitorGuard(unittest.TestCase):
    def test_zero_rows_fail_before_reading_csv(self):
        import compute as C
        H = read(FIX)
        self.assertEqual(C.deployed_competitors(H), ["가짜경쟁A", "가짜경쟁B"])
        R = jread(FIXJ)
        self.assertEqual(C.deployed_competitors(A.apply(H, R, load_config(), layout=True)), [r["검색어"] for r in R["07"]["경쟁사표"]])   # 접힌 표도 그대로(신규 변형 행 포함)
        td = tempfile.mkdtemp()
        try:
            bad = os.path.join(td, "prev.html")
            with open(bad, "w", encoding="utf-8") as f:
                f.write(H.replace("경쟁사 브랜드명 검색어</div>", "경쟁사 검색어 (2개)</div>", 1))   # r10 유형 — 소제목만 바뀜
            r = subprocess.run([sys.executable, COMPUTE, os.path.join(td, "없는합본"), "--competitors-html", bad, "-o", os.path.join(td, "o.json")],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("[FAIL] 직전 배포본 경쟁사표 0행", r.stdout)
            self.assertFalse(os.path.exists(os.path.join(td, "o.json")))
        finally:
            shutil.rmtree(td, ignore_errors=True)


@unittest.skipUnless(os.path.exists(os.path.join(ROOT, "work", "R3", "index.html")) and os.path.exists(os.path.join(ROOT, "work", "R3", "compute.json")),
                     "리허설 산출 work/R3 없음(구현·검증 회차 리허설 뒤에만)")
class ApplyRehearsal(unittest.TestCase):
    def test_r3_output_idempotent(self):
        H = read(os.path.join(ROOT, "work", "R3", "index.html"))
        R = jread(os.path.join(ROOT, "work", "R3", "compute.json"))
        self.assertGreater(H.count("<!-- n:"), 20)
        self.assertIn('<meta name="report-layout" content="r2026-10-C">', H)               # 리허설 R3 = 판 C(meta 로 판 선택 — --layout 없이)
        self.assertEqual(A.apply(H, R, load_config()), H)


if __name__ == "__main__":
    unittest.main(verbosity=1)
