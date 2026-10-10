#!/usr/bin/env python3
"""합본 4종 + config → 12개 섹션 값 JSON (5단계의 유일한 계산 출처 — 즉석 계산 금지).

사용법:
    "$PY" scripts/compute.py <합본폴더> [--competitors-html <직전 배포본 index.html>] [--balance <work/balance.json>] [-o out.json]

- 키는 report-structure.md 절 번호("KPI","01"~"10") + "masthead","og","minwidth","nlabels". 자리마다 값이 있어
  다음 회차의 자동 교체(E2)가 그대로 쓸 수 있게 한다. 11·12번은 계산 대상이 아니다(사람이 쓴다).
- 정의는 report-structure.md 각 절의 "정의(compute.py)" 줄과 1:1이다. 문서와 이 코드가 어긋나면 둘 다 고친다.
- 경쟁사 집합 = config `competitors` 이름을 포함하는 검색어 ∪ 직전 배포본 07번 경쟁사표의 검색어(표기 변형은 사람이
  행을 추가하는 관행이라 배포본이 정본). --competitors-html 이 없으면 config 이름 포함분만.
  --competitors-html 을 줬는데 그 표가 0행이면 `[FAIL]` exit 1(2026-10-06 — 소제목·행 마크업이 바뀌면 어순 변형 행이
  조용히 빠지던 경로, 탐색 기준선 프로브 r10: 36행 exit 0).
- validate.py 와 값 계산을 공유하지 않는다(reportlib은 읽기·필터·일수·섹션 자르기까지).
- (2026-10-09 판 F) --balance 가 있으면 "잔액"(광고비 잔액 카드 — balance_card 정의)을 더 낸다. 기록이 없거나·못 읽거나·꼴이 다르거나·읽은 날이
  집계 마지막 날 이하(지난 회차 기록)면 `[FAIL] 잔액 기록…` exit 1(출력 파일 안 씀). 5단계(balance.py 바로 뒤)·precheck 는 늘 붙이고, 5a(2-1 대조용)는 붙이지 않는다.
- (2026-10-10 매출 작업 A·C) --leads <장부> 면 "성과장부"(leads.verdict — 판정 낱말·'M/D까지'·입력 주 수뿐, **건수·매출 0** — config leads.publish = verdict 만,
  다른 값이면 [FAIL]) · --place <체크리스트> 면 "플레이스전후"(place_effect — 12번 플레이스 행 목록·효과 판정·채팅 질문 신호·이월 줄). 장부·체크리스트가 없거나 꼴이
  다르면 `[주의]` 를 찍고 판정 '확인 못 함'(장부) / 12번 플레이스 행 0(체크리스트 없음) — exit 0. 5단계·precheck 는 늘 붙인다(precheck 는 config 경로, 시험은
  환경 변수 SAERO_LEADS·SAERO_PLACE). 'M/D까지' 는 합본 마지막 날(masthead 끝).
"""
import argparse
import datetime as dt
import json
import math
import re
import sys

import pandas as pd

from reportlib import day_list, exclude_groups, load_config, read_csv, read_html, section

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — fetch_reports.py·exclusions.py와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

WD = "월화수목금토일"


def md(s):
    y, m, d = s.rstrip(".").split(".")
    return f"{int(m)}/{int(d)}"


def lab(s):
    y, m, d = s.rstrip(".").split(".")
    return f"{md(s)}({WD[pd.Timestamp(int(y), int(m), int(d)).weekday()]})"


def wrank(df):
    """평균노출순위 노출 가중평균, 순위 0 행 제외 (SKILL.md 계산 규칙)."""
    r = df[df["평균노출순위"] > 0]
    return round(float((r["평균노출순위"] * r["노출수"]).sum() / r["노출수"].sum()), 2) if r["노출수"].sum() else None


def pct(a, b, n=2):
    return round(a / b * 100, n) if b else 0


def cpc(cost, clk):
    return int(round(cost / clk)) if clk else None


def lr_share(vals, total):
    """04번 예산 비중 — 최대잔여법(소수 1자리, 합 100.0)."""
    raw = [v / total * 1000 for v in vals]
    fl = [int(x) for x in raw]
    rem = 1000 - sum(fl)
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - fl[i], reverse=True)[:rem]:
        fl[i] += 1
    return [x / 10 for x in fl]


def deployed_competitors(html):
    """직전 배포본 07번 경쟁사표 name-cell 목록."""
    s7 = section(html, 7)
    seg = s7[s7.find("경쟁사 브랜드명 검색어"):]
    return re.findall(r'<td class="name-cell">([^<]+)</td>\s*<td>[^<]*</td>\s*<td><span class="tag', seg)


def compute(D, cfg, comp_prev=(), bal=None, leads=None, place=None, prev_html=None):
    kw, sr, rg, hr = (read_csv(f"{D}/{k}.csv") for k in ("키워드", "검색어", "상세지역", "시간대별"))
    EXC, TARGET, CTRH = cfg["excluded_groups"], cfg["target_districts"], cfg["ctr_high_threshold"]
    out = {}
    days = day_list(kw)
    nd = len(days)
    inc = exclude_groups(kw, cfg)
    imp, clk, cost = int(inc["노출수"].sum()), int(inc["클릭수"].sum()), int(inc["총비용"].sum())
    all_imp, all_clk = int(kw["노출수"].sum()), int(kw["클릭수"].sum())
    out["masthead"] = f"{days[0][:10]} — {days[-1][5:10]} ({nd}일)"
    out["og"] = f"{md(days[0])}~{md(days[-1])} 주간 성과 요약"
    out["KPI"] = {"노출": imp, "클릭": clk, "CTR": pct(clk, imp), "광고비": cost, "일평균노출": round(imp / nd, 1),
                  "일평균클릭": round(clk / nd, 1), "클릭당": cpc(cost, clk)}
    out["minwidth"] = max(nd * cfg["chart_min_width"]["per_day_px"], cfg["chart_min_width"]["floor_px"])
    out["nlabels"] = nd
    # ---- 01 일별 추이
    g = inc.groupby("일별")
    pl = inc[inc["캠페인"].str.startswith("플레이스")]
    pw = inc[~inc["캠페인"].str.startswith("플레이스")]
    srch = inc[inc["검색/콘텐츠 매체"] == "검색"]
    cont = inc[inc["검색/콘텐츠 매체"] == "콘텐츠"]
    di = g["노출수"].sum().reindex(days)
    dc = g["클릭수"].sum().reindex(days)
    dcost = g["총비용"].sum().reindex(days)
    dsi = srch.groupby("일별")["노출수"].sum().reindex(days).fillna(0).astype(int)
    dci = cont.groupby("일별")["노출수"].sum().reindex(days).fillna(0).astype(int)
    rank5 = [{"날짜": md(d), "순위": wrank(pl[pl["일별"] == d])} for d in days[-5:]]  # 플레이스 광고 일별 가중순위
    out["01"] = {
        "labels": [lab(d) for d in days], "노출": [int(x) for x in di], "총비용": [int(x) for x in dcost],
        "표5": [{"날짜": lab(d), "노출": int(di[d]), "검색": int(dsi[d]), "콘텐츠": int(dci[d]), "클릭": int(dc[d]),
                "CTR": pct(dc[d], di[d]), "hl": bool(pct(dc[d], di[d]) >= CTRH), "CPC": cpc(int(dcost[d]), int(dc[d]))} for d in days[-5:]],
        "플레이스순위5": rank5, "순위민트": min(rank5, key=lambda x: x["순위"])["날짜"],  # 닷새 중 최솟값
        "누적CTR": pct(clk, imp),
        "검색지면": {"노출": int(srch["노출수"].sum()), "클릭": int(srch["클릭수"].sum()), "CTR": pct(srch["클릭수"].sum(), srch["노출수"].sum())},
        "플레이스누적가중순위": wrank(pl), "콘텐츠누적노출": int(cont["노출수"].sum())}

    def avg_pl(a, b):
        s = pl[(pl["일별"] >= a) & (pl["일별"] <= b)]
        n = s["일별"].nunique()
        return {"일수": n, "광고비": round(s["총비용"].sum() / n), "클릭": round(s["클릭수"].sum() / n, 1),
                "CPC": cpc(int(s["총비용"].sum()), int(s["클릭수"].sum()))}
    out["01"]["상향후"] = avg_pl("2026.09.17.", days[-1])   # 플레이스 일예산 상향(9/17) 뒤 — 배포본 서술용
    out["01"]["상향전"] = avg_pl("2026.09.01.", "2026.09.16.")
    # ---- 02 광고 유형별
    out["02"] = {"플레이스비중": lr_share([int(pl["총비용"].sum()), int(pw["총비용"].sum())], cost)[0],
                 "groupChart": {"노출": [int(pl["노출수"].sum()), int(pw["노출수"].sum())], "클릭": [int(pl["클릭수"].sum()), int(pw["클릭수"].sum())]},
                 "costPie": [int(pl["총비용"].sum()), int(pw["총비용"].sum())]}

    # ---- 03 일별 광고비
    def dcol(df, d):
        s = df[df["일별"] == d]
        c, k = int(s["총비용"].sum()), int(s["클릭수"].sum())
        return [c, k, cpc(c, k)]
    out["03"] = {"rows": [{"날짜": lab(d), "플레이스": dcol(pl, d), "파워링크": dcol(pw, d), "합계": int(dcost[d])} for d in days],
                 "합계": {"플레이스": [int(pl["총비용"].sum()), int(pl["클릭수"].sum()), cpc(int(pl["총비용"].sum()), int(pl["클릭수"].sum()))],
                        "파워링크": [int(pw["총비용"].sum()), int(pw["클릭수"].sum()), cpc(int(pw["총비용"].sum()), int(pw["클릭수"].sum()))], "총": cost},
                 "최고일": lab(dcost.idxmax()), "최고액": int(dcost.max())}
    # ---- 04 캠페인 상세 — 플레이스 1행 + 파워링크 그룹 총비용 내림차순, 예산 비중 최대잔여법
    rows4 = [("플레이스", "새로필라테스", pl)] + [("파워링크", gname, pw[pw["광고그룹"] == gname]) for gname in pw["광고그룹"].unique()]
    rows4 = [(t, n, int(s["노출수"].sum()), int(s["클릭수"].sum()), pct(s["클릭수"].sum(), s["노출수"].sum()), int(s["총비용"].sum()),
              cpc(int(s["총비용"].sum()), int(s["클릭수"].sum())), wrank(s) if t == "파워링크" else None) for t, n, s in rows4]
    rows4 = [rows4[0]] + sorted(rows4[1:], key=lambda r: -r[5])
    sh = lr_share([r[5] for r in rows4], cost)
    out["04"] = {"rows": [dict(zip(["유형", "그룹", "노출", "클릭", "CTR", "총비용", "CPC", "순위"], r)) | {"비중": s} for r, s in zip(rows4, sh)],
                 "비중합": round(sum(sh), 1), "CPC격차": round(rows4[0][6] / rows4[1][6], 2),
                 "파워링크비중": lr_share([int(pl["총비용"].sum()), int(pw["총비용"].sum())], cost)[1]}
    # ---- 05 매체·기기 — top5 = 매체이름 노출 상위 5(제외 그룹 뺀 값), 색 = 캠페인 유형
    m5 = inc.groupby("매체이름")["노출수"].sum().sort_values(ascending=False)
    mtype = inc.groupby("매체이름")["캠페인"].agg(lambda s: "플레이스" if s.str.startswith("플레이스").all() else ("파워링크" if (~s.str.startswith("플레이스")).all() else "혼합"))
    out["05"] = {"top5": [{"매체": m, "노출": int(v), "유형": mtype[m]} for m, v in m5.head(5).items()],
                 "device": [int(pl[pl["PC/모바일 매체"] == "모바일"]["노출수"].sum()), int(pl[pl["PC/모바일 매체"] == "PC"]["노출수"].sum()),
                            int(pw[pw["PC/모바일 매체"] == "모바일"]["노출수"].sum()), int(pw[pw["PC/모바일 매체"] == "PC"]["노출수"].sum())],
                 "모바일비중": round(inc[inc["PC/모바일 매체"] == "모바일"]["노출수"].sum() / imp * 100, 1)}
    # ---- 06 순위 추이 — rankChart = 노원역필라테스 그룹 전체(자동매칭 포함) 일별 가중순위, 매칭표 순위 1자리, 카드 = 최근 7일 노출 있는 신규 그룹
    nw = pw[pw["광고그룹"] == "노원역필라테스"]
    direct, auto = pw[pw["키워드"] != "-"], pw[pw["키워드"] == "-"]

    def mrow(s):
        return {"노출": int(s["노출수"].sum()), "클릭": int(s["클릭수"].sum()), "순위": round(wrank(s), 1), "총비용": int(s["총비용"].sum())}
    first_day = {gname: pw[pw["광고그룹"] == gname]["일별"].min() for gname in pw["광고그룹"].unique()}
    to_ts = lambda s: pd.Timestamp(s.rstrip(".").replace(".", "-"))
    out["06"] = {"rankChart": [wrank(nw[nw["일별"] == d]) for d in days], "노원역순위": wrank(nw), "직접": mrow(direct), "자동": mrow(auto),
                 "카드": {gname: {"순위": wrank(pw[pw["광고그룹"] == gname]), "등록일": md(first_day[gname]),
                                "일차": (to_ts(days[-1]) - to_ts(first_day[gname])).days + 1}
                         for gname in pw["광고그룹"].unique()
                         if gname != "노원역필라테스" and pw[(pw["광고그룹"] == gname) & (pw["일별"].isin(days[-7:]))]["노출수"].sum() > 0},
                 "마지막날": {"직접": int(direct[direct["일별"] == days[-1]]["노출수"].sum()), "자동": int(auto[auto["일별"] == days[-1]]["노출수"].sum())}}
    # 카드 서술용(카드 대조 항목과 섞지 않게 따로) — 그룹 하루 노출 30회 이상인 날(승격 조건 판정, [의도된 동작] 15)
    out["06"]["카드30회이상일"] = {g: [md(d) for d, v in pw[pw["광고그룹"] == g].groupby("일별")["노출수"].sum().items() if v >= 30]
                              for g in out["06"]["카드"]}
    # ---- 07 검색어 — 검색어 단위 합산(유형은 뱃지로), 경쟁사는 표로 분리
    gs = sr.groupby("검색어").agg(노출=("노출수", "sum"), 클릭=("클릭수", "sum"), 총비용=("총비용", "sum")).reset_index()
    comp_cfg = {k for k in gs["검색어"] if any(c in k for c in cfg["competitors"])}
    comp = comp_cfg | set(comp_prev)
    tt = sr.groupby(["검색어", "검색 유형"])["노출수"].sum().reset_index()
    badge = {}
    for k, s in tt.groupby("검색어"):
        s = s.sort_values("노출수", ascending=False)
        tie = len(s) > 1 and s.iloc[0]["노출수"] == s.iloc[1]["노출수"]
        badge[k] = ("일치" if s.iloc[0]["검색 유형"].startswith("일치") else "확장") + ("*동률" if tie else "")  # 동률이면 직전 뱃지 유지
    gen = gs[~gs["검색어"].isin(comp)]
    main = gen[gen["클릭"] >= 2].sort_values(["클릭", "노출"], ascending=[False, False])  # 동률 → 노출 내림차순
    out["07"] = {
        "정식표": [{"검색어": r.검색어, "매칭": badge[r.검색어], "노출": int(r.노출), "클릭": int(r.클릭), "CTR": pct(r.클릭, r.노출),
                   "hl": bool(pct(r.클릭, r.노출) >= CTRH), "CPC": cpc(int(r.총비용), int(r.클릭)), "총비용": int(r.총비용)} for r in main.itertuples()],
        "클릭1": [{"검색어": r.검색어, "노출": int(r.노출), "총비용": int(r.총비용)}
                 for r in gen[gen["클릭"] == 1].sort_values(["노출", "총비용"], ascending=[False, False]).itertuples()],  # 노출↓. 동률: HTML은 직전 순서 유지가 정본, 이 출력의 2차 키(총비용↓)는 참고 — compare.py는 집합+정렬 방향만 본다
        "클릭0목록": [{"검색어": r.검색어, "노출": int(r.노출)} for r in gen[(gen["클릭"] == 0) & (gen["노출"] >= 5)].sort_values("노출", ascending=False).itertuples()],
        "클릭0전체": {"개수": int((gs["클릭"] == 0).sum()), "노출": int(gs[gs["클릭"] == 0]["노출"].sum())},  # 경쟁사 포함
        "경쟁사표": [{"검색어": r.검색어, "노출": int(r.노출), "클릭": int(r.클릭), "총비용": int(r.총비용)}
                  for r in gs[gs["검색어"].isin(comp)].sort_values(["노출", "클릭"], ascending=[False, False]).itertuples()],  # 노출↓ 클릭↓, 그 안은 직전 순서
        "경쟁사클릭합": int(gs[gs["검색어"].isin(comp)]["클릭"].sum()), "정식표클릭합": int(main["클릭"].sum()), "클릭1합": int((gen["클릭"] == 1).sum()),
        "상위2비중": round((main.iloc[0]["클릭"] + main.iloc[1]["클릭"]) / clk * 100), "상위2": [main.iloc[0]["검색어"], main.iloc[1]["검색어"]],
        "확장클릭0행단위3일": {md(d): int(sr[(sr["일별"] == d) & (sr["검색 유형"] == "확장") & (sr["클릭수"] == 0)]["노출수"].sum()) for d in days[-3:]},
        "확장클릭0마지막날개수": int(sr[(sr["일별"] == days[-1]) & (sr["검색 유형"] == "확장") & (sr["클릭수"] == 0)]["검색어"].nunique()),
        "신규변형후보": sorted(comp_cfg - set(comp_prev)),  # config 이름을 포함하는데 직전 표에 없던 검색어 — 사람이 행 추가
        "검색어CSV클릭합": int(sr["클릭수"].sum())}
    # ---- 08 상세지역 — TOP10 = 노출 내림차순(확인불가 포함), 컴팩트 = 클릭↓ 노출↓, 비중 분모 = 제외 전 전체
    gr = rg.groupby("상세지역").agg(노출=("노출수", "sum"), 클릭=("클릭수", "sum"), 총비용=("총비용", "sum")).reset_index().sort_values(["노출", "클릭"], ascending=[False, False])
    top10, rest = gr.head(10), gr.iloc[10:]
    is_target = lambda n: any(n.endswith(t) for t in TARGET)
    tg = gr[gr["상세지역"].apply(is_target)]
    unk = gr[gr["상세지역"].str.contains("확인불가")]
    seoul_out = gr[gr["상세지역"].str.startswith("서울") & ~gr["상세지역"].apply(is_target)]
    outside = gr[~gr["상세지역"].str.startswith("서울") & ~gr["상세지역"].str.startswith("경기") & ~gr["상세지역"].str.contains("확인불가")]
    nowon = gr[gr["상세지역"] == "서울특별시 노원구"].iloc[0]
    out["08"] = {
        "top10": [{"지역": r.상세지역, "노출": int(r.노출), "클릭": int(r.클릭), "총비용": int(r.총비용)} for r in top10.itertuples()],
        "컴팩트": [{"지역": r.상세지역, "노출": int(r.노출), "클릭": int(r.클릭)} for r in rest[rest["클릭"] > 0].sort_values(["클릭", "노출"], ascending=[False, False]).itertuples()],
        "컴팩트수": int((rest["클릭"] > 0).sum()), "컴팩트클릭": int(rest[rest["클릭"] > 0]["클릭"].sum()),
        "클릭0": {"개수": int((rest["클릭"] == 0).sum()), "노출": int(rest[rest["클릭"] == 0]["노출"].sum())},
        "각주": {"전체": all_imp, "KPI": imp, "차이": all_imp - imp},
        "노원": {"노출%": round(nowon["노출"] / all_imp * 100), "클릭%": round(nowon["클릭"] / all_clk * 100)},
        "타겟": {"노출%": round(tg["노출"].sum() / all_imp * 100), "클릭%": round(tg["클릭"].sum() / all_clk * 100), "CTR": pct(tg["클릭"].sum(), tg["노출"].sum())},
        "확인불가": {"노출": int(unk["노출"].sum()), "클릭": int(unk["클릭"].sum()), "비용": int(unk["총비용"].sum()),
                  "비용%": round(unk["총비용"].sum() / rg["총비용"].sum() * 100, 1), "CTR": pct(unk["클릭"].sum(), unk["노출"].sum())},
        "타겟밖서울": {"노출": int(seoul_out["노출"].sum()), "클릭": int(seoul_out["클릭"].sum()), "CTR": pct(seoul_out["클릭"].sum(), seoul_out["노출"].sum())},
        "서울경기밖비용%": round(outside["총비용"].sum() / rg["총비용"].sum() * 100, 1), "11위": {"지역": gr.iloc[10]["상세지역"], "노출": int(gr.iloc[10]["노출"])}}
    # ---- 09 시간대별 — 심야 = 22·23·0~8시(09시 배타)
    night = [22, 23] + list(range(0, 9))
    hi, hc, hcost = [int(x) for x in hr["노출수"]], [int(x) for x in hr["클릭수"]], [int(x) for x in hr["총비용"]]
    ni, nc, ncost = sum(hi[h] for h in night), sum(hc[h] for h in night), sum(hcost[h] for h in night)
    order = sorted(range(24), key=lambda h: -hc[h])
    out["09"] = {"노출": hi, "클릭": hc, "심야": {"노출": ni, "클릭": nc, "비용": ncost, "노출%": round(ni / sum(hi) * 100), "클릭%": round(nc / sum(hc) * 100)},
                 "최다": {"시": order[0], "클릭": hc[order[0]]},
                 "2위": {"시": order[1], "클릭": hc[order[1]], "동률": [h for h in range(24) if hc[h] == hc[order[1]] and h != order[0]]},
                 "각주": {"전체": sum(hi), "KPI": imp, "차이": sum(hi) - imp}}
    # ---- 10 지면 — A = 검색 & 매체이름 `네이버` 접두 전부, B = 검색 & 그 외(기타 매체 검색분 포함), C·D = 콘텐츠
    isn = inc["매체이름"].str.startswith("네이버")
    iss = inc["검색/콘텐츠 매체"] == "검색"
    agg = lambda m: [int(inc[m]["노출수"].sum()), int(inc[m]["클릭수"].sum()), int(inc[m]["총비용"].sum())]
    since = days[days.index("2026.09.06."):] if "2026.09.06." in days else []
    out["10"] = {"A": agg(iss & isn), "B": agg(iss & ~isn), "C": agg(~iss & isn), "D": agg(~iss & ~isn),
                 "placement": {"노출": [int(srch["노출수"].sum()), int(cont["노출수"].sum())], "클릭": [int(srch["클릭수"].sum()), int(cont["클릭수"].sum())]},
                 "9/6이후일수": len(since), "9/6이후노출": [int(di[d]) for d in since], "9/6이후클릭": [int(dc[d]) for d in since],
                 "9/6이후하루평균클릭": round(sum(dc[d] for d in since) / len(since), 1) if since else None,
                 "최근7일노출": [int(di[d]) for d in days[-7:]], "최근7일클릭": [int(dc[d]) for d in days[-7:]],
                 "최근7일": f"{md(days[-7:][0])}~{md(days[-1])}",
                 "파트너마지막날": int(inc[(inc["일별"] == days[-1]) & iss & ~isn]["노출수"].sum()),
                 "B분해": {k: int(v) for k, v in inc[iss & ~isn].groupby("매체이름")["노출수"].sum().items()}}
    if bal is not None:
        out["잔액"] = balance_card(bal, kw, inc)
    end = dt.date(*(int(x) for x in days[-1].rstrip(".").split(".")))
    if leads is not None:
        out["성과장부"] = leads_card(leads, end, cfg)
    if place is not None:
        first = dt.date(*(int(x) for x in days[0].rstrip(".").split(".")))
        out["플레이스전후"] = place_effect(inc, first, end, place, cfg, prev_period_end(prev_html), section(prev_html or "", 12),
                                       out["성과장부"]["판정"] if "성과장부" in out else cfg["leads"]["verdict_words"]["unknown"])
    return out


class LeadsPublishError(ValueError):
    """config leads.publish 가 verdict 가 아님 — 건수를 내는 길은 설계 회차 몫."""


def leads_card(path, end, cfg):
    """12번 장부 행 값 — 판정 낱말·'M/D까지'·입력 주 수(공개 범위 verdict: 건수·매출 0). 장부 없음·꼴 다름 = '확인 못 함' + [주의]."""
    import leads as L
    c = cfg["leads"]
    if c.get("publish") != "verdict":
        raise LeadsPublishError(f"config leads.publish {c.get('publish')!r} — verdict 만(건수를 공개하는 길은 설계 회차 몫)")
    rows, st = L.load_ledger(path)
    word, n = L.verdict(rows, end, cfg)
    if rows is None:
        print(f"[주의] 장부 확인 못 함({st}) — 12번 장부 판정 '{word}' ({path})", file=sys.stderr)
    return {"판정": word, "기준": f"{end.month}/{end.day}까지", "상태": "ok" if rows is not None else st.split(":")[0],
            "입력주수": n, "창주": int(c["window_weeks"]), "최소주": int(c["min_weeks"])}


def place_effect(inc, first, end, path, cfg, prev_end, prev12, leads_word):
    """플레이스 손보기 효과(독립 계산 — 01 avg_pl 재사용 안 함). 플레이스 캠페인 **검색 지면만**(콘텐츠 행 뺌) · 바꾼 날 D 앞 W일 [D−W, D−1] vs 뒤 W일 [D+1, D+W] ·
    **달력 일수**(행 없는 날 = 0) · 하루 클릭 변화%·CTR 변화%가 둘 다 band 위 = 좋아짐 / 둘 다 아래 = 나빠짐 / 그 밖 = 구별 안 됨 · 앞뒤 W일 안에 다른 바꿈(다른 항목·
    같은 항목의 지난 바꿈) = 겹침 · D−W < 집계 첫날 = 비교 불가 · 뒤 W일이 덜 찼으면 측정 중(n/W일). 12번 = 판정 난 뒤 final_show_days 일까지의 바꾼 항목(바꾼 날 순) +
    ✗ 행(place.py 가 적은 in12_since — config 순서, items_in_12 개)."""
    import place as PL
    c = cfg["place_checklist"]
    W, keep, chat_days = int(c["window_days"]), int(c["final_show_days"]), int(c["chat_after_days"])
    vw, sw, band = c["verdict_words"], c["state_words"], c["band_pct"]
    names = {it["id"]: it["문구"] for it in c["items"]}
    mdd = lambda d: f"{d.month}/{d.day}"
    out = {"기준": f"{mdd(end)}까지", "창일수": W, "띠": band, "남김일": keep, "낱말": vw, "장부판정": leads_word,
           "12번": [], "측정": [], "채팅질문": [], "이월줄": [], "빠짐": []}
    rows, st = PL.load_checklist(path, cfg)
    if rows is None:
        out["상태"] = st.split(":")[0]
        print(f"[주의] {st} — 12번 플레이스 행 0 ({path})", file=sys.stderr)
        return out
    out["상태"] = "ok"
    s = inc[inc["캠페인"].str.startswith("플레이스") & (inc["검색/콘텐츠 매체"] == "검색")]
    sd = pd.to_datetime(s["일별"].astype(str).str.rstrip("."), format="%Y.%m.%d").dt.date
    daily = {d: (int(g["노출수"].sum()), int(g["클릭수"].sum())) for d, g in s.groupby(sd)}

    def window(a, b):  # 달력 날짜 a~b(포함) 합 — 행 없는 날 0
        imp = clk = 0
        for k in range((b - a).days + 1):
            i, cl = daily.get(a + dt.timedelta(days=k), (0, 0))
            imp += i
            clk += cl
        return imp, clk

    cur = PL.current(rows)
    events = PL.done_events(rows)
    measured = sorted([r for r in cur.values() if r["state"] == "done" and r["state_date"]], key=lambda r: (r["state_date"], r["id"]))
    for r in measured:
        Dd, rid = r["state_date"], r["id"]
        m = {"id": rid, "문구": names[rid], "바꾼날": mdd(Dd), "끝날": mdd(Dd + dt.timedelta(days=W))}
        others = [d for (i2, d) in events if (i2, d) != (rid, Dd)]
        n_after = max(0, min(W, (end - Dd).days))
        if Dd - dt.timedelta(days=W) < first:
            word = vw["short"]
        elif any(abs((d - Dd).days) <= W for d in others):
            word = vw["overlap"]
        elif n_after < W:
            word = f"{vw['measuring']}({n_after}/{W}일)"
        else:
            ib, cb = window(Dd - dt.timedelta(days=W), Dd - dt.timedelta(days=1))
            ia, ca = window(Dd + dt.timedelta(days=1), Dd + dt.timedelta(days=W))
            if cb == 0 or ib == 0 or ia == 0:
                word = vw["short"]
            else:
                dc, dctr = (ca / cb - 1) * 100, ((ca / ia) / (cb / ib) - 1) * 100
                if dc > band["clicks"][1] and dctr > band["ctr"][1]:
                    word = vw["up"]
                elif dc < band["clicks"][0] and dctr < band["ctr"][0]:
                    word = vw["down"]
                else:
                    word = vw["same"]
                m.update({"전": {"노출": ib, "클릭": cb, "하루클릭": round(cb / W, 1), "CTR": pct(cb, ib)},
                          "후": {"노출": ia, "클릭": ca, "하루클릭": round(ca / W, 1), "CTR": pct(ca, ia)},
                          "변화%": {"하루클릭": round(dc, 1), "CTR": round(dctr, 1)}})
        m["판정"] = word
        out["측정"].append(m)
        age = (end - (Dd + dt.timedelta(days=W))).days  # 판정 날(D+W) 뒤 지난 날 — 음수면 측정 중
        if age < keep:
            out["12번"].append(dict({k: v for k, v in m.items() if k != "판정"}, 종류="판정", 값=word))
        if prev_end is not None and (prev_end - (Dd + dt.timedelta(days=W))).days < keep <= age:
            out["빠짐"].append(f"{rid} {word}")
    for rid in PL.in12_ids(cur, cfg):
        since = cur[rid]["in12_since"]
        out["12번"].append({"id": rid, "문구": names[rid], "종류": "상태", "값": sw["todo"], "since": mdd(since)})
        if (end - since).days >= chat_days:
            out["채팅질문"].append(f"{rid} 12번 {mdd(since)}부터 {(end - since).days}일 그대로")
    # 이월 줄은 한 번 — 지난 배포본(끝 날 P) 뒤에 적힌 결정만: 보통은 적힌 날 > P + 1(P 회차는 P + 1 에 돌았다). 같은 기간 다시 계산(P = 이번 끝 날)이면
    # 이번 회차 날(> 끝 날)에 적혔고 지난 배포본 12번에 그 줄이 아직 없을 때만(앞 배포가 이미 실었으면 다시 안 씀)
    same = prev_end is not None and prev_end >= end
    gate = end if (prev_end is None or same) else prev_end + dt.timedelta(days=1)
    seen = (lambda line: line in (prev12 or "")) if same else (lambda line: False)
    for it in c["items"]:
        r = cur.get(it["id"])
        if r and r["state"] == "later" and r["revisit"] <= end:
            out["채팅질문"].append(f"{r['id']} 미룸 다시 볼 날({mdd(r['revisit'])}) 지남")
        line = None
        if r and r["state"] in ("no", "later") and r["recorded"] > gate:
            line = (f"{r['id']} {sw['no']}({mdd(r['state_date'])} 결정)" if r["state"] == "no"
                    else f"{r['id']} {sw['later']}({mdd(r['revisit'])} 다시 봄)")
        if r and r["state"] == "todo" and r["in12_since"] is None and r["recorded"] > gate:  # 순서에 밀려 12번에서 내려간 ✗ — 조용히 사라지지 않게 한 번
            hist = [x for x in rows if x["id"] == r["id"]]
            if len(hist) >= 2 and hist[-2]["state"] == "todo" and hist[-2]["in12_since"] is not None:
                line = f"{r['id']} {sw['todo']}(12번 자리 순서로 내림)"
        if line and not seen(line):
            out["이월줄"].append(line)
    return out


def prev_period_end(html):
    """직전 배포본 masthead `집계 기간<b>YYYY.MM.DD — MM.DD (N일)</b>` 의 끝 날짜(date) — 못 찾으면 None."""
    m = re.search(r"집계 기간<b>(\d{4})\.(\d{2})\.(\d{2}) — (\d{2})\.(\d{2}) \(\d+일\)</b>", html or "")
    if not m:
        return None
    y, m1, _, m2, d2 = (int(x) for x in m.groups())
    return dt.date(y + (1 if m2 < m1 else 0), m2, d2)


class BalanceError(ValueError):
    """잔액 기록(balance.py 의 work/balance.json)이 꼴이 다르거나 이번 회차 것이 아님 — 카드 값을 만들지 않는다."""


KST = dt.timezone(dt.timedelta(hours=9))


def balance_card(bal, kw, inc):
    """레이아웃 판 r2026-10-F 광고비 잔액 카드(report-structure.md "KPI 요약" — 정의(compute.py)).
    원 = balance.py 가 버린 bizmoney(= ⌊bizmoney_raw⌋ 대조) · 기준 = 읽은 시각 KST 'M/D(요일) HH:MM' ·
    창 = 키워드 보고서 `일별` 의 달력 날짜로 집계 마지막 날까지 7일(첫날보다 앞은 자른다 · 행 없는 날 = 0원) · 창합계 = 그 창의 총비용(제외 그룹 뺌 = 01 총비용·KPI 광고비 정의) ·
    일분 = ⌊원 × 창일수 ÷ 창합계⌋(정수 나눗셈 — 평균을 반올림하지 않는다) · 창합계 0 이면 None(며칠분 생략).
    실패 기록이면 {"상태": "fail", "기준": …}(값 없음 — 카드 "확인 못 함"). 읽은 날(KST)이 집계 마지막 날 이하면 BalanceError(지난 회차 기록 — 데이터는 언제나 어제까지)."""
    if not isinstance(bal, dict) or bal.get("status") not in ("ok", "fail") or not isinstance(bal.get("read_at"), str):
        raise BalanceError("잔액 기록 꼴이 다름(status ok|fail · read_at 문자열)")
    try:
        t = dt.datetime.fromisoformat(bal["read_at"].replace("Z", "+00:00"))
    except ValueError:
        raise BalanceError(f"잔액 기록 꼴이 다름(read_at {bal['read_at']!r})")
    if t.tzinfo is None:
        raise BalanceError(f"잔액 기록 꼴이 다름(read_at 시간대 없음 {bal['read_at']!r})")
    t = t.astimezone(KST)
    d = pd.to_datetime(kw["일별"].astype(str).str.rstrip("."), format="%Y.%m.%d")
    first, last = d.min(), d.max()
    if t.date() <= last.date():
        raise BalanceError(f"잔액 기록을 읽은 날 {t.date()}(KST)이 집계 마지막 날 {last.date()} 이하 — 지난 회차 기록, 이번 회차에 balance.py 를 다시")
    shown = f"{t.month}/{t.day}({WD[t.weekday()]}) {t:%H:%M}"
    if bal["status"] == "fail":
        return {"상태": "fail", "기준": shown}
    won, raw = bal.get("bizmoney"), bal.get("bizmoney_raw")
    if (isinstance(won, bool) or not isinstance(won, int) or isinstance(raw, bool) or not isinstance(raw, (int, float))
            or not math.isfinite(raw) or raw < 0 or won != math.floor(raw)):
        raise BalanceError(f"잔액 기록 꼴이 다름(bizmoney {won!r} · bizmoney_raw {raw!r} — 원 = ⌊raw⌋ 정수여야)")
    lo = max(first, last - dt.timedelta(days=6))
    di = pd.to_datetime(inc["일별"].astype(str).str.rstrip("."), format="%Y.%m.%d")
    total = int(inc.loc[(di >= lo) & (di <= last), "총비용"].sum())
    n = (last - lo).days + 1
    return {"상태": "ok", "원": won, "기준": shown, "창": f"{lo.month}/{lo.day}~{last.month}/{last.day}", "창일수": n, "창합계": total,
            "일분": (won * n // total) if total > 0 else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("combined")
    ap.add_argument("--competitors-html")
    ap.add_argument("--balance", help="balance.py 의 잔액 기록(work/balance.json) — 판 F 광고비 잔액 카드 값(\"잔액\")을 낸다. 5단계·precheck 는 늘 붙인다")
    ap.add_argument("--leads", help="주간 성과 장부(저장소 밖 — precheck 는 config leads.path·환경 변수 SAERO_LEADS) → \"성과장부\"(판정 낱말만)")
    ap.add_argument("--place", help="플레이스 체크리스트(precheck 는 config place_checklist.path·SAERO_PLACE) → \"플레이스전후\"")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    cfg = load_config()
    prev_html = read_html(a.competitors_html) if a.competitors_html else None
    comp_prev = deployed_competitors(prev_html) if a.competitors_html else ()
    if a.competitors_html and not comp_prev:  # 합본을 읽기 전에 멈춘다 — 직전 표 0행으로 계산하면 어순 변형 행이 조용히 빠진다
        print(f'[FAIL] 직전 배포본 경쟁사표 0행 — 머리글 "경쟁사 브랜드명 검색어" 또는 행 마크업 확인 ({a.competitors_html})')
        sys.exit(1)
    bal = None
    if a.balance:  # 합본을 읽기 전에 — 기록이 없거나 못 읽으면 compute.json 을 쓰지 않는다(카드 값을 옛 값으로 두는 길 0)
        try:
            with open(a.balance, encoding="utf-8") as f:
                bal = json.load(f)
        except (OSError, ValueError) as e:
            print(f"[FAIL] 잔액 기록을 못 읽음({type(e).__name__}): {a.balance} — 5단계 첫 명령 balance.py 를 이번 회차에 돌렸는지")
            sys.exit(1)
    try:
        out = compute(a.combined, cfg, comp_prev, bal, a.leads, a.place, prev_html)
    except BalanceError as e:
        print(f"[FAIL] 잔액 기록: {e} ({a.balance})")
        sys.exit(1)
    except LeadsPublishError as e:
        print(f"[FAIL] 성과 장부: {e}")
        sys.exit(1)
    text = json.dumps(out, ensure_ascii=False, indent=1, default=str)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[compute] {a.out}  {out['masthead']}  KPI {out['KPI']['노출']:,}/{out['KPI']['클릭']}/{out['KPI']['CTR']}%/{out['KPI']['광고비']:,}원"
              f"  경쟁사 {len(out['07']['경쟁사표'])}행(신규 변형 후보 {out['07']['신규변형후보']})"
              + ("" if "잔액" not in out else f"  잔액 {out['잔액']}")
              + ("" if "성과장부" not in out else f"  장부 판정 {out['성과장부']['판정']}")
              + ("" if "플레이스전후" not in out else
                 f"  플레이스 12번 {[(x['id'], x['값']) for x in out['플레이스전후']['12번']]} 채팅 질문 {len(out['플레이스전후']['채팅질문'])}"))
    else:
        print(text)


if __name__ == "__main__":
    main()
