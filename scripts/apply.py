#!/usr/bin/env python3
"""compute.json → 작업본 index.html 의 기계 자리 교체(5단계, E2 — 2026-10-06 저장소화) + 레이아웃 판 변환(2026-10-06 회차 2 · 판 C 01 차트 회차 1 · 판 D 모바일 기간 접기 2026-10-07 ·
판 E 01 모바일 터치 날짜 2026-10-08 · 판 F 광고비 잔액 카드 2026-10-09).

사용법: "$PY" scripts/apply.py --layout [--html work/index.html] [--compute work/compute.json]

- 레이아웃 판(config `report_layout`, references/report-structure.md "레이아웃 판" 절 — 지금 r2026-10-F):
  · `<meta name="report-layout" content="…">` 가 config `layout_id` 와 같으면 그 판으로 값만 바꾼다 — `--layout` 이 있어도 변환은 건너뜀(멱등).
  · 판 사슬(`STEPS`): r2026-10-B(접기형) → r2026-10-C(`convert_b_to_c` — meta · 왼쪽 페이드 CSS · 01·06 차트 블록을 PC/모바일 두 모양 템플릿으로 ·
    차트 스크립트 끝 분기 도우미 · 가로 안내 스크립트 4줄) → r2026-10-D(`convert_c_to_d` — meta · 펼치기 버튼 CSS · 01 비용 라벨 간격 두 곳 ·
    분기 도우미를 판 D 도우미로(모바일 01·06 처음 최근 `mobile.recent_days` 일 + 펼치기 버튼, 인쇄 때 전 기간)) → r2026-10-E(`convert_d_to_e` — meta ·
    01 모바일 모양의 interaction 한 줄에 axis:'y' — 가로 막대에서 터치한 줄(날짜)의 팝업이 뜨게) → r2026-10-F(`convert_e_to_f` — meta ·
    `.kpi-wide` CSS · KPI 카드 넷 아래 한 줄 전체 광고비 잔액 카드 하나(.kpi-row 다섯째 자식 — 카드 넷 그대로)). meta 가 사슬 위의 옛 판이면
    `--layout` 일 때 config 판까지 차례로 변환한 뒤 값을 바꾼다. `--layout` 없이 옛 판이면 `[FAIL] apply: ApplyError: 레이아웃 판 meta r2026-10-D ≠ config …`.
  · meta 가 없는 옛 판은 `--layout` 일 때만 사슬로 변환(`convert_layout(h, LAYOUT_B)` → `convert_b_to_c` → `convert_c_to_d` → `convert_d_to_e` → `convert_e_to_f`) 뒤 값을 바꾼다.
    `--layout` 없이 옛 판이면 `[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout …` (옛 배치로 쓰지 않는다). 사슬 밖 meta 는 FAIL(판 변경은 설계 회차 몫).
  · config 대조(details 수 = `markers.details` · 분기 표지 주석 `/* saero:mobile-branch 01|06 */` 수 = `markers.mobile_branch` · 판 F 잔액 카드 표지
    `data-balance="value"`·`"sub"` 각 `markers.balance_card` · .kpi-row 안)는 사슬 끝에 한 번 — 값만 경로도 같다.
- 바꾸는 자리(매 회차 — 변환을 건너뛴 회차에도): masthead · og:description · KPI 4 + sub 3 · 차트 min-width 2(01·06) · 차트 배열·라벨(01·02·05·06·09·10) ·
  02 도넛 제목 총액 · 01 표 5행·순위 5칸(오름차순 그대로) · 03 두 표(위 = 합계 + 최근 `recent_days`일 최신 위 · 접힌 표 = 나머지 날짜 최신 위) ·
  04 표(앞 2칸 = 직전 행) · 06 매칭표 2행·카드 일차·큰 숫자 · 07 정식표 · 07 클릭 1건·클릭 0 목록(동률은 직전 순서) ·
  07 경쟁사표(소재구·매칭 = 직전 행, 신규 변형 = config `competitor_defaults`) · 08 TOP 10 · 08 TOP 10 밖 목록(동률은 직전 순서)·개수 줄 · 10 표 4행 ·
  **summary 의 개수·날짜 전부**(03 "이전 N일(M/D~M/D)" · 07 클릭 1건·클릭 0 "(N개 · 펼치기)" · 경쟁사표 "표 N행" · 08 "(N개 지역·클릭 M건)") — 막음 M2 ·
  분기 도우미의 M 줄(`var M = {maxPx: …, printMaxH: …, row: {…}, pad: {…}, recent: {…}};` = config `report_layout.mobile`, 판 D) ·
  판 F 광고비 잔액 카드의 값·보조 줄(compute.json "잔액" — 없으면 `[FAIL] apply: … "잔액" 없음`, 실패 기록이면 "확인 못 함" · "M/D(요일) HH:MM 조회 실패").
  01·06 모바일 펼치기 버튼 문구("이전 N일(M/D~M/D) 펼치기")는 HTML 에 없다 — 도우미가 화면에서 data.labels 로 만든다(apply 기계 자리 0).
- 서술(문장)은 바꾸지 않는다 — 그 회차의 n<날짜>.py(저장소 밖 스크래치)가 서술 표지 `<!-- n:<자리>:<매회차|고정> -->` 안을 바꾼다
  (references/report-structure.md "서술 표지"). 변환·값 교체 모두 표지 안쪽 바이트를 건드리지 않는다. summary·details 는 apply 몫.
- 앵커: `once()` 만 "정확히 하나"를 검사한다(못 찾거나 둘 이상이면 `[FAIL] apply: …` exit 1). 차트 배열의 `chart()`/`labels()` 는
  `getElementById('<id>')` 부터 다음 `new Chart` 앞까지에서 **첫 일치**를 바꾼다(없으면 FAIL, 둘이어도 FAIL 하지 않음 — 판 C 템플릿은 블록 안에 하나씩).
  파일은 끝에 한 번만 쓰므로 실패하면 작업본은 그대로다.
- 같은 compute.json 으로 두 번 돌려도 바이트가 같다(멱등 — tests/test_apply.py).
"""
import argparse
import json
import re
import sys

from reportlib import load_config

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — 다른 스크립트와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


class ApplyError(Exception):
    pass


def c(n):
    return f"{n:,}"


def once(pat, rep, s, flags=0):
    new, n = re.subn(pat, rep, s, count=1, flags=flags)
    if n != 1 or len(re.findall(pat, s, flags)) != 1:
        raise ApplyError(f"앵커가 정확히 하나가 아님({len(re.findall(pat, s, flags))}개): {pat[:80]}")
    return new


def find1(s, needle, start=0):
    i = s.find(needle, start)
    if i == -1:
        raise ApplyError(f"앵커 없음: {needle[:80]}")
    return i


def tbody(s, after, rows_html, start=0, stop=None):
    """start 뒤 첫 앵커 → 그 뒤 첫 <tbody> 안을 통째로 바꾼다. (새 문자열, 옛 tbody 안) 를 돌려준다.
    stop 이 있으면 그 </tbody> 가 stop 앞이어야 한다(구역 밖 표를 덮지 않게 — 03 접힌 표)."""
    i = find1(s, after, start)
    a = find1(s, "<tbody>", i) + len("<tbody>")
    b = find1(s, "</tbody>", a)
    if stop is not None and b > stop:
        raise ApplyError(f"앵커 {after[:40]!r} 뒤 첫 <tbody> 가 구역 밖")
    return s[:a] + "\n" + rows_html + s[b:], s[a:b]


def bounds(s, n):
    """<!-- Section n: --> 부터 <!-- Section n+1: --> 앞까지 (시작, 끝)."""
    a = find1(s, f"<!-- Section {n}:")
    return a, find1(s, f"<!-- Section {n + 1}:", a)


def once_in(s, n, pat, rep, flags=0):
    """once 를 n 번 구역 안에서만."""
    a, b = bounds(s, n)
    return s[:a] + once(pat, rep, s[a:b], flags) + s[b:]


LAYOUT_META = re.compile(r'<meta name="report-layout" content="([^"]*)">')
DETAILS = re.compile(r"<details(?:\s[^>]*)?>")

FOLD_CSS = """  /* 접기(레이아웃 판 r2026-10-B 이후, 2026-10-06) — details.fold(태그 이름을 꺾쇠로 쓰지 말 것: validate 태그 짝이 셈): 03 이전 날짜 · 07 클릭 1건·클릭 0 목록 · 07 경쟁사표 · 08 TOP 10 밖.
     기본 닫힘. 펼치면 아래 스크립트가 가로 스크롤 안내를 다시 맞추고, 인쇄할 때는 전부 펼쳤다가 되돌린다(css-and-layout.md "접기 안내") */
  .fold > summary{cursor:pointer;}
  .fold-more{font-size:12px;font-weight:700;color:var(--mint-dark);}
  .fold[open] > .fold-more{margin-bottom:8px;}
"""
RESIZE = "  window.addEventListener('resize', function(){ clearTimeout(t); t = setTimeout(sync, 200); });\n"
FOLD_JS = """  // 접기(details — 레이아웃 판 r2026-10-B 이후): 펼칠 때 안쪽 표의 안내·페이드를 다시 맞추고, 인쇄할 때는 닫힌 것을 전부 펼쳤다가 원래대로
  document.querySelectorAll('details').forEach(function(d){ d.addEventListener('toggle', sync); });
  var folded = [];
  window.addEventListener('beforeprint', function(){
    folded = Array.prototype.filter.call(document.querySelectorAll('details'), function(d){ return !d.open; });
    folded.forEach(function(d){ d.open = true; });
  });
  window.addEventListener('afterprint', function(){ folded.forEach(function(d){ d.open = false; }); folded = []; });
"""
LIST = r'(\s*<div [^>]*line-height:1\.9;">.*?</div>)'  # 목록 div — validate·compare·listblock 이 "앵커 뒤 첫 line-height:1.9;\">" 로 읽는 자리


def convert_layout(h, lay):
    """옛 판(meta 없음 · details 0) → 레이아웃 판 뼈대. 값(행·목록·summary 개수)은 뒤의 apply 가 채운다.
    서술 표지 안쪽은 건드리지 않는다 — 머리글 div·표 wrapper·목록 div 를 details/summary 로 감싸고 meta·CSS·스크립트만 넣는다."""
    if DETAILS.search(h):
        raise ApplyError(f"레이아웃 판 meta 가 없는데 <details> 가 {len(DETAILS.findall(h))}개 — 손으로 고친 판으로 보임, 변환하지 않음")
    lid = lay["layout_id"]
    h = once(r'(<meta charset="UTF-8">\n)', lambda m: m.group(1) + f'<meta name="report-layout" content="{lid}">\n', h)
    h = once(r"(\n</style>)", lambda m: "\n" + FOLD_CSS.rstrip("\n") + m.group(1), h)
    h = once(re.escape(RESIZE), lambda m: RESIZE + FOLD_JS, h)

    # 03 — 표 아래에 접힌 표(같은 머리글, 빈 tbody — 행·summary 는 값 교체가 쓴다)
    a, b = bounds(h, 3)
    s = h[a:b]
    if s.count("<table>") != 1:
        raise ApplyError(f"03 구역 표가 1개가 아님({s.count('<table>')}개)")
    th = re.search(r"<thead>.*?</thead>", s, re.S)
    if not th:
        raise ApplyError("03 구역 <thead> 없음")

    def fold3(m):
        ind = m.group(2)
        return (m.group(0) + f'{ind}<details class="fold" style="margin-top:10px;">\n'
                f'{ind}  <summary class="fold-more">이전 0일 펼치기</summary>\n'
                f'{ind}  <div style="overflow-x:auto;" class="wide-table">\n{ind}  <table>\n{ind}    {th.group(0)}\n'
                f'{ind}    <tbody>\n{ind}    </tbody>\n{ind}  </table>\n{ind}  </div>\n{ind}</details>\n')
    h = h[:a] + once(r"(</table>\n)([ \t]*)</div>\n", fold3, s) + h[b:]

    # 07 — 클릭 1건·클릭 0 목록: 머리글 div → summary(앵커 문구 그대로 + 개수), 목록 div(line-height:1.9;) 는 details 안 그대로
    def fold_list(head):
        def r(m):
            ind = m.group(1)
            return f'\n{ind}<details class="fold">\n{ind}<summary {m.group(2)}>{head}</summary>{m.group(3)}\n{ind}</details>'
        return r
    h = once_in(h, 7, r'\n([ \t]*)<div (style="[^"]*")>클릭 1건 검색어</div>' + LIST,
                fold_list('클릭 1건 검색어 <span style="font-weight:400;">(0개 · 펼치기)</span>'), re.S)
    h = once_in(h, 7, r'\n([ \t]*)<div (style="[^"]*")>노출은 있으나 클릭 0건인 검색어 <span style="font-weight:400;">\(노출 5회 이상만\)</span></div>' + LIST,
                fold_list('노출은 있으나 클릭 0건인 검색어 <span style="font-weight:400;">(노출 5회 이상 0개 · 펼치기)</span>'), re.S)
    # 07 경쟁사표 — 머리글 div "경쟁사 브랜드명 검색어"(compute·apply·validate 앵커) 그대로, 표 wrapper 만 details 안으로
    h = once_in(h, 7, r'(경쟁사 브랜드명 검색어</div>\n)([ \t]*)(<div style="overflow-x:auto;" class="wide-table">.*?</table>\s*</div>)',
                lambda m: (f'{m.group(1)}{m.group(2)}<details class="fold">\n{m.group(2)}<summary class="fold-more">표 0행 · 펼치기</summary>\n'
                           f'{m.group(2)}{m.group(3)}\n{m.group(2)}</details>'), re.S)
    # 08 — TOP 10 밖: sub-head → summary("(N개 지역·클릭 M건)" 괄호 그대로, "· 펼치기" 는 괄호 밖), 목록 div 만 안으로(각주 note 는 밖)
    h = once_in(h, 8, r'\n([ \t]*)<div (class="sub-head"[^>]*)>(TOP 10 외[^<]*<span[^>]*>\(\d+개 지역·클릭 \d+건\)</span>)</div>' + LIST,
                lambda m: f'\n{m.group(1)}<details class="fold">\n{m.group(1)}<summary {m.group(2)}>{m.group(3)} · 펼치기</summary>{m.group(4)}\n{m.group(1)}</details>', re.S)
    n = len(DETAILS.findall(h))
    if n != int(lay["markers"]["details"]):
        raise ApplyError(f"변환 뒤 details {n}개 ≠ config report_layout.markers.details {lay['markers']['details']}")
    return h


# ── 판 C(r2026-10-C, 2026-10-06 — 01 일별 추이 모바일 차트 회차 1, 설계안 A): 01·06 모바일 가로 막대 ──
# 옛 판 → B 단계 값(config 를 C 로 올린 뒤에도 사슬 중간 단계는 이 값으로 돈다 — convert_layout 의 meta·details 대조)
LAYOUT_B = {"layout_id": "r2026-10-B", "markers": {"details": 5}}
LAYOUT_C = "r2026-10-C"
LAYOUT_D = "r2026-10-D"
LAYOUT_E = "r2026-10-E"
BRANCH = re.compile(r"/\* saero:mobile-branch (01|06) \*/")
M_LINE_C = re.compile(r'var M = \{maxPx: \d+, printMaxH: \d+, row: \{"01": \d+, "06": \d+\}, pad: \{"01": \d+, "06": \d+\}\};')   # 판 C 도우미의 M 줄(사슬 중간 단계)

# CSS·JS 주석에 태그 이름을 꺾쇠로 쓰지 말 것(validate 태그 짝·apply details 수가 셈) · 새 색 0(기존 ::after 와 같은 값)
MOBILE_CSS = """  /* 왼쪽 페이드(레이아웃 판 r2026-10-C, 2026-10-06) — PC 01·06 차트는 최신 쪽(오른쪽 끝)에서 시작하므로 왼쪽으로 이전 날짜가 이어짐을 알린다.
     맨 왼쪽(.at-start)이면 숨김 — 아래 안내 스크립트가 at-end 와 같이 맞춘다(css-and-layout.md "가로 스크롤 안내 자동화"). 모바일 가로 막대는 넘침이 없어 페이드가 없다 */
  .scroll-fade::before{
    content:"";position:absolute;top:0;left:0;width:38px;height:100%;
    background:linear-gradient(to left, rgba(255,255,255,0), var(--card) 85%);
    pointer-events:none;opacity:1;transition:opacity .15s ease;
  }
  .scroll-fade.at-start::before{opacity:0;}
"""

# 01·06 블록 — 한 스크립트 안 직렬 실행이라 이 시점엔 분기 도우미가 아직 없다: 제자리에서 PC 모양으로 만들고 큐에 넣기만 한다.
# apply chart()/labels() 앵커가 사는 순서: getElementById → labels: [ (블록 안 하나) → label: '…', data: [ → 그 뒤에야 첫 new Chart(
# PC 옵션 값 = 판 B 배포본 그대로(06 은 날짜축 autoSkip:false 를 명시). 배열은 data 하나 — 모바일은 같은 객체로 다시 그린다(숫자 1벌).
CHART01_C = """/* saero:mobile-branch 01 */
(function(){  // 판 C: PC 는 세로 콤보 그대로 · 화면 폭 ≤ M.maxPx 이면 차트 스크립트 끝 분기 도우미가 같은 data 로 가로 막대(날짜 세로축·최신 위)를 다시 만든다
  var canvas = document.getElementById('dailyChart');
  var data = {
    labels: [],
    datasets: [
      {
        type: 'bar',
        label: '노출수',
        data: [],
        backgroundColor: '#cdeee7',
        borderRadius: 6,
        order: 1
      },
      {
        type: 'line',
        label: '총비용(원)',
        data: [],
        borderColor: mintDark,
        backgroundColor: mintDark,
        tension: 0.35,
        pointBackgroundColor: mintDark,
        order: 0
      }
    ]
  };
  function axes(key, ids){ data.datasets.forEach(function(d, i){ delete d.xAxisID; delete d.yAxisID; d[key] = ids[i]; }); }
  function pc(){
    axes('yAxisID', ['y', 'y1']);
    data.datasets[0].datalabels = {display: true, anchor: 'start', align: 'top', offset: 4, color: ink, font: {size:11, weight:'700'}, formatter: (v) => v.toLocaleString()};
    data.datasets[1].borderWidth = 3;
    data.datasets[1].pointRadius = 5;
    data.datasets[1].datalabels = {display: true, align: 'top', anchor: 'end', offset: 8, clip: false, color: ink, font: {size:11, weight:'600'}, formatter: (v) => v.toLocaleString() + '원'};
    return {
      type: 'bar',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {mode:'index', intersect:false},
        layout: { padding: {top: 24} },
        plugins: {
          legend: {position:'bottom', labels:{usePointStyle:true, boxWidth:8}},
        },
        scales: {
          x: {grid:{display:false}, ticks:{font:{size:10.5}, maxRotation:0, autoSkip:false}},
          y: {position:'left', grid:{color:grid}, title:{display:true,text:'노출수',font:{size:11}}},
          y1:{position:'right', grid:{display:false}, title:{display:true,text:'비용(원)',font:{size:11}}}
        }
      }
    };
  }
  function costGap(ctx){  // 모바일 비용 라벨 간격 — 점이 같은 행의 노출 라벨(막대 시작 쪽) 안쪽이면 그 라벨 상자 오른쪽 끝 + 4px 뒤에서 시작(글자 겹침 0)
    var ch = ctx.chart, bs = ch.scales.x, cs = ch.scales.x1, i = ctx.dataIndex, c2 = ch.ctx;
    if (!bs || !cs) return 8;
    c2.save(); c2.font = '700 11px ' + Chart.defaults.font.family;
    var w = c2.measureText(Number(data.datasets[0].data[i]).toLocaleString()).width;
    c2.restore();
    return Math.max(8, bs.getPixelForValue(0) + 4 + w + 8 + 4 - cs.getPixelForValue(data.datasets[1].data[i]));
  }
  function mobile(){
    axes('xAxisID', ['x', 'x1']);
    data.datasets[0].datalabels = {display: true, anchor: 'start', align: 'right', offset: 4, color: ink, font: {size:11, weight:'700'}, formatter: (v) => v.toLocaleString()};
    data.datasets[1].borderWidth = 2;
    data.datasets[1].pointRadius = 4;
    data.datasets[1].datalabels = {display: true, anchor: 'center', align: 'right', offset: costGap, clip: false, color: ink, font: {size:11, weight:'600'}, formatter: (v) => v.toLocaleString() + '원'};
    return {
      type: 'bar',
      data: data,
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        interaction: {mode:'index', intersect:false},
        layout: { padding: {right: 64} },
        plugins: {
          legend: {position:'bottom', labels:{usePointStyle:true, boxWidth:8}},
        },
        scales: {
          y: {reverse:true, grid:{display:false}, ticks:{font:{size:10.5}, autoSkip:false}},
          x: {position:'top', grid:{color:grid}, title:{display:true,text:'노출수',font:{size:11}}},
          x1:{position:'bottom', grid:{display:false}, title:{display:true,text:'비용(원)',font:{size:11}}}
        }
      }
    };
  }
  var ch = null;
  try { ch = new Chart(canvas, pc()); } catch (e) {}
  (window.__saeroMobileQ = window.__saeroMobileQ || []).push({key: '01', canvas: canvas, data: data, pc: pc, mobile: mobile, chart: ch});
})();
"""

CHART06_C = """/* saero:mobile-branch 06 */
(function(){  // 판 C: PC 는 그대로 · 화면 폭 ≤ M.maxPx 이면 가로(날짜 세로축·최신 위, 순위축 1 이 오른쪽)에 순위 라벨 — 정의·전 기간 배열 그대로
  var canvas = document.getElementById('rankChart');
  var data = {
    labels: [],
    datasets: [{
      label: '평균노출순위',
      data: [],
      borderColor: mintDark,
      backgroundColor: 'rgba(69,206,179,0.12)',
      borderWidth: 3,
      tension: 0.35,
      pointBackgroundColor: mintDark,
      fill: true
    }]
  };
  function title(){ return {display:true, text:'파워링크(노원역필라테스) 일별 평균순위 · 낮을수록 상단', align:'start', font:{size:12,weight:'600'}, color: ink, padding:{bottom:14}}; }
  function pc(){
    delete data.datasets[0].datalabels;
    data.datasets[0].pointRadius = 5;
    return {
      type: 'line',
      data: data,
      options: {
        maintainAspectRatio:false,
        responsive:true,
        plugins:{
          legend:{display:false},
          title: title()
        },
        scales:{
          y:{reverse:true, min:1, grid:{color:grid}, title:{display:true,text:'순위',font:{size:11}}, ticks:{stepSize:1}},
          x:{grid:{display:false}, ticks:{autoSkip:false}}
        }
      }
    };
  }
  function mobile(){
    data.datasets[0].pointRadius = 4;
    data.datasets[0].datalabels = {display: true, anchor: 'center', align: 'right', offset: 8, color: ink, font: {size:10.5, weight:'600'}, formatter: (v) => v.toFixed(2)};
    return {
      type: 'line',
      data: data,
      options: {
        indexAxis: 'y',
        maintainAspectRatio:false,
        responsive:true,
        layout: { padding: {right: 40} },
        plugins:{
          legend:{display:false},
          title: title()
        },
        scales:{
          x:{reverse:true, min:1, position:'top', grid:{color:grid}, title:{display:true,text:'순위',font:{size:11}}, ticks:{stepSize:1}},
          y:{reverse:true, offset:true, grid:{display:false}, ticks:{font:{size:10.5}, autoSkip:false}}
        }
      }
    };
  }
  var ch = null;
  try { ch = new Chart(canvas, pc()); } catch (e) {}
  (window.__saeroMobileQ = window.__saeroMobileQ || []).push({key: '06', canvas: canvas, data: data, pc: pc, mobile: mobile, chart: ch});
})();
"""

# 판 C 분기 도우미(차트 스크립트 끝, 한 번) — @@M@@ 자리에 판 C M 줄(m_line_c). 사슬 중간 단계(B → C)와 C → D 변환의 대조 기준으로만 쓴다(판 D 는 아래 MOBILE_JS).
# getElementById('dailyChart'|'rankChart') 리터럴을 쓰지 않는다(apply·compare 의 첫 일치 앵커).
MOBILE_JS_C = """
/* saero:mobile-helper — 판 C(r2026-10-C, 2026-10-06) 01·06 분기 도우미(차트 스크립트 끝, 한 번).
   위 01·06 블록은 제자리에서 PC 모양으로 만들고 큐(window.__saeroMobileQ)에 넣기만 한다 — 한 스크립트 안 직렬 실행이라 이 도우미는 그 뒤에 정의된다.
   화면 폭 ≤ M.maxPx(= 배포본 CSS 모바일 경계)이면 같은 data 로 가로 막대를 다시 만들고(컨테이너 높이 = 날짜 수 × M.row + M.pad, 원래 min-width·height 는 보관했다가 PC 복귀 때 복원),
   회전·창 크기(matchMedia change)에 다시 판정한다(상태 비교 · 동기 · 안내 sync 직접 · PC 면 최신 쪽 스크롤). 인쇄 중에는 판정을 잠그고,
   모바일이면 01·06 높이를 M.printMaxH 이하로 줄여 한 쪽 안에 찍은 뒤(afterprint) 되돌린다. M 줄은 apply 가 매 회차 config report_layout.mobile 로 다시 쓴다(기계 자리). */
(function(){
  @@M@@
  var mqOk = ('matchMedia' in window);
  var mq = mqOk ? window.matchMedia('(max-width: ' + M.maxPx + 'px)') : null;
  var items = [], state = {mobile: false, printing: false};
  function restore(b){ if (b.dataset.minwidth !== undefined) { b.style.minWidth = b.dataset.minwidth; b.style.height = b.dataset.height; } }
  function build(it, toMobile){
    var b = it.canvas.parentElement;
    try {
      if (it.chart) { it.chart.destroy(); it.chart = null; }
      if (toMobile) {
        if (b.dataset.minwidth === undefined) { b.dataset.minwidth = b.style.minWidth; b.dataset.height = b.style.height; }
        b.style.minWidth = '0';
        b.style.height = (it.data.labels.length * M.row[it.key] + M.pad[it.key]) + 'px';
        it.chart = new Chart(it.canvas, it.mobile());
      } else {
        restore(b);
        it.chart = new Chart(it.canvas, it.pc());
      }
    } catch (e) {
      it.chart = null;
      try { var s = Chart.getChart(it.canvas); if (s) s.destroy(); restore(b); it.chart = new Chart(it.canvas, it.pc()); } catch (e2) {}
    }
  }
  function scrollEnd(){
    if (state.mobile) return;
    items.forEach(function(it){
      var s = it.canvas.closest ? it.canvas.closest('.scroll-x') : null;
      if (!s) return;
      s.scrollLeft = s.scrollWidth;
      try { s.dispatchEvent(new Event('scroll')); } catch (e) {}
    });
  }
  function judge(){
    var m = !!(mqOk && mq.matches);
    if (state.printing || m === state.mobile) return;
    state.mobile = m;
    items.forEach(function(it){ build(it, m); });
    try { if (window.__saeroSync) window.__saeroSync(); } catch (e) {}
    if (!m) scrollEnd();
  }
  window.addEventListener('beforeprint', function(){
    state.printing = true;
    if (!state.mobile) return;
    items.forEach(function(it){
      try {
        var b = it.canvas.parentElement;
        it.printH = b.style.height;
        b.style.height = Math.min(parseFloat(b.style.height) || b.clientHeight, M.printMaxH) + 'px';
        if (it.chart) { it.chart.resize(); it.chart.update('none'); }
      } catch (e) {}
    });
  });
  window.addEventListener('afterprint', function(){
    if (state.mobile) items.forEach(function(it){
      try {
        if (it.printH !== undefined) { it.canvas.parentElement.style.height = it.printH; delete it.printH; }
        if (it.chart) { it.chart.resize(); it.chart.update('none'); }
      } catch (e) {}
    });
    state.printing = false;
  });
  window.__saeroMobile = {M: M, items: items, state: state, build: build, judge: judge, scrollEnd: scrollEnd};
  (window.__saeroMobileQ || []).forEach(function(it){ items.push(it); if (mqOk && mq.matches) build(it, true); }); window.__saeroMobileQ = []; state.mobile = !!(mqOk && mq.matches);
  if (mqOk) { if (mq.addEventListener) mq.addEventListener('change', judge); else if (mq.addListener) mq.addListener(judge); }
})();
"""

# ── 판 D(r2026-10-D, 2026-10-07 — 01 모바일 기간 접기): 모바일 01·06 처음 최근 mobile.recent_days 일 + 펼치기 버튼(01·06 따로) ──
# 배열·min-width·details·태그는 그대로(HTML 1벌) — 접는 것은 화면만. 버튼은 도우미가 모바일에서 카드 아래에 만든다(HTML 텍스트에 태그 0).
MOBILE_CSS_D = """  /* 01·06 모바일 펼치기 버튼(레이아웃 판 r2026-10-D, 2026-10-07) — 차트 스크립트 끝 분기 도우미가 모바일에서만 차트 카드 아래에 만든다(HTML 에는 없음).
     글꼴·색은 03 접기 summary 와 같은 .fold-more 를 같이 달고, 여기서는 버튼 기본 모양(테두리·배경·안쪽 여백·글꼴 묶음)만 지운다 — 새 색 0 */
  .chart-fold{display:block;width:100%;margin:2px 0 0;padding:6px 0;border:0;background:none;font-family:inherit;line-height:1.5;text-align:left;cursor:pointer;-webkit-appearance:none;appearance:none;}
"""

# 01 비용 라벨 간격(costGap) — 판 D 는 그리는 범위(최근 날짜만)를 잘라 그리므로 ctx.dataIndex 는 그 범위 안 번호다: 블록 data 대신 차트가 그리는 data 를 읽는다
COSTGAP_C_TO_D = (("Number(data.datasets[0].data[i])", "Number(ch.data.datasets[0].data[i])"),
                  ("cs.getPixelForValue(data.datasets[1].data[i])", "cs.getPixelForValue(ch.data.datasets[1].data[i])"))

# 판 D 분기 도우미(차트 스크립트 끝, 한 번) — @@M@@ 자리에 config M 줄(m_line). getElementById('dailyChart'|'rankChart') 리터럴을 쓰지 않는다(apply·compare 의 첫 일치 앵커).
MOBILE_JS = """
/* saero:mobile-helper — 판 D(r2026-10-D, 2026-10-07) 01·06 분기 도우미(차트 스크립트 끝, 한 번 — 판 C 도우미 + 모바일 기간 접기).
   위 01·06 블록은 제자리에서 PC 모양으로 만들고 큐(window.__saeroMobileQ)에 넣기만 한다 — 한 스크립트 안 직렬 실행이라 이 도우미는 그 뒤에 정의된다.
   화면 폭 ≤ M.maxPx(= 배포본 CSS 모바일 경계)이면 같은 data 로 가로 막대를 다시 만든다 — 처음에는 최근 M.recent 일만(최신 위 · 배열은 1벌 그대로, 그리는 범위만 자른다).
   날짜가 그보다 많으면 차트 카드 아래 펼치기 버튼(03 접기 summary 와 같은 .fold-more · 문구 "이전 N일(M/D~M/D) 펼치기" 는 data.labels 에서 만든다)이
   전 기간 ↔ 최근을 오간다(01·06 따로 · 문구는 그대로 · 접을 때는 버튼이 그 자리에 남는다). 컨테이너 높이 = 그리는 날짜 수 × M.row + M.pad
   (원래 min-width·height 는 보관했다가 PC 복귀 때 복원). 회전·창 크기(matchMedia change)에 다시 판정한다(상태 비교 · 동기 · 안내 sync 직접 ·
   PC 면 버튼을 걷고 최신 쪽 스크롤 · 모바일로 들어오면 접힘부터). 인쇄 중에는 판정을 잠그고, 모바일이면 접힌 차트를 전 기간으로 다시 그려(애니메이션 없이)
   01·06 높이를 M.printMaxH 이하로 줄여 한 쪽 안에 찍은 뒤(afterprint) 원래 접힘·높이로 되돌린다 — 종이에 날짜 누락 0(03 접기를 인쇄 때 펼치는 것과 같은 원칙).
   M 줄은 apply 가 매 회차 config report_layout.mobile 로 다시 쓴다(기계 자리). 버튼은 화면에만 있다(HTML 텍스트에 없음 — 태그 짝·details 수 그대로). */
(function(){
  @@M@@
  var mqOk = ('matchMedia' in window);
  var mq = mqOk ? window.matchMedia('(max-width: ' + M.maxPx + 'px)') : null;
  var items = [], state = {mobile: false, printing: false};
  function restore(b){ if (b.dataset.minwidth !== undefined) { b.style.minWidth = b.dataset.minwidth; b.style.height = b.dataset.height; } }
  function hidden(it){ var n = it.data.labels.length, k = M.recent[it.key]; return (k > 0 && n > k) ? n - k : 0; }   // 접는 앞쪽 날짜 수(0 = 접지 않음 · 버튼 없음)
  function draw(it, full, quiet){   // 모바일 모양 — full 이면 전 기간, 아니면 최근 M.recent 일(앞쪽 날짜는 그리지 않는다 · 데이터셋 설정은 얕은 복사로 같이)
    var d = it.data, from = full ? 0 : hidden(it);
    if (it.chart) { it.chart.destroy(); it.chart = null; }
    it.canvas.parentElement.style.height = ((d.labels.length - from) * M.row[it.key] + M.pad[it.key]) + 'px';
    var cfg = it.mobile();
    if (from) cfg.data = {labels: d.labels.slice(from), datasets: d.datasets.map(function(s){ var o = {}, k; for (k in s) o[k] = s[k]; o.data = s.data.slice(from); return o; })};
    if (quiet) cfg.options.animation = false;
    it.chart = new Chart(it.canvas, cfg);
  }
  function button(it, on){   // 차트 카드 아래 펼치기 버튼 — 모바일이고 접을 날짜가 있을 때만(없으면 걷는다)
    var n = on ? hidden(it) : 0, L = it.data.labels;
    if (!n) { if (it.btn && it.btn.parentNode) it.btn.parentNode.removeChild(it.btn); it.btn = null; return; }
    if (!it.btn) {
      var card = it.canvas.closest ? it.canvas.closest('.card') : null;
      if (!card) return;
      it.btn = document.createElement('button');
      it.btn.type = 'button';
      it.btn.className = 'fold-more chart-fold';
      it.btn.addEventListener('click', function(){ toggle(it); });
      card.appendChild(it.btn);
    }
    it.btn.textContent = '이전 ' + n + '일(' + String(L[0]).split('(')[0] + '~' + String(L[n - 1]).split('(')[0] + ') 펼치기';
    it.btn.setAttribute('aria-expanded', it.open ? 'true' : 'false');
  }
  function build(it, toMobile){
    var b = it.canvas.parentElement;
    try {
      if (it.chart) { it.chart.destroy(); it.chart = null; }
      if (toMobile) {
        if (b.dataset.minwidth === undefined) { b.dataset.minwidth = b.style.minWidth; b.dataset.height = b.style.height; }
        b.style.minWidth = '0';
        button(it, true);
        draw(it, it.open || !it.btn, false);   // 버튼이 없으면(접을 날짜 없음·카드 못 찾음) 전 기간 — 펼칠 길 없는 접힘 0
      } else {
        button(it, false);
        restore(b);
        it.chart = new Chart(it.canvas, it.pc());
      }
    } catch (e) {
      it.chart = null;
      try { button(it, false); var s = Chart.getChart(it.canvas); if (s) s.destroy(); restore(b); it.chart = new Chart(it.canvas, it.pc()); } catch (e2) {}
    }
  }
  function toggle(it){   // 펼치기 버튼 — 펼치면 전 기간, 다시 누르면 최근만(문구 그대로). 접을 때는 위 차트가 줄어든 만큼 올려 버튼을 그 자리에 둔다
    if (state.printing || !state.mobile || !it.btn) return;
    var bt = it.btn, top = bt.getBoundingClientRect().top;
    it.open = !it.open;
    build(it, true);
    if (!it.open && it.btn === bt) { var dy = bt.getBoundingClientRect().top - top; if (dy) window.scrollBy(0, dy); }
  }
  function scrollEnd(){
    if (state.mobile) return;
    items.forEach(function(it){
      var s = it.canvas.closest ? it.canvas.closest('.scroll-x') : null;
      if (!s) return;
      s.scrollLeft = s.scrollWidth;
      try { s.dispatchEvent(new Event('scroll')); } catch (e) {}
    });
  }
  function judge(){
    var m = !!(mqOk && mq.matches);
    if (state.printing || m === state.mobile) return;
    state.mobile = m;
    items.forEach(function(it){ it.open = false; build(it, m); });
    try { if (window.__saeroSync) window.__saeroSync(); } catch (e) {}
    if (!m) scrollEnd();
  }
  window.addEventListener('beforeprint', function(){
    state.printing = true;
    if (!state.mobile) return;
    items.forEach(function(it){
      try {
        var b = it.canvas.parentElement;
        it.printH = b.style.height;
        if (it.btn && !it.open) { it.printFold = true; draw(it, true, true); }   // 접힌 차트는 전 기간으로(종이에 날짜 누락 0)
        b.style.height = Math.min(parseFloat(b.style.height) || b.clientHeight, M.printMaxH) + 'px';
        if (it.chart) { it.chart.resize(); it.chart.update('none'); }
      } catch (e) {}
    });
  });
  window.addEventListener('afterprint', function(){
    if (state.mobile) items.forEach(function(it){
      try {
        if (it.printFold) { delete it.printFold; draw(it, false, true); }   // 원래 접힘(높이는 draw 가 다시)
        else if (it.printH !== undefined) it.canvas.parentElement.style.height = it.printH;
        delete it.printH;
        if (it.chart) { it.chart.resize(); it.chart.update('none'); }
      } catch (e) {}
    });
    state.printing = false;
  });
  window.__saeroMobile = {M: M, items: items, state: state, build: build, judge: judge, scrollEnd: scrollEnd};
  (window.__saeroMobileQ || []).forEach(function(it){ it.open = false; items.push(it); if (mqOk && mq.matches) build(it, true); }); window.__saeroMobileQ = []; state.mobile = !!(mqOk && mq.matches);
  if (mqOk) { if (mq.addEventListener) mq.addEventListener('change', judge); else if (mq.addListener) mq.addListener(judge); }
})();
"""

# 가로 안내 스크립트(별도 script) — S(스크롤 시작 최신 쪽)·회전 규약 네 줄. (c)(d) 는 FOLD_JS 마지막 줄 뒤.
AFTERPRINT = "  window.addEventListener('afterprint', function(){ folded.forEach(function(d){ d.open = false; }); folded = []; });\n"
SYNC_JS = ("  window.__saeroSync = sync; // 판 C: 01·06 분기 도우미(차트 스크립트 끝)가 회전 뒤 안내·페이드를 바로 다시 맞춘다\n"
           "  window.addEventListener('load', function(){ setTimeout(function(){ if (window.__saeroMobile) window.__saeroMobile.scrollEnd(); }, 0); }); "
           "// 판 C: PC 01·06 은 최신 쪽(오른쪽 끝)에서 시작 — load 의 sync(래퍼 감싸기) 뒤\n")


M_LINE = re.compile(r'var M = \{maxPx: \d+, printMaxH: \d+, row: \{"01": \d+, "06": \d+\}, pad: \{"01": \d+, "06": \d+\}, recent: \{"01": \d+, "06": \d+\}\};')

# ── 판 E(r2026-10-E, 2026-10-08 — 01 모바일 터치 날짜): 01 모바일 모양(가로 막대 · indexAxis 'y')의 interaction 에 axis:'y' ──
# Chart.js 4 의 index 모드는 axis 를 안 주면 x(가로 거리)로 가장 가까운 요소를 고른다 — 날짜가 세로로 쌓인 모바일 01 에서는 터치한 줄과 무관하게
# 가로 위치가 비슷한 막대 끝·비용 점의 날짜 팝업이 떴다(배포본 10-08 재현: 10/7 줄 왼쪽 → 9/25). 앵커 = 01 mobile() 의 interaction 줄 + 바로 다음 padding 줄
# (PC 모양 padding top:24 · 09 hourlyChart 들여쓰기 4칸과 갈린다 — 정확히 하나). 판 C·D 템플릿(CHART01_C)은 사슬 중간 단계라 그대로 둔다.
TOUCH_D_TO_E = ("        interaction: {mode:'index', intersect:false},\n        layout: { padding: {right: 64} },",
                "        interaction: {mode:'index', intersect:false, axis:'y'},\n        layout: { padding: {right: 64} },")

# ── 판 F(r2026-10-F, 2026-10-09 — 광고비 잔액 카드): KPI 카드 넷 아래 한 줄 전체 카드 하나(.kpi-row 다섯째 자식 · 데스크톱·모바일 같은 모양) ──
# 카드 넷 마크업은 그대로 두고 넷째 카드(총 광고비 — "클릭당 평균 N원" sub) 바로 뒤, .kpi-row 닫힘 앞에 넣는다. 값·보조 줄은 data-balance 표지 안 — 매 회차 apply 가
# compute.json "잔액"(← balance.py 가 읽은 비즈머니 · compute.py --balance)으로 둘 다 다시 쓴다(실패 기록이면 "확인 못 함" — 옛 값이 새 시각과 같이 남는 길 0).
# data-balance 속성 덕분에 기존 KPI 앵커(validate parse_kpi_tiles · apply 총 광고비 once · compare _kpi 의 sub 순번)에 잡히지 않는다. 새 색 0(accent = 넷째 카드 값).
LAYOUT_F = "r2026-10-F"
CARD_LAYOUTS = (LAYOUT_F,)   # 잔액 카드가 있는 판(apply 가 값을 쓰고 표지 수를 대조하는 판)
BALANCE_CSS = """  /* 광고비 잔액 카드(레이아웃 판 r2026-10-F, 2026-10-09) — KPI 카드 넷 아래 한 줄 전체(데스크톱 4칸·모바일 2칸 모두 grid-column 1 / -1). 모양·색은 .kpi 그대로 — 새 색 0.
     값·보조 줄(data-balance)은 scripts/apply.py 가 매 회차 compute.json 의 잔액(scripts/balance.py 가 읽은 비즈머니)으로 쓴다(기계 자리) */
  .kpi-wide{grid-column:1 / -1;}
"""
BALANCE_CARD = """    <div class="kpi kpi-wide" style="--accent:#1c2b2a;">
      <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 7V5.5A1.5 1.5 0 0 0 17.5 4H5a2 2 0 0 0 0 4h14a1 1 0 0 1 1 1v3"/><path d="M3 6v12a2 2 0 0 0 2 2h14a1 1 0 0 0 1-1v-3"/><path d="M21 12h-4a2 2 0 0 0 0 4h4z"/></svg></div>
      <div class="label">광고비 잔액</div>
      <div class="value" data-balance="value">확인 못 함</div>
      <div class="sub" data-balance="sub">—</div>
    </div>
"""
KPI_END = r'(<div class="sub">클릭당 평균 [\d,]+원</div>\n    </div>\n)(  </div>\n)'   # 넷째 카드 끝 + .kpi-row 닫힘(정확히 하나)
BAL_VALUE = r'(<div class="value" data-balance="value">)[^\n]*?(</div>)'
BAL_SUB = r'(<div class="sub" data-balance="sub">)[^<\n]*(</div>)'
BAL_STAMP = re.compile(r"\d{1,2}/\d{1,2}\([월화수목금토일]\) \d{2}:\d{2}")


def m_line_c(lay):
    """판 C 도우미의 M 줄(사슬 중간 단계 B → C 전용 — 판 D 변환이 도우미째 바꾼다)."""
    m = lay["mobile"]
    row, pad = m["row_px"], m["pad_px"]
    return (f'var M = {{maxPx: {int(m["max_px"])}, printMaxH: {int(m["print_max_height_px"])}, '
            f'row: {{"01": {int(row["01"])}, "06": {int(row["06"])}}}, pad: {{"01": {int(pad["01"])}, "06": {int(pad["06"])}}}}};')


def m_line(lay):
    """config report_layout.mobile → 판 D 분기 도우미의 M 줄(한 줄 리터럴 — 매 회차 기계 자리). recent = 모바일 처음 그리는 최근 일수(01·06)."""
    rec = lay["mobile"]["recent_days"]
    return m_line_c(lay)[:-2] + f', recent: {{"01": {int(rec["01"])}, "06": {int(rec["06"])}}}}};'


def chart_block(h, cid, tpl):
    """`new Chart(document.getElementById('<cid>'), {` 부터 그 뒤 첫 `\\n});\\n` 까지(끝 포함)를 tpl 로. 시작이 정확히 하나·블록 안 new Chart 하나여야."""
    start = f"new Chart(document.getElementById('{cid}'), {{"
    if h.count(start) != 1:
        raise ApplyError(f"차트 블록 시작 {start!r} 가 정확히 하나가 아님({h.count(start)}개)")
    i = h.index(start)
    j = h.find("\n});\n", i)
    if j == -1:
        raise ApplyError(f"차트 블록 {cid} 끝(첫 줄머리 '}});') 없음")
    j += len("\n});\n")
    if h.count("new Chart(", i, j) != 1:
        raise ApplyError(f"차트 블록 {cid} 안에 new Chart 가 {h.count('new Chart(', i, j)}개 — 블록 끝을 잘못 찾음")
    return h[:i] + tpl + h[j:]


def check_branches(h, lay, why):
    n = {k: len([x for x in BRANCH.findall(h) if x == k]) for k in ("01", "06")}
    want = int(lay["markers"]["mobile_branch"])
    if n["01"] != 1 or n["06"] != 1 or n["01"] + n["06"] != want:
        raise ApplyError(f"{why} 분기 표지 {n['01'] + n['06']}개(01 {n['01']} · 06 {n['06']}) ≠ config {want} — 손으로 바꾼 판으로 보임")


def convert_b_to_c(h, lay):
    """레이아웃 판 r2026-10-B → r2026-10-C(01·06 모바일 가로 막대). 앵커는 전부 once(정확히 하나) — 서술 표지 블록·섹션 HTML·min-width 텍스트는 건드리지 않는다.
    값(01·06 배열·M 줄)은 뒤의 apply 가 채운다(템플릿의 빈 [] · M 줄)."""
    h = once(r'<meta name="report-layout" content="r2026-10-B">', f'<meta name="report-layout" content="{LAYOUT_C}">', h)   # ①
    h = once(r"(\n</style>)", lambda m: "\n" + MOBILE_CSS.rstrip("\n") + m.group(1), h)                                    # ② 왼쪽 페이드
    h = chart_block(h, "dailyChart", CHART01_C)                                                                              # ③
    h = chart_block(h, "rankChart", CHART06_C)                                                                               # ④
    h = once(r"\n\}\);\n</script>\n", lambda m: "\n});\n\n" + MOBILE_JS_C.lstrip("\n").replace("@@M@@", m_line_c(lay)) + "</script>\n", h)   # ⑤ 차트 스크립트 끝
    # ⑥ 안내 스크립트 S·sync 규약 네 줄
    h = once(r"([ \t]*)(wrapper\.classList\.toggle\('at-end', atEnd\);)",
             lambda m: f"{m.group(1)}{m.group(2)}\n{m.group(1)}wrapper.classList.toggle('at-start', box.scrollLeft <= 2);", h)                  # (a)
    h = once(re.escape("box.parentNode.classList.add('at-end'); // 페이드 숨김"),
             lambda m: "box.parentNode.classList.add('at-end', 'at-start'); // 페이드 둘 다 숨김", h)                                       # (b)
    h = once(re.escape(AFTERPRINT), lambda m: AFTERPRINT + SYNC_JS, h)                                                                         # (c)(d)
    check_branches(h, lay, "변환 뒤")                                                                                                          # ⑦
    return h


def convert_c_to_d(h, lay):
    """레이아웃 판 r2026-10-C → r2026-10-D(모바일 01·06 기간 접기). 앵커는 전부 정확히 하나 — 섹션 HTML·서술 표지·min-width 텍스트·배열·
    01·06 블록의 나머지·가로 안내 스크립트는 건드리지 않는다. 판 C 분기 도우미는 템플릿(M 줄 빼고)과 바이트가 같을 때만 판 D 도우미로 바꾼다."""
    h = once(rf'<meta name="report-layout" content="{LAYOUT_C}">', f'<meta name="report-layout" content="{LAYOUT_D}">', h)        # ①
    h = once(r"(\n</style>)", lambda m: "\n" + MOBILE_CSS_D.rstrip("\n") + m.group(1), h)                                        # ② 펼치기 버튼 CSS
    for old, new in COSTGAP_C_TO_D:                                                                                                # ③ 01 비용 라벨 간격
        h = once(re.escape(old), lambda m, new=new: new, h)
    i = find1(h, "/* saero:mobile-helper")                                                                                         # ④ 분기 도우미
    if h.count("/* saero:mobile-helper") != 1:
        raise ApplyError(f"분기 도우미 시작 표지가 {h.count('/* saero:mobile-helper')}개 — 손으로 바꾼 판으로 보임")
    j = find1(h, "\n})();\n", i) + len("\n})();\n")
    if re.sub(r"var M = \{[^\n]*\};", "@@M@@", h[i:j], count=1) != MOBILE_JS_C.lstrip("\n"):
        raise ApplyError("판 C 분기 도우미가 템플릿(M 줄 빼고)과 다름 — 손으로 바꾼 판으로 보임, 변환하지 않음")
    h = h[:i] + MOBILE_JS.lstrip("\n").replace("@@M@@", m_line(lay)) + h[j:]
    check_branches(h, lay, "변환 뒤")                                                                                              # ⑤
    return h


def convert_d_to_e(h, lay):
    """레이아웃 판 r2026-10-D → r2026-10-E(01 모바일 터치 날짜). 바뀌는 곳은 meta 와 01 모바일 interaction 한 줄뿐 — 앵커 둘 다 정확히 하나.
    01 블록을 손으로 바꿔 그 줄이 없거나 둘이면 FAIL(변환 안 함)."""
    h = once(rf'<meta name="report-layout" content="{LAYOUT_D}">', f'<meta name="report-layout" content="{LAYOUT_E}">', h)        # ①
    h = once(re.escape(TOUCH_D_TO_E[0]), lambda m: TOUCH_D_TO_E[1], h)                                                            # ② 01 모바일 터치 축
    check_branches(h, lay, "변환 뒤")                                                                                              # ③
    return h


def check_balance(h, lay, why):
    """판 F 잔액 카드 표지 — 값·보조 줄 각 config markers.balance_card(1) · .kpi-row 안 넷째 카드("클릭당 평균") 뒤 · 01 섹션 앞."""
    want = int(lay["markers"].get("balance_card", 1))
    nv, ns = h.count('data-balance="value"'), h.count('data-balance="sub"')
    if nv != want or ns != want:
        raise ApplyError(f"{why} 잔액 카드 표지 값 {nv} · 보조 줄 {ns} ≠ config {want} — 손으로 바꾼 판으로 보임")
    kr, iv, s1 = h.find('<div class="kpi-row">'), h.find('data-balance="value"'), h.find("<!-- Section 1:")
    if not (-1 < kr < h.rfind("클릭당 평균", 0, iv) < iv < s1):
        raise ApplyError(f"{why} 잔액 카드가 .kpi-row 안 넷째 카드 뒤(01 섹션 앞)가 아님 — 손으로 옮긴 판으로 보임")


def convert_e_to_f(h, lay):
    """레이아웃 판 r2026-10-E → r2026-10-F(광고비 잔액 카드). 바뀌는 곳 = meta · `</style>` 앞 CSS(.kpi-wide) · .kpi-row 끝(넷째 카드 뒤)에 카드 하나 —
    앵커 셋 다 정확히 하나. 카드 넷·섹션 HTML·서술 표지·스크립트는 건드리지 않는다. 카드 값·보조 줄은 뒤의 apply 가 compute.json "잔액"으로 쓴다(템플릿은 자리만)."""
    if "data-balance=" in h:
        raise ApplyError("판 E 인데 잔액 카드 표지(data-balance)가 이미 있음 — 손으로 넣은 판으로 보임, 변환하지 않음")
    h = once(rf'<meta name="report-layout" content="{LAYOUT_E}">', f'<meta name="report-layout" content="{LAYOUT_F}">', h)        # ①
    h = once(r"(\n</style>)", lambda m: "\n" + BALANCE_CSS.rstrip("\n") + m.group(1), h)                                         # ② 한 줄 전체 CSS
    h = once(KPI_END, lambda m: m.group(1) + BALANCE_CARD + m.group(2), h)                                                         # ③ 카드(넷째 카드 뒤)
    check_balance(h, lay, "변환 뒤")                                                                                               # ④
    return h


def balance_values(h, R):
    """판 F 카드 값·보조 줄(매 회차 — 변환을 건너뛴 회차에도). compute.json "잔액" 이 없으면 FAIL(카드를 옛 값으로 두지 않는다).
    ok → `217,817<span class="unit">원</span>` · `10/9(금) 14:34 기준 · 약 24일분`(일분 None 이면 ` · 약 …` 없음) / fail → `확인 못 함` · `10/9(금) 14:34 조회 실패`."""
    b = R.get("잔액")
    if not isinstance(b, dict):
        raise ApplyError('compute.json 에 "잔액" 없음 — 5단계는 balance.py → compute.py … --balance work/balance.json → apply.py 순서(카드를 옛 값으로 두지 않음)')
    stamp = b.get("기준")
    if not isinstance(stamp, str) or not BAL_STAMP.fullmatch(stamp):
        raise ApplyError(f'compute.json "잔액" 기준 {stamp!r} 꼴이 다름(M/D(요일) HH:MM)')
    if b.get("상태") == "ok":
        won, days = b.get("원"), b.get("일분")
        if isinstance(won, bool) or not isinstance(won, int) or won < 0 or not (days is None or (isinstance(days, int) and not isinstance(days, bool) and days >= 0)):
            raise ApplyError(f'compute.json "잔액" 원 {won!r} · 일분 {days!r} 꼴이 다름')
        val, sub = f'{c(won)}<span class="unit">원</span>', f"{stamp} 기준" + ("" if days is None else f" · 약 {c(days)}일분")
    elif b.get("상태") == "fail":
        val, sub = "확인 못 함", f"{stamp} 조회 실패"
    else:
        raise ApplyError(f'compute.json "잔액" 상태 {b.get("상태")!r} — ok|fail 이어야')
    h = once(BAL_VALUE, lambda m: m.group(1) + val + m.group(2), h)
    return once(BAL_SUB, lambda m: m.group(1) + sub + m.group(2), h)


# 판 사슬 — (옛 판, 새 판, 변환). meta 가 사슬 위에 있으면 config 판까지 차례로(--layout 일 때만)
STEPS = (("r2026-10-B", LAYOUT_C, convert_b_to_c), (LAYOUT_C, LAYOUT_D, convert_c_to_d), (LAYOUT_D, LAYOUT_E, convert_d_to_e),
         (LAYOUT_E, LAYOUT_F, convert_e_to_f))


def chain(frm, to):
    """frm 판에서 to 판까지의 변환 목록(사슬 순서) — 닿지 못하면 None."""
    path = []
    for a, b, f in STEPS:
        if frm == to:
            break
        if frm == a:
            path.append(f)
            frm = b
    return path if frm == to else None


def trs(block):
    return re.findall(r"<tr[^>]*>.*?</tr>", block, re.S)


def td(v, cls="num"):
    return f'            <td class="{cls}">{v}</td>'


def tr(cells, style=""):
    return "          <tr" + style + ">\n" + "\n".join(cells) + "\n          </tr>"


def apply(h, R, cfg, layout=False):
    """layout = --layout(옛 판·사슬 위 옛 판이면 config 판까지 변환). meta = config layout_id 면 변환 없이 값만(멱등).
    판 사슬: meta 없음 → convert_layout(LAYOUT_B) → convert_b_to_c → convert_c_to_d → convert_d_to_e → convert_e_to_f · meta r2026-10-B → C → D → E → F ·
    meta r2026-10-C·D·E → … → F · meta = config → 값만 · 사슬 밖 FAIL. config 대조(details 수 · 분기 표지 수 · 판 F 잔액 카드 표지)는 사슬 끝에 한 번(값만 경로 포함).
    판 F 는 compute.json "잔액" 이 없으면 FAIL(balance_values)."""
    lay = cfg["report_layout"]
    lid, k = lay["layout_id"], int(lay["recent_days"])
    if k < 1:
        raise ApplyError(f"config report_layout.recent_days {k} — 1 이상이어야 함")
    metas = LAYOUT_META.findall(h)
    if len(metas) > 1:
        raise ApplyError(f'<meta name="report-layout"> 가 {len(metas)}개')
    bid = LAYOUT_B["layout_id"]
    if not metas:
        if not layout:
            raise ApplyError(f"레이아웃 판 meta 없음 — --layout 을 붙여 다시(옛 모양 → {lid} 변환 + 값 교체)")
        path = chain(bid, lid)
        if path is None:
            raise ApplyError(f"config 레이아웃 판 {lid!r} 은 판 사슬 밖 — 옛 모양에서 바꾸는 변환이 없음")
        h = convert_layout(h, LAYOUT_B)
    else:
        path = chain(metas[0], lid)
        if path is None:
            raise ApplyError(f"레이아웃 판 meta {metas[0]!r} ≠ config {lid!r} — 이 판에서 바꾸는 변환은 없음(판 변경은 설계 회차·사용자 결정)")
        if path and not layout:
            raise ApplyError(f"레이아웃 판 meta {metas[0]} ≠ config {lid} — --layout 을 붙여 {metas[0]} → {lid}")
    for f in path:
        h = f(h, lay)
    if LAYOUT_META.findall(h) != [lid]:
        raise ApplyError(f"변환 뒤 레이아웃 판 meta {LAYOUT_META.findall(h)} ≠ config {lid!r}")
    if len(DETAILS.findall(h)) != int(lay["markers"]["details"]):
        raise ApplyError(f"레이아웃 판 {lid} 인데 details {len(DETAILS.findall(h))}개 ≠ config {lay['markers']['details']} — 접기를 손으로 바꾼 판으로 보임")
    check_branches(h, lay, f"레이아웃 판 {lid} 인데")
    if lid in CARD_LAYOUTS:
        check_balance(h, lay, f"레이아웃 판 {lid} 인데")
    h = once(M_LINE.pattern, lambda m: m_line(lay), h)   # 분기 도우미 M 줄 = config report_layout.mobile(매 회차 — 변환을 건너뛴 회차에도)
    if lid in CARD_LAYOUTS:
        h = balance_values(h, R)                          # 판 F 잔액 카드 값·보조 줄(매 회차 — compute.json "잔액")
    K = R["KPI"]
    # masthead·og·KPI
    h = once(r"(집계 기간<b>)[^<]+(</b>)", rf'\g<1>{R["masthead"]}\g<2>', h)
    h = once(r'(og:description" content=")[^"]+', rf'\g<1>{R["og"]}', h)
    for label, val in [("총 노출수", c(K["노출"])), ("총 클릭수", c(K["클릭"])), ("평균 클릭률", f"{K['CTR']:g}"), ("총 광고비", c(K["광고비"]))]:
        h = once(rf'(<div class="label">{label}</div>\s*<div class="value">)[^<]+', rf"\g<1>{val}", h)
    h = once(r'일 평균 [\d.]+회(</div>\s*</div>\s*<div class="kpi" style="--accent:#2ea88f;">)', rf'일 평균 {K["일평균노출"]}회\g<1>', h)
    h = once(r'(총 클릭수</div>\s*<div class="value">[^<]+<span class="unit">회</span></div>\s*<div class="sub">)일 평균 [\d.]+회', rf'\g<1>일 평균 {K["일평균클릭"]}회', h)
    h = once(r"클릭당 평균 [\d,]+원", f'클릭당 평균 {c(K["클릭당"])}원', h)
    h = re.sub(r'min-width:\s*\d+px;">(\s*<canvas id="(?:dailyChart|rankChart)")', rf'min-width:{R["minwidth"]}px;">\g<1>', h)
    h = re.sub(r'(height:280px; )min-width:\d+px;(">\s*<canvas id="dailyChart")', rf'\g<1>min-width:{R["minwidth"]}px;\g<2>', h)
    # 01·06 두 컨테이너만 센다(옛 판은 문서 전체 개수 — 기간 8일 이하면 바닥값 650px 이 09번 고정 650px 과 겹쳐 3이 됨)
    n_mw = len(re.findall(rf'min-width:{R["minwidth"]}px;">\s*<canvas id="(?:dailyChart|rankChart)"', h))
    if n_mw != 2:
        raise ApplyError(f'차트 min-width:{R["minwidth"]}px 가 2곳(dailyChart·rankChart)이 아니라 {n_mw}곳')

    # 차트 배열·라벨 — getElementById('<id>') 부터 다음 new Chart 까지 안에서 한 번
    def chart(h, cid, label, arr, fmt=str):
        i = find1(h, f"getElementById('{cid}')")
        j = h.find("new Chart", i + 10)
        j = len(h) if j == -1 else j
        pat = rf"(label:\s*'{label}'\s*,\s*data:\s*\[)[^\]]*" if label else r"(data:\s*\[)[^\]]*"
        blk, n = re.subn(pat, lambda m: m.group(1) + ", ".join(fmt(x) for x in arr), h[i:j], count=1)
        if n != 1:
            raise ApplyError(f"차트 {cid} {label or 'data'} 배열 없음")
        return h[:i] + blk + h[j:]

    def labels(h, cid, arr):
        i = find1(h, f"getElementById('{cid}')")
        j = h.find("new Chart", i + 10)
        j = len(h) if j == -1 else j
        blk, n = re.subn(r"labels:\s*\[[^\]]*\]", "labels: [" + ",".join(f"'{x}'" for x in arr) + "]", h[i:j], count=1)
        if n != 1:
            raise ApplyError(f"차트 {cid} labels 없음")
        return h[:i] + blk + h[j:]

    h = labels(h, "dailyChart", R["01"]["labels"]); h = labels(h, "rankChart", R["01"]["labels"])
    h = chart(h, "dailyChart", "노출수", R["01"]["노출"]); h = chart(h, "dailyChart", r"총비용\(원\)", R["01"]["총비용"])
    h = chart(h, "groupChart", "노출수", R["02"]["groupChart"]["노출"]); h = chart(h, "groupChart", "클릭수", R["02"]["groupChart"]["클릭"])
    h = chart(h, "costPie", None, R["02"]["costPie"])
    h = once(r"광고비 비중 \(총 [\d,]+원\)", f'광고비 비중 (총 {c(K["광고비"])}원)', h)
    h = chart(h, "mediaChart", "노출수", [t["노출"] for t in R["05"]["top5"]]); h = chart(h, "deviceChart", None, R["05"]["device"])
    h = chart(h, "rankChart", "평균노출순위", R["06"]["rankChart"], lambda x: f"{x:.2f}")
    h = chart(h, "hourlyChart", "노출수", R["09"]["노출"]); h = chart(h, "hourlyChart", "클릭수", R["09"]["클릭"])
    h = chart(h, "placementChart", "노출수", R["10"]["placement"]["노출"]); h = chart(h, "placementChart", "클릭수", R["10"]["placement"]["클릭"])

    # 01 표·순위 5칸 — 순위 5칸 끝 앵커는 서술 없이 grid 닫는 줄 + 다음 note 여는 태그(서술 표지 유무와 무관)
    rows = [tr([td(r["날짜"], "name-cell"), td(r["노출"]), td(r["검색"]), td(r["콘텐츠"]), td(r["클릭"]),
                td(f"{r['CTR']:.2f}%", "num ctr-high" if r["hl"] else "num"), td(f"{c(r['CPC'])}원")]) for r in R["01"]["표5"]]
    h, _ = tbody(h, "① 일별 지표", "\n".join(rows) + "\n")
    cells = []
    for g in R["01"]["플레이스순위5"]:
        col = "color:var(--mint-dark);" if g["날짜"] == R["01"]["순위민트"] else ""
        cells.append(f'        <div>\n          <div style="font-size:11px;color:var(--ink-soft);margin-bottom:2px;">{g["날짜"]}</div>\n'
                     f'          <div style="font-size:15px;font-weight:800;{col}">{g["순위"]:.2f}위</div>\n        </div>')
    h = once(r'(<div style="display:grid;grid-template-columns:repeat\(5,1fr\);gap:6px;margin-bottom:6px;">\n).*?(\n      </div>\n      <div class="note">)',
             lambda m: m.group(1) + "\n".join(cells) + m.group(2), h, re.S)

    # 03 — 위 표 = 합계(굵게) + 최근 recent_days 일 최신 위 · 접힌 표 = 나머지 날짜 최신 위(DOM 전체 = 합계 + 날짜 역순) · summary "이전 N일(M/D~M/D)"
    def p3(v):
        return [td(f"{c(v[0])}원"), td(v[1]), td("–" if v[2] is None else f"{c(v[2])}원")]

    def row3(r):
        return tr([td(r["날짜"], "name-cell")] + p3(r["플레이스"]) + p3(r["파워링크"]) + [td(f"{c(r['합계'])}원")])
    rows3 = R["03"]["rows"]
    recent, older = rows3[-k:][::-1], rows3[:-k][::-1]
    T = R["03"]["합계"]
    top = [tr([td("합계", "name-cell")] + p3(T["플레이스"]) + p3(T["파워링크"]) + [td(f"{c(T['총'])}원")], ' style="font-weight:800;"')] + [row3(r) for r in recent]
    h, _ = tbody(h, "<!-- Section 3", "\n".join(top) + "\n        ")
    i3, i4 = bounds(h, 3)
    h, _ = tbody(h, "<summary", "".join(row3(r) + "\n" for r in older) + "        ", start=i3, stop=i4)   # 접힌 표 = 03 첫 summary 뒤 첫 tbody

    def md(r):
        return r["날짜"].split("(")[0]
    h = once_in(h, 3, r"(<summary[^>]*>)이전 \d+일(?:\([^)<]*\))? 펼치기(</summary>)",
                lambda m: m.group(1) + (f"이전 {len(older)}일({md(older[-1])}~{md(older[0])}) 펼치기" if older else "이전 0일 펼치기") + m.group(2))

    # 04 — 유형 태그·이름 칸 메모는 직전 행 그대로(새 그룹이면 멈춤)
    h, old = tbody(h, "<!-- Section 4", "@@04@@")
    prev = {}
    for t in trs(old):
        tds = re.findall(r"<td[^>]*>.*?</td>", t, re.S)
        prev[re.sub(r"<[^>]+>", "", tds[1]).split("(")[0].strip()] = tds[:2]
    rows = []
    for r in R["04"]["rows"]:
        if r["그룹"] not in prev:
            raise ApplyError(f"04 표에 없는 새 그룹 {r['그룹']!r} — 유형 태그·이름 칸을 사람이 한 행 넣은 뒤 다시")
        a, b = prev[r["그룹"]]
        rows.append(tr(["            " + a, "            " + b, td(c(r["노출"])), td(r["클릭"]), td(f"{r['CTR']:.2f}%"), td(f"{c(r['총비용'])}원"),
                        td(f"{c(r['CPC'])}원"), td(f"{r['비중']:.1f}%"), td("—" if r["순위"] is None else f"{r['순위']:.2f}위")]))
    h = h.replace("@@04@@", "\n" + "\n".join(rows) + "\n        ", 1)

    # 06 매칭표·카드
    for name, key in [("직접 등록 키워드", "직접"), ("자동매칭( - )", "자동")]:
        v = R["06"][key]
        h = once(rf"({re.escape(name)}<br>.*?</td>\s*<td class=\"num\">)[\d,]+(</td>\s*<td class=\"num\">)\d+(</td>\s*<td class=\"num\">)[\d.]+(위</td>\s*<td class=\"num\">)[\d,]+원",
                 lambda m, v=v: f"{m.group(1)}{c(v['노출'])}{m.group(2)}{v['클릭']}{m.group(3)}{v['순위']:.1f}{m.group(4)}{c(v['총비용'])}원", h, re.S)
    for g, v in R["06"]["카드"].items():
        h = once(rf'({re.escape(g)} <span style="color:var\(--mint-dark\);font-weight:700;">\({v["등록일"]} 등록, )\d+(일차\).*?font-weight:800;color:var\(--mint-dark\);">)[\d.]+위',
                 lambda m, v=v: f"{m.group(1)}{v['일차']}{m.group(2)}{v['순위']:.2f}위", h, re.S)

    # 07 정식표 — <!-- Section 7 뒤 첫 tbody(정식표 앞에 다른 table 금지)
    def tag(m):
        return f'<span class="tag tag-mint">{m}</span>' if m.startswith("일치") else f'<span class="tag tag-ink">{m}</span>'
    rows = [tr([td(r["검색어"], "name-cell"), f'            <td>{tag(r["매칭"].replace("*동률", ""))}</td>', td(r["노출"]), td(r["클릭"]),
                td(f"{r['CTR']:.2f}%", "num ctr-high" if r["hl"] else "num"), td(f"{c(r['CPC'])}원"), td(f"{c(r['총비용'])}원")]) for r in R["07"]["정식표"]]
    h, _ = tbody(h, "<!-- Section 7", "\n".join(rows) + "\n          ")

    def keep_order(new, old_names, key):  # 정렬 키 동률은 직전 순서 유지, 새 이름은 뒤
        pos = {n: i for i, n in enumerate(old_names)}
        return sorted(new, key=lambda x: key(x) + (pos.get(x["검색어"] if "검색어" in x else x["지역"], 10**6),))

    def old_list(h, anchor):
        a = find1(h, "line-height:1.9;\">", find1(h, anchor)) + len("line-height:1.9;\">")
        return [x.split("(")[0].strip() for x in re.sub(r"\s+", " ", h[a:]).split("</div>")[0].split(" · ")]

    def listblock(h, anchor, text):  # 앵커 → 첫 line-height:1.9;"> → 첫 </div>
        a = find1(h, "line-height:1.9;\">", find1(h, anchor)) + len("line-height:1.9;\">")
        b = find1(h, "</div>", a)
        return h[:a] + "\n            " + text + "\n          " + h[b:]

    L1 = keep_order(R["07"]["클릭1"], old_list(h, "클릭 1건 검색어"), lambda x: (-x["노출"],))
    h = listblock(h, "클릭 1건 검색어", " · ".join(f"{x['검색어']}({x['노출']}회/{c(x['총비용'])}원)" for x in L1))
    L0 = keep_order(R["07"]["클릭0목록"], old_list(h, "노출은 있으나 클릭 0건인"), lambda x: (-x["노출"],))
    h = listblock(h, "노출은 있으나 클릭 0건인", " · ".join(f"{x['검색어']}({x['노출']}회)" for x in L0))
    h = once_in(h, 7, r"(클릭 1건 검색어 <span[^>]*>\()\d+(개 · 펼치기\)</span>)", lambda m: f"{m.group(1)}{len(R['07']['클릭1'])}{m.group(2)}")
    h = once_in(h, 7, r"(노출은 있으나 클릭 0건인 검색어 <span[^>]*>\(노출 5회 이상 )\d+(개 · 펼치기\)</span>)", lambda m: f"{m.group(1)}{len(R['07']['클릭0목록'])}{m.group(2)}")

    # 07 경쟁사표 — 소재구·매칭 칸은 직전 행 그대로, 직전 표에 없는 신규 변형만 config competitor_defaults
    h, old = tbody(h, "경쟁사 브랜드명 검색어</div>", "@@07c@@")
    prev = {}
    for t in trs(old):
        tds = re.findall(r"<td[^>]*>.*?</td>", t, re.S)
        prev[re.sub(r"<[^>]+>", "", tds[0])] = tds[1:3]
    dflt = cfg["competitor_defaults"]
    newc = [f'<td>{dflt["district"]}</td>', f'<td>{tag(dflt["match"])}</td>']
    rows = []
    for r in R["07"]["경쟁사표"]:
        cells = prev.get(r["검색어"])
        if cells is None:
            if r["검색어"] not in R["07"]["신규변형후보"]:
                raise ApplyError(f"07 경쟁사표에 직전 행도 신규 변형 후보도 아닌 이름 {r['검색어']!r}")
            cells = newc
        rows.append(tr([td(r["검색어"], "name-cell"), "            " + cells[0], "            " + cells[1], td(r["노출"]), td(r["클릭"]), td(f"{c(r['총비용'])}원")]))
    h = h.replace("@@07c@@", "\n" + "\n".join(rows) + "\n        ", 1)
    h = once_in(h, 7, r"(<summary[^>]*>표 )\d+(행 · 펼치기</summary>)", lambda m: f"{m.group(1)}{len(R['07']['경쟁사표'])}{m.group(2)}")

    # 08
    rows = [tr([td(r["지역"], "name-cell"), td(c(r["노출"])), td(r["클릭"]), td(f"{c(r['총비용'])}원")]) for r in R["08"]["top10"]]
    h, _ = tbody(h, "<!-- Section 8", "\n".join(rows) + "\n        ")

    def short(f):  # compare.py short() 와 같은 표(report-structure.md 08번)
        return (f.replace("서울특별시 ", "").replace("경기도 ", "").replace("인천광역시 ", "인천 ").replace("광주광역시 ", "광주 ")
                .replace("전남광주통합특별시 ", "광주 ").replace("부산광역시 ", "부산 ").replace("경상북도 ", "").replace("세종특별자치시", "세종시"))
    L8 = keep_order([dict(x, 지역=short(x["지역"])) for x in R["08"]["컴팩트"]], old_list(h, "TOP 10 외"), lambda x: (-x["클릭"], -x["노출"]))
    h = listblock(h, "TOP 10 외", " · ".join(f"{x['지역']}(노출{x['노출']}·클릭{x['클릭']})" for x in L8))
    h = once(r"\(\d+개 지역·클릭 \d+건\)", f"({R['08']['컴팩트수']}개 지역·클릭 {R['08']['컴팩트클릭']}건)", h)

    # 10 표 4행 — A·B·C·D 순서
    i10 = find1(h, "<!-- Section 10")
    a = find1(h, "<tbody>", i10)
    b = find1(h, "</tbody>", a)
    it = iter([R["10"][k] for k in "ABCD"])
    blk, n = re.subn(r'(</td>\s*<td>[^<]*</td>\s*<td class="num">)[\d,]+(</td>\s*<td class="num">)[\d,]+(</td>\s*<td class="num">)[\d,]+원',
                     lambda m: (lambda v: f"{m.group(1)}{c(v[0])}{m.group(2)}{c(v[1])}{m.group(3)}{c(v[2])}원")(next(it)), h[a:b])
    if n != 4:
        raise ApplyError(f"10 표 행이 4개가 아님({n}개)")
    return h[:a] + blk + h[b:]


def main():
    ap = argparse.ArgumentParser(description="compute.json → 작업본 기계 자리 교체(5단계) + 레이아웃 판 변환(--layout)")
    ap.add_argument("--layout", action="store_true", help="옛 판(meta 없음)·사슬 위 옛 판(r2026-10-B·C·D)이면 레이아웃 판(config report_layout)까지 사슬 변환한 뒤 값 교체 — 이미 그 판이면 건너뜀(멱등). 5단계는 매 회차 붙인다")
    ap.add_argument("--html", default="work/index.html")
    ap.add_argument("--compute", default="work/compute.json")
    a = ap.parse_args()
    with open(a.html, encoding="utf-8", newline="") as f:
        h = f.read()
    with open(a.compute, encoding="utf-8") as f:
        R = json.load(f)
    try:
        new = apply(h, R, load_config(), layout=a.layout)
    except (ApplyError, KeyError, StopIteration) as e:
        print(f"[FAIL] apply: {type(e).__name__}: {e} — 작업본은 바꾸지 않음({a.html})")
        return 1
    with open(a.html, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    lid = LAYOUT_META.search(new).group(1)
    old = LAYOUT_META.search(h)
    nbr = len(BRANCH.findall(new))

    def steps(frm):  # 사슬로 지난 판 이름(frm 부터 lid 까지)
        out = [frm]
        for a, b, _ in STEPS:
            if out[-1] == a and out[-1] != lid:
                out.append(b)
        return " → ".join(out)
    if not old:
        conv = f" · 레이아웃 판 변환(meta 없음 → {steps(LAYOUT_B['layout_id'])}, details {len(DETAILS.findall(new))} · 분기 {nbr})"
    elif old.group(1) != lid:
        conv = f" · 레이아웃 판 변환({steps(old.group(1))}, 분기 {nbr})"
    else:
        conv = f" · 레이아웃 판 {lid}(변환 건너뜀)"
    mv, ms = re.search(BAL_VALUE, new), re.search(BAL_SUB, new)
    card = (f" · 잔액 카드 {re.sub(r'<[^>]+>', '', mv.group(0))} · {re.sub(r'<[^>]+>', '', ms.group(0))}" if mv and ms else "")   # 판 F — 운영 세션이 출력에서 카드 글을 본다
    print(f"[apply] {a.html} ← {a.compute}  {R['masthead']} · {len(h):,} → {len(new):,}자" + conv + card + (" (변경 없음)" if new == h else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
