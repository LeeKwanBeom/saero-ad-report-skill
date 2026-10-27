#!/usr/bin/env python3
"""
새로필라테스 광고 리포트 배포 전 검증 — **compute.py와 독립된 검산**.

사용법:
    "$PY" scripts/validate.py <index.html> <키워드CSV> <검색어CSV> <시간대별CSV> <상세지역CSV>

설정값(제외그룹·CTR 기준·차트 폭 규칙·날짜축 섹션·경쟁사 목록)은 config/report-config.json에서 읽는다.
이 스크립트에 값을 직접 적지 않는다. reportlib.py와 공유하는 것은 읽기·제외그룹 필터·일수·섹션 자르기까지다 —
KPI 합·순위·정렬 같은 값 계산은 compute.py와 공유하지 않는다(같은 오류를 두 번 통과시키지 않기 위해, 2026-09-26).

확인 항목(출력의 [PASS]/[FAIL] 줄을 세어 개수를 확인한다 — 설정에 따라 늘고 준다):
  1. HTML 태그 짝 (div/table/tr/td/th/span/script 등)
  2. KPI 총클릭수 = 07번 정식표 + 클릭1건 목록 + 경쟁사표 합계
  3. 09번 시간대별 클릭 합계 = 키워드 보고서 제외 전 전체 클릭 합계
     (시간대별 보고서는 광고그룹 구분이 없어 OFF 그룹이 포함된 값이다)
  4. 07번 클릭률 기준 이상 행에만 .ctr-high가 적용됐는지 전수 대조 — (판 J 2026-10-23) 노출 config `ctr_few_07.min_imps` 미만 행은 클릭률 칸 '적음'(강조 0)이어야, 그 밖은 숫자
  5. 01번 표도 같은 규칙으로 전수 대조 (.ctr-high는 표 무관, 클릭률 전용)
  6. masthead 집계 기간 = CSV 일별 min~max·일수
  7. KPI 타일 4개(노출·클릭·클릭률·광고비) = CSV 계산값
  8. 04번 예산 비중 합계 = 100.0%
  9. 날짜축 차트 min-width = 날짜 수 × per_day_px (floor 적용)
     — 대상 섹션은 config chart_min_width.date_based_sections (현재 01·06번). 섹션마다 검사 1개.
 10. 날짜축 차트 x축 라벨 배열('M/D(요일)' 형태) 길이 = 날짜 수
 11. 섹션 주석 <!-- Section N: --> 1~N 존재 — N = config report_layout.markers.sections(판 I 2026-10-23 부터 11 · 판 H 까지 12) · 순서대로 하나씩 · 그 밖 번호 0
 12. 08·09번 각주의 "N회 차이" = 제외 전 전체 노출 − KPI 노출
 13. 상세지역 CSV 노출 합계 = 제외 전 전체 노출
 14. (2026-09-26 추가) 05번 mediaChart top5 = 키워드 CSV `매체이름` 노출 상위 5 — 라벨·값·순서·색(플레이스=mint/파워링크=ink)
     (판 J 2026-10-23 — 정의만 바꿈: config `media_chart` — `검색/콘텐츠 매체` == placement(검색) 행의 매체이름 노출 상위 top_n(4). 콘텐츠 매체 막대 0)
 15. (2026-09-26 추가) 06번 신규 키워드 카드 큰 숫자 = 04번 같은 그룹의 평균순위 셀
 16. (2026-09-26 추가) config `competitors` 이름을 포함하는 검색어(검색어 CSV)가 07번 경쟁사표 밖에 없는지 — 순방향만.
     표 안 이름이 config에 있는지(역방향)는 검사하지 않는다(어순이 다른 표기 변형이 있음)
 17. (2026-09-26 추가) 07번 경쟁사표 각 행의 노출·클릭 = 검색어 CSV 합계
 18. (2026-09-26 추가) 검색어 CSV 클릭 합계 = KPI 클릭 (종전 `참고` 출력을 FAIL로)
 19. (2026-09-26 추가) 10번(핵심 요약 — 판 H 까지 11번) 항목 수 ≤ 8 + (참고) ≤ 2, 판정 줄 "지난 회차 10번 N개 항목 판정: 유지+뒤집힘+근거 소멸 = 직전 항목 수"
     — (판 J) 판정 줄 앞 `M/D까지 ` = 키워드 CSV 집계 마지막 날(뒤집힘 0 회차끼리 바이트가 같아지지 않게 · 낡은 날짜 FAIL)
 20. (2026-09-26 추가) 10·11번 본문(<script> 앞까지) 금칙어(필요·시점·할 것·검토·주째) 0건 — 조치 문장은 11번(다음 액션) 몫
 21. (2026-09-26 추가, 09-27 범위 확장) 07번 각주(`class="note"`)·10·11번 본문(<script> 앞까지)의 잔존 문구
     (확인 요청·판단 요청·기다림·확인 중·대기) 0건. 잔존 문구 검사는 이 검사 하나뿐이다(compare.py에는 없음 — --pending 일원화).
     사용자 답을 기다리며 배포하는 회차(4c08ab3처럼 채팅 질문을 남긴 배포)는 `--pending`을 붙여 이 검사만 허용한다
     (건수는 그대로 출력). 답을 반영한 재배포에는 붙이지 않는다 — 기본은 엄격. 세 범위 중 하나라도 못 찾으면 0건 가드 FAIL.
 22. (2026-10-06 추가) "07 각주 세 자리(경쟁사 판정·제외 검색어·클릭 0 전체)" — 07번 `class="note"` 전부를 이어 붙인 글에
     ① `경쟁사 판정(` · ② `제외 검색어: … 등록 N개 · 확인 a/b · 실패 n` · ③ `클릭 0인 검색어 전체는 N개·노출 N회` 가 다 있고,
     ②의 b = 등록 수 × config `exclusions.targets` 수, a ≤ b. 같은 검사 안에서 클릭 0 목록 항목 ≥ 1(`click0_items`).
     하나라도 0건이면 FAIL(글을 줄인 뒤 옛 각주 형식으로 돌아가거나 자리가 빠지는 것을 막는다 — 기능 추가 회차 1).
     검사는 이름으로 부른다(번호는 출력 순서일 뿐 — 이 목록 번호와 다를 수 있다).
 23. (2026-10-06 추가) "레이아웃 판" — `<meta name="report-layout" content="…">` 가 정확히 하나이고 값 = config `report_layout.layout_id`,
     `<details` 수 = config `report_layout.markers.details`, details 마다 바로 안에 summary(짝 — summary 수 = details 수) — 판 G 추가 블록(표지 사이) 안 접기는
     빼고 센다(04 변경 기록 접기는 이전 줄이 있을 때만 생긴다 — 2026-10-15, 그 접기는 27 이 본다).
     meta 0건·details 0건이면 FAIL(옛 모양으로 조용히 되돌아가는 것을 막는다 — 기능 추가 회차 2, 사용자 결정 2026-10-06).
     (판 C, 2026-10-06 01 차트 회차 1) 같은 검사 안에서: 분기 표지 주석 `/* saero:mobile-branch 01 */`·`06` 각 정확히 1(합 = `markers.mobile_branch`) ·
     `matchMedia(` 는 `matchMedia('(max-width: ' + M.maxPx + 'px)')` 꼴 정확히 1건 · 분기 도우미 M 줄(`var M = {maxPx: …};`) 정확히 1건이고
     값 = config `report_layout.mobile`(max_px · print_max_height_px · row_px · pad_px) · 배포본 CSS `@media (max-width: Npx){` 정확히 1건이고 N = max_px
     (JS 분기 경계 = CSS 경계). 하나라도 0건·불일치면 FAIL(이름·검사 수는 그대로).
     (판 D, 2026-10-07 모바일 기간 접기) M 줄 꼴에 `recent: {"01": K, "06": K}` 가 붙고 값 = config `report_layout.mobile.recent_days` 까지 대조
     (recent 없는 판 C 꼴 M 줄은 0건 → FAIL). PASS 문구에 `최근 K/K`.
     (판 E, 2026-10-08 01 모바일 터치 날짜) 01 모바일 모양의 `interaction: {mode:'index', intersect:false, axis:'y'}` 정확히 1건(0건이면 터치한 줄과
     다른 날짜 팝업 — FAIL). PASS 문구 끝에 `01 터치 y`.
     (판 F, 2026-10-09 광고비 잔액 카드) 카드 표지 `data-balance="value"`·`"sub"` 각 config `markers.balance_card`(1) · `.kpi-row` 안(카드 넷 뒤 · 01 섹션 앞) ·
     CSS `.kpi-wide{grid-column:1 / -1;}` 1건. PASS 문구 끝에 `잔액 카드 1`.
     (판 H, 2026-10-17 07 정식표 접기) 코드 변경 없이 config `markers.details` 6 으로 센다(07 정식표 아래 접힌 표 하나 — PASS `r2026-10-H · details 6 · summary 짝 6 …`).
     07 정식표 행은 2·4 가 07 구역 전체(위 표 + 접힌 표)를 읽는다 — 위 표 행 수·접힌 행 summary 숫자는 compare 몫("07 정식표 위 표 행수"·"07 summary 정식표 나머지").
     (판 I, 2026-10-23 콘텐츠 지면 빼기) 같은 검사 안에서: 번호 배지 `<span class="section-num">NN</span>` = 01~markers.sections(11) 순서대로 · 다음 액션 주석
     `<!-- Section N: Action items -->` 이 마지막 구역(11) · 지면 구역 흔적 0(placementChart · 서술 표지 10-* · 제목 "검색 지면 vs 콘텐츠 지면") · `<canvas id=` 수 =
     markers.canvases(7) · 01 ① 칸 머리 5(날짜·노출·클릭·CTR·CPC). PASS 문구 끝에 `구역 11 · 캔버스 7 · ① 5칸`.
     (판 K, 2026-10-26 01 요일 카드) 캔버스 = markers.canvases 8 · config `markers.weekday_card`(1)가 있으면 요일 카드 표지 `data-weekday="card"`·`"sub"`·`<canvas id="weekdayChart">` 각 그 수 ·
     01 구역 안 dailyChart 캔버스 뒤 · ① 머리글 앞 · 차트 블록 `getElementById('weekdayChart')` 정확히 1 = 분기 도우미(`/* saero:mobile-helper`) 뒤 · labels 월~일(날짜 꼴 아님 — 10 이 세지 않는다).
     값(막대·클릭·보조 줄)은 compare "01 요일 카드(판 K)" 몫. PASS 문구 끝에 `구역 11 · 캔버스 8 · ① 5칸 · 판 J 고정 글 · 요일 카드 1`.
     (판 L, 2026-10-27 하루예산 카드) details = markers.details 7 · config `markers.budget_card`(1)가 있으면 표지 `data-budget="card|value|sub|fold|summary|list"` 각 그 수 ·
     `.kpi-row` 안 잔액 카드 바로 뒤(01 섹션 앞) · `.kpi-row` 마지막 자식 · 접기·목록이 카드 안 · 잔액 카드 표지는 그대로(카드 넷 뒤 다섯째). PASS 문구 끝에 `· 하루예산 카드 1`.
 24. (2026-10-09 추가) "광고비 잔액 카드 = 잔액 기록(balance.json)·며칠분" — `--balance <work/balance.json>`(balance.py 기록 — precheck 는 작업본 옆 파일)을
     직접 읽어(compute.py 와 계산 공유 0) 기록이 ok 면 카드 값 = ⌊bizmoney_raw⌋ 원(콤마 · 기록의 bizmoney 도 같은 값) · 보조 줄 = 읽은 시각 KST `M/D(요일) HH:MM 기준`
     + ` · 약 N일분`(N = ⌊원 × 창일수 ÷ 창합계⌋ — 창 = 키워드 CSV `일별` 달력 날짜로 마지막 날까지 7일(첫날 앞은 자름 · 행 없는 날 0원), 합계 = 제외 그룹 뺀 총비용,
     합계 0 이면 며칠분 없음) / fail 이면 값 `확인 못 함` · 보조 줄 `M/D(요일) HH:MM 조회 실패`. 읽은 날(KST)이 집계 마지막 날 이하(지난 회차 기록)·기록 없음·
     꼴 다름·카드 값/보조 줄 0건 또는 둘 이상이면 FAIL.
 24b. (2026-10-27 판 L 추가) "하루예산 카드 = 예산 기록(balance.json budget) · 원장 SYSTEM 줄" — `--balance` 기록의 "budget"(balance.py 가 읽은 캠페인·그룹 하루예산)과
     `--extra` 원장 사본(변경이력.csv · 변경이력_기록구간.csv)을 직접 읽어(compute.py 와 계산 공유 0) 값(플레이스 실제 한도 = 켜진 그룹 하나면 min(그룹, 캠페인) · 최근 7일 멈춘 수) ·
     보조 줄(파워링크 캠페인 값 · 켜진 그룹 값 · 멈춘 수) · summary(기간 시작 = 그 유형 마지막 하루예산 변경(사람) — 없으면 기록 구간 첫날 · 일수 · 멈춘 수 · 범위) · 목록(멈춘 줄 전부 최신 위 ·
     시각 · 설정 값 — 00:00~00:09 줄은 전날 몫 `M/D(요) 밤 · 기록 M/D HH:MM` · 최근 7일·범위도 그 날 · 끝날 다음 날 00:0x 줄은 끝날 몫(2026-10-27 사용자 "전날 밤으로 표시"))을 다시 센 글과 바이트까지 대조. 예산 기록 없음·fail = '확인 못 함' · 원장 사본 없음·기록 구간이 집계 끝날에 못 미침 = 멈춤 칸 '확인 못 함'.
     카드 표지가 하나씩이 아니거나·잔액 기록이 없거나·꼴이 다르거나·예산을 읽은 날 ≤ 집계 마지막 날이면 FAIL. config markers.budget_card 가 없는 판이면 검사 없음.

 25. (2026-10-10 매출 작업 A) "01·10·11 서술에 장부 라벨+숫자 0(공개 범위 verdict)" — 01·10·11(판 H 까지 01·11·12) 본문(<script> 앞까지, 태그·표지 뺀 글)에 config `leads.public_labels`
     (문의·체험·상담·등록·매출·네이버 경유 …) 바로 뒤 숫자가 0건(scripts/leads.py label_hits — '등록 N개'·'등록 N · verified'·'N행'·날짜는 제외 검색어·기록 문구라 안 셈).
     config `leads.publish` 가 verdict 가 아니면 FAIL(건수 공개는 설계 회차 몫). 장부 파일은 읽지 않는다(공개 글만 본다).
 26. (2026-10-10 매출 작업 A·C) "11번 장부·플레이스 행"(판 H 까지 12번) — 11번 표에 `장부 기준 판정 = X` 행이 정확히 1(X = config `leads.verdict_words` 낱말 또는 `판정 전(N/min_weeks주)`) ·
     장부 행·플레이스 행(`플레이스 P<n> `)마다 `M/D까지` = 키워드 CSV 집계 마지막 날(같은 주 다음 날 회차도 바이트가 달라 narrative 가 서술 미교체를 잡는다) ·
     플레이스 ✗ 행(`상태 = ✗`) ≤ config `place_checklist.items_in_12` · ✓ 아닌 행 ≤ config `place_checklist.max_open_rows_12`(11번 작성 기준 4 — 키 이름의 12 는 그대로). 11번 표 행 0 이면 FAIL.

 27. (2026-10-12 판 G 보고서 더 받기 A + B) "추가 카드·표(판 G — 성별·연령대 · 계정 변경 기록) = work/extra" — `--extra <work/extra>`(precheck 는 작업본 옆 extra/)의
     파일 유무가 카드 유무 기준(A-5): `<종류>.csv`(성별·연령대 합본)·`변경이력.csv`+`변경이력_기록구간.csv`(원장 사본)가 있으면 카드·표의 기간 표기·줄 값이 compute.py 와
     따로 다시 센 값과 같아야(성별·연령대 = 합본 머리 기간 · 노출·비중·클릭·클릭률(min_imps 미만 '적음')·비용 · 알 수 없음 % / 변경 기록 = 키워드 CSV 집계 기간 ∩ 기록 구간
     마지막 연속 구간 · 보일 주체 줄(같은 분은 한 줄 — 2026-10-12) 최신 위 max_rows · 내용 한 구 · 스킬 등록 n회(고유 분)·삭제 k건 · 펼친 표 = 맨 위 줄과 같은
     날짜 줄 전부, 나머지는 접기 하나 안 · summary "이전 N건(M/D~M/D) 펼치기"(이전 줄이 없으면 접기 0 — 2026-10-15)), 없으면 그 자리가 '확인 못 함'. show_system false 면 SYSTEM·하루예산 중단 0 ·
     배포본 전체 아이디 꼴 `:naver` 0. "레이아웃 판" 검사(23)에 판 G 표지(블록 여닫이 각 1 · 04 안 본 표 뒤 · 05 안) 대조가 붙는다.

 28. (2026-10-23 판 I 콘텐츠 지면 빼기) "화면 글 구역 번호(판 I — 없는 12번·지면 10번·옛 지면 글 0)" — 서술 표지 안 글(태그 뺀)의 구역 번호 참조
     (`NN번` — 앞이 숫자·글자가 아니고 뒤가 '째'·'출구'가 아닌 것 · `07·10번`·`01~07·10번` 묶음은 숫자마다)가 ① 1~markers.sections(11) 밖이면 FAIL(옛 다음 액션 12번 —
     `12번 1번`·`지난 회차 12번`·`(12번 행 없음)`) · ② 10번이 지면 구역을 가리키면 FAIL(같은 묶음에 07 — 옛 `KPI·01~07·10번에서 제외` · 앞뒤 30자 안에 지면·매체 설정·
     파트너 매체) · ③ 옛 지면 구역 글(`콘텐츠 지면 N일 연속 0` · `검색 지면 vs 콘텐츠 지면`)이 있으면 FAIL. 검색어 속 숫자(`노원역10번출구`)는 안 센다.
     복사된 서술 스크립트(판 H 꼴)가 옛 번호를 다시 쓰는 길을 막는다. 서술 표지 0개면 FAIL(0건 가드).

 29. (2026-10-23 판 J 불필요 항목 빼기 — 결정 5·30) "06번 카드 그룹 = 카드 규칙 · 04 신규 메모 = 등록 뒤 N일 미만만" — 키워드 CSV(제외 그룹 뺌)로 compute.py 와 따로:
     카드 그룹 = 노원역필라테스 밖 파워링크 그룹 중 최근 7일(날짜 7개) 노출 > 0 이고 (일차 < config group_cards.new_days 이거나 promotion_groups) — 화면 카드 그룹 집합과 같아야 ·
     04 이름 칸 `(M/D 신규)` 가 붙은 그룹은 일차 < new_days 여야. 카드 0건이면 15 가 FAIL(0건 가드는 15).
 30. (판 J) "판 J 뺀 글 0(…)" — 판 J 가 뺀 서술 글(01 누적 CTR A → B · 01 닷새 나열·'~어려워 보임' · 03 '그대로'·마지막 날 · 04 격차 되풀이·예산 비중·'회차부터'·회색 숫자 ·
     06 '회차 연속'·매칭 숫자·카드 'N일차 · 평균순위' · 07 ③ 지난 회차·행 단위 · 08 '모두 표시됨'·11위·지난 회차·확인불가 숫자 · 09 '회차 연속'·'전략과 부합'·'최다 클릭 시간대는'·지난 회차·클릭 '회' ·
     10 순위 방향·상향 유지·클릭 1건 목록·(참고) 경쟁사·클릭 0·누적 CTR·판정 되풀이·변화 없음 숫자·제외 검색어(07 ② 에 실패·재노출이 없는 날) ·
     11 registry·'다시 묻지 않음'·'채팅으로 알림'·정렬·경쟁사·신규 없음 사유·'조용히 사라진 항목'·체크리스트 9항목)이 그 구역에 다시 나오면 FAIL — 옛 서술 스크립트를 복사해
     뺀 글이 돌아와도 다른 검사는 통과하던 길을 막는다. 구역 하나라도 0자면 FAIL(0건 가드).
     (판 J — "레이아웃 판"(23) 에) 판 J 가 뺀 고정 글(masthead '주간' · KPI '업종 평균 수준' · groupChart '4개 키워드 합산' · 04-foot·07-src·12-desc·12-basis 옛 글) 0 · KPI 총 클릭수 단위 '건' 하나 ·
     고정 표지 04-foot·07-src·12-desc = 판 J 글 · 07-legend 끝 '노출 N회 미만은 '적음''·12-basis 클릭률 강조 줄 = config 숫자 · 서술 표지 03-desc·08-note·09-desc·09-call = 고정. PASS 끝 `· 판 J 고정 글`.

사용법(옵션): "$PY" scripts/validate.py ... [--pending] [--balance <work/balance.json>] [--extra <work/extra>]   ($PY = 저장소 밖 venv 파이썬 — references/code-tab.md 1절)

검사 대상 셀이 0건이면 PASS가 아니라 FAIL이다. 마크업이 바뀌어 정규식이
안 맞는데 조용히 통과하는 것을 막기 위한 것이다.

하나라도 FAIL이면 배포하지 말고 원인을 고친 뒤 다시 실행할 것.
종료 코드: 0=전부 통과, 1=실패 있음
"""

import csv
import datetime as dt
import io
import json
import math
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — fetch_reports.py·exclusions.py와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

try:
    import pandas as pd  # noqa: F401  (reportlib이 필요로 함)
except ImportError:
    sys.exit("pandas가 필요합니다 — Code 탭은 저장소 밖 venv 파이썬(PY)으로 실행한다(references/code-tab.md 1절)")

from reportlib import exclude_groups, load_config, parse_days, read_csv, read_html, section
from leads import label_hits  # 공개 범위 가드 규칙(라벨+숫자) — leads.py guard 와 같은 규칙(값 계산 아님)

CFG = load_config()
EXCLUDED_GROUPS = CFG["excluded_groups"]
CTR_HIGH = float(CFG["ctr_high_threshold"])
PER_DAY_PX = int(CFG["chart_min_width"]["per_day_px"])
FLOOR_PX = int(CFG["chart_min_width"]["floor_px"])
DATE_SECTIONS = [int(n) for n in CFG["chart_min_width"]["date_based_sections"]]
COMPETITORS = list(CFG["competitors"])
FORBIDDEN = ["필요", "시점", "할 것", "검토", "주째"]          # report-structure.md 10번(판 H 까지 11번) 수동 검사
RESIDUAL = ["확인 요청", "판단 요청", "기다림", "확인 중", "대기"]  # 채팅 후속 뒤 남기면 안 되는 문구

TAGS = ["div", "table", "tr", "td", "th", "thead", "tbody",
        "ul", "li", "span", "script", "style", "details", "summary"]  # details·summary: 2026-10-06(접기 모양 회차 2 선반영)
N_TARGETS = len(CFG["exclusions"]["targets"])  # 07 각주 ② 확인 a/b 의 b = 등록 수 × 대상 그룹 수
FEW07 = int(CFG["ctr_few_07"]["min_imps"])     # 판 J — 07 정식표 노출 이 값 미만은 클릭률 '적음'(05 의 min_imps 와 따로)
LAYOUT = CFG["report_layout"]  # 레이아웃 판(2026-10-06 회차 2 · 판 C 01 차트 회차 1 · 판 D 모바일 기간 접기 2026-10-07) — layout_id · markers.details·mobile_branch · mobile

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
    """07번 정식 표의 (검색어, 노출, 클릭, ctr적용여부, CTR값 — 판 J '적음' 칸이면 None)."""
    pat = re.compile(
        r'<td class="name-cell">([^<]+)</td>\s*'
        r'<td><span class="tag[^>]*>[^<]*</span></td>\s*'
        r'<td class="num">([\d,]+)</td>\s*'
        r'<td class="num">(\d+)</td>\s*'
        r'<td class="num([^"]*)">(?:([\d.]+)%|(적음))</td>'
    )
    return [{"kw": m.group(1).strip(), "imps": int(m.group(2).replace(",", "")), "clicks": int(m.group(3)), "has_hl": "ctr-high" in m.group(4),
             "ctr": float(m.group(5)) if m.group(5) else None, "few": bool(m.group(6))} for m in pat.finditer(s7)]


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
    """11. 구역 주석 <!-- Section N: --> = 1~markers.sections 순서대로 하나씩(그 밖 번호 0 — 판 I 2026-10-23: 지면 구역이 빠져 11개, 판 H 까지 12개)."""
    n = int(LAYOUT["markers"]["sections"])
    found = [int(x) for x in re.findall(r"<!-- Section (\d+):", html)]
    missing = [k for k in range(1, n + 1) if k not in found]
    check(f"섹션 주석 1~{n} 존재(순서 · 그 밖 번호 0)", found == list(range(1, n + 1)),
          "전부 있음" if found == list(range(1, n + 1)) else f"주석 {found} — 누락 {missing} · 밖 {[k for k in found if not 1 <= k <= n]}")


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


MEDIA = CFG["media_chart"]   # 판 J(2026-10-23 결정 1) — 막대 = 검색 지면 매체 상위 top_n
MEDIA_NAME = f"05번 mediaChart = CSV {MEDIA['placement']} 지면 매체 상위 {int(MEDIA['top_n'])}(라벨·값·순서·색)"


def check_media_top5(html, kw_inc):
    """14. 05번 mediaChart 라벨·값·순서·색 = 키워드 CSV 매체이름 노출 상위(판 J — `검색/콘텐츠 매체` == media_chart.placement 행만 · top_n 개)."""
    i = html.find("getElementById('mediaChart')")
    blk = html[i:i + 3000] if i != -1 else ""
    lab = re.search(r"labels:\s*\[(.*?)\],\n", blk, re.S)
    dat = re.search(r"label:\s*'노출수'[^\n]*\n\s*data:\s*\[([^\]]*)\]", blk)
    col = re.search(r"backgroundColor:\s*\[([^\]]*)\]", blk)
    if not (lab and dat and col):
        check(MEDIA_NAME, False, "mediaChart 라벨/데이터/색 배열을 못 찾음 — 스크립트 마크업 변경 의심")
        return
    labels = [re.sub(r"[\[\]']", "", x).replace(",", " ").strip() for x in re.findall(r"\[[^\]]*\]", lab.group(1))]
    values = [int(x) for x in dat.group(1).split(",")]
    colors = col.group(1).replace(" ", "").split(",")
    sel = kw_inc[kw_inc["검색/콘텐츠 매체"] == MEDIA["placement"]]
    top = sel.groupby("매체이름")["노출수"].sum().sort_values(ascending=False).head(int(MEDIA["top_n"]))
    kind = sel.groupby("매체이름")["캠페인"].agg(lambda s: "mint" if s.str.startswith("플레이스").all() else "ink")
    want = [(m.replace(" - ", " ").replace("-", " "), int(v), kind[m]) for m, v in top.items()]
    got = list(zip(labels, values, colors))
    check(MEDIA_NAME, got == want,
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


GC = CFG["group_cards"]
CARD_RE = re.compile(r'color:var\(--ink-soft\);">(\S+) <span style="color:var\(--mint-dark\);font-weight:700;">\([\d/]+ 등록, \d+일차\)</span></div>')


def check_card_rule(html, kw, kw_inc):
    """29. (판 J 결정 5·30) 06 카드 그룹 = 규칙(compute 와 따로 — 키워드 CSV) · 04 '(M/D 신규)' 메모 = 일차 < new_days 그룹만."""
    name = f"06번 카드 그룹 = 카드 규칙 · 04 신규 메모 = 등록 뒤 {int(GC['new_days'])}일 미만만"
    pw = kw_inc[~kw_inc["캠페인"].astype(str).str.startswith("플레이스")]
    dates = sorted(kw["일별"].astype(str).unique())   # 날짜 = 키워드 보고서 전체(compute day_list 와 같은 정의 — 계산은 따로)
    if pw.empty or not dates:
        check(name, False, "파워링크 행 0건 — 키워드 CSV 확인")
        return
    day = lambda s: dt.date(*(int(x) for x in s.rstrip(".").split(".")))
    last, last7 = day(dates[-1]), set(dates[-7:])
    nth = {g: (last - day(min(s["일별"].astype(str)))).days + 1 for g, s in pw.groupby("광고그룹")}
    exp7 = {g: int(s[s["일별"].astype(str).isin(last7)]["노출수"].sum()) for g, s in pw.groupby("광고그룹")}
    want = sorted(g for g in nth if g != "노원역필라테스" and exp7[g] > 0 and (nth[g] < int(GC["new_days"]) or g in GC["promotion_groups"]))
    got = sorted(CARD_RE.findall(section(html, 6)))
    tagged = re.findall(r'<td class="name-cell">([^<]+?)\s*<span[^>]*>\(\d+/\d+ 신규\)</span>', section(html, 4))
    bad = []
    if got != want:
        bad.append(f"06 카드 {got} ≠ 규칙 {want}(최근 7일 노출 · 일차 < {GC['new_days']} 또는 승격 그룹 {GC['promotion_groups']})")
    old = [f"{g.strip()}({nth.get(g.strip(), '?')}일차)" for g in tagged if nth.get(g.strip(), 0) >= int(GC["new_days"])]
    if old:
        bad.append(f"04 '(M/D 신규)' 가 등록 {GC['new_days']}일 넘은 그룹에 {old}")
    check(name, not bad, "; ".join(bad) if bad else f"카드 {got} · 04 신규 메모 {len(tagged)}개 · 그룹 일차 {dict(sorted(nth.items()))}")


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


def check_11_12(html, pending=False, dmax=None):
    """19~21. 10번 항목 수·판정 줄, 10·11번 본문 금칙어, 07 각주·10·11 잔존 문구(--pending이면 허용).
    판 I(2026-10-23 — 지면 구역이 빠져 핵심 요약 10 · 다음 액션 11, 판 H 까지 11·12). 함수 이름은 그대로(내부 이름)."""
    s11, s12 = section(html, 10), section(html, 11)   # 변수 이름은 옛 번호 그대로 — s11 = 핵심 요약(10번) · s12 = 다음 액션(11번)
    notes7 = re.findall(r'<(?:p|div)[^>]*class="note"[^>]*>(.*?)</(?:p|div)>', section(html, 7), re.S)
    li = re.findall(r"<li>(.*?)</li>", s11, re.S)
    m = re.search(r"지난 회차 10번 (\d+)개 항목 판정: 유지 (\d+) · 뒤집힘 (\d+) · 근거 소멸 (\d+)", s11)
    if not li or not m:
        check("10번 항목 수·판정 줄", False, f"<li> {len(li)}개, 판정 줄 {'있음' if m else '없음'} — 마크업 변경 의심")
    else:
        n_main = len([x for x in li if "(참고)" not in x[:30]])
        n_ref = len([x for x in li if "(참고)" in x[:30]])
        prev, keep, flip, gone = (int(x) for x in m.groups())
        bad = []
        if n_main > 8: bad.append(f"본문 {n_main}개 > 8")
        if n_ref > 2: bad.append(f"(참고) {n_ref}개 > 2")
        if keep + flip + gone != prev: bad.append(f"판정 줄 {keep}+{flip}+{gone} ≠ {prev}")
        md = re.search(r"(\d+/\d+)까지 지난 회차 10번 \d+개 항목 판정:", s11)   # 판 J — 판정 줄 앞 M/D까지 = 집계 끝(G1)
        want_md = f"{dmax.month}/{dmax.day}" if dmax is not None else None
        if want_md and (not md or md.group(1) != want_md): bad.append(f"판정 줄 앞 'M/D까지' {md.group(1) if md else '없음'} ≠ 집계 끝 {want_md}")
        check("10번 항목 수·판정 줄", not bad, f"본문 {n_main} + (참고) {n_ref}, 판정 {prev} = {keep}+{flip}+{gone}" + (f" · {want_md}까지" if want_md and not bad else "")
              + (f" — {'; '.join(bad)}" if bad else ""))
    text = re.sub(r"<[^>]+>", "", s11 + s12)
    if not text.strip():
        check("10·11번 금칙어 0건", False, "10·11번 본문 0자 — 섹션 주석 또는 마크업 변경 의심")
        check("07 각주·10·11번 잔존 문구 0건", False, "10·11번 본문 0자")
        return
    hits = {w: len(re.findall(w, text)) for w in FORBIDDEN}
    bad = [f"{w} {n}건" for w, n in hits.items() if n]
    check("10·11번 금칙어 0건", not bad, f"{len(hits)}종 검사, {len(text):,}자" + (f" — {', '.join(bad)}" if bad else ""))
    text7 = re.sub(r"<[^>]+>", "", " ".join(notes7))
    if not notes7 or not s11.strip() or not s12.strip():
        check("07 각주·10·11번 잔존 문구 0건", False, f"07 각주 {len(notes7)}개 / 10번 {len(s11)}자 / 11번 {len(s12)}자 — 범위를 못 찾음, 마크업 변경 의심")
        return
    hits7 = {w: len(re.findall(w, text7)) for w in RESIDUAL}
    hits = {w: len(re.findall(w, text)) for w in RESIDUAL}
    bad = [f"{w} {n}건" for w, n in ((w, hits7[w] + hits[w]) for w in RESIDUAL) if n]
    detail = f"{len(RESIDUAL)}종 검사 — 07 각주 {sum(hits7.values())}건 + 10·11번 {sum(hits.values())}건"
    if bad and pending:
        check("07 각주·10·11번 잔존 문구 0건", True, f"--pending: 사용자 답 대기 배포라 허용 — {detail}: {', '.join(bad)} (답을 반영한 재배포에선 0건이어야 함)")
    else:
        check("07 각주·10·11번 잔존 문구 0건", not bad, detail + (f": {', '.join(bad)}" if bad else ""))


def check_07_footnotes(s7):
    """22. 07 각주 세 자리(① 경쟁사 판정 · ② 제외 검색어 등록/확인/실패 · ③ 클릭 0 전체) + 클릭 0 목록 ≥ 1."""
    name = "07 각주 세 자리(경쟁사 판정·제외 검색어·클릭 0 전체)"
    notes7 = re.findall(r'<(?:p|div)[^>]*class="note"[^>]*>(.*?)</(?:p|div)>', s7, re.S)
    t = re.sub(r"<[^>]+>", "", " ".join(notes7))
    n1 = len(re.findall(r"경쟁사 판정\(", t))
    m2 = re.findall(r"제외 검색어: .*?등록 (\d+)개 · 확인 (\d+)/(\d+) · 실패 (\d+)", t)
    m3 = re.findall(r"클릭 0인 검색어 전체는 (\d+)개·노출 ([\d,]+)회", t)
    n0 = len(click0_items(s7))
    bad = []
    if not notes7: bad.append('07 class="note" 0개 — 섹션 주석 또는 마크업 변경 의심')
    if n1 == 0: bad.append("① 경쟁사 판정( 0건")
    if not m2:
        bad.append("② 제외 검색어: … 등록 N개 · 확인 a/b · 실패 n 0건")
    else:
        reg, a, b, _ = (int(x) for x in m2[0])
        if b != reg * N_TARGETS: bad.append(f"② 확인 {a}/{b}의 {b} ≠ 등록 {reg} × 대상 {N_TARGETS}그룹")
        if a > b: bad.append(f"② 확인 {a}/{b} — a > b")
    if not m3: bad.append("③ 클릭 0인 검색어 전체는 N개·노출 N회 0건")
    if n0 == 0: bad.append("클릭 0 목록 항목 0건(노출은 있으나 클릭 0건인 … 목록)")
    check(name, not bad, "; ".join(bad) if bad else
          f"① {n1}건 · ② 등록 {m2[0][0]}개 확인 {m2[0][1]}/{m2[0][2]} 실패 {m2[0][3]} · ③ {m3[0][0]}개 · 클릭 0 목록 {n0}개")


def check_layout(html):
    """23. 레이아웃 판 = config report_layout(meta 값 · details 수 · details/summary 짝 · 판 C 분기 표지·M 줄·matchMedia·CSS 경계 · 판 D M 줄 recent ·
    판 E 01 모바일 터치 축). 0건이면 FAIL."""
    name = "레이아웃 판(meta report-layout = config · 접기 details 수·짝)"
    metas = re.findall(r'<meta name="report-layout" content="([^"]*)">', html)
    out = re.sub(r"<!-- saero:extra (\S+) -->.*?<!-- /saero:extra \1 -->", "", html, flags=re.S)   # 판 G 추가 블록 안 접기는 빼고(2026-10-15 — 27 이 본다)
    n_det = len(re.findall(r"<details(?:\s[^>]*)?>", out))
    n_sum = len(re.findall(r"<summary(?:\s[^>]*)?>", out))
    n_pair = len(re.findall(r"<details(?:\s[^>]*)?>\s*<summary(?:\s[^>]*)?>", out))
    want = int(LAYOUT["markers"]["details"])
    bad = []
    if not metas: bad.append('<meta name="report-layout"> 0건 — 옛 모양이거나 표지를 잃음(apply.py --layout)')
    elif len(metas) > 1: bad.append(f"meta {len(metas)}개")
    elif metas[0] != LAYOUT["layout_id"]: bad.append(f"meta {metas[0]!r} ≠ config {LAYOUT['layout_id']!r}")
    if n_det == 0: bad.append("details 0건 — 접기가 없어짐")
    elif n_det != want: bad.append(f"details {n_det}개 ≠ config {want}")
    if n_sum != n_det or n_pair != n_det: bad.append(f"details/summary 짝 어긋남(details {n_det} · summary {n_sum} · 바로 안 summary {n_pair})")
    # 판 C(2026-10-06 — 01·06 모바일 가로 막대): 분기 표지 주석 01·06 각 1(합 = markers.mobile_branch) · matchMedia 는 M.maxPx 꼴 하나뿐 ·
    # 분기 도우미 M 줄 하나 = config mobile · 배포본 CSS 모바일 경계 @media (max-width: Npx) 하나 = config max_px(JS 경계 = CSS 경계)
    mob, want_br = LAYOUT["mobile"], int(LAYOUT["markers"]["mobile_branch"])
    n01, n06 = (len(re.findall(rf"/\* saero:mobile-branch {k} \*/", html)) for k in ("01", "06"))
    if n01 != 1 or n06 != 1 or n01 + n06 != want_br: bad.append(f"분기 표지 01 {n01}개 · 06 {n06}개(합 {n01 + n06}) ≠ config {want_br}(각 1)")
    n_mm = len(re.findall(r"matchMedia\(", html))
    n_mm_ok = len(re.findall(r"matchMedia\('\(max-width: ' \+ M\.maxPx \+ 'px\)'\)", html))
    if n_mm != 1 or n_mm_ok != 1: bad.append(f"matchMedia {n_mm}건(그중 M.maxPx 꼴 {n_mm_ok}) ≠ 1")
    # 판 D(2026-10-07 — 모바일 기간 접기): M 줄에 recent(모바일 처음 그리는 최근 일수 01·06) = config mobile.recent_days
    ml = re.findall(r'var M = \{maxPx: (\d+), printMaxH: (\d+), row: \{"01": (\d+), "06": (\d+)\}, pad: \{"01": (\d+), "06": (\d+)\}, '
                    r'recent: \{"01": (\d+), "06": (\d+)\}\};', html)
    want_m = (int(mob["max_px"]), int(mob["print_max_height_px"]), int(mob["row_px"]["01"]), int(mob["row_px"]["06"]), int(mob["pad_px"]["01"]), int(mob["pad_px"]["06"]),
              int(mob["recent_days"]["01"]), int(mob["recent_days"]["06"]))
    if len(ml) != 1: bad.append(f"M 줄(var M = {{maxPx… recent…}}) {len(ml)}건 ≠ 1")
    elif tuple(int(x) for x in ml[0]) != want_m: bad.append(f"M 줄 {tuple(int(x) for x in ml[0])} ≠ config mobile {want_m}(maxPx·printMaxH·row 01·06·pad 01·06·recent 01·06)")
    css = [int(x) for x in re.findall(r"@media\s*\(max-width:\s*(\d+)px\)\s*\{", html)]
    if len(css) != 1 or css[0] != want_m[0]: bad.append(f"CSS @media (max-width: Npx) {css} ≠ config max_px [{want_m[0]}](정확히 1건)")
    # 판 E(2026-10-08 — 01 모바일 터치 날짜): 01 모바일 모양(indexAxis 'y' 가로 막대)의 interaction 에 axis:'y' 정확히 1건 —
    # 빠지면 Chart.js index 모드가 가로 거리로 골라 터치한 줄과 다른 날짜 팝업이 뜬다
    n_ty = len(re.findall(r"interaction:\s*\{mode:'index', intersect:false, axis:'y'\}", html))
    if n_ty != 1: bad.append(f"01 모바일 터치 축 interaction axis:'y' {n_ty}건 ≠ 1 — apply.py --layout 으로 판 E")
    # 판 F(2026-10-09 — 광고비 잔액 카드): 값·보조 줄 표지 각 markers.balance_card · .kpi-row 안(넷째 카드 "클릭당 평균" 뒤 · 01 섹션 앞) · .kpi-wide CSS 한 줄
    want_bc = int(LAYOUT["markers"].get("balance_card", 0))
    nv, ns = html.count('data-balance="value"'), html.count('data-balance="sub"')
    kr, iv, s1 = html.find('<div class="kpi-row">'), html.find('data-balance="value"'), html.find("<!-- Section 1:")
    if nv != want_bc or ns != want_bc: bad.append(f"잔액 카드 표지 값 {nv} · 보조 줄 {ns} ≠ config {want_bc} — apply.py --layout 으로 판 F")
    elif want_bc and not (-1 < kr < html.rfind("클릭당 평균", 0, iv) < iv < s1): bad.append("잔액 카드가 .kpi-row 안 넷째 카드 뒤(01 섹션 앞)가 아님")
    n_kw = html.count(".kpi-wide{grid-column:1 / -1;}")
    if want_bc and n_kw != 1: bad.append(f"CSS .kpi-wide{{grid-column:1 / -1;}} {n_kw}건 ≠ 1(잔액 카드 한 줄 전체)")
    # 판 G(2026-10-12 — 보고서 더 받기 A + B): 04 변경 기록·05 성별·연령대 블록 표지 각 1(여닫이 짝) · 합 = markers.extra_blocks · 04 블록은 04 안 본 표 뒤 · 05 블록은 05 안
    want_eb = int(LAYOUT["markers"].get("extra_blocks", 0))
    if want_eb:
        n_open = [html.count(f"<!-- saero:extra {k} -->") for k in ("history", "gender-age")]
        n_close = [html.count(f"<!-- /saero:extra {k} -->") for k in ("history", "gender-age")]
        if n_open != [1, 1] or n_close != [1, 1] or sum(n_open) != want_eb:
            bad.append(f"추가 블록 표지 여는 {n_open} · 닫는 {n_close} ≠ 각 1(config extra_blocks {want_eb}) — apply.py --layout 으로 판 G")
        else:
            s4, s5 = section(html, 4), section(html, 5)
            if not (-1 < s4.find("</table>") < s4.find("<!-- saero:extra history -->") < s4.find("<!-- /saero:extra history -->")):
                bad.append("변경 기록 블록이 04 구역 안 본 표 뒤가 아님")
            if not (-1 < s5.find("<!-- saero:extra gender-age -->") < s5.find("<!-- /saero:extra gender-age -->")):
                bad.append("성별·연령대 블록이 05 구역 안이 아님")
    # 판 I(2026-10-23 — 콘텐츠 지면 빼기): 번호 배지 = 01~markers.sections 순서대로 · 마지막 구역 = 다음 액션(Action items) · 지면 구역 흔적 0
    # (placementChart · 서술 표지 10-* · 제목 "검색 지면 vs 콘텐츠 지면") · 캔버스 = markers.canvases · 01 ① 칸 머리 5(날짜·노출·클릭·CTR·CPC) — 구역 주석은 11 이 본다
    want_sec, want_cv = int(LAYOUT["markers"]["sections"]), int(LAYOUT["markers"]["canvases"])
    badges = re.findall(r'<span class="section-num">(\d+)</span>', html)
    if badges != [f"{k:02d}" for k in range(1, want_sec + 1)]: bad.append(f"번호 배지 {badges} ≠ 01~{want_sec:02d}")
    act = re.findall(r"<!-- Section (\d+): Action items -->", html)
    if act != [str(want_sec)]: bad.append(f"다음 액션(Action items) 주석 {act} ≠ 마지막 구역 {want_sec}")
    n_pl, n_m10, n_t10 = html.count("placementChart"), html.count("<!-- n:10-"), html.count("검색 지면 vs 콘텐츠 지면")
    if n_pl or n_m10 or n_t10: bad.append(f"지면 구역 흔적 placementChart {n_pl} · 표지 10-* {n_m10} · 제목 {n_t10} — apply.py --layout 으로 판 I")
    cv = re.findall(r'<canvas id="([^"]+)"', html)
    if len(cv) != want_cv: bad.append(f"캔버스 {len(cv)}개 ≠ config markers.canvases {want_cv}")
    s1 = section(html, 1)
    th1 = re.search(r"<thead>(.*?)</thead>", s1[s1.find("① 일별 지표"):], re.S) if "① 일별 지표" in s1 else None
    n_th1 = len(re.findall(r"<th[\s>]", th1.group(1))) if th1 else 0
    if n_th1 != 5 or "<th class=\"num\">콘텐츠</th>" in s1: bad.append(f"01 ① 칸 머리 {n_th1}개 ≠ 5(날짜·노출·클릭·CTR·CPC)")
    # 판 K(2026-10-26 — 01 요일 카드): 표지 card·sub·캔버스 각 markers.weekday_card · 01 안 차트 카드 뒤 · ① 앞 · 차트 블록 하나 = 분기 도우미 뒤 · labels 월~일 — apply check_weekday 와 따로 쓴 같은 규칙
    want_wc = int(LAYOUT["markers"].get("weekday_card", 0))
    if want_wc:
        n_wc = [html.count('data-weekday="card"'), html.count('data-weekday="sub"'), html.count('<canvas id="weekdayChart">')]
        wjs, hp = html.count("getElementById('weekdayChart')"), html.find("/* saero:mobile-helper")
        wb = html[html.find("getElementById('weekdayChart')"):] if wjs else ""
        wb = wb[:wb.find("</script>")]
        if n_wc != [want_wc] * 3: bad.append(f"요일 카드 표지 card·sub·캔버스 {n_wc} ≠ 각 config weekday_card {want_wc} — apply.py --layout 으로 판 K")
        elif not (-1 < s1.find('<canvas id="dailyChart">') < s1.find('data-weekday="card"') < s1.find("① 일별 지표")): bad.append("요일 카드가 01 구역 안 차트 카드 뒤 · ① 앞이 아님")
        if wjs != 1 or not -1 < hp < html.find("getElementById('weekdayChart')"): bad.append(f"요일 차트 블록 {wjs}개(분기 도우미 뒤 하나여야)")
        elif re.sub(r"\s+", "", (re.search(r"labels:\s*\[([^\]]*)\]", wb) or [None, ""])[1]) != "'월','화','수','목','금','토','일'": bad.append("요일 차트 labels 가 월~일이 아님")
    # 판 L(2026-10-27 — 하루예산 카드): 표지 각 markers.budget_card · .kpi-row 안 잔액 카드 바로 뒤 · .kpi-row 마지막 자식 · 접기·목록 카드 안 — apply check_budget 과 따로 쓴 같은 규칙
    want_bd = int(LAYOUT["markers"].get("budget_card", 0))
    if want_bd:
        n_bd = [html.count(f'data-budget="{k}"') for k in ("card", "value", "sub", "fold", "summary", "list")]
        bc, p1 = html.find('data-budget="card"'), html.find("<!-- Section 1:")   # s1 은 위에서 01 구역 글로 다시 쓰였다 — 위치는 따로
        ls = html.rfind("\n", 0, bc) + 1
        ce = html.find("\n    </div>\n", bc)
        if n_bd != [want_bd] * 6: bad.append(f"하루예산 카드 표지 card·value·sub·fold·summary·list {n_bd} ≠ 각 config budget_card {want_bd} — apply.py --layout 으로 판 L")
        elif not (-1 < kr < iv < bc < p1): bad.append("하루예산 카드가 .kpi-row 안 잔액 카드 뒤(01 섹션 앞)가 아님")
        elif not re.search(r'data-balance="sub">[^<\n]*</div>\n    </div>\n\Z', html[max(0, ls - 400):ls]): bad.append("하루예산 카드 바로 앞이 잔액 카드가 아님")
        elif ce == -1 or not html.startswith("\n    </div>\n  </div>\n", ce) or html[ce + len("\n    </div>\n  </div>\n"):p1].strip():
            bad.append("하루예산 카드가 .kpi-row 마지막 자식(바로 뒤 01 섹션)이 아님")
        elif not (ls < html.find('data-budget="fold"') < html.find('data-budget="list"') < ce) or html.count("<details", ls, ce) != 1:
            bad.append("하루예산 카드 접기·목록이 카드 안 하나가 아님")
    # 판 J(2026-10-23 오후 — 불필요 항목 빼기): 뺀 고정 글 0 · KPI 총 클릭수 '건' · 고정 표지 새 글(config 숫자) · 네 표지 고정 — apply check_trim 과 따로 쓴 같은 규칙
    bad += check_trim_fixed(html)
    check(name, not bad, "; ".join(bad) if bad else
          f"{metas[0]} · details {n_det} · summary 짝 {n_pair} · 분기 {n01 + n06} · M {ml[0][0]}/{ml[0][1]} · 최근 {ml[0][6]}/{ml[0][7]} · CSS {css[0]} · 01 터치 y"
          + (f" · 잔액 카드 {nv}" if want_bc else "") + (f" · 추가 블록 {want_eb}" if want_eb else "") + f" · 구역 {want_sec} · 캔버스 {len(cv)} · ① 5칸 · 판 J 고정 글"
          + (f" · 요일 카드 {want_wc}" if want_wc else "") + (f" · 하루예산 카드 {want_bd}" if want_bd else ""))


J_FIXED_GONE = ("주간 리포트", "업종 평균 수준", "(4개 키워드 합산)", "평균순위는 파워링크 전용 지표", "900~1,300원대는 플레이스", "지난 회차 항목 이월 판정 +",
                "최근 30일까지만 내려줘", "<b>타겟 지역</b>", "인 행만 진한 민트색")
J_FIXED = {"04-foot": "※ 평균순위 칸은 파워링크 그룹만 — 플레이스 순위는 01번 ②",
           "07-src": '네이버 검색어 보고서는 광고 유형을 구분하지 않습니다. 매칭이 "확장"인 행은 파워링크 자동매칭(CPC 대개 600원 이하), "일치" 행은 대부분 플레이스(CPC 1,000원 이상)입니다.',
           "12-desc": "다음 조치 · 비용 영향 큰 순"}
J_TO_FIXED = ("03-desc", "08-note", "09-desc", "09-call")


def _marker_body(html, nm):
    m = re.findall(r"<!-- n:" + re.escape(nm) + r":(매회차|고정) -->(.*?)<!-- /n -->", html, re.S)
    return m


def check_trim_fixed(html):
    """판 J 고정 글(레이아웃 판 검사 안) — 어긋남 목록. 표지가 없으면 그 자리 0건이라 FAIL(0건 가드)."""
    bad = []
    gone = [w for w in J_FIXED_GONE if w in html]
    if gone: bad.append(f"판 J 가 뺀 고정 글 {gone}")
    n_clk = len(re.findall(r'<div class="label">총 클릭수</div>\s*<div class="value">[\d,]+<span class="unit">건</span></div>\s*<div class="sub">일 평균 [\d.]+건</div>', html))
    if n_clk != 1: bad.append(f"KPI 총 클릭수 단위 '건'(값·일 평균) {n_clk}곳 ≠ 1")
    for nm, want in J_FIXED.items():
        m = _marker_body(html, nm)
        if len(m) != 1 or m[0][1] != want: bad.append(f"고정 표지 {nm} ≠ 판 J 글({len(m)}개{' · ' + m[0][1][:30] if m else ''})")
    tail = f" · 노출 {FEW07}회 미만은 '적음'"
    m = _marker_body(html, "07-legend")
    if len(m) != 1 or not m[0][1].endswith(tail): bad.append(f"07-legend 끝 {tail!r} 아님(config ctr_few_07)")
    ctr = f"· <b>클릭률 강조</b>: 01·07번 표의 클릭률 {CTR_HIGH:g}% 이상 칸은 진한 민트색(07번 노출 {FEW07}회 미만 행은 '적음')"
    m = _marker_body(html, "12-basis")
    if len(m) != 1 or ctr not in m[0][1]: bad.append("12-basis 클릭률 강조 줄 ≠ config(ctr_high_threshold · ctr_few_07)")
    kinds = {nm: [k for k, _ in _marker_body(html, nm)] for nm in J_TO_FIXED}
    off = {nm: k for nm, k in kinds.items() if k != ["고정"]}
    if off: bad.append(f"서술 표지 {off} ≠ 고정(판 J — compare 가 숫자를 전부 읽는 표지)")
    return bad


KST = dt.timezone(dt.timedelta(hours=9))
YOIL = "월화수목금토일"


def check_balance_card(html, kw, bal_path):
    """24. 판 F 광고비 잔액 카드 = 잔액 기록(balance.py 의 balance.json)·며칠분 — compute.py 와 계산 공유 0(제외 그룹 필터·일수만 reportlib).
    카드 값·보조 줄 표지가 하나씩이 아니거나·기록이 없거나·꼴이 다르거나·지난 회차 기록(읽은 날 ≤ 집계 마지막 날)이면 FAIL."""
    name = "광고비 잔액 카드 = 잔액 기록(balance.json)·며칠분"
    vals = re.findall(r'<div class="value" data-balance="value">(.*?)</div>', html)
    subs = re.findall(r'<div class="sub" data-balance="sub">([^<]*)</div>', html)
    if len(vals) != 1 or len(subs) != 1:
        check(name, False, f"카드 값 {len(vals)}건 · 보조 줄 {len(subs)}건 ≠ 1 — 카드가 없거나 마크업 변경 의심(apply.py --layout 판 F)")
        return
    if not bal_path:
        check(name, False, "잔액 기록 인자 없음 — validate.py … --balance work/balance.json(precheck 는 작업본 옆 balance.json 을 넘긴다)")
        return
    try:
        with open(bal_path, encoding="utf-8") as f:
            rec = json.load(f)
        st, ra = rec["status"], rec["read_at"]
        t = dt.datetime.fromisoformat(ra.replace("Z", "+00:00"))
        if st not in ("ok", "fail") or t.tzinfo is None:
            raise ValueError(f"status {st!r} · read_at {ra!r}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        check(name, False, f"잔액 기록을 못 읽음·꼴 다름({type(e).__name__}: {str(e)[:80]}): {bal_path}")
        return
    k = t.astimezone(KST)
    dmin, dmax, _ = parse_days(kw)
    stamp = f"{k.month}/{k.day}({YOIL[k.weekday()]}) {k.hour:02d}:{k.minute:02d}"
    bad = []
    if k.date() <= dmax.date():
        bad.append(f"읽은 날 {k.date()}(KST) ≤ 집계 마지막 날 {dmax.date()} — 지난 회차 잔액 기록(balance.py 를 이번 회차에)")
    if st == "fail":
        want_v, want_s, extra = "확인 못 함", f"{stamp} 조회 실패", "기록 fail"
    else:
        raw, won = rec.get("bizmoney_raw"), rec.get("bizmoney")
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(raw) or raw < 0:
            check(name, False, f"잔액 기록 꼴 다름(bizmoney_raw {raw!r}): {bal_path}")
            return
        floor_won = int(math.floor(raw))
        if won != floor_won or isinstance(won, bool):
            bad.append(f"기록 bizmoney {won!r} ≠ ⌊bizmoney_raw {raw!r}⌋ {floor_won}")
        inc = exclude_groups(kw, CFG)
        window = []
        for i in range(7):  # 마지막 날부터 거꾸로 달력 7일 — 첫날 앞은 자른다(행 없는 날도 창에 들어간다 = 0원)
            day = dmax - dt.timedelta(days=i)
            if day < dmin:
                break
            window.append(day.strftime("%Y.%m.%d."))
        spend = int(inc[inc["일별"].astype(str).isin(window)]["총비용"].sum())
        want_v = f'{floor_won:,}<span class="unit">원</span>'
        want_s = f"{stamp} 기준" + (f" · 약 {floor_won * len(window) // spend:,}일분" if spend > 0 else "")
        extra = f"기록 ok ⌊{raw}⌋ · 창 {len(window)}일 총비용 {spend:,}원"
    if vals[0] != want_v:
        bad.append(f"값 화면 {vals[0]!r} ≠ 기대 {want_v!r}")
    if subs[0] != want_s:
        bad.append(f"보조 줄 화면 {subs[0]!r} ≠ 기대 {want_s!r}")
    check(name, not bad, "; ".join(bad) if bad else f"{re.sub(r'<[^>]+>', '', vals[0])} · {subs[0]} ({extra} · 읽은 시각 {ra})")


def _bud_lim(x):
    """예산 기록 캠페인·그룹 한 칸 → 한도(원) · 하루예산을 안 쓰면 None(제한 없음)."""
    return x["dailyBudget"] if x["useDailyBudget"] else None


def _bud_won(v):
    return "제한 없음" if v is None else f"{v:,}원"


def _bud_groups(vals):
    if not vals:
        return "켜진 그룹 없음"
    k = sorted(v for v in vals if v is not None)
    if not k:
        return "그룹 제한 없음"
    if len(k) != len(vals):
        return f"그룹 {k[0]:,}원~제한 없음"
    return f"그룹마다 {k[0]:,}원" if k[0] == k[-1] else f"그룹 {k[0]:,}~{k[-1]:,}원"


def _bud_expect(budget, extra_dir, dmax):
    """24b 기대 글 (값 글, 보조 줄, summary(None = '멈춤 기록 확인 못 함' 로 시작), 목록 [(시각, 설정 값)]) — compute.py 와 따로 센다."""
    import extras as X
    camps = budget["campaigns"]
    kinds = {"플레이스": "PLACE", "파워링크": "WEB_SITE"}
    T = {}
    for lab, tp in kinds.items():
        cs = [c for c in camps if c["type"] == tp]
        if len(cs) > 1:
            cs = [c for c in cs if not c["userLock"]] if len([c for c in cs if not c["userLock"]]) == 1 else cs
        if not cs:
            T[lab] = ("캠페인 없음", None)
        elif len(cs) > 1:
            T[lab] = ("확인 못 함", None)
        else:
            T[lab] = ("꺼짐" if cs[0]["userLock"] else "ok", cs[0])
    # 멈춤 — 원장 사본(csv 로 직접)
    stops, why = None, None
    ex, _ = X.extras_config(CFG["report_fetch"])
    led = os.path.join(extra_dir, X.HISTORY_FILE) if extra_dir else None
    cov = os.path.join(extra_dir, X.COVERED_FILE) if extra_dir else None
    if not ex or not ex.get("history"):
        why = "extras 꺼짐"
    elif not led or not os.path.exists(led) or not os.path.exists(cov):
        why = "원장 사본 없음"
    else:
        with open(cov, encoding="utf-8-sig", newline="") as f:
            got = [r for r in csv.reader(f)][1:]
        days = set()
        for r in got:
            if r:
                a, b = dt.date.fromisoformat(r[0]), dt.date.fromisoformat(r[1])
                while a <= b:
                    days.add(a)
                    a += dt.timedelta(days=1)
        end = max(days) if days else None
        if end is None or end < dmax.date():
            why = "기록 구간이 집계 끝날에 못 미침"
        else:
            start = end
            while start - dt.timedelta(days=1) in days:
                start -= dt.timedelta(days=1)
            with open(led, encoding="utf-8-sig", newline="") as f:
                lrows = [r for r in csv.reader(f)][1:]
            ts = lambda r: dt.datetime(int(r[0][:4]), int(r[0][5:7]), int(r[0][8:10]), int(r[0][12:14]), int(r[0][15:17]))
            inside = [r for r in lrows if r and start <= ts(r).date() <= dmax.date()]
            # 2026-10-27 사용자 "전날 밤으로 표시": 00:00~00:09 멈춤 = 전날 몫(전날이 기간 안일 때) — 집계 끝날 다음 날 00:0x 줄도 끝날 몫
            late = [r for r in lrows if r and ts(r).date() == dmax.date() + dt.timedelta(days=1) and ts(r).hour == 0 and ts(r).minute < 10]
            names ={lab: ({g["name"] for g in c["groups"]} if c else set()) for lab, (_, c) in T.items()}
            stops = {}
            for lab, (st, c) in T.items():
                if c is None:
                    stops[lab] = None
                    continue
                def changed(r):
                    seg = r[5].split("\n")
                    if r[2] != "사람" or "변경 전" not in seg or "변경 후" not in seg:
                        return False
                    i, j = seg.index("변경 전"), seg.index("변경 후")
                    pick = lambda xs: {x.split(":", 1)[0].strip(): x.split(":", 1)[1].strip() for x in xs if x.startswith("하루예산") and ":" in x}
                    b, a = pick(seg[i + 1:j]), pick(seg[j + 1:])
                    if j < i or not (a or b) or a == b:
                        return False
                    return r[3] == c["name"] or (r[3] == "" and (r[4] in names[lab] or seg[0].strip() in names[lab] | {c["name"]}))
                marks = [ts(r) for r in inside if changed(r)]
                t0 = max(marks) if marks else None
                d0 = t0.date() if t0 else start
                mine = [r for r in inside + late if r[2] == "시스템" and r[1] == "광고그룹 하루예산 중단"
                        and r[5].split("\n")[0].strip() in names[lab] and sum(r[5].split("\n")[0].strip() in v for v in names.values()) == 1
                        and (t0 is None or ts(r) > t0)]
                uniq = sorted({(ts(r), r[5].split("\n")[0].strip()): r for r in mine}.items(), key=lambda kv: kv[0][0], reverse=True)
                out, sday = [], []
                for (t, _), r in uniq:
                    m = [re.fullmatch(r"하루예산:\s*([\d,]+)원", x.strip()) for x in r[5].split("\n")]
                    m = next((x for x in m if x), None)
                    prev = t.date() - dt.timedelta(days=1)
                    d = prev if (t.hour, t.minute) < (0, 10) and prev >= d0 else t.date()
                    sday.append(d)
                    when_txt = (f"{t.month}/{t.day}({YOIL[t.weekday()]}) {t.hour:02d}:{t.minute:02d}" if d == t.date()
                                else f"{d.month}/{d.day}({YOIL[d.weekday()]}) 밤 · 기록 {t.month}/{t.day} {t.hour:02d}:{t.minute:02d}")
                    out.append((when_txt, f"하루예산 {m.group(1)}원" if m else "하루예산 —"))
                lo7 = dmax.date() - dt.timedelta(days=6)
                stops[lab] = {"d0": d0, "kind": "변경" if t0 else "기록", "n": len(out), "n7": sum(1 for d in sday if d >= lo7),
                              "rows": out, "days": (dmax.date() - d0).days + 1, "first": sday[-1] if sday else None, "last": sday[0] if sday else None}
    pst, pc = T["플레이스"]
    sp = stops.get("플레이스") if stops else None
    sw = stops.get("파워링크") if stops else None
    if pst != "ok":
        head = f"플레이스 {pst}"
    else:
        on = [g for g in pc["groups"] if not g["userLock"]]
        if len(on) == 1:
            k = [v for v in (_bud_lim(pc), _bud_lim(on[0])) if v is not None]
            head = "플레이스 " + (_bud_won(min(k)) if k else "제한 없음")
        elif not on:
            head = "플레이스 켜진 그룹 없음"
        else:
            head = f"플레이스 {_bud_won(_bud_lim(pc))}({_bud_groups([_bud_lim(g) for g in on])})"
    value = head + (f" · 최근 7일 {sp['n7']}번 멈춤" if sp else " · 최근 7일 멈춤 확인 못 함")
    wst, wc = T["파워링크"]
    pw = wst if wst != "ok" else f"{_bud_won(_bud_lim(wc))}({_bud_groups([_bud_lim(g) for g in wc['groups'] if not g['userLock']])})"
    sub = f"파워링크 {pw} · " + (f"멈춤 {sw['n']}번" if sw else "멈춤 확인 못 함")
    if not sp:
        return value, sub, None, [], why or "플레이스 캠페인을 못 가름"
    md = lambda d: f"{d.month}/{d.day}"
    pre = ("기록 시작 " if sp["kind"] == "기록" else "") + f"{md(sp['d0'])} 뒤 {sp['days']}일 중 "
    if sp["n"]:
        a, b = md(sp["first"]), md(sp["last"])
        summ = pre + f"{sp['n']}번 멈춤({a if a == b else a + '~' + b}) 펼치기"
    else:
        summ = pre + "멈춤 0번 펼치기"
    return value, sub, summ, sp["rows"], f"{sp['kind']} {md(sp['d0'])} · {sp['days']}일 · 플레이스 {sp['n']}번 · 파워링크 {sw['n'] if sw else '?'}번"


def check_budget_card(html, kw, bal_path, extra_dir):
    """24b. 판 L 하루예산 카드 = 예산 기록(balance.json budget) · 원장 SYSTEM 줄 — compute.py 와 계산 공유 0(읽기·일수만 reportlib · 설정은 extras_config)."""
    if not int(LAYOUT["markers"].get("budget_card", 0)):
        return
    name = "하루예산 카드 = 예산 기록(balance.json budget) · 원장 SYSTEM 줄"
    vals = re.findall(r'<div class="value" data-budget="value">(.*?)</div>', html)
    subs = re.findall(r'<div class="sub" data-budget="sub">([^<]*)</div>', html)
    sums = re.findall(r'<summary class="fold-more" data-budget="summary">([^<]*)</summary>', html)
    if len(vals) != 1 or len(subs) != 1 or len(sums) != 1 or html.count('data-budget="list"') != 1:
        check(name, False, f"카드 값 {len(vals)} · 보조 줄 {len(subs)} · summary {len(sums)} · 목록 {html.count('data-budget=' + chr(34) + 'list' + chr(34))} ≠ 1 — 카드가 없거나 마크업 변경 의심(apply.py --layout 판 L)")
        return
    li = html.find('data-budget="list"')
    rows = re.findall(r"<div><span>([^<]*)</span><span>([^<]*)</span></div>", html[li:html.find("</details>", li)])
    if not bal_path:
        check(name, False, "잔액 기록 인자 없음 — validate.py … --balance work/balance.json(precheck 는 작업본 옆 balance.json 을 넘긴다)")
        return
    try:
        with open(bal_path, encoding="utf-8") as f:
            rec = json.load(f)
        b = rec.get("budget")
        if b is not None:
            if b["status"] not in ("ok", "fail"):
                raise ValueError(f"budget.status {b['status']!r}")
            t = dt.datetime.fromisoformat(b["read_at"].replace("Z", "+00:00"))
        else:
            t = dt.datetime.fromisoformat(rec["read_at"].replace("Z", "+00:00"))
        if t.tzinfo is None:
            raise ValueError("read_at 시간대 없음")
        if b is not None and b["status"] == "ok":
            for c in b["campaigns"]:
                for x in [c] + list(c["groups"]):
                    if not (isinstance(x["name"], str) and isinstance(x["type"], str) and isinstance(x["useDailyBudget"], bool) and isinstance(x["userLock"], bool)
                            and isinstance(x["dailyBudget"], int) and not isinstance(x["dailyBudget"], bool) and x["dailyBudget"] >= 0):
                        raise ValueError(f"캠페인·그룹 칸 꼴 {str(x)[:60]}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        check(name, False, f"잔액 기록(budget)을 못 읽음·꼴 다름({type(e).__name__}: {str(e)[:80]}): {bal_path}")
        return
    k = t.astimezone(KST)
    dmin, dmax, _ = parse_days(kw)
    stamp = f"{k.month}/{k.day}({YOIL[k.weekday()]}) {k.hour:02d}:{k.minute:02d}"
    bad = []
    if k.date() <= dmax.date():
        bad.append(f"예산을 읽은 날 {k.date()}(KST) ≤ 집계 마지막 날 {dmax.date()} — 지난 회차 기록(balance.py 를 이번 회차에)")
    plain = lambda x: re.sub(r"<[^>]+>", "", x).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    if b is None or b["status"] == "fail":
        want = ("확인 못 함", f"{stamp} 조회 실패", None, [], "예산 기록 없음" if b is None else "기록 fail")
    else:
        want = _bud_expect(b, extra_dir, dmax)
    wv, ws, wsum, wrows, info = want
    if plain(vals[0]) != wv:
        bad.append(f"값 화면 {plain(vals[0])!r} ≠ 기대 {wv!r}")
    if plain(subs[0]) != ws:
        bad.append(f"보조 줄 화면 {plain(subs[0])!r} ≠ 기대 {ws!r}")
    if (wsum is None and not plain(sums[0]).startswith("멈춤 기록 확인 못 함")) or (wsum is not None and plain(sums[0]) != wsum):
        bad.append(f"summary 화면 {plain(sums[0])!r} ≠ 기대 {wsum or '멈춤 기록 확인 못 함 …'!r}")
    if [(plain(a), plain(c)) for a, c in rows] != wrows:
        bad.append(f"목록 {len(rows)}줄 ≠ 원장 {len(wrows)}줄" + (f" — 첫 다름 화면 {next((x for x, y in zip(rows, wrows) if (plain(x[0]), plain(x[1])) != y), None)} · 원장 {next((y for x, y in zip(rows, wrows) if (plain(x[0]), plain(x[1])) != y), None)}" if rows and wrows else ""))
    check(name, not bad, "; ".join(bad) if bad else f"{plain(vals[0])} · {subs[0]} · {plain(sums[0])} · 목록 {len(rows)}줄 ({info} · 입력 {bal_path} · {extra_dir or '추가 폴더 없음'})")


def _block(html, key):
    """판 G 블록 안쪽(여는 표지 ~ 닫는 표지). 없으면 None."""
    a, b = html.find(f"<!-- saero:extra {key} -->"), html.find(f"<!-- /saero:extra {key} -->")
    return html[a:b] if -1 < a < b else None


def _plain(s):
    return re.sub(r"<[^>]+>", "", s).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").strip()


def _ga_expect(path, dim, unk, min_imps, show_unknown):
    """성별·연령대 합본 하나를 compute.py 와 따로 다시 센다(csv 모듈 · 값 계산 공유 0) → (기간 'M/D~M/D', 알 수 없음 % 글, [(구분, 노출, 비중, 클릭, 클릭률|적음, 비용)])."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        text = f.read()
    head, _, rest = text.partition("\n")
    m = re.search(r"\((\d{4})\.(\d{2})\.(\d{2})\.~(\d{4})\.(\d{2})\.(\d{2})\.\)", head)
    rows = list(csv.reader(io.StringIO(rest)))
    cols = rows[0]
    i_d, i_n, i_c, i_k = cols.index(dim), cols.index("노출수"), cols.index("클릭수"), cols.index("총비용")
    agg = {}
    for r in rows[1:]:
        if not r:
            continue
        a = agg.setdefault(r[i_d], [0, 0, 0])
        for j, col in enumerate((i_n, i_c, i_k)):
            try:
                a[j] += int(float(r[col])) if r[col] != "" else 0
            except ValueError:
                pass
    total = sum(v[0] for v in agg.values())
    def key(lbl):   # 첫 숫자가 같으면 '미만' 이 앞(판 J 결정 36 — 14세 미만 · 14세 ~ 18세)
        num = re.findall(r"\d+", lbl)
        return (1 if lbl == unk else 0, int(num[0]) if num else 10**6, 0 if "미만" in lbl else 1, lbl)
    out = []
    for lbl in sorted(agg, key=key):
        n, cl, k = agg[lbl]
        if lbl == unk and not show_unknown:
            continue
        ctr = "적음" if (n < min_imps or n == 0) else f"{round(cl / n * 100, 2):.2f}%"
        share = f"{(round(n / total * 100, 1) if total else 0.0):.1f}%"
        out.append((lbl, f"{n:,}", share, f"{cl:,}", ctr, f"{k:,}원"))
    per = f"{int(m.group(2))}/{int(m.group(3))}~{int(m.group(5))}/{int(m.group(6))}"
    u = agg.get(unk, [0])[0]
    shown = any(r[0] == unk for r in out)   # 판 J(결정 8) — 표에 알 수 없음 줄이 있으면 머리 괄호에 % 0
    return per, (f" · 알 수 없음 {round(u / total * 100, 1):.1f}%" if total and not shown else ""), out


def _v_phrase(kind, body):
    """변경 내용 → '내용' 한 구(compute.py change_phrase 와 따로 쓴 같은 규칙 — 둘째 줄로 가름)."""
    lines = body.split("\n")
    tag = lines[1].strip() if len(lines) > 1 else ""

    def count(seg):
        total = 0
        for ln in seg:
            val = ln.split(":", 1)[1] if ":" in ln else ln
            total += sum(1 for x in val.strip().split(", ") if x.strip())
        return total
    def fields(seg):
        seen = []
        for ln in seg:
            if ":" in ln:
                f = ln.split(":", 1)[0].strip()
                if f and f not in seen:
                    seen.append(f)
        return "·".join(seen)
    if kind == "확장소재 추가" and tag == "등록된 내용":   # 판 J(결정 28) — 원장 한 줄 = 확장 소재 하나(속성 칸 수가 아니다)
        return "확장 소재 1개 추가"
    if tag in ("등록된 내용", "삭제된 내용"):
        f = fields(lines[2:])
        return ("등록" if tag.startswith("등록") else "삭제") + f" {count(lines[2:])}개" + (f"({f})" if f else "")
    if tag == "변경 전" and "변경 후" in lines[2:]:
        k = lines.index("변경 후", 2)
        if kind == "타겟팅 변경":
            f = fields(lines[2:k])
            return (f + " " if f else "") + f"변경(전 {count(lines[2:k])} → 후 {count(lines[k + 1:])}개)"
        before = [(l.split(":", 1)[0].strip(), l.split(":", 1)[1].strip()) for l in lines[2:k] if ":" in l]
        after = dict((l.split(":", 1)[0].strip(), l.split(":", 1)[1].strip()) for l in lines[k + 1:] if ":" in l)
        bits = []
        for f, v in before:
            if f in after:
                w = after[f]
                bits.append(f"{f} {count([v])} → {count([w])}개" if (", " in v or ", " in w) else f"{f} {v} → {w}")
        return " · ".join(bits)
    return ""


def _merge_ext(phrases):
    """같은 분 묶음 안 '확장 소재 n개 추가' 구들 → 첫 자리에 하나(건수 합 — compute merge_ext 와 따로 쓴 같은 규칙, 판 J 결정 28)."""
    n = sum(int(m.group(1)) for m in (re.fullmatch(r"확장 소재 (\d+)개 추가", p) for p in phrases) if m)
    out = []
    for p in phrases:
        if not re.fullmatch(r"확장 소재 \d+개 추가", p):
            out.append(p)
        elif f"확장 소재 {n}개 추가" not in out:
            out.append(f"확장 소재 {n}개 추가")
    return out


def check_extras(html, extra_dir, kw):
    """27. (판 G, 2026-10-12) 추가 카드·표 = work/extra(독립 재계산). 카드 유무 기준 = `<extra>/<종류>.csv`·`<extra>/변경이력.csv`(+기록 구간) 파일 유무(A-5 —
    precheck 가 늘 넘겨도 첫 회·실패면 '확인 못 함'이 맞음). 있으면 표 기간·줄 값이 다시 센 값과 같아야, 없으면 그 자리가 '확인 못 함' 이어야.
    B 표 기간 = 키워드 CSV 집계 기간 ∩ 기록 구간 마지막 연속 구간(막음 B-1) · 보일 주체 줄(같은 분은 한 줄 — 2026-10-12) 최신 위 max_rows · 스킬 등록 n회(고유 분)·삭제 k건 ·
    show_system false 면 SYSTEM·하루예산 중단 0(09-21 결정) · 배포본 전체에 아이디 꼴(`:naver`) 0."""
    import extras as X
    name = "추가 카드·표(판 G — 성별·연령대 · 계정 변경 기록) = work/extra"
    if not int(LAYOUT["markers"].get("extra_blocks", 0)):
        return
    ex, _ = X.extras_config(CFG["report_fetch"])
    ga_b, hi_b = _block(html, "gender-age"), _block(html, "history")
    bad, info = [], []
    if ga_b is None or hi_b is None:
        check(name, False, "추가 블록 표지를 못 찾음 — apply.py --layout(판 G)")
        return
    if ":naver" in html:
        bad.append(f"배포본에 아이디 꼴 ':naver' {html.count(':naver')}곳")
    reports = (ex or {}).get("reports") or {}
    ga = (ex or {}).get("gender_age") or {}
    subs = re.split(r'<div class="sub-head">', ga_b)[1:]   # [0] 표지~카드 머리(style 붙은 sub-head) · [1:] 종류마다
    got_ga = {}
    for s in subs:
        m = re.match(r"([^<]+?) <span[^>]*>\((.*?)\)</span></div>", s)
        if m:
            cells = [[_plain(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)] for tr in re.findall(r"<tr>(.*?)</tr>", s, re.S)]
            got_ga[_plain(m.group(1))] = (_plain(m.group(2)), [tuple(c) for c in cells if c])
    any_file = False
    for rname, spec in reports.items():
        k = spec["kind"]
        p = os.path.join(extra_dir, f"{k}.csv") if extra_dir else None
        g = got_ga.get(k)
        if p and os.path.exists(p):
            any_file = True
            per, unk_txt, want_rows = _ga_expect(p, spec["dim"], ga.get("unknown", "알 수 없음"), int(ga.get("min_imps", 0)),
                                                 bool(ga.get("show_unknown", True)) and k not in ga.get("hide_unknown_kinds", []))
            if g is None:
                bad.append(f"{k}: 합본이 있는데 카드에 표가 없음('확인 못 함' 또는 마크업)")
                continue
            if g[0] != per + unk_txt:
                bad.append(f"{k} 머리 화면 ({g[0]}) ≠ 합본 ({per}{unk_txt})")
            if g[1] != want_rows:
                bad.append(f"{k} 표 {len(g[1])}줄 ≠ 다시 센 {len(want_rows)}줄" + (f" — 첫 다름 화면 {next((a for a, b in zip(g[1], want_rows) if a != b), None)} · 합본 {next((b for a, b in zip(g[1], want_rows) if a != b), None)}" if g[1] else ""))
            info.append(f"{k} {per} {len(want_rows)}줄")
        else:
            if g is not None and not g[0].startswith("확인 못 함"):
                bad.append(f"{k}: 합본(work/extra/{k}.csv)이 없는데 카드에 값이 있음 — 옛 값이 남았거나 입력이 다름")
            info.append(f"{k} 확인 못 함")
    if not any_file and "확인 못 함" not in ga_b:
        bad.append("성별·연령대 합본이 하나도 없는데 카드에 '확인 못 함'이 없음")
    # B — 계정 변경 기록
    h = (ex or {}).get("history")
    led = os.path.join(extra_dir, X.HISTORY_FILE) if extra_dir else None
    cov = os.path.join(extra_dir, X.COVERED_FILE) if extra_dir else None
    if h and led and os.path.exists(led) and os.path.exists(cov):
        with open(cov, encoding="utf-8-sig", newline="") as f:
            spans = [r for r in csv.reader(f)][1:]
        days = set()
        for r in spans:
            if not r:
                continue
            a = dt.date.fromisoformat(r[0])
            b = dt.date.fromisoformat(r[1])
            while a <= b:
                days.add(a)
                a += dt.timedelta(days=1)
        dmin, dmax, _ = parse_days(kw)
        end = max(days) if days else None
        start = end
        while start is not None and (start - dt.timedelta(days=1)) in days:
            start -= dt.timedelta(days=1)
        lo, hi = (max(dmin.date(), start), min(dmax.date(), end)) if days else (None, None)
        if not days or lo > hi:
            if "확인 못 함" not in hi_b:
                bad.append("기록 구간이 집계 기간과 겹치지 않는데 표에 '확인 못 함'이 없음")
        else:
            with open(led, encoding="utf-8-sig", newline="") as f:
                lrows = [r for r in csv.reader(f)][1:]
            inside = [r for r in lrows if r and lo <= dt.date(int(r[0][:4]), int(r[0][5:7]), int(r[0][8:10])) <= hi]
            show = [r for r in inside if r[2] in h["show"]]
            show = sorted(show, key=lambda r: r[0], reverse=True)
            # 같은 분(일시 원문)은 한 줄(2026-10-12 사용자 결정) — 칸마다 겹치지 않는 값을 원장 순서대로 ' · ' 로(compute 와 따로 다시 묶는다)
            grp_keys = list(dict.fromkeys(r[0] for r in show))
            uniq = lambda xs: " · ".join(dict.fromkeys(x for x in xs if x))
            show = [[r for r in show if r[0] == k] for k in grp_keys]
            want = [(f"{int(g[0][0][5:7])}/{int(g[0][0][8:10])} {g[0][0][12:17]}", uniq(r[1] for r in g), uniq(r[4] or r[3] or "—" for r in g),
                     uniq(_merge_ext([_v_phrase(r[1], r[5]) for r in g])) or "—") for g in show[:int(h["max_rows"])]]
            label = f"{lo.month}/{lo.day}~{hi.month}/{hi.day} 기록" + (f" · 최근 {len(want)}건 / {len(show)}건" if len(show) > len(want) else "")
            mh = re.search(r"계정 변경 기록\([^)]*\) <span[^>]*>\((.*?)\)</span>", hi_b)
            if not mh or _plain(mh.group(1)) != label:
                bad.append(f"변경 기록 머리 화면 ({_plain(mh.group(1)) if mh else '없음'}) ≠ ({label})")
            got = [tuple(_plain(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)) for tr in re.findall(r"<tr>(.*?)</tr>", hi_b, re.S)]
            got = [g for g in got if g]
            if got != want:
                bad.append(f"변경 기록 표 {len(got)}줄 ≠ 원장 {len(want)}줄" + (f" — 첫 다름 화면 {next((a for a, b in zip(got, want) if a != b), None)} · 원장 {next((b for a, b in zip(got, want) if a != b), None)}" if got and want else ""))
            # 맨 위 줄과 같은 날짜 줄만 펼친 표, 나머지는 접기 하나 안(2026-10-15 사용자 결정) — 펼친 줄 수·summary 글·접기 수
            day = lambda t: t[0].split(" ")[0]
            k = next((i for i, t in enumerate(want) if day(t) != day(want[0])), len(want))
            vis = hi_b.split("<details", 1)[0]
            n_vis = len([1 for tr in re.findall(r"<tr>(.*?)</tr>", vis, re.S) if "<td" in tr])
            sums = re.findall(r'<details class="fold"[^>]*>\s*<summary class="fold-more">([^<]*)</summary>', hi_b)
            a, b = (day(want[-1]), day(want[k])) if k < len(want) else (None, None)
            want_sum = [f"이전 {len(want) - k}건({a if a == b else f'{a}~{b}'}) 펼치기"] if k < len(want) else []
            if n_vis != k or sums != want_sum or hi_b.count("<details") != len(want_sum) or hi_b.count("</details>") != len(want_sum):
                bad.append(f"변경 기록 접기 — 펼친 줄 {n_vis} · summary {sums} · details {hi_b.count('<details')} ≠ 기대 펼친 줄 {k}(맨 위 날짜) · {want_sum}")
            sk = [r for r in inside if r[2] == "스킬" and r[1] == "타겟팅 변경"]
            sec_line = lambda r: (r[5].split("\n") + ["", ""])[1].strip()
            n_run = len({r[0] for r in sk if sec_line(r) == "등록된 내용"})
            n_del = len([r for r in sk if sec_line(r) == "삭제된 내용"])
            if "스킬 제외 검색어 등록" in _plain(hi_b):   # 판 J(결정 7) — 스킬 줄을 뺐다(제외 검색어 현황은 07 ②)
                bad.append("스킬 줄('스킬 제외 검색어 등록 n회') 이 남음 — 판 J 에서 뺀 줄")
            if not h.get("show_system") and ("하루예산 중단" in hi_b or "SYSTEM" in hi_b or "시스템" in hi_b):
                bad.append("show_system false 인데 표에 SYSTEM·하루예산 중단")
            info.append(f"변경 기록 {lo.month}/{lo.day}~{hi.month}/{hi.day} {len(want)}/{len(show)}줄(펼침 {k}) · 스킬 줄 0(원장 스킬 {n_run}회·삭제 {n_del})")
    else:
        if "확인 못 함" not in hi_b:
            bad.append("원장 사본(work/extra/변경이력.csv·기록 구간)이 없는데 표에 '확인 못 함'이 없음 — 옛 값이 남았거나 입력이 다름")
        info.append("변경 기록 확인 못 함")
    check(name, not bad, "; ".join(bad) if bad else " · ".join(info) + (f" · 입력 {extra_dir}" if extra_dir else " · 입력 없음(--extra)"))


def check_leads_public(html):
    """25. 01·10·11 본문에 장부 라벨+숫자 0(publish = verdict) — 공개 배포본에 문의·등록·매출 숫자가 실리는 길(막음 A-F2)의 배포 전 관문(판 I — 판 H 까지 01·11·12)."""
    name = "01·10·11 서술에 장부 라벨+숫자 0(공개 범위 verdict)"
    c = CFG.get("leads", {})
    text = re.sub(r"<[^>]+>", "", section(html, 1) + section(html, 10) + section(html, 11))
    if not text.strip():
        check(name, False, "01·10·11 본문 0자 — 섹션 주석 또는 마크업 변경 의심")
        return
    if c.get("publish") != "verdict":
        check(name, False, f"config leads.publish {c.get('publish')!r} ≠ verdict — 건수 공개는 설계 회차 몫")
        return
    hits = label_hits(text, c["public_labels"])
    check(name, not hits, f"라벨 {len(c['public_labels'])}종 · {len(text):,}자" + (f" — {', '.join(f'{a} {b}' for a, b in hits[:5])}" if hits else ""))


def check_12_growth(html, dmax):
    """26. 11번(판 I — 판 H 까지 12번) 장부 행 1 · 판정 낱말 꼴 · 장부·플레이스 행의 M/D까지 = 집계 끝 · 플레이스 ✗ 행 ≤ items_in_12 · ✓ 아닌 행 ≤ max_open_rows_12.
    함수·config 키 이름의 12 는 그대로(내부 이름)."""
    name = "11번 장부·플레이스 행(장부 판정 1 · M/D까지 = 집계 끝 · ✗ ≤ items_in_12 · 항목 ≤ 7)"
    lc, pc = CFG["leads"], CFG["place_checklist"]
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", section(html, 11), re.S)
    plain = [re.sub(r"<[^>]+>", "", t) for t in trs]
    if not trs:
        check(name, False, "11번 표 행 0 — 섹션 주석 또는 마크업 변경 의심")
        return
    end = f"{dmax.month}/{dmax.day}까지"
    bad = []
    lead = [i for i, t in enumerate(plain) if "장부 기준 판정 = " in t]
    place = [i for i, t in enumerate(plain) if re.search(r"플레이스 P\d+ ", t)]
    if len(lead) != 1:
        bad.append(f"장부 판정 행 {len(lead)}개 ≠ 1")
    else:
        m = re.search(r"장부 기준 판정 = ([^<]+?)</b>", trs[lead[0]])
        vw = lc["verdict_words"]
        ok_words = {vw[k] for k in ("hole", "nocompare", "up", "down", "same", "unknown")}
        v = m.group(1) if m else None
        if not (v in ok_words or (v and re.fullmatch(rf"{re.escape(vw['before'])}\(\d+/{int(lc['min_weeks'])}주\)", v))):
            bad.append(f"장부 판정 낱말 {v!r} — config leads.verdict_words 밖")
    for i in lead + place:
        if not re.search(rf"(?<!\d){re.escape(end)}", plain[i]):
            bad.append(f"{i + 1}번째 행에 '{end}' 없음(M/D까지 = 집계 마지막 날)")
    todo = pc["state_words"]["todo"]
    n_x = len([i for i in place if f"상태 = {todo}" in plain[i]])
    if n_x > int(pc["items_in_12"]):
        bad.append(f"플레이스 {todo} 행 {n_x}개 > items_in_12 {pc['items_in_12']}")
    n_open = len([t for t in trs if 'tag tag-ink">✓' not in t])
    max_open = int(pc["max_open_rows_12"])
    if n_open > max_open:
        bad.append(f"✓ 아닌 행 {n_open}개 > {max_open}(config place_checklist.max_open_rows_12)")
    check(name, not bad, "; ".join(bad) if bad else
          f"표 {len(trs)}행(✓ 아닌 {n_open}) · 장부 판정 1 · 플레이스 {len(place)}행(✗ {n_x}) · {end}")


TRIM_GONE = {   # 판 J(2026-10-23 오후 — 불필요 항목 빼기 결정 10~14·19~24·37) 가 뺀 서술 글 — 그 구역에 다시 나오면 FAIL(옛 서술 스크립트 복사 · 손 편집). (이름, 정규식)
    1: [("01 머리 줄 누적 CTR A → B", r"누적 CTR [\d.]+ → [\d.]+%"), ("01 ② 닷새 나열", r"닷새 [\d.]+ →"), ("01 ② '~어려워 보임'", r"어려워 보임")],
    3: [("03 머리 줄 '그대로'·마지막 날", r"원 그대로|\(플레이스 [\d,]+원 \+ 파워링크")],
    4: [("04 민트 줄 격차 되풀이", r"격차 [\d.]+ → <b>"), ("04 '(지난 회차'", r"\(지난 회차"), ("04 '회차부터'", r"회차부터"),
        ("04 회색 클릭 수", r"클릭 중 [\d,]+건"), ("04 회색 마지막 날", r"광고비 [\d,]+원·클릭 \d+건, 비중은")],
    6: [("06 '회차 연속'", r"회차 연속"), ("06 매칭 숫자 되풀이", r"→ 노출 [\d,]+ 대 [\d,]+"), ("06 카드 'N일차 · 평균순위'", r"일차 · 평균순위"), ("06 '그룹 중 가장 좋음'", r"그룹 중 가장 좋음")],
    7: [("07 ③ 지난 회차", r"경쟁사 포함 · 지난 회차"), ("07 ③ 행 단위", r"행 단위 확장")],
    8: [("08 '모두 표시됨'", r"모두 표시됨"), ("08 '11위'", r"11위 "), ("08 '(지난 회차'", r"\(지난 회차"), ("08 확인불가 숫자 되풀이", r"확인불가\"는 노출")],
    9: [("09 '회차 연속'", r"회차 연속"), ("09 '전략과 부합'", r"전략과 부합"), ("09 '최다 클릭 시간대는'", r"최다 클릭 시간대는"), ("09 '(지난 회차'", r"\(지난 회차"),
        ("09 클릭 단위 '회'", r"클릭 \d+회|최다\(\d+회|\d+시 \d+회")],
    10: [("10 순위·클릭 방향", r"순위와 하루 클릭"), ("10 상향 유지", r"상향 유지"), ("10 클릭 1건 목록", r"클릭 1건 목록"), ("10 (참고) 경쟁사·클릭 0", r"\(참고\)</b> (?:경쟁사|클릭 0)"),
         ("10 누적 CTR·비중·직접/자동 되풀이", r"누적 CTR|비중 [\d.]+ → |직접 \d+·자동"), ("10 판정 줄 되풀이", r"이번 요약은|맨 위에 올렸고")],
    11: [("11 registry 구", r"registry|다시 묻지 않음"), ("11 '채팅으로 알림'", r"채팅으로 알림"), ("11 '\"확장\" 행'", r"\"확장\" 행"),
         ("11 note 정렬·경쟁사", r"<b>정렬</b>|경쟁사는 액션 항목"), ("11 note 신규 없음 사유", r"신규 없음(?:</b>)?\s*:"),
         ("11 note '조용히 사라진 항목'", r"조용히 사라진 항목"), ("11 note 체크리스트", r"체크리스트 \d+항목")]}
EXCL_EVENT = ("등록돼 있는데도 노출", "등록 누락", "미확인")   # 07 ② 의 예외 꼴(exclusion-ui.md 9절) — 이때만 10 에 제외 검색어 항목


def check_trim_gone(html):
    """30. (판 J) 뺀 서술 글 0 — TRIM_GONE · 10 변화 없음 줄 숫자 0(M/D까지 · (N시) · 구역 번호 · 'N위 그룹' 밖) · 10 제외 검색어 항목은 07 ② 에 실패·재노출·미확인이 있는 날만."""
    name = "판 J 뺀 글 0(01·03·04·06~11 — 옛 서술 꼴·다른 구역 숫자 되풀이)"
    bad, empty = [], []
    for n, pats in TRIM_GONE.items():
        s = section(html, n)
        if not s.strip():
            empty.append(n)
            continue
        for label, pat in pats:
            hit = re.search(pat, s)
            if hit:
                bad.append(f"{label}: {re.sub(r'<[^>]+>', '', s[max(0, hit.start() - 12):hit.end() + 12])!r}")
    if empty:
        check(name, False, f"구역 {empty} 0자 — 섹션 주석 또는 마크업 변경 의심")
        return
    s10 = section(html, 10)
    for li in re.findall(r"<li>(.*?)</li>", s10, re.S):
        if "변화 없음" in li[:40]:
            rest = re.sub(r"\d+/\d+까지|\(\d+시\)|\((?:\d{2}·)*\d{2}번\)|(?<![\d.])\d+위(?= 그룹)", "", re.sub(r"<[^>]+>", "", li))   # 순위 낱말(총비용 1위 그룹)은 값 아님
            if re.search(r"\d", rest):
                bad.append(f"10 변화 없음 줄에 숫자 {re.findall(r'[0-9][0-9.,%]*', rest)[:4]}(자리만 — 판 J 결정 14 (d))")
        if re.search(r"<b>[^<]*제외 검색어", li[:60]):
            t7 = re.sub(r"<[^>]+>", "", " ".join(re.findall(r'class="note"[^>]*>(.*?)</div>', section(html, 7), re.S)))
            if not (re.search(r"실패 [1-9]", t7) or any(w in t7 for w in EXCL_EVENT)):
                bad.append("10 제외 검색어 항목 — 07 ② 에 실패·재노출·미확인이 없는 날(판 J 결정 14 (a))")
    check(name, not bad, "; ".join(bad[:6]) + (f" 외 {len(bad) - 6}건" if len(bad) > 6 else "") if bad else
          f"구역 {len(TRIM_GONE)}개 · 꼴 {sum(len(v) for v in TRIM_GONE.values())}종 · 0건")


NARR = re.compile(r"<!-- n:([^\s:]+):(?:매회차|고정) -->(.*?)<!-- /n -->", re.S)
# 구역 번호 참조 — 'NN번'(앞이 숫자·글자 아님: 검색어 '노원역10번출구' 제외 · 뒤가 '째'·'출구' 아님) · 'NN·NN번'·'01~07·10번' 묶음은 숫자마다 본다
SECREF = re.compile(r"(?<![0-9A-Za-z가-힣])((?:\d{1,2}[·~])*\d{1,2})번(?!\s*(?:째|출구))")
PLACE_WORDS = ("지면", "매체 설정", "파트너 매체")   # 지면 구역(옛 10번)을 가리키는 10번의 앞뒤 낱말


def check_section_refs(html):
    """28. (2026-10-23 판 I 콘텐츠 지면 빼기) "화면 글 구역 번호" — 서술 표지 안 글(태그 뺀)의 구역 번호 참조가 판 I 번호인지.
    ① 없는 구역(> markers.sections — 옛 '12번 1번'·'지난 회차 12번'·'(12번 행 없음)') 0 · ② 지면 구역을 가리키는 10번 0 — 같은 묶음에 07(옛 'KPI·01~07·10번에서 제외')
    이거나 앞뒤 30자 안에 지면·매체 설정·파트너 매체 · ③ 옛 지면 구역 글 0 — '검색 지면 vs 콘텐츠 지면'·'콘텐츠 지면 N일 연속 0'. 복사된 서술 스크립트가 옛 번호를
    다시 쓰는 길을 막는다(검색어 '노원역10번출구' 같은 낱말 속 숫자는 안 셈). 표지 0개면 FAIL(0건 가드)."""
    name = "화면 글 구역 번호(판 I — 없는 12번·지면 10번·옛 지면 글 0)"
    n = int(LAYOUT["markers"]["sections"])
    blocks = NARR.findall(html)
    if not blocks:
        check(name, False, "서술 표지 0개 — 표지를 잃었거나 마크업 변경 의심")
        return
    bad, refs = [], 0
    for nm, body in blocks:
        t = re.sub(r"<[^>]+>", "", body)
        for m in SECREF.finditer(t):
            nums = [int(x) for x in re.split(r"[·~]", m.group(1))]
            refs += len(nums)
            ctx = t[max(0, m.start() - 30):m.end() + 30]
            if any(k > n for k in nums):
                bad.append(f"{nm}: '{m.group(0)}'(없는 구역 — 구역은 1~{n})")
            elif 10 in nums and (7 in nums or any(w in ctx for w in PLACE_WORDS)):
                bad.append(f"{nm}: '{m.group(0)}'(지면 구역을 가리키는 10번 — 10번은 핵심 요약)")
        if re.search(r"콘텐츠 지면 \d+일 연속 0", t) or "검색 지면 vs 콘텐츠 지면" in t:
            bad.append(f"{nm}: 옛 지면 구역 글(콘텐츠 지면 N일 연속 0 · 검색 지면 vs 콘텐츠 지면)")
    check(name, not bad, "; ".join(bad[:6]) + (f" 외 {len(bad) - 6}건" if len(bad) > 6 else "") if bad else
          f"표지 {len(blocks)}개 · 번호 참조 {refs}개 전부 1~{n}")


def main():
    argv = sys.argv[1:]
    bal_path = None
    if "--balance" in argv:  # 판 F 잔액 기록(precheck 가 작업본 옆 balance.json 을 넘긴다) — 없으면 "광고비 잔액 카드" FAIL
        i = argv.index("--balance")
        if i + 1 >= len(argv):
            sys.exit(__doc__)
        bal_path = argv[i + 1]
        del argv[i:i + 2]
    extra_dir = None
    if "--extra" in argv:  # 판 G 추가 합본 폴더(precheck 가 작업본 옆 extra/ 를 넘긴다) — 카드 유무 기준 = 그 안 파일 유무
        i = argv.index("--extra")
        if i + 1 >= len(argv):
            sys.exit(__doc__)
        extra_dir = argv[i + 1]
        del argv[i:i + 2]
    pending = "--pending" in argv
    args = [a for a in argv if a != "--pending"]
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

    # --- 4. CTR 강조 규칙 (07번) — 판 J: 노출 FEW07 미만은 '적음'(강조 0), 그 밖은 숫자 + 기준 이상에만 강조 ---
    n7 = f"07번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high(노출 {FEW07}회 미만 '적음')"
    if not rows:
        check(n7, False, "정식표 행 0건 — 마크업이 바뀌어 정규식이 안 맞을 수 있음")
    else:
        def ok7(r):
            if r["imps"] < FEW07:
                return r["few"] and not r["has_hl"]
            return not r["few"] and r["has_hl"] == (r["ctr"] >= CTR_HIGH)
        mismatched = [f"{r['kw']}(노출 {r['imps']} · {'적음' if r['few'] else str(r['ctr']) + '%'}, 강조={'있음' if r['has_hl'] else '없음'})" for r in rows if not ok7(r)]
        check(n7, not mismatched,
              f"{len(rows)}행 검사(적음 {sum(r['few'] for r in rows)}), 불일치 {len(mismatched)}건" + (f": {', '.join(mismatched)}" if mismatched else ""))

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
    check_card_rule(html, kw, kw_inc)  # 2026-10-23 — 판 J 06 카드 규칙 · 04 신규 메모 기한
    sr = read_csv(sr_path)
    check_competitors(s7, sr)
    sr_clicks = int(sr["클릭수"].sum())
    check("검색어 CSV 클릭 합계 = KPI 클릭", sr_clicks == kpi_clicks,
          f"검색어 CSV {sr_clicks} vs KPI {kpi_clicks}" + ("" if sr_clicks == kpi_clicks else " — 검색어 보고서 기간이 다를 수 있음"))
    check_11_12(html, pending, dmax)
    check_07_footnotes(s7)  # 2026-10-06 — 글 줄이기 회차 1
    check_layout(html)  # 2026-10-06 — 레이아웃 판 회차 2
    check_balance_card(html, kw, bal_path)  # 2026-10-09 — 판 F 광고비 잔액 카드
    check_budget_card(html, kw, bal_path, extra_dir)  # 2026-10-27 — 판 L 하루예산 카드(config markers.budget_card 가 없으면 검사 없음)
    check_leads_public(html)  # 2026-10-10 — 매출 작업 A 공개 범위
    check_12_growth(html, dmax)  # 2026-10-10 — 매출 작업 A·C 11번(판 H 까지 12번) 행
    check_extras(html, extra_dir, kw)  # 2026-10-12 — 판 G 추가 카드·표(보고서 더 받기 A + B)
    check_section_refs(html)  # 2026-10-23 — 판 I 화면 글 구역 번호(옛 12번·지면 10번 0)
    check_trim_gone(html)  # 2026-10-23 — 판 J 뺀 서술 글 0

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
