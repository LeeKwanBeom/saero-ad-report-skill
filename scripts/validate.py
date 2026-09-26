#!/usr/bin/env python3
"""
새로필라테스 광고 리포트 배포 전 검증 — **compute.py와 독립된 검산**.

사용법:
    python3 validate.py <index.html> <키워드CSV> <검색어CSV> <시간대별CSV> <상세지역CSV>

설정값(제외그룹·CTR 기준·차트 폭 규칙·날짜축 섹션·경쟁사 목록)은 config/report-config.json에서 읽는다.
이 스크립트에 값을 직접 적지 않는다. reportlib.py와 공유하는 것은 읽기·제외그룹 필터·일수·섹션 자르기까지다 —
KPI 합·순위·정렬 같은 값 계산은 compute.py와 공유하지 않는다(같은 오류를 두 번 통과시키지 않기 위해, 2026-09-26).

확인 항목(출력의 [PASS]/[FAIL] 줄을 세어 개수를 확인한다 — 설정에 따라 늘고 준다):
  1. HTML 태그 짝 (div/table/tr/td/th/span/script 등)
  2. KPI 총클릭수 = 07번 정식표 + 클릭1건 목록 + 경쟁사표 합계
  3. 09번 시간대별 클릭 합계 = 키워드 보고서 제외 전 전체 클릭 합계
     (시간대별 보고서는 광고그룹 구분이 없어 OFF 그룹이 포함된 값이다)
  4. 07번 클릭률 기준 이상 행에만 .ctr-high가 적용됐는지 전수 대조
  5. 01번 표도 같은 규칙으로 전수 대조 (.ctr-high는 표 무관, 클릭률 전용)
  6. masthead 집계 기간 = CSV 일별 min~max·일수
  7. KPI 타일 4개(노출·클릭·클릭률·광고비) = CSV 계산값
  8. 04번 예산 비중 합계 = 100.0%
  9. 날짜축 차트 min-width = 날짜 수 × per_day_px (floor 적용)
     — 대상 섹션은 config chart_min_width.date_based_sections (현재 01·06번). 섹션마다 검사 1개.
 10. 날짜축 차트 x축 라벨 배열('M/D(요일)' 형태) 길이 = 날짜 수
 11. 섹션 주석 <!-- Section N: --> 1~12 존재
 12. 08·09번 각주의 "N회 차이" = 제외 전 전체 노출 − KPI 노출
 13. 상세지역 CSV 노출 합계 = 제외 전 전체 노출
 14. (2026-09-26 추가) 05번 mediaChart top5 = 키워드 CSV `매체이름` 노출 상위 5 — 라벨·값·순서·색(플레이스=mint/파워링크=ink)
 15. (2026-09-26 추가) 06번 신규 키워드 카드 큰 숫자 = 04번 같은 그룹의 평균순위 셀
 16. (2026-09-26 추가) config `competitors` 이름을 포함하는 검색어(검색어 CSV)가 07번 경쟁사표 밖에 없는지 — 순방향만.
     표 안 이름이 config에 있는지(역방향)는 검사하지 않는다(어순이 다른 표기 변형이 있음)
 17. (2026-09-26 추가) 07번 경쟁사표 각 행의 노출·클릭 = 검색어 CSV 합계
 18. (2026-09-26 추가) 검색어 CSV 클릭 합계 = KPI 클릭 (종전 `참고` 출력을 FAIL로)
 19. (2026-09-26 추가) 11번 항목 수 ≤ 8 + (참고) ≤ 2, 판정 줄 "유지+뒤집힘+근거 소멸 = 직전 항목 수"
 20. (2026-09-26 추가) 11·12번 본문(<script> 앞까지) 금칙어(필요·시점·할 것·검토·주째) 0건 — 조치 문장은 12번 몫
 21. (2026-09-26 추가, 09-27 범위 확장) 07번 각주(`class="note"`)·11·12번 본문(<script> 앞까지)의 잔존 문구
     (확인 요청·판단 요청·기다림·확인 중·대기) 0건. 잔존 문구 검사는 이 검사 하나뿐이다(compare.py에는 없음 — --pending 일원화).
     사용자 답을 기다리며 배포하는 회차(4c08ab3처럼 채팅 질문을 남긴 배포)는 `--pending`을 붙여 이 검사만 허용한다
     (건수는 그대로 출력). 답을 반영한 재배포에는 붙이지 않는다 — 기본은 엄격. 세 범위 중 하나라도 못 찾으면 0건 가드 FAIL.

사용법(옵션): python3 validate.py ... [--pending]

검사 대상 셀이 0건이면 PASS가 아니라 FAIL이다. 마크업이 바뀌어 정규식이
안 맞는데 조용히 통과하는 것을 막기 위한 것이다.

하나라도 FAIL이면 배포하지 말고 원인을 고친 뒤 다시 실행할 것.
종료 코드: 0=전부 통과, 1=실패 있음
"""

import re
import sys

try:
    import pandas as pd  # noqa: F401  (reportlib이 필요로 함)
except ImportError:
    sys.exit("pandas가 필요합니다: pip install pandas --break-system-packages")

from reportlib import exclude_groups, load_config, parse_days, read_csv, read_html, section

CFG = load_config()
EXCLUDED_GROUPS = CFG["excluded_groups"]
CTR_HIGH = float(CFG["ctr_high_threshold"])
PER_DAY_PX = int(CFG["chart_min_width"]["per_day_px"])
FLOOR_PX = int(CFG["chart_min_width"]["floor_px"])
DATE_SECTIONS = [int(n) for n in CFG["chart_min_width"]["date_based_sections"]]
COMPETITORS = list(CFG["competitors"])
FORBIDDEN = ["필요", "시점", "할 것", "검토", "주째"]          # report-structure.md 11번 수동 검사
RESIDUAL = ["확인 요청", "판단 요청", "기다림", "확인 중", "대기"]  # 채팅 후속 뒤 남기면 안 되는 문구

TAGS = ["div", "table", "tr", "td", "th", "thead", "tbody",
        "ul", "li", "span", "script", "style"]

results = []


def check(name, passed, detail=""):
    results.append((name, passed, detail))
    mark = "PASS" if passed else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))


def check_tags(html):
    bad = []
    for tag in TAGS:
        opened = len(re.findall(rf"<{tag}(?:\s[^>]*)?>", html))
        closed = len(re.findall(rf"</{tag}>", html))
        if opened != closed:
            bad.append(f"{tag} {opened}/{closed}")
    check("HTML 태그 짝", not bad, ", ".join(bad) if bad else "전부 일치")


def parse_main_rows(s7):
    """07번 정식 표의 (검색어, 클릭, ctr적용여부, CTR값)."""
    pat = re.compile(
        r'<td class="name-cell">([^<]+)</td>\s*'
        r'<td><span class="tag[^>]*>[^<]*</span></td>\s*'
        r'<td class="num">([\d,]+)</td>\s*'
        r'<td class="num">(\d+)</td>\s*'
        r'<td class="num([^"]*)">([\d.]+)%</td>'
    )
    return [{"kw": m.group(1).strip(), "clicks": int(m.group(3)), "has_hl": "ctr-high" in m.group(4), "ctr": float(m.group(5))}
            for m in pat.finditer(s7)]


def parse_ctr_cells(sec):
    """섹션 안의 클릭률 셀 (강조여부, 값). <td class="num...">X%</td> 형태만."""
    pat = re.compile(r'<td class="num([^"]*)">([\d.]+)%</td>')
    return [{"has_hl": "ctr-high" in m.group(1), "ctr": float(m.group(2))} for m in pat.finditer(sec)]


def check_ctr_rule(label, cells):
    """클릭률 CTR_HIGH 이상에만 .ctr-high. 셀 0건이면 마크업 변경으로 보고 FAIL."""
    if not cells:
        check(label, False, "검사 대상 셀 0건 — 마크업이 바뀌어 정규식이 안 맞을 수 있음")
        return
    bad = [f"{c['ctr']}%(강조={'있음' if c['has_hl'] else '없음'})"
           for c in cells if c["has_hl"] != (c["ctr"] >= CTR_HIGH)]
    check(label, not bad, f"{len(cells)}행 검사, 불일치 {len(bad)}건" + (f": {', '.join(bad)}" if bad else ""))


def click1_items(s7):
    """클릭 1건 컴팩트 목록의 항목 문자열들."""
    i = s7.find("클릭 1건 검색어")
    if i == -1:
        return []
    m = re.search(r'line-height:1\.9;">(.*?)</div>', s7[i:], re.S)
    return [x.strip() for x in m.group(1).split("·") if x.strip()] if m else []


def click0_items(s7):
    i = s7.find("노출은 있으나 클릭 0건인")
    if i == -1:
        return []
    m = re.search(r'line-height:1\.9;">(.*?)</div>', s7[i:], re.S)
    return [x.strip() for x in m.group(1).split("·") if x.strip()] if m else []


def competitor_rows(s7):
    """경쟁사표 (검색어, 노출, 클릭)."""
    i = s7.find("경쟁사 브랜드명")
    if i == -1:
        return []
    pat = re.compile(
        r'<td class="name-cell">([^<]+)</td>\s*<td>[^<]*</td>\s*'
        r'<td><span class="tag[^>]*>[^<]*</span></td>\s*'
        r'<td class="num">(\d+)</td>\s*<td class="num">(\d+)</td>', re.S)
    return [(m.group(1).strip(), int(m.group(2)), int(m.group(3))) for m in pat.finditer(s7[i:])]


def check_masthead(html, dmin, dmax, ndays):
    m = re.search(r"집계 기간<b>([^<]+)</b>", html)
    if not m:
        check("masthead 집계 기간", False, "문구를 못 찾음 — 마크업 변경 의심")
        return
    got = m.group(1).strip()
    want = f"{dmin.strftime('%Y.%m.%d')} — {dmax.strftime('%m.%d')} ({ndays}일)"
    check("masthead 집계 기간", got == want, f"화면 `{got}` vs CSV `{want}`")


def parse_kpi_tiles(html):
    pat = re.compile(r'<div class="label">([^<]+)</div>\s*<div class="value">([^<]+)<span class="unit">')
    return {m.group(1).strip(): m.group(2).strip() for m in pat.finditer(html)}


def check_kpi_tiles(html, imp, clicks, cost):
    tiles = parse_kpi_tiles(html)
    if not tiles:
        check("KPI 타일 값", False, "타일을 못 찾음 — 마크업 변경 의심")
        return
    ctr = round(clicks / imp * 100, 2) if imp else 0
    want = {"총 노출수": f"{imp:,}", "총 클릭수": f"{clicks:,}", "총 광고비": f"{cost:,}", "평균 클릭률": f"{ctr:g}"}
    bad = [f"{k}: 화면 {tiles.get(k, '없음')} vs CSV {v}" for k, v in want.items() if tiles.get(k) != v]
    check("KPI 타일 4개 = CSV", not bad, f"{len(want)}개 검사, 불일치 {len(bad)}건" + (f": {'; '.join(bad)}" if bad else ""))


def parse_04_rows(html):
    """04번 표 (그룹명, 예산 비중 문자열, 평균순위 문자열)."""
    s4 = section(html, 4)
    out = []
    for r in re.findall(r"<tr>(.*?)</tr>", s4, re.S):
        cells = re.findall(r'<td class="num[^"]*">([^<]+)</td>', r)
        name = re.search(r'<td class="name-cell">([^<]+?)(?:\s*<span|</td>)', r)
        if len(cells) >= 7 and cells[5].endswith("%"):
            out.append((name.group(1).strip() if name else "", cells[5], cells[6]))
    return out


def check_budget_share(rows4):
    shares = [float(c.rstrip("%")) for _, c, _ in rows4]
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
        sec = section(html, num)
        widths = [int(x) for x in re.findall(r"min-width:\s*(\d+)px", sec)]
        if not widths:
            check(label, False, "min-width 0건 — 섹션 주석 또는 마크업 변경 의심")
            continue
        check(f"{label} = 날짜수x{PER_DAY_PX}px", want in widths, f"화면 {widths} / 기대 {want}px ({ndays}일)")


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
    check("날짜축 x축 라벨 개수 = 날짜수", not bad, f"배열 {len(found)}개 {found} / 기대 {ndays}개")


def check_section_comments(html):
    missing = [n for n in range(1, 13) if f"<!-- Section {n}:" not in html]
    check("섹션 주석 1~12 존재", not missing, "전부 있음" if not missing else f"누락 {missing}")


def check_diff_footnotes(html, all_imp, kpi_imp, rg_imp):
    diff = all_imp - kpi_imp
    notes = re.findall(r"노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이", html)
    if not notes:
        check("08·09번 각주 N회 차이", False, "각주 0건 — 마크업 변경 의심")
    else:
        bad = [f"각주 {a}/{b}/{c}회" for a, b, c in notes
               if int(a.replace(",", "")) != all_imp or int(b.replace(",", "")) != kpi_imp or int(c) != diff]
        check("08·09번 각주 N회 차이", not bad,
              f"각주 {len(notes)}곳 검사, 불일치 {len(bad)}건" + (f": {'; '.join(bad)}" if bad else f" (전체 {all_imp:,} / KPI {kpi_imp:,} / 차이 {diff})"))
    check("상세지역 CSV 노출 합계 = 제외 전 전체", rg_imp == all_imp, f"상세지역 CSV {rg_imp:,} vs 제외 전 전체 {all_imp:,}")


def check_media_top5(html, kw_inc):
    """14. 05번 mediaChart 라벨·값·순서·색 = 키워드 CSV 매체이름 노출 상위 5."""
    i = html.find("getElementById('mediaChart')")
    blk = html[i:i + 3000] if i != -1 else ""
    lab = re.search(r"labels:\s*\[(.*?)\],\n", blk, re.S)
    dat = re.search(r"label:\s*'노출수'[^\n]*\n\s*data:\s*\[([^\]]*)\]", blk)
    col = re.search(r"backgroundColor:\s*\[([^\]]*)\]", blk)
    if not (lab and dat and col):
        check("05번 mediaChart top5 = CSV 매체 상위 5", False, "mediaChart 라벨/데이터/색 배열을 못 찾음 — 스크립트 마크업 변경 의심")
        return
    labels = [re.sub(r"[\[\]']", "", x).replace(",", " ").strip() for x in re.findall(r"\[[^\]]*\]", lab.group(1))]
    values = [int(x) for x in dat.group(1).split(",")]
    colors = col.group(1).replace(" ", "").split(",")
    top = kw_inc.groupby("매체이름")["노출수"].sum().sort_values(ascending=False).head(5)
    kind = kw_inc.groupby("매체이름")["캠페인"].agg(lambda s: "mint" if s.str.startswith("플레이스").all() else "ink")
    want = [(m.replace(" - ", " ").replace("-", " "), int(v), kind[m]) for m, v in top.items()]
    got = list(zip(labels, values, colors))
    check("05번 mediaChart top5 = CSV 매체 상위 5", got == want,
          f"화면 {[(l, v) for l, v, _ in got]} / CSV {[(l, v) for l, v, _ in want]}" + ("" if [c for _, _, c in got] == [c for _, _, c in want] else f" / 색 화면 {colors} vs {[c for _, _, c in want]}"))


def check_cards_vs_04(html, rows4):
    """15. 06번 신규 키워드 카드 큰 숫자 = 04번 같은 그룹의 평균순위 셀."""
    s6 = section(html, 6)
    cards = re.findall(r'color:var\(--ink-soft\);">(\S+) <span style="color:var\(--mint-dark\);font-weight:700;">\([\d/]+ 등록, \d+일차\)</span></div>'
                       r'.*?font-weight:800;color:var\(--mint-dark\);">([\d.]+)위', s6, re.S)
    if not cards:
        check("06번 카드 큰 숫자 = 04번 평균순위 셀", False, "카드 0건 — 카드가 없어졌으면 이 검사를 config로 끄는 설계가 필요, 마크업 변경이면 정규식 확인")
        return
    rank04 = {name: rank for name, _, rank in rows4}
    bad = [f"{g}: 카드 {v}위 vs 04번 {rank04.get(g, '없음')}" for g, v in cards if rank04.get(g) != f"{v}위"]
    check("06번 카드 큰 숫자 = 04번 평균순위 셀", not bad, f"카드 {len(cards)}개 검사, 불일치 {len(bad)}건" + (f": {'; '.join(bad)}" if bad else ""))


def check_competitors(s7, sr):
    """16·17. config competitors 순방향 포함 검사 + 경쟁사표 행 값 = 검색어 CSV."""
    rows = competitor_rows(s7)
    if not rows:
        check("07번 경쟁사표 밖 config 경쟁사명 검색어 0건", False, "경쟁사표 행 0건 — 마크업 변경 의심")
        check("07번 경쟁사표 노출·클릭 = 검색어 CSV", False, "경쟁사표 행 0건")
        return
    in_table = {n for n, _, _ in rows}
    agg = sr.groupby("검색어").agg(노출=("노출수", "sum"), 클릭=("클릭수", "sum"))
    leaked = sorted(k for k in agg.index if any(c in k for c in COMPETITORS) and k not in in_table)
    check("07번 경쟁사표 밖 config 경쟁사명 검색어 0건", not leaked,
          f"config {len(COMPETITORS)}개 이름 대조, 표 밖 {len(leaked)}건" + (f": {', '.join(leaked)} — 표기 변형이면 경쟁사표에 행 추가" if leaked else ""))
    bad = [f"{n}: 화면 {i}/{c} vs CSV {int(agg.loc[n, '노출']) if n in agg.index else '없음'}/{int(agg.loc[n, '클릭']) if n in agg.index else '없음'}"
           for n, i, c in rows if n not in agg.index or int(agg.loc[n, "노출"]) != i or int(agg.loc[n, "클릭"]) != c]
    check("07번 경쟁사표 노출·클릭 = 검색어 CSV", not bad, f"{len(rows)}행 검사, 불일치 {len(bad)}건" + (f": {'; '.join(bad)}" if bad else ""))


def check_11_12(html, pending=False):
    """19~21. 11번 항목 수·판정 줄, 11·12번 본문 금칙어, 07 각주·11·12 잔존 문구(--pending이면 허용)."""
    s11, s12 = section(html, 11), section(html, 12)
    notes7 = re.findall(r'<(?:p|div)[^>]*class="note"[^>]*>(.*?)</(?:p|div)>', section(html, 7), re.S)
    li = re.findall(r"<li>(.*?)</li>", s11, re.S)
    m = re.search(r"지난 회차 11번 (\d+)개 항목 판정: 유지 (\d+) · 뒤집힘 (\d+) · 근거 소멸 (\d+)", s11)
    if not li or not m:
        check("11번 항목 수·판정 줄", False, f"<li> {len(li)}개, 판정 줄 {'있음' if m else '없음'} — 마크업 변경 의심")
    else:
        n_main = len([x for x in li if "(참고)" not in x[:30]])
        n_ref = len([x for x in li if "(참고)" in x[:30]])
        prev, keep, flip, gone = (int(x) for x in m.groups())
        bad = []
        if n_main > 8: bad.append(f"본문 {n_main}개 > 8")
        if n_ref > 2: bad.append(f"(참고) {n_ref}개 > 2")
        if keep + flip + gone != prev: bad.append(f"판정 줄 {keep}+{flip}+{gone} ≠ {prev}")
        check("11번 항목 수·판정 줄", not bad, f"본문 {n_main} + (참고) {n_ref}, 판정 {prev} = {keep}+{flip}+{gone}" + (f" — {'; '.join(bad)}" if bad else ""))
    text = re.sub(r"<[^>]+>", "", s11 + s12)
    if not text.strip():
        check("11·12번 금칙어 0건", False, "11·12번 본문 0자 — 섹션 주석 또는 마크업 변경 의심")
        check("07 각주·11·12번 잔존 문구 0건", False, "11·12번 본문 0자")
        return
    hits = {w: len(re.findall(w, text)) for w in FORBIDDEN}
    bad = [f"{w} {n}건" for w, n in hits.items() if n]
    check("11·12번 금칙어 0건", not bad, f"{len(hits)}종 검사, {len(text):,}자" + (f" — {', '.join(bad)}" if bad else ""))
    text7 = re.sub(r"<[^>]+>", "", " ".join(notes7))
    if not notes7 or not s11.strip() or not s12.strip():
        check("07 각주·11·12번 잔존 문구 0건", False, f"07 각주 {len(notes7)}개 / 11번 {len(s11)}자 / 12번 {len(s12)}자 — 범위를 못 찾음, 마크업 변경 의심")
        return
    hits7 = {w: len(re.findall(w, text7)) for w in RESIDUAL}
    hits = {w: len(re.findall(w, text)) for w in RESIDUAL}
    bad = [f"{w} {n}건" for w, n in ((w, hits7[w] + hits[w]) for w in RESIDUAL) if n]
    detail = f"{len(RESIDUAL)}종 검사 — 07 각주 {sum(hits7.values())}건 + 11·12번 {sum(hits.values())}건"
    if bad and pending:
        check("07 각주·11·12번 잔존 문구 0건", True, f"--pending: 사용자 답 대기 배포라 허용 — {detail}: {', '.join(bad)} (답을 반영한 재배포에선 0건이어야 함)")
    else:
        check("07 각주·11·12번 잔존 문구 0건", not bad, detail + (f": {', '.join(bad)}" if bad else ""))


def main():
    pending = "--pending" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--pending"]
    if len(args) != 5:
        sys.exit(__doc__)

    html_path, kw_path, sr_path, hr_path, rg_path = args
    html = read_html(html_path)

    # --- 1. 태그 짝 ---
    check_tags(html)

    # --- 기준값: 제외 그룹을 뺀 키워드 보고서 (값 계산은 여기서 독립적으로) ---
    kw = read_csv(kw_path)
    kw_inc = exclude_groups(kw, CFG)
    kpi_clicks = int(kw_inc["클릭수"].sum())
    kpi_imp = int(kw_inc["노출수"].sum())
    kpi_cost = int(kw_inc["총비용"].sum())
    all_clicks = int(kw["클릭수"].sum())      # 제외 전 전체 (08·09번 기준)
    all_imp = int(kw["노출수"].sum())
    print(f"\n기준 KPI — 노출 {kpi_imp:,} / 클릭 {kpi_clicks} / 광고비 {kpi_cost:,}원")
    print(f"제외 전 전체 — 노출 {all_imp:,} / 클릭 {all_clicks} "
          f"(08·09번 각주 차이: 노출 {all_imp - kpi_imp}회 / 클릭 {all_clicks - kpi_clicks}회)\n")

    # --- 2. 07번 클릭수 검산 ---
    s7 = section(html, 7)
    rows = parse_main_rows(s7)
    main_clicks = sum(r["clicks"] for r in rows)
    one_clicks = len(click1_items(s7))
    comp_clicks = sum(c for _, _, c in competitor_rows(s7))
    total = main_clicks + one_clicks + comp_clicks
    check("07번 클릭수 합계 = KPI", total == kpi_clicks,
          f"정식표 {main_clicks} + 클릭1건 {one_clicks} + 경쟁사 {comp_clicks} = {total} (KPI {kpi_clicks})")

    # --- 3. 시간대별 클릭 합계 (KPI가 아니라 제외 전 전체와 비교 — SKILL.md "집계 기준") ---
    hr = read_csv(hr_path)
    hourly_clicks = int(hr["클릭수"].sum())
    check("09번 시간대별 클릭 합계 = 키워드 보고서 전체 클릭", hourly_clicks == all_clicks,
          f"시간대별 CSV {hourly_clicks} vs 전체 {all_clicks} (KPI {kpi_clicks})")

    # --- 4. CTR 강조 규칙 (07번) ---
    if not rows:
        check(f"07번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high", False, "정식표 행 0건 — 마크업이 바뀌어 정규식이 안 맞을 수 있음")
    else:
        mismatched = [f"{r['kw']}({r['ctr']}%, 강조={'있음' if r['has_hl'] else '없음'})" for r in rows if r["has_hl"] != (r["ctr"] >= CTR_HIGH)]
        check(f"07번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high", not mismatched,
              f"{len(rows)}행 검사, 불일치 {len(mismatched)}건" + (f": {', '.join(mismatched)}" if mismatched else ""))

    # --- 5. CTR 강조 규칙 (01번) ---
    check_ctr_rule(f"01번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high", parse_ctr_cells(section(html, 1)))

    # --- 6~13. 확장 검사 ---
    dmin, dmax, ndays = parse_days(kw)
    check_masthead(html, dmin, dmax, ndays)
    check_kpi_tiles(html, kpi_imp, kpi_clicks, kpi_cost)
    rows4 = parse_04_rows(html)
    check_budget_share(rows4)
    check_chart_width(html, ndays)
    check_date_labels(html, ndays)
    check_section_comments(html)
    rg = read_csv(rg_path)
    check_diff_footnotes(html, all_imp, kpi_imp, int(rg["노출수"].sum()))

    # --- 14~20. 2026-09-26 추가 (05 top5 · 06 카드 · 경쟁사 · 검색어 클릭합 · 11·12번) ---
    check_media_top5(html, kw_inc)
    check_cards_vs_04(html, rows4)
    sr = read_csv(sr_path)
    check_competitors(s7, sr)
    sr_clicks = int(sr["클릭수"].sum())
    check("검색어 CSV 클릭 합계 = KPI 클릭", sr_clicks == kpi_clicks,
          f"검색어 CSV {sr_clicks} vs KPI {kpi_clicks}" + ("" if sr_clicks == kpi_clicks else " — 검색어 보고서 기간이 다를 수 있음"))
    check_11_12(html, pending)

    failed = [n for n, ok, _ in results if not ok]
    print("\n" + "=" * 50)
    print(f"검사 {len(results)}개: PASS {len(results) - len(failed)} / FAIL {len(failed)}")
    if failed:
        print(f"실패 {len(failed)}건: {', '.join(failed)}")
        print("배포하지 말고 원인을 고친 뒤 다시 실행할 것.")
        return 1
    print("전부 통과. 배포 진행 가능.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
