#!/usr/bin/env python3
"""index.html(배포본 또는 작업본)에서 12개 섹션 값을 파싱해 compute.py JSON과 항목별 대조. 배포 전 차이 0이어야 한다.

사용법: python3 scripts/compare.py <index.html> <compute.json>
- 표 값·차트 배열·각주·section-desc 숫자·11번 수동 검사까지 대조한다(2026-09-26 ad48222 기준 99항목).
- 동률 자리는 "직전 순서 유지" 관행이라 집합+정렬 방향으로 대조한다(경쟁사표·클릭1건·클릭0·08 컴팩트).
- 마크업이 바뀌어 항목을 못 찾으면 [DIFF]로 나온다(조용히 통과하지 않음). 종료 코드 1 = 차이 있음.
"""
import json
import re
import sys

from reportlib import read_html, section as _section

html = read_html(sys.argv[1])
R = json.load(open(sys.argv[2], encoding="utf-8"))
sec = lambda n: _section(html, n)
def num(s): return int(s.replace(",", "").replace("원", "").replace("회", "").replace("위", "").strip())
def cells(tr): return [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
def rows(s): return [cells(t) for t in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S) if "<td" in t]
def chart_data(cid, label=None):
    blk = html[html.find(f"getElementById('{cid}')"):]
    nxt = blk.find("new Chart", 10)
    blk = blk[:nxt] if nxt != -1 else blk
    m = re.search(rf"label:\s*'{label}'\s*,\s*data:\s*\[([^\]]*)\]", blk) if label else re.search(r"data:\s*\[([^\]]*)\]", blk)
    return [float(x) if "." in x else int(x) for x in m.group(1).split(",")] if m else None
diffs = []; n_ok = 0
def cmp(name, got, want):
    global n_ok
    if got == want:
        n_ok += 1; print(f"  [OK]   {name}: {want if len(str(want)) < 60 else str(want)[:57] + '...'}")
    else:
        diffs.append(name); print(f"  [DIFF] {name}: 배포본 {got} / 재계산 {want}")
def grp(pat, s, flags=0):
    m = re.search(pat, s, flags)
    if not m: raise ValueError(pat)
    return m
try:
    # ---- masthead · og · KPI
    cmp("masthead", grp(r"집계 기간<b>([^<]+)</b>", html).group(1).strip(), R["masthead"])
    cmp("og:description", grp(r'og:description" content="([^"]+)"', html).group(1), R["og"])
    kpi = dict(re.findall(r'<div class="label">([^<]+)</div>\s*<div class="value">([^<]+)<span', html)); sub = re.findall(r'<div class="sub">([^<]+)</div>', html)
    cmp("KPI 노출", num(kpi["총 노출수"]), R["KPI"]["노출"]); cmp("KPI 클릭", num(kpi["총 클릭수"]), R["KPI"]["클릭"])
    cmp("KPI CTR", float(kpi["평균 클릭률"]), R["KPI"]["CTR"]); cmp("KPI 광고비", num(kpi["총 광고비"]), R["KPI"]["광고비"])
    cmp("KPI sub 일평균노출", float(grp(r"([\d.]+)회", sub[0]).group(1)), R["KPI"]["일평균노출"]); cmp("KPI sub 일평균클릭", float(grp(r"([\d.]+)회", sub[1]).group(1)), R["KPI"]["일평균클릭"])
    cmp("KPI sub 클릭당", num(grp(r"([\d,]+)원", sub[3]).group(1)), R["KPI"]["클릭당"])
    # ---- 01
    s1 = sec(1)
    cmp("01 dailyChart 노출", chart_data("dailyChart", "노출수"), R["01"]["노출"]); cmp("01 dailyChart 총비용", chart_data("dailyChart", "총비용\\(원\\)"), R["01"]["총비용"])
    lbl = re.findall(r"labels:\s*\[((?:'\d+/\d+\(.\)',?)+)\]", html)
    cmp("01/06 labels", [l.split(",")[0].strip("'") for l in lbl] + [len(l.split(",")) for l in lbl], [R["01"]["labels"][0]] * 2 + [R["nlabels"]] * 2)
    cmp("01 min-width", int(grp(r"min-width:\s*(\d+)px", s1).group(1)), R["minwidth"])
    t1 = [{"날짜": r[0], "노출": num(r[1]), "검색": num(r[2]), "콘텐츠": num(r[3]), "클릭": num(r[4]), "CTR": float(r[5].rstrip("%")), "CPC": num(r[6])} for r in rows(s1) if len(r) == 7]
    hl1 = re.findall(r'<td class="num( ctr-high)?">([\d.]+)%</td>', s1)
    cmp("01 표 5일", t1, [{k: v for k, v in r.items() if k != "hl"} for r in R["01"]["표5"]]); cmp("01 표 .ctr-high", [bool(h) for h, _ in hl1], [r["hl"] for r in R["01"]["표5"]])
    grid = re.findall(r'margin-bottom:2px;">([^<]+)</div>\s*<div style="font-size:15px;font-weight:800;(color:var\(--mint-dark\);)?">([\d.]+)위', s1)
    cmp("01 플레이스 순위 5칸", [{"날짜": d, "순위": float(v)} for d, _, v in grid], R["01"]["플레이스순위5"]); cmp("01 순위 민트 칸", [d for d, c, _ in grid if c], [R["01"]["순위민트"]])
    m = grp(r"검색 지면만 계산하면 <b>([\d.]+)%</b>\(노출 ([\d,]+)·클릭 (\d+)\)", s1)
    cmp("01 검색지면 CTR", float(m.group(1)), R["01"]["검색지면"]["CTR"]); cmp("01 검색지면 노출·클릭", [num(m.group(2)), num(m.group(3))], [R["01"]["검색지면"]["노출"], R["01"]["검색지면"]["클릭"]])
    m = grp(r"하루 평균은 ([\d,]+)원·클릭 ([\d.]+)건·CPC ([\d,]+)원으로, 상향 전 9/1~9/16\(하루 평균 ([\d,]+)원·([\d.]+)건·CPC ([\d,]+)원\)", s1)
    cmp("01 상향후 평균", [num(m.group(1)), float(m.group(2)), num(m.group(3))], [R["01"]["상향후"]["광고비"], R["01"]["상향후"]["클릭"], R["01"]["상향후"]["CPC"]])
    cmp("01 상향전 평균", [num(m.group(4)), float(m.group(5)), num(m.group(6))], [R["01"]["상향전"]["광고비"], R["01"]["상향전"]["클릭"], R["01"]["상향전"]["CPC"]])
    cmp("01 누적 가중순위", float(grp(r"누적 가중평균은 [\d.]+ → ([\d.]+)위", s1).group(1)), R["01"]["플레이스누적가중순위"])
    cmp("01 콘텐츠 누적 노출", num(grp(r"콘텐츠 노출 ([\d,]+)회", s1).group(1)), R["01"]["콘텐츠누적노출"])
    # ---- 02
    cmp("02 desc 플레이스 비중", float(grp(r"예산의 ([\d.]+)%", sec(2)).group(1)), R["02"]["플레이스비중"])
    cmp("02 groupChart 노출", chart_data("groupChart", "노출수"), R["02"]["groupChart"]["노출"]); cmp("02 groupChart 클릭", chart_data("groupChart", "클릭수"), R["02"]["groupChart"]["클릭"])
    cmp("02 costPie", chart_data("costPie"), R["02"]["costPie"])
    # ---- 03
    r3 = rows(sec(3)); body = [r for r in r3 if r[0] != "합계"]; tot = [r for r in r3 if r[0] == "합계"][0]
    def p3(r): return [num(r[1]), num(r[2]), None if r[3] == "–" else num(r[3])], [num(r[4]), num(r[5]), None if r[6] == "–" else num(r[6])], num(r[7])
    cmp("03 일별 표 전체 행", [{"날짜": r[0], "플레이스": p3(r)[0], "파워링크": p3(r)[1], "합계": p3(r)[2]} for r in body], R["03"]["rows"])
    cmp("03 합계 행", {"플레이스": p3(tot)[0], "파워링크": p3(tot)[1], "총": p3(tot)[2]}, R["03"]["합계"])
    cmp("03 desc 최고일", grp(r"최고치 (\S+) ([\d,]+)원", sec(3)).groups(), (R["03"]["최고일"], f"{R['03']['최고액']:,}"))
    # ---- 04
    got4 = [{"유형": r[0].replace(" 광고", ""), "그룹": re.split(r"\s*\(", r[1])[0].strip(), "노출": num(r[2]), "클릭": num(r[3]), "CTR": float(r[4].rstrip("%")),
             "총비용": num(r[5]), "CPC": num(r[6]), "순위": None if r[8] == "—" else float(r[8].rstrip("위")), "비중": float(r[7].rstrip("%"))} for r in rows(sec(4))]
    cmp("04 표", got4, R["04"]["rows"]); cmp("04 CPC 격차 desc", float(grp(r"→ ([\d.]+)배", sec(4)).group(1)), R["04"]["CPC격차"])
    cmp("04 파워링크 비중", float(grp(r"비중은 [\d.]+ → ([\d.]+)%", sec(4)).group(1)), R["04"]["파워링크비중"])
    # ---- 05
    blk5 = html[html.find("getElementById('mediaChart')"):]
    lab5 = [re.sub(r"[\[\]']", "", x).replace(",", " ").strip() for x in re.findall(r"\[[^\]]*\]", grp(r"labels:\s*\[(.*?)\],\n", blk5, re.S).group(1))]
    norm = lambda m: m.replace(" - ", " ").replace("-", " ")
    cmp("05 mediaChart top5 라벨", lab5, [norm(t["매체"]) for t in R["05"]["top5"]]); cmp("05 mediaChart top5 값", chart_data("mediaChart", "노출수"), [t["노출"] for t in R["05"]["top5"]])
    col5 = grp(r"backgroundColor:\s*\[([^\]]*)\]", blk5).group(1).replace(" ", "").split(",")
    cmp("05 mediaChart 색", col5, ["mint" if t["유형"] == "플레이스" else "ink" for t in R["05"]["top5"]])
    cmp("05 deviceChart", chart_data("deviceChart"), R["05"]["device"]); cmp("05 desc 모바일 비중", float(grp(r"모바일이 노출의 ([\d.]+)%", sec(5)).group(1)), R["05"]["모바일비중"])
    # ---- 06
    s6 = sec(6); cmp("06 rankChart", chart_data("rankChart", "평균노출순위"), R["06"]["rankChart"]); cmp("06 min-width", int(grp(r"min-width:\s*(\d+)px", s6).group(1)), R["minwidth"])
    cmp("06 desc 노원역 순위", float(grp(r"평균 ([\d.]+)위", s6).group(1)), R["06"]["노원역순위"])
    r6 = rows(s6); cmp("06 직접 등록", {"노출": num(r6[0][1]), "클릭": num(r6[0][2]), "순위": float(r6[0][3].rstrip("위")), "총비용": num(r6[0][4])}, R["06"]["직접"])
    cmp("06 자동매칭", {"노출": num(r6[1][1]), "클릭": num(r6[1][2]), "순위": float(r6[1][3].rstrip("위")), "총비용": num(r6[1][4])}, R["06"]["자동"])
    cmp("06 마지막날 직접/자동", [int(x) for x in grp(r"직접 (\d+)·자동 (\d+)회", s6).groups()], [R["06"]["마지막날"]["직접"], R["06"]["마지막날"]["자동"]])
    cards = re.findall(r'color:var\(--ink-soft\);">(\S+) <span style="color:var\(--mint-dark\);font-weight:700;">\(([\d/]+) 등록, (\d+)일차\)</span></div>.*?font-weight:800;color:var\(--mint-dark\);">([\d.]+)위', s6, re.S)
    cmp("06 카드(그룹·등록일·일차·큰숫자)", {c[0]: {"순위": float(c[3]), "등록일": c[1], "일차": int(c[2])} for c in cards}, R["06"]["카드"])
    cmp("06 카드 큰 숫자 = 04 셀", {c[0]: float(c[3]) for c in cards}, {r["그룹"]: r["순위"] for r in got4 if r["그룹"] in {c[0] for c in cards}})
    # ---- 07
    s7 = sec(7); main_html = s7[:s7.find("클릭 1건 검색어")]
    m7 = re.findall(r'<td class="name-cell">([^<]+)</td>\s*<td><span class="tag[^>]*>([^<]*)</span></td>\s*<td class="num">([\d,]+)</td>\s*<td class="num">(\d+)</td>\s*<td class="num( ctr-high)?">([\d.]+)%</td>\s*<td class="num">([\d,]+)원</td>\s*<td class="num">([\d,]+)원</td>', main_html)
    got7 = [{"검색어": a, "매칭": b, "노출": num(c), "클릭": num(d), "CTR": float(f), "hl": bool(e), "CPC": num(g), "총비용": num(h)} for a, b, c, d, e, f, g, h in m7]
    want7 = [dict(r, 매칭=r["매칭"].replace("*동률", "")) for r in R["07"]["정식표"]]
    cmp("07 정식표 행수", len(got7), len(want7))
    cmp("07 정식표 값(뱃지 동률은 배포본 유지)", got7, [dict(w, 매칭=g["매칭"]) if "*동률" in r["매칭"] else w for w, g, r in zip(want7, got7, R["07"]["정식표"])] if len(got7) == len(want7) else want7)
    print("      07 뱃지 동률 항목:", [r["검색어"] for r in R["07"]["정식표"] if "*동률" in r["매칭"]])
    txt = grp(r'line-height:1\.9;">(.*?)</div>', s7[s7.find("클릭 1건 검색어"):], re.S).group(1)
    c1 = [grp(r"(.+?)\((\d+)회/([\d,]+)원\)", x.strip()).groups() for x in txt.split(" · ")]
    cmp("07 클릭1건 목록(집합)", sorted([{"검색어": a, "노출": int(b), "총비용": num(c)} for a, b, c in c1], key=lambda x: x["검색어"]), sorted(R["07"]["클릭1"], key=lambda x: x["검색어"]))
    cmp("07 클릭1건 노출 내림차순", [int(b) for _, b, _ in c1] == sorted([int(b) for _, b, _ in c1], reverse=True), True)
    txt0 = grp(r'line-height:1\.9;">(.*?)</div>', s7[s7.find("노출은 있으나 클릭 0건인"):], re.S).group(1)
    c0 = [grp(r"(.+?)\((\d+)회\)", x.strip()).groups() for x in txt0.split(" · ")]
    cmp("07 클릭0 목록(집합)", sorted([{"검색어": a, "노출": int(b)} for a, b in c0], key=lambda x: x["검색어"]), sorted(R["07"]["클릭0목록"], key=lambda x: x["검색어"]))
    cmp("07 클릭0 목록 노출 내림차순", [int(b) for _, b in c0] == sorted([int(b) for _, b in c0], reverse=True), True)
    m = grp(r"클릭 0인 검색어 전체는 (\d+)개·노출 ([\d,]+)회", s7); cmp("07 클릭0 전체 각주", {"개수": int(m.group(1)), "노출": num(m.group(2))}, R["07"]["클릭0전체"])
    m = grp(r"행 단위 확장·클릭 0 노출은 (\S+) (\d+)회 → (\S+) (\d+)회 → (\S+) <b>(\d+)회</b>\((\d+)개", s7)
    cmp("07 확장·클릭0 행단위 3일", {m.group(1): int(m.group(2)), m.group(3): int(m.group(4)), m.group(5): int(m.group(6))}, R["07"]["확장클릭0행단위3일"]); cmp("07 확장·클릭0 마지막날 개수", int(m.group(7)), R["07"]["확장클릭0마지막날개수"])
    segc = s7[s7.find("경쟁사 브랜드명 검색어"):]
    mc = re.findall(r'<td class="name-cell">([^<]+)</td>\s*<td>[^<]*</td>\s*<td><span class="tag[^>]*>[^<]*</span></td>\s*<td class="num">(\d+)</td>\s*<td class="num">(\d+)</td>\s*<td class="num">([\d,]+)원</td>', segc)
    gc = [{"검색어": a, "노출": int(b), "클릭": int(c), "총비용": num(d)} for a, b, c, d in mc]
    cmp("07 경쟁사표(집합)", sorted(gc, key=lambda x: x["검색어"]), sorted(R["07"]["경쟁사표"], key=lambda x: x["검색어"]))
    cmp("07 경쟁사표 정렬(노출↓, 동률 클릭↓, 그 안은 직전 순서)", [(x["노출"], x["클릭"]) for x in gc] == sorted([(x["노출"], x["클릭"]) for x in gc], reverse=True), True)
    cmp("07 desc 상위2 비중", int(grp(r"클릭의 (\d+)% 차지", s7).group(1)), R["07"]["상위2비중"])
    cmp("07 클릭 합계(정식+1건+경쟁사)", num(kpi["총 클릭수"]), R["07"]["정식표클릭합"] + R["07"]["클릭1합"] + R["07"]["경쟁사클릭합"])
    print("      config 경쟁사명을 포함하는데 직전 표에 없는 검색어(신규 변형 후보):", R["07"]["신규변형후보"])
    # ---- 08
    s8 = sec(8)
    cmp("08 TOP10", [{"지역": r[0], "노출": num(r[1]), "클릭": num(r[2]), "총비용": num(r[3])} for r in rows(s8)], R["08"]["top10"])
    m = grp(r"\((\d+)개 지역·클릭 (\d+)건\)", s8); cmp("08 컴팩트 개수·클릭", [int(m.group(1)), int(m.group(2))], [R["08"]["컴팩트수"], R["08"]["컴팩트클릭"]])
    txt8 = grp(r'line-height:1\.9;">(.*?)</div>', s8[s8.find("TOP 10 외"):], re.S).group(1)
    c8 = [grp(r"(.+?)\(노출(\d+)·클릭(\d+)\)", x.strip()).groups() for x in txt8.split(" · ") if "노출" in x]
    def short(full):  # 08 컴팩트 목록 지역명 축약 규칙(report-structure.md 08번)
        return (full.replace("서울특별시 ", "").replace("경기도 ", "").replace("인천광역시 ", "인천 ").replace("광주광역시 ", "광주 ")
                .replace("전남광주통합특별시 ", "광주 ").replace("부산광역시 ", "부산 ").replace("경상북도 ", "").replace("세종특별자치시", "세종시"))
    cmp("08 컴팩트 목록(순서 포함, 지역명 축약)", [{"지역": a, "노출": int(b), "클릭": int(c)} for a, b, c in c8], [{"지역": short(r["지역"]), "노출": r["노출"], "클릭": r["클릭"]} for r in R["08"]["컴팩트"]])
    m = grp(r"클릭 0인 (\d+)개 지역에서 노출 ([\d,]+)회", s8); cmp("08 클릭0 각주", {"개수": int(m.group(1)), "노출": num(m.group(2))}, R["08"]["클릭0"])
    m = grp(r"노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이", s8); cmp("08 각주 N회", {"전체": num(m.group(1)), "KPI": num(m.group(2)), "차이": int(m.group(3))}, R["08"]["각주"])
    m = grp(r"노원구 단독으로 전체 노출의 (\d+)%·클릭의 (\d+)%", s8); cmp("08 노원 비중", {"노출%": int(m.group(1)), "클릭%": int(m.group(2))}, R["08"]["노원"])
    m = grp(r"노출 비중 (\d+)%·클릭 (\d+)%", s8); cmp("08 desc 타겟 비중", {"노출%": int(m.group(1)), "클릭%": int(m.group(2))}, {k: R["08"]["타겟"][k] for k in ("노출%", "클릭%")})
    m = grp(r"확인불가\"는 노출 ([\d,]+)·클릭 (\d+)·비용 ([\d,]+)원.*?비용 비중이 [\d.]+% → <b>([\d.]+)%</b>, CTR은 [\d.]+% → ([\d.]+)%", s8, re.S)
    cmp("08 확인불가", {"노출": num(m.group(1)), "클릭": int(m.group(2)), "비용": num(m.group(3)), "비용%": float(m.group(4)), "CTR": float(m.group(5))}, R["08"]["확인불가"])
    m = grp(r"타겟 밖 서울\(노출 ([\d,]+)·클릭 (\d+)\)의 CTR ([\d.]+)%는 타겟 5개 구\(([\d.]+)%\)", s8)
    cmp("08 타겟 밖 서울", {"노출": num(m.group(1)), "클릭": int(m.group(2)), "CTR": float(m.group(3))}, R["08"]["타겟밖서울"]); cmp("08 타겟 CTR", float(m.group(4)), R["08"]["타겟"]["CTR"])
    cmp("08 서울·경기 밖 비용%", float(grp(r"비용 비중 5%는 [\d.]+ → ([\d.]+)%", s8).group(1)), R["08"]["서울경기밖비용%"])
    m = grp(r"11위 (\S+)는 .*?(\d+)회·(\d+)건이 돼", s8); cmp("08 11위", {"지역": m.group(1), "노출": int(m.group(2))}, {"지역": short(R["08"]["11위"]["지역"]), "노출": R["08"]["11위"]["노출"]})
    # ---- 09
    s9 = sec(9); cmp("09 hourlyChart 노출", chart_data("hourlyChart", "노출수"), R["09"]["노출"]); cmp("09 hourlyChart 클릭", chart_data("hourlyChart", "클릭수"), R["09"]["클릭"])
    m = grp(r"심야\(22시~09시\)에도 노출 ([\d,]+)회·클릭 (\d+)회\(전체 클릭의 (\d+)%\)·비용 ([\d,]+)원 발생. 노출 비중은 (\d+)%, 클릭 비중은 (\d+)%", s9)
    cmp("09 심야 콜아웃", {"노출": num(m.group(1)), "클릭": int(m.group(2)), "비용": num(m.group(4)), "노출%": int(m.group(5)), "클릭%": int(m.group(6))}, R["09"]["심야"]); cmp("09 심야 클릭% (괄호)", int(m.group(3)), R["09"]["심야"]["클릭%"])
    m = grp(r"최다 클릭 시간대는 (\d+)시 (\d+)회", s9); cmp("09 최다", {"시": int(m.group(1)), "클릭": int(m.group(2))}, R["09"]["최다"])
    m = grp(r"2위는 (\d+)시 (\d+)회", s9); cmp("09 2위", {"시": int(m.group(1)), "클릭": int(m.group(2))}, {k: R["09"]["2위"][k] for k in ("시", "클릭")}); print("      09 2위 동률:", R["09"]["2위"]["동률"])
    cmp("09 desc 최다", [int(x) for x in grp(r"(\d+)시대 클릭 최다\((\d+)회", s9).groups()], [R["09"]["최다"]["시"], R["09"]["최다"]["클릭"]])
    m = grp(r"노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이", s9); cmp("09 각주 N회", {"전체": num(m.group(1)), "KPI": num(m.group(2)), "차이": int(m.group(3))}, R["09"]["각주"])
    # ---- 10
    s10 = sec(10)
    cmp("10 A/B/C/D 표", [[num(r[2]), num(r[3]), num(r[4])] for r in rows(s10)], [R["10"]["A"], R["10"]["B"], R["10"]["C"], R["10"]["D"]])
    cmp("10 placementChart 노출", chart_data("placementChart", "노출수"), R["10"]["placement"]["노출"]); cmp("10 placementChart 클릭", chart_data("placementChart", "클릭수"), R["10"]["placement"]["클릭"])
    m = grp(r"(\d+)일간 노출은 (.*?)회, 클릭은 (.*?)건으로 하루 평균 ([\d.]+)건", s10)
    cmp("10 9/6이후 노출 나열", [int(x) for x in re.sub(r"<wbr>", "", m.group(2)).split("·")], R["10"]["9/6이후노출"]); cmp("10 9/6이후 클릭 나열", [int(x) for x in re.sub(r"<wbr>", "", m.group(3)).split("·")], R["10"]["9/6이후클릭"])
    cmp("10 일수·하루평균클릭", [int(m.group(1)), float(m.group(4))], [R["10"]["9/6이후일수"], R["10"]["9/6이후하루평균클릭"]])
    cmp("10 desc 콘텐츠 N일 연속 0·클릭 A", [int(x) for x in grp(r"콘텐츠 지면 (\d+)일 연속 0회 — 클릭 (\d+)건 중 (\d+)건", s10).groups()], [R["10"]["9/6이후일수"], R["KPI"]["클릭"], R["10"]["A"][1]])
    cmp("10 파트너 마지막날", int(grp(r"— 9/\d+는 (\d+)회", s10).group(1)), R["10"]["파트너마지막날"]); print("      10 B 분해:", R["10"]["B분해"])
    # ---- 11·12 수동 검사(validate.py 20·21과 같은 규칙)
    s11, s12 = sec(11), sec(12); li = re.findall(r"<li>(.*?)</li>", s11, re.S)
    cmp("11 항목 수(본문 ≤8, 참고 ≤2)", [len([x for x in li if "(참고)" not in x[:30]]) <= 8, len([x for x in li if "(참고)" in x[:30]]) <= 2], [True, True])
    for w in ["필요", "시점", "할 것", "검토", "주째"]: cmp(f"11·12 금칙어 '{w}'", len(re.findall(w, re.sub(r"<[^>]+>", "", s11 + s12))), 0)
    for w in ["확인 요청", "판단 요청", "기다림", "확인 중", "대기"]: cmp(f"07·11·12 잔존 문구 '{w}'", len(re.findall(w, re.sub(r"<[^>]+>", "", s7 + s11 + s12))), 0)
    cmp("11 판정 줄 유지+뒤집힘+소멸 = 직전 항목 수", (lambda m: int(m.group(2)) + int(m.group(3)) + int(m.group(4)) == int(m.group(1)))(grp(r"지난 회차 11번 (\d+)개 항목 판정: 유지 (\d+) · 뒤집힘 (\d+) · 근거 소멸 (\d+)", s11)), True)
except (ValueError, IndexError, KeyError) as e:
    diffs.append(f"파싱 실패 {e}"); print(f"  [DIFF] 파싱 실패 — 마크업이 바뀌었으면 compare.py를 고칠 것: {e}")
print(f"\n== 대조 결과: OK {n_ok} / DIFF {len(diffs)}")
for d in diffs: print("   DIFF:", d)
sys.exit(1 if diffs else 0)
