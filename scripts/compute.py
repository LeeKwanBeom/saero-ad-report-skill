#!/usr/bin/env python3
"""합본 4종 + config → 12개 섹션 값 JSON (5단계의 유일한 계산 출처 — 즉석 계산 금지).

사용법:
    python3 scripts/compute.py <합본폴더> [--competitors-html <직전 배포본 index.html>] [-o out.json]

- 키는 report-structure.md 절 번호("KPI","01"~"10") + "masthead","og","minwidth","nlabels". 자리마다 값이 있어
  다음 회차의 자동 교체(E2)가 그대로 쓸 수 있게 한다. 11·12번은 계산 대상이 아니다(사람이 쓴다).
- 정의는 report-structure.md 각 절의 "정의(compute.py)" 줄과 1:1이다. 문서와 이 코드가 어긋나면 둘 다 고친다.
- 경쟁사 집합 = config `competitors` 이름을 포함하는 검색어 ∪ 직전 배포본 07번 경쟁사표의 검색어(표기 변형은 사람이
  행을 추가하는 관행이라 배포본이 정본). --competitors-html 이 없으면 config 이름 포함분만.
- validate.py 와 값 계산을 공유하지 않는다(reportlib은 읽기·필터·일수·섹션 자르기까지).
"""
import argparse
import json
import re

import pandas as pd

from reportlib import day_list, exclude_groups, load_config, read_csv, read_html, section

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


def compute(D, cfg, comp_prev=()):
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
                 "파트너마지막날": int(inc[(inc["일별"] == days[-1]) & iss & ~isn]["노출수"].sum()),
                 "B분해": {k: int(v) for k, v in inc[iss & ~isn].groupby("매체이름")["노출수"].sum().items()}}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("combined")
    ap.add_argument("--competitors-html")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    cfg = load_config()
    comp_prev = deployed_competitors(read_html(a.competitors_html)) if a.competitors_html else ()
    out = compute(a.combined, cfg, comp_prev)
    text = json.dumps(out, ensure_ascii=False, indent=1, default=str)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[compute] {a.out}  {out['masthead']}  KPI {out['KPI']['노출']:,}/{out['KPI']['클릭']}/{out['KPI']['CTR']}%/{out['KPI']['광고비']:,}원"
              f"  경쟁사 {len(out['07']['경쟁사표'])}행(신규 변형 후보 {out['07']['신규변형후보']})")
    else:
        print(text)


if __name__ == "__main__":
    main()
