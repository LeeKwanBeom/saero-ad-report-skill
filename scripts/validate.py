#!/usr/bin/env python3
"""
새로필라테스 광고 리포트 배포 전 검증.

사용법:
    python3 validate.py <index.html> <키워드CSV> <검색어CSV> <시간대별CSV>

확인 항목:
  1. HTML 태그 짝 (div/table/tr/td/th/span/script 등)
  2. KPI 총클릭수 = 07번 정식표 + 클릭1건 목록 + 경쟁사표 합계
  3. 09번 시간대별 클릭 합계도 KPI와 일치하는지
  4. 07번 클릭률 4% 이상 행에만 .ctr-high가 적용됐는지 전수 대조

하나라도 FAIL이면 배포하지 말고 원인을 고친 뒤 다시 실행할 것.
종료 코드: 0=전부 통과, 1=실패 있음
"""

import re
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas가 필요합니다: pip install pandas --break-system-packages")


# 이미 확인된 제외 그룹. 새 그룹이 생기면 SKILL.md의 판정 규칙에 따라
# 사용자에게 확인한 뒤 여기에 추가할 것.
EXCLUDED_GROUPS = ["노원필라테스(삭제)"]

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


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)

    html_path, kw_path, sr_path, hr_path = sys.argv[1:5]
    html = open(html_path, encoding="utf-8").read()

    # --- 1. 태그 짝 ---
    check_tags(html)

    # --- 기준값: 제외 그룹을 뺀 키워드 보고서 ---
    kw = read_csv(kw_path)
    kw_inc = kw[~kw["광고그룹"].isin(EXCLUDED_GROUPS)]
    kpi_clicks = int(kw_inc["클릭수"].sum())
    kpi_imp = int(kw_inc["노출수"].sum())
    kpi_cost = int(kw_inc["총비용"].sum())
    print(f"\n기준 KPI — 노출 {kpi_imp:,} / 클릭 {kpi_clicks} / 광고비 {kpi_cost:,}원\n")

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
    check(
        "09번 시간대별 클릭 합계 = KPI",
        hourly_clicks == kpi_clicks,
        f"시간대별 CSV {hourly_clicks} vs KPI {kpi_clicks}",
    )

    # --- 4. CTR 강조 규칙 ---
    mismatched = [
        f"{r['kw']}({r['ctr']}%, 강조={'있음' if r['has_hl'] else '없음'})"
        for r in rows
        if r["has_hl"] != (r["ctr"] >= 4.0)
    ]
    check(
        "07번 클릭률 4% 이상에만 .ctr-high",
        not mismatched,
        f"{len(rows)}행 검사, 불일치 {len(mismatched)}건"
        + (f": {', '.join(mismatched)}" if mismatched else ""),
    )

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
