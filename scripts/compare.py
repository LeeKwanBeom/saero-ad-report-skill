#!/usr/bin/env python3
"""index.html(배포본 또는 작업본)에서 11개 구역 값을 파싱해 compute.py JSON과 항목별 대조. 배포 전 차이 0이어야 한다.

사용법: "$PY" scripts/compare.py <index.html> <compute.json>   ($PY = 저장소 밖 venv 파이썬 — references/code-tab.md 1절)
- 표 값·차트 배열·각주·section-desc 숫자·11번 항목 수·금칙어까지 대조한다(2026-09-27 ad48222 기준 95항목 —
  09-26 99에서 잔존 문구 5항목을 validate.py 검사 21로 일원화하고 08 컴팩트를 집합+정렬 2항목으로 나눔).
- 동률 자리는 "직전 순서 유지" 관행이라 집합+정렬 방향으로 대조한다(경쟁사표·클릭1건·클릭0·08 컴팩트).
  HTML의 동률 순서는 직전 순서 유지가 정본이고 compute.py 출력의 동률 순서(클릭1건 2차 키 총비용↓ 등)는 참고다.
- 잔존 문구(확인 요청 등)는 여기서 보지 않는다 — validate.py 검사 21(`--pending`)이 유일한 자리.
- 마크업이 바뀌어 항목을 못 찾으면 [DIFF]로 나온다(조용히 통과하지 않음). 종료 코드 1 = 차이 있음.
- (2026-10-06) 구역별 try — 한 구역(masthead·KPI, 01~09, 10·11 — 판 H 까지 01~10, 11·12)에서 파싱이 실패하면 그 구역만 `파싱 실패 [구역]` [DIFF]로
  남기고 다음 구역을 계속 대조한다(옛 판은 첫 실패 뒤 나머지 항목을 전부 생략 — 01 해석 문단 삭제 프로브가 OK 17에서 멈춤).
  10번 나열 항목은 "최근 7일 노출은 …회, 클릭은 …건(M/D~M/D)" + "9/6 이후 N일 하루 평균 N건(N일 평균 N건)"으로 바뀜
  (항목 수 95 그대로 — 9/6 이후 나열 2항목·일수 1항목 → 최근 7일 2항목·일수/평균 1항목).
- (2026-10-06 회차 2 — 레이아웃 판 r2026-10-B) "03 일별 표 전체 행"은 03 구역의 두 표(위 = 합계 + 최근 날짜, 접힌 표 = 나머지)를
  DOM 순서대로 이어 읽어 거꾸로(`[::-1]`) compute 오름차순과 대조한다 — 최신 위가 정본, 오름차순으로 되돌린 판은 DIFF.
  summary(접기 머리) 4항목 신설: 07 클릭 1건 "(N개 · 펼치기)" · 클릭 0 "(노출 5회 이상 N개 · 펼치기)" · 경쟁사표 "표 N행" = compute 목록 길이,
  03 "이전 N일(M/D~M/D)" = 접힌 표의 행 수·첫/끝 날짜. 08 summary 의 "(N개 지역·클릭 M건)"은 기존 "08 컴팩트 개수·클릭"이 읽는다(구역 첫 일치).
  **항목 수 N = 99**(95 + summary 4).
- (2026-10-10 매출 작업 A·C) 구역 "12 장부·플레이스" 2항목 — 12번 `장부 기준 판정 = X` 리터럴 = compute `성과장부.판정`(precheck 가 --leads 를 넘긴 재계산 —
  낡은 판정이 본보기 복사로 배포되는 길을 막는다, 막음 A-F3) · 12번 플레이스 행 `플레이스 P<n> … — M/D까지 (상태|판정) = X` 의 (id, 종류, 값) 집합 = compute
  `플레이스전후.12번`. 리터럴이 없거나 compute 키가 없으면 그 구역만 [DIFF]. **항목 수 N = 101**.
- (2026-10-12 판 G 보고서 더 받기 A + B) `_s04` 는 04 구역 **첫 `<table>` 만** 읽는다(B-6 — 본 표·note 뒤에 계정 변경 기록 표가 붙는다). 판 G 블록(`<!-- saero:extra … -->`)이
  있으면 구역 "04·05 추가(판 G)": 04 변경 기록 머리(기간·최근 n건 / 전체) · 표 줄 · 스킬 줄(등록 n회·삭제 k건) = compute `변경기록` / 05 종류마다(성별·연령대) 머리(기간 ·
  알 수 없음 %) · 표 줄 = compute `성별연령` — compute 상태가 ok 가 아니면 그 자리 '확인 못 함' 1항목. **항목 수 N = 101 + 7**(둘 다 ok · 종류 2) — 확인 못 함이면 줄어든다.
- (2026-10-17 판 H 07 정식표 접기) "07 정식표 행수·값"은 그대로 "클릭 1건 검색어" 앞을 이어 읽는다(위 표 + 접힌 표 = 정식표 전 행 · 순서 대조). 07 구역 끝에 2항목:
  "07 정식표 위 표 행수 = min(K, n)"(07 구역 첫 tbody 의 행 수 · K = config `report_layout.top_rows_07`) · "07 summary 정식표 나머지(행·클릭 범위·합·비용) = compute 정식표[K:]"
  ("클릭 1건 검색어" 앞의 `나머지 N행(클릭 a~b건 · 합 M건 · X원) 펼치기` — 나머지가 없으면 `나머지 0행 펼치기`). 시안에서 summary 숫자를 틀리게 바꾼 사본이
  108/0 으로 조용히 통과하던 길을 막는다. **항목 수 N = 108 + 2 = 110**.
- (2026-10-23 판 I 콘텐츠 지면 빼기) 구역 "10"(지면 — A/B/C/D 표 · placementChart 노출·클릭 · 최근 7일 노출·클릭 나열 · 9/6 이후 평균 · desc · 파트너 마지막날 8항목)을
  뺀다(리포트 구역 없음 — compute "10" 은 서술 재료로만 남는다). 구역 "11·12" → "10·11"(10 핵심 요약 · 11 다음 액션 — 항목 이름·판정 줄 리터럴 `지난 회차 10번`) ·
  "12 장부·플레이스" → "11 장부·플레이스". 01: 표는 5칸(날짜·노출·클릭·CTR·CPC — `len(r) == 5` · "01 표 5일(5칸)") · 옛 3항목(검색지면 CTR · 검색지면 노출·클릭 ·
  콘텐츠 누적 노출) 대신 ③ 첫 문장 3항목: "01 ③ 누적 CTR" = compute `01.누적CTR` · "01 ③ 괄호(…)" = [콘텐츠첫날, 콘텐츠끝날, 콘텐츠누적노출, 검색지면.CTR]
  (콘텐츠 노출 합 0 이면 괄호 없음 = None) · "01 ③ 옛 구절 0"(콘텐츠 지면 없는 날 · 검색 지면만 계산하면 · 콘텐츠 노출 N회는 — 판 H 꼴이 복사돼 남으면 DIFF).
  **항목 수 N = 110 − 8 = 102**(판 G 둘 다 ok · 종류 2).
- (2026-10-23 판 J 불필요 항목 빼기 — 사용자 결정 "추천대로") KPI 보조 줄은 순번이 아니라 글로 찾는다(평균 클릭률 보조 줄이 빠져 넷 → 셋 · 클릭 단위 '건') ·
  04 새 2항목 "04 예산 비중 한 값(02 desc = 04 표 플레이스 행 · 04 회색 파워링크 = 100 − 그 값)"(결정 27 — 화면 세 자리를 서로 대조) · "04 격차 기준(…)"(04 민트 줄 그룹·CPC 둘 = 04 rows[1]·rows[0]) ·
  07 정식표 행에 '적음'(노출 config ctr_few_07 미만 — 클릭률 칸 '적음' · 강조 0, 결정 35 · 노출 쉼표 34) · 07 "확장·클릭0 행단위 3일"·"마지막날 개수" 2항목 삭제(결정 10 — ③ 뒷부분을 뺌) ·
  08 "확인불가" = 비용 비중 하나(결정 23) · "08 11위" 삭제(결정 11) · "08 각주 N회" 에 '비중 계산도 N 기준' 의 N(= 전체 — 08-note 가 고정 표지가 되어 숫자를 전부 읽는다) ·
  09 "심야 콜아웃" 새 꼴(`심야(22시~09시) 노출 N회(N%)·클릭 N건(N%)·비용 N원` — 결정 24) · "09 심야 클릭% (괄호)"·"09 최다" 삭제(콜아웃의 최다 구절을 뺌 — 최다는 "09 desc 최다") ·
  "09 2위" 에 동률 시간(`… N건으로 N시와 같음` — 09-call 이 고정 표지가 되어 숫자를 전부 읽는다) · 클릭 단위 '건'(09 desc·2위) ·
  판 G "04 변경 기록 스킬 줄" → "04 변경 기록 스킬 줄 0"(결정 7 — 줄이 남으면 DIFF) · 05 머리 알 수 없음 % 는 표에 그 줄이 없는 종류만(결정 8).
  **항목 수 N = 102 + 2 − 2 − 1 − 2 = 99**(판 G 둘 다 ok · 종류 2).
"""
import json
import re
import sys

from reportlib import load_config, read_html, section as _section

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — fetch_reports.py·exclusions.py와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

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
def _kpi():  # masthead·KPI
    cmp("masthead", grp(r"집계 기간<b>([^<]+)</b>", html).group(1).strip(), R["masthead"])
    cmp("og:description", grp(r'og:description" content="([^"]+)"', html).group(1), R["og"])
    kpi = S["kpi"] = dict(re.findall(r'<div class="label">([^<]+)</div>\s*<div class="value">([^<]+)<span', html)); sub = re.findall(r'<div class="sub">([^<]+)</div>', html)
    cmp("KPI 노출", num(kpi["총 노출수"]), R["KPI"]["노출"]); cmp("KPI 클릭", num(kpi["총 클릭수"]), R["KPI"]["클릭"])
    cmp("KPI CTR", float(kpi["평균 클릭률"]), R["KPI"]["CTR"]); cmp("KPI 광고비", num(kpi["총 광고비"]), R["KPI"]["광고비"])
    # 보조 줄은 글로 찾는다(판 J — 평균 클릭률 카드 보조 줄이 빠져 순번이 당겨짐 · 클릭 단위 '건'). 잔액 카드 보조 줄은 data-balance 라 안 잡힌다
    cmp("KPI sub 일평균노출", float(grp(r"([\d.]+)회", sub[0]).group(1)), R["KPI"]["일평균노출"]); cmp("KPI sub 일평균클릭", float(grp(r"일 평균 ([\d.]+)건", sub[1]).group(1)), R["KPI"]["일평균클릭"])
    cmp("KPI sub 클릭당", num(grp(r"([\d,]+)원", next(s for s in sub if s.startswith("클릭당 평균"))).group(1)), R["KPI"]["클릭당"])

# 01 ③ 첫 문장(판 I — 2026-10-23 사용자 승인 꼴): "→ 누적 CTR <b>N%</b>(M/D~M/D 콘텐츠 지면 노출 N회 포함 — 빼면 <b>N%</b>). 상향 뒤 …" · 콘텐츠 노출 합 0 이면 괄호 없이
# "→ 누적 CTR <b>N%</b>. 상향 뒤 …". 띄어쓰기 자리는 공백 여럿·줄바꿈도 받는다(폭에 맞춘 줄바꿈). 글자를 바꾸려면 사용자에게 다시 묻는다.
MINT01 = (r"→\s+누적\s+CTR\s+<b>([\d.]+)%</b>(?:\((\d+/\d+)~(\d+/\d+)\s+콘텐츠\s+지면\s+노출\s+([\d,]+)회\s+포함\s+—\s+빼면\s+<b>([\d.]+)%</b>\))?\.\s+상향\s+뒤")
OLD01 = ("콘텐츠 지면 없는 날", "검색 지면만 계산하면", "회는 9/6 이후")   # 판 H 까지의 ③ 구절(판 I 에서 0)


def _s01():  # 01 — 표 5행은 최신 위(2026-10-15) → DOM [::-1] = compute 표5 오름차순 · 순위 5칸은 오름차순 그대로 · 판 I(2026-10-23) 표 5칸 · ③ 첫 문장 괄호
    s1 = sec(1)
    cmp("01 dailyChart 노출", chart_data("dailyChart", "노출수"), R["01"]["노출"]); cmp("01 dailyChart 총비용", chart_data("dailyChart", "총비용\\(원\\)"), R["01"]["총비용"])
    lbl = re.findall(r"labels:\s*\[((?:'\d+/\d+\(.\)',?)+)\]", html)
    cmp("01/06 labels", [l.split(",")[0].strip("'") for l in lbl] + [len(l.split(",")) for l in lbl], [R["01"]["labels"][0]] * 2 + [R["nlabels"]] * 2)
    cmp("01 min-width", int(grp(r"min-width:\s*(\d+)px", s1).group(1)), R["minwidth"])
    t1 = [{"날짜": r[0], "노출": num(r[1]), "클릭": num(r[2]), "CTR": float(r[3].rstrip("%")), "CPC": num(r[4])} for r in rows(s1) if len(r) == 5][::-1]
    hl1 = re.findall(r'<td class="num( ctr-high)?">([\d.]+)%</td>', s1)[::-1]
    cmp("01 표 5일(5칸)", t1, [{k: v for k, v in r.items() if k != "hl"} for r in R["01"]["표5"]]); cmp("01 표 .ctr-high", [bool(h) for h, _ in hl1], [r["hl"] for r in R["01"]["표5"]])
    grid = re.findall(r'margin-bottom:2px;">([^<]+)</div>\s*<div style="font-size:15px;font-weight:800;(color:var\(--mint-dark\);)?">([\d.]+)위', s1)
    cmp("01 플레이스 순위 5칸", [{"날짜": d, "순위": float(v)} for d, _, v in grid], R["01"]["플레이스순위5"]); cmp("01 순위 민트 칸", [d for d, c, _ in grid if c], [R["01"]["순위민트"]])
    m = grp(r"하루 평균은 ([\d,]+)원·클릭 ([\d.]+)건·CPC ([\d,]+)원으로, 상향 전 9/1~9/16\(하루 평균 ([\d,]+)원·([\d.]+)건·CPC ([\d,]+)원\)", s1)
    cmp("01 상향후 평균", [num(m.group(1)), float(m.group(2)), num(m.group(3))], [R["01"]["상향후"]["광고비"], R["01"]["상향후"]["클릭"], R["01"]["상향후"]["CPC"]])
    cmp("01 상향전 평균", [num(m.group(4)), float(m.group(5)), num(m.group(6))], [R["01"]["상향전"]["광고비"], R["01"]["상향전"]["클릭"], R["01"]["상향전"]["CPC"]])
    cmp("01 누적 가중순위", float(grp(r"누적 가중평균은 [\d.]+ → ([\d.]+)위", s1).group(1)), R["01"]["플레이스누적가중순위"])
    # ③ 첫 문장(판 I) — 누적 CTR · 괄호 숫자 넷(기간 첫날·끝날 · 콘텐츠 노출 합 · 검색 지면만 CTR) = compute · 합 0 이면 괄호 없음 · 옛 세 구절 0
    m = grp(MINT01, s1)
    cmp("01 ③ 누적 CTR", float(m.group(1)), R["01"]["누적CTR"])
    got = None if m.group(2) is None else [m.group(2), m.group(3), num(m.group(4)), float(m.group(5))]
    want = None if not R["01"]["콘텐츠누적노출"] else [R["01"]["콘텐츠첫날"], R["01"]["콘텐츠끝날"], R["01"]["콘텐츠누적노출"], R["01"]["검색지면"]["CTR"]]
    cmp("01 ③ 괄호(콘텐츠 기간·노출 합·검색 지면만 CTR — 합 0 이면 괄호 없음)", got, want)
    cmp("01 ③ 옛 구절 0(콘텐츠 지면 없는 날·검색 지면만 계산하면·콘텐츠 노출 N회는)", [w for w in OLD01 if w in s1] + re.findall(r"콘텐츠 노출 [\d,]+회는", s1), [])

def _s02():  # 02
    cmp("02 desc 플레이스 비중", float(grp(r"예산의 ([\d.]+)%", sec(2)).group(1)), R["02"]["플레이스비중"])
    cmp("02 groupChart 노출", chart_data("groupChart", "노출수"), R["02"]["groupChart"]["노출"]); cmp("02 groupChart 클릭", chart_data("groupChart", "클릭수"), R["02"]["groupChart"]["클릭"])
    cmp("02 costPie", chart_data("costPie"), R["02"]["costPie"])

def _s03():  # 03 — 레이아웃 판 r2026-10-B: 위 표(합계 + 최근 날짜 최신 위) + 접힌 표(나머지 최신 위) → DOM 전체 [::-1] = 오름차순
    s3 = sec(3); r3 = rows(s3); body = [r for r in r3 if r[0] != "합계"]; tot = [r for r in r3 if r[0] == "합계"][0]
    def p3(r): return [num(r[1]), num(r[2]), None if r[3] == "–" else num(r[3])], [num(r[4]), num(r[5]), None if r[6] == "–" else num(r[6])], num(r[7])
    cmp("03 일별 표 전체 행", [{"날짜": r[0], "플레이스": p3(r)[0], "파워링크": p3(r)[1], "합계": p3(r)[2]} for r in body][::-1], R["03"]["rows"])
    cmp("03 합계 행", {"플레이스": p3(tot)[0], "파워링크": p3(tot)[1], "총": p3(tot)[2]}, R["03"]["합계"])
    cmp("03 desc 최고일", grp(r"최고치 (\S+) ([\d,]+)원", sec(3)).groups(), (R["03"]["최고일"], f"{R['03']['최고액']:,}"))
    # summary(접기 머리)는 구역 끝 — 형식이 깨져도 위 데이터 항목은 먼저 대조된다
    m = grp(r"<summary[^>]*>이전 (\d+)일(?:\((\d+/\d+)~(\d+/\d+)\))? 펼치기</summary>", s3); fold = [r[0].split("(")[0] for r in rows(s3[m.start():])]
    cmp("03 summary 이전 N일·기간 = 접힌 표", [int(m.group(1)), m.group(2), m.group(3)], [len(fold), fold[-1] if fold else None, fold[0] if fold else None])

def _s04():  # 04 — 본 표 = 04 구역 첫 <table> 만(B-6, 2026-10-12: 판 G 의 계정 변경 기록 표가 본 표·note 뒤에 붙는다)
    s4 = sec(4); t4 = s4[:s4.find("</table>") + len("</table>")] if "</table>" in s4 else s4
    got4 = [{"유형": r[0].replace(" 광고", ""), "그룹": re.split(r"\s*\(", r[1])[0].strip(), "노출": num(r[2]), "클릭": num(r[3]), "CTR": float(r[4].rstrip("%")),
             "총비용": num(r[5]), "CPC": num(r[6]), "순위": None if r[8] == "—" else float(r[8].rstrip("위")), "비중": float(r[7].rstrip("%"))} for r in rows(t4)]
    S["got4"] = got4
    cmp("04 표", got4, R["04"]["rows"]); cmp("04 CPC 격차 desc", float(grp(r"→ ([\d.]+)배", sec(4)).group(1)), R["04"]["CPC격차"])
    pw4 = float(grp(r"비중은 [\d.]+ → ([\d.]+)%", sec(4)).group(1))
    cmp("04 파워링크 비중", pw4, R["04"]["파워링크비중"])
    # 판 J(결정 27) — 같은 비중이 한 값: 02 desc = 04 표 플레이스 행 · 04 회색 파워링크 = 100 − 그 값(화면 세 자리끼리 — compute 정의가 다시 갈라져도 DIFF)
    pl4 = got4[0]["비중"] if got4 and got4[0]["유형"] == "플레이스" else None
    cmp("04 예산 비중 한 값(02 desc = 04 표 플레이스 행 · 04 회색 파워링크 = 100 − 그 값)",
        [float(grp(r"예산의 ([\d.]+)%", sec(2)).group(1)), pw4], [pl4, None if pl4 is None else round(100 - pl4, 1)])
    m = grp(r'격차 기준 = 파워링크 총비용 1위 "([^"]+)" CPC ([\d,]+)원 vs 플레이스 ([\d,]+)원', sec(4))   # 판 J(결정 21 (b)) — 04 민트 줄
    cmp("04 격차 기준(파워링크 총비용 1위 그룹·CPC · 플레이스 CPC)", [m.group(1), num(m.group(2)), num(m.group(3))],
        [R["04"]["rows"][1]["그룹"], R["04"]["rows"][1]["CPC"], R["04"]["rows"][0]["CPC"]])

def _s05():  # 05
    blk5 = html[html.find("getElementById('mediaChart')"):]
    lab5 = [re.sub(r"[\[\]']", "", x).replace(",", " ").strip() for x in re.findall(r"\[[^\]]*\]", grp(r"labels:\s*\[(.*?)\],\n", blk5, re.S).group(1))]
    norm = lambda m: m.replace(" - ", " ").replace("-", " ")
    cmp("05 mediaChart top5 라벨", lab5, [norm(t["매체"]) for t in R["05"]["top5"]]); cmp("05 mediaChart top5 값", chart_data("mediaChart", "노출수"), [t["노출"] for t in R["05"]["top5"]])
    col5 = grp(r"backgroundColor:\s*\[([^\]]*)\]", blk5).group(1).replace(" ", "").split(",")
    cmp("05 mediaChart 색", col5, ["mint" if t["유형"] == "플레이스" else "ink" for t in R["05"]["top5"]])
    cmp("05 deviceChart", chart_data("deviceChart"), R["05"]["device"]); cmp("05 desc 모바일 비중", float(grp(r"모바일이 노출의 ([\d.]+)%", sec(5)).group(1)), R["05"]["모바일비중"])

def _s06():  # 06
    s6 = sec(6); cmp("06 rankChart", chart_data("rankChart", "평균노출순위"), R["06"]["rankChart"]); cmp("06 min-width", int(grp(r"min-width:\s*(\d+)px", s6).group(1)), R["minwidth"])
    cmp("06 desc 노원역 순위", float(grp(r"평균 ([\d.]+)위", s6).group(1)), R["06"]["노원역순위"])
    r6 = rows(s6); cmp("06 직접 등록", {"노출": num(r6[0][1]), "클릭": num(r6[0][2]), "순위": float(r6[0][3].rstrip("위")), "총비용": num(r6[0][4])}, R["06"]["직접"])
    cmp("06 자동매칭", {"노출": num(r6[1][1]), "클릭": num(r6[1][2]), "순위": float(r6[1][3].rstrip("위")), "총비용": num(r6[1][4])}, R["06"]["자동"])
    cmp("06 마지막날 직접/자동", [int(x) for x in grp(r"직접 (\d+)·자동 (\d+)회", s6).groups()], [R["06"]["마지막날"]["직접"], R["06"]["마지막날"]["자동"]])
    cards = re.findall(r'color:var\(--ink-soft\);">(\S+) <span style="color:var\(--mint-dark\);font-weight:700;">\(([\d/]+) 등록, (\d+)일차\)</span></div>.*?font-weight:800;color:var\(--mint-dark\);">([\d.]+)위', s6, re.S)
    cmp("06 카드(그룹·등록일·일차·큰숫자)", {c[0]: {"순위": float(c[3]), "등록일": c[1], "일차": int(c[2])} for c in cards}, R["06"]["카드"])
    cmp("06 카드 큰 숫자 = 04 셀", {c[0]: float(c[3]) for c in cards}, {r["그룹"]: r["순위"] for r in S["got4"] if r["그룹"] in {c[0] for c in cards}})

ROW7 = r'<td class="name-cell">([^<]+)</td>\s*<td><span class="tag[^>]*>([^<]*)</span></td>\s*<td class="num">([\d,]+)</td>\s*<td class="num">(\d+)</td>\s*<td class="num( ctr-high)?">(?:([\d.]+)%|(적음))</td>\s*<td class="num">([\d,]+)원</td>\s*<td class="num">([\d,]+)원</td>'
SUM07 = r"<summary[^>]*>나머지 ([\d,]+)행(?:\(클릭 ([\d,]+)(?:~([\d,]+))?건 · 합 ([\d,]+)건 · ([\d,]+)원\))? 펼치기</summary>"


def _s07():  # 07 — 판 H(2026-10-17): 정식표 = 위 표(07 첫 tbody) + 접힌 표("나머지 N행" summary 뒤) — "클릭 1건 검색어" 앞을 이어 읽으면 전 행
    s7 = sec(7); main_html = s7[:s7.find("클릭 1건 검색어")]
    m7 = re.findall(ROW7, main_html)
    # 판 J(결정 35) — 노출 config ctr_few_07 미만 행은 클릭률 칸 '적음'(CTR 없음 · 강조 0) — compute 적음 과 대조
    got7 = [{"검색어": a, "매칭": b, "노출": num(c), "클릭": num(d), "CTR": float(f) if f else None, "hl": bool(e), "적음": bool(z), "CPC": num(g), "총비용": num(h)}
            for a, b, c, d, e, f, z, g, h in m7]
    want7 = [dict(r, 매칭=r["매칭"].replace("*동률", ""), CTR=None if r["적음"] else r["CTR"]) for r in R["07"]["정식표"]]
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
    # (판 J 결정 10 — ③ 뒷부분 "행 단위 확장·클릭 0 노출 …" 을 뺐다: 그 2항목 삭제. 남으면 validate "판 J 뺀 글 0" 이 FAIL)
    segc = s7[s7.find("경쟁사 브랜드명 검색어"):]
    mc = re.findall(r'<td class="name-cell">([^<]+)</td>\s*<td>[^<]*</td>\s*<td><span class="tag[^>]*>[^<]*</span></td>\s*<td class="num">(\d+)</td>\s*<td class="num">(\d+)</td>\s*<td class="num">([\d,]+)원</td>', segc)
    gc = [{"검색어": a, "노출": int(b), "클릭": int(c), "총비용": num(d)} for a, b, c, d in mc]
    cmp("07 경쟁사표(집합)", sorted(gc, key=lambda x: x["검색어"]), sorted(R["07"]["경쟁사표"], key=lambda x: x["검색어"]))
    cmp("07 경쟁사표 정렬(노출↓, 동률 클릭↓, 그 안은 직전 순서)", [(x["노출"], x["클릭"]) for x in gc] == sorted([(x["노출"], x["클릭"]) for x in gc], reverse=True), True)
    cmp("07 desc 상위2 비중", int(grp(r"클릭의 (\d+)% 차지", s7).group(1)), R["07"]["상위2비중"])
    cmp("07 클릭 합계(정식+1건+경쟁사)", num(S["kpi"]["총 클릭수"]), R["07"]["정식표클릭합"] + R["07"]["클릭1합"] + R["07"]["경쟁사클릭합"])
    print("      config 경쟁사명을 포함하는데 직전 표에 없는 검색어(신규 변형 후보):", R["07"]["신규변형후보"])
    # summary(접기 머리)는 구역 끝 — 형식이 깨져도 위 데이터 항목은 먼저 대조된다
    cmp("07 summary 클릭1건 개수", int(grp(r"클릭 1건 검색어 <span[^>]*>\((\d+)개 · 펼치기\)", s7).group(1)), len(R["07"]["클릭1"]))
    cmp("07 summary 클릭0 개수", int(grp(r"노출은 있으나 클릭 0건인 검색어 <span[^>]*>\(노출 5회 이상 (\d+)개 · 펼치기\)", s7).group(1)), len(R["07"]["클릭0목록"]))
    cmp("07 summary 경쟁사표 행수", int(grp(r"<summary[^>]*>표 (\d+)행 · 펼치기</summary>", segc).group(1)), len(R["07"]["경쟁사표"]))
    # 판 H 07 정식표 접기(2026-10-17) — 위 표 행 수 · 접힌 행 summary 숫자(apply 가 매 회차 쓴다 — 틀리면 DIFF, 시안의 summary 변조 사본은 108/0 이었다)
    k7 = int(load_config()["report_layout"]["top_rows_07"]); rest = R["07"]["정식표"][k7:]
    cmp("07 정식표 위 표 행수 = min(K, n)", len(re.findall(ROW7, s7[s7.find("<tbody>"):s7.find("</tbody>")])), min(k7, len(R["07"]["정식표"])))
    m = grp(SUM07, main_html)
    got = {"행": num(m.group(1))} if m.group(2) is None else {"행": num(m.group(1)), "클릭": [num(m.group(2)), num(m.group(3) or m.group(2))], "합": num(m.group(4)), "비용": num(m.group(5))}
    want = {"행": 0} if not rest else {"행": len(rest), "클릭": [min(r["클릭"] for r in rest), max(r["클릭"] for r in rest)], "합": sum(r["클릭"] for r in rest), "비용": sum(r["총비용"] for r in rest)}
    cmp("07 summary 정식표 나머지(행·클릭 범위·합·비용) = compute 정식표[K:]", got, want)

def _s08():  # 08
    s8 = sec(8)
    cmp("08 TOP10", [{"지역": r[0], "노출": num(r[1]), "클릭": num(r[2]), "총비용": num(r[3])} for r in rows(s8)], R["08"]["top10"])
    m = grp(r"\((\d+)개 지역·클릭 (\d+)건\)", s8); cmp("08 컴팩트 개수·클릭", [int(m.group(1)), int(m.group(2))], [R["08"]["컴팩트수"], R["08"]["컴팩트클릭"]])
    txt8 = grp(r'line-height:1\.9;">(.*?)</div>', s8[s8.find("TOP 10 외"):], re.S).group(1)
    c8 = [grp(r"(.+?)\(노출(\d+)·클릭(\d+)\)", x.strip()).groups() for x in txt8.split(" · ") if "노출" in x]
    def short(full):  # 08 컴팩트 목록 지역명 축약 규칙(report-structure.md 08번)
        return (full.replace("서울특별시 ", "").replace("경기도 ", "").replace("인천광역시 ", "인천 ").replace("광주광역시 ", "광주 ")
                .replace("전남광주통합특별시 ", "광주 ").replace("부산광역시 ", "부산 ").replace("경상북도 ", "").replace("세종특별자치시", "세종시"))
    got8 = [{"지역": a, "노출": int(b), "클릭": int(c)} for a, b, c in c8]
    cmp("08 컴팩트 목록(집합, 지역명 축약)", sorted(got8, key=lambda x: x["지역"]), sorted([{"지역": short(r["지역"]), "노출": r["노출"], "클릭": r["클릭"]} for r in R["08"]["컴팩트"]], key=lambda x: x["지역"]))
    cmp("08 컴팩트 정렬(클릭↓, 동률 노출↓, 그 안은 직전 순서)", [(x["클릭"], x["노출"]) for x in got8] == sorted([(x["클릭"], x["노출"]) for x in got8], reverse=True), True)
    m = grp(r"클릭 0인 (\d+)개 지역에서 노출 ([\d,]+)회", s8); cmp("08 클릭0 각주", {"개수": int(m.group(1)), "노출": num(m.group(2))}, R["08"]["클릭0"])
    m = grp(r"노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이.*?비중 계산도 ([\d,]+) 기준", s8, re.S)   # 판 J — 08-note 고정 표지: 분모 숫자까지 읽는다
    cmp("08 각주 N회", {"전체": num(m.group(1)), "KPI": num(m.group(2)), "차이": int(m.group(3)), "분모": num(m.group(4))}, dict(R["08"]["각주"], 분모=R["08"]["각주"]["전체"]))
    m = grp(r"노원구 단독으로 전체 노출의 (\d+)%·클릭의 (\d+)%", s8); cmp("08 노원 비중", {"노출%": int(m.group(1)), "클릭%": int(m.group(2))}, R["08"]["노원"])
    m = grp(r"노출 비중 (\d+)%·클릭 (\d+)%", s8); cmp("08 desc 타겟 비중", {"노출%": int(m.group(1)), "클릭%": int(m.group(2))}, {k: R["08"]["타겟"][k] for k in ("노출%", "클릭%")})
    cmp("08 확인불가 비용 비중", float(grp(r'확인불가["\']? 비용 비중 ([\d.]+)%', s8).group(1)), R["08"]["확인불가"]["비용%"])   # 판 J(결정 23) — 표에 없는 비용 비중 하나만
    m = grp(r"타겟 밖 서울\(노출 ([\d,]+)·클릭 (\d+)\)의 CTR ([\d.]+)%는 타겟 5개 구\(([\d.]+)%\)", s8)
    cmp("08 타겟 밖 서울", {"노출": num(m.group(1)), "클릭": int(m.group(2)), "CTR": float(m.group(3))}, R["08"]["타겟밖서울"]); cmp("08 타겟 CTR", float(m.group(4)), R["08"]["타겟"]["CTR"])
    cmp("08 서울·경기 밖 비용%", float(grp(r"비용 비중 5%는 [\d.]+ → ([\d.]+)%", s8).group(1)), R["08"]["서울경기밖비용%"])
    # (판 J 결정 11 — "11위 … 바로 아래" 문장을 뺐다: "08 11위" 항목 삭제. 남으면 validate "판 J 뺀 글 0" 이 FAIL)

def _s09():  # 09
    s9 = sec(9); cmp("09 hourlyChart 노출", chart_data("hourlyChart", "노출수"), R["09"]["노출"]); cmp("09 hourlyChart 클릭", chart_data("hourlyChart", "클릭수"), R["09"]["클릭"])
    # 판 J(결정 24·37) — 콜아웃 첫 문장 새 꼴 · 클릭 단위 '건' · 최다 구절은 머리 줄에만("09 desc 최다") · 09-desc·09-call 은 고정 표지(숫자를 전부 읽는다 — 동률 시간 포함)
    m = grp(r"심야\(22시~09시\) 노출 ([\d,]+)회\((\d+)%\)·클릭 (\d+)건\((\d+)%\)·비용 ([\d,]+)원", s9)
    cmp("09 심야 콜아웃", {"노출": num(m.group(1)), "클릭": int(m.group(3)), "비용": num(m.group(5)), "노출%": int(m.group(2)), "클릭%": int(m.group(4))}, R["09"]["심야"])
    m = grp(r"2위는 (\d+)시 (\d+)건(?:으로 ((?:\d+시·)*\d+시)와 같음)?", s9)
    cmp("09 2위(동률 시간 포함)", {"시": int(m.group(1)), "클릭": int(m.group(2)), "동률": [int(x) for x in re.findall(r"\d+", m.group(3) or "")]},
        {"시": R["09"]["2위"]["시"], "클릭": R["09"]["2위"]["클릭"], "동률": [x for x in R["09"]["2위"]["동률"] if x != R["09"]["2위"]["시"]]})
    cmp("09 desc 최다", [int(x) for x in grp(r"(\d+)시대 클릭 최다\((\d+)건\)", s9).groups()], [R["09"]["최다"]["시"], R["09"]["최다"]["클릭"]])
    m = grp(r"노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이", s9); cmp("09 각주 N회", {"전체": num(m.group(1)), "KPI": num(m.group(2)), "차이": int(m.group(3))}, R["09"]["각주"])

def _s11():  # 10·11 — 판 I(2026-10-23): 10 핵심 요약 · 11 다음 액션(판 H 까지 11·12 — 지면 구역 10 이 빠지며 당김). 함수 이름은 그대로
    s10, s11 = sec(10), sec(11); li = re.findall(r"<li>(.*?)</li>", s10, re.S)
    cmp("10 항목 수(본문 ≤8, 참고 ≤2)", [len([x for x in li if "(참고)" not in x[:30]]) <= 8, len([x for x in li if "(참고)" in x[:30]]) <= 2], [True, True])
    for w in ["필요", "시점", "할 것", "검토", "주째"]: cmp(f"10·11 금칙어 '{w}'", len(re.findall(w, re.sub(r"<[^>]+>", "", s10 + s11))), 0)
    cmp("10 판정 줄 유지+뒤집힘+소멸 = 직전 항목 수", (lambda m: int(m.group(2)) + int(m.group(3)) + int(m.group(4)) == int(m.group(1)))(grp(r"지난 회차 10번 (\d+)개 항목 판정: 유지 (\d+) · 뒤집힘 (\d+) · 근거 소멸 (\d+)", s10)), True)


PLACE_ROW = re.compile(r"플레이스 (P\d+) [^<]*? — [^<]*?(?<!\d)\d+/\d+까지 (상태|판정) = ([^<]+?)</b>")


def _s12g():  # 11 장부·플레이스(2026-10-10 매출 작업 A·C — 판 H 까지 12번). 함수 이름·compute 키 "12번"은 그대로
    s11 = sec(11)
    got = re.findall(r"장부 기준 판정 = ([^<]+?)</b>", s11)
    cmp("11 장부 기준 판정 = 성과장부.판정", got, [R["성과장부"]["판정"]])
    rows = sorted(PLACE_ROW.findall(s11))
    cmp("11 플레이스 행(id·상태/판정) = 플레이스전후.12번", rows, sorted((x["id"], x["종류"], x["값"]) for x in R["플레이스전후"]["12번"]))


def _plain(x): return re.sub(r"<[^>]+>", "", x).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").strip()
def _blk(key):
    a, b = html.find(f"<!-- saero:extra {key} -->"), html.find(f"<!-- /saero:extra {key} -->")
    if not -1 < a < b: raise ValueError(f"판 G 블록 {key} 표지 없음")
    return html[a:b]
def _trs(x): return [t for t in (tuple(_plain(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)) for tr in re.findall(r"<tr>(.*?)</tr>", x, re.S)) if t]


def _sx():  # 판 G(2026-10-12 보고서 더 받기 A + B) — 04 계정 변경 기록 · 05 성별·연령대 = compute "변경기록"·"성별연령"(precheck 가 --extra 를 넘긴 재계산)
    hb, gb = _blk("history"), _blk("gender-age")
    H = R.get("변경기록") or {"상태": "없음"}
    if H.get("상태") != "ok":
        cmp("04 변경 기록 '확인 못 함'(compute 상태 " + str(H.get("상태")) + ")", "확인 못 함 —" in hb, True)
    else:
        more = f" · 최근 {H['표시']}건 / {H['건수']}건" if H["건수"] > H["표시"] else ""
        cmp("04 변경 기록 머리(기간)", _plain(grp(r"계정 변경 기록\([^)]*\) <span[^>]*>\((.*?)\)</span>", hb).group(1)), f"{H['기간']} 기록{more}")
        cmp("04 변경 기록 표", _trs(hb), [(r["일시"], r["유형"], r["대상"], r["내용"] or "—") for r in H["rows"]])
        cmp("04 변경 기록 스킬 줄 0(판 J — 제외 검색어 현황은 07 ②)", "스킬 제외 검색어 등록" in _plain(hb), False)
    G = R.get("성별연령") or {"상태": "없음"}
    if G.get("상태") != "ok":
        cmp("05 성별·연령대 '확인 못 함'(compute 상태 " + str(G.get("상태")) + ")", ("확인 못 함 —" in gb) and gb.count('<div class="sub-head">') == 0, True)
        return
    parts = {}
    for seg in re.split(r'<div class="sub-head">', gb)[1:]:
        m = grp(r"([^<]+?) <span[^>]*>\((.*?)\)</span></div>", seg)
        parts[_plain(m.group(1))] = (_plain(m.group(2)), [t for t in _trs(seg)])
    for t in G["표"]:
        got = parts.get(t["종류"])
        if t.get("상태") != "ok":
            cmp(f"05 {t['종류']} '확인 못 함'", bool(got) and got[0].startswith("확인 못 함"), True)
            continue
        unk = "" if t.get("알수없음%") is None or t.get("알수없음줄") else f" · 알 수 없음 {t['알수없음%']:.1f}%"   # 판 J(결정 8) — 표에 그 줄이 있으면 괄호에 % 0
        cmp(f"05 {t['종류']} 머리(기간·알 수 없음)", got[0] if got else None, f"{t['기간']}{unk}")
        cmp(f"05 {t['종류']} 표", got[1] if got else None,
            [(r["구분"], f"{r['노출']:,}", f"{r['비중']:.1f}%", f"{r['클릭']:,}", "적음" if r["적음"] else f"{r['CTR']:.2f}%", f"{r['비용']:,}원") for r in t["rows"]])


S = {}  # 구역 사이에 넘기는 값(kpi → 07 · got4 → 06). 앞 구역이 실패해 없으면 뒤 구역의 그 항목이 KeyError → 그 구역 [DIFF]
SECTIONS = [("masthead·KPI", _kpi), ("01", _s01), ("02", _s02), ("03", _s03), ("04", _s04), ("05", _s05), ("06", _s06),
            ("07", _s07), ("08", _s08), ("09", _s09), ("10·11", _s11), ("11 장부·플레이스", _s12g)]   # 판 I — 지면 구역(옛 10) 없음
if "saero:extra" in html:  # 판 G 블록이 있는 판만(옛 판 대조는 항목 그대로)
    SECTIONS.append(("04·05 추가(판 G)", _sx))
for _label, _fn in SECTIONS:  # 구역별 try — 한 구역의 첫 파싱 실패가 다른 구역 항목을 생략시키지 않는다(2026-10-06, 탐색 프로브 r9: OK 17에서 멈춤)
    try:
        _fn()
    except Exception as e:  # noqa: BLE001 — 어떤 실패든 그 구역만 [DIFF]로 남기고 다음 구역으로
        diffs.append(f"파싱 실패 [{_label}] {type(e).__name__}: {e}"); print(f"  [DIFF] 파싱 실패 [{_label}] — 마크업이 바뀌었으면 compare.py를 고칠 것: {type(e).__name__}: {e}")
print(f"\n== 대조 결과: OK {n_ok} / DIFF {len(diffs)}")
for d in diffs: print("   DIFF:", d)
sys.exit(1 if diffs else 0)
