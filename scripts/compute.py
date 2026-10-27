#!/usr/bin/env python3
"""합본 4종 + config → 리포트 11개 구역 값 JSON (5단계의 유일한 계산 출처 — 즉석 계산 금지).

사용법:
    "$PY" scripts/compute.py <합본폴더> [--competitors-html <직전 배포본 index.html>] [--balance <work/balance.json>] [--extra <work/extra>] [-o out.json]

- 키는 report-structure.md 절 번호("KPI","01"~"10") + "masthead","og","minwidth","nlabels". 자리마다 값이 있어
  다음 회차의 자동 교체(E2)가 그대로 쓸 수 있게 한다. 10·11번(핵심 요약·다음 액션)은 계산 대상이 아니다(사람이 쓴다).
  (2026-10-23 판 I 콘텐츠 지면 빼기) 키 "10"(A~D · placement · 최근7일* · 9/6이후*)은 리포트 구역이 없다 — 운영 서술 스크립트의 다른 구역 글 재료로만 남긴다
  (리포트 10번 = 핵심 요약). "01" 표5 는 날짜·노출·클릭·CTR·CPC(검색·콘텐츠 칸 없음) · "01" 에 01 ③ 괄호 재료 "콘텐츠첫날"·"콘텐츠끝날"(콘텐츠 지면 노출이 있는
  첫날·끝날 M/D — 없으면 null) · 재발 감시 "콘텐츠재발"(config content_watch.since 이후 날 중 콘텐츠 노출 > 0 인 날 [{날짜, 노출}] — 있으면 `[주의] 콘텐츠 지면 노출 재발 — …`
  한 줄을 stderr 에, exit 0 · 멈추지 않는다). 직전 배포본의 다음 액션 구역은 번호가 아니라 주석 이름(Action items — 판 H 까지 12번 · 판 I 부터 11번)으로 읽는다
  (reportlib.action_section — 못 찾거나 둘이면 `[FAIL]` exit 1: 조용히 빈 글로 읽으면 플레이스 이월 줄이 다시 써진다).
- 정의는 report-structure.md 각 절의 "정의(compute.py)" 줄과 1:1이다. 문서와 이 코드가 어긋나면 둘 다 고친다.
- 경쟁사 집합 = config `competitors` 이름을 포함하는 검색어 ∪ 직전 배포본 07번 경쟁사표의 검색어(표기 변형은 사람이
  행을 추가하는 관행이라 배포본이 정본). --competitors-html 이 없으면 config 이름 포함분만.
  --competitors-html 을 줬는데 그 표가 0행이면 `[FAIL]` exit 1(2026-10-06 — 소제목·행 마크업이 바뀌면 어순 변형 행이
  조용히 빠지던 경로, 탐색 기준선 프로브 r10: 36행 exit 0).
- validate.py 와 값 계산을 공유하지 않는다(reportlib은 읽기·필터·일수·섹션 자르기까지).
- (2026-10-09 판 F) --balance 가 있으면 "잔액"(광고비 잔액 카드 — balance_card 정의)을 더 낸다. 기록이 없거나·못 읽거나·꼴이 다르거나·읽은 날이
  집계 마지막 날 이하(지난 회차 기록)면 `[FAIL] 잔액 기록…` exit 1(출력 파일 안 씀). 5단계(balance.py 바로 뒤)·precheck 는 늘 붙이고, 5a(2-1 대조용)는 붙이지 않는다.
- (2026-10-10 매출 작업 A·C) --leads <장부> 면 "성과장부"(leads.verdict — 판정 낱말·'M/D까지'·입력 주 수뿐, **건수·매출 0** — config leads.publish = verdict 만,
  다른 값이면 [FAIL]) · --place <체크리스트> 면 "플레이스전후"(place_effect — 11번(판 H 까지 12번) 플레이스 행 목록·효과 판정·채팅 질문 신호·이월 줄 — 키 이름 "12번"은 그대로). 장부·체크리스트가 없거나 꼴이
  다르면 `[주의]` 를 찍고 판정 '확인 못 함'(장부) / 11번 플레이스 행 0(체크리스트 없음) — exit 0. 5단계·precheck 는 늘 붙인다(precheck 는 config 경로, 시험은
  환경 변수 SAERO_LEADS·SAERO_PLACE). 'M/D까지' 는 합본 마지막 날(masthead 끝).
- (2026-10-12 판 G 보고서 더 받기 A + B) --extra <work/extra>(extras.py combine 의 추가 합본·원장 사본) 면 "성별연령"(05 아래 카드 — 종류마다 기간 = 합본 머리 ·
  노출·비중·클릭·클릭률(노출 min_imps 미만 '적음')·비용 · 알 수 없음 % · 캠페인 단위라 제외 그룹 포함)·"변경기록"(04 아래 표 — 기간 = 집계 기간 ∩ 기록 구간 마지막 연속 구간 ·
  보일 주체 줄 — 같은 분은 한 줄(2026-10-12) — 최신 위 max_rows · 내용 한 구(등록 n개 · 삭제 n개 · 변경(전 n → 후 m개) · 칸 전 → 후 · 확장 소재 n개 추가 · 그 밖 유형만) · 스킬 등록 n회(고유 분)·삭제 k건 ·
  show_system 이면 SYSTEM 하루예산 중단 회수). 폴더·파일이 없거나 extras 설정이 꺼져 있으면 상태 '없음' + [주의](exit 0 — '확인 못 함'). 5단계·precheck 는 늘 붙인다.
- (2026-10-23 판 J 불필요 항목 빼기 — 사용자 결정 "추천대로") og = 'M/D~M/D 누적 성과 요약'(38) · 02.플레이스비중 = 04 표 플레이스 행 비중 · 04.파워링크비중 = 100 − 그 값(27 — 한 값) ·
  04.신규 = 일차 < config group_cards.new_days 인 파워링크 그룹(apply 가 04 이름 칸 '(M/D 신규)' 를 그 밖 그룹에서 뺀다 — 30) · 05.top5 = config media_chart(검색 지면 매체 상위 4 — 1) ·
  06.카드 = 최근 7일 노출 있고 (일차 < new_days 또는 config group_cards.promotion_groups) 인 그룹(5) · 07.정식표[].적음 = 노출 < config ctr_few_07.min_imps(hl 은 적음이 아닐 때만 — 35) ·
  성별·연령대: config gender_age.hide_unknown_kinds 종류는 알 수 없음 줄 0 · 표마다 '알수없음줄'(줄이 보이면 sub-head 괄호에 % 를 쓰지 않는다 — 8) · 첫 숫자가 같으면 '미만' 이 앞(36) ·
  변경 기록 확장소재 추가 = '확장 소재 n개 추가'(같은 분 묶음 안 건수의 합 — 28).
- (2026-10-26 판 K 01 요일 카드 — 사용자 결정 "추천대로 진행해줘") "01" 에 "요일"(weekday_avg — 검색 지면 · 제외 그룹 뺌 · 전 기간 누적 요일(월~일) 하루 평균:
  첫날·끝날 M/D · 일수 7 · 노출 7(반올림 정수) · 클릭 7(소수 1자리 — 그 요일 날이 0 이면 노출 0 · 클릭 null)). 01 차트(지면 전부)와 틀이 달라 평균 × 일수 합 ≠ 01 막대 합이 정상.
- (2026-10-27 판 L 하루예산 카드 — 사용자 결정 "추천대로 7건만 보여주고 진행해줘") --balance 가 있으면 "예산"(budget_card — balance.json 의 "budget"(balance.py 가 읽은 캠페인·그룹
  하루예산) + --extra 원장 사본의 SYSTEM `광고그룹 하루예산 중단` 줄: 플레이스 실제 한도 · 파워링크 캠페인·켜진 그룹 · 유형마다 기간(마지막 하루예산 변경 뒤 ~ 집계 끝날) 멈춘 수 ·
  최근 7일 · 멈춘 줄 전부 최신 위 — 00:00~00:09 줄은 전날 몫 `M/D(요) 밤 · 기록 M/D HH:MM`(2026-10-27 사용자 "전날 밤으로 표시"))). 예산 읽기 실패 = 상태 fail(카드 '확인 못 함' — exit 0) · 원장 사본 없음·extras 꺼짐·기록 구간이 집계 끝날에 못 미침 = 멈춤 상태 '없음'(exit 0) ·
  예산 기록 꼴이 다르거나 읽은 날 ≤ 집계 마지막 날이면 `[FAIL] 잔액 기록…`(잔액과 같은 길). 09-21 결정(config extras.history.show_system false)은 04 변경 기록 블록 몫 — 이 카드만 SYSTEM 줄을 쓴다.
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import sys

import pandas as pd

from reportlib import SectionError, action_section, day_list, exclude_groups, load_config, read_csv, read_html, section

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


def content_days(inc, days, cfg):
    """판 I(2026-10-23 콘텐츠 지면 빼기) — 콘텐츠 지면 노출(제외 그룹 뺀 키워드 보고서 `검색/콘텐츠 매체` = 콘텐츠)이 있는 날로 (첫날 M/D, 끝날 M/D, 재발).
    첫날·끝날 = 01 ③ 괄호 기간(없으면 None — 괄호 없음) · 재발 = config content_watch.since 이후 날 중 노출 > 0 인 날 [{날짜, 노출}] — 있으면
    `[주의] 콘텐츠 지면 노출 재발 — …` 한 줄(날짜·노출)을 stderr 에 찍는다(사용자 결정 5 — 리포트에 지면 구역이 없으니 운영 회차 끝 보고·채팅 한 줄, 멈추지 않는다)."""
    dci = inc[inc["검색/콘텐츠 매체"] == "콘텐츠"].groupby("일별")["노출수"].sum().reindex(days).fillna(0).astype(int)
    cdays = [d for d in days if dci[d] > 0]
    since = cfg["content_watch"]["since"].replace("-", ".") + "."   # '2026-09-06' → 키워드 보고서 `일별` 꼴 '2026.09.06.'
    rec = [{"날짜": md(d), "노출": int(dci[d])} for d in cdays if d >= since]
    first, last = (md(cdays[0]), md(cdays[-1])) if cdays else (None, None)
    if rec:
        print(f"[주의] 콘텐츠 지면 노출 재발 — 기준일 {md(since)} 이후 {len(rec)}일: " + " · ".join(f"{x['날짜']} {x['노출']:,}회" for x in rec)
              + f" (01 ③ 괄호 기간 {first}~{last} · 리포트에는 지면 구역 없음 — 끝 보고·채팅 한 줄)", file=sys.stderr)
    return first, last, rec


def weekday_avg(srch, days):
    """판 K(2026-10-26 01 요일 카드) — 제외 그룹 뺀 키워드 보고서 `검색/콘텐츠 매체` == 검색 행(srch)을 날마다 합한 노출·클릭(날 = day_list 전부 — 행 없는 날 0)을
    달력 요일(월~일)로 묶은 하루 평균. 노출 = 반올림 정수 · 클릭 = 소수 1자리(KPI 일평균클릭과 같은 파이썬 round — 정확히 반이면 짝수 쪽, 예 10.25 → 10.2) ·
    그 요일 날이 0 이면(합본 7일 미만) 노출 0 · 클릭 None. 기간은 전 기간 누적(최근 N주로 자르지 않음 — 사용자 결정 기본값 3).
    지면 전부(01 차트 틀)로 내지 않는 까닭: 8/28~9/5 콘텐츠 지면 노출이 토요일(8/29·9/5)을 가장 높게 만든다(검색 지면만이면 가장 낮음 — 기본값 2)."""
    di = srch.groupby("일별")["노출수"].sum().reindex(days).fillna(0)
    dc = srch.groupby("일별")["클릭수"].sum().reindex(days).fillna(0)

    def wday(s):
        y, m, d = s.rstrip(".").split(".")
        return pd.Timestamp(int(y), int(m), int(d)).weekday()
    by = [[d for d in days if wday(d) == k] for k in range(7)]
    return {"첫날": md(days[0]), "끝날": md(days[-1]), "일수": [len(b) for b in by],
            "노출": [round(int(di[b].sum()) / len(b)) if b else 0 for b in by],
            "클릭": [round(int(dc[b].sum()) / len(b), 1) if b else None for b in by]}


def card_groups(pw, days, nth, gc):
    """판 J(2026-10-23 결정 5) 06 요약 카드 그룹(파워링크 그룹 순서) — 노원역필라테스(rankChart 그룹) 밖 · 최근 7일(날짜 7개) 노출 > 0 ·
    (일차 < config group_cards.new_days 이거나 promotion_groups). nth = {그룹: 첫 노출일 포함 일차}."""
    promo = set(gc["promotion_groups"])
    return [g for g in pw["광고그룹"].unique()
            if g != "노원역필라테스" and pw[(pw["광고그룹"] == g) & (pw["일별"].isin(days[-7:]))]["노출수"].sum() > 0
            and (nth[g] < int(gc["new_days"]) or g in promo)]


def deployed_competitors(html):
    """직전 배포본 07번 경쟁사표 name-cell 목록."""
    s7 = section(html, 7)
    seg = s7[s7.find("경쟁사 브랜드명 검색어"):]
    return re.findall(r'<td class="name-cell">([^<]+)</td>\s*<td>[^<]*</td>\s*<td><span class="tag', seg)


def compute(D, cfg, comp_prev=(), bal=None, leads=None, place=None, prev_html=None, extra=None):
    kw, sr, rg, hr = (read_csv(f"{D}/{k}.csv") for k in ("키워드", "검색어", "상세지역", "시간대별"))
    EXC, TARGET, CTRH = cfg["excluded_groups"], cfg["target_districts"], cfg["ctr_high_threshold"]
    out = {}
    days = day_list(kw)
    nd = len(days)
    inc = exclude_groups(kw, cfg)
    imp, clk, cost = int(inc["노출수"].sum()), int(inc["클릭수"].sum()), int(inc["총비용"].sum())
    all_imp, all_clk = int(kw["노출수"].sum()), int(kw["클릭수"].sum())
    out["masthead"] = f"{days[0][:10]} — {days[-1][5:10]} ({nd}일)"
    out["og"] = f"{md(days[0])}~{md(days[-1])} 누적 성과 요약"   # 판 J(결정 38 — '주간' 빼기)
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
    rank5 = [{"날짜": md(d), "순위": wrank(pl[pl["일별"] == d])} for d in days[-5:]]  # 플레이스 광고 일별 가중순위
    out["01"] = {
        "labels": [lab(d) for d in days], "노출": [int(x) for x in di], "총비용": [int(x) for x in dcost],
        "표5": [{"날짜": lab(d), "노출": int(di[d]), "클릭": int(dc[d]),
                "CTR": pct(dc[d], di[d]), "hl": bool(pct(dc[d], di[d]) >= CTRH), "CPC": cpc(int(dcost[d]), int(dc[d]))} for d in days[-5:]],
        "플레이스순위5": rank5, "순위민트": min(rank5, key=lambda x: x["순위"])["날짜"],  # 닷새 중 최솟값
        "누적CTR": pct(clk, imp),
        "검색지면": {"노출": int(srch["노출수"].sum()), "클릭": int(srch["클릭수"].sum()), "CTR": pct(srch["클릭수"].sum(), srch["노출수"].sum())},
        "플레이스누적가중순위": wrank(pl), "콘텐츠누적노출": int(cont["노출수"].sum())}
    out["01"]["콘텐츠첫날"], out["01"]["콘텐츠끝날"], out["01"]["콘텐츠재발"] = content_days(inc, days, cfg)   # 판 I — 01 ③ 괄호 기간 · 재발 감시
    out["01"]["요일"] = weekday_avg(srch, days)   # 판 K — 01 요일 카드(검색 지면 · 전 기간 누적 요일 하루 평균)

    def avg_pl(a, b):
        s = pl[(pl["일별"] >= a) & (pl["일별"] <= b)]
        n = s["일별"].nunique()
        return {"일수": n, "광고비": round(s["총비용"].sum() / n), "클릭": round(s["클릭수"].sum() / n, 1),
                "CPC": cpc(int(s["총비용"].sum()), int(s["클릭수"].sum()))}
    out["01"]["상향후"] = avg_pl("2026.09.17.", days[-1])   # 플레이스 일예산 상향(9/17) 뒤 — 배포본 서술용
    out["01"]["상향전"] = avg_pl("2026.09.01.", "2026.09.16.")
    # ---- 02 광고 유형별
    out["02"] = {"플레이스비중": None,   # 판 J(결정 27) — 04 표 플레이스 행 비중과 한 값(아래 04 뒤에 채운다 — 두 몫 최대잔여법은 다섯 행 값과 어긋났다)
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
    gc = cfg["group_cards"]
    first_day = {gname: pw[pw["광고그룹"] == gname]["일별"].min() for gname in pw["광고그룹"].unique()}
    to_ts = lambda s: pd.Timestamp(s.rstrip(".").replace(".", "-"))
    nth = {gname: (to_ts(days[-1]) - to_ts(first_day[gname])).days + 1 for gname in first_day}   # 등록일(첫 노출일) 포함 일차
    out["04"] = {"rows": [dict(zip(["유형", "그룹", "노출", "클릭", "CTR", "총비용", "CPC", "순위"], r)) | {"비중": s} for r, s in zip(rows4, sh)],
                 "비중합": round(sum(sh), 1), "CPC격차": round(rows4[0][6] / rows4[1][6], 2),
                 "파워링크비중": round(100 - sh[0], 1),   # 판 J(결정 27) — = 04 표 파워링크 행 합(플레이스 + 파워링크 = 100.0)
                 "신규": sorted(g for g, n in nth.items() if n < int(gc["new_days"]))}   # 판 J(결정 30) — '(M/D 신규)' 를 둘 그룹(일차 < new_days)
    out["02"]["플레이스비중"] = sh[0]
    # ---- 05 매체·기기 — top5(키 이름 그대로) = config media_chart: `검색/콘텐츠 매체` == placement 행의 매체이름 노출 상위 top_n(제외 그룹 뺀 값 — 판 J 결정 1, 판 I 까지 전체 상위 5), 색 = 캠페인 유형
    mc = cfg["media_chart"]
    med = inc[inc["검색/콘텐츠 매체"] == mc["placement"]]
    m5 = med.groupby("매체이름")["노출수"].sum().sort_values(ascending=False)
    mtype = med.groupby("매체이름")["캠페인"].agg(lambda s: "플레이스" if s.str.startswith("플레이스").all() else ("파워링크" if (~s.str.startswith("플레이스")).all() else "혼합"))
    out["05"] = {"top5": [{"매체": m, "노출": int(v), "유형": mtype[m]} for m, v in m5.head(int(mc["top_n"])).items()],
                 "device": [int(pl[pl["PC/모바일 매체"] == "모바일"]["노출수"].sum()), int(pl[pl["PC/모바일 매체"] == "PC"]["노출수"].sum()),
                            int(pw[pw["PC/모바일 매체"] == "모바일"]["노출수"].sum()), int(pw[pw["PC/모바일 매체"] == "PC"]["노출수"].sum())],
                 "모바일비중": round(inc[inc["PC/모바일 매체"] == "모바일"]["노출수"].sum() / imp * 100, 1)}
    # ---- 06 순위 추이 — rankChart = 노원역필라테스 그룹 전체(자동매칭 포함) 일별 가중순위, 매칭표 순위 1자리,
    # 카드 = 최근 7일 노출 있고 (일차 < group_cards.new_days 또는 promotion_groups) 인 그룹(판 J 결정 5 — 판 I 까지 최근 7일 노출 있는 그룹 전부)
    nw = pw[pw["광고그룹"] == "노원역필라테스"]
    direct, auto = pw[pw["키워드"] != "-"], pw[pw["키워드"] == "-"]

    def mrow(s):
        return {"노출": int(s["노출수"].sum()), "클릭": int(s["클릭수"].sum()), "순위": round(wrank(s), 1), "총비용": int(s["총비용"].sum())}
    out["06"] = {"rankChart": [wrank(nw[nw["일별"] == d]) for d in days], "노원역순위": wrank(nw), "직접": mrow(direct), "자동": mrow(auto),
                 "카드": {gname: {"순위": wrank(pw[pw["광고그룹"] == gname]), "등록일": md(first_day[gname]), "일차": nth[gname]}
                         for gname in card_groups(pw, days, nth, gc)},
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
    few = int(cfg["ctr_few_07"]["min_imps"])   # 판 J(결정 35) — 노출이 이보다 적으면 클릭률 칸 '적음'(강조 0)
    out["07"] = {
        "정식표": [{"검색어": r.검색어, "매칭": badge[r.검색어], "노출": int(r.노출), "클릭": int(r.클릭), "CTR": pct(r.클릭, r.노출),
                   "hl": bool(pct(r.클릭, r.노출) >= CTRH and r.노출 >= few), "적음": bool(r.노출 < few),
                   "CPC": cpc(int(r.총비용), int(r.클릭)), "총비용": int(r.총비용)} for r in main.itertuples()],
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
        out["예산"] = budget_card(bal, extra, cfg, days)   # 판 L — 하루예산 · 예산 도달 멈춤 카드(예산 = balance.json budget · 멈춤 = --extra 원장 사본)
    if extra is not None:   # 판 G(2026-10-12 보고서 더 받기 A + B) — 05 아래 성별·연령대 카드 · 04 아래 계정 변경 기록 표
        out["성별연령"], out["변경기록"] = extra_cards(extra, cfg, days)
    end = dt.date(*(int(x) for x in days[-1].rstrip(".").split(".")))
    if leads is not None:
        out["성과장부"] = leads_card(leads, end, cfg)
    if place is not None:
        first = dt.date(*(int(x) for x in days[0].rstrip(".").split(".")))
        out["플레이스전후"] = place_effect(inc, first, end, place, cfg, prev_period_end(prev_html), action_section(prev_html),   # 다음 액션 = 판 H 12번 · 판 I 11번
                                       out["성과장부"]["판정"] if "성과장부" in out else cfg["leads"]["verdict_words"]["unknown"])
    return out


# ---- 판 G(2026-10-12 — 보고서 더 받기 A + B): 추가 합본(work/extra — scripts/extras.py combine) → 05 아래 카드 · 04 아래 표
def _ga_order(label, unknown):
    """성별·연령대 줄 순서 — 알 수 없음은 맨 끝, 숫자가 든 값(연령 구간)은 첫 숫자 순(같으면 '미만' 이 앞 — 판 J 결정 36: 14세 미만 · 14세 ~ 18세), 그 밖은 글자 순(남성 < 여성)."""
    m = re.search(r"\d+", label)
    return (label == unknown, int(m.group(0)) if m else 10**6, "미만" not in label, label)


def ga_table(path, name, spec, ga):
    """추가 합본 <종류>.csv 하나 → 성별 또는 연령대 표 값. 기간 = 합본 머리(실제 기간 — masthead 와 다를 수 있다) · 비중 = 노출 ÷ 합(소수 1자리) ·
    클릭률 = 노출 min_imps 미만이면 None + 적음 · 알 수 없음% = 알 수 없음 노출 ÷ 합 · show_unknown false 거나 종류가 hide_unknown_kinds 에 들면 그 줄은 표에서 뺀다
    (판 J 결정 8 — 연령대: 줄이 성별과 같다) · 알수없음줄 = 그 줄이 표에 있나(있으면 sub-head 괄호에 % 를 쓰지 않는다 — apply·compare·validate).
    캠페인 단위 보고서라 excluded_groups 를 못 뺀다(카드 ※ 각주 '캠페인 단위라 04 표와 합이 다를 수 있음' — A-6 · 판 J 부터 머리 괄호는 '(네이버 추정)' 만)."""
    import extras as X
    if not os.path.exists(path):
        return {"상태": "없음", "사유": "추가 합본 없음(첫 회·수집 실패)"}
    _, s, e, _ = X.read_head(path)
    df = read_csv(path)
    dim, unk, mi = spec["dim"], ga["unknown"], int(ga["min_imps"])
    show_unk = bool(ga["show_unknown"]) and spec["kind"] not in ga.get("hide_unknown_kinds", [])
    for c in ("노출수", "클릭수", "총비용"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    g = df.groupby(df[dim].astype(str))[["노출수", "클릭수", "총비용"]].sum()
    tot_i, tot_c, tot_k = int(g["노출수"].sum()), int(g["클릭수"].sum()), int(g["총비용"].sum())
    rows = []
    for val in sorted(g.index, key=lambda v: _ga_order(v, unk)):
        n, c, k = int(g.loc[val, "노출수"]), int(g.loc[val, "클릭수"]), int(g.loc[val, "총비용"])
        if val == unk and not show_unk:
            continue
        few = n < mi or n == 0
        rows.append({"구분": val, "노출": n, "비중": round(n / tot_i * 100, 1) if tot_i else 0.0, "클릭": c,
                     "CTR": None if few else pct(c, n), "적음": few, "비용": k})
    by_type = {}
    if "캠페인" in df.columns:
        pl = df["캠페인"].astype(str).str.startswith("플레이스")
        for t, m in (("플레이스", pl), ("파워링크", ~pl)):
            gt = df[m].groupby(df[m][dim].astype(str))[["노출수", "클릭수"]].sum()
            by_type[t] = {v: {"노출": int(gt.loc[v, "노출수"]), "클릭": int(gt.loc[v, "클릭수"])} for v in gt.index}
    u = int(g.loc[unk, "노출수"]) if unk in g.index else 0
    return {"상태": "ok", "이름": name, "기간": f"{md(s.strftime('%Y.%m.%d.'))}~{md(e.strftime('%Y.%m.%d.'))}",
            "시작": s.strftime("%Y.%m.%d."), "끝": e.strftime("%Y.%m.%d."), "rows": rows,
            "합": {"노출": tot_i, "클릭": tot_c, "비용": tot_k}, "알수없음%": round(u / tot_i * 100, 1) if tot_i else None,
            "알수없음줄": any(r["구분"] == unk for r in rows), "유형별": by_type}


def _items(lines):
    """변경 내용 세부 줄('확장 검색: a, b, c' · '제외키워드: ') → 항목 수(', ' 로 가름 · 빈칸 0)."""
    n = 0
    for ln in lines:
        v = ln.partition(":")[2].strip() if ":" in ln else ln.strip()
        n += len([x for x in v.split(", ") if x.strip()])
    return n


def change_phrase(kind, content):
    """변경 내용 → 표의 '내용' 한 구(목록 원문 0 — 개수만). 둘째 줄로 가른다(막음 B-2):
    `등록된 내용` = 등록 n개 · `삭제된 내용` = 삭제 n개 · `변경 전`…`변경 후` = 타겟팅 변경이면 변경(전 n → 후 m개), 그 밖은 '칸 전 → 후'(값에 ', ' 목록이면 개수) ·
    그 밖(설정 값 등) = '' (유형만). 확장소재 추가 + `등록된 내용` = '확장 소재 1개 추가'(원장 한 줄 = 확장 소재 하나 — 판 J 결정 28, 그 전엔 속성 칸 수 '등록 5개' 로 틀렸다 ·
    같은 분 묶음은 history_table 이 건수를 더한다)."""
    L = content.split("\n")
    lab = L[1].strip() if len(L) > 1 else ""
    if kind == "확장소재 추가" and lab == "등록된 내용":
        return "확장 소재 1개 추가"
    names = lambda seg: "·".join(dict.fromkeys(ln.partition(":")[0].strip() for ln in seg if ":" in ln and ln.partition(":")[0].strip()))
    if lab in ("등록된 내용", "삭제된 내용"):
        k = names(L[2:])
        return f"{'등록' if lab == '등록된 내용' else '삭제'} {_items(L[2:])}개" + (f"({k})" if k else "")
    if lab == "변경 전" and "변경 후" in L[2:]:
        i = L.index("변경 후", 2)
        before, after = L[2:i], L[i + 1:]
        if kind == "타겟팅 변경":
            k = names(before)
            return (f"{k} " if k else "") + f"변경(전 {_items(before)} → 후 {_items(after)}개)"
        fb = dict((ln.partition(":")[0].strip(), ln.partition(":")[2].strip()) for ln in before if ":" in ln)
        fa = dict((ln.partition(":")[0].strip(), ln.partition(":")[2].strip()) for ln in after if ":" in ln)
        parts = []
        for k in fb:
            if k not in fa:
                continue
            if ", " in fb[k] or ", " in fa[k]:
                parts.append(f"{k} {_items([fb[k]])} → {_items([fa[k]])}개")
            else:
                parts.append(f"{k} {fb[k]} → {fa[k]}")
        return " · ".join(parts)
    return ""


EXT_ADD = re.compile(r"확장 소재 (\d+)개 추가")


def merge_ext(phrases):
    """같은 분 묶음 안 '확장 소재 n개 추가' 구들 → 첫 자리에 하나(건수 합 — 판 J 결정 28: 12:46 노원역 2 + 노원산전 1 = 3개). 그 밖 구는 그대로(겹침 제거는 부르는 쪽)."""
    n = sum(int(m.group(1)) for m in (EXT_ADD.fullmatch(p) for p in phrases) if m)
    out, done = [], False
    for p in phrases:
        if not EXT_ADD.fullmatch(p):
            out.append(p)
        elif not done:
            out.append(f"확장 소재 {n}개 추가")
            done = True
    return out


def history_table(D, h, days):
    """원장 사본(work/extra/변경이력.csv) + 기록 구간 사본 → 04 아래 '계정 변경 기록' 표 값.
    표 기간 = masthead ∩ 기록 구간의 **마지막 연속 구간**(막음 B-1 — 기록 구간 = 성공한 다운로드마다 [화면 시작, 받은 날 − 1]) · 그 안의 show 주체 줄을
    같은 분(일시 원문)끼리 한 줄로 묶어(2026-10-12 — 유형·대상·내용은 겹치지 않는 값을 ' · ' 로) 최신 위 max_rows 개 · '건수' = 묶은 줄 수 · 스킬 줄은 '제외 검색어 등록 n회(실행 수 = 고유 분) · 삭제 k건' · show_system 이면 SYSTEM 하루예산 중단 회수(기본 false — 09-21 결정)."""
    import extras as X
    led, cov = os.path.join(D, X.HISTORY_FILE), os.path.join(D, X.COVERED_FILE)
    if not os.path.exists(led) or not os.path.exists(cov):
        return {"상태": "없음", "사유": "원장 없음(첫 회·수집 실패)"}
    rows, spans = X.read_ledger(led), X.read_covered(cov)
    if not spans:
        return {"상태": "없음", "사유": "기록 구간 없음"}
    runs = []
    for s, e in sorted(spans):
        if runs and s <= runs[-1][1] + dt.timedelta(days=1):
            runs[-1][1] = max(runs[-1][1], e)
        else:
            runs.append([s, e])
    cs, ce = runs[-1]
    m0 = dt.date(*(int(x) for x in days[0].rstrip(".").split(".")))
    m1 = dt.date(*(int(x) for x in days[-1].rstrip(".").split(".")))
    ps, pe = max(m0, cs), min(m1, ce)
    if ps > pe:
        return {"상태": "없음", "사유": f"기록 구간 {cs.month}/{cs.day}~{ce.month}/{ce.day} 이 집계 기간과 겹치지 않음"}
    d = lambda r: dt.date(int(r[0][0:4]), int(r[0][5:7]), int(r[0][8:10]))
    inp = [r for r in rows if ps <= d(r) <= pe]
    # 같은 분(일시 원문)은 한 줄로 묶는다(사용자 결정 2026-10-12 "같은 시각 줄은 하나로 묶어줘") — 유형·대상·내용은 겹치지 않는 값을 원장 순서대로 ' · ' 로 잇는다
    srt = sorted([r for r in inp if r[2] in h["show"]], key=lambda r: r[0], reverse=True)
    shown = []
    for r in srt:
        if shown and shown[-1][0][0] == r[0]:
            shown[-1].append(r)
        else:
            shown.append([r])
    j = lambda xs: " · ".join(dict.fromkeys(x for x in xs if x))
    out_rows = [{"일시": f"{int(g[0][0][5:7])}/{int(g[0][0][8:10])} {g[0][0][12:17]}", "유형": j(r[1] for r in g), "주체": j(r[2] for r in g),
                 "대상": j(r[4] or r[3] or "—" for r in g), "내용": j(merge_ext([change_phrase(r[1], r[5]) for r in g]))} for g in shown[:int(h["max_rows"])]]
    sk = [r for r in inp if r[2] == "스킬" and r[1] == "타겟팅 변경"]
    lab = lambda r: (r[5].split("\n") + ["", ""])[1].strip()
    out = {"상태": "ok", "기간": f"{ps.month}/{ps.day}~{pe.month}/{pe.day}", "시작": ps.strftime("%Y.%m.%d."), "끝": pe.strftime("%Y.%m.%d."),
           "집계기간같음": (ps, pe) == (m0, m1), "rows": out_rows, "보일주체": list(h["show"]), "건수": len(shown), "표시": len(out_rows),
           "스킬": {"등록회": len({r[0] for r in sk if lab(r) == "등록된 내용"}), "삭제건": sum(1 for r in sk if lab(r) == "삭제된 내용")}}
    if h.get("show_system"):
        out["시스템"] = {"하루예산중단": sum(1 for r in inp if r[2] == "시스템" and "하루예산 중단" in r[1])}
    return out


def extra_cards(D, cfg, days):
    """--extra <폴더> → ("성별연령", "변경기록"). 폴더·합본이 없거나 extras 설정이 꺼져 있으면 각 {"상태": "없음", "사유": …} + [주의](exit 0 — 카드·표 '확인 못 함')."""
    import extras as X
    ex, warns = X.extras_config(cfg["report_fetch"])
    for w in warns:
        print(w, file=sys.stderr)
    if ex is None:
        off = {"상태": "없음", "사유": "extras 설정 꺼짐"}
        return dict(off), dict(off)
    ga = {"상태": "ok", "min_imps": ex["gender_age"]["min_imps"] if ex["gender_age"] else None, "표": []}
    for name, spec in ex["reports"].items():
        try:
            t = ga_table(os.path.join(D, f"{spec['kind']}.csv"), name, spec, ex["gender_age"])
        except (X.ExtrasError, KeyError, ValueError, OSError) as e:
            t = {"상태": "없음", "사유": f"추가 합본을 못 읽음({type(e).__name__})"}
        t["종류"] = spec["kind"]
        if t["상태"] != "ok":
            print(f"[주의] {spec['kind']} 카드 확인 못 함 — {t['사유']} ({D})", file=sys.stderr)
        ga["표"].append(t)
    if not any(t["상태"] == "ok" for t in ga["표"]):
        ga = {"상태": "없음", "사유": "추가 합본 없음(첫 회·수집 실패·입력 없음)", "표": ga["표"]}
    if ex["history"]:
        try:
            hist = history_table(D, ex["history"], days)
        except (X.ExtrasError, ValueError, OSError, IndexError) as e:
            hist = {"상태": "없음", "사유": f"원장 사본을 못 읽음({type(e).__name__})"}
    else:
        hist = {"상태": "없음", "사유": "history 설정 없음"}
    if hist["상태"] != "ok":
        print(f"[주의] 계정 변경 기록 확인 못 함 — {hist['사유']} ({D})", file=sys.stderr)
    return ga, hist


class LeadsPublishError(ValueError):
    """config leads.publish 가 verdict 가 아님 — 건수를 내는 길은 설계 회차 몫."""


def leads_card(path, end, cfg):
    """11번(판 H 까지 12번) 장부 행 값 — 판정 낱말·'M/D까지'·입력 주 수(공개 범위 verdict: 건수·매출 0). 장부 없음·꼴 다름 = '확인 못 함' + [주의]."""
    import leads as L
    c = cfg["leads"]
    if c.get("publish") != "verdict":
        raise LeadsPublishError(f"config leads.publish {c.get('publish')!r} — verdict 만(건수를 공개하는 길은 설계 회차 몫)")
    rows, st = L.load_ledger(path)
    word, n = L.verdict(rows, end, cfg)
    if rows is None:
        print(f"[주의] 장부 확인 못 함({st}) — 11번 장부 판정 '{word}' ({path})", file=sys.stderr)
    return {"판정": word, "기준": f"{end.month}/{end.day}까지", "상태": "ok" if rows is not None else st.split(":")[0],
            "입력주수": n, "창주": int(c["window_weeks"]), "최소주": int(c["min_weeks"])}


def place_effect(inc, first, end, path, cfg, prev_end, prev12, leads_word):
    """플레이스 손보기 효과(독립 계산 — 01 avg_pl 재사용 안 함). 플레이스 캠페인 **검색 지면만**(콘텐츠 행 뺌) · 바꾼 날 D 앞 W일 [D−W, D−1] vs 뒤 W일 [D+1, D+W] ·
    **달력 일수**(행 없는 날 = 0) · 하루 클릭 변화%·CTR 변화%가 둘 다 band 위 = 좋아짐 / 둘 다 아래 = 나빠짐 / 그 밖 = 구별 안 됨 · 앞뒤 W일 안에 다른 바꿈(다른 항목·
    같은 항목의 지난 바꿈) = 겹침 · D−W < 집계 첫날 = 비교 불가 · 뒤 W일이 덜 찼으면 측정 중(n/W일). 11번(키 "12번" — 판 H 까지 화면 12번) = 판정 난 뒤 final_show_days 일까지의 바꾼 항목(바꾼 날 순) +
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
        print(f"[주의] {st} — 11번 플레이스 행 0 ({path})", file=sys.stderr)
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
            out["채팅질문"].append(f"{rid} 11번 {mdd(since)}부터 {(end - since).days}일 그대로")
    # 이월 줄은 한 번 — 지난 배포본(끝 날 P) 뒤에 적힌 결정만: 보통은 적힌 날 > P + 1(P 회차는 P + 1 에 돌았다). 같은 기간 다시 계산(P = 이번 끝 날)이면
    # 이번 회차 날(> 끝 날)에 적혔고 지난 배포본 다음 액션 구역(판 H 12번 · 판 I 11번 — action_section)에 그 줄이 아직 없을 때만(앞 배포가 이미 실었으면 다시 안 씀)
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
        if r and r["state"] == "todo" and r["in12_since"] is None and r["recorded"] > gate:  # 순서에 밀려 11번에서 내려간 ✗ — 조용히 사라지지 않게 한 번
            hist = [x for x in rows if x["id"] == r["id"]]
            if len(hist) >= 2 and hist[-2]["state"] == "todo" and hist[-2]["in12_since"] is not None:
                line = f"{r['id']} {sw['todo']}(11번 자리 순서로 내림)"
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


# ---- 판 L(2026-10-27 — 하루예산 카드, 사용자 결정 "추천대로 7건만 보여주고 진행해줘"): 잔액 카드 아래 한 줄 전체 카드
BUDGET_TYPES = (("플레이스", "PLACE"), ("파워링크", "WEB_SITE"))   # 카드 두 줄 = 캠페인 유형(campaignTp) — 그 밖 유형 캠페인은 카드 밖([주의])
STOP_KIND = "광고그룹 하루예산 중단"                               # 원장 SYSTEM 줄 유형(references/report-fetch.md — 캠페인·그룹 칸 빈칸, 내용 첫 줄 = 그룹 이름)
BUDGET_LINE = re.compile(r"^하루예산:\s*([\d,]+)원\s*$")
STOP_LATE_MIN = 10   # (2026-10-27 사용자 "전날 밤으로 표시") 00:00~00:09 멈춤 줄 = 전날 예산이 자정 직전에 다 쓰인 기록(9/17 광고비 20,312원 · 기록 9/18 00:02)


def _stop_day(t, d0):
    """멈춤 줄 일시 → 그 멈춤의 날(예산을 다 쓴 날). 00:00~00:(STOP_LATE_MIN-1) 이고 전날 ≥ 기간 시작 d0 이면 전날, 아니면 그날."""
    p = t.date() - dt.timedelta(days=1)
    return p if t.hour == 0 and t.minute < STOP_LATE_MIN and p >= d0 else t.date()


def _when(r):
    """원장 일시 '2026.10.26. 20:19' → datetime(분)."""
    return dt.datetime.strptime(r[0], "%Y.%m.%d. %H:%M")


def _stamp(t):
    return f"{t.month}/{t.day}({WD[t.weekday()]}) {t:%H:%M}"


def _budget_rec(b):
    """balance.json "budget"(ok) 의 꼴 — 캠페인·그룹마다 이름·유형 문자열 · useDailyBudget·userLock bool · dailyBudget 0 이상 정수. 다르면 BalanceError."""
    def item(x, what):
        if (not isinstance(x, dict) or not isinstance(x.get("name"), str) or not isinstance(x.get("type"), str)
                or not isinstance(x.get("useDailyBudget"), bool) or not isinstance(x.get("userLock"), bool)
                or isinstance(x.get("dailyBudget"), bool) or not isinstance(x.get("dailyBudget"), int) or x["dailyBudget"] < 0):
            raise BalanceError(f"예산 기록 꼴이 다름({what} {str(x)[:80]})")
    cs = b.get("campaigns")
    if not isinstance(cs, list):
        raise BalanceError("예산 기록 꼴이 다름(campaigns 목록 아님)")
    for c in cs:
        item(c, "캠페인")
        if not isinstance(c.get("groups"), list):
            raise BalanceError(f"예산 기록 꼴이 다름(캠페인 {c['name']!r} groups 목록 아님)")
        for g in c["groups"]:
            item(g, "그룹")
    return cs


def budget_card(bal, D, cfg, days):
    """레이아웃 판 r2026-10-L 하루예산 카드(report-structure.md "KPI 요약" — 하루예산 카드(판 L) 정의(compute.py)).
    예산(balance.json "budget" — 캠페인 유형 PLACE = 플레이스 · WEB_SITE = 파워링크, 유형마다 캠페인 하나 — 둘 이상이면 켜진 것 하나, 아니면 '확인 못 함' + [주의]):
      한도 값 = useDailyBudget 이면 dailyBudget, 아니면 None(제한 없음) · 켜진 그룹 = userLock false · 플레이스 '한도' = 켜진 그룹이 하나일 때 min(그룹, 캠페인)(None 은 한도 없음 —
      둘 다 None 이면 None) · 파워링크(와 켜진 그룹 둘 이상인 플레이스)는 캠페인 값 + 켜진 그룹 값 목록 · 캠페인 userLock = 상태 '꺼짐'.
    멈춤(budget_stops) · 예산 기록 없음(판 L 전 balance.py)·fail = {"상태": "fail", "기준", "사유"} — 카드 '확인 못 함'. 꼴이 다르거나 읽은 날 ≤ 집계 마지막 날 = BalanceError."""
    last = dt.date(*(int(x) for x in days[-1].rstrip(".").split(".")))
    b = bal.get("budget")
    if b is None:
        t = dt.datetime.fromisoformat(bal["read_at"].replace("Z", "+00:00")).astimezone(KST)   # balance_card 가 먼저 꼴·날짜를 봤다
        return {"상태": "fail", "기준": _stamp(t), "사유": "예산 기록 없음(판 L 전 balance.py 기록)"}
    if not isinstance(b, dict) or b.get("status") not in ("ok", "fail") or not isinstance(b.get("read_at"), str):
        raise BalanceError("예산 기록 꼴이 다름(budget.status ok|fail · read_at 문자열)")
    try:
        t = dt.datetime.fromisoformat(b["read_at"].replace("Z", "+00:00"))
    except ValueError:
        raise BalanceError(f"예산 기록 꼴이 다름(budget.read_at {b['read_at']!r})")
    if t.tzinfo is None:
        raise BalanceError(f"예산 기록 꼴이 다름(budget.read_at 시간대 없음 {b['read_at']!r})")
    t = t.astimezone(KST)
    if t.date() <= last:
        raise BalanceError(f"예산 기록을 읽은 날 {t.date()}(KST)이 집계 마지막 날 {last} 이하 — 지난 회차 기록, 이번 회차에 balance.py 를 다시")
    if b["status"] == "fail":
        return {"상태": "fail", "기준": _stamp(t), "사유": str(b.get("reason") or "알 수 없음")}
    cs = _budget_rec(b)
    out, warn = {"상태": "ok", "기준": _stamp(t)}, []
    lim = lambda x: x["dailyBudget"] if x["useDailyBudget"] else None
    for label, tp in BUDGET_TYPES:
        mine = [c for c in cs if c["type"] == tp]
        if len(mine) > 1 and len([c for c in mine if not c["userLock"]]) == 1:
            mine = [c for c in mine if not c["userLock"]]
        if not mine:
            out[label] = {"상태": "캠페인 없음"}
            continue
        if len(mine) > 1:
            out[label] = {"상태": "확인 못 함"}
            warn.append(f"{label} 캠페인 {len(mine)}개({', '.join(c['name'] for c in mine)}) — 카드는 유형마다 하나")
            continue
        c = mine[0]
        on = [g for g in c["groups"] if not g["userLock"]]
        e = {"상태": "꺼짐" if c["userLock"] else "ok", "캠페인이름": c["name"], "캠페인": lim(c), "그룹": [lim(g) for g in on],
             "그룹이름": [g["name"] for g in c["groups"]]}
        if label == "플레이스":
            vals = [v for v in (e["캠페인"], e["그룹"][0]) if v is not None] if len(on) == 1 else []
            e["한도"] = min(vals) if vals else None
        out[label] = e
    other = [c["name"] for c in cs if c["type"] not in {tp for _, tp in BUDGET_TYPES}]
    if other:
        warn.append(f"카드 밖 유형 캠페인 {other}")
    out["멈춤"] = budget_stops(D, cfg, last, out)
    out["주의"] = warn + out["멈춤"].pop("주의", [])
    for w in out["주의"]:
        print(f"[주의] 하루예산 카드 — {w}", file=sys.stderr)
    return out


def _budget_change(content):
    """사람 변경 줄 내용 → 하루예산 칸(`하루예산:` · `하루예산 사용여부:`)이 변경 전 → 후로 바뀌었나."""
    L = [x.strip() for x in content.split("\n")]
    if "변경 전" not in L or "변경 후" not in L:
        return False
    i, j = L.index("변경 전"), L.index("변경 후")
    if j < i:
        return False
    kv = lambda seg: {x.partition(":")[0].strip(): x.partition(":")[2].strip() for x in seg if ":" in x and x.startswith("하루예산")}
    fb, fa = kv(L[i + 1:j]), kv(L[j + 1:])
    return bool(fb or fa) and any(fb.get(k) != fa.get(k) for k in set(fb) | set(fa))


def budget_stops(D, cfg, last, B):
    """판 L 멈춤 셈 — 입력 = --extra 원장 사본(work/extra/변경이력.csv · 변경이력_기록구간.csv ← extras.py combine) · 기록 구간 = 마지막 연속 구간(history_table 과 같은 규칙).
    멈춤 줄 = 주체 `시스템` · 유형 `광고그룹 하루예산 중단` · 그룹 = 내용 첫 줄 → 예산 읽기의 그룹 이름(유형 안 모든 그룹 — 꺼진 그룹 포함)으로 유형을 가른다
    (이름이 안 맞거나 두 유형에 다 있으면 카드에 넣지 않고 [주의]). 유형마다 기간 시작 = 그 캠페인 또는 그 유형 그룹의 하루예산 변경(주체 `사람` · 내용 `변경 전`/`변경 후` 의
    `하루예산…:` 값이 다름) 중 마지막 줄의 일시 — 그 일시 **뒤** 멈춤만 센다(같은 날 앞선 멈춤은 옛 예산) · 일수 = 그 날 ~ 집계 끝날 양끝 포함. 기록 구간 안에 변경이 없으면
    기록 구간 첫날(시작종류 '기록' — 그날 0시부터). 기간 끝 = 집계 끝날(그 뒤 일시 줄은 안 셈). 같은 분 같은 그룹 줄은 한 줄. 최근 7일 = 집계 끝날 포함 7 달력 날 ∩ 기간.
    (2026-10-27 사용자 "전날 밤으로 표시") 00:00~00:09 멈춤 줄은 전날 몫(_stop_day — 전날이 기간 안일 때만): 목록 `M/D(요) 밤 · 기록 M/D HH:MM` · 최근 7일·범위도 그 날로 ·
    집계 끝날 다음 날 00:00~00:09 줄도 끝날 몫으로 센다.
    원장 사본 없음 · extras·history 꺼짐 · 기록 구간 없음 · 기록 구간 끝 < 집계 끝날 → {"상태": "없음", "사유"}(카드 멈춤 칸 '확인 못 함' — exit 0)."""
    import extras as X
    ex, warns = X.extras_config(cfg["report_fetch"])
    for w in warns:
        print(w, file=sys.stderr)
    if ex is None or not ex["history"]:
        return {"상태": "없음", "사유": "extras 설정 꺼짐"}
    if D is None:
        return {"상태": "없음", "사유": "원장 사본 인자 없음(compute --extra)"}
    led, cov = os.path.join(D, X.HISTORY_FILE), os.path.join(D, X.COVERED_FILE)
    if not os.path.exists(led) or not os.path.exists(cov):
        return {"상태": "없음", "사유": "원장 없음(첫 회·수집 실패)"}
    try:
        rows, spans = X.read_ledger(led), X.read_covered(cov)
        when = {r[0]: _when(r) for r in rows}
    except (X.ExtrasError, ValueError, OSError, IndexError) as e:
        return {"상태": "없음", "사유": f"원장 사본을 못 읽음({type(e).__name__})"}
    if not spans:
        return {"상태": "없음", "사유": "기록 구간 없음"}
    runs = []
    for a, e in sorted(spans):
        if runs and a <= runs[-1][1] + dt.timedelta(days=1):
            runs[-1][1] = max(runs[-1][1], e)
        else:
            runs.append([a, e])
    cs, ce = runs[-1]
    if ce < last:
        return {"상태": "없음", "사유": f"기록 구간 끝 {ce.month}/{ce.day} 이 집계 끝날 {last.month}/{last.day} 에 못 미침"}
    inside = [r for r in rows if cs <= when[r[0]].date() <= last]
    late = [r for r in rows if when[r[0]].date() == last + dt.timedelta(days=1) and when[r[0]].hour == 0 and when[r[0]].minute < STOP_LATE_MIN]
    owner = {}
    for label, _ in BUDGET_TYPES:
        for n in B[label].get("그룹이름", []):
            owner.setdefault(n, set()).add(label)
    per, warn = {label: [] for label, _ in BUDGET_TYPES}, []
    for r in inside + late:
        if r[2] != "시스템" or r[1] != STOP_KIND:
            continue
        g = r[5].split("\n")[0].strip()
        o = owner.get(g, set())
        if len(o) != 1:
            warn.append(f"멈춤 줄 {r[0]} 그룹 {g!r} 이 예산 읽기 그룹 이름과 {'안 맞음' if not o else '두 유형에 다 있음'} — 카드에 안 넣음")
            continue
        per[next(iter(o))].append(r)
    out = {"상태": "ok", "끝": f"{last.month}/{last.day}", "기록구간": f"{cs.month}/{cs.day}~{ce.month}/{ce.day}", "주의": warn}
    for label, _ in BUDGET_TYPES:
        e = B[label]
        if "캠페인이름" not in e:   # 캠페인 없음·확인 못 함 — 그 유형은 셀 수 없다
            out[label] = None
            continue
        names = set(e["그룹이름"])
        hit = lambda r: r[2] == "사람" and _budget_change(r[5]) and (
            r[3] == e["캠페인이름"] or (r[3] == "" and (r[4] in names or r[5].split("\n")[0].strip() in names | {e["캠페인이름"]})))
        ch = [when[r[0]] for r in inside if hit(r)]
        t0 = max(ch) if ch else None
        d0 = t0.date() if t0 else cs
        seen, ss = set(), []
        for r in sorted(per[label], key=lambda r: when[r[0]], reverse=True):
            k = (r[0], r[5].split("\n")[0].strip())
            if (t0 is not None and when[r[0]] <= t0) or k in seen:
                continue
            seen.add(k)
            ss.append(r)
        def amount(r):
            m = next((BUDGET_LINE.match(x.strip()) for x in r[5].split("\n") if BUDGET_LINE.match(x.strip())), None)
            return int(m.group(1).replace(",", "")) if m else None
        lo7 = last - dt.timedelta(days=6)
        day = [_stop_day(when[r[0]], d0) for r in ss]
        stamp = lambda t, d: _stamp(t) if d == t.date() else f"{d.month}/{d.day}({WD[d.weekday()]}) 밤 · 기록 {t.month}/{t.day} {t:%H:%M}"
        out[label] = {"시작": f"{d0.month}/{d0.day}", "시작종류": "변경" if t0 else "기록", "일수": (last - d0).days + 1, "횟수": len(ss),
                      "최근7일": sum(1 for d in day if d >= lo7),
                      "범위": [f"{day[-1].month}/{day[-1].day}", f"{day[0].month}/{day[0].day}"] if ss else None,
                      "줄": [{"일시": stamp(when[r[0]], d), "하루예산": amount(r)} for r, d in zip(ss, day)]}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("combined")
    ap.add_argument("--competitors-html")
    ap.add_argument("--balance", help="balance.py 의 잔액 기록(work/balance.json) — 판 F 광고비 잔액 카드 값(\"잔액\") · 판 L 하루예산 카드 값(\"예산\" — 멈춤은 --extra 원장 사본)을 낸다. 5단계·precheck 는 늘 붙인다")
    ap.add_argument("--leads", help="주간 성과 장부(저장소 밖 — precheck 는 config leads.path·환경 변수 SAERO_LEADS) → \"성과장부\"(판정 낱말만)")
    ap.add_argument("--place", help="플레이스 체크리스트(precheck 는 config place_checklist.path·SAERO_PLACE) → \"플레이스전후\"")
    ap.add_argument("--extra", help="추가 합본 폴더(work/extra — extras.py combine) → \"성별연령\"(05 아래 카드)·\"변경기록\"(04 아래 표). 판 G — 5단계·precheck 는 늘 붙인다(없거나 비면 [주의] · '확인 못 함')")
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
        out = compute(a.combined, cfg, comp_prev, bal, a.leads, a.place, prev_html, a.extra)
    except BalanceError as e:
        print(f"[FAIL] 잔액 기록: {e} ({a.balance})")
        sys.exit(1)
    except LeadsPublishError as e:
        print(f"[FAIL] 성과 장부: {e}")
        sys.exit(1)
    except SectionError as e:
        print(f"[FAIL] 직전 배포본 다음 액션 구역: {e} ({a.competitors_html})")
        sys.exit(1)
    text = json.dumps(out, ensure_ascii=False, indent=1, default=str)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[compute] {a.out}  {out['masthead']}  KPI {out['KPI']['노출']:,}/{out['KPI']['클릭']}/{out['KPI']['CTR']}%/{out['KPI']['광고비']:,}원"
              f"  경쟁사 {len(out['07']['경쟁사표'])}행(신규 변형 후보 {out['07']['신규변형후보']})"
              + ("" if "잔액" not in out else f"  잔액 {out['잔액']}")
              + ("" if "예산" not in out else f"  하루예산 {out['예산']['상태']}" + (
                  "" if out["예산"]["상태"] != "ok" else f"(플레이스 {out['예산']['플레이스'].get('한도', out['예산']['플레이스']['상태'])} · 멈춤 {out['예산']['멈춤']['상태']}"
                  + ("" if out["예산"]["멈춤"]["상태"] != "ok" or not out["예산"]["멈춤"].get("플레이스") else
                     f" {out['예산']['멈춤']['플레이스']['시작']} 뒤 {out['예산']['멈춤']['플레이스']['일수']}일 {out['예산']['멈춤']['플레이스']['횟수']}번") + ")"))
              + ("" if "성과장부" not in out else f"  장부 판정 {out['성과장부']['판정']}")
              + ("" if "성별연령" not in out else f"  성별·연령대 {out['성별연령']['상태']}"
                 + "".join(f"({t['종류']} {t.get('기간', t['상태'])})" for t in out['성별연령'].get('표', [])))
              + ("" if "변경기록" not in out else f"  변경 기록 {out['변경기록']['상태']}"
                 + (f"({out['변경기록']['기간']} · {out['변경기록']['표시']}/{out['변경기록']['건수']}줄)" if out['변경기록']['상태'] == "ok" else ""))
              + ("" if "플레이스전후" not in out else
                 f"  플레이스 11번 {[(x['id'], x['값']) for x in out['플레이스전후']['12번']]} 채팅 질문 {len(out['플레이스전후']['채팅질문'])}")
              + ("" if not out["01"]["콘텐츠재발"] else f"  콘텐츠 재발 {len(out['01']['콘텐츠재발'])}일"))
    else:
        print(text)


if __name__ == "__main__":
    main()
