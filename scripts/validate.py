#!/usr/bin/env python3
"""
새로필라테스 광고 리포트 배포 전 검증.

사용법:
    python3 validate.py <index.html> <키워드CSV> <검색어CSV> <시간대별CSV> <상세지역CSV>

설정값(제외그룹·CTR 기준·차트 폭 규칙·날짜축 섹션)은 config/report-config.json에서 읽는다.
이 스크립트에 값을 직접 적지 않는다.

확인 항목:
  1. HTML 태그 짝 (div/table/tr/td/th/span/script 등)
  2. KPI 총클릭수 = 07번 정식표 + 클릭1건 목록 + 경쟁사표 합계
  3. 09번 시간대별 클릭 합계 = 키워드 보고서 제외 전 전체 클릭 합계
     (시간대별 보고서는 광고그룹 구분이 없어 OFF 그룹이 포함된 값이다.
      KPI와 비교하면 OFF 그룹에 클릭이 생기는 순간 데이터가 맞아도 FAIL이 난다)
  4. 07번 클릭률 기준 이상 행에만 .ctr-high가 적용됐는지 전수 대조
  5. 01번 표도 같은 규칙으로 전수 대조 (.ctr-high는 표 무관, 클릭률 전용)
  6. masthead 집계 기간 = CSV 일별 min~max·일수
  7. KPI 타일 4개(노출·클릭·클릭률·광고비) = CSV 계산값
  8. 04번 예산 비중 합계 = 100.0%
  9. 날짜축 차트 min-width = 날짜 수 × per_day_px (floor 적용)
     — 대상 섹션은 config chart_min_width.date_based_sections (현재 01·06번).
       섹션마다 검사 1개가 나온다. 설정에 섹션을 더하면 검사도 늘어난다.
 10. 날짜축 차트 x축 라벨 배열('M/D(요일)' 형태) 길이 = 날짜 수
     — 라벨 배열은 하단 스크립트에 있어 섹션 슬라이스 밖이므로 html 전체에서 찾는다.
 11. 섹션 주석 <!-- Section N: --> 1~12 존재
 12. 08·09번 각주의 "N회 차이" = 제외 전 전체 노출 − KPI 노출
 13. 상세지역 CSV 노출 합계 = 제외 전 전체 노출

검사 대상 셀이 0건이면 PASS가 아니라 FAIL이다. 마크업이 바뀌어 정규식이
안 맞는데 조용히 통과하는 것을 막기 위한 것이다.

하나라도 FAIL이면 배포하지 말고 원인을 고친 뒤 다시 실행할 것.
종료 코드: 0=전부 통과, 1=실패 있음
"""

import re
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas가 필요합니다: pip install pandas --break-system-packages")


import json
import os
from datetime import datetime

_CFG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config", "report-config.json")
try:
    with open(_CFG_PATH, encoding="utf-8") as _f:
        CFG = json.load(_f)
except FileNotFoundError:
    sys.exit(f"설정 파일이 없습니다: {_CFG_PATH}\n"
             "스킬 저장소를 통째로 받았는지 확인하세요.")

EXCLUDED_GROUPS = CFG["excluded_groups"]
CTR_HIGH = float(CFG["ctr_high_threshold"])
PER_DAY_PX = int(CFG["chart_min_width"]["per_day_px"])
FLOOR_PX = int(CFG["chart_min_width"]["floor_px"])
DATE_SECTIONS = [int(n) for n in CFG["chart_min_width"]["date_based_sections"]]

TAGS = ["div", "table", "tr", "td", "th", "thead", "tbody",
        "ul", "li", "span", "script", "style"]

results = []


def check(name, passed, detail=""):
    results.append((name, passed, detail))
    mark = "PASS" if passed else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))


def read_csv(path):
    """네이버 보고서는 첫 줄이 기간 헤더."""
    return pd.read_csv(path, skiprows=1)


def check_tags(html):
    bad = []
    for tag in TAGS:
        opened = len(re.findall(rf"<{tag}(?:\s[^>]*)?>", html))
        closed = len(re.findall(rf"</{tag}>", html))
        if opened != closed:
            bad.append(f"{tag} {opened}/{closed}")
    check("HTML 태그 짝", not bad, ", ".join(bad) if bad else "전부 일치")


def section(html, num, next_num):
    """<!-- Section N: ... --> 사이를 잘라낸다."""
    start = html.find(f"<!-- Section {num}:")
    end = html.find(f"<!-- Section {next_num}:")
    if start == -1:
        return ""
    return html[start:end if end != -1 else len(html)]


def parse_main_rows(s7):
    """07번 정식 표의 (검색어, 클릭, ctr적용여부, CTR값)."""
    pat = re.compile(
        r'<td class="name-cell">([^<]+)</td>\s*'
        r'<td><span class="tag[^>]*>[^<]*</span></td>\s*'
        r'<td class="num">([\d,]+)</td>\s*'
        r'<td class="num">(\d+)</td>\s*'
        r'<td class="num([^"]*)">([\d.]+)%</td>'
    )
    out = []
    for m in pat.finditer(s7):
        out.append({
            "kw": m.group(1).strip(),
            "clicks": int(m.group(3)),
            "has_hl": "ctr-high" in m.group(4),
            "ctr": float(m.group(5)),
        })
    return out


def parse_ctr_cells(sec):
    """섹션 안의 클릭률 셀 (강조여부, 값). <td class="num...">X%</td> 형태만."""
    pat = re.compile(r'<td class="num([^"]*)">([\d.]+)%</td>')
    return [{"has_hl": "ctr-high" in m.group(1), "ctr": float(m.group(2))}
            for m in pat.finditer(sec)]


def check_ctr_rule(label, cells):
    """클릭률 CTR_HIGH 이상에만 .ctr-high. 셀 0건이면 마크업 변경으로 보고 FAIL."""
    if not cells:
        check(label, False, "검사 대상 셀 0건 — 마크업이 바뀌어 정규식이 안 맞을 수 있음")
        return
    bad = [f"{c['ctr']}%(강조={'있음' if c['has_hl'] else '없음'})"
           for c in cells if c["has_hl"] != (c["ctr"] >= CTR_HIGH)]
    check(label, not bad,
          f"{len(cells)}행 검사, 불일치 {len(bad)}건"
          + (f": {', '.join(bad)}" if bad else ""))


def count_click1(s7):
    """클릭 1건 컴팩트 목록의 항목 수 = 클릭 수."""
    i = s7.find("클릭 1건 검색어")
    if i == -1:
        return 0
    seg = s7[i:]
    m = re.search(r'line-height:1\.9;">(.*?)</div>', seg, re.S)
    if not m:
        return 0
    text = m.group(1).strip()
    return len([x for x in text.split("·") if x.strip()])


def sum_competitor(s7):
    i = s7.find("경쟁사 브랜드명")
    if i == -1:
        return 0
    seg = s7[i:]
    pat = re.compile(
        r'<td class="name-cell">.*?</td>\s*<td>[^<]*</td>\s*'
        r'<td><span class="tag[^>]*>[^<]*</span></td>\s*'
        r'<td class="num">\d+</td>\s*<td class="num">(\d+)</td>',
        re.S)
    return sum(int(m.group(1)) for m in pat.finditer(seg))


def parse_days(kw):
    """키워드 보고서의 일별 컬럼에서 (min, max, 일수)."""
    d = pd.to_datetime(kw["일별"].astype(str).str.rstrip("."), format="%Y.%m.%d")
    return d.min(), d.max(), (d.max() - d.min()).days + 1


def check_masthead(html, dmin, dmax, ndays):
    m = re.search(r"집계 기간<b>([^<]+)</b>", html)
    if not m:
        check("masthead 집계 기간", False, "문구를 못 찾음 — 마크업 변경 의심")
        return
    got = m.group(1).strip()
    want = f"{dmin.strftime('%Y.%m.%d')} — {dmax.strftime('%m.%d')} ({ndays}일)"
    check("masthead 집계 기간", got == want, f"화면 `{got}` vs CSV `{want}`")


def parse_kpi_tiles(html):
    """KPI 타일의 (라벨, 값 문자열)."""
    pat = re.compile(r'<div class="label">([^<]+)</div>\s*'
                     r'<div class="value">([^<]+)<span class="unit">')
    return {m.group(1).strip(): m.group(2).strip() for m in pat.finditer(html)}


def check_kpi_tiles(html, imp, clicks, cost):
    tiles = parse_kpi_tiles(html)
    if not tiles:
        check("KPI 타일 값", False, "타일을 못 찾음 — 마크업 변경 의심")
        return
    ctr = round(clicks / imp * 100, 2) if imp else 0
    want = {"총 노출수": f"{imp:,}", "총 클릭수": f"{clicks:,}",
            "총 광고비": f"{cost:,}", "평균 클릭률": f"{ctr:g}"}
    bad = [f"{k}: 화면 {tiles.get(k, '없음')} vs CSV {v}"
           for k, v in want.items() if tiles.get(k) != v]
    check("KPI 타일 4개 = CSV", not bad,
          f"{len(want)}개 검사, 불일치 {len(bad)}건" + (f": {'; '.join(bad)}" if bad else ""))


def check_budget_share(html):
    s4 = section(html, 4, 5)
    rows = re.findall(r"<tr>(.*?)</tr>", s4, re.S)
    shares = []
    for r in rows:
        cells = re.findall(r'<td class="num[^"]*">([^<]+)</td>', r)
        if len(cells) >= 7 and cells[5].endswith("%"):
            shares.append(float(cells[5].rstrip("%")))
    if not shares:
        check("04번 예산 비중 합계", False, "비중 셀 0건 — 마크업 변경 의심")
        return
    total = round(sum(shares), 1)
    check("04번 예산 비중 합계 = 100.0%", abs(total - 100.0) < 0.05,
          f"{len(shares)}행 합계 {total}% ({' + '.join(str(x) for x in shares)})")


def check_chart_width(html, ndays):
    """config date_based_sections에 적힌 섹션마다 min-width = max(일수×per_day_px, floor)."""
    want = max(ndays * PER_DAY_PX, FLOOR_PX)
    for num in DATE_SECTIONS:
        label = f"{num:02d}번 차트 min-width"
        sec = section(html, num, num + 1)
        widths = [int(x) for x in re.findall(r"min-width:\s*(\d+)px", sec)]
        if not widths:
            check(label, False, "min-width 0건 — 섹션 주석 또는 마크업 변경 의심")
            continue
        check(f"{label} = 날짜수x{PER_DAY_PX}px",
              want in widths, f"화면 {widths} / 기대 {want}px ({ndays}일)")


def check_date_labels(html, ndays):
    """'M/D(요일)' 형태로만 이루어진 labels:[...] 배열은 전부 날짜축이다. 길이 = 일수."""
    found = []
    for m in re.finditer(r"labels\s*:\s*\[([^\]]*)\]", html):
        items = [x.strip() for x in m.group(1).split(",") if x.strip()]
        if items and all(re.fullmatch(r"'\d+/\d+\(.\)'", x) for x in items):
            found.append(len(items))
    if not found:
        check("날짜축 x축 라벨 개수", False, "날짜형 라벨 배열 0건 — 스크립트 마크업 변경 의심")
        return
    bad = [n for n in found if n != ndays]
    check("날짜축 x축 라벨 개수 = 날짜수", not bad,
          f"배열 {len(found)}개 {found} / 기대 {ndays}개")


def check_section_comments(html):
    missing = [n for n in range(1, 13) if f"<!-- Section {n}:" not in html]
    check("섹션 주석 1~12 존재", not missing,
          "전부 있음" if not missing else f"누락 {missing}")


def check_diff_footnotes(html, all_imp, kpi_imp, rg_imp):
    diff = all_imp - kpi_imp
    notes = re.findall(r"노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이", html)
    if not notes:
        check("08·09번 각주 N회 차이", False, "각주 0건 — 마크업 변경 의심")
    else:
        bad = [f"각주 {a}/{b}/{c}회" for a, b, c in notes
               if int(a.replace(",", "")) != all_imp
               or int(b.replace(",", "")) != kpi_imp
               or int(c) != diff]
        check("08·09번 각주 N회 차이", not bad,
              f"각주 {len(notes)}곳 검사, 불일치 {len(bad)}건"
              + (f": {'; '.join(bad)}" if bad else f" (전체 {all_imp:,} / KPI {kpi_imp:,} / 차이 {diff})"))
    check("상세지역 CSV 노출 합계 = 제외 전 전체", rg_imp == all_imp,
          f"상세지역 CSV {rg_imp:,} vs 제외 전 전체 {all_imp:,}")


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__)

    html_path, kw_path, sr_path, hr_path, rg_path = sys.argv[1:6]
    html = open(html_path, encoding="utf-8").read()

    # --- 1. 태그 짝 ---
    check_tags(html)

    # --- 기준값: 제외 그룹을 뺀 키워드 보고서 ---
    kw = read_csv(kw_path)
    kw_inc = kw[~kw["광고그룹"].isin(EXCLUDED_GROUPS)]
    kpi_clicks = int(kw_inc["클릭수"].sum())
    kpi_imp = int(kw_inc["노출수"].sum())
    kpi_cost = int(kw_inc["총비용"].sum())
    all_clicks = int(kw["클릭수"].sum())      # 제외 전 전체 (08·09번 기준)
    all_imp = int(kw["노출수"].sum())
    print(f"\n기준 KPI — 노출 {kpi_imp:,} / 클릭 {kpi_clicks} / 광고비 {kpi_cost:,}원")
    print(f"제외 전 전체 — 노출 {all_imp:,} / 클릭 {all_clicks} "
          f"(08·09번 각주 차이: 노출 {all_imp - kpi_imp}회 / 클릭 {all_clicks - kpi_clicks}회)\n")

    # --- 2. 07번 클릭수 검산 ---
    s7 = section(html, 7, 8)
    rows = parse_main_rows(s7)
    main_clicks = sum(r["clicks"] for r in rows)
    one_clicks = count_click1(s7)
    comp_clicks = sum_competitor(s7)
    total = main_clicks + one_clicks + comp_clicks
    check(
        "07번 클릭수 합계 = KPI",
        total == kpi_clicks,
        f"정식표 {main_clicks} + 클릭1건 {one_clicks} + 경쟁사 {comp_clicks} "
        f"= {total} (KPI {kpi_clicks})",
    )

    # --- 3. 시간대별 클릭 합계 ---
    hr = read_csv(hr_path)
    hourly_clicks = int(hr["클릭수"].sum())
    # KPI가 아니라 제외 전 전체와 비교한다. 시간대별 보고서에는 광고그룹 구분이
    # 없어 OFF 그룹 클릭이 포함되기 때문(SKILL.md "집계 기준" 참고).
    check(
        "09번 시간대별 클릭 합계 = 키워드 보고서 전체 클릭",
        hourly_clicks == all_clicks,
        f"시간대별 CSV {hourly_clicks} vs 전체 {all_clicks} (KPI {kpi_clicks})",
    )

    # --- 4. CTR 강조 규칙 (07번) ---
    if not rows:
        check(f"07번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high", False,
              "정식표 행 0건 — 마크업이 바뀌어 정규식이 안 맞을 수 있음")
    else:
        mismatched = [
            f"{r['kw']}({r['ctr']}%, 강조={'있음' if r['has_hl'] else '없음'})"
            for r in rows
            if r["has_hl"] != (r["ctr"] >= CTR_HIGH)
        ]
        check(
            f"07번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high",
            not mismatched,
            f"{len(rows)}행 검사, 불일치 {len(mismatched)}건"
            + (f": {', '.join(mismatched)}" if mismatched else ""),
        )

    # --- 5. CTR 강조 규칙 (01번) ---
    # .ctr-high는 07번 전용이 아니다. 01번 일별 표에도 같은 기준으로 적용된다.
    check_ctr_rule(f"01번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high",
                   parse_ctr_cells(section(html, 1, 2)))

    # --- 6~11. 확장 검사 ---
    dmin, dmax, ndays = parse_days(kw)
    check_masthead(html, dmin, dmax, ndays)
    check_kpi_tiles(html, kpi_imp, kpi_clicks, kpi_cost)
    check_budget_share(html)
    check_chart_width(html, ndays)
    check_date_labels(html, ndays)
    check_section_comments(html)
    rg = read_csv(rg_path)
    check_diff_footnotes(html, all_imp, kpi_imp, int(rg["노출수"].sum()))

    # --- 참고: 검색어 CSV와 대조 (누락 탐지) ---
    sr = read_csv(sr_path)
    sr_clicks = int(sr["클릭수"].sum())
    if sr_clicks != kpi_clicks:
        print(f"\n참고: 검색어 CSV 클릭 합계 {sr_clicks} — KPI {kpi_clicks}와 다르면 "
              "검색어 보고서 기간이 다를 수 있으니 확인 필요")

    failed = [n for n, ok, _ in results if not ok]
    print("\n" + "=" * 50)
    if failed:
        print(f"실패 {len(failed)}건: {', '.join(failed)}")
        print("배포하지 말고 원인을 고친 뒤 다시 실행할 것.")
        return 1
    print("전부 통과. 배포 진행 가능.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
