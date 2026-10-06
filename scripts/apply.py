#!/usr/bin/env python3
"""compute.json → 작업본 index.html 의 기계 자리 교체(5단계, E2 — 2026-10-06 저장소화).

사용법: "$PY" scripts/apply.py [--html work/index.html] [--compute work/compute.json]

- 바꾸는 자리(현행 전부): masthead · og:description · KPI 4 + sub 3 · 차트 min-width 2(01·06) · 차트 배열·라벨(01·02·05·06·09·10) ·
  02 도넛 제목 총액 · 01 표 5행·순위 5칸 · 03 표 전체(오름차순 + 합계 행) · 04 표(앞 2칸 = 직전 행) · 06 매칭표 2행·카드 일차·큰 숫자 ·
  07 정식표 · 07 클릭 1건·클릭 0 목록(동률은 직전 순서) · 07 경쟁사표(소재구·매칭 = 직전 행, 신규 변형 = config `competitor_defaults`) ·
  08 TOP 10 · 08 TOP 10 밖 목록(동률은 직전 순서)·개수 줄 · 10 표 4행.
- 서술(문장)은 바꾸지 않는다 — 그 회차의 n<날짜>.py(저장소 밖 스크래치)가 서술 표지 `<!-- n:<자리>:<매회차|고정> -->` 안을 바꾼다
  (references/report-structure.md "서술 표지").
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


def tbody(s, after, rows_html):
    """앵커 뒤 첫 <tbody> 안을 통째로 바꾼다. (새 문자열, 옛 tbody 안) 를 돌려준다."""
    i = find1(s, after)
    a = find1(s, "<tbody>", i) + len("<tbody>")
    b = find1(s, "</tbody>", a)
    return s[:a] + "\n" + rows_html + s[b:], s[a:b]


def trs(block):
    return re.findall(r"<tr[^>]*>.*?</tr>", block, re.S)


def td(v, cls="num"):
    return f'            <td class="{cls}">{v}</td>'


def tr(cells, style=""):
    return "          <tr" + style + ">\n" + "\n".join(cells) + "\n          </tr>"


def apply(h, R, cfg):
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

    # 03 — 오름차순 + 합계 행(굵게). 순서·합계 위치는 회차 2(모양)에서 바뀐다
    def p3(v):
        return [td(f"{c(v[0])}원"), td(v[1]), td("–" if v[2] is None else f"{c(v[2])}원")]
    rows = [tr([td(r["날짜"], "name-cell")] + p3(r["플레이스"]) + p3(r["파워링크"]) + [td(f"{c(r['합계'])}원")]) for r in R["03"]["rows"]]
    T = R["03"]["합계"]
    rows.append(tr([td("합계", "name-cell")] + p3(T["플레이스"]) + p3(T["파워링크"]) + [td(f"{c(T['총'])}원")], ' style="font-weight:800;"'))
    h, _ = tbody(h, "<!-- Section 3", "\n".join(rows) + "\n        ")

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
    ap = argparse.ArgumentParser(description="compute.json → 작업본 기계 자리 교체(5단계)")
    ap.add_argument("--html", default="work/index.html")
    ap.add_argument("--compute", default="work/compute.json")
    a = ap.parse_args()
    with open(a.html, encoding="utf-8", newline="") as f:
        h = f.read()
    with open(a.compute, encoding="utf-8") as f:
        R = json.load(f)
    try:
        new = apply(h, R, load_config())
    except (ApplyError, KeyError, StopIteration) as e:
        print(f"[FAIL] apply: {type(e).__name__}: {e} — 작업본은 바꾸지 않음({a.html})")
        return 1
    with open(a.html, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print(f"[apply] {a.html} ← {a.compute}  {R['masthead']} · {len(h):,} → {len(new):,}자" + (" (변경 없음)" if new == h else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
