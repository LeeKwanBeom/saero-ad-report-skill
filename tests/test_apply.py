#!/usr/bin/env python3
"""scripts/apply.py 시험(E2 저장소화 2026-10-06 + 레이아웃 판 r2026-10-B 회차 2 + 판 r2026-10-C 01 차트 회차 1 + 판 r2026-10-D 모바일 기간 접기 2026-10-07 +
판 r2026-10-E 01 모바일 터치 날짜 2026-10-08 + 판 r2026-10-F 광고비 잔액 카드 2026-10-09 + 판 r2026-10-G 보고서 더 받기 2026-10-12 +
판 r2026-10-H 07 정식표 접기 2026-10-17 + 판 r2026-10-I 콘텐츠 지면 빼기 2026-10-23 + 판 r2026-10-J 불필요 항목 빼기 2026-10-23 오후 + 판 r2026-10-K 01 요일 카드 2026-10-26) + compute.py 직전 경쟁사표 0행 가드 ·
콘텐츠 재발 감시(content_days) · 06 카드 규칙(card_groups — 판 J).

fixture = tests/fixtures/layout_old.html(배포본 앵커 마크업 발췌 — 숫자·검색어·경쟁사·그룹 이름 가짜, 서술 표지·레이아웃 meta 없는 옛 판) +
          tests/fixtures/layout_old.compute.json(같은 가짜 값의 compute 출력 꼴 — 03.rows 만 10일(12/29~1/7)이라 "최근 7 + 접힌 3" 분배가 보인다).
- 판 고르기: meta 없음 + --layout 없음 → `[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout …`(옛 배치로 쓰지 않음, 작업본 그대로) ·
  meta 다름·details 수 다름 → FAIL · --layout 변환 = 사슬(옛 → r2026-10-B: meta + details 5 + 접기 CSS·스크립트 → r2026-10-C: 분기 표지 2 ·
  01·06 템플릿 · 분기 도우미 · 왼쪽 페이드 · 안내 4줄 → r2026-10-D: 버튼 CSS · 01 비용 라벨 간격 2곳 · 판 D 분기 도우미 → r2026-10-E: 01 모바일 터치 축 한 줄
  → r2026-10-F: .kpi-wide CSS · KPI 카드 넷 아래 광고비 잔액 카드 하나 → r2026-10-G: 04·05 추가 블록(test_extras) → r2026-10-H: 07 정식표 아래 접힌 표 하나 — details 6),
  두 번째(변환 건너뜀)는 바이트 같음.
- 판 F(ApplyLayoutF): meta r2026-10-E 판 + --layout 없음 → `레이아웃 판 meta r2026-10-E ≠ config r2026-10-F — --layout …` · + --layout → 사슬과 같은 바이트 ·
  E → F 가 바꾸는 곳 = meta · .kpi-wide CSS · 카드 하나뿐(카드 넷·섹션 바이트 그대로 · 기존 KPI 정규식에 새 카드 안 잡힘) · 값·보조 줄 매 회차(ok · 일분 없음 · fail —
  실패 → 성공 글자 남김 0) · compute.json "잔액" 없음·꼴 다름 FAIL · 손 수정 E(넷째 카드 끝 앵커 없음·표지 있음)·F(카드 지움·둘·01 섹션 뒤) FAIL.
- 판 E(ApplyLayoutE — config 는 판 F, E 는 사슬 중간): meta r2026-10-D 판 + --layout 없음 → `레이아웃 판 meta r2026-10-D ≠ config r2026-10-F — --layout …` · + --layout → 사슬과 같은 바이트 ·
  D → E 가 바꾸는 곳 = meta · 01 mobile() interaction 한 줄(axis:'y')뿐 · PC 01·09 interaction 그대로 · 그 줄을 손으로 바꾼 D 판(이미 axis 있음 포함) → FAIL(변환 안 함).
- 판 D(ApplyLayoutD — config 는 판 F, D 는 사슬 중간): meta r2026-10-B·r2026-10-C 판 + --layout 없음 → `레이아웃 판 meta r2026-10-B|C ≠ config r2026-10-F — --layout …` · + --layout → 사슬과 같은 바이트 ·
  판 C 도우미·비용 라벨 간격 줄을 손으로 바꾼 C 판 → FAIL(변환 안 함) · 분기 표지 하나 지운 D 판 → FAIL "분기 표지" · 묵은 M 줄(recent 포함) → config 값으로 다시 씀 ·
  판 C 꼴 M 줄(recent 없음)이 남은 D 판 → FAIL · C → D 변환이 섹션 HTML·서술 표지·min-width·배열·안내 스크립트를 건드리지 않음(바뀌는 곳 = meta·버튼 CSS·비용 간격 2·도우미) ·
  HTML 에 버튼 태그·"이전 N일" 문구 0(03 summary 하나뿐) · B → C 중간 단계 범위도 그대로.
- 판 H(ApplyLayoutH, 2026-10-17 — 07 정식표 접기): G → H = 사슬 바이트 · `--layout` 없이 G 면 `레이아웃 판 meta r2026-10-G ≠ config r2026-10-H — --layout …` ·
  바뀌는 곳 = meta · 정식표 wrapper 바로 뒤 접힌 표 뼈대 하나뿐(같은 thead · 범례·클릭 1건 목록 앞) · 위 표 = compute 정식표 앞 top_rows_07 행 · 접힌 표 = 나머지(이어 읽으면 정식표 순서) ·
  summary `나머지 N행(클릭 a~b건 · 합 M건 · X원) 펼치기`(a = b 면 `클릭 a건` · 행 ≤ K 면 `나머지 0행 펼치기` + 빈 tbody — details 6 고정) · 회차마다 행 수가 오가도 옛 글자 0 ·
  묵은 summary 다시 씀 · 경쟁사·클릭 1건·클릭 0 summary 그대로 · top_rows_07 1 미만·정수 아님 FAIL · 손 수정 G(정식표 thead·wrapper 없음 · 접기 이미 있음)·H(접기 지움·옮김·둘) FAIL.
  (판 G 까지의 사슬 중간 판은 `at(cfg, lid)` — config 를 그 판 + 접기 5개로 둔 시험용 사본 · 판 H 는 접기 6개 그대로)
- 판 I(ApplyLayoutI, 2026-10-23 — 콘텐츠 지면 빼기): H → I = 사슬 바이트 · `--layout` 없이 H 면 `레이아웃 판 meta r2026-10-H ≠ config r2026-10-I — --layout …` ·
  바뀌는 곳 = meta · 01 ① 머리글·칸 머리 둘 · 10 구역 통째 · placementChart 스크립트 블록 · 11·12 주석·배지 → 10·11 · 고정 표지 12-basis 한 곳뿐(구역 2~9·CSS 바이트 그대로 ·
  다른 서술 표지 안쪽 그대로 · 10-* 표지는 구역째 사라짐) · ① 5칸 = compute 표5 · 캔버스 7 · 구역 주석 1~11 · 멱등 · 판 H 경로(at(cfg, H))는 7칸·placementChart·10 표 그대로 ·
  손 수정 H(① 칸 머리 없음 · 10 구역에 다른 캔버스 · placementChart 블록 없음 · 10-* 표지가 구역 밖 · 12-basis 다른 10번 · 마지막 구역 아님 · 배지 다름)·
  I(구역 12 주석 · placementChart · 배지 · ① 7칸 · 캔버스 8 · 옛 머리글 · Action items 이름) FAIL.
- 판 J(ApplyLayoutJ, 2026-10-23 오후 — 불필요 항목 빼기, 판 K 부터 사슬 중간 — config 를 판 J 로 둔 사본): I → J = 사슬 바이트 · `--layout` 없이 I 면 `레이아웃 판 meta r2026-10-I ≠ config r2026-10-J — --layout …` ·
  바뀌는 곳 = 고정 글만(meta · 제목 · KPI 평균 클릭률 보조 줄 · KPI 클릭 단위 · groupChart 이름 · 04-foot·07-src·12-desc · 12-basis 세 줄 · 07-legend 끝 · 네 표지 종류 — 줄 단위 diff 가 허용 목록 밖 0) ·
  값 갈래(KPI 건 · 07 노출 쉼표·'적음' · 04 '(M/D 신규)' 기한 · 06 카드 집합 — 밖이 된 카드 지움·없는 카드 FAIL · 판 G 블록 머리·알 수 없음 %·스킬 줄 0) · 멱등 ·
  손 수정 I(고정 표지 다른 글 · 12-basis 줄 없음 · KPI 보조 줄 없음 · 07-legend 에 이미 한 구)·J(뺀 고정 글 되살림 · 표지 매회차 · 07-legend 끝 없음 · KPI 클릭 '회' · 카드 블록에 다른 표지) FAIL ·
  직전 판 I·J 읽기 같음(G3 — compute prev_period_end · deployed_competitors · reportlib action_section 의 이월 줄 · apply 04 이름 칸 그룹 키).
  (판 I 시험 ApplyLayoutI 는 config 를 판 I 로 둔 사본 `at(cfg, LAYOUT_I)` 로 돈다 — 판 I 몫은 사슬 중간)
- 06 카드 규칙(ComputeCardRule — 판 J 결정 5 · 완료 기준 "시험(새 그룹 카드)"): compute card_groups = 새 그룹(일차 < new_days) · 승격 그룹 — 오래된 그룹·최근 7일 노출 0·노원역 0 ·
  validate "06번 카드 그룹" 이 같은 판정(CSV 로 따로) · 새 그룹 카드가 없으면·오래된 그룹에 '(M/D 신규)' 가 남으면 FAIL.
- compute 콘텐츠 재발 감시(ComputeContentWatch): 콘텐츠 노출 0 이면 (None, None, []) · 줄 0 / since 뒤 노출 있으면 [주의] 한 줄(날짜·노출) · 첫날·끝날.
- 멱등: 같은 compute.json 으로 두 번 돌리면 바이트 같음(--layout 있음·없음, 서술 표지를 넣은 fixture 도 — 표지 안쪽 바이트 불변·details 밖).
- 앵커·행 수: masthead·og·KPI·차트·01 표 5행(최신 위 — 2026-10-15)·순위 5칸(오름차순 그대로)·03 = 합계 맨 위 + 최근 7일 최신 위 + 접힌 표 나머지 최신 위 ·
  04·06·07 정식표/목록/경쟁사표·08·10 이 compute 값과 같음. 동률은 직전 순서(클릭 1건 목록) · 신규 변형 행 = config competitor_defaults.
- summary 기계 자리(막음 M2): 03 "이전 N일(M/D~M/D)"·07 "(N개 · 펼치기)"·경쟁사 "표 N행"·08 "(N개 지역·클릭 M건)" — 옛 값으로 바꿔 둔 판도 다시 쓰고,
  일수 ≤ recent_days 면 접힌 표 0행 + "이전 0일 펼치기"(details 5 그대로).
- 05 mediaChart(ApplyMediaLabels, 2026-10-14): 라벨·색 = compute 05.top5 순서(fixture HTML 순서와 다름 · 4·5위 바뀜 · 새 매체 '-' 없는 이름·'ZUM - PC' ·
  직전 블록의 같은 매체 줄 나눔 유지 · 멱등·되돌리면 바이트 그대로) — validate check_media_top5 와 같은 읽기로 대조 · 따옴표 이름·낯선 유형·빈 조각·색 배열 없음 → ApplyError.
- 시끄러운 실패: 앵커가 없거나 둘이면·새 04 그룹·직전/후보 밖 경쟁사 → `[FAIL] apply:` exit 1, 작업본 바이트 그대로.
- compute.py: --competitors-html 의 경쟁사표 0행(소제목만 바꾼 사본 — 탐색 프로브 r10 유형) → `[FAIL]` exit 1(합본을 읽기 전) · 접힌 경쟁사표도 그대로 읽음.
- 판 K(ApplyLayoutK, 2026-10-26 — 01 요일 카드, config 판): J → K = 사슬 바이트 · `--layout` 없이 J 면 `레이아웃 판 meta r2026-10-J ≠ config r2026-10-K — --layout …` ·
  바뀌는 곳 = meta · 01 차트 카드 뒤 카드 하나 · 분기 도우미 뒤 차트 블록 하나뿐(다른 구역·01 차트·서술 표지·CSS 바이트 그대로 · 01 첫 일치 앵커 글자 0 · 색 = #cdeee7 하나) ·
  값(막대·clicks·보조 줄 = compute 01.요일 · 0일 요일 null·0~1일 · 8~9일 · 정수 클릭 10.0 · 되돌리면 바이트 그대로) · "01.요일" 없음·꼴 다름 FAIL ·
  손 수정 J(요일 표지 이미 있음 · 차트 카드와 ① 사이 다른 것 · 도우미가 스크립트 끝 아님 · ① 머리글 둘)·K(카드 지움 · 카드 ① 뒤 · 블록 도우미 앞 · 블록 지움 · labels · clicks 둘 · sub 둘) FAIL.
  (판 J 시험 ApplyLayoutJ 는 config 를 판 J 로 둔 사본 `at(cfg, LAYOUT_J)` 로 돈다 — 판 K 부터 판 J 는 사슬 중간 · 판 I·J 캔버스 7)
- compute 요일 평균(ComputeWeekday — 판 K): 검색 지면 · 제외 그룹 뺌 · 28일 요일마다 4일 · 행 없는 날 0 · 반올림(250.5 → 250 · 10.25 → 10.2 · 6.75 → 6.8) · 0일 요일 노출 0·클릭 None.
- 리허설 산출(work/RX/same/index.html + compute.json, 서술 표지·레이아웃 판 r2026-10-K 있음 — 2026-10-26 구현 리허설: 운영 배포본(판 J 6bc57c8) 사본을 apply --layout 으로 바꾼 것 — 같은 기간이라 서술 그대로)이 있으면 그것도 멱등(없으면 건너뜀) — A.apply() 직접(meta 로 판 선택).
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


def at(cfg, lid):
    """config 를 사슬 중간 판 lid 로 둔 시험용 사본 — 판 G 까지는 접기 5개(markers.details 5 — 판 H 가 07 정식표 접기 하나를 더한다 · 판 I 도 6) ·
    판 K 전(요일 카드 없음)은 캔버스 7(판 I·J — 판 H 까지는 캔버스를 세지 않는다) · weekday_card 없음. 여러 번 거쳐도 같은 사본(값을 빼지 않고 정해 둔다)."""
    lay = dict(cfg["report_layout"], layout_id=lid)
    mk = dict(lay["markers"])
    if lid not in (A.LAYOUT_H, A.LAYOUT_I, A.LAYOUT_J, A.LAYOUT_K):
        mk["details"] = 5
    if lid not in A.WEEKDAY_LAYOUTS:
        mk["canvases"] = 7
        mk.pop("weekday_card", None)
    lay["markers"] = mk
    return dict(cfg, report_layout=lay)


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
        want = [b.replace("<!-- n:08-note:매회차 -->", "<!-- n:08-note:고정 -->") for b in re.findall(blk, H2, re.S)]   # 판 J 변환은 08-note 종류만 고정으로
        self.assertEqual(re.findall(blk, o1, re.S), want)                         # 변환·값 교체 모두 표지 안쪽 바이트 불변
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
        s1, s3, s4, s6, s7, s8 = (section(o, n) for n in (1, 3, 4, 6, 7, 8))
        self.assertEqual([cells(t)[0] for t in rows(s1) if "<td" in t], [r["날짜"] for r in R["01"]["표5"]][::-1])
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
        r1 = [cells(t) for t in rows(s1) if "<td" in t]
        self.assertEqual(r1[0][0], R["01"]["표5"][-1]["날짜"])                                           # 01 표 = 최신 위(2026-10-15 — 결정 4 (가) 의 표 부분만 바꿈)
        self.assertEqual({len(r) for r in r1}, {5})                                                     # 판 I — 5칸(날짜·노출·클릭·CTR·CPC)
        self.assertEqual([r[4] for r in r1], [f"{r['CPC']:,}원" for r in R["01"]["표5"]][::-1])         # 값도 같은 행에
        self.assertEqual(len(re.findall(r'<td class="num ctr-high">', s1)), sum(r["hl"] for r in R["01"]["표5"]))
        self.assertEqual([cells(t)[1].split("(")[0].strip() for t in rows(s4)], [r["그룹"] for r in R["04"]["rows"]])
        self.assertIn("(1/2 신규)", s4)                                                                  # 이름 칸 메모는 직전 행 그대로
        self.assertIn("(1/2 등록, 6일차)", s6)
        self.assertIn('font-weight:800;color:var(--mint-dark);">1.55위', s6)
        main7 = [cells(t) for t in rows(s7[:s7.index("클릭 1건 검색어")]) if "<td" in t]                  # 위 표 + 접힌 표(판 H) — 머리줄 빼고
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
        self.assertNotIn("placementChart", o)                                                            # 판 I — 지면 구역·차트 없음(10 표는 ApplyLayoutI 의 판 H 경로가 본다)
        self.assertEqual(re.findall(r"<!-- Section (\d+):", o), [str(n) for n in range(1, 12)])


def media_block(h):
    """05 mediaChart (라벨 글, 값, 색) — validate check_media_top5 와 같은 읽기(라벨 줄을 띄어쓰기로 이음)."""
    i = h.index("getElementById('mediaChart')")
    blk = h[i:h.index("new Chart", i + 10)]
    lab = re.search(r"labels:\s*\[(.*?)\],\n", blk, re.S).group(1)
    labels = [re.sub(r"[\[\]']", "", x).replace(",", " ").strip() for x in re.findall(r"\[[^\]]*\]", lab)]
    values = [int(x) for x in re.search(r"label:\s*'노출수'[^\n]*\n\s*data:\s*\[([^\]]*)\]", blk).group(1).split(",")]
    colors = re.search(r"backgroundColor:\s*\[([^\]]*)\]", blk).group(1).replace(" ", "").split(",")
    return labels, values, colors


def media_want(top5):
    """validate 의 기대값 꼴 — 이름의 ' - '·'-' 를 띄어쓰기로, 색 = 플레이스 mint · 그 밖 ink."""
    return ([t["매체"].replace(" - ", " ").replace("-", " ") for t in top5], [t["노출"] for t in top5],
            ["mint" if t["유형"] == "플레이스" else "ink" for t in top5])


class ApplyMediaLabels(unittest.TestCase):
    """05 mediaChart 라벨·색 = compute 05.top5 순서(2026-10-14 — 값만 바꾸던 때 4·5위가 바뀐 날 라벨·색이 옛 순서로 남아 validate FAIL)."""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)

    def with_top5(self, top5):
        R2 = json.loads(json.dumps(self.R))
        R2["05"]["top5"] = top5
        return R2

    def test_fixture_follows_compute_order(self):
        # fixture HTML 라벨 순서(매체 모바일·매체 PC·검색 모바일 …)는 compute 순서(매체 모바일·검색 모바일·매체 PC …)와 다르다 — 고친 뒤엔 compute 순서
        self.assertNotEqual(media_block(self.H)[0], media_want(self.R["05"]["top5"])[0])
        self.assertEqual(media_block(self.out), media_want(self.R["05"]["top5"]))
        self.assertIn("labels: [['가짜매체','모바일'],['가짜검색','모바일'],['가짜매체','PC'],['가짜검색','PC'],['가짜기타','모바일']],", self.out)
        self.assertIn("backgroundColor: [mint, ink, mint, ink, ink]", self.out)

    def test_rank_swap_like_1014(self):
        top = json.loads(json.dumps(self.R["05"]["top5"]))
        top[3], top[4] = top[4], top[3]                                          # 4·5위가 자리를 바꾼 날(10/14 — 통합검색 PC 836 · MLB파크 828 꼴)
        top[3]["노출"], top[4]["노출"] = 130, 90
        R2 = self.with_top5(top)
        o2 = A.apply(self.out, R2, self.cfg)
        self.assertEqual(media_block(o2), media_want(top))
        self.assertEqual(A.apply(o2, R2, self.cfg), o2)                           # 멱등
        self.assertEqual(A.apply(o2, self.R, self.cfg), self.out)                 # 되돌리면 바이트 그대로

    def test_new_media_and_kept_split(self):
        top = json.loads(json.dumps(self.R["05"]["top5"]))
        top[3] = {"매체": "네이버 블로그", "노출": 120, "유형": "혼합"}               # '-' 없는 이름 → 한 줄
        top[4] = {"매체": "ZUM - PC", "노출": 80, "유형": "파워링크"}
        o2 = A.apply(self.out, self.with_top5(top), self.cfg)
        self.assertEqual(media_block(o2), media_want(top))
        self.assertIn("['네이버 블로그'],['ZUM','PC']]", o2)
        # 직전 블록에 같은 매체가 다른 줄 나눔으로 있으면 그 나눔 그대로(사람이 나눈 두 줄)
        o3 = o2.replace("['네이버 블로그']", "['네이버','블로그']", 1)
        o4 = A.apply(o3, self.with_top5(top), self.cfg)
        self.assertIn("['네이버','블로그'],['ZUM','PC']]", o4)
        self.assertEqual(media_block(o4), media_want(top))

    def test_fails_loudly(self):
        bad_name = json.loads(json.dumps(self.R["05"]["top5"]))
        bad_name[0]["매체"] = "가짜'매체 - 모바일"
        bad_kind = json.loads(json.dumps(self.R["05"]["top5"]))
        bad_kind[1]["유형"] = "모름"
        bad_split = json.loads(json.dumps(self.R["05"]["top5"]))
        bad_split[2]["매체"] = "가짜매체 - "
        for top, msg in ((bad_name, "따옴표"), (bad_kind, "유형"), (bad_split, "빈 조각")):
            with self.assertRaisesRegex(A.ApplyError, msg):
                A.apply(self.out, self.with_top5(top), self.cfg)
        i = self.out.index("getElementById('mediaChart')")
        j = self.out.index("new Chart", i + 10)
        no_col = self.out[:i] + re.sub(r"backgroundColor:\s*\[[^\]]*\]", "borderRadius:6", self.out[i:j], count=1) + self.out[j:]
        with self.assertRaisesRegex(A.ApplyError, "backgroundColor 0개"):
            A.apply(no_col, self.R, self.cfg)


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
        with self.assertRaisesRegex(A.ApplyError, "details 5개"):
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


class ApplyLayoutD(unittest.TestCase):
    """판 r2026-10-D(모바일 01·06 기간 접기 — 판 C 가로 막대 위) — 사슬(옛 → B → C → D)·B → D·C → D·멱등·손 수정 FAIL·M 줄 기계 자리·변환 범위."""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)
        cls.B = A.convert_layout(cls.H, A.LAYOUT_B)                          # meta r2026-10-B 판(배포본 014472d 꼴 — 값은 fixture 옛 값)
        cls.C = A.convert_b_to_c(cls.B, cls.lay)                             # meta r2026-10-C 판(배포본 479d866·60d2aee 꼴 — 배열은 빈 [], 값은 apply 가 채움)

    def block(self, h, cid):
        i = h.index(f"getElementById('{cid}')")
        return h[i:h.index("new Chart", i + 10)]

    def helper(self, h):
        i = h.index("/* saero:mobile-helper")
        return h[i:h.index("\n})();\n", i) + len("\n})();\n")]

    def test_chain_old_to_d(self):
        o, R = self.out, self.R
        self.assertEqual(self.lay["layout_id"], "r2026-10-K")                     # config 는 판 K — 판 D 몫은 사슬 끝(K) 결과에 그대로 남는다
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), ["r2026-10-K"])
        self.assertEqual(o.count("/* saero:mobile-branch 01 */"), 1)
        self.assertEqual(o.count("/* saero:mobile-branch 06 */"), 1)
        self.assertEqual(len(A.BRANCH.findall(o)), self.lay["markers"]["mobile_branch"])
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", o)), self.lay["markers"]["details"])
        self.assertEqual(A.M_LINE.findall(o), [A.m_line(self.lay)])
        self.assertIn('var M = {maxPx: 640, printMaxH: 1000, row: {"01": 26, "06": 22}, pad: {"01": 90, "06": 70}, recent: {"01": 14, "06": 14}};', o)
        self.assertEqual(A.M_LINE_C.findall(o), [])                              # 판 C 꼴 M 줄은 남지 않는다
        self.assertEqual(o.count("matchMedia("), 1)
        self.assertEqual(o.count(".scroll-fade.at-start::before{opacity:0;}"), 1)   # 판 C 몫 그대로
        self.assertEqual(o.count(".chart-fold{"), 1)                              # 판 D 버튼 CSS
        self.assertEqual(o.count("/* saero:mobile-helper — 판 D"), 1)
        self.assertEqual(o.count("/* saero:mobile-helper"), 1)
        self.assertEqual(o.count("createElement('button')"), 1)
        for old, new in A.COSTGAP_C_TO_D:                                         # 01 비용 라벨 간격 = 그리는 data
            self.assertEqual(o.count(new), 1)
            self.assertEqual(o.count(old), 0)
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
        self.assertEqual(len(re.findall(r"labels:\s*\[((?:'\d+/\d+\(.\)',?)+)\]", o)), 2)   # compare "01/06 labels" 정확히 2개(배열 1벌)
        self.assertEqual(len(re.findall(rf'min-width:{R["minwidth"]}px;">\s*<canvas id="(?:dailyChart|rankChart)"', o)), 2)
        self.assertNotIn("<details", o[o.index("<script>"):])                   # 스크립트·주석에 태그 꺾쇠 없음(details 수·태그 짝)
        self.assertNotIn("<button", o)                                          # 버튼은 화면에서만(HTML 텍스트에 태그 0)
        self.assertEqual(len(re.findall(r"이전 \d+일", o)), 1)                  # "이전 N일" 글자는 03 summary 하나뿐 — 01·06 버튼 문구는 런타임에 labels 로(HTML 기계 자리 0)
        self.assertEqual(A.apply(o, R, self.cfg), o)                            # 값만(멱등)
        self.assertEqual(A.apply(o, R, self.cfg, layout=True), o)

    def test_b_and_c_to_d(self):
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.B), ["r2026-10-B"])
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.C), ["r2026-10-C"])
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-B ≠ config r2026-10-K — --layout 을 붙여 r2026-10-B → r2026-10-K"):
            A.apply(self.B, self.R, self.cfg)
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-C ≠ config r2026-10-K — --layout 을 붙여 r2026-10-C → r2026-10-K"):
            A.apply(self.C, self.R, self.cfg)
        self.assertEqual(A.apply(self.B, self.R, self.cfg, layout=True), self.out)   # B → C → D → E → F → G → H → I = 옛 → B → … → I 사슬과 같은 바이트
        self.assertEqual(A.apply(self.C, self.R, self.cfg, layout=True), self.out)   # C → D → E → F → G → H → I 도 같은 바이트
        self.assertEqual(A.chain("r2026-10-C", "r2026-10-D"), [A.convert_c_to_d])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-D"), [A.convert_b_to_c, A.convert_c_to_d])
        self.assertEqual(A.chain("r2026-10-D", "r2026-10-D"), [])
        self.assertIsNone(A.chain("r2026-10-D", "r2026-10-C"))                       # 거꾸로는 없다
        with self.assertRaisesRegex(A.ApplyError, "이 판에서 바꾸는 변환은 없음"):
            A.apply(self.out, self.R, at(self.cfg, "r2026-10-C"), layout=True)

    def test_hand_edited_c_fails(self):
        """C → D 변환 앵커 — 판 C 도우미가 템플릿과 다르거나·비용 라벨 간격 줄이 없거나·도우미가 둘이면 변환하지 않는다."""
        cases = (("도우미 한 줄 바뀜", self.C.replace("    if (!m) scrollEnd();\n", "    if (!m) { scrollEnd(); }\n", 1), "판 C 분기 도우미가 템플릿"),
                 ("비용 라벨 간격 줄 바뀜", self.C.replace("Number(data.datasets[0].data[i])", "Number(data.datasets[0].data[i] || 0)", 1), "앵커가 정확히 하나가 아님"),
                 ("도우미 표지 둘", self.C.replace("</script>\n", "/* saero:mobile-helper */\n</script>\n", 1), "분기 도우미 시작 표지가 2개"))
        for label, bad, msg in cases:
            with self.subTest(label=label):
                self.assertNotEqual(bad, self.C)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, self.R, self.cfg, layout=True)

    def test_hand_edited_d_fails(self):
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
        with self.assertRaisesRegex(A.ApplyError, "앵커가 정확히 하나가 아님"):            # recent 가 빠진 판 C 꼴 M 줄 — 판 D 도우미가 읽을 값이 없다
            A.apply(A.M_LINE.sub(A.m_line_c(self.lay), self.out, count=1), self.R, self.cfg)

    def test_stale_m_line_rewritten(self):
        stale = (self.out.replace("var M = {maxPx: 640, printMaxH: 1000,", "var M = {maxPx: 641, printMaxH: 999,", 1)
                 .replace('recent: {"01": 14, "06": 14}', 'recent: {"01": 13, "06": 15}', 1))
        self.assertEqual(stale.count('recent: {"01": 13, "06": 15}'), 1)
        self.assertEqual(A.apply(stale, self.R, self.cfg), self.out)                # M 줄은 compute 가 아니라 config 에서 온다
        cfg2 = json.loads(json.dumps(self.cfg))
        cfg2["report_layout"]["mobile"]["recent_days"] = {"01": 7, "06": 21}
        o2 = A.apply(self.out, self.R, cfg2)
        self.assertIn('recent: {"01": 7, "06": 21}};', o2)
        self.assertEqual(o2.replace('recent: {"01": 7, "06": 21}', 'recent: {"01": 14, "06": 14}', 1), self.out)   # 바뀌는 곳은 M 줄뿐

    def test_conversion_scope_c_to_d(self):
        """C → D 변환은 섹션 HTML(서술 표지 포함)·min-width 텍스트·배열·01/06 블록 나머지·안내 스크립트를 건드리지 않는다 —
        바뀌는 곳은 meta · style 끝(버튼 CSS) · 01 비용 라벨 간격 두 곳 · 분기 도우미뿐."""
        H2 = self.H.replace('<div class="note">닷새 동안 가짜 순위 서술.</div>',
                            '<div class="note"><!-- n:01-rank:매회차 -->닷새 가짜 순위 서술.<!-- /n --></div>', 1)
        H2 = H2.replace("        4일차. 가짜 카드 서술.", "        <!-- n:06-card-가짜그룹B:매회차 -->4일차. 가짜 카드 서술.<!-- /n -->", 1)
        c2 = A.convert_b_to_c(A.convert_layout(H2, A.LAYOUT_B), self.lay)
        d2 = A.convert_c_to_d(c2, self.lay)
        blk = r"<!-- n:[^>]+-->.*?<!-- /n -->"
        self.assertEqual(len(re.findall(blk, d2, re.S)), 2)
        self.assertEqual(re.findall(blk, d2, re.S), re.findall(blk, c2, re.S))
        for n in range(1, 13):
            self.assertEqual(section(d2, n), section(c2, n), n)
        self.assertEqual(re.findall(r"min-width:\s*\d+px", d2[d2.index("<body>"):]), re.findall(r"min-width:\s*\d+px", c2[c2.index("<body>"):]))
        head_d, head_c = d2[:d2.index("<body>")], c2[:c2.index("<body>")]
        self.assertEqual(head_d.replace(A.MOBILE_CSS_D.rstrip("\n") + "\n", "", 1).replace('content="r2026-10-D"', 'content="r2026-10-C"', 1), head_c)
        self.assertEqual(d2[d2.index("<body>"):d2.index("<script>")], c2[c2.index("<body>"):c2.index("<script>")])
        back = d2.replace(self.helper(d2), self.helper(c2), 1)
        for old, new in A.COSTGAP_C_TO_D:
            back = back.replace(new, old, 1)
        self.assertEqual(back[back.index("<body>"):], c2[c2.index("<body>"):])   # 스크립트에서 바뀐 곳 = 도우미 + 비용 라벨 간격 두 곳뿐
        self.assertEqual(self.helper(d2), A.MOBILE_JS.lstrip("\n").replace("@@M@@", A.m_line(self.lay)))

    def test_conversion_scope_b_to_c(self):
        """B → C 변환(사슬 중간)은 섹션 HTML(서술 표지 포함)·min-width 텍스트를 건드리지 않는다 — 바뀌는 곳은 meta·style 끝·스크립트뿐(판 C 꼴 M 줄)."""
        H2 = self.H.replace('<div class="note">닷새 동안 가짜 순위 서술.</div>',
                            '<div class="note"><!-- n:01-rank:매회차 -->닷새 가짜 순위 서술.<!-- /n --></div>', 1)
        b2 = A.convert_layout(H2, A.LAYOUT_B)
        c2 = A.convert_b_to_c(b2, self.lay)
        for n in range(1, 13):
            self.assertEqual(section(c2, n), section(b2, n), n)
        head_c, head_b = c2[:c2.index("<body>")], b2[:b2.index("<body>")]
        self.assertEqual(head_c.replace(A.MOBILE_CSS.rstrip("\n") + "\n", "", 1).replace('content="r2026-10-C"', 'content="r2026-10-B"', 1), head_b)
        self.assertEqual(c2[c2.index("<body>"):c2.index("<script>")], b2[b2.index("<body>"):b2.index("<script>")])
        self.assertEqual(A.M_LINE_C.findall(c2), [A.m_line_c(self.lay)])
        self.assertEqual(self.helper(c2), A.MOBILE_JS_C.lstrip("\n").replace("@@M@@", A.m_line_c(self.lay)))


class ApplyLayoutE(unittest.TestCase):
    """판 r2026-10-E(01 모바일 터치 날짜 — 판 D 위, config 는 판 I) — D → E · 사슬과 같은 바이트 · 바뀌는 곳 = meta·터치 축 한 줄 · 손 수정 D FAIL."""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)
        cls.cfg_d = at(cls.cfg, "r2026-10-D")
        cls.D = A.apply(cls.H, cls.R, cls.cfg_d, layout=True)                    # meta r2026-10-D 판(배포본 04abd00 꼴 — 값 채움)
        cls.cfg_e = at(cls.cfg, "r2026-10-E")
        cls.E = A.apply(cls.H, cls.R, cls.cfg_e, layout=True)                    # meta r2026-10-E 판(사슬 끝이 E 인 값 채운 판)

    def test_d_to_e(self):
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.D), ["r2026-10-D"])
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-D ≠ config r2026-10-K — --layout 을 붙여 r2026-10-D → r2026-10-K"):
            A.apply(self.D, self.R, self.cfg)
        self.assertEqual(A.apply(self.D, self.R, self.cfg_e, layout=True), self.E)   # D → E = 옛 → B → C → D → E 사슬과 같은 바이트
        self.assertEqual(A.apply(self.D, self.R, self.cfg, layout=True), self.out)   # D → E → F → G → H 도 사슬과 같은 바이트
        self.assertEqual(A.chain("r2026-10-D", "r2026-10-E"), [A.convert_d_to_e])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-E"), [A.convert_b_to_c, A.convert_c_to_d, A.convert_d_to_e])
        self.assertEqual(A.chain("r2026-10-E", "r2026-10-E"), [])
        self.assertIsNone(A.chain("r2026-10-E", "r2026-10-D"))                       # 거꾸로는 없다
        self.assertEqual(A.apply(self.out, self.R, self.cfg), self.out)              # 값만(멱등)
        self.assertEqual(A.apply(self.out, self.R, self.cfg, layout=True), self.out)

    def test_touch_axis_only_in_01_mobile(self):
        o = self.out
        old, new = A.TOUCH_D_TO_E
        self.assertEqual(o.count(new), 1)
        self.assertEqual(o.count(old), 0)
        b01, b06 = o.index("/* saero:mobile-branch 01 */"), o.index("/* saero:mobile-branch 06 */")
        mob = o.index("function mobile(){", b01)
        self.assertTrue(b01 < mob < o.index(new) < b06)                              # 01 블록의 mobile() 안
        self.assertIn("indexAxis: 'y'", o[mob:o.index(new)])                          # 가로 막대 모양(날짜 세로축)과 같은 options
        self.assertEqual(o.count("axis:'y'"), 1)
        self.assertEqual(o[b01:mob].count("interaction: {mode:'index', intersect:false},"), 1)        # PC 01 은 그대로(세로 콤보 — x 가 맞음)
        pc = "interaction: {mode:'index', intersect:false},"
        self.assertEqual(o.count(pc), self.H.count(pc) + 1)                                           # PC 01(템플릿) + 01 밖(배포본 09 hourlyChart · fixture 0)은 그대로

    def test_conversion_scope_d_to_e(self):
        """D → E 가 바꾸는 곳은 meta 와 01 모바일 interaction 한 줄뿐(서술 표지·섹션 HTML·배열·도우미·M 줄 그대로)."""
        e = A.convert_d_to_e(self.D, self.lay)
        self.assertEqual(e, self.E)
        back = e.replace(A.TOUCH_D_TO_E[1], A.TOUCH_D_TO_E[0], 1).replace('content="r2026-10-E"', 'content="r2026-10-D"', 1)
        self.assertEqual(back, self.D)

    def test_hand_edited_d_fails(self):
        old = A.TOUCH_D_TO_E[0]
        cases = (("터치 줄을 손으로 이미 고침", self.D.replace(old, A.TOUCH_D_TO_E[1], 1)),
                 ("터치 줄 다음 padding 바뀜", self.D.replace(old, old.replace("right: 64", "right: 60"), 1)),
                 ("터치 줄 둘", self.D.replace("</script>\n", "/*\n" + old + "\n*/\n</script>\n", 1)))
        for label, bad in cases:
            with self.subTest(label=label):
                self.assertNotEqual(bad, self.D)
                with self.assertRaisesRegex(A.ApplyError, "앵커가 정확히 하나가 아님"):
                    A.apply(bad, self.R, self.cfg, layout=True)


class ApplyLayoutF(unittest.TestCase):
    """판 r2026-10-F(광고비 잔액 카드 — 판 E 위, config 는 판 H) — E → F = 사슬 바이트 · 바뀌는 곳 = meta·CSS·카드 하나(카드 넷·섹션 그대로) · 값·보조 줄 매 회차 ·
    "잔액" 없음·꼴 다름 FAIL · 손 수정 E/F FAIL. (판 G 부터 F 는 사슬 중간 — out 은 사슬 끝 H, F 는 cfg_f 로 만든 판)"""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)
        cls.cfg_e = at(cls.cfg, "r2026-10-E")
        cls.E = A.apply(cls.H, cls.R, cls.cfg_e, layout=True)                      # meta r2026-10-E 판(배포본 5e33f38·765cf77 꼴 — 값 채움)
        cls.cfg_f = at(cls.cfg, "r2026-10-F")
        cls.F = A.apply(cls.H, cls.R, cls.cfg_f, layout=True)                      # meta r2026-10-F 판(사슬 끝이 F 인 값 채운 판 — 배포본 판 F 꼴)

    def card(self, o):
        i = o.rindex("\n", 0, o.index('<div class="kpi kpi-wide"')) + 1           # 줄 머리(들여쓰기 포함)부터
        return o[i:o.index("\n    </div>\n", i) + len("\n    </div>\n")]

    def test_e_to_f(self):
        self.assertEqual(self.lay["layout_id"], "r2026-10-K")
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.E), ["r2026-10-E"])
        self.assertNotIn("data-balance", self.E)
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-E ≠ config r2026-10-K — --layout 을 붙여 r2026-10-E → r2026-10-K"):
            A.apply(self.E, self.R, self.cfg)
        self.assertEqual(A.apply(self.E, self.R, self.cfg_f, layout=True), self.F)   # E → F = 옛 → B → C → D → E → F 사슬과 같은 바이트
        self.assertEqual(A.apply(self.E, self.R, self.cfg, layout=True), self.out)   # E → F → G → H 도 사슬과 같은 바이트
        self.assertEqual(A.chain("r2026-10-E", "r2026-10-F"), [A.convert_e_to_f])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-F"), [A.convert_b_to_c, A.convert_c_to_d, A.convert_d_to_e, A.convert_e_to_f])
        self.assertIsNone(A.chain("r2026-10-F", "r2026-10-E"))                       # 거꾸로는 없다
        self.assertEqual(A.apply(self.out, self.R, self.cfg), self.out)              # 값만(멱등)
        self.assertEqual(A.apply(self.out, self.R, self.cfg, layout=True), self.out)
        self.assertEqual(A.apply(self.F, self.R, self.cfg_f), self.F)                # 판 F 값만(멱등 — 사슬 중간 판도)
        o = self.F
        self.assertEqual(o.count('data-balance="value"'), 1)
        self.assertEqual(o.count('data-balance="sub"'), 1)
        self.assertEqual(o.count(".kpi-wide{grid-column:1 / -1;}"), 1)
        kr = o.index('<div class="kpi-row">')
        self.assertTrue(kr < o.index("클릭당 평균") < o.index('<div class="kpi kpi-wide"') < o.index("<!-- Section 1:"))   # 넷째 카드 뒤 · .kpi-row 안
        self.assertIn('style="--accent:#1c2b2a;"', self.card(o))                    # 새 색 0 — 넷째 카드의 accent 값
        self.assertNotIn("<details", o[o.index("<style>"):o.index("</style>")])     # CSS 주석에 태그 꺾쇠 없음

    def test_conversion_scope_e_to_f(self):
        """E → F 가 바꾸는 곳은 meta · CSS 한 덩이 · 카드 하나뿐 — 카드 넷·섹션 HTML·스크립트·서술 표지 그대로."""
        f = A.convert_e_to_f(self.E, self.lay)
        back = (f.replace(self.card(f), "", 1).replace("\n" + A.BALANCE_CSS.rstrip("\n"), "", 1)
                .replace('content="r2026-10-F"', 'content="r2026-10-E"', 1))
        self.assertEqual(back, self.E)
        sec = lambda h: h[h.index("<!-- Section 1:"):]
        self.assertEqual(sec(f), sec(self.E))
        row = lambda h: h[h.index('<div class="kpi-row">'):h.index("클릭당 평균")]
        self.assertEqual(row(f), row(self.E))                                       # 카드 넷 바이트 그대로
        tiles = re.findall(r'<div class="label">([^<]+)</div>\s*<div class="value">([^<]+)<span class="unit">', self.out)
        self.assertEqual([t[0] for t in tiles], ["총 노출수", "총 클릭수", "평균 클릭률", "총 광고비"])   # validate parse_kpi_tiles 에 새 카드가 안 잡힘
        subs = re.findall(r'<div class="sub">([^<]+)</div>', self.out)
        self.assertEqual(len(subs), 3)                                               # 판 J — 평균 클릭률 보조 줄 0 · compare _kpi 는 '클릭당 평균' 을 글로 찾는다
        self.assertTrue(subs[2].startswith("클릭당 평균"))
        self.assertEqual(len(re.findall(r'<div class="sub">([^<]+)</div>', self.F)), 4)   # 판 F(사슬 중간)는 넷 그대로

    def test_values_every_run(self):
        o, R = self.out, self.R
        self.assertIn('<div class="value" data-balance="value">123,456<span class="unit">원</span></div>', o)
        self.assertIn('<div class="sub" data-balance="sub">1/8(목) 09:05 기준 · 약 28일분</div>', o)
        R2 = jread(FIXJ)
        R2["잔액"] = dict(R2["잔액"], 일분=None)                                       # 평균 0 → 며칠분 생략
        o2 = A.apply(o, R2, self.cfg)
        self.assertIn('<div class="sub" data-balance="sub">1/8(목) 09:05 기준</div>', o2)
        R3 = jread(FIXJ)
        R3["잔액"] = {"상태": "fail", "기준": "1/9(금) 10:00"}                        # 조회 실패 → 옛 값이 남지 않는다
        o3 = A.apply(o, R3, self.cfg)
        self.assertIn('<div class="value" data-balance="value">확인 못 함</div>', o3)
        self.assertIn('<div class="sub" data-balance="sub">1/9(금) 10:00 조회 실패</div>', o3)
        self.assertNotIn("123,456", o3)
        self.assertEqual(A.apply(o3, R, self.cfg), o)                                # 실패 → 성공도 글자 남김 없이
        R4 = jread(FIXJ)
        R4["잔액"] = dict(R4["잔액"], 원=1234567, 일분=1234)
        self.assertIn(">1,234,567<span class=\"unit\">원</span></div>", A.apply(o, R4, self.cfg))
        self.assertIn("기준 · 약 1,234일분</div>", A.apply(o, R4, self.cfg))

    def test_missing_or_bad_balance_fails(self):
        R = jread(FIXJ)
        del R["잔액"]
        for page in (self.E, self.out):                                              # 변환 회차·값만 회차 둘 다
            with self.assertRaisesRegex(A.ApplyError, '"잔액" 없음'):
                A.apply(page, R, self.cfg, layout=True)
        for label, b, frag in (("기준 꼴", {"상태": "ok", "원": 1, "기준": "2026-01-08 09:05", "일분": 1}, "기준"),
                               ("상태", {"상태": "unknown", "기준": "1/8(목) 09:05"}, "상태"),
                               ("원 문자열", {"상태": "ok", "원": "123", "기준": "1/8(목) 09:05", "일분": 1}, "원"),
                               ("원 음수", {"상태": "ok", "원": -1, "기준": "1/8(목) 09:05", "일분": 1}, "원"),
                               ("일분 bool", {"상태": "ok", "원": 1, "기준": "1/8(목) 09:05", "일분": True}, "원")):
            with self.subTest(label=label):
                R = jread(FIXJ)
                R["잔액"] = b
                with self.assertRaisesRegex(A.ApplyError, frag):
                    A.apply(self.out, R, self.cfg)

    def test_hand_edited_fails(self):
        cases = (("E 넷째 카드 끝 앵커 없음", self.E.replace('<div class="sub">클릭당 평균', '<div class="sub" >클릭당 평균', 1), "앵커가 정확히 하나가 아님"),
                 ("E 인데 카드 표지 있음", self.E.replace("</body>", '<div data-balance="value"></div></body>', 1), "이미 있음"),
                 ("F 카드 지움", self.out.replace(self.card(self.out), "", 1), "잔액 카드 표지 값 0"),
                 ("F 카드 둘", self.out.replace(self.card(self.out), self.card(self.out) * 2, 1), "잔액 카드 표지 값 2"),
                 ("F 카드를 01 섹션 뒤로", self.out.replace(self.card(self.out), "", 1).replace("<!-- Section 2:", self.card(self.out) + "<!-- Section 2:", 1),
                  ".kpi-row 안"))
        for label, bad, frag in cases:
            with self.subTest(label=label):
                self.assertNotEqual(bad, self.E)
                with self.assertRaisesRegex(A.ApplyError, frag):
                    A.apply(bad, self.R, self.cfg, layout=True)



def long07(R, n):
    """정식표를 n 행으로 늘린 compute 사본(가짜 — 클릭↓ · 끝 3행은 클릭 5·3·3 이라 접힌 행의 클릭 범위가 '3~5건')."""
    R2 = json.loads(json.dumps(R))
    clicks = list(range(n + 20, n + 20 - (n - 3), -1)) + [5, 3, 3]
    R2["07"]["정식표"] = [{"검색어": f"가짜정식{i:02d}", "매칭": "일치" if i % 2 else "확장", "노출": 50 + c * 10, "클릭": c,
                           "CTR": round(c * 100 / (50 + c * 10), 2), "hl": c * 100 / (50 + c * 10) >= 4, "적음": False, "CPC": 400 + i, "총비용": c * (400 + i)}
                          for i, c in enumerate(clicks[:n])]
    return R2


def fold7(h):
    """07 구역 (위 표 행, 접힌 표 행, summary 글) — 위 표 = 구역 첫 tbody · 접힌 표 = "나머지" summary 뒤 첫 tbody."""
    s7 = section(h, 7)
    top = [cells(t) for t in rows(s7[s7.index("<tbody>"):s7.index("</tbody>")]) if "<td" in t]
    i = s7.index('<summary class="fold-more">나머지 ')
    fold = [cells(t) for t in rows(s7[s7.index("<tbody>", i):s7.index("</tbody>", i)]) if "<td" in t]
    return top, fold, re.search(r'<summary class="fold-more">([^<]*)</summary>', s7[i:]).group(1)


class ApplyLayoutH(unittest.TestCase):
    """판 r2026-10-H(07 정식표 접기 — 2026-10-17 사용자 결정 "추천안대로 진행하자" 안 1): G → H · 위 표 K행 + 접힌 표 나머지 · summary · 멱등 · 손 수정 FAIL."""
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.K = cls.lay["top_rows_07"]
        cls.out = A.apply(cls.H, cls.R, cls.cfg, layout=True)                      # fixture 정식표 2행 ≤ K — "나머지 0행"
        cls.cfg_g = at(cls.cfg, "r2026-10-G")
        cls.G = A.apply(cls.H, cls.R, cls.cfg_g, layout=True)                      # meta r2026-10-G 판(배포본 판 G 꼴 — 값 채움)
        cls.RL = long07(cls.R, cls.K + 3)
        cls.long = A.apply(cls.H, cls.RL, cls.cfg, layout=True)                    # 정식표 K + 3 행 — 접힌 표 3행

    def test_config_and_chain(self):
        self.assertEqual((self.lay["layout_id"], self.K, self.lay["markers"]["details"]), ("r2026-10-K", 10, 6))   # config 는 판 K — 판 H 몫(07 접기)은 사슬 끝(K)에 그대로
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.G), ["r2026-10-G"])
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", self.G)), 5)
        self.assertIsNone(A.SUM07_HEAD.search(self.G))
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-G ≠ config r2026-10-K — --layout 을 붙여 r2026-10-G → r2026-10-K"):
            A.apply(self.G, self.R, self.cfg)
        self.assertEqual(A.apply(self.G, self.R, self.cfg, layout=True), self.out)   # G → H → I → J = 옛 → B → … → J 사슬과 같은 바이트
        self.assertEqual(A.apply(self.G, self.RL, self.cfg, layout=True), self.long)
        self.assertEqual(A.chain("r2026-10-G", "r2026-10-H"), [A.convert_g_to_h])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-H")[-2:], [A.convert_f_to_g, A.convert_g_to_h])
        self.assertIsNone(A.chain("r2026-10-H", "r2026-10-G"))                       # 거꾸로는 없다
        for o in (self.out, self.long):
            self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), ["r2026-10-K"])
            self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", o)), 6)
            self.assertEqual(len(re.findall(r"<details[^>]*>\s*<summary", o)), 6)
            self.assertEqual(o.count("</details>"), 6)
            self.assertEqual(A.apply(o, self.R if o is self.out else self.RL, self.cfg), o)               # 값만(멱등)
            self.assertEqual(A.apply(o, self.R if o is self.out else self.RL, self.cfg, layout=True), o)

    def test_conversion_scope_g_to_h(self):
        """G → H 가 바꾸는 곳 = meta · 정식표 wrapper 바로 뒤 접힌 표 뼈대 하나(같은 thead · 빈 tbody) — 그 밖 바이트(위 표 행·다른 구역·스크립트·CSS) 그대로."""
        h = A.convert_g_to_h(self.G, self.lay)
        blk = re.search(r'\n([ \t]*)<details class="fold" style="margin-top:10px;">\n[ \t]*<summary class="fold-more">나머지 0행 펼치기</summary>\n.*?</details>\n', h, re.S)
        self.assertIsNotNone(blk)
        self.assertEqual((h[:blk.start() + 1] + h[blk.end():]).replace('content="r2026-10-H"', 'content="r2026-10-G"', 1), self.G)
        s7 = section(h, 7)
        self.assertLess(s7.index("</table>"), s7.index("나머지 0행 펼치기"))                  # 정식표 뒤
        self.assertLess(s7.index("나머지 0행 펼치기"), s7.index("클릭 1건 검색어"))            # 클릭 1건 목록(·범례·각주) 앞
        heads = re.findall(r"<thead>(.*?)</thead>", s7, re.S)
        self.assertEqual(re.sub(r"\s+", "", heads[0]), re.sub(r"\s+", "", heads[1]))          # 접힌 표 머리 = 정식표 머리
        self.assertEqual(tbodies(s7)[1], [])
        self.assertNotIn("<style>", blk.group(0))
        self.assertEqual(h[h.index("<style>"):h.index("</style>")], self.G[self.G.index("<style>"):self.G.index("</style>")])   # 새 CSS 0
        self.assertEqual(h[h.index("<script>"):], self.G[self.G.index("<script>"):])                                        # 새 JS 0

    def test_split_and_summary(self):
        names = [r["검색어"] for r in self.RL["07"]["정식표"]]
        top, fold, summ = fold7(self.long)
        self.assertEqual([r[0] for r in top], names[:self.K])                                 # 위 표 = 앞 K 행
        self.assertEqual([r[0] for r in fold], names[self.K:])                                # 접힌 표 = 나머지(순서 그대로)
        rest = self.RL["07"]["정식표"][self.K:]
        self.assertEqual([r[3] for r in fold], [str(r["클릭"]) for r in rest])
        self.assertEqual(summ, f"나머지 3행(클릭 3~5건 · 합 11건 · {sum(r['총비용'] for r in rest):,}원) 펼치기")
        s7 = section(self.long, 7)
        i = s7.index('<summary class="fold-more">나머지 ')
        self.assertEqual(s7[i:].count('<td class="num ctr-high">', 0, s7[i:].index("</tbody>")), sum(r["hl"] for r in rest))   # 강조도 접힌 표 행에
        main7 = [cells(t)[0] for t in rows(s7[:s7.index("클릭 1건 검색어")]) if "<td" in t]
        self.assertEqual(main7, names)                                                        # 이어 읽으면 정식표(compare _s07 읽기)
        for frag in ("클릭 1건 검색어", "노출은 있으나 클릭 0건인", "line-height:1.9;", "클릭의", "· 펼치기"):
            self.assertNotIn(frag, summ)                                                     # 07 앵커·경쟁사 summary 꼴과 안 겹침
        self.assertEqual(len(re.findall(r"<summary[^>]*>표 \d+행 · 펼치기</summary>", s7)), 1)
        self.assertIn(f'<summary class="fold-more">표 {len(self.RL["07"]["경쟁사표"])}행 · 펼치기</summary>', s7)
        self.assertIn(f"클릭 1건 검색어 <span style=\"font-weight:400;\">({len(self.RL['07']['클릭1'])}개 · 펼치기)</span></summary>", s7)

    def test_short_rows_and_shift(self):
        top, fold, summ = fold7(self.out)
        self.assertEqual([r[0] for r in top], [r["검색어"] for r in self.R["07"]["정식표"]])
        self.assertEqual((fold, summ), ([], "나머지 0행 펼치기"))                              # 행 ≤ K — 빈 접힌 표(details 수 고정)
        self.assertEqual(A.apply(self.long, self.R, self.cfg), self.out)                      # 행이 줄면 접힌 표 비움(옛 행·옛 숫자 0)
        self.assertEqual(A.apply(self.out, self.RL, self.cfg), self.long)                     # 다시 늘면 채움
        R1 = json.loads(json.dumps(self.R))
        R1["07"]["정식표"] = self.RL["07"]["정식표"][:self.K]
        top, fold, summ = fold7(A.apply(self.long, R1, self.cfg))
        self.assertEqual((len(top), fold, summ), (self.K, [], "나머지 0행 펼치기"))           # 딱 K 행

    def test_k_config(self):
        cfg1 = dict(self.cfg, report_layout=dict(self.lay, top_rows_07=1))
        o1 = A.apply(self.H, self.R, cfg1, layout=True)
        top, fold, summ = fold7(o1)
        r2 = self.R["07"]["정식표"][1]
        self.assertEqual(([r[0] for r in top], [r[0] for r in fold]), (["가짜검색어1"], ["가짜검색어2"]))
        self.assertEqual(summ, f"나머지 1행(클릭 {r2['클릭']}건 · 합 {r2['클릭']}건 · {r2['총비용']:,}원) 펼치기")   # 클릭 범위가 한 값이면 'a건'
        self.assertEqual(A.apply(o1, self.R, self.cfg), self.out)                             # K 를 바꿔도 다음 회차가 다시 나눈다
        for bad in (0, -1, "10", 10.0, True, None):
            lay = dict(self.lay, top_rows_07=bad)
            if bad is None:
                del lay["top_rows_07"]
            with self.subTest(bad=bad), self.assertRaisesRegex(A.ApplyError, "top_rows_07"):
                A.apply(self.out, self.R, dict(self.cfg, report_layout=lay))

    def test_stale_values_rewritten(self):
        """막음 M2 와 같은 꼴 — summary 숫자·접힌 표 행을 옛 값으로 바꿔 둔 판도 compute.json 으로 다시 쓴다."""
        top, fold, summ = fold7(self.long)
        stale = self.long.replace(summ, "나머지 99행(클릭 1~2건 · 합 3건 · 4원) 펼치기", 1)
        self.assertNotEqual(stale, self.long)
        self.assertEqual(A.apply(stale, self.RL, self.cfg), self.long)
        i = self.long.index('<summary class="fold-more">나머지 ')
        a = self.long.index("<tbody>", i) + len("<tbody>")
        stale2 = self.long[:a] + self.long[a:self.long.index("</tbody>", a)] * 2 + self.long[self.long.index("</tbody>", a):]   # 접힌 표 행 두 벌
        self.assertEqual(A.apply(stale2, self.RL, self.cfg), self.long)

    def test_hand_edited_fails(self):
        s7 = section(self.G, 7)
        th = re.search(r"\n[ \t]*<thead>.*?</thead>", s7, re.S).group(0)
        no_head = self.G.replace(s7, s7.replace(th, "", 1), 1)
        with self.assertRaisesRegex(A.ApplyError, "<thead> 없음"):
            A.apply(no_head, self.R, self.cfg, layout=True)
        no_wrap = self.G.replace(s7, s7.replace("</table>\n        </div>\n", "</table>\n", 1), 1)
        with self.assertRaisesRegex(A.ApplyError, "wrapper 닫는 div"):
            A.apply(no_wrap, self.R, self.cfg, layout=True)
        dup = self.G.replace("클릭 1건 검색어 <span", '나머지 1행 펼치기</summary><summary class="fold-more">나머지 2행 펼치기</summary>클릭 1건 검색어 <span', 1)
        with self.assertRaisesRegex(A.ApplyError, "이미 있음"):
            A.convert_g_to_h(dup, self.lay)
        blk = re.search(r'\n[ \t]*<details class="fold" style="margin-top:10px;">\n[ \t]*<summary class="fold-more">나머지 .*?</details>\n', self.long, re.S).group(0)
        moved = self.long.replace(blk, "\n", 1)
        k1 = moved.index('          <details class="fold">\n          <summary style="font-size:12px;font-weight:600;color:var(--ink-soft);margin-bottom:8px;">클릭 1건')
        s8 = moved.index("\n", moved.index("<!-- Section 8:")) + 1
        cases = (("접기 지움", moved, "details 5개"),
                 ("접기 둘", self.long.replace(blk, blk + blk[1:], 1), "details 7개"),
                 ("08 로 옮김", moved[:s8] + blk[1:] + moved[s8:], "07 안 0개"),
                 ("클릭 1건 목록 안으로 옮김", moved[:k1] + blk[1:] + moved[k1:], "wrapper 바로 뒤"),
                 ("summary 글 바꿈", self.long.replace("나머지 3행", "남은 3행", 1), "나머지 N행"))
        for label, bad, frag in cases:
            with self.subTest(label=label):
                self.assertIsNotNone(bad)
                with self.assertRaisesRegex(A.ApplyError, frag):
                    A.apply(bad, self.RL, self.cfg)

BASIS_H = ("· <b>집계 기간</b>: 개업일(2026.08.26)부터 누적 — 네이버가 보고서를 최근 30일까지만 내려줘 2026.09.26부터 월별 원본을 따로 보관해 합산<br>\n"
           '      · <b>제외 규칙</b>: 파워링크 첫 광고그룹 "노원필라테스"는 <b>OFF 상태</b>(키워드 10개 등록, 집행만 멈춤)라 KPI·01~07·10번에서 제외 — '
           "08·09번은 원본 보고서에 광고그룹 구분이 없어 포함(차이는 08·09번 각주)<br>\n"
           "      · <b>평균노출순위</b>: <b>노출수 가중평균</b>(광고시스템 화면의 단순 평균과 다를 수 있음)<br>\n"
           "      · <b>타겟 지역</b>: 노원·도봉·강북·중랑·성북구 5개 자치구 합산<br>\n"
           "      · <b>클릭률 강조</b>: 01·07번 표에서 클릭률 4% 이상인 행만 진한 민트색")   # 배포본 판 H 12-basis 글(판 I 변환이 'KPI·01~07·10번' 한 곳 · 판 J 변환이 세 줄을 고친다)


def with_marks(h):
    """판 I 변환 범위 시험용 — 옛 fixture 에 서술 표지(01-rank · 10 구역 안 10-desc·10-mint · 11-list · 12-note · 12-basis(옛 'KPI·01~07·10번'))와
    번호 배지(10·11·12)를 넣은 판(배포본 판 H 꼴 — 표지는 운영 서술이 넣는 자리)."""
    reps = (('<div class="note">닷새 동안 가짜 순위 서술.</div>', '<div class="note"><!-- n:01-rank:매회차 -->닷새 가짜 순위 서술(12번 1번 참고).<!-- /n --></div>'),
            ('  <!-- Section 10: search vs content placement -->\n  <div class="section">\n',
             '  <!-- Section 10: search vs content placement -->\n  <div class="section">\n'
             '    <div class="section-head"><span class="section-num">10</span><span class="section-desc"><!-- n:10-desc:고정 -->콘텐츠 지면 가짜 0회<!-- /n --></span></div>\n'),
            ("      </table>\n    </div>\n  </div>\n\n  <!-- Section 11:",
             '      </table>\n      <div class="note-mint"><!-- n:10-mint:매회차 -->→ 가짜 지면 민트<!-- /n --></div>\n    </div>\n  </div>\n\n  <!-- Section 11:'),
            ('  <div class="section"><ul><li>가짜 요약</li></ul></div>',
             '  <div class="section"><div class="section-head"><span class="section-num">11</span></div><!-- n:11-list:매회차 --><ul><li>가짜 요약(07번 ②·12번 1번)</li></ul><!-- /n --></div>'),
            ('  <div class="section"><div class="note">가짜 액션</div></div>\n',
             '  <div class="section"><div class="section-head"><span class="section-num">12</span></div><div class="note"><!-- n:12-note:매회차 -->가짜 액션(12번 행 없음)<!-- /n --></div></div>\n'
             '  <div class="card"><div class="note"><!-- n:12-basis:고정 -->' + BASIS_H + '<!-- /n --></div></div>\n'))
    for a, b in reps:
        assert h.count(a) == 1, a[:60]
        h = h.replace(a, b)
    return h


NARR = r"<!-- n:([^\s:]+):[^>]*-->(.*?)<!-- /n -->"


class ApplyLayoutI(unittest.TestCase):
    """판 r2026-10-I(콘텐츠 지면 빼기 — 2026-10-23 사용자 결정 1~6): H → I · 바뀌는 곳 · ① 5칸 · 구역 11·캔버스 7 · 멱등 · 판 H 경로 그대로 · 손 수정 FAIL.
    (판 J 부터 판 I 는 사슬 중간 — config 를 판 I 로 둔 사본 cfg_i 로 돈다)"""
    @classmethod
    def setUpClass(cls):
        cls.F, cls.R, cls.cfg = with_marks(read(FIX)), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.cfg_h = at(cls.cfg, A.LAYOUT_H)
        cls.cfg_i = at(cls.cfg, A.LAYOUT_I)                                      # 판 J 부터 판 I 는 사슬 중간 — config 를 판 I 로 둔 사본
        cls.H = A.apply(cls.F, cls.R, cls.cfg_h, layout=True)                    # meta r2026-10-H 판(배포본 판 H 꼴 — 값 채움, 표지·배지 있음)
        cls.out = A.apply(cls.F, cls.R, cls.cfg_i, layout=True)                  # 옛 → … → H → I

    def test_config_and_chain(self):
        self.assertEqual((self.cfg_i["report_layout"]["layout_id"], self.lay["markers"]["sections"], self.cfg_i["report_layout"]["markers"]["canvases"], self.lay["markers"]["canvases"]),
                         ("r2026-10-I", 11, 7, 8))                               # 판 I 캔버스 7 · config(판 K) 8 — convert_h_to_i 는 config 로도 7 을 센다(canvases_at)
        self.assertEqual(A.chain("r2026-10-H", "r2026-10-I"), [A.convert_h_to_i])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-I")[-2:], [A.convert_g_to_h, A.convert_h_to_i])
        self.assertIsNone(A.chain("r2026-10-I", "r2026-10-H"))
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', self.H), ["r2026-10-H"])
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-H ≠ config r2026-10-I — --layout 을 붙여 r2026-10-H → r2026-10-I"):
            A.apply(self.H, self.R, self.cfg_i)
        self.assertEqual(A.apply(self.H, self.R, self.cfg_i, layout=True), self.out)   # H → I = 옛 → … → I 사슬과 같은 바이트
        self.assertEqual(A.apply(self.out, self.R, self.cfg_i), self.out)               # 값만(멱등)
        self.assertEqual(A.apply(self.out, self.R, self.cfg_i, layout=True), self.out)
        o = self.out
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), ["r2026-10-I"])
        self.assertEqual(re.findall(r"<!-- Section (\d+):", o), [str(n) for n in range(1, 12)])
        self.assertEqual(re.findall(r"<!-- Section (\d+): Action items -->", o), ["11"])
        self.assertEqual(re.findall(r"<!-- Section (\d+): Insight summary -->", o), ["10"])
        self.assertEqual(len(re.findall(r'<canvas id="', o)), 7)
        self.assertNotIn("placementChart", o)
        self.assertNotIn("search vs content placement", o)
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", o)), 6)

    def test_conversion_scope_h_to_i(self):
        """H → I 가 바꾸는 곳 = meta · ① 머리글·칸 머리 둘 · 10 구역 통째 · placementChart 블록 · 11·12 주석·배지 · 12-basis 한 곳 — 그 밖 바이트 그대로."""
        h, i = self.H, A.convert_h_to_i(self.H, self.lay)
        for n in range(2, 10):
            self.assertEqual(section(i, n), section(h, n), n)                                          # 구역 2~9 그대로
        s1 = section(h, 1).replace(A.H1_OLD, A.H1_NEW, 1)
        s1 = re.sub(A.TH_SC, "", s1, count=1)
        self.assertEqual(section(i, 1), s1)                                                            # 01 = 머리글 글·칸 머리 둘만
        re10 = section(h, 11).replace("<!-- Section 11:", "<!-- Section 10:", 1).replace('<span class="section-num">11</span>', '<span class="section-num">10</span>', 1)
        self.assertEqual(section(i, 10), re10)                                                         # 옛 11 → 10(주석·배지만)
        re11 = (section(h, 12).replace("<!-- Section 12:", "<!-- Section 11:", 1).replace('<span class="section-num">12</span>', '<span class="section-num">11</span>', 1)
                .replace(A.BASIS_OLD, A.BASIS_NEW, 1))
        self.assertEqual(section(i, 11), re11)                                                         # 옛 12 → 11(주석·배지·12-basis 한 곳)
        self.assertEqual(i[:i.index("<body>")].replace('content="r2026-10-I"', 'content="r2026-10-H"', 1), h[:h.index("<body>")])   # 머리(CSS 포함) = meta 만
        a = h.index("new Chart(document.getElementById('placementChart'), {")
        b = h.index("\n});\n", a) + len("\n});\n")
        self.assertEqual(i[i.index("<script>"):], (h[:a] + h[b:])[(h[:a] + h[b:]).index("<script>"):])          # 스크립트 = placementChart 블록만 빠짐(새 JS 0)
        nh, ni = dict(re.findall(NARR, h, re.S)), dict(re.findall(NARR, i, re.S))
        self.assertEqual(sorted(set(nh) - set(ni)), ["10-desc", "10-mint"])                           # 10-* 표지는 구역째 사라짐
        self.assertEqual({k: v for k, v in nh.items() if not k.startswith("10-") and k != "12-basis"}, {k: v for k, v in ni.items() if k != "12-basis"})   # 다른 표지 안쪽 그대로
        self.assertEqual(ni["12-basis"], nh["12-basis"].replace("KPI·01~07·10번에서 제외", "KPI·01~07번에서 제외"))
        self.assertIn("가짜 요약(07번 ②·12번 1번)", i)                                                  # 매회차 표지 글의 번호는 운영 서술 몫(변환은 안 바꿈 — validate 28 이 잡는다)

    def test_values_rows_5(self):
        o, R = self.out, self.R
        s1 = section(o, 1)
        th = re.search(r"<thead>(.*?)</thead>", s1, re.S).group(1)
        self.assertEqual(re.findall(r"<th[^>]*>([^<]*)</th>", th), ["날짜", "노출", "클릭", "CTR", "CPC"])
        self.assertIn(">① 일별 지표 — 노출·CTR 변화</div>", s1)
        r1 = [cells(t) for t in rows(s1) if "<td" in t]
        want = [[r["날짜"], str(r["노출"]), str(r["클릭"]), f"{r['CTR']:.2f}%", f"{r['CPC']:,}원"] for r in R["01"]["표5"]][::-1]
        self.assertEqual(r1, want)
        self.assertEqual(len(re.findall(r'<td class="num ctr-high">', s1)), sum(r["hl"] for r in R["01"]["표5"]))
        R2 = json.loads(json.dumps(R))
        for r in R2["01"]["표5"]:                                                                     # 판 I 표는 검색·콘텐츠 키를 읽지 않는다(compute 판 I 출력 꼴)
            r.pop("검색", None), r.pop("콘텐츠", None)
        self.assertEqual(A.apply(o, R2, self.cfg_i), o)

    def test_layout_h_path_unchanged(self):
        """판 H 경로(config 판 H — 사슬 중간): ① 7칸 · placementChart 배열 · 10 표 4행 = compute "10" 그대로(옛 판 회귀 0)."""
        h, R = self.H, self.R
        r1 = [cells(t) for t in rows(section(h, 1)) if "<td" in t]
        self.assertEqual([r[2:4] for r in r1], [[str(r["검색"]), str(r["콘텐츠"])] for r in R["01"]["표5"]][::-1])
        self.assertEqual([[c.replace(",", "").replace("원", "") for c in cells(t)[2:5]] for t in rows(section(h, 10)) if "<td" in t],
                         [[str(v) for v in R["10"][k]] for k in "ABCD"])
        blk = h[h.index("getElementById('placementChart')"):]
        self.assertIn("data:[" + ", ".join(map(str, R["10"]["placement"]["노출"])) + "]", blk.replace("data: [", "data:["))
        s10 = section(h, 10)
        bad = h.replace(s10, s10.replace('<td class="name-cell">추천·콘텐츠 지면 › 가짜 D</td>\n            <td>가짜 매체</td>', '<td class="name-cell">D</td>', 1), 1)
        self.assertNotEqual(bad, h)
        with self.assertRaisesRegex(A.ApplyError, "10 표 행이 4개가 아님"):
            A.apply(bad, self.R, self.cfg_h)

    def test_hand_edited_h_fails(self):
        h = self.H
        s10 = section(h, 10)
        cases = (("① 칸 머리 없음", re.sub(A.TH_SC, "", h, count=1), "앵커가 정확히 하나가 아님"),
                 ("10 구역에 다른 캔버스", h.replace(s10, s10.replace('<canvas id="placementChart"></canvas>', '<canvas id="placementChart"></canvas><canvas id="extra"></canvas>', 1), 1), "10 구역에 지면 구역 밖의 것"),
                 ("10 구역에 접기", h.replace(s10, s10.replace("<table>", "<details><summary>x</summary></details><table>", 1), 1), "10 구역에 지면 구역 밖의 것"),
                 ("placementChart 블록 없음", h.replace("getElementById('placementChart'), {", "getElementById('placementChartX'), {", 1), "placementChart 차트 블록 시작이 0개"),
                 ("10-* 표지가 구역 밖", h.replace("<!-- Section 10:", "<!-- n:10-note:매회차 -->x<!-- /n -->\n  <!-- Section 10:", 1), "10 구역 밖에 서술 표지 10-*"),
                 ("12-basis 다른 10번", h.replace("KPI·01~07·10번에서 제외", "KPI·01~10번에서 제외", 1), "12-basis 에"),
                 ("마지막 구역 아님", h.replace("<!-- Section 12: Action items -->", "<!-- Section 12: Actions -->", 1), "마지막 구역이 12번 다음 액션"),
                 ("옛 11 배지 다름", h.replace('<span class="section-num">11</span>', '<span class="section-num">09</span>', 1), "옛 11 구역 번호 배지"))
        for label, bad, msg in cases:
            with self.subTest(label=label):
                self.assertNotEqual(bad, h)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, self.R, self.cfg_i, layout=True)

    def test_hand_edited_i_fails(self):
        o = self.out
        s1 = section(o, 1)
        th7 = s1.replace('<th class="num">노출</th>\n', '<th class="num">노출</th>\n            <th class="num">검색</th>\n            <th class="num">콘텐츠</th>\n', 1)
        cases = (("구역 12 주석", o.replace("</div>\n\n<script>", "</div>\n<!-- Section 12: x -->\n\n<script>", 1), "구역 주석"),
                 ("placementChart 캔버스", o.replace('<canvas id="hourlyChart"></canvas>', '<canvas id="hourlyChart"></canvas><canvas id="placementChart"></canvas>', 1), "지면 구역 흔적"),
                 ("배지 다름", o.replace('<span class="section-num">11</span>', '<span class="section-num">12</span>', 1), "번호 배지"),
                 ("① 7칸 머리", o.replace(s1, th7, 1), "칸 머리 7개"),
                 ("캔버스 8", o.replace('<canvas id="hourlyChart"></canvas>', '<canvas id="hourlyChart"></canvas><canvas id="extra"></canvas>', 1), "캔버스 8개"),
                 ("옛 머리글", o.replace(A.H1_NEW, A.H1_OLD, 1), "머리글"),
                 ("Action items 이름", o.replace("<!-- Section 11: Action items -->", "<!-- Section 11: Actions -->", 1), "다음 액션"))
        for label, bad, msg in cases:
            with self.subTest(label=label):
                self.assertNotEqual(bad, o)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, self.R, self.cfg_i)


def with_marks_j(h):
    """판 J 변환 범위 시험용 — with_marks(판 H 꼴 표지) 위에 판 J 가 고치는 표지(매회차 03-desc·08-note·09-desc·09-call · 고정 04-foot·07-src·07-legend·12-desc —
    고정 글은 배포본 판 I 글 그대로)를 구역 첫 줄 뒤에 하나씩 더한 판. 변환은 표지 이름으로 찾으므로 구역 안 자리면 된다."""
    h = with_marks(h)
    add = {3: '<span class="section-desc"><!-- n:03-desc:매회차 -->최고치 1/2(금) 9,000원 그대로 — 1/7(수)은 5,000원(플레이스 4,000원 + 파워링크 1,000원)<!-- /n --></span>',
           4: f'<div style="font-size:11px;"><!-- n:04-foot:고정 -->{A.FOOT04[0]}<!-- /n --></div>',
           7: (f'<div class="note"><!-- n:07-src:고정 -->{A.SRC07[0]}<!-- /n --></div><div><!-- n:07-legend:고정 --><span style="color:var(--mint-dark);font-weight:800;">'
               '진한 민트색 클릭률</span> = 4% 이상 (일반적인 검색광고 "양호" 기준인 2%의 2배 이상)<!-- /n --></div>'),
           8: '<div class="note"><!-- n:08-note:매회차 -->가짜 08 각주.<!-- /n --></div>',
           9: '<span class="section-desc"><!-- n:09-desc:매회차 -->1시대 클릭 최다(2회, 3회차 연속) — 상시 문의 대응 전략과 부합<!-- /n --></span><div><!-- n:09-call:매회차 -->→ 가짜 심야.<!-- /n --></div>'}
    for n, blk in add.items():
        a = h.index(f"<!-- Section {n}:")
        e = h.index("\n", h.index('<div class="section"', a)) + 1
        h = h[:e] + "    " + blk + "\n" + h[e:]
    old = '<div class="section-head"><span class="section-num">12</span></div>'
    assert h.count(old) == 1
    return h.replace(old, f'<div class="section-head"><span class="section-num">12</span><span class="section-desc"><!-- n:12-desc:고정 -->{A.DESC12[0]}<!-- /n --></span></div>')


J_DIFF_OK = (  # 판 I → J 줄 단위 diff 에 나올 수 있는 글(이 밖의 줄이 바뀌면 FAIL — G5)
    'content="r2026-10-I"', 'content="r2026-10-J"', A.TITLE_OLD, A.TITLE_NEW, "업종 평균 수준", '<span class="unit">회</span>', '<span class="unit">건</span>',
    A.GROUP_OLD, A.GROUP_NEW, A.FOOT04[0], A.FOOT04[1], A.SRC07[0], A.SRC07[1], A.DESC12[0], A.DESC12[1], "진한 민트색 클릭률",
    "<b>집계 기간</b>", "<b>타겟 지역</b>", "<b>클릭률 강조</b>", "<!-- n:03-desc:", "<!-- n:08-note:", "<!-- n:09-desc:", "<!-- n:09-call:",
    f"일 평균 {jread(FIXJ)['KPI']['일평균클릭']}")   # KPI 클릭 보조 줄(fixture 값 — 노출 보조 줄은 이 글이 아니라 허용 밖)


class ApplyLayoutJ(unittest.TestCase):
    """판 r2026-10-J(불필요 항목 빼기 — 2026-10-23 오후 사용자 결정 "추천대로"): I → J · 바뀌는 곳(고정 글만) · 값 갈래(KPI 건 · 07 쉼표·'적음' · 04 신규 기한 ·
    06 카드 집합 · 판 G 블록 글) · 멱등 · 손 수정 I/J FAIL · 직전 판 I·J 읽기 같음(G3)."""
    @classmethod
    def setUpClass(cls):
        cls.F, cls.R, cls.cfg = with_marks_j(read(FIX)), jread(FIXJ), at(load_config(), A.LAYOUT_J)   # 판 K 부터 판 J 는 사슬 중간 — config 를 판 J 로 둔 사본
        cls.lay = cls.cfg["report_layout"]
        cls.cfg_i = at(cls.cfg, A.LAYOUT_I)
        cls.I = A.apply(cls.F, cls.R, cls.cfg_i, layout=True)                    # meta r2026-10-I 판(표지 있음 — 배포본 판 I 꼴)
        cls.out = A.apply(cls.F, cls.R, cls.cfg, layout=True)                    # 옛 → … → I → J

    def test_config_and_chain(self):
        self.assertEqual(self.lay["layout_id"], "r2026-10-J")
        self.assertEqual(A.chain("r2026-10-I", "r2026-10-J"), [A.convert_i_to_j])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-J")[-2:], [A.convert_h_to_i, A.convert_i_to_j])
        self.assertIsNone(A.chain("r2026-10-J", "r2026-10-I"))
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-I ≠ config r2026-10-J — --layout 을 붙여 r2026-10-I → r2026-10-J"):
            A.apply(self.I, self.R, self.cfg)
        self.assertEqual(A.apply(self.I, self.R, self.cfg, layout=True), self.out)   # I → J = 옛 → … → J 사슬과 같은 바이트
        self.assertEqual(A.apply(self.out, self.R, self.cfg), self.out)               # 값만(멱등)
        self.assertEqual(A.apply(self.out, self.R, self.cfg, layout=True), self.out)
        o = self.out
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), ["r2026-10-J"])
        self.assertEqual(re.findall(r"<!-- Section (\d+):", o), [str(n) for n in range(1, 12)])
        self.assertEqual(len(re.findall(r'<canvas id="', o)), 7)
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", A.strip_extra(o))), 6)
        self.assertEqual([w for w in A.TRIM_GONE if w in o], [])

    def test_conversion_scope_i_to_j(self):
        """I → J 가 바꾸는 줄은 허용 목록(J_DIFF_OK)의 글이 든 줄뿐 — 다른 구역·서술 표지 안쪽·CSS·JS 바이트 그대로(G5). 바뀐 곳마다 새 글."""
        import difflib
        i, j = self.I, A.convert_i_to_j(self.I, self.lay, self.cfg)
        changed = [l for l in difflib.unified_diff(i.split("\n"), j.split("\n"), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        self.assertTrue(changed)
        self.assertEqual([l for l in changed if not any(w in l for w in J_DIFF_OK)], [])
        self.assertEqual(i[i.index("<style>"):i.index("</style>")], j[j.index("<style>"):j.index("</style>")])                # 새 CSS 0
        si, sj = i[i.index("<script>"):], j[j.index("<script>"):]
        self.assertEqual(si.replace(A.GROUP_OLD, A.GROUP_NEW, 1), sj)                                                      # 스크립트 = groupChart 이름 한 곳
        for n in (2, 5, 6, 10):
            self.assertEqual(section(i, n), section(j, n), n)                                                               # 고칠 글이 없는 구역 그대로
        nar = lambda h: dict((k, v) for k, v in re.findall(NARR, h, re.S))
        ni, nj = nar(i), nar(j)
        self.assertEqual(set(ni), set(nj))
        self.assertEqual({k for k in ni if ni[k] != nj[k]}, {"04-foot", "07-src", "07-legend", "12-desc", "12-basis"})    # 안쪽이 바뀐 표지 = 고정 글 다섯
        self.assertEqual(nj["07-legend"], ni["07-legend"] + A.legend07_tail(self.cfg))
        self.assertEqual(nj["12-basis"].count("<br>"), ni["12-basis"].count("<br>") - 1)                                   # 타겟 지역 줄 하나 빠짐
        self.assertIn(A.basis_ctr(self.cfg), nj["12-basis"])
        self.assertIn("· <b>집계 기간</b>: 개업일(2026.08.26)부터 누적<br>", nj["12-basis"])
        for n in A.TO_FIXED:
            self.assertEqual((i.count(f"<!-- n:{n}:매회차 -->"), j.count(f"<!-- n:{n}:고정 -->")), (1, 1), n)

    def test_values_j(self):
        o, R = self.out, self.R
        self.assertIn(f'<div class="value">{R["KPI"]["클릭"]:,}<span class="unit">건</span></div>', o)          # 결정 37 — 클릭 '건'
        self.assertIn(f"일 평균 {R['KPI']['일평균클릭']}건", o)
        self.assertIn(f'<div class="value">{R["KPI"]["노출"]:,}<span class="unit">회</span></div>', o)          # 노출은 '회' 그대로
        self.assertEqual(len(re.findall(r'<div class="sub">([^<]+)</div>', o)), 3)                              # 결정 13 — 평균 클릭률 보조 줄 0
        R2 = json.loads(json.dumps(R))                                                                          # 결정 34·35 — 07 노출 쉼표 · '적음'
        R2["07"]["정식표"][0].update(노출=2671)
        R2["07"]["정식표"][1].update(노출=9, CTR=22.22, hl=False, 적음=True)
        o2 = A.apply(o, R2, self.cfg)
        s7 = section(o2, 7)
        top = [cells(t) for t in rows(s7[s7.index("<tbody>"):s7.index("</tbody>")]) if "<td" in t]
        self.assertEqual([(r[2], r[4]) for r in top], [("2,671", f"{R2['07']['정식표'][0]['CTR']:.2f}%"), ("9", "적음")])
        self.assertEqual(s7.count('<td class="num">적음</td>'), 1)
        self.assertNotIn("22.22%", s7)
        self.assertEqual(A.apply(o2, R, self.cfg), o)                                                           # 되돌리면 바이트 그대로
        self.assertIn("(1/2 신규)", section(o, 4))                                                             # 결정 30 — 04.신규 = [가짜그룹B](4일차)
        R3 = json.loads(json.dumps(R))
        R3["04"]["신규"] = []
        o3 = A.apply(o, R3, self.cfg)
        self.assertNotIn("신규)", section(o3, 4))
        self.assertIn('<td class="name-cell">가짜그룹B</td>', section(o3, 4))
        self.assertEqual(A.apply(o3, R3, self.cfg), o3)
        R4 = json.loads(json.dumps(R))                                                                          # 결정 5 — 카드 밖이 된 그룹의 카드는 지움
        R4["06"]["카드"] = {}
        o4 = A.apply(o, R4, self.cfg)
        self.assertEqual((A.card_groups(o), A.card_groups(o4)), (["가짜그룹B"], []))
        self.assertNotIn("평균노출순위", section(o4, 6))
        self.assertEqual(A.apply(o4, R4, self.cfg), o4)
        with self.assertRaisesRegex(A.ApplyError, "06 카드가 없는 그룹"):                                       # 있어야 할 카드는 만들지 않는다(사람이 넣는다 — 04 새 그룹과 같음)
            A.apply(o4, R, self.cfg)

    def test_extra_blocks_trim(self):
        """결정 7·8 — 판 G 블록: 변경 기록 끝 스킬 줄 0 · 성별·연령대 머리 '(네이버 추정)' · 알 수 없음 % 는 표에 그 줄이 없는 종류만(trim=False = 판 I 글)."""
        H = {"상태": "ok", "기간": "9/12~10/10", "건수": 1, "표시": 1, "보일주체": ["사람"], "스킬": {"등록회": 3, "삭제건": 1},
             "rows": [{"일시": "10/10 10:00", "유형": "확장소재 추가", "대상": "가짜", "내용": "확장 소재 2개 추가"}]}
        hb, hb_i = A.hi_block({"변경기록": H}), A.hi_block({"변경기록": H}, trim=False)
        self.assertNotIn("스킬 제외 검색어 등록", hb)
        self.assertIn("스킬 제외 검색어 등록 3회(실행 수) · 삭제 1건", hb_i)
        self.assertIn("SYSTEM 하루예산 중단 2회", A.hi_block({"변경기록": dict(H, 시스템={"하루예산중단": 2})}))
        rows_ = lambda unk: [{"구분": "가", "노출": 100, "비중": 80.0, "클릭": 1, "CTR": 1.0, "적음": False, "비용": 10}] + (
            [{"구분": "알 수 없음", "노출": 25, "비중": 20.0, "클릭": 0, "CTR": None, "적음": True, "비용": 0}] if unk else [])
        G = {"상태": "ok", "min_imps": 100, "표": [{"상태": "ok", "종류": "성별", "기간": "10/1~10/9", "알수없음%": 20.0, "알수없음줄": True, "rows": rows_(True)},
                                                 {"상태": "ok", "종류": "연령대", "기간": "10/1~10/9", "알수없음%": 20.0, "알수없음줄": False, "rows": rows_(False)}]}
        gb, gb_i = A.ga_block({"성별연령": G}), A.ga_block({"성별연령": G}, trim=False)
        self.assertIn(A.GA_HEAD_J, gb)
        self.assertNotIn("제외 그룹 포함", gb)
        self.assertIn(f">성별 <span {A.MUTED}>(10/1~10/9)</span>", gb)                                           # 줄이 있는 종류 — 괄호에 % 0
        self.assertIn(f">연령대 <span {A.MUTED}>(10/1~10/9 · 알 수 없음 20.0%)</span>", gb)                     # 줄이 없는 종류 — % 남김
        self.assertIn(A.GA_HEAD_I, gb_i)
        self.assertIn(f">성별 <span {A.MUTED}>(10/1~10/9 · 알 수 없음 20.0%)</span>", gb_i)

    def test_hand_edited_fails(self):
        i, o, R = self.I, self.out, self.R
        legend_i = '2배 이상)<!-- /n -->'
        cases_i = (("04-foot 다른 글", i.replace(A.FOOT04[0], "※ 손으로 고친 각주", 1), "고정 표지 04-foot 글이 판 I 글이 아님"),
                   ("12-basis 타겟 지역 줄 없음", A.BASIS_TARGET.sub("", i, count=1), "12-basis 가 판 I 글"),
                   ("KPI 평균 클릭률 보조 줄 없음", i.replace('<div class="sub">업종 평균 수준</div>', "", 1), "앵커가 정확히 하나가 아님"),
                   ("07-legend 에 이미 한 구", i.replace(legend_i, "2배 이상) · 노출 20회 미만은 '적음'<!-- /n -->", 1), "이미 있음"),
                   ("03-desc 표지 둘", i.replace("<!-- Section 4:", "<!-- n:03-desc:매회차 -->x<!-- /n -->\n  <!-- Section 4:", 1), "03-desc 가 2개"))
        for label, bad, msg in cases_i:
            with self.subTest(label=label):
                self.assertNotEqual(bad, i)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, R, self.cfg, layout=True)
        R4 = json.loads(json.dumps(R))
        R4["06"]["카드"] = {}
        card_note = "<!-- n:06-card-가짜그룹B:"
        cases_j = (("뺀 고정 글 되살림", o.replace("</body>", "<!-- 업종 평균 수준 --></body>", 1), R, "뺀 고정 글이 남음"),
                   ("표지 매회차로", o.replace("<!-- n:09-call:고정 -->", "<!-- n:09-call:매회차 -->", 1), R, "가 매회차"),
                   ("07-legend 끝 없음", o.replace(A.legend07_tail(self.cfg) + "<!-- /n -->", "<!-- /n -->", 1), R, "07-legend 끝"),
                   ("KPI 클릭 '회'", o.replace('<span class="unit">건</span>', '<span class="unit">회</span>', 1), R, "KPI 총 클릭수 단위"),
                   ("카드 블록에 다른 표지", o.replace('4일차. 가짜 카드 서술.', '4일차. 가짜 카드 서술.<!-- n:xx:고정 -->x<!-- /n -->', 1) if card_note not in o else None, R4, "카드 밖의 것"))
        for label, bad, RR, msg in cases_j:
            with self.subTest(label=label):
                self.assertIsNotNone(bad)
                self.assertNotEqual(bad, o)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, RR, self.cfg)

    def test_prev_readers_i_and_j_same(self):
        """G3 — 다음 회차가 직전 배포본에서 읽는 곳이 판 I·J 둘 다 같은 결과: masthead 끝 날 · 07 경쟁사표 행 · 다음 액션 구역(이월 줄) · 04 이름 칸 그룹 키."""
        import compute as C
        from reportlib import action_section
        i, j = self.I, self.out
        self.assertIsNotNone(C.prev_period_end(j))
        self.assertEqual(C.prev_period_end(i), C.prev_period_end(j))
        self.assertEqual(C.deployed_competitors(i), C.deployed_competitors(j))
        self.assertTrue(C.deployed_competitors(j))
        line = "P3 안 함(1/5 결정)"
        for h in (i, j):
            page = h.replace("<!-- n:12-note:매회차 -->", f"<!-- n:12-note:매회차 -->{line} ", 1)
            self.assertIn(line, action_section(page))
        names = lambda h: [cells(t)[1].split("(")[0].strip() for t in rows(section(h, 4)) if "<td" in t]
        self.assertEqual(names(i), names(j))
        self.assertEqual(names(j), [r["그룹"] for r in self.R["04"]["rows"]])


WEEK_BLOCK = re.compile(r"// 8\. Weekday average.*?\n\}\)\(\);\n", re.S)   # 판 K 차트 블록(주석 줄 ~ IIFE 끝)
WEEK_CARD_RE = re.compile(r'    <div class="card" data-weekday="card".*?\n    </div>\n', re.S)   # 판 K 카드(값이 들어간 뒤)


class ApplyLayoutK(unittest.TestCase):
    """판 r2026-10-K(01 요일 카드 — 2026-10-26 사용자 결정 "추천대로 진행해줘", config 판): J → K = 사슬 바이트 · `--layout` 없이 J 면 FAIL ·
    바뀌는 곳 = meta · 01 차트 카드 뒤 · ① 박스 앞 카드 하나 · 차트 스크립트 끝(분기 도우미 뒤) 블록 하나(다른 구역 · 01 차트 · ① ② ③ · 서술 표지 · CSS 바이트 그대로) ·
    값(막대 · clicks · 보조 줄 = compute 01.요일 — 0일 요일 · 일수 범위) · 멱등 · "01.요일" 없음·꼴 다름 FAIL · 손 수정 J/K FAIL."""
    @classmethod
    def setUpClass(cls):
        cls.F, cls.R, cls.cfg = with_marks_j(read(FIX)), jread(FIXJ), load_config()
        cls.lay = cls.cfg["report_layout"]
        cls.cfg_j = at(cls.cfg, A.LAYOUT_J)
        cls.J = A.apply(cls.F, cls.R, cls.cfg_j, layout=True)                    # meta r2026-10-J 판(표지 있음 — 배포본 판 J 꼴)
        cls.out = A.apply(cls.F, cls.R, cls.cfg, layout=True)                    # 옛 → … → J → K

    def wblk(self, h):
        b = h[h.index("getElementById('weekdayChart')"):]
        return b[:b.index("</script>")]

    def test_config_and_chain(self):
        self.assertEqual((self.lay["layout_id"], self.lay["markers"]["canvases"], self.lay["markers"]["weekday_card"]), ("r2026-10-K", 8, 1))
        self.assertEqual(A.chain("r2026-10-J", "r2026-10-K"), [A.convert_j_to_k])
        self.assertEqual(A.chain("r2026-10-B", "r2026-10-K")[-2:], [A.convert_i_to_j, A.convert_j_to_k])
        self.assertIsNone(A.chain("r2026-10-K", "r2026-10-J"))
        with self.assertRaisesRegex(A.ApplyError, "레이아웃 판 meta r2026-10-J ≠ config r2026-10-K — --layout 을 붙여 r2026-10-J → r2026-10-K"):
            A.apply(self.J, self.R, self.cfg)
        self.assertEqual(A.apply(self.J, self.R, self.cfg, layout=True), self.out)   # J → K = 옛 → … → K 사슬과 같은 바이트
        self.assertEqual(A.apply(self.out, self.R, self.cfg), self.out)               # 값만(멱등)
        self.assertEqual(A.apply(self.out, self.R, self.cfg, layout=True), self.out)
        o = self.out
        self.assertEqual(re.findall(r'<meta name="report-layout" content="([^"]*)">', o), ["r2026-10-K"])
        self.assertEqual(re.findall(r"<!-- Section (\d+):", o), [str(n) for n in range(1, 12)])   # 새 구역 0
        cv = re.findall(r'<canvas id="([^"]+)"', o)
        self.assertEqual((len(cv), cv.count("weekdayChart")), (8, 1))
        self.assertEqual(len(re.findall(r"<details(?:\s[^>]*)?>", A.strip_extra(o))), 6)

    def test_conversion_scope_j_to_k(self):
        """J → K 가 바꾸는 곳 = meta · 01 카드 하나(차트 카드 바로 뒤 · ① 박스 앞) · 분기 도우미 뒤 차트 블록 하나 — 그 밖 바이트 그대로 · 01 첫 일치 앵커 보호."""
        j, k = self.J, A.convert_j_to_k(self.J, self.lay)
        self.assertEqual(k[:k.index("<body>")].replace('content="r2026-10-K"', 'content="r2026-10-J"', 1), j[:j.index("<body>")])   # 머리(CSS 포함) = meta 만
        for n in range(2, 12):
            self.assertEqual(section(k, n), section(j, n), n)                                          # 구역 2~11 그대로
        s1 = section(k, 1)
        self.assertEqual((s1.count(A.WEEK_CARD), s1.replace(A.WEEK_CARD, "", 1)), (1, section(j, 1)))   # 01 = 카드 하나만 더함
        self.assertLess(s1.index('<canvas id="dailyChart">'), s1.index(A.WEEK_CARD))
        self.assertLess(s1.index(A.WEEK_CARD), s1.index("① 일별 지표"))
        self.assertTrue(s1[:s1.index(A.WEEK_CARD)].endswith("    </div>\n"))                        # 차트 카드 닫힘 바로 뒤
        sj, sk = j[j.index("<script>"):], k[k.index("<script>"):]
        self.assertEqual(sk.replace(A.WEEK_JS.lstrip("\n"), "", 1), sj)                                 # 스크립트 = 블록 하나만 더함(다른 차트 바이트 그대로)
        self.assertLess(k.index("/* saero:mobile-helper"), k.index("getElementById('weekdayChart')"))
        self.assertTrue(k[k.index("getElementById('weekdayChart')"):].split("</script>", 1)[0].rstrip().endswith("})();"))   # 스크립트 맨 끝
        nar = lambda h: dict(re.findall(NARR, h, re.S))
        self.assertEqual(nar(k), nar(j))                                                                # 서술 표지 안쪽 그대로
        for w in ("getElementById('dailyChart')", "getElementById('rankChart')", "min-width", "<td", "note-mint", "→ 누적 CTR", "하루 평균은",
                  'margin-bottom:2px;">', "line-height:1.9;", "<details", "<summary", "ctr-high", "mintDark", "mint-dark", "saero:mobile-branch"):
            self.assertNotIn(w, A.WEEK_CARD + A.WEEK_JS, w)                                            # apply·compare·validate 01 첫 일치 앵커 · 강조색 0
        self.assertIsNone(re.search(r"'\d+/\d+\(.\)'", A.WEEK_JS))                                       # 날짜 꼴 labels 0(validate 10 · compare 01/06 labels 2배열 그대로)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{6}", A.WEEK_CARD + A.WEEK_JS), ["#cdeee7"])           # 색 = 01 막대 하나(팔레트 밖 0)

    def test_values_k(self):
        o, R = self.out, self.R
        b = self.wblk(o)
        self.assertIn("data: [155, 140, 140, 140, 150, 130, 145]", b)
        self.assertIn("clicks: [5.0, 4.0, 3.0, 4.0, 6.0, 2.0, 6.0]", b)
        self.assertIn('<div class="note" data-weekday="sub">검색 지면 · 1/1~1/7 · 요일마다 1일</div>', o)
        R2 = json.loads(json.dumps(R))                                                                   # 0일 요일(합본 7일 미만) — 막대 0 · clicks null · 범위에 0
        R2["01"]["요일"] = {"첫날": "1/1", "끝날": "1/3", "일수": [0, 0, 0, 1, 1, 1, 0], "노출": [0, 0, 0, 140, 150, 130, 0], "클릭": [None, None, None, 4.0, 6.0, 2.5, None]}
        o2 = A.apply(o, R2, self.cfg)
        b2 = self.wblk(o2)
        self.assertIn("data: [0, 0, 0, 140, 150, 130, 0]", b2)
        self.assertIn("clicks: [null, null, null, 4.0, 6.0, 2.5, null]", b2)
        self.assertIn(">검색 지면 · 1/1~1/3 · 요일마다 0~1일</div>", o2)
        for n in range(2, 12):
            self.assertEqual(section(o2, n), section(o, n), n)                                         # 요일 값만 — 다른 구역 그대로
        self.assertEqual(o2.replace(b2, b, 1).replace("1/1~1/3 · 요일마다 0~1일", "1/1~1/7 · 요일마다 1일", 1), o)   # 바뀐 곳 = 블록 배열 · 보조 줄뿐
        R3 = json.loads(json.dumps(R))                                                                   # 일수가 다른 요일(61일 — 8~9일) · 정수 클릭 10 → '10.0'
        R3["01"]["요일"] = {"첫날": "8/26", "끝날": "10/25", "일수": [8, 8, 9, 9, 9, 9, 9], "노출": [277, 322, 289, 264, 249, 206, 238], "클릭": [11.8, 10, 10.7, 10.6, 9.7, 6.9, 9.2]}
        o3 = A.apply(o, R3, self.cfg)
        self.assertIn("clicks: [11.8, 10.0, 10.7, 10.6, 9.7, 6.9, 9.2]", self.wblk(o3))
        self.assertIn(">검색 지면 · 8/26~10/25 · 요일마다 8~9일</div>", o3)
        self.assertEqual(A.apply(o3, R3, self.cfg), o3)
        self.assertEqual(A.apply(o2, R, self.cfg), o)                                                    # 되돌리면 바이트 그대로

    def test_missing_or_bad_weekday_fails(self):
        o, R = self.out, self.R
        for label, edit in (("키 없음", lambda W: None), ("노출 6칸", lambda W: dict(W, 노출=W["노출"][:6])), ("첫날 없음", lambda W: {k: v for k, v in W.items() if k != "첫날"}),
                            ("클릭 문자열", lambda W: dict(W, 클릭="5.0"))):
            with self.subTest(label=label):
                R2 = json.loads(json.dumps(R))
                W = edit(R2["01"]["요일"])
                if W is None:
                    del R2["01"]["요일"]
                else:
                    R2["01"]["요일"] = W
                with self.assertRaisesRegex(A.ApplyError, '"01.요일" 없음 또는 꼴이 다름'):
                    A.apply(o, R2, self.cfg)

    def test_hand_edited_fails(self):
        j, o, R = self.J, self.out, self.R
        gap = "    </div>\n    <div class=\"card\" style=\"margin-top:12px; padding-bottom:20px;\">"
        s1 = section(j, 1)
        self.assertEqual(s1.count(gap), 1)
        hp_end = j.index("\n})();\n", j.index("/* saero:mobile-helper")) + len("\n})();\n")
        cases_j = (("요일 표지 이미 있음", j.replace("</body>", '<div data-weekday="card"></div></body>', 1), "이미 있음"),
                   ("차트 카드와 ① 사이 다른 것", j.replace(s1, s1.replace(gap, "    </div>\n    <div class=\"note\">x</div>\n" + gap[len("    </div>\n"):], 1), 1), "닫는 div 셋 밖"),
                   ("분기 도우미가 스크립트 끝 아님", j[:hp_end] + "// 덧붙인 줄\n" + j[hp_end:], "스크립트 끝이 아님"),
                   ("① 머리글 둘", j.replace("</body>", "<!-- ① 일별 지표 --></body>", 1).replace("<!-- Section 2:", "<div>① 일별 지표</div>\n  <!-- Section 2:", 1), "① 머리글 2개"))
        for label, bad, msg in cases_j:
            with self.subTest(label=label):
                self.assertNotEqual(bad, j)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, R, self.cfg, layout=True)
        card, blk = WEEK_CARD_RE.search(o).group(0), WEEK_BLOCK.search(o).group(0)
        no_card = o.replace(card, "", 1)
        moved = no_card.replace("  <!-- Section 2:", card + "  <!-- Section 2:", 1)
        no_blk = o.replace(blk, "", 1)
        cases_k = (("카드 지움(캔버스 7)", no_card, "캔버스 7개"),
                   ("카드를 ① 뒤로", moved, "요일 카드가 01 구역 안 차트 카드 뒤"),
                   ("차트 블록을 도우미 앞으로", no_blk.replace("/* saero:mobile-helper", blk + "/* saero:mobile-helper", 1), "요일 차트 블록 1개"),
                   ("차트 블록 지움", no_blk, "앵커 없음|요일 차트 블록 0개"),
                   ("labels 바꿈", o.replace(A.WEEK_LABELS, "['일','월','화','수','목','금','토']", 1), "labels\\(월~일\\)"),
                   ("clicks 둘", o.replace("          clicks: [", "          clicks: [1],\n          clicks: [", 1), "clicks 배열"),
                   ("sub 표지 둘", o.replace('<div class="note" data-weekday="sub">', '<div class="note" data-weekday="sub"></div><div class="note" data-weekday="sub">', 1), "요일 카드 표지"))
        for label, bad, msg in cases_k:
            with self.subTest(label=label):
                self.assertNotEqual(bad, o)
                with self.assertRaisesRegex(A.ApplyError, msg):
                    A.apply(bad, R, self.cfg)


class ComputeWeekday(unittest.TestCase):
    """compute weekday_avg(판 K — 사용자 결정 기본값 2·3): 제외 그룹 뺀 검색 지면 행만 날마다 합 → 달력 요일 하루 평균(전 기간) · 행 없는 날 0 ·
    반올림 = 파이썬 round(정수 · 소수 1자리 — 정확히 반이면 짝수 쪽: 250.5 → 250 · 10.25 → 10.2) · 0일 요일 노출 0 · 클릭 None. 기대값은 손으로 적은 값."""
    def run_w(self, rows, days):
        import pandas as pd
        import compute as C
        from reportlib import exclude_groups
        kw = pd.DataFrame([{"일별": d, "광고그룹": g, "검색/콘텐츠 매체": m, "노출수": i, "클릭수": c} for d, g, m, i, c in rows])
        inc = exclude_groups(kw, load_config())
        return C.weekday_avg(inc[inc["검색/콘텐츠 매체"] == "검색"], days)                         # compute 01 과 같은 프레임(srch)

    def test_four_weeks(self):
        days = [f"2026.10.{d:02d}." for d in range(5, 32)] + ["2026.11.01."]                      # 10/5(월) ~ 11/1(일) 28일 — 요일마다 4일
        imp = {0: [100, 101, 99, 100], 1: [250, 251, 250, 251], 2: [251, 252, 251, 252], 3: [300, None, 300, 300], 4: [10, 10, 10, 10], 5: [5, 6, 7, 8], 6: [1, 2, 3, 4]}
        clk = {0: [5, 6, 4, 5], 1: [10, 10, 10, 11], 2: [3, 3, 3, 4], 3: [9, None, 9, 9], 4: [1, 0, 0, 0], 5: [0, 0, 0, 0], 6: [2, 2, 2, 3]}
        rows = []
        for w in range(4):
            for k in range(7):
                d = days[w * 7 + k]
                if imp[k][w] is None:                                                                # 목 10/15 — 행 없는 날(0 으로 셈)
                    continue
                rows.append((d, "가짜그룹", "검색", imp[k][w] - 1, clk[k][w]))                         # 같은 날 두 행(합)
                rows.append((d, "가짜그룹2", "검색", 1, 0))
        rows += [("2026.10.10.", "가짜그룹", "콘텐츠", 1000, 50),                                        # 토 콘텐츠 지면 — 빼야(지면 전부면 토가 가장 높아짐)
                 ("2026.10.06.", load_config()["excluded_groups"][0], "검색", 5000, 99)]               # 제외 그룹 — 빼야
        W = self.run_w(rows, days)
        self.assertEqual(W["일수"], [4] * 7)
        self.assertEqual((W["첫날"], W["끝날"]), ("10/5", "11/1"))
        # 월 400/4=100 · 화 1002/4=250.5→250 · 수 1006/4=251.5→252 · 목 900/4=225(행 없는 날 0) · 금 10 · 토 26/4=6.5→6 · 일 10/4=2.5→2
        self.assertEqual(W["노출"], [100, 250, 252, 225, 10, 6, 2])
        # 월 20/4=5.0 · 화 41/4=10.25→10.2 · 수 13/4=3.25→3.2 · 목 27/4=6.75→6.8 · 금 1/4=0.25→0.2 · 토 0.0 · 일 9/4=2.25→2.2
        self.assertEqual(W["클릭"], [5.0, 10.2, 3.2, 6.8, 0.2, 0.0, 2.2])

    def test_zero_day_weekday(self):
        days = ["2026.10.05.", "2026.10.06.", "2026.10.07."]                                         # 월화수 3일 — 목~일 0일
        W = self.run_w([(d, "가짜그룹", "검색", 100 + n, n) for n, d in enumerate(days)], days)
        self.assertEqual(W, {"첫날": "10/5", "끝날": "10/7", "일수": [1, 1, 1, 0, 0, 0, 0], "노출": [100, 101, 102, 0, 0, 0, 0], "클릭": [0.0, 1.0, 2.0, None, None, None, None]})
        self.assertEqual(A.week_sub(W), "검색 지면 · 10/5~10/7 · 요일마다 0~1일")


class ComputeCardRule(unittest.TestCase):
    """판 J(결정 5·30) 06 카드 규칙 — compute card_groups(새 그룹 · 승격 그룹 · 오래된 그룹 · 최근 7일 노출 0 · 노원역) + validate "06번 카드 그룹"(CSV 로 따로) 같은 판정 ·
    완료 기준 "시험(새 그룹 카드)"."""
    GC = {"new_days": 10, "promotion_groups": ["승격그룹"]}

    def frames(self):
        import pandas as pd
        days = [f"2026.10.{d:02d}." for d in range(1, 21)]
        rows_ = []
        for g, first, last in (("노원역필라테스", 0, 19), ("새그룹", 15, 19), ("오래된그룹", 0, 19), ("승격그룹", 0, 19), ("멈춘새그룹", 12, 12)):
            for k in range(first, last + 1):
                rows_.append({"일별": days[k], "캠페인": "새로필라테스 파워링크", "광고그룹": g, "노출수": 10, "클릭수": 0, "총비용": 0})
        rows_.append({"일별": days[0], "캠페인": "플레이스#1", "광고그룹": "새로필라테스", "노출수": 10, "클릭수": 0, "총비용": 0})
        kw = pd.DataFrame(rows_)
        return kw, days

    def test_new_group_card(self):
        import compute as C
        kw, days = self.frames()
        pw = kw[~kw["캠페인"].str.startswith("플레이스")]
        to = lambda s: dt_date(s)
        nth = {g: (to(days[-1]) - to(s["일별"].min())).days + 1 for g, s in pw.groupby("광고그룹")}
        self.assertEqual((nth["새그룹"], nth["멈춘새그룹"], nth["오래된그룹"]), (5, 8, 20))
        self.assertEqual(C.card_groups(pw, days, nth, self.GC), ["새그룹", "승격그룹"])     # 새 그룹(5일차) · 승격 그룹 — 오래된·최근 7일 노출 0·노원역 밖
        self.assertEqual(C.card_groups(pw, days, nth, dict(self.GC, promotion_groups=[])), ["새그룹"])
        self.assertEqual(C.card_groups(pw, days, nth, dict(self.GC, new_days=21)), ["새그룹", "오래된그룹", "승격그룹"])

    def vcheck(self, html, kw):
        import contextlib
        import io
        import validate as V
        cfg = dict(V.GC)
        V.GC.update(self.GC)
        try:
            del V.results[:]
            with contextlib.redirect_stdout(io.StringIO()):
                V.check_card_rule(html, kw, kw)
            return V.results[-1]
        finally:
            V.GC.clear()
            V.GC.update(cfg)

    def page(self, cards, tagged=()):
        head = lambda g: (f'<div style="font-size:12px;font-weight:600;color:var(--ink-soft);">{g} <span style="color:var(--mint-dark);font-weight:700;">'
                          f'(10/1 등록, 3일차)</span></div>')
        names = "".join(f'<tr><td class="name-cell">{g} <span style="font-weight:400;">(10/1 신규)</span></td></tr>' for g in tagged)
        return f'<!-- Section 4: x --><table>{names}</table><!-- Section 6: x -->{"".join(head(g) for g in cards)}<!-- Section 7: x -->'

    def test_validate_same_rule(self):
        kw, _ = self.frames()
        self.assertTrue(self.vcheck(self.page(["새그룹", "승격그룹"], ["새그룹"]), kw)[1])
        name, ok, det = self.vcheck(self.page(["승격그룹"]), kw)                                     # 새 그룹 카드 없음
        self.assertFalse(ok)
        self.assertIn("규칙 ['새그룹', '승격그룹']", det)
        self.assertFalse(self.vcheck(self.page(["새그룹", "승격그룹", "오래된그룹"]), kw)[1])           # 오래된 그룹 카드가 남음
        name, ok, det = self.vcheck(self.page(["새그룹", "승격그룹"], ["오래된그룹"]), kw)             # 오래된 그룹에 '(M/D 신규)'
        self.assertFalse(ok)
        self.assertIn("오래된그룹(20일차)", det)


def dt_date(s):
    import datetime as dt
    return dt.date(*(int(x) for x in s.rstrip(".").split(".")))


class ComputeContentWatch(unittest.TestCase):
    """compute content_days(판 I — 사용자 결정 5): 콘텐츠 노출 0 → (None, None, []) · [주의] 줄 0 / since 뒤 노출 > 0 → 줄 1(날짜·노출) · 첫날·끝날."""
    def frame(self, rows):
        import pandas as pd
        return pd.DataFrame([{"일별": d, "검색/콘텐츠 매체": m, "노출수": i} for d, m, i in rows])

    def run_cd(self, rows, days):
        import contextlib
        import io
        import compute as C
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            out = C.content_days(self.frame(rows), days, load_config())
        return out, [x for x in err.getvalue().splitlines() if x.startswith("[주의]")]

    def test_zero_and_recur(self):
        days = ["2026.09.04.", "2026.09.05.", "2026.09.06.", "2026.10.24.", "2026.10.25."]
        base = [(d, "검색", 100) for d in days]
        out, lines = self.run_cd(base, days)                                                     # 콘텐츠 0
        self.assertEqual((out, lines), ((None, None, []), []))
        old = base + [("2026.09.04.", "콘텐츠", 7), ("2026.09.05.", "콘텐츠", 5)]                   # 기준일(9/6) 앞만 — 재발 아님
        out, lines = self.run_cd(old, days)
        self.assertEqual((out, lines), (("9/4", "9/5", []), []))
        rec = old + [("2026.10.24.", "콘텐츠", 12), ("2026.10.24.", "콘텐츠", 3), ("2026.10.25.", "검색", 1)]
        out, lines = self.run_cd(rec, days)                                                      # 10/24 재발(같은 날 두 행 합)
        self.assertEqual(out, ("9/4", "10/24", [{"날짜": "10/24", "노출": 15}]))
        self.assertEqual(len(lines), 1)
        self.assertIn("[주의] 콘텐츠 지면 노출 재발 — 기준일 9/6 이후 1일: 10/24 15회", lines[0])
        out, lines = self.run_cd(rec + [("2026.09.06.", "콘텐츠", 1000)], days)                     # 기준일 당일도 재발(9/6 이후 날 = 9/6 포함)
        self.assertEqual(out[2], [{"날짜": "9/6", "노출": 1000}, {"날짜": "10/24", "노출": 15}])
        self.assertIn("9/6 1,000회 · 10/24 15회", lines[0])


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
        self.assertIn("레이아웃 판 변환(meta 없음 → r2026-10-B → r2026-10-C → r2026-10-D → r2026-10-E → r2026-10-F → r2026-10-G → r2026-10-H → r2026-10-I → r2026-10-J → r2026-10-K, details 6 · 분기 2)", out)
        self.assertIn("· 잔액 카드 123,456원 · 1/8(목) 09:05 기준 · 약 28일분", out)                  # 판 F — 운영 세션이 출력에서 카드 글을 본다
        self.assertIn("· 07 정식표 위 2행 · 나머지 0행 펼치기", out)                                      # 판 H — fixture 정식표 2행 ≤ K
        self.assertIn("· 구역 11 · 캔버스 8(지면 구역 없음)", out)                                        # 판 I — 운영 세션이 출력에서 구역·캔버스 수를 본다(판 K 요일 캔버스 +1)
        self.assertIn("· 06 카드 ['가짜그룹B'] · 04 신규 메모 1", out)                                    # 판 J — 06 카드 집합 · 04 신규 메모 수
        self.assertIn("· 요일 카드 검색 지면 · 1/1~1/7 · 요일마다 1일", out)                               # 판 K — 운영 세션이 출력에서 요일 카드 보조 줄을 본다

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
            self.assertIn("(변환 건너뜀) · 잔액 카드 ", r.stdout)
            self.assertTrue(r.stdout.rstrip().endswith("(변경 없음)"), r.stdout)
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
                            ("판 I ① 칸 머리 검색·콘텐츠 없음", H.replace('            <th class="num">검색</th>\n            <th class="num">콘텐츠</th>\n', '', 1)),
                            ("판 I placementChart 블록 없음", H.replace("new Chart(document.getElementById('placementChart'), {", "new Chart(document.getElementById('placementChartX'), {", 1)),
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


@unittest.skipUnless(os.path.exists(os.path.join(ROOT, "work", "RX", "same", "index.html")) and os.path.exists(os.path.join(ROOT, "work", "RX", "same", "compute.json")),
                     "리허설 산출 work/RX/same 없음(구현·검증 회차 리허설 뒤에만)")
class ApplyRehearsal(unittest.TestCase):
    def test_rx_output_idempotent(self):
        H = read(os.path.join(ROOT, "work", "RX", "same", "index.html"))
        R = jread(os.path.join(ROOT, "work", "RX", "same", "compute.json"))
        self.assertGreater(H.count("<!-- n:"), 20)
        self.assertIn('<meta name="report-layout" content="r2026-10-K">', H)               # 리허설 RX = 판 K(meta 로 판 선택 — --layout 없이 · 2026-10-26 구현 리허설)
        self.assertEqual((H.count('data-weekday="card"'), H.count('data-weekday="sub"'), H.count("getElementById('weekdayChart')")), (1, 1, 1))   # 판 K 요일 카드
        self.assertIn("요일", R["01"])
        self.assertEqual([w for w in A.TRIM_GONE if w in H], [])                            # 판 J 가 뺀 고정 글 0
        self.assertNotIn("placementChart", H)                                               # 지면 구역 없음
        self.assertEqual(re.findall(r"<!-- Section (\d+):", H), [str(n) for n in range(1, 12)])
        self.assertNotIn("<!-- n:10-", H)
        self.assertEqual(len(A.SUM07_HEAD.findall(H)), 1)                                   # 07 정식표 접기 하나
        self.assertEqual(H.count(A.TOUCH_D_TO_E[1]), 1)
        self.assertEqual(H.count('data-balance="value"'), 1)
        self.assertEqual((H.count(A.HI_OPEN), H.count(A.GA_OPEN)), (1, 1))
        self.assertIn("잔액", R)
        self.assertEqual((R["변경기록"]["상태"], R["성별연령"]["상태"]), ("ok", "ok"))
        self.assertEqual(A.apply(H, R, load_config()), H)


if __name__ == "__main__":
    unittest.main(verbosity=1)
