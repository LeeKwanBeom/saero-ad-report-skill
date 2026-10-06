#!/usr/bin/env python3
"""compute.json → 작업본 index.html 의 기계 자리 교체(5단계, E2 — 2026-10-06 저장소화) + 레이아웃 판 변환(2026-10-06 회차 2).

사용법: "$PY" scripts/apply.py --layout [--html work/index.html] [--compute work/compute.json]

- 레이아웃 판(config `report_layout`, references/report-structure.md "레이아웃 판 r2026-10-B"):
  · `<meta name="report-layout" content="…">` 가 config `layout_id` 와 같으면 그 판(B 접기형)으로 값만 바꾼다 — `--layout` 이 있어도 변환은 건너뜀(멱등).
  · meta 가 없는 옛 판은 `--layout` 일 때만 변환(meta + `<details class="fold">` 5개 뼈대 + 접기 CSS·스크립트) 뒤 값을 바꾼다.
    `--layout` 없이 옛 판이면 `[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout …` (옛 배치로 쓰지 않는다). meta 가 다른 값이면 FAIL(판 변경은 설계 회차 몫).
- 바꾸는 자리(매 회차 — 변환을 건너뛴 회차에도): masthead · og:description · KPI 4 + sub 3 · 차트 min-width 2(01·06) · 차트 배열·라벨(01·02·05·06·09·10) ·
  02 도넛 제목 총액 · 01 표 5행·순위 5칸(오름차순 그대로) · 03 두 표(위 = 합계 + 최근 `recent_days`일 최신 위 · 접힌 표 = 나머지 날짜 최신 위) ·
  04 표(앞 2칸 = 직전 행) · 06 매칭표 2행·카드 일차·큰 숫자 · 07 정식표 · 07 클릭 1건·클릭 0 목록(동률은 직전 순서) ·
  07 경쟁사표(소재구·매칭 = 직전 행, 신규 변형 = config `competitor_defaults`) · 08 TOP 10 · 08 TOP 10 밖 목록(동률은 직전 순서)·개수 줄 · 10 표 4행 ·
  **summary 의 개수·날짜 전부**(03 "이전 N일(M/D~M/D)" · 07 클릭 1건·클릭 0 "(N개 · 펼치기)" · 경쟁사표 "표 N행" · 08 "(N개 지역·클릭 M건)") — 막음 M2.
- 서술(문장)은 바꾸지 않는다 — 그 회차의 n<날짜>.py(저장소 밖 스크래치)가 서술 표지 `<!-- n:<자리>:<매회차|고정> -->` 안을 바꾼다
  (references/report-structure.md "서술 표지"). 변환·값 교체 모두 표지 안쪽 바이트를 건드리지 않는다. summary·details 는 apply 몫.
- 앵커는 전부 "정확히 하나"를 요구한다. 못 찾거나 둘 이상이면 `[FAIL] apply: …` exit 1 — 파일은 끝에 한 번만 쓰므로 실패하면 작업본은 그대로다.
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

FOLD_CSS = """  /* 접기(레이아웃 판 r2026-10-B, 2026-10-06) — details.fold(태그 이름을 꺾쇠로 쓰지 말 것: validate 태그 짝이 셈): 03 이전 날짜 · 07 클릭 1건·클릭 0 목록 · 07 경쟁사표 · 08 TOP 10 밖.
     기본 닫힘. 펼치면 아래 스크립트가 가로 스크롤 안내를 다시 맞추고, 인쇄할 때는 전부 펼쳤다가 되돌린다(css-and-layout.md "접기 안내") */
  .fold > summary{cursor:pointer;}
  .fold-more{font-size:12px;font-weight:700;color:var(--mint-dark);}
  .fold[open] > .fold-more{margin-bottom:8px;}
"""
RESIZE = "  window.addEventListener('resize', function(){ clearTimeout(t); t = setTimeout(sync, 200); });\n"
FOLD_JS = """  // 접기(details — 레이아웃 판 r2026-10-B): 펼칠 때 안쪽 표의 안내·페이드를 다시 맞추고, 인쇄할 때는 닫힌 것을 전부 펼쳤다가 원래대로
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


def trs(block):
    return re.findall(r"<tr[^>]*>.*?</tr>", block, re.S)


def td(v, cls="num"):
    return f'            <td class="{cls}">{v}</td>'


def tr(cells, style=""):
    return "          <tr" + style + ">\n" + "\n".join(cells) + "\n          </tr>"


def apply(h, R, cfg, layout=False):
    """layout = --layout(meta 없는 옛 판이면 변환). meta = config layout_id 면 변환 없이 값만(멱등)."""
    lay = cfg["report_layout"]
    lid, k = lay["layout_id"], int(lay["recent_days"])
    if k < 1:
        raise ApplyError(f"config report_layout.recent_days {k} — 1 이상이어야 함")
    metas = LAYOUT_META.findall(h)
    if len(metas) > 1:
        raise ApplyError(f'<meta name="report-layout"> 가 {len(metas)}개')
    if not metas:
        if not layout:
            raise ApplyError(f"레이아웃 판 meta 없음 — --layout 을 붙여 다시(옛 모양 → {lid} 변환 + 값 교체)")
        h = convert_layout(h, lay)
    elif metas[0] != lid:
        raise ApplyError(f"레이아웃 판 meta {metas[0]!r} ≠ config {lid!r} — 이 판에서 바꾸는 변환은 없음(판 변경은 설계 회차·사용자 결정)")
    elif len(DETAILS.findall(h)) != int(lay["markers"]["details"]):
        raise ApplyError(f"레이아웃 판 {lid} 인데 details {len(DETAILS.findall(h))}개 ≠ config {lay['markers']['details']} — 접기를 손으로 바꾼 판으로 보임")
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
    ap.add_argument("--layout", action="store_true", help="meta 없는 옛 판이면 레이아웃 판(config report_layout)으로 변환한 뒤 값 교체 — 이미 그 판이면 건너뜀(멱등). 5단계는 매 회차 붙인다")
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
    print(f"[apply] {a.html} ← {a.compute}  {R['masthead']} · {len(h):,} → {len(new):,}자"
          + (f" · 레이아웃 판 변환(meta 없음 → {lid}, details {len(DETAILS.findall(new))})" if not LAYOUT_META.search(h) else f" · 레이아웃 판 {lid}(변환 건너뜀)")
          + (" (변경 없음)" if new == h else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
