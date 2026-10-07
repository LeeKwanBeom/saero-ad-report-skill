## 검증·병합 기록(2026-10-08 — 01 모바일 기간 접기(레이아웃 판 r2026-10-D): 검증 1(막음 0) → main 병합)

**병합**: `feat-20261007-mobilefold`(`8a3c050` — 38e0123 위 2커밋: `9db296a` 코드·시험·문서 · `8a3c050` 수정 기록)를 main(`38e0123` — 분기 뒤 main 변경 0, 2026-10-08 00:24 KST `ls-remote` 로 main = 38e0123 · 브랜치 = 8a3c050 확인 · 운영 작업 폴더 `git --no-optional-locks status --short` 0줄 · `work/` 최근 변경 10/7 08:09 → 갱신 회차 돌지 않음)에 `git merge --no-ff` → 병합 커밋 **`f342f6c`**(부모 38e0123 · 8a3c050, 트리 `c21ce7cd` = 8a3c050 트리 — `git diff --stat 8a3c050 HEAD` 빈 출력 · 38e0123 대비 11 파일 +784/−160). 경우 A — 충돌 0(audit/last-audit.md 포함 — main 이 움직이지 않아 자동 병합). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`(전역 설정 변경 0). clone `D:\saero-verify\merge-20261008-mobilefold`(`git clone -c core.autocrlf=false`). 사용자 병합 지시(2026-10-08 00:24 KST 무렵, 채팅 원문 "병합" — 병합 지시문 `D:\saero-verify\saero-ad-report_병합지시_01모바일기간접기_회차1_2026-10-08.md` 를 따름) 뒤 병합. 브랜치 `feat-20261007-mobilefold` 는 지우지 않고 둔다. 코드·문서·config·data 재수정 없음(이 절 추가만). 아래 수정 기록의 `브랜치 push 1회(feat-20261007-mobilefold, main 아님)` 와 `다음 단계: ④ 검증 … Fable 5.1 · ultracode` 는 당시 사실 — 원문 보존, 이 절로 정정(**검증 모델은 Opus 5.5 로 바뀜 · 2026-10-08 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고에). 에이전트 0(지시 "조정자가 직접").

**검증 1**(`D:\saero-verify\saero-ad-report_검증_01모바일기간접기_회차1_2026-10-07.md`, 별도 세션 — `D:\saero-verify` 2026-10-07 21:38~21:56 KST, Opus 5.5 · ultracode(Fable 한도 96% — 사용자 결정), 검토 에이전트 4 = 런타임 Sonnet 5.5 `claude-sonnet-5-5` 1 · Opus 5.5 2 · Haiku 4.5 1 · 반박 0 · 하위 토큰 634,684, clone `D:\saero-verify\feat-20261007-mobilefold-1`, 대상 8a3c050): 아래 수정 기록 "검증 회차가 볼 것" 1~8 전부 참 · 리허설 R1~R6 재실행(rehearse.sh) — 경로·소요 시간 3줄 빼고 로그 전 줄 같음, md5 22줄 같음(index 02e80dac · PNG 10 · compare.html 5f37cbae) · chart_check **PASS 27 / FAIL 0** · 외부 요청 허용 2 · 차단 0 · test_apply **21** OK · test_deploy `-k layout_gate` **4** OK(격리 env · deploy 실행 0) · 리허설 밖 재측정 0(막음 후보 0) · **막음 0** → "다음 단계로 가도 된다".

**병합 main 확인**(경우 A — 병합 트리 = 브랜치 트리 해시 같음 · 전체 시험은 구현 세션이 병합 전 한 번(20:27~20:31, `work/RD/fulltest.sh`) · 최종 코드로 검증 세션이 R1~R6·게이트 4 재실행 → 작업 알고리즘 4절 "전체 시험은 병합 전 한 번" 이 채워져 다시 돌리지 않음) [실측 00:25~00:27 KST]:
- 병합 트리 `c21ce7cd` = 8a3c050 트리 · `git diff --stat 8a3c050 HEAD` 빈 출력.
- `cat data/*/*.csv audit/exclusions.csv | md5sum` 병합 전 origin/main = 병합 뒤 **`39493a38`**.
- registry(`audit/exclusions.csv`) **`fe0aa09c`**(894행) · config/report-config.json **`b9be593d`**(175행).
- `git diff --stat 38e0123 HEAD -- local/` 빈 출력 · 작업 트리 변경 0.
- audit/last-audit.md(이 절 전) **2,118행 · 600,406바이트** · CR 0.
배포 PUT 0 · 네이버 0 · fetch_reports·deploy 실행 0 · 운영 작업 폴더 `D:\saero` 쓰기 0 · 작업 clone 열기 0.

**이월**(한 줄씩 — 검증 1 판정의 이월 9건 그대로):
- (검증 이월 1) chart_check 는 화면(접힘·펼침)의 보이는 라벨 글자를 compute 값과 대조하지 않는다(개수·순서·위치만 본다. 값 대조는 인쇄 PDF 에만 있다). 코드는 같은 from 으로 자르고, R4 PNG 01·06 14행을 눈으로 대조해 같았다.
- (검증 이월 2) 06 모바일 순위 축 눈금이 접힘(3·2·1)과 펼침(4·3·2·1)에서 달라, 누르면 점의 가로 위치가 움직인다. 값과 날짜는 어긋나지 않는다. max 를 고정할지는 첫 실사용 뒤 사용자 결정이다.
- (검증 이월 3) chart_check 인쇄 시나리오는 처음(접힘) 상태만 본다. 펼친 뒤 인쇄 · 06 만 펼친 뒤 인쇄 · 인쇄 중 버튼은 저장소 시험에 없다.
- (검증 이월 4) 1280 의 최신 쪽 시작(S)은 새 판 절대 기대로만 판정하고, 기준 prev 의 로드 상태 S 는 재지 않는다(같은 판 C 규칙이라 결과는 같다).
- (검증 이월 5) CRLF 판 C 를 `apply --layout` 하면 FAIL 문구가 앵커 줄바꿈 때문에 3줄로 갈라진다(apply.py:615). rc 1 이고 작업본은 그대로다(요란).
- (검증 이월 6) 값만 경로(D → D)는 판 D 도우미 바이트를 템플릿과 대조하지 않는다. 그래서 손으로 고친 판 D 도우미가 그대로 지나간다(정상 흐름 밖).
- (검증 이월 7) precheck 는 통과하면 validate 끝 3줄만 찍어 `레이아웃 판 … 최근 14/14` 줄이 안 보인다. 임의 결정 10 의 근거와 첫 적용 본보기 "6 precheck 기대" 는 validate 를 따로 돌려야 확인된다.
- (검증 이월 8) checklist.md:30 [의도된 동작] 27 판 D 문단의 "앞 28일" 은 42일 데이터에 묶인 고정 숫자다(날짜가 늘면 n−14).
- (검증 이월 9) css-and-layout.md:197 반응형 4 가 판 C 표기 "`n × row_px + pad_px`" 그대로다(판 D 는 그리는 날짜 수).

**병합 뒤**(이 병합 세션은 하지 않았다): ① main 작업 폴더 `D:\saero\saero-ad-report-skill` `git pull --ff-only`(운영 세션 몫, 다음 `/saero-run` 첫머리 — ingest·S0 의 "HEAD = origin/main" 이 막는다) ② local/ 변경 0 → 설치본(`D:\saero\CLAUDE.md` · `saero-run`) 갱신 불필요 ③ **첫 적용 = 다음 `/saero-run`**(Opus 5.5 · high · ultracode 끔), 첫 말 "판 D(01 모바일 기간 접기) 첫 적용 — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함", 순서는 아래 수정 기록 "첫 적용 본보기": 5단계 `apply --layout` → `레이아웃 판 변환(r2026-10-C → r2026-10-D, 분기 2)` → 6단계 precheck 도장 → **보류 멈춤**: `"$PY" tests/chart_check.py work/index.html work/compute.json --base work/prev.html --out work/chart_<날짜>`(PASS 27 · 허용 2·차단 0) → `work/chart_<날짜>/compare.html` + 폰(390 세로 · 펼치기·다시 접기 · 844 회전 뒤 접힘 · 인쇄 미리보기)·PC 확인 → 사용자 "배포" → dry-run `[주의] 레이아웃 판이 바뀜` → `push --layout-change` → `verify` → 기록. 검증 이월 7 때문에 `레이아웃 판 … 최근 14/14` 줄은 validate 를 따로 돌려 본다. 첫 말 없이 데이터 회차가 먼저 돌면 5단계가 C→D 로 바꾸고 7단계 게이트가 `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함` 으로 멈춰 묻는다(요란 — 그 회차가 보류 회차가 된다) ④ 이월(검증 9 + 수정 기록 10)은 첫 실사용 뒤 또는 정기점검 때 본다.
효율: 벽시계 약 10분(00:24 ls-remote → clone·병합 → 확인 → 기록·push) · 도구 호출 약 12회 · 하위 에이전트 0 · 즉석 코드 약 20행(덧붙이기 스크립트 — 스크래치).

---

## 수정 기록(2026-10-07 — 01 모바일 기간 접기) · 브랜치 `feat-20261007-mobilefold`

점검일: 2026-10-07 19:50~20:55 KST 무렵 (기능 추가 — **작은 작업**(작업 + 검증 세션 2개), 레이아웃 판 **r2026-10-C → r2026-10-D**. 데스크톱 앱 Code 탭, 이 PC, `D:\saero` 로 연 작업 세션, Opus 5.5).
작업 clone `D:\saero\feat-20261007-mobilefold`(`git clone -c core.autocrlf=false`, origin/main **`38e0123`** 에서 분기 — 지시의 사실 기준 8파일 커밋(apply·config·test_apply 9bbfd2c · validate 48fc991 · compare eae81ef · chart_check 57cf58b · report-structure·css-and-layout 073647c) 전부 일치, 시작·20:27 fetch 둘 다 origin/main 그대로).
사용자 원문(2026-10-07): "현재 모바일 화면은 보면은 8/26 ~ 10/6 까지의 데이터가 전부다 나오고있어 해당 부분이 너무 길기에 어느정도는 숨김처리 하려고" · 03 의 펼치기를 01 에 적용(06 도 같은 규칙, 01·06 버튼 따로).
판 C 이월 "모바일 기간 창 규칙"(탐색 기준선 6절 A-6 · report-structure "판 C" 끝 줄 · css-and-layout 버그 8 끝 줄)을 이 회차가 푼다(남은 몫 = 펼친 높이는 여전히 n 비례 · 행 높이 하한 없음 — 아래 이월 9).
외부 쓰기 0: 배포 PUT 0 · 네이버 0 · 키 파일 0 · deploy.py 는 `push --dry-run` 1회(R7 — 읽기·자격 확인만) · 운영 main 작업 폴더는 `work/` 재료 읽기 복사만 · 배포 저장소는 공개 읽기 shallow clone(`work/pages` — 옛 판 실물) · 스킬 저장소는 브랜치 push 만.
효율: 벽시계 약 65분 · 도구 호출 약 110회 · 하위 에이전트 1(독립 검토 opus — 하위 토큰 약 14.5만 · 도구 25) · 즉석 코드 약 250행(패치 스크립트·탐침 — 스크래치, `work/RD/rehearse.sh` 95행·`fulltest.sh` 45행 제외).
표기: [실측] 이번에 파일·명령으로 확인 / [추론] 확인 못 함.

### 바뀐 것(파일별, `wc -l` 전 → 후 · md5 앞 8자리 — 코드 커밋 `9db296a`) [실측]

| 파일 | 행 | md5 | 무엇 |
|---|---|---|---|
| `config/report-config.json` | 171 → 175 | b9be593d | `report_layout.layout_id` "r2026-10-C" → **"r2026-10-D"** · 신설 `mobile.recent_days {"01": 14, "06": 14}`(03 표의 `recent_days` 7 과 다른 값) · `_comment` 판 D 줄. 그 밖의 값 0 |
| `scripts/apply.py` | 706 → 892 | cffc4294 | `LAYOUT_D` · `M_LINE`(recent 포함 — 판 D) · `M_LINE_C`·`m_line_c`(판 C 꼴 — 사슬 중간 B → C 전용) · `m_line`(= C 꼴 + recent) · `MOBILE_JS_C`(판 C 도우미 원문 보존) · **`MOBILE_JS`(판 D 도우미 — `hidden`·`draw`·`button`·`build`·`toggle`·`judge`·beforeprint·afterprint)** · `MOBILE_CSS_D`(`.chart-fold`) · `COSTGAP_C_TO_D`(01 비용 라벨 간격 2곳 `data.datasets[i]` → `ch.data.datasets[i]`) · **`convert_c_to_d`**(① meta ② `</style>` 앞 CSS ③ costGap 2 ④ 도우미 — 판 C 템플릿(M 줄 빼고)과 바이트 같을 때만 교체, 아니면 FAIL ⑤ 분기 표지) · `STEPS`·`chain()` 판 사슬 · `apply()` 사슬 일반화(`--layout` 없이 옛 판 FAIL 문구 `레이아웃 판 meta r2026-10-C ≠ config r2026-10-D — --layout 을 붙여 r2026-10-C → r2026-10-D`) · main 출력이 지나는 판 전부(`meta 없음 → r2026-10-B → r2026-10-C → r2026-10-D`) · docstring |
| `scripts/validate.py` | 497 → 502 | e38cd135 | `check_layout` M 줄 정규식에 `recent: {"01": K, "06": K}` = config `mobile.recent_days` 대조(판 C 꼴은 0건 FAIL) · PASS `r2026-10-D · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · 최근 14/14 · CSS 640` · docstring(이름·검사 수 24 그대로) |
| `tests/chart_check.py` | 516 → 733 | a6c7525a | 판 D 기대값: 390 처음(접힘) 01·06 최근 K일·라벨 2K/K·높이 K×row+pad·버튼 문구·aria-expanded·글꼴 = 03 summary / 01 버튼 진짜 누름 → 전 기간(06 그대로) → 다시 누름 → 처음과 같음·버튼 화면 y 그대로 / 06 펼침(01 그대로) / 둘 다 펼침 / **짧은 사본**(apply 로 01·06 배열을 K·K+1일로) / 1280 버튼 0 / 회전은 01 펼친 채 → 844(버튼 0) → 390 처음과 같음 / 인쇄 beforeprint 날짜 n·높이 min(n×row+pad, 1000) · afterprint 날짜 K / PDF 날짜 n 전부 · **기준(--base)도 맨 왼쪽으로 되돌려 PC 대조**(판 C 기준은 로드 때 최신 쪽) · `--out`·`--base` 면 기준 캡처 + **전후 비교 `compare.html`**(그림 내장 한 파일 · 높이 표) · 캡처 방식 full_page → 뷰포트 늘려 찍기 · 임시 폴더 항상 지움 |
| `tests/test_apply.py` | 436 → 500 | 43142397 | `ApplyLayoutC` → **`ApplyLayoutD`** 7(사슬 옛 → D · B/C → D 같은 바이트·`--layout` 없음 FAIL 문구·`chain()`·사슬 밖 FAIL · 손 수정 C(도우미 한 줄·costGap 줄·도우미 표지 둘) FAIL · 손 수정 D(분기 표지·M 줄 이름·판 C 꼴 M 줄) FAIL · 묵은 M 줄(recent 포함) → config · C → D 변환 범위(바뀌는 곳 = meta·버튼 CSS·costGap 2·도우미뿐) · B → C 중간 범위) · CLI 문구 · ApplyRehearsal `work/RD`(meta D) → **Ran 21 OK** |
| `SKILL.md` | 608 → 609 | b89d77ad | 원칙 판 `r2026-10-D` · 5단계 `--layout` 사슬·FAIL 문구 · 체크 3 판 D 한 줄 · 검산 "레이아웃 판" 판 D 줄(PASS 문구) · chart_check 줄 · 참고 파일(test_apply 사슬·chart_check). 7단계 게이트 문단은 판 이름이 없어 그대로 |
| `references/report-structure.md` | 596 → 624 | b0514cb7 | 절 제목 "레이아웃 판 r2026-10-D(… 2026-10-06·07)"·목차 앵커 · 표지·바꾸는 코드 줄 · 판 B 표 아래 "버튼은 details 가 아니다" · 판 C 끝 줄(이월 문장 → 판 D 가 풀었다) · **"판 D" 문단**(사용자 원문 · K일 · 버튼 문구·글꼴 · 가장자리 · 인쇄 · 배열 1벌 · M 줄 · 변환 · 글자 바꾸려면 묻기) · 01 모바일 모양 · 06 판 D 한 줄 |
| `references/css-and-layout.md` | 268 → 279 | 26ab2e84 | 유틸리티 `.chart-fold` · 접기 안내 6(버튼 — details 아님 · CSS · 마커 없음 · 접을 때 scrollBy · 인쇄) · 버그 8 끝 줄(기간 창 이월 → 판 D) · 버그 12 (7)(그리는 범위 자르기와 `ctx.chart.data` · 인쇄 재생성 animation false) · 재발 방지 ApplyLayoutD |
| `references/code-tab.md` | 244 → 245 | 6d43c94b | 3절 6단계 "판 C·D" · 4절 첫 적용 문단에 **판 D 첫 적용(직전 배포본 meta r2026-10-C)** + `work/chart_<날짜>/compare.html` (지시의 문서 목록 밖 — 다음 `/saero-run` 보류 회차가 읽는 자리라, 임의 결정 13) |
| `audit/checklist.md` | 528 → 534 | e60daf50 | 갱신 이력 한 줄(v4.7 유지) · [의도된 동작] 2 끝 · 27 판 D 문단(사용자 원문) · [되돌리면 안 되는 것] 판 C 분기 표지·M 줄 행(convert_c_to_d·ApplyLayoutD·M 줄 recent) · 인쇄 F 규약 행(접힌 차트 전 기간). [알려진 이월 항목]은 last-audit 정본이라 걸린 줄 없음 |
| `audit/last-audit.md` | — | (커밋 뒤) | 이 절 |

지시 밖 변경 0: `compute.py`·`compare.py`·`deploy.py`·`reportlib.py`·`narrative_check.py`·`precheck.sh`·`exclusions.py`·`fetch_reports.py`·`archive.py`·`ingest.sh`·`overflow_check.py`·`mutation_test.py`·`test_deploy.py`·`test_compare_sections.py`·`tests/fixtures/*`·`local/`·`data/`·`audit/exclusions.csv` 불변(`git diff --stat 38e0123 9db296a` 10파일 +683/−160). 06 블록(`CHART06_C`)·01 블록의 나머지·안내 스크립트·03·07·08 접기·PC 모양은 그대로.

### 임의 결정(번호 = 사용자가 바꿀 단위)
1. **접는 방법 = 도우미가 그리는 범위만 자르기**: `draw()` 가 `it.mobile()` 설정을 받은 뒤 `data` 를 `labels.slice(from)`·데이터셋 얕은 복사 + `data.slice(from)` 로 바꿔 그린다(배열 1벌 그대로 · 축 min/max 방식은 datalabels·막대가 창 밖에서도 그려져 숨김 처리가 더 든다). 그래서 **06 블록 `mobile()` 은 바꿀 것이 없다**(지시의 "CHART06_C 의 mobile()" — 자르기를 도우미 한 곳에 둠). 01 은 비용 라벨 간격(costGap)이 블록 `data` 를 읽어 범위 안 번호(`ctx.dataIndex`)와 어긋나므로 그 2곳만 `ch.data` 로.
2. **판 C 상수 보존**: `CHART01_C`·`CHART06_C`·`MOBILE_JS_C`·`M_LINE_C`·`m_line_c` 는 사슬 중간(B → C)에 그대로 쓰고, 판 D 는 `convert_c_to_d` 의 패치(costGap 2 · 도우미 교체 · CSS · meta). 덕분에 배포본 C → D 와 옛 판 → B → C → D 가 같은 바이트(R5 [실측]).
3. **판 C 도우미 대조**: 도우미 블록(`/* saero:mobile-helper` ~ 첫 `\n})();\n`)이 판 C 템플릿과 M 줄만 빼고 바이트 같을 때만 교체 — 손으로 바꾼 판은 `판 C 분기 도우미가 템플릿(M 줄 빼고)과 다름 — 손으로 바꾼 판으로 보임, 변환하지 않음` FAIL.
4. **버튼 모양**: `button` 요소 · `class="fold-more chart-fold"` · 차트 카드(`.card`) 끝에 붙임 · `display:block; width:100%; margin:2px 0 0; padding:6px 0`(손가락 누르기 높이 ≈30px) · 테두리·배경 없음 · `font-family:inherit` · **▶ 마커 없음**(03 은 summary 기본 마커 — 버튼에 넣으면 글자가 바뀌어 사용자 결정 몫).
5. **접을 때 버튼 자리 그대로**: 다시 누르면 위 차트가 줄어든 만큼 `window.scrollBy` 로 올려 버튼이 화면의 그 자리에 남는다(390 실측 y 406.8 → 406.8). 펼칠 때는 그대로(차트 위쪽 고정·아래로 늘어남 — details 와 같은 느낌).
6. **버튼 먼저 · 못 만들면 전 기간**: 카드를 못 찾아 버튼을 못 붙이면 접지 않는다(펼칠 길 없는 접힘 0 — 자체 검토 중 바꿈).
7. `aria-expanded` true/false(문구는 그대로).
8. **인쇄**: 접힌 차트만 beforeprint 에 전 기간으로 **애니메이션 없이** 다시 만들고(첫 그림이 동기라 판 C 의 `resize()` 가 미뤄지지 않음) 높이 캡 → afterprint 에 접힘으로 애니메이션 없이 다시 만든다. 펼쳐 둔 차트는 판 C 그대로(resize).
9. config 키 = 지시 예시 그대로 `mobile.recent_days`, M 줄 키 = `recent`.
10. validate PASS 문구에 `최근 14/14` 를 더함(운영 세션이 6단계 출력에서 값을 본다).
11. apply 출력의 사슬 문구는 지나는 판을 전부 적는다(`r2026-10-B → r2026-10-C → r2026-10-D`).
12. **chart_check**: 짧은 사본은 `apply.apply()` 로 만든 실제 HTML(브라우저 안 데이터 조작 아님) · 버튼은 playwright 진짜 클릭 · 전후 비교 페이지를 chart_check 가 직접 씀(이전 생성기 `feat-20261006-dailychart/work/P/mk_compare.py` 는 clone 정리로 없어짐 [실측] — 다음 보류 회차가 옛/새 캡처 비교를 내려면 저장소 안 도구가 필요) · 캡처 방식 변경(아래 리허설 R4 [실측]).
13. code-tab.md 4절에 판 D 첫 적용 한 줄(지시의 "같이 맞출 문서" 목록 밖 — 다음 `/saero-run` 이 보류·비교 페이지를 내는 근거 문장이라).

### 리허설 결과(전부 clone 안 사본, 최종 코드 — `work/RD/rehearse.sh`(34b84dc0) 두 번 돌려 md5 22줄 전부 같음) [실측]
- **R1** 재료: `work/prev.html` = 배포 `60d2aee`(f2519cbb · 판 C · 42일 — 배포 저장소 `git show 60d2aee:index.html` 과 cmp 같음) · combined 4(검색어 ff5033fd · 상세지역 dd3a7f11 · 시간대별 fab50354 · 키워드 330e47c7 — 운영 `work/` 읽기 복사) · compute `f643ff54`(운영 `work/compute.json` 과 같음).
- **R2** apply: `--layout` 없음 → `[FAIL] apply: ApplyError: 레이아웃 판 meta r2026-10-C ≠ config r2026-10-D — --layout 을 붙여 r2026-10-C → r2026-10-D` rc 1·파일 그대로 → `--layout` → `· 101,984 → 105,077자 · 레이아웃 판 변환(r2026-10-C → r2026-10-D, 분기 2)` **02e80dac** → 두 번째·`--layout` 없이 `(변환 건너뜀) (변경 없음)` 같은 md5 · 서술 표지 36 안쪽 바이트 같음 · 01/06 labels 날짜형 배열 2 · min-width 2곳 · details 5 · `<button` 0 · `getElementById` 01·06 각 1 · diff 덩이 16 = meta · CSS 3줄 · costGap 2 · 도우미뿐.
- **R3** precheck(`work/RD/index.html work/combined work/RD/prev.html`): **validate 24/24**(`[PASS] 레이아웃 판(…) — r2026-10-D · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · 최근 14/14 · CSS 640`) · **compare OK 99/DIFF 0** · overflow 넘침 0(밖 요청 6건 차단) · narrative `[주의] 같은 기간` · 도장 `02e80dac · f2519cbb · full`.
- **R4** `tests/chart_check.py work/RD/index.html work/RD/compute.json --base work/RD/prev.html --out work/RD/shots` → **PASS 27 / FAIL 0 · 외부 요청 허용 2 · 차단 0**:
  390 처음 01 `y · 날짜 14/42 · ticks 14 · 라벨 28/28 · 밖 0 · 글자 겹침 0 · padding 0(기준 0) · 제목 띠 0 · 높이 454 = 14×26+90 · 맨 위 10/6(화) · 맨 아래 9/23(수) · 버튼 '이전 28일(8/26~9/22) 펼치기' aria-expanded false · 글꼴 = 03 summary` / 06 `14/14 · 378 = 14×22+70` 같은 꼴 /
  01 펼침 `42 · 84/84 · 1182 = 42×26+90 · 맨 아래 8/26(수) · 문구 그대로 · aria-expanded true` + 06 처음과 같음 / 01 다시 접힘 = 처음과 같음 · 버튼 화면 y 406.8 → 406.8 / 06 펼침 `42/42 · 994` + 01 그대로 / 둘 다 펼침 캔버스 8/8 · 문서 폭 390 /
  짧은 사본 14일 01·06 버튼 0·전부 · 15일 `이전 1일(9/22~9/22) 펼치기` · 처음 14일 /
  1280 01 S `scrollLeft 2538 = 3360−822 · 첫 화면 10일 9/27~10/6` · 맨 왼쪽 = 기준(`chartArea [64.2, 24, 3286.7, 221.4] · 8/26~9/4 · 84/84 · 3360×280`) · 06 S `2923 · 10/1~10/6` · 맨 왼쪽 = 기준 · 섹션 841/589 = 기준 · 버튼 0 /
  회전 01 펼친 채 390 → 844 `01·06 x · ticks 42 · scrollWidth 3360 · 끝 · 뱃지 · 버튼 0` → 390 처음(접힘)과 같음(버튼 2 · aria false) /
  인쇄 390(A4 · 0.4in) beforeprint 01 `날짜 42 · 높이 1000 = min(1182, 1000) · 비트맵 656×2000` · 06 `42 · 994` · afterprint `14 · 454 / 14 · 378` · 뒤 상태 처음과 같음 · **PDF 16쪽 — 01 벡터 행 42/42 2쪽 · 06 42/42 8쪽 · 둘 다 최신 위** · 1280 PDF 이미지 구성 = 기준.
  높이 390(섹션 1 · 6 · 문서): 기준 1,772 · 1,589 · 11,697 → 처음 **1,076 · 1,005 · 10,417** → 둘 다 펼침 1,804 · 1,621 · 11,761. PNG 10장 두 번 같은 md5(01 처음 0bf14735 · 06 처음 8f84bb66 · 01 펼침 4318e4bd · 06 펼침 925d401d · 1280 = 기준 75c9eb55·085b682c) · **전후 비교 `work/RD/shots/compare.html` 5f37cbae**(옛 판 · 새 판 처음 · 새 판 펼침 나란히 + 높이 표, 3.4MB).
  캡처 방식 [실측]: full_page 캡처는 같은 페이지 두 번째부터 창이 순간 4×4 로 바뀌는 resize 가 와 Chart.js 가 다시 붙으며 애니메이션 첫 프레임(막대 0)이 찍혔다(차트 id 그대로·판정 수치 그대로 — 시험 도구 몫) → 뷰포트를 문서 높이로 잠시 늘려 찍기로 바꾼 뒤 펼침 PNG 도 두 번 같은 md5(로드 상태 PNG 는 바꾸기 전과도 같은 md5).
- **R5** 옛 판 사슬(배포 저장소 실물 + 같은 합본 42일 compute): `037aca8`(meta 없음) `레이아웃 판 변환(meta 없음 → r2026-10-B → r2026-10-C → r2026-10-D, details 5 · 분기 2)` · `014472d`(B) `r2026-10-B → r2026-10-C → r2026-10-D` · `479d866`(C) `r2026-10-C → r2026-10-D` — 셋 다 rc 0 · 두 번째 (변경 없음) · **차트 스크립트(01·06 블록·도우미·M 줄) = R2 결과와 바이트 같음** · validate "레이아웃 판" PASS · validate 23/24(`08·09번 각주 N회 차이` FAIL) · compare DIFF 2(`10 desc` · `10 파트너 마지막날`) — 41일 기준 옛 서술을 42일 값에 둔 것(판 C 만 바꾼 479d866 도 같음 — 판 D 무관, 실제 회차는 n<날짜>.py 가 서술을 바꾼다).
- **R6** test_apply **Ran 21 OK**(ApplyRehearsal `work/RD` 포함, skip 0) · `test_compare_sections.py work/RD/index.html work/RD/compute.json` 5경우 전부 맞음.
- **R7** 실제 환경(20:32 KST): `deploy.py push --file work/RD/index.html --base work/RD/prev.html --message "…" --dry-run` → `precheck 도장 = 작업본 md5 02e80dac… · 직전 배포본 f2519cbb… 확인` · **`[주의] 레이아웃 판이 바뀜 — 실제 push 에는 --layout-change(사용자가 작업본 화면을 본 뒤) · 직전 배포본(--base) r2026-10-C → 작업본(--file) r2026-10-D`** · 배포본 = --base md5 확인(sha e8a1ab62) · 자격 증명 확인됨(출처: git) · 쓰기 권한 참 · `[dry-run] PUT을 보내지 않음` rc 0.

**병합 전 전체 시험 한 번**(20:27~20:31 KST, `work/RD/fulltest.sh` 16bc4c4b — 결과 `work/RD/full/`): test_exclusions OK(registry md5 fe0aa09c 전후 같음) · **test_deploy Ran 21 OK**(GIT_* 제거·`GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`) · test_ingest OK(data/ 12파일 같음) · test_fetch_reports OK(data/2026-09·config 같음) · test_narrative_check OK · test_validate_07 OK · test_apply 21 OK · py_compile 21/21 · `bash -n` ingest·precheck 통과 · config `json.load` 통과 ·
**mutation_test rc 1** — `[SKIP] 01 첫 .ctr-high 제거 — 변조 위치를 못 찾음` · `[UNCOVERED] 01번 클릭률 4% 이상에만 .ctr-high` · `[OK]` 51 · config 실험 layout_id·max_px FAIL 1씩 · 원본 md5 같음 → **같은 데이터로 origin/main 코드(분리 worktree, 끝에 지움)도 rc 1 · 같은 SKIP·UNCOVERED · [OK] 51** — 이번 01 표 5행(10/2~10/6) CTR 이 전부 4% 미만이라 `.ctr-high` 가 0(배포본 60d2aee 도 0)인 데이터 탓, 판 D 무관 → 이월 4.
md5 전후: `cat data/*/*.csv audit/exclusions.csv | md5sum` **39493a38** 전 = 후 · registry fe0aa09c · config 5a01e26d → **b9be593d**(새 키·layout_id·_comment 뿐) · chart_check 는 전체 시험 뒤 캡처 방식만 바꿈(리허설 R4 가 최종).

### 자체 검토(지시의 [검토 깊이 규칙] — 독립 검토자 1(opus · 읽기만 + 사본 탐침) + 조정자)
**막음 0** — "다음 단계로 가도 된다". 검토자 근거 [실측]: 접힘 상태 01 라벨 28·06 14 의 글자가 원래 배열의 같은 날짜 값과 같음(10/6 421·11,602원·1.52) · 01 펼침 + 06 접힘에서 beforeprint → 06 만 42일·994, 01 1000 · afterprint 뒤 06 14·378, 01 1182 복원 · 06 두 번 누름·1280 → 390 축소에서 접힘부터 · convert_c_to_d 앵커 정확히 하나·CRLF 면 FAIL(조용히 안 지나감) · validate 가 판 C 꼴 M 줄을 0건 FAIL · 문서의 출력 문구 = 코드. 조정자가 고친 것(검토 중): 임의 결정 6(버튼 먼저) · chart_check 기준 대조 자리·캡처 방식(시험 도구).

### 이월(한 줄씩 — 막음 아님, 첫 실사용(보류 회차) 뒤 또는 정기점검)
1. beforeprint 가 오지 않는 인쇄 경로(iOS 공유 → PDF 등 [추론])는 01·06 이 최근 14일만 찍힌다 — 요란(버튼 문구 "이전 28일(…) 펼치기" 가 같이 찍혀 빠진 기간이 보임), 펼친 뒤 찍으면 전부 · 03 details 도 같은 이벤트에 기댐 — 첫 적용 보류 회차 실기기 "인쇄 미리보기" 항목.
2. 인쇄할 때 버튼 문구가 종이에 같이 찍힌다(날짜 누락 0 — 1 의 단서라 숨기지 않음, 숨길지는 사용자 결정).
3. afterprint 가 오지 않는 브라우저면 `printing` 잠금이 풀리지 않아 버튼·회전 판정이 멈춘다(차트는 전 기간 상태 — 손실 아님, 판 C 와 같은 잠금).
4. mutation_test 에 판 D M 줄 변조(recent 빠짐·값 어긋남)가 없다 — validate 코드는 둘 다 FAIL 로 잡음(test_apply 는 apply 쪽만) · 01 `.ctr-high` 변조는 데이터에 따라 SKIP(이번 10/2~10/6) — 정기점검 때 변조 위치를 다른 자리로.
5. 펼친 차트를 애니메이션 중(누른 뒤 약 1초 안)에 인쇄하면 판 C 이월 2 와 같은 길(resize 가 다음 그리기로 미뤄짐 — 1,182px 비트맵이 1,000px 에서 잘림, 접힌 차트는 이번에 애니메이션 없이 다시 만들어 해당 없음).
6. 펼칠 때 캔버스가 화면 밖이고 버튼만 보이는 자리에서 누르면 브라우저 스크롤 고정(Chrome)이 버튼을 잡아 차트가 위로 늘어난 것처럼 보일 수 있다 [추론] — 실기기 확인 몫.
7. 버튼에 03 summary 의 ▶ 마커가 없다(임의 결정 4 — 넣으면 글자 변경이라 사용자 결정).
8. `tests/fixtures/layout_old.html` 머리 주석 "사슬 변환(옛 → r2026-10-B → r2026-10-C)" 이 판 D 를 안 적음(주석만 — 시험은 D 까지 돈다).
9. 탐색 기준선 A-6 의 남은 몫: 펼친 높이는 여전히 n 에 비례(행 높이 하한 없음) · 인쇄 F 의 n 상한(≈46일부터 06 도 1,000 캡에 걸려 행 간격이 준다) — 그대로.
10. 판 C 검증 이월(1·3·4·8 등)·구현 기준선 이월 1~8 은 그대로(다시 올리지 않음).

### 검증 회차가 볼 것(완료 기준 표 줄로 — 판정만, 쓰기 0)
1. 모바일 01·06 처음 최근 14일 · 높이 K×row+pad · 버튼 문구 "이전 N일(M/D~M/D) 펼치기" — chart_check 390(R4).
2. 펼치면 전 기간 · 보이는 라벨 누락 0 · 다시 누르면 접힘 — chart_check 390 펼침·다시 접힘·06 따로(R4).
3. 날짜 ≤ 14 면 버튼 없음 — chart_check 짧은 사본 14·15일(R4).
4. PC 모양 · 최신 쪽 스크롤 그대로 — chart_check 1280(판 C 기준 = `work/RD/prev.html`, 맨 왼쪽 대조).
5. 인쇄에 날짜 전부 · 뒤에 접힘 복원 — chart_check 인쇄(beforeprint 42 · afterprint 14 · PDF 벡터 42/42).
6. HTML 배열 · min-width · details 5 그대로, M 줄 = config — validate "레이아웃 판" · compare 01/06 labels(99/0) · test_apply ApplyLayoutD · R2 diff 덩이 16.
7. 실제 환경 리허설 — R1~R7(`rehearse.sh` 재실행 md5 22줄 같음 · R7 은 구현 세션 기록으로 확인 — 검증은 deploy 실행 0).
8. 문서 = 코드(출력 문구 셋 · 판 이름 · 개수).

### 마무리 기록(이번 회차)
- 커밋(경로 지정 add · `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`): `9db296a` 코드·시험·문서 · 그리고 이 절(기록 커밋 — 해시는 자기 참조라 적지 않는다).
- 끝 확인: `git fetch` → origin/main 확인 · 브랜치 push 1회(`feat-20261007-mobilefold`, main 아님) · 재clone 대조는 채팅 보고.
- 다음 단계: ④ 검증 `D:\saero-verify` 새 세션 **Fable 5.1 · ultracode** — 지시문 `D:\saero\saero-ad-report_01모바일기간접기_검증지시_회차1_2026-10-07.md` / ⑤ 수정(막음이 있을 때만) 새 세션 **Opus 5.5 · xhigh · ultracode 끔** / 재검증 새 세션 · 바뀐 것만 · **Fable 5.1 · xhigh** / ⑥ 병합은 검증 뒤·갱신 회차가 돌지 않을 때 / 설치본(`D:\saero\CLAUDE.md`·`saero-run`)은 `local/` 변경 0 이라 갱신 불필요(병합 뒤 사용자 몫 확인만).

### 첫 적용 본보기(운영 세션이 그대로 쓴다)
- 병합 뒤 운영 main 작업 폴더 `git pull --ff-only`(ingest·S0 의 "HEAD = origin/main" 이 막는다) → 다음 `/saero-run`(**Opus 5.5 · high · ultracode 끔**), 첫 말 **"판 D(01 모바일 기간 접기) 첫 적용 — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함"** — 데이터 회차와 같이 돌아도 된다(4 fetch = 판 C 배포본 → 5 `apply.py --layout` 출력 `레이아웃 판 변환(r2026-10-C → r2026-10-D, 분기 2)`).
- 6 precheck 기대: validate 24/24 · `레이아웃 판 … r2026-10-D · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · 최근 14/14 · CSS 640` · compare DIFF 0 · 도장 → **보류 멈춤**: `"$PY" tests/chart_check.py work/index.html work/compute.json --base work/prev.html --out work/chart_<날짜>`(기대 PASS 27 · 외부 허용 2·차단 0 — 날짜가 14 보다 많을 때) → **`work/chart_<날짜>/compare.html`(옛 판 · 새 판 처음 · 새 판 펼침 나란히)** 과 작업본을 보이고, 사용자는 폰(390 세로 · 버튼 펼치기·다시 접기 · 844 회전 뒤 접힘 · 인쇄 미리보기 — 이월 1·2)과 PC 로 본다.
- 사용자 **"배포"** → 7 `deploy.py push … --dry-run`(`[주의] 레이아웃 판이 바뀜 … r2026-10-C → … r2026-10-D`) → `push … --layout-change` → `verify --ref <커밋>` → 8 기록. 그 다음 회차부터 직전 배포본이 판 D — `apply --layout` 은 값·M 줄만, 게이트 조용히 통과(자동 배포 그대로).

---

## 갱신 회차 (2026-10-07 08:08~08:30 KST 무렵 — Code 탭 `/saero-run`, main 작업 폴더, 2-1 같음 "다시 계산") · **배포 없음(작업본 = 배포본)**
합본 `일별` 2026.08.26 — 10.06 (42일, 01:22 ingest 합본 그대로 — ① 수집 안 함) · 배포본 `60d2aee`(md5 f2519cbb) 그대로 · 집계 기간 `2026.08.26 — 10.06 (42일)`
S0 PASS(08:08) → 같은 날 01시 회차가 10/6까지 반영했고 10/7 집계는 10/8 01:00 뒤라 크롬 수집을 먼저 띄우지 않고 4 fetch(f2519cbb)·5a compute → 2-1 같음 → 앞 질문 → 사용자 답 "다시 계산" → 3 신규 0(노원키즈필라테스 최근 3일 [0,0,0] — 09-17 규칙대로 `excluded_groups` 밖) → 5-0a pull(3그룹 각 297 — 01시 등록 3개 반영, registry 파일 변경 0)·propose `--since 2026-10-07` → `[주의] 빈 창`(후보 0 · 재노출 판정 0) → ⓐ (1)~(4) 모두 0이라 묻지 않음 → 5 apply(`변환 건너뜀` · `변경 없음`) + `work/n1007.py` 다시 → 작업본 md5 f2519cbb = 배포본 → 6 precheck `[FAIL] 직전 배포본이 작업본과 같다`(md5 가드 — 정상, 같은 판 재배포 방지) → 7 PUT 0.
compute 차이: `work/c42/compute.json`(01시) ↔ 이번 — `신규변형후보` ["노원노부티필라테스"] → [](01시 회차에 경쟁사 표 41행으로 들어감) 하나뿐.
`--pending` 사용: 아니오 — 채팅 질문 1건(2-1 같음 앞 질문)
**효율: 벽시계 약 20분 · 도구 호출 약 15회 · 즉석 코드 약 15행**(제외 그룹 판정)
제외 검색어(5-0단계): 재노출 판정 0건 / 후보 0 → 등록 0 / registry 893행(변경 없음)
propose 창 2026-10-07~2026-10-06(빈 창) · 등록 미룸(사용자): 아니오
- 다음 회차: 10/8 01:00 KST 뒤 — `--prev ~/saero-fetch/downloads/2026-10-07` · propose `--since 2026-10-07` · 서술 본보기 `work/n1007.py`(지난 회차 값 = `work/c42/`).
- 다음에 볼 것(후보): 같은 날 데이터 회차가 이미 끝난 뒤 `/saero-run` 이면 ① 수집이 같은 기간을 다시 받는다 — 이번엔 세션이 ①을 건너뛰고 2-1부터 물었다(code-tab.md 3절 순서와 다름). 순서표에 "직전 회차가 같은 날 · 같은 masthead 끝이면 ① 전에 2-1" 을 둘지 다음 점검에서 판단.

---

## 갱신 회차 (2026-10-07 01:13~01:30 KST — Code 탭 `/saero-run`, main 작업 폴더, 데이터 회차) · **배포 완료 `60d2aee`**
합본 `일별` 2026.08.26 — 10.06 (42일) · 배포 커밋 `60d2aee`(직전 `479d866`, 파일 sha 35b041c → e8a1ab6) · 집계 기간 `2026.08.26 — 10.06 (42일)`
S0 전 `git pull --ff-only`(사용자 승인 — 8ba1c37 → **b62c112**, 작업 트리 깨끗 · 바뀐 local/prompt-polish 세 파일 = 설치본 cmp 같음) → S0 PASS → ① 수집 PASS(`--prev 2026-10-06` → `~/saero-fetch/downloads/2026-10-07`, 10/1~10/6 4개 · 노출 1,640) → ingest(보관본 push `227df2e`) → 4 fetch(배포본 `479d866` = 4492c1f4, meta r2026-10-C) → 5a compute → 2-1 다름(41 → 42일) → 3 신규 0 → 5-0a pull(3그룹 각 294)·propose `--since 2026-10-06` → ⓐ (2)·(4) 한 메시지 → 사용자 답 "보류 / 등록승인3개" → 등록 → registry 커밋 `f1c6ede` → 5 apply(`변환 건너뜀`) + `work/n1007.py`(narr_lib 서술 — 표지 36) → 6 precheck → 7 dry-run → push → `verify --ref 60d2aee…` 1회째 일치.
validate.py 검사 24개 전부 PASS · compare.py 차이 0(항목 99, 직전 배포본 인자 4492c1f4) · overflow 360/390/430 넘침 0(details 5개 연 상태) · narrative 표지 36개 · 매회차 24개 전부 교체 · 도장 f2519cbb · 4492c1f4 · full · 재수령본 md5 일치(f2519cbb)
`--pending` 사용: 아니오 — 채팅 질문 1건(승인 묶음 (2)·(4))
**효율: 벽시계 약 17분 · 도구 호출 약 35회 · 즉석 코드 약 90행**(그룹 판정 12 · 경쟁사 후보 대조 10 · 서술 입력 확인 20 · 서술 스크립트 `work/n1007.py` 약 45 — narr_lib 재사용)
2-1단계 다름(41 → 42일) / 제외 그룹 신규 후보 0(노원키즈필라테스 최근 3일 [0,0,0]은 09-17 규칙대로 `excluded_groups` 밖) / 01·06 min-width·라벨 apply 값(42일) / 11번 판정: 직전 7개 → 유지 7 · 뒤집힘 0 · 근거 소멸 0(10/5 노출 반등이 10/6 421회로 이어짐 — 이틀 연속 증가), 이번 7 + (참고) 2 / 12번 이월: 1번 상시 유지 · 2번 보류 유지(상계동 30회 이상 9/18 하루뿐) / 경쟁사: 신규 변형 "노원노부티필라테스" 행 추가(40 → 41행) · 10/6 첫 등장 상호 4종 보류 · 포미·포레 종결 · 포인트·아라·피오르 보류 유지(아래 경쟁사 판정 이력) / 사용자에게 요청한 값: 승인 묶음 (2)·(4)
**사용자 답 해석**: "보류"는 (2) 애매 후보 제안("보류")에 대한 답으로 읽음 — 배포 보류 아님(답 두 줄이 질문 (2)·(4) 순서와 같음). 이 해석으로 자동 배포.
제외 검색어(5-0단계): 재노출 판정 0건(등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0) / 후보 3 → 승인 3 → 등록 3 · verified 3(9/9) · 실패 0(description `saero 10-07`, 승인 파일 `work/approved_2026-10-07_012548.txt`) / registry 893행(+9)
propose 창 2026-10-06~2026-10-06 · 등록 미룸(사용자): 아니오
- **10/6 판 C 라이브 시크릿 창 확인**(10/6 마감 때 요청 · 답 없던 것): 사용자 이 세션 첫 말 "10/6 판 C 시크릿 창 확인: 좋음".
- 다음 회차: propose `--since 2026-10-07` · `--prev ~/saero-fetch/downloads/2026-10-07` · 서술은 `work/n1007.py` 본보기(META·11번 판정만 바꿈, 지난 회차 값 = 이번 compute → `work/c42/` 로 복사해 두고 쓸 것).
- 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고).

---

## 검증·병합 기록(2026-10-07 — 검토 비용 줄이기 작업 2(기록 보관 분리, 문서만): 검증 1(막음 0) → main 병합)

**병합**: `fix-20261007-archive`(`fd54459` — f2aec20 위 2커밋: `d4446e9` 나누기 · `fd54459` 수정 기록)를 main(`f2aec20` — 분기 뒤 main 변경 0, 01:10 KST 무렵 `ls-remote` 로 main = f2aec20 · 브랜치 = fd54459 확인 · 갱신 회차 돌지 않음)에 `git merge --no-ff` → 병합 커밋 **`3e5341a`**(부모 f2aec20 · fd54459, 트리 `1b11c1be` = fd54459 트리 — `git diff --stat fd54459 HEAD` 0 · f2aec20 대비 5 파일 +2,406/−2,352). 충돌 0(audit/last-audit.md 포함 — main 이 움직이지 않아 자동 병합). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`(전역 설정 변경 0). clone `D:\saero-verify\merge-20261007-archive`(`git clone -c core.autocrlf=false`). 사용자 병합 지시(2026-10-07, 검증 판정 "막음 0 → 가도 된다" 를 붙인 병합 지시문) 뒤 병합. 브랜치 `fix-20261007-archive` 는 지우지 않고 둔다. 문서·코드·config·data 재수정 없음(이 절 추가만). 위 작업 2 수정 기록의 "main 병합 안 함 — 지시에 없음" 은 당시 사실 — 원문 보존, 이 절로 정정(**2026-10-07 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고에). 에이전트 0(지시 "에이전트 0" — 'ultracode' 신호가 있었으나 확인만 남은 문서 회차라 워크플로를 띄우지 않음).

**검증 1**(별도 세션 — `D:\saero-verify`, Opus 5.5, 하위 에이전트 0, 스크래치 clone `D:\saero-verify\verify-20261007-costcut`, 행 번호 fd54459 기준): 작업 1(규칙 문서, origin/main f2aec20) 1~5 · 작업 2(기록 보관, fd54459) 1~5 전부 참 → **막음 0** → "다음 단계로 가도 된다". 요지:
- 작업 1: work-algorithm.md 승인한 6자리만(.bak 245행 035d452e → 249행 504ae634, 8절 그대로) · 다듬기 스킬 B-1~4 정본 = 설치본(diff -r 0줄 · md5 3/3 42ac79b5·627c9410·c278b027) · 메모리 C-1·C-2 · skill-audit 수정본 162행 d28bcea3 · diff 재생성 일치 · AppData 현재 d28bcea3(사용자 업로드 동기화 = 정상값) · 문서끼리 예산·재측정·작은 작업·검토자·ultracode 같은 말.
- 작업 2: 독립 스크립트(줄비교.py 안 씀)로 잃은 줄 0(옛 4,256 = 남김 1,906 + 보관 2,350, 개수까지) · 남긴 쪽 = 옛에서 6구간만 뺀 것 · 6구간 md5 a1c290be·fc96ffb4·c94302c7·03f7a8a7·e531ac7b·704b0c27 옛 = 보관 · 보관 = 6구간을 이은 것(94f5ee7f) · CRLF 0 · 가리키는 곳 전부 살아 있음(남긴 절·고친 경로 2·끝 보관 절 → 보관 1028행) · scripts·tests·config 의 last-audit 읽기 0 · 열린 이월 사라짐 0 · 1,030,679 → 552,051바이트(d4446e9) · wrapup·saero-run "맨 위에 쓰기" 그대로(새 1-1015행 = 옛 1-1015행).

**병합 main 확인**(문서만 바뀐 회차라 이것만 — 시험 재실행 없음) [실측 01:12~01:15 KST]:
- 병합 트리 = fd54459 트리(`1b11c1be` · `git diff --stat fd54459 HEAD` 0줄).
- `cat data/*/*.csv config/*.json audit/exclusions.csv | md5sum` 병합 전 main(f2aec20) = 병합 뒤 **`eeb3587c`**.
- `git diff --name-only f2aec20 HEAD -- scripts tests` 0 — 바뀐 파일은 audit/archive/last-audit_~2026-10-05.md(새) · audit/checklist.md · audit/last-audit.md · references/exclusion-ui.md · references/report-fetch.md 5개뿐.
- audit/last-audit.md(이 절 전) **1,959행 · 563,987바이트** · CR 0 · 보관 파일 md5 **`94f5ee7f`**.
배포 PUT 0 · 네이버 0 · 운영 작업 폴더 `D:\saero` 쓰기 0.

**이월**(한 줄씩 — 검증 1 판정의 이월 2줄):
- skill-audit 기능 추가 회차(조정 세션 · ⑥ 탐색)가 외부 쓰기 여부를 가르지 않아, 화면·문서 기능을 그 길로 열면 work-algorithm:17(작은 작업 — 조정·탐색 세션 없음)과 갈림 — 가끔(사용자가 그 길로 열 때만).
- last-audit(fd54459):1638(09-26 진단 마무리) "09-07 기준선 이하는 '이전 기록' 표제 아래 원문 보존" 이 이제 일부만 맞음(나머지는 보관 파일) — 원문 보존이라 못 고침, 끝 보관 절이 안내 — 여러 우연.

**병합 뒤**(이 병합 세션은 하지 않았다): main 작업 폴더 `D:\saero\saero-ad-report-skill` `git pull --ff-only` 는 다음 운영 세션 몫(ingest 시작 검사 "HEAD = origin/main" 이 막는다) · local/ 변경 0 → 설치본 갱신 불필요.
효율: 벽시계 약 10분 · 도구 호출 약 12회 · 하위 에이전트 0 · 즉석 코드 약 15행(덧붙이기 조각 — 스크래치).

---

## 수정 기록(2026-10-07 — 검토 비용 줄이기 작업 2: 기록 보관 분리, 문서만) · 브랜치 `fix-20261007-archive`
**사용자 요청**: 지시문 `D:\saero\saero-ad-report_검토비용줄이기_작업2_기록보관_2026-10-07.md`(last-audit 를 작게 — 지난 회차 절을 보관 파일로, 지금 쓰는 절만 남김. 지시의 "4,241줄"은 작업 1 기록 전 값, `f2aec20` 은 4,256행). 세션 00:37~01:05 KST 무렵, Code 탭 `D:\saero`, Opus 5.5. 시작 확인 : `origin/main` 맨 위 = `f2aec20`(작업 1 기록) · 그 아래 병합 `92c7837` → 시작 조건 충족. 에이전트 0. 외부 쓰기 = 스킬 저장소 브랜치 `fix-20261007-archive` push 만(main 병합 안 함 — 지시에 없음 · 배포 PUT 0 · 네이버 0). scripts · tests · data · config · registry · local/ 변경 0. 운영 작업 폴더 : 시작 확인 때 `git fetch` 1회(원격 추적 ref 만 — HEAD `8ba1c37` · 작업 트리 그대로, origin/main 보다 5 뒤 — pull 은 다음 운영 세션 몫). clone `D:\saero\fix-20261007-archive`(`git clone -c core.autocrlf=false`).
**나누기 커밋 `d4446e9`**(f2aec20 위 1커밋, 5파일):
- `audit/last-audit.md` 4,256행 · 1,030,679바이트 · md5 8b6b3ef6 → **1,915행 · 552,051바이트 · 17551b6a**(= 남긴 1,906행 + 맨 끝 "보관 파일" 절 9행). 남긴 옛 행 : 1–1015 · 1725–1957 · 2050–2053 · 2669–3017 · 3142–3309 · 3679–3815(순서 그대로).
- `audit/archive/last-audit_~2026-10-05.md` 새 파일 **2,350행 · 482,098바이트 · 94f5ee7f** = 옛 1016–1724 · 1958–2049 · 2054–2668 · 3018–3141 · 3310–3678 · 3816–4256 을 순서대로 이은 것(머리말 없음 — 구간마다 보관 행 · md5 · 제목은 last-audit 끝 "보관 파일" 절).
- `references/exclusion-ui.md` 4행 · `references/report-fetch.md` 5행 : 경로 `audit/last-audit.md` → `audit/archive/last-audit_~2026-10-05.md`(절 이름 · 절 번호 그대로). 173행 1f382675 · 112행 8abab00b.
- `audit/checklist.md` 16행 새 줄(개정안 14 머리 단락 끝) : "날짜로 보관"은 개정안 14 와 다른 일 · 14 는 그대로 이월. 528행 aafc5804. 버전 줄 그대로.
**남긴 것과 까닭**(지시 2):
① 1–901 = 2026-10-06 이후 회차 전부 — 지시의 "리포트 읽기 쉽게 탐색 기준선 끝"(886행) 뒤 887–901(10-06 질문 다듬기 수정 기록 · 10-06 09:24 갱신 회차)도 10-06 이라 남김(보관 파일 이름 ~10-05 와 맞춤).
② 본보기(아래 참조 표) : 916–925 수정·병합 기록(2026-09-30) · 932–971 2026-09-29 후속 두 절 · 1725–1923 기능 추가 탐색 기준선(Code 탭 전 단계 실행).
③ 운영 표 : 3016 "# 이전 기록 (2026-09-07 저녁 기준선 … 현행 운영 표 …)" 머리 줄 · 3142 개선안 표(그 머리 줄이 운영 표로 지정) · 3156 등록 제외 검색어 대조 목록 · 3679 경쟁사 판정 이력.
④ 열린 이월 : 최신 점검 기준선 2709–3015(2026-09-26 진단 — 개선안 · 효율 개선안 · 점검표 개정안 · 다음 점검에서 대조할 것 · [수정 회차에 적용할 것], skill-audit 조정 0단계가 읽는 자리) + 그 뒤(09-27~10-05) 회차의 이월 · 다음에 볼 것 · 첫 실사용에서 볼 것이 든 절 — 다음 정기점검이 아직 거르지 않았으므로 항목별 닫힘 판정 없이 절째 남김 : 902–915(10-05 · 10-01) · 926–931(09-30) · 972–978(09-29 첫 실사용) · 979–1015(검증·병합 09-29 Code 탭 — 이월 목록) · 1924–1957(보고서 자동 수집 C 머리 + 검증·병합 — 이월 · 첫 실사용에서 볼 것) · 2050–2053(그 다음에 볼 것 — 2회차 후보) · 2669–2708(제외 검색어 검증·병합 · 첫 실사용 기록 — 이월).
⑤ 남긴 요약 절이 "상세 = 아래 '## … 갱신 회차' 절"로 가리키는 하단 상세 절 3192–3309(10-06 오후 · 10-06 · 10-05 · 10-01 · 09-30 · 09-29).
옮긴 쪽 이월 대조 : Code 탭 수정 기록 2 · 3 · 4 와 구현 기록의 "(새로) 내가 고를 항목"은 고르기 목록 — 조정 결정(보관 230행 "사용자 결정(조정)")과 남긴 검증·병합 기록(2026-09-29 Code 탭) 이월 목록의 "(수정 기록 4)" · "(이전)" 줄로 모였다. 09-07 기준선들의 개선안 · 다음 점검 목록은 2026-09-26 진단 "직전 기준선 판정"이 판정했고 미채택 개정안은 그 개정안 13 등으로 재상정됨(남김). 하단 09-28~09-12 갱신 회차의 "12번 이월 판정"은 리포트 12번 내용(최신은 10-06 절, 남김) · 09-28 "노원힐링장소." 는 남긴 이월 목록 "(이전)" 줄.
**참조 표**(지시 1 — 어디 → 어느 절 → 처리):
| 어디 | 가리키는 절 | 처리 |
|---|---|---|
| references/code-tab.md:5 | 기능 추가 탐색 기준선(Code 탭 전 단계 실행, 2026-09-28) 0~7절 | 남김 |
| references/exclusion-ui.md:4 | 기능 추가 탐색 기준선(제외 검색어 등록 자동화, 2026-09-27) 0~5절 | 옮김 · 경로 고침 |
| references/report-fetch.md:5(91행 "탐색 기준선 6-5" 는 5행을 따름) | 기능 추가 탐색 기준선(보고서 자동 수집, 2026-09-28) 1절 · 6-5 · 6-6 · 6-7 | 옮김 · 경로 고침 |
| references/report-structure.md:556 | 기능 추가 구현 기준선(리포트 읽기 쉽게 — 회차 1 글) | 남김 |
| local/prompt-polish/SKILL.md:142 · 이력.md:9 | 본보기 2026-09-29 후속 · 2026-09-30 절 | 남김 |
| local/prompt-polish/유난히큼.md:22 | 본보기 기능 추가 탐색 기준선(Code 탭 전 단계 실행) 0~7절 | 남김 |
| local/prompt-polish/이력.md:16 | 기능 추가 탐색 기준선(01 일별 추이 모바일 차트, 2026-10-06) | 남김 |
| SKILL.md:237 · 397 · references/report-structure.md:312 · 335 · 515 · 535 · exclusion-ui.md:158 · checklist.md:181 · 275 · local/prompt-polish/SKILL.md:65 · wrapup(설치본):28 · 29 | 등록 제외 검색어 대조 목록 · 경쟁사 판정 이력 | 남김(운영 표) |
| checklist.md:270~271 · skill-audit(AppData):30 | "개선안" 표 · "다음 점검에서 대조할 것" · 이월 개선안 | 남김(2026-09-26 기준선 + 운영 표) |
| saero-run(local/ = 설치본):11 · wrapup:16 · 30 · 35 · prompt-polish SKILL.md:35 · 44 · checklist.md:84 · skill-audit:101 · 150 · 메모리 saero-wrapup-feature-clone | 맨 위 절 · 최근 갱신 회차 절 | 남김(맨 위 1015행 옛과 같음) |
| SKILL.md:347 · code-tab.md:78 · checklist.md:7 · 12 · 149 · 418 · 434 · 462~469 · prompt-polish SKILL.md:48 · 156 · skill-audit:26 · 31 · 37 · 77 · 93 · 115 · work-algorithm.md:19 · 126 · 133 · 192 · 215 · 메모리 saero-audit-round-stop-rule · saero-handoff-prompt | 특정 절 아님(파일 · 절 종류 · 키워드 grep) | 해당 없음 — prompt-polish:48 은 이월 |
| 경로 없는 출처 표지(코드 · config · fixture — 바꾸지 않음) : scripts/fetch_reports.py:4 · 119 · compute.py:13 · ingest.sh:6 · 7 · 9 · precheck.sh:9 · deploy.py:34 · tests/test_deploy.py:9 · 14 · 271 · 324 · test_ingest.py:5 · 13 · test_fetch_reports.py:607 · fixtures/report-ui-fixture.html:18 · config/report-config.json:114 | Code 탭 수정 기록 2~4(N · W · X 번호) · 보고서 자동 수집 탐색 기준선 1절 · 6-5 · 6-6 · ③ · 6절 · 프로브 r10 | 옮김 — 보관 파일에 있음(끝 "보관 파일" 절 목록). "검증 1 결론 N" · "검증 2 참고 ①" 꼴은 저장소 밖 검증 보고 파일 — 해당 없음 |
| 경로 없는 문서 표지 : checklist.md:24~42 · 190 · exclusion-ui.md:48 · 173 · code-tab.md:165 | 수정 회차 2~4 · 제외 검색어 탐색 기준선 0절 · 그 수정 기록 2 | 옮김 — 고칠 경로 없음, 같은 목록으로 |
| last-audit 안(남긴 → 옮긴, 원문 못 고침 — 줄 비교) : 새 1018행 Code 탭 탐색 기준선 머리 '아래 "기능 추가 탐색 기준선(보고서 자동 수집)" 절 끝 사용자 결정(2026-09-28 저녁) 블록' · 그 밖 표지("수정 기록 2" · "탐색 기준선 4절" 등) | 보고서 자동 수집 탐색 기준선 끝 결정 · 각 표지 절 | 옮김 — 끝 "보관 파일" 절에 "보관 1028행"으로 적음 · 표지는 목록으로 |
| last-audit 안(남긴 → 남긴) : "상세 = 아래 '## 2026-10-06 오후 · 10-06 · 10-05 · 10-01 · 09-30 · 09-29 갱신 회차' 절" 6곳 · '기준 = 아래 "첫 실사용 회차" 절' · "# 이전 기록 … 운영 표" 머리 줄 | 하단 상세 절 · 첫 실사용 회차 · 운영 표 3개 | 남김 |
| scripts · tests · config 가 last-audit 를 읽는 곳(`grep -rn -E 'last.audit\|audit/' scripts tests config`) | — | 0곳(10/7 grep 과 같음 — registry `audit/exclusions.csv` 만) |
| D:\saero\CLAUDE.md · 메모리 MEMORY.md | — | 없음 |
**확인**(줄 비교 — 시험은 이것뿐, `D:\saero\.venv` Python 3.12) : `D:\saero\saero-ad-report_검토비용줄이기_작업2_줄비교.py`(54be44fa, 읽기만) — `git show f2aec20:audit/last-audit.md > old.md` · `git show d4446e9:audit/last-audit.md > new.md` · `git show 'd4446e9:audit/archive/last-audit_~2026-10-05.md' > arch.md` → `PYTHONUTF8=1 "$PY" <줄비교.py> old.md new.md arch.md <clone 루트>` → **전부 참 · rc 0** : 잃은 줄 0(옛 4,256 = 남김 1,906 + 보관 2,350 · 옛에만 0 · 새에만 0) · 옮긴 구간 6개 md5 = 보관 쪽 · 보관 = 구간을 순서대로 이음(94f5ee7f) · 남긴 줄 = 옛에서 구간만 뺀 것(1de4ae9d) · 맨 위 1015행 같음 · 가리킴 29줄(위 표의 경로 줄 · 운영 표 · 본보기 · 대표 표지 · last-audit 안) · 보관 1028행 = 사용자 결정(2026-09-28 저녁) · 남은 쪽 이월 머리 15개. 이 기록 절이 붙은 브랜치 끝 파일로 돌리려면 new 에 `--top-extra 44`(이 절 41행 + 빈 줄 · `---` · 빈 줄).
**맨 위 쓰기 그대로** : wrapup(설치본 `D:\saero\.claude\skills\wrapup\SKILL.md` 16 · 30 · 35 "맨 위 절") · saero-run(설치본 = local/ 사본, diff 0 — 11행 "맨 위 절을 읽는다") 원문 변경 0 · 나누기 뒤 1~1015행 = 옛 1~1015행 · "보관 파일" 절은 맨 끝.
**크기** : 1,030,679 → 552,051바이트(−46%) · 4,256 → 1,915행(이 기록 절 전).
**고치지 않고 적기만**(지시 4) : skill-audit 설치본(AppData, md5 070ea338 — 이 세션 실측) 26행 "last-audit.md(최신 기준선이 맨 위, 이전 기록 원문 보존)" — 이전 기록 일부가 이제 보관 파일(원문 그대로) · 30행 "다음 점검에서 대조할 것 · 이월 개선안"은 남긴 쪽. work-algorithm.md(읽기만) 19 · 126 · 133 · 192 · 215 "탐색 기준선 절"은 특정 절이 아님 — 고칠 것 없음.
**이월**(한 줄씩) : prompt-polish SKILL.md:35 · 156 "약 74만 자" 크기 문구(지금 약 55만 바이트) · :48 옛 결정 키워드 grep 범위에 보관 파일이 없음(옛 결정 일부가 보관 쪽) · checklist 120행 점검 대상 목록에 `audit/archive/` 없음(다음 진단이 "ls 다름"으로 알림) · 개정안 14(updates.md / registry.md 분리) 그대로.
**다음** : 마감 → 검증 `D:\saero-verify` 새 세션 · Fable 5.1 · ultracode(지시문 예산 에이전트 2개), 지시문 `D:\saero\saero-ad-report_검토비용줄이기_검증_2026-10-07.md` — 작업 2 는 브랜치를 clone(`git clone -c core.autocrlf=false -b fix-20261007-archive …`) → "가도 된다" 뒤 main 병합(`--no-ff`, 갱신 회차가 돌지 않을 때). 그새 main 맨 위에 갱신 회차 절이 붙었으면 맨 위 두 절이 같은 자리라 충돌(둘 다 살림 — 늦은 절이 위), 아래쪽 나누기는 겹치지 않는다. 병합 뒤 다음 운영 세션이 `git pull --ff-only`.
효율 : 벽시계 약 30분 · 도구 호출 약 45회 · 즉석 코드 약 190행(나누기 스크립트 약 75 — 스크래치 · 줄 비교 약 115 — `D:\saero`) · 하위 에이전트 0.

---

## 수정 기록(2026-10-07 — 검토 비용 줄이기 작업 1: 규칙 문서, 문서만) · 브랜치 `fix-20261007-rules`
**사용자 요청**: 지시문 `D:\saero\saero-ad-report_검토비용줄이기_작업1_규칙문서_2026-10-07.md`(A~E — 배경: 10/6 하루 기능 회차 세 벌에 탐색 에이전트 37 · 검토 다섯 겹 · 커밋 42). 세션 00:05~00:40 KST 무렵, Code 탭 `D:\saero`. 에이전트 0(지시문 예산 "0개(혼자)" — 'ultracode' 신호는 지시문 본문 낱말이라 워크플로를 띄우지 않음). 외부 쓰기 = 스킬 저장소 push만(배포 PUT 0 · 네이버 0). scripts · tests · data · config · registry 변경 0, 운영 작업 폴더 쓰기 0(HEAD `8ba1c37` 그대로 — origin/main 보다 뒤, pull 은 다음 운영 세션 몫).
**A. 작업 알고리즘**(`C:\Users\UserX\.claude\work-algorithm.md`, 저장소 밖): 전·후를 보인 뒤 사용자 "전부 승인" → 사본 `work-algorithm.md.bak-20261007`(245행 035d452e) → **249행 504ae634**. 바뀐 자리 : 1행 머리 꼬리 "· 작은 작업 · 재측정" · 17행 1절(새 줄 — 외부 쓰기를 바꾸지 않는 화면·문서·검사 수정은 새 기능이어도 작은 작업, 탐색·조정 세션·지시문 검토자 대조 없음) · 46행 2절 요령 1 끝 반 줄(질문·조정 세션도 길어지면 새 창) · 56행 3절(새 줄 — 작은 작업은 ①~③을 작업 세션 하나로, Opus 5.5 · xhigh, B 구현 + A 4·5번) · 144행 7절 [검토 깊이 규칙](새 줄 — 리허설 밖 재측정은 막음 후보가 있을 때 그 후보를 확인하는 만큼만) · 163행 skill-audit 줄("4~6번과 6절 끝 예산 줄을"). 8절 예시 그대로. `.bak` 과 diff = 이 6자리뿐.
**B. 다듬기 스킬**(`local/prompt-polish/`): 커밋 `cc865f2`(세 파일 — 절차 4 유난히 큼 : 받는 곳이 ① 탐색·설계면 묻지 않고 혼자 확인 · 새 '작은 작업 상자' 줄과 모델 표 줄 · 틀 끝 [넘길 때 — 작은 작업] · 단계 표 ① 줄 예시 · `유난히큼.md` 16 · 26 · 34 · 49행 · 이력.md 10/7(2)) → 병합 `460c038` → 커밋 `a192ab2`(SKILL.md 한 줄) → 병합 **`92c7837`**(둘 다 `--no-ff`, 분기 뒤 main 변경 0 · 충돌 0). `wc -l` · md5 : SKILL.md 205 42ac79b5 · 유난히큼.md 56 627c9410 · 이력.md 17 c278b027. 설치본 `D:\saero\.claude\skills\prompt-polish\` = 정본(`diff -r` 0줄 · md5 3/3).
**C. 메모리**(D--saero): `saero-handoff-prompt` (3) 검토자 둘 대조는 외부 쓰기(배포·제외 검색어 등록·승인 자리)를 바꾸는 작업 지시문만, 그 밖은 혼자 한 번 — 검증 지시문 "렌즈 둘" 대조도 같은 범위 · `saero-audit-round-stop-rule` "ultracode 켜 둠" → 첫 깊은 검토 자리에만(① · ③은 외부 쓰기 작업만, ④ 첫 검증 — 10-07 좁힘) · MEMORY.md 2 · 5행 요약 같은 뜻.
**D. skill-audit 수정본**(`D:\saero\skill-audit-수정본_2026-10-07\`): SKILL.md 162행 **d28bcea3**(③ 끝 재측정 줄 · ⑥ 끝 예산 줄) · SKILL.md.diff · skill-audit.zip(올릴 판, 안에 `skill-audit/SKILL.md` 하나) · skill-audit-원본.zip(되돌릴 판). 이 세션은 AppData 설치본에 쓰지 않음(원본 159행 **070ea338**). 그 뒤 **사용자가 claude.ai 에 직접 올림**(2026-10-07 00:30 무렵 — 사용자 지정 → Skills → skill-audit ⋮ 제거 → + 추가 → Skill 업로드 → skill-audit.zip 8.8kB, 미리보기 이름·설명 같음 → 목록 6개 · 켜짐 확인). 00:35 실측 AppData 는 아직 070ea338(동기화 전 — PC 는 Code 세션 시작 때와 약 10분마다 받음).
- **검증 판정 기준(완료 기준 표 "원본 그대로" 줄)**: AppData `skill-audit/SKILL.md` md5 가 `070ea338…`(동기화 전) 또는 `d28bcea3…`(사용자 업로드 뒤 동기화 = 수정본)이면 정상, 그 밖이면 손상. uuid 폴더는 동기화로 바뀔 수 있어 `find /c/Users/UserX/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin -path '*skill-audit/SKILL.md'` 로 찾는다.
**문서끼리 대조**: work-algorithm ↔ `유난히큼.md` ↔ SKILL.md ↔ 메모리 ↔ skill-audit 수정본 grep(예산 · 재측정 · 작은 작업 · 검토자 · 켜 둠) — 같은 말.
**임의 결정**: ① 작은 작업 상자는 다듬기의 '큼' 두 갈래 반박도 하지 않음(A-3 "지시문 검토자 대조 없음"과 같은 뜻으로 읽음) ② 작은 작업 검증 = Fable 5.1 · ultracode(2절 ④ 첫 검증 그대로) ③ 작은 작업 상자는 '작음'(문서 글 한 곳 등)이 아닐 때만 — 작음은 그대로 ④ 단계 표 ① 줄의 "(화면 · 문서 · 검사만)" 예시를 "그 밖"으로(작은 작업과 겹치지 않게) ⑤ handoff 메모리의 검증 지시문 대조도 (3)과 같은 범위로.
**바로잡은 것**: 첫 병합 뒤 대조에서 [넘길 때 — 작은 작업] 의 "7절 [검토 깊이 규칙](… +150만)" 이 7절에 +150만이 있는 것처럼 읽혀 `a192ab2` 로 옮길 줄로 풀어 씀.
**다음에 볼 것**: stock 은 다듬기 스킬(`D:\stock\.claude\skills\prompt-polish`)과 메모리가 따로라 B · C 가 닿지 않고, work-algorithm · skill-audit 는 계정 · PC 공통이라 닿는다(사용자에게 알림). stock 메모리 `prompt-verify-before-commit`(모든 `docs\prompt_*.md` 두 갈래 반박)이 1절 작은 작업 줄과 화면 · 문서 작업에서 어긋남 — stock 세션 몫.
**다음**: 작업 2(기록 보관 분리) — 새 세션 `D:\saero` · Opus 5.5 · xhigh · ultracode 끔, 지시문 `D:\saero\saero-ad-report_검토비용줄이기_작업2_기록보관_2026-10-07.md` → 그 마감 뒤 검증 `D:\saero-verify` 새 세션 · Fable 5.1 · ultracode(지시문 예산 에이전트 2개), 지시문 `D:\saero\saero-ad-report_검토비용줄이기_검증_2026-10-07.md`.

---

## 갱신 회차 (2026-10-06 23:43~23:50 KST — Code 탭 `/saero-run`, main 작업 폴더, **01 일별 추이 모바일 차트 회차 1(판 C) 첫 적용 · 경로 C**) · **배포 완료 `479d866`**
합본 `일별` 2026.08.26 — 10.05 (41일) · 배포 커밋 `479d8666`(직전 `014472d`, 파일 sha 74a46bf → 35b041c) · 집계 기간 `2026.08.26 — 10.05 (41일)`
사용자 첫 말 "01 차트 판 C 첫 적용 — 경로 C — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함"(아래 구현 기준선 "첫 적용 본보기" 그대로 — 병합 세션이 쓴 지시문을 붙여 넣음). S0 전 `git pull --ff-only origin main`(사용자 승인 — f799bb6 → **1b6f069**, 작업 트리 깨끗 · config `report_layout.layout_id` = r2026-10-C) → S0 PASS → 수집·ingest 생략(오전 합본 그대로 — combined 4 e3a352a2·e70e5023·faac5a0a·b7d91858) → 4 fetch(배포본 `014472d` = **46e15c8a**, meta r2026-10-B · sha 74a46bf) → `cp` → 5a compute(**2446b7c0** · 41일) → 2-1 같음(41일) → 사용자 답(첫 말 안) "다시 계산" → 3 신규 0(노원키즈필라테스 최근 3일 [0,0,0]은 09-17 규칙대로 `excluded_groups` 밖) → 5-0a pull(3그룹 각 294개 · registry 884행 바이트 불변 665ad61f)·propose `--since 2026-10-06`(`[주의] 빈 창`, 후보 0) → ⓐ 해당 0(질문 없음) → **5 = `apply.py --layout` 1회**(`93,339 → 101,313자 · 레이아웃 판 변환(r2026-10-B → r2026-10-C, 분기 2)`, 서술 스크립트 없음) → 작업본 **4492c1f4 = 검증 리허설 R3 와 바이트 동일**(diff 범위 = R2 와 같음: meta · CSS 8줄 · 01·06 블록 · 도우미 · 안내 4줄 · M 줄 1건) → 6 precheck → **보류**(chart_check + 전후 비교 + 결정 11 질문) → 사용자 결정 11 답 → 사용자 "배포" → 7 dry-run(`[주의] 레이아웃 판이 바뀜`) → `push … --layout-change` 1회 → `verify --ref 479d8666…` 1회째 일치(재수령 sha 35b041c · md5 4492c1f4).
validate.py 검사 24개 전부 PASS(`[PASS] 레이아웃 판(…) — r2026-10-C · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · CSS 640` — validate 따로 실행으로 확인) · compare.py 차이 0(항목 99, 직전 배포본 인자 46e15c8a) · overflow 360/390/430 넘침 0(details 5개 연 상태) · narrative `[주의] 같은 기간 — 대조 생략(표지 36개 중 매회차 24개)` · 도장 4492c1f4 · 46e15c8a · full · 재수령본 md5 일치
`--pending` 사용: 아니오 — 채팅 질문 1건(결정 11 ①~④ — 보류 멈춤, 2-1 답은 사용자 첫 말에 있음)
**효율: 벽시계 약 7분 · 도구 호출 약 30회 · 즉석 코드 약 18행**(3단계 그룹 판정 12 · 서술 표지 전후 대조 5 · layout_id 확인 1 — chart_check 는 저장소 `tests/chart_check.py`, 비교 페이지는 기능 clone `mk_compare.py`(md5 622cb68a, 읽어 쓰기만))
2-1단계 같음(경로 C) / 제외 그룹 신규 후보 0 / 서술 그대로(표지 36개 직전 배포본과 바이트 같음 — 손 수정 0, summary·01·06 블록·M 줄은 apply 값 그대로) / 01·06 PC min-width 3280·라벨 그대로(모바일은 화면 분기) / 11·12번 판정·이월 변경 없음(같은 데이터) / 경쟁사 신규 변형 후보 [] / 사용자에게 요청한 값: 결정 11 ①~④
제외 검색어(5-0단계): 후보 0 → 승인 0 → 등록 0 · verified 0 · 실패 0 / registry 884행
propose 창 2026-10-06~2026-10-05(빈 창) · 등록 미룸(사용자): 아니오
- **chart_check**(`tests/chart_check.py work/index.html work/compute.json --base work/prev.html --out work/chart_1006`, precheck 밖 · gitignore): **PASS 18 / FAIL 0 · 외부 요청 허용 2 · 차단 0** — 390 01 `y · ticks 41/41 · 라벨 82/82 · 밖 0 · 글자 겹침 0 · padding 겹침 0(기준 1) · 제목 띠 0 · 높이 1156` / 06 `y · 41/41 · 41/41 · 높이 972` / 섹션 1 1,746 · 6 1,567(기준 901·866) · 문서 11,699(기준 10,153) / 1280 01 S `scrollLeft 2458 · 첫 화면 9/26(토)~10/5(월)`·06 S `2843 · 9/30~10/5` · 맨 왼쪽 = 기준 · 섹션 [841, 589] = 기준 / 회전 390→844→390 복원 / 인쇄 390 beforeprint 01 1000·06 972 · PDF 16쪽 01 벡터 행 {2: 41}·06 {8: 41} 최신 위 · 1280 PDF 13쪽 이미지 구성 = 기준 · 8 캔버스·pageerror 0. 리허설 R4 와 값 같음.
- **전후 비교**(`work/compare_1006.html` fbacd48f, gitignore — `--online`, 구역 01·06): 390 01 901 → 1,746 · 06 866 → 1,567 · 문서 닫힘 10,153 → 11,699px(12.0 → 13.9장)·열림 13,982 → 15,528 · 1280 01·06 841/589 그대로 · 문서 1280 닫힘 7,914 그대로. 수치는 리허설 R3 compare(d021661a)와 같음 — 파일 md5 차이는 캡처 이미지(실행마다 다름).
- **결정 11 답**(사용자 채팅 원문 — 위 "사용자 결정(2026-10-06 — ② 고르기)" 블록 끝에도 한 줄): ① 주로 모바일 ② 인쇄·PDF 안 씀 ③ 10/06 회차 2 시크릿 창(03·07·08 접기) 좋았음 ④ 01 세로 흐름 모양 괜찮음. → 검증 이월 3(Letter·여백 0.6in 이상에서 모바일 01 PDF 누락)은 사용 밖 · `print_max_height_px` 1000 그대로.
- 보류 멈춤 때 보인 실기기 목록(답 받지 않음 — 나열만): 390 세로 · 844 회전(가로 막대 → 세로 콤보 3,280 스크롤 → 복귀) · 접기 펼침 03·07·08 · 인쇄 미리보기(A4·기본 여백 41/41, Letter·0.6in 이상은 알려진 한계).
- **다음 회차**: 직전 배포본이 판 C(meta r2026-10-C)라 `apply --layout` 은 변환을 건너뛰고 값·M 줄만 바꾸며, 레이아웃 판 게이트는 조용히 통과한다(자동 배포 그대로) — `--layout-change` 는 쓰지 않는다. **chart_check 는 데이터 회차 6단계에 없다**(precheck 밖 — 검증·정기점검·다음 모양 회차 몫). 서술은 표지 기반(ⓑ). propose `--since 2026-10-06` · `--prev ~/saero-fetch/downloads/2026-10-06`.
- 기능 clone `D:\saero\feat-20261006-dailychart` 는 `mk_compare.py` 읽기만(쓰기 0, 지우지 않음) · `D:\saero-verify` 열기 0 · 네이버 쓰기 0 · 배포 PUT 1(위 커밋) · 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고).
- **마감**(2026-10-06 23:50 무렵): 기록 커밋 `1742b91`(스크래치 재clone 대조 일치 — last-audit 4,240행 aa81ebb0 · registry 665ad61f · config 5a01e26d). 라이브 시크릿 창 확인(390 세로 01·06 가로 막대·최신 위 / 844 회전 → 콤보 → 복귀 / PC 01·06 스크롤 오른쪽 끝 시작)은 요청했으나 마감까지 답 없음 — 다음 세션 첫머리에 사용자에게 확인. 운영 작업 폴더 HEAD = origin/main · 메모리 변경 없음(결정 11 답은 이 기록에).

---

## 검증·병합 기록(2026-10-06 — 01 일별 추이 모바일 차트 회차 1(설계안 A · 레이아웃 판 r2026-10-C): 검증 1(막음 0) → main 병합)

**병합**: `feat-20261006-dailychart`(`5cf79d6` — f799bb6 위 8커밋: 탐색 기록 3 `9838789` 탐색 기준선 · `7b12912` 사용자 결정 · `887b43c` 지시문 대조 + 구현 5 `9bbfd2c` apply·config·test_apply·fixture · `48fc991` validate·mutation · `57cf58b` chart_check 신설 · `073647c` 문서 · `5cf79d6` 구현 기준선)을 main(`f799bb6` — 분기 뒤 main 변경 0, 23:30 KST `ls-remote` 확인 · 갱신 회차 돌지 않는 시각)에 `git merge --no-ff` → 병합 커밋 **`ab03a3d`**(부모 f799bb6 · 5cf79d6, 트리 = 5cf79d6 와 동일 — `git diff --stat 5cf79d6 HEAD` 0 · f799bb6 대비 13 파일 +1,429/−62). 충돌 0(audit/last-audit.md 포함 — main 이 움직이지 않아 자동 병합). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`(전역 설정 변경 0). clone `D:\saero-verify\merge-20261006-dailychart`(`git clone -c core.autocrlf=false`). 사용자 병합 지시(2026-10-06 23:25 무렵, 검증 세션 채팅 원문 "지금 바로 다음 단계 하자") 뒤 병합 — 본보기 조건 "그날 아침 데이터 회차 뒤 + 첫 적용 바로"에서 날짜를 오늘로 당김: 오늘 데이터 회차(09:24)·회차 2 첫 적용(16:58, 배포 014472d = 판 B)이 끝났고 합본 41일(2026.08.26 — 10.05) 그대로라, 첫 적용(경로 C)을 이 뒤 바로 붙이면 리허설 R3 와 같은 입력(prev 46e15c8a · compute 2446b7c0 → `apply --layout` 4492c1f4)이 된다. **첫 적용 전에 10/7 아침 데이터 회차가 먼저 돌면** 5단계 `apply --layout` 이 B→C 로 바꾸고 7단계 게이트가 `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함` 으로 멈추고 묻는다(그 회차가 보류 회차 — chart_check·전후 비교를 보인 뒤 "배포" 답에만 `--layout-change`). 브랜치 `feat-20261006-dailychart` 는 지우지 않고 둔다. 코드·문서·config·data 재수정 없음(이 절 추가만). 아래 구현 기준선 "마무리 기록"의 `브랜치 push 1회(… main 아님)` 는 당시 사실 — 원문 보존, 이 절로 정정(**2026-10-06 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고에).

**검증 1**(`D:\saero-verify\saero-ad-report_검증_01차트_회차1_2026-10-06.md`, 별도 세션 — Code 탭·이 PC, Fable 5.1 · ultracode, clone `D:\saero-verify\feat-20261006-dailychart-1`, 대상 5cf79d6, 워크플로 에이전트 4 = 검토자 3(코드·검사 / 화면·인쇄·런타임 / 배포 흐름·문서) + 기계 확인 1(haiku), 막음 후보 0 이라 반박 단계 생략): 아래 구현 기준선 "검증 회차가 볼 것" 1~12 전부 참 · 리허설 R1~R8 재실행 md5 전부 기록과 일치(compute 2446b7c0 · index 4492c1f4 · chart_check PASS 18/FAIL 0 · 외부 요청 허용 2·차단 0 · mutation `[OK]` 52·config 실험 4 · R6 14건 · PNG 4·compare.html d021661a 까지) · 리허설 밖 재측정(판 고르기 14경우 문구·파일 불변 · 폭 320~1280 7개 누락 0 · 회전·창 축소 6회 복원 · A4 여백 0·1cm·0.4in·0.5in 인쇄 41/41 · 벡터 판정을 pypdf 좌표 + Chromium 뷰어 렌더로 증명 · 템플릿 예외 3종 번짐 0 · 게이트 흐름 코드 추적) · 구현 기준선 이월 1~8 전부 막음 아님 · **막음 0** → "다음 단계로 가도 된다". 이월 12건은 보고 전문에(아래 이월에 일부만). 짚을 것 하나: 이월 3 실측 — Letter 용지·A4 여백 0.6in 이상(쪽 콘텐츠 높이 < ≈1,010px)에서 모바일 01 이 PDF 에서 통째로 빠진다(같은 설정의 판 B 는 7.5~8.3일) · 한국 A4·기본 여백은 41/41 → 정상 흐름 밖으로 이월, 첫 적용 보류 회차 실기기 "인쇄 미리보기" 항목 · `print_max_height_px` 값은 사용자 결정 몫.

**병합 main에서 전체 세트 재실행** [실측 23:32~23:34 KST] — 이 PC(venv `D:\saero\.venv` Python 3.12.10), `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1`, `-W error::ResourceWarning`, test_deploy 는 GIT_* unset·`GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`·`GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`(실제 자격 증명 0 — 하네스 자체도 GIT_* 제거·가짜 urlopen). 재료는 검증 clone `work/` 에서 읽기만으로 사본(병합 clone `work/R3/` = 판 C index 4492c1f4·compute.json 2446b7c0 · `work/index.html` = 배포본 사본 46e15c8a(판 B) · `work/combined/` 4 검색어 e3a352a2·상세지역 e70e5023·시간대별 faac5a0a·키워드 b7d91858):
- 전체 시험 4: `tests/test_exclusions.py` **Ran 49 OK** rc 0(1.1초, registry md5 665ad61f 전후 동일) · `tests/test_deploy.py` **Ran 21 OK** rc 0(33초 — 17 + 레이아웃 게이트 4) · `tests/test_ingest.py` **Ran 10 OK** rc 0(64초, data/ md5 916f98c7 전후 동일) · `tests/test_fetch_reports.py` **Ran 15 OK** rc 0(100초, "OK" 줄로 판정, config md5 5a01e26d 전후 동일). skipped 0 · ResourceWarning 0.
- 회차 시험 4: `tests/test_apply.py` **Ran 19 OK**(11.8초 — ApplyLayoutC 5 + 판 C 앵커 4 + ApplyRehearsal `work/R3/` meta r2026-10-C, skip 0) · `tests/test_narrative_check.py` **Ran 7 OK** · `tests/test_validate_07.py` **Ran 6 OK** · `tests/test_compare_sections.py work/R3/index.html work/R3/compute.json` **전부 맞음** rc 0(5경우).
- `tests/mutation_test.py work/R3/index.html <combined 4>` rc 0 **"전부 살아 있음"**(36초) — 기준 24/24 · 커버리지 24/24 · `[OK]` **52**(변조 26 + 0건 가드 19 + archive 7) · config 실험 **4**(ctr 4→5 · date_sections [1,6]→[1] · layout_id → "레이아웃 판" FAIL 1 · `mobile.max_px` 640→641 → FAIL 1) · MISS/UNCOVERED/SKIP 0 · 원본 md5(html·CSV 4·data/ 12개) 전부 동일. 배포 저장소 현재 배포본(014472d = 판 B, meta r2026-10-B)으로는 돌리지 않음(config C 라 24번째 "레이아웃 판" FAIL 이 정상). deploy.py 는 test_deploy 안에서만.
- `tests/chart_check.py work/R3/index.html work/R3/compute.json --base work/index.html --out work/R3/shots`(precheck 밖, cdnjs 2건만) **PASS 18 / FAIL 0 · 외부 요청 허용 2 · 차단 0**(44초 — 390 01 41/41·82/82·밖 0·글자 0·padding 0·높이 1156 / 1280 섹션 [841, 589] = 기준 / 인쇄 390 01 벡터 행 {2: 41} 최신 위).
- `py_compile` scripts 12 · tests 9 = **21/21**(cfile 스크래치) · `bash -n` ingest.sh·precheck.sh 통과 · config `json.load` 통과.
- md5: `cat data/*/*.csv audit/exclusions.csv | md5sum` 병합 전 main = 병합 뒤 = 전체 세트 뒤 **`aa89297c`** · config/report-config.json **`5a01e26d`**(171행 — f799bb6 07562fde 와 차이는 `report_layout` 의 layout_id C·markers.mobile_branch·mobile 블록·_comment 뿐) · local/·data/·registry 변경 0(`git diff --stat f799bb6 HEAD -- local/ data/ audit/exclusions.csv` 빈 출력) · 작업 트리 변경 0(무시 파일 `work/` 뿐). 배포 PUT 0 · 네이버 0 · fetch_reports 실제 실행 0(시험 fixture 만) · 실제 자격 증명 0 · 운영 작업 폴더·작업 clone 열기 0(검증 clone 사본만).

**이월**(한 줄씩 — 나머지는 보고 전문 6절 12건):
- (검증 이월 1) validate `check_layout` M 줄 검사가 전체 꼴 리터럴만 세어 꼴이 다른 두 번째 `var M = {…}` 손 편집을 못 잡음(정상 흐름 밖) — `var M\s*=` 수 1 또는 mutation 0건 가드 1건 후보.
- (검증 이월 3·4) 인쇄 쪽 높이 경계 실측: A4 0.5in(≈1,026px) 통과 · 0.6in(≈1,007px) 01 탈락 · Letter 0.4in 01·06 탈락 — `print_max_height_px` 조정은 사용자 결정 재료 · chart_check 인쇄가 A4 0.4in 한 설정만 재므로 Letter·0.6in 을 같이 찍어 행 0 = FAIL 로 둘지(정기점검·다음 모양 회차).
- (검증 이월 8) test_deploy layout_gate 4건 fixture 는 r2026-10-B vs 없음/X — r2026-10-C 리터럴 0(코드가 `lf != lb` 하나라 같은 길).
- (검증 이월 2·7, 문서) apply 출력 3꼴·validate PASS 문구 원문이 SKILL.md·references 에는 축약 서술(모순 0) · PC 인쇄 일수 "≈8일"(report-structure·css-and-layout) ↔ 막음 기준 "≈8.9일" 표기 통일.
- (검증 이월 5·6·9·10·11·12) 회전 직후 0ms 인쇄는 PC 모양(≈8일 = B) · 이월 4 의 13배 거짓 FAIL 재현 안 됨 · 도우미 IIFE 예외 시 PC 모양 폴백 메모 · chart_check `--out` 때 빈 임시 폴더 · hex 색 세는 법(17/18) · PDF 보는 법(pdftoppm 없음 → Chromium 뷰어).

**병합 뒤**(이 병합 세션은 하지 않았다): ① main 작업 폴더 `D:\saero\saero-ad-report-skill` `git pull --ff-only`(운영 세션 몫, 첫 적용 전 — ingest 시작 검사 "HEAD = origin/main" 이 막는다) ② local/ 변경 0 → 설치본(`D:\saero\CLAUDE.md` · `D:\saero\.claude\skills\saero-run\SKILL.md`) 갱신 불필요 ③ **첫 적용 = 01 차트 판 C 첫 적용을 바로**(오늘 밤 또는 10/7 아침 데이터 회차 뒤 — 데이터 회차가 먼저 돌면 그 회차가 게이트 멈춤으로 보류 회차가 된다, 경로 A 는 쓰지 않는다) — 운영 세션 `/saero-run` Opus 5.5 · high · ultracode 끔, 첫 말 "01 차트 판 C 첫 적용 — 경로 C — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함", 본보기 = 아래 구현 기준선 "첫 적용 본보기" 절(4 fetch(직전 배포본 014472d = 판 B, 46e15c8a) → 5 `"$PY" scripts/apply.py --layout --html work/index.html --compute work/compute.json`(`레이아웃 판 변환(r2026-10-B → r2026-10-C, 분기 2)` · 기대 4492c1f4) → 6 precheck 기대 validate 24/24(`레이아웃 판 … r2026-10-C · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · CSS 640`) · compare OK 99/DIFF 0 · 3폭 · narrative `[주의] 같은 기간` · 도장 → **보류 멈춤**: `"$PY" tests/chart_check.py work/index.html work/compute.json --base work/prev.html --out work/chart_<날짜>`(PASS 18 · 허용 2·차단 0) + 전후 비교 `"$PY" /d/saero/feat-20261006-dailychart/work/P/mk_compare.py --old work/prev.html --new work/index.html --out work/compare_<날짜>.html --sections 1,6 --online`(622cb68a) + 실기기 목록(390 세로·844 회전·접기·인쇄 미리보기 A4 기본 여백) + 결정 11 ①~④ → 사용자 "배포" → 7 dry-run `[주의] 레이아웃 판이 바뀜` → `push … --layout-change` → `verify --ref` → 8 기록) ④ 그 다음 회차부터 직전 배포본이 판 C — `apply --layout` 은 변환 건너뛰고 값·M 줄만, 게이트 조용히 통과(자동 배포 그대로), chart_check 는 데이터 회차 6단계에 없다.
효율: 벽시계 약 15분(23:30 ls-remote → 23:31 clone·병합 → 전체 세트 23:32~23:34(병렬 7) → 기록·push) · 도구 호출 약 12회 · 하위 에이전트 0 · 즉석 코드 약 15행(py_compile·md5 조각 — 스크래치).

---

# 기능 추가 구현 기준선(01 일별 추이 모바일 차트 — 회차 1 A 가로 막대, 2026-10-06)
점검일: 2026-10-06 (기능 추가 회차 — **구현, 회차 1 = 설계안 A · 레이아웃 판 r2026-10-B → r2026-10-C**. 데스크톱 앱 Code 탭, 이 PC, 작업 폴더 `D:\saero`로 연 세션, Opus 5.5 · ultracode). 작업 clone `D:\saero\feat-20261006-dailychart`(탐색 clone 이어 쓰기, 브랜치 같은 이름). 시작 확인 [실측]: **HEAD = `887b43c`**(지시문의 `7b12912` 위 기록 커밋 1개 — `audit/last-audit.md` +4줄 "지시문 검토자 대조 결과", 코드 변경 0 · 시작 때 사용자에게 먼저 알림) · `git fetch` 뒤 origin/main = **`f799bb6`** 그대로(갱신 회차 기록 커밋 없음 → rebase 없음) · 재료 md5 20개 = 지시(`work/materials.md5` 19개 — work/index.html 46e15c8a · compute.json 2446b7c0 · combined 4 e3a352a2·e70e5023·faac5a0a·b7d91858 · M0 measure.py 97bc7ec2·base_measure.json a09d95f7·probe.json f1abda10 · P P_A.html 76593db4·A_measure.json 8a3f8b8c·A_390_sec1_start.png 28c0c33f·A_390_sec6.png 390d98bf·compare_A.html 432873ca·mk_compare.py 622cb68a·FACTS.md 31449c6b · W skep3r/exp_fix_print.json d0b5f9d6·F390_p2.png e5404c6b · revA/print_events.json 9283e051 + fixture `tests/fixtures/layout_old.html` f89b159d 는 할 일 4 로 바뀌므로 `work/materials_fixture_orig.md5` 에 887b43c 원본 값으로 따로). 운영 main 작업 폴더 열기 0 · `D:\saero\feat-20261006-layout` 열기 0 · data/·registry·local/ 변경 0 · 외부 쓰기 0(네이버·API·배포 저장소 요청 0, 키 파일·자격 증명 열지 않음, fetch_reports·exclusions·deploy(dry-run 포함)·ingest·archive 실행 0 — deploy 는 test_deploy 하네스 안에서만) · 브라우저는 playwright chromium 새 임시 프로필(CDN 2건만 허용).
설계: 탐색 기준선(아래 "기능 추가 탐색 기준선(01 일별 추이 모바일 차트)") 3.0 공통 뼈대 · 3.1 **A 열** · 4절 완료 기준 표 · 5절 막음 기준 · 6절 이월(반영분) · "사용자 결정(2026-10-06 — ② 고르기)" 1~12 전부 + 지시문 `D:\saero\saero-ad-report_01차트_구현지시_회차1_2026-10-06.md` 할 일 1~8. **B·C 안 · n 규칙(행 높이 하한·기간 창) · 01 인사이트 박스·서술 표지 블록 · compare.py·compute.py·deploy.py·test_deploy.py · validate 검사 수·이름 · 06 정의 · per_day_px · 배포본에 이미 실린 접기 주석 2곳 · local/ 은 건드리지 않았다.**
검증용 clone: `git clone -c core.autocrlf=false -b feat-20261006-dailychart --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill D:\saero-verify\feat-20261006-dailychart-1`
효율: 벽시계 약 90분(21:12 무렵 시작 확인 → 21:40 코드·chart_check 첫 실측 → 21:50 리허설 R1~R7 → 21:52~22:18 자기 검토 → 22:20 리허설 재실행·커밋 → 기록·push) · 도구 호출 조정자 약 90회 + 자기 검토 워크플로 에이전트 4개(검토 3 + 기계 확인 1(haiku), 하위 토큰 약 90만 · 도구 호출 177 · 25분) · 즉석 코드 약 650행(패치 스크립트 스크래치 ≈ 400 · `work/R3/rehearse.sh` 45 · `work/R4/r6.py` 110 · 인쇄 실험 `work/R3/try/exp_print.py` 40(지움) · 한 줄 조각 ≈ 50). 저장소 파일 `tests/chart_check.py`(516행)는 즉석 코드에 안 셈.
표기: [실측] 이번에 파일·명령으로 확인 / [추론] 확인 못 함. 행 번호는 이 브랜치 커밋 기준.

## 바뀐 것(파일별, `wc -l` 전 → 후 · md5 앞 8자리) [실측]

| 파일 | 행 | md5 | 무엇 |
|---|---|---|---|
| `config/report-config.json` | 158 → 171 | 5a01e26d | `report_layout.layout_id` "r2026-10-B" → **"r2026-10-C"** · `markers{details 5, mobile_branch 2}` · 신설 `mobile{max_px 640, print_max_height_px 1000, row_px{01 26, 06 22}, pad_px{01 90, 06 70}}` · `_comment` 판 C 줄. `recent_days`·`chart_min_width`(per_day_px 80) 그대로 |
| `scripts/apply.py` | 375 → 706 | 3c11daca | `LAYOUT_B`·`LAYOUT_C`·`BRANCH`·`M_LINE` · `MOBILE_CSS`(왼쪽 페이드 `::before` + `.at-start`) · **`CHART01_C`·`CHART06_C`**(제자리 PC 생성 + `window.__saeroMobileQ` 큐, `pc()`/`mobile()` 두 모양이 같은 `data` 하나) · **`MOBILE_JS`** 분기 도우미(M 줄 · matchMedia 기능 감지 · build/judge/scrollEnd · beforeprint 높이 캡 + 동기 resize · afterprint 복구 · 큐 소비 뒤 change 등록) · `AFTERPRINT`·`SYNC_JS` · `m_line`·`chart_block`·`check_branches` · **`convert_b_to_c`**(① meta ② `\n</style>` 앞 CSS ③ 01 블록 ④ 06 블록 ⑤ `\n});\n</script>\n` 의 `});` 뒤 도우미 ⑥ 안내 스크립트 4줄 ⑦ 분기 표지 2) · `apply()` 판 사슬(meta 없음 → `convert_layout(LAYOUT_B)` → `convert_b_to_c` · B + `--layout` → C · C 값만 · B + `--layout` 없음 → 새 FAIL 문구 · 사슬 끝 meta·details·분기 대조) · 매 회차 M 줄 once · main 출력 3꼴 · FOLD_CSS·FOLD_JS 주석 "r2026-10-B 이후" · docstring L6~23(사슬·M 줄·**앵커 정정: once 만 유일성, chart()/labels() 는 첫 일치**) |
| `scripts/validate.py` | 478 → 497 | 6cdc37f1 | `check_layout` 확장(이름 그대로 — 검사 24): 분기 표지 01·06 각 1(합 = `markers.mobile_branch`) · `matchMedia(` 문서 전체 1건 = M.maxPx 꼴 · M 줄 1건 = config mobile · CSS `@media (max-width: Npx){` 1건 = max_px. PASS `r2026-10-C · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · CSS 640` · docstring 23 |
| `tests/mutation_test.py` | 405 → 418 | 979f6864 | 변조 +1(분기 표지 06 주석 제거) · 0건 가드 +1(`var M = {` → `var MX = {`) · config 실험 +1(`mobile.max_px` +1 → 기준 사본 "레이아웃 판" FAIL) → **[OK] 52**(변조 26 + 가드 19 + archive 7) · config 실험 4 |
| `tests/test_apply.py` | 343 → 436 | 22666709 | 신설 `ApplyLayoutC` 5(사슬 옛 → C · B → C(--layout 없음 FAIL 문구 / 있음 = 사슬과 같은 바이트) · 손 수정(분기 01·06 제거·06 중복·M 줄 0) FAIL · 묵은 M 줄(641/999) → config 값 · 변환 범위(섹션 1~12·서술 표지·min-width 텍스트·head 는 CSS·meta 만)) · `test_missing_or_duplicate_anchor` +4(판 C 앵커 없음) · 리터럴: 출력 `레이아웃 판 변환(meta 없음 → r2026-10-B → r2026-10-C, details 5 · 분기 2)` · ApplyRehearsal `work/R3` + meta C · docstring → **Ran 19 OK** |
| `tests/fixtures/layout_old.html` | 475 → 478 | **89470872**(← f89b159d) | 안내 발췌에 판 C 앵커: `function updateEnd(box, wrapper){ … wrapper.classList.toggle('at-end', atEnd); }` 한 줄 · `function sync(){` 안 `box.parentNode.classList.add('at-end'); // 페이드 숨김` 한 줄(가짜 발췌 꼴 — `sync(){}` 가 세 줄로) · 머리 주석 2곳 |
| `tests/chart_check.py` | 신설 516 | 6f2b409f | 01·06 라이브 차트 확인(precheck 밖, 사용자 결정 8): 인자 `index.html compute.json [--base] [--out] [--widths 390,1280]` · 390 누락 0·글자 겹침 0·padding 겹침 ≤ 기준·제목 띠 0·높이·최신 위·뱃지 0 / 1280 S 최신 쪽 + 맨 왼쪽에서 = 기준 / 회전 390→844→390 / page.pdf(A4·0.4in) 벡터 행 또는 비트맵 이미지 · PC 이미지 구성 = 기준 / 8 캔버스·pageerror 0 / 외부 요청 허용 2·차단 0 · Chart.js 미로드 exit 2 · 캡처 섹션 1·6 PNG + PDF |
| `SKILL.md` | 600 → 608 | 99b632db | 원칙 판 `r2026-10-C` · 5단계 `--layout` 사슬·B 판 FAIL 문구 · 체크 3·4(배열·min-width 는 PC·HTML 그대로, 모바일은 화면 분기) · 검산 "레이아웃 판" 판 C 줄 · precheck 밖 chart_check 줄 · 참고 파일(test_apply·chart_check) |
| `references/report-structure.md` | 561 → 596 | d4cba21a | "레이아웃 판 r2026-10-C" 절(B 그대로 + 판 C 문단: 사용자 원문 · 가로 막대·최신 위 · 1벌 · 재판정 · 인쇄 F · S · 표지·M 줄 · 바꾸는 코드 · n 규칙 이월) · 목차 링크 · 01 절 "PC 모양"/"모바일 모양(판 C)" · 06 절 판 C 한 줄(제목 문구 그대로) |
| `references/css-and-layout.md` | 234 → 268 | 33222144 | `.scroll-fade` 줄 · 가로 안내 3(왼쪽 페이드)·시작 위치(S)·`window.__saeroSync`(PC 인쇄는 scrollLeft 를 따른다 — 자기 검토 정정) · 반응형 420px 줄 **삭제**(배포본에 없음) + JS 경계 = CSS 경계 = config · PWA 한 줄 · 버그 4·5(예외)·8(높이 비례) · **버그 12 신설**(1)~(6) [실측] |
| `references/code-tab.md` | 243 → 244 | a7190b44 | 3절 6단계 "chart_check 는 precheck 밖(4절)" · 4절 레이아웃 판 첫 적용 문단에 "판 C 첫 적용" + chart_check 명령 |
| `audit/checklist.md` | 519 → 527 | 80477db5 | 갱신 이력 한 줄(v4.7 유지) · 대상 파일 목록 `chart_check.py` · [의도된 동작] 2 끝 · 14 · 16(mutation [OK] 52·config 실험 4) · 17 · 27 회차 3 문단(사용자 원문) · 회귀 표 "순회" 문구 정정(check_date_labels 는 HTML 전체) · [되돌리면 안 되는 것] 2행(판 C 분기 표지·M 줄 = config / 인쇄 F 규약) |
| `audit/last-audit.md` | — | (커밋 뒤) | 이 절 |

지시 밖 변경 0: `scripts/compute.py`·`compare.py`·`deploy.py`·`reportlib.py`·`narrative_check.py`·`precheck.sh`·`exclusions.py`·`fetch_reports.py`·`archive.py`·`ingest.sh`·`tests/test_deploy.py`·`overflow_check.py`·`test_compare_sections.py`·`references/exclusion-ui.md`·`report-fetch.md`·`local/`·`data/`·`audit/exclusions.csv` 불변(`git diff --stat 887b43c --` 0줄). 배포본에 이미 실린 접기 주석 2곳(`<style>` 접기 주석 · 안내 `// 접기(details — 레이아웃 판 r2026-10-B)`)은 B → C 변환이 건드리지 않는다(C 판 배포본엔 옛 문구 그대로 — 지시).

## 임의 결정(번호 = 사용자가 바꿀 단위)
1. **분기 도우미 순서 = 큐 방식**: 01·06 블록은 제자리에서 `pc()` 로 만들고 `window.__saeroMobileQ` 에 `{key, canvas, data, pc, mobile, chart}` 를 넣기만, 도우미(차트 스크립트 끝)가 큐를 비운다. 지시의 "마지막 줄에서 큐를 비운다" 와 "change 등록은 큐 소비 뒤" 가 겹쳐 — 큐 소비 줄 바로 다음 줄(맨 끝)에 등록(동기 실행이라 동작 차이 0).
2. **노출 이름**: `window.__saeroSync = sync`(지시) · `window.__saeroMobile = {M, items, state, build, judge, scrollEnd}`(M 을 더함 — chart_check·실기기 디버그에서 기준값 확인용).
3. **회전 재판정 = destroy → 같은 data 로 재생성**(제자리 update 아님). 실패하면 `Chart.getChart(canvas)` 로 남은 인스턴스를 지우고 PC 모양 재시도, 그것도 실패하면 그대로(다른 차트에 안 번짐).
4. **beforeprint 재렌더 = 동기 `chart.resize()` + `update('none')`**(탐색 F 실험과 같은 호출) · 높이 = `Math.min(현재 style 높이, M.printMaxH)`(06 972px 는 그대로) · 인쇄 전 높이는 항목에 보관했다가 afterprint 에 되돌림.
5. **원래 높이도 `dataset.height` 로 보관**(지시는 `dataset.minwidth` 만 — PC 복귀 때 280/240 을 리터럴로 두지 않으려고). 둘 다 런타임 속성(HTML 텍스트 0).
6. **모바일 비용 라벨(01)**: 지시의 `anchor end · align right · offset 6` → **`anchor center · align right · offset = costGap(ctx)`**(점이 같은 행 노출 라벨 상자 안쪽이면 그 상자 오른쪽 끝 + 4px 뒤에서 시작, 아니면 8px). 지시 값 그대로의 첫 실측에서 390 01 **글자 겹침 1**(8/26 `497원`×`150`) · padding 겹침 2(기준 1 초과) · 제목 띠 침범 1(맨 위 행 비용 라벨이 위로 뜸) [실측] → 완료 기준 "글자 겹침 0·padding ≤ 기준·제목 띠 0" 을 지키려고. 결과 글자 0 · padding 0 · 제목 띠 0.
7. **06 모바일 라벨**: 지시의 `anchor end · offset 6` → `anchor center · offset 8` + 날짜축 `offset:true`(선 차트는 기본 false 라 맨 위 점이 chartArea.top 에 붙어 라벨이 제목 띠 침범 1 [실측]) · `layout.padding.right 40`(지시에 값 없음 — 프로토타입 P_A 값).
8. **모바일 선·점**: 01 `borderWidth 2 · pointRadius 4`, 06 `pointRadius 4`(프로토타입 P_A 값 — 지시의 데이터셋 줄에 없음). PC 는 `pc()` 가 매번 3·5 로 다시 씀(배포본 값 그대로).
9. `axes()` 가 모양을 바꿀 때 반대 축 ID 를 지운다(`xAxisID`·`yAxisID` 가 남으면 Chart.js 가 여분 축을 만든다).
10. **chart_check 세부**: 글자 상자 = datalabels `_box._rect` 에서 `_model.padding` 을 뺀 상자(탐색 SK1 방식) · `__ev` 훅 = `add_init_script` 가 `DOMContentLoaded` 에 리스너를 걸어 페이지 리스너(도우미·안내 스크립트) **뒤**에 돈다 · **PDF 판정 = 벡터 또는 비트맵**(Chromium 은 beforeprint 에 다시 그린 캔버스를 그리기 명령 그대로 PDF 에 싣는다 — 글자가 PDF 텍스트 [실측]; pypdf layout 추출 한 줄 토큰이 `날짜 노출 비용원`/`날짜 순위` 인 행이 한 쪽에 n 개·최신 위. 비트맵이면 beforeprint 비트맵 크기 이미지 1·보이는 비율 1·픽셀 > 0) · PC 대조 = 01·06 박스를 맨 왼쪽으로 되돌린 상태에서 `--base` 와 같음(S 로 첫 화면 날짜가 달라져서) + S 는 로드 상태로 따로 · PC PDF = 이미지 구성(크기·배치 수·보이는 비율) · 외부 요청 = 정확한 URL 2개 allow-list(file·data·blob·about 은 통과) · `--base` 없으면 padding 기준 1·대조 생략 · 캡처 = 섹션 1·6 clip 스크린샷(DOM 변경 0).
11. **M 줄 regex 꼴**: `var M = \{maxPx: \d+, printMaxH: \d+, row: \{"01": \d+, "06": \d+\}, pad: \{"01": \d+, "06": \d+\}\};`(apply·validate 같은 꼴, 키 순서 고정).
12. **apply docstring L17 은 정정**("once() 만 유일성 검사, chart()/labels() 는 첫 일치") — `labels: [` 둘 FAIL 검사는 넣지 않음(판 C 템플릿은 블록 안에 하나씩 — test_apply 가 블록당 `labels: [` 1 을 본다).
13. **분기 표지 ApplyError 문구** = `레이아웃 판 r2026-10-C 인데 분기 표지 N개(01 a · 06 b) ≠ config 2 — 손으로 바꾼 판으로 보임`(지시 문구 + 01·06 괄호) · 변환 직후는 `변환 뒤 분기 표지 …` · 사슬 끝에 meta = config 재확인 한 줄(`변환 뒤 레이아웃 판 meta … ≠ config`).
14. **validate 세부**: CSS 경계 = `@media\s*\(max-width:\s*(\d+)px\)\s*\{`(max-width 하나뿐인 쿼리 — 태블릿 `and (min-width: 641px)` 제외) 정확히 1 · matchMedia 는 문서 전체 `matchMedia(` 1건이면서 그것이 M.maxPx 꼴 · row·pad 도 M 줄에서 대조(PASS 문구에는 maxPx·printMaxH 만).
15. **B → C 앵커 꼴**: ⑥(a) 는 줄머리를 요구하지 않는 `([ \t]*)wrapper.classList.toggle('at-end', atEnd);`(fixture 한 줄 발췌에도 맞게) · ⑤ 는 `});` 뒤 빈 줄 하나 + 도우미 · (c)(d) 는 설명을 줄 끝 주석으로(4줄 유지).
16. 왼쪽 페이드 CSS 주석·도우미 주석에 경계 숫자(640)를 쓰지 않음(config 가 바뀌면 묵는다) · CSS·JS 주석에 태그 꺾쇠 0.
17. **리허설 파일 이름**: R6 = `work/R4/r6_01~11.html`·`r6_mstale.html`·`r6_branchless.html`·`r6_b_noflag.html`(스크립트 `work/R4/r6.py` e035926e) · R7 = `work/R4/prev.html`·`index.html` · 전체 = `work/R3/rehearse.sh`(2383519c → `work/R3/rehearse.log`).
18. `work/materials.md5` 는 work/ 19개만 — fixture 원본 md5 는 `work/materials_fixture_orig.md5`(`git show 887b43c:tests/fixtures/layout_old.html` 대조, 할 일 4 로 바뀌는 파일이라 끝 `md5sum -c` 가 실패하지 않게).

## 리허설 결과(전부 clone 안 사본, 최종 코드 — `work/R3/rehearse.sh` 두 번 돌려 같은 md5) [실측]
- **R1**: `work/materials.md5` 19/19 OK · `work/R3/{index,prev}.html` = 배포본 사본(46e15c8a) · compute(prev = R3/prev) `경쟁사 40행(신규 변형 후보 [])` **2446b7c0**.
- **R2**: `apply --layout` → `· 93,339 → 101,313자 · 레이아웃 판 변환(r2026-10-B → r2026-10-C, 분기 2)` **4492c1f4** → 두 번째 `레이아웃 판 r2026-10-C(변환 건너뜀) (변경 없음)` 같은 md5 → `--layout` 없이도 `(변경 없음)` 같은 md5 → 서술 표지 36 안쪽 바이트 전부 같음(`narrative_check.blocks`) · diff 범위 = L5 meta · L219 뒤 CSS 8줄 · 01 블록(L1966~2028 → 템플릿) · 06 블록(L2164~2192) · L2293 뒤 도우미 · 안내 4줄(L2322 뒤 · L2352 · L2367 뒤 2줄)뿐.
- **R3** precheck(`work/R3/index.html work/combined work/R3/prev.html`): **validate 24/24**(`[PASS] 레이아웃 판(…) — r2026-10-C · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · CSS 640`) · **compare OK 99/DIFF 0** · overflow 360/390/430 넘침 0(밖 요청 6건 차단) · narrative `[주의] 같은 기간 — 대조 생략(… 표지 36개 중 매회차 24개)` · 도장 `4492c1f4 · 46e15c8a · full`.
- **R4** `tests/chart_check.py work/R3/index.html work/R3/compute.json --base work/index.html --out work/R3/shots` → **PASS 18 / FAIL 0**:
  390 01 `indexAxis y · ticks 41/41 · 라벨 82/82 · 밖 0 · 글자 겹침 0 · padding 겹침 0(기준 1) · 제목 띠 0 · 높이 1156 = 41×26+90 · 박스 328/328 · 뱃지 없음 · 맨 위 10/5(월)` / 06 `y · 41/41 · 41/41 · 겹침 0 · 높이 972 = 41×22+70 · 맨 위 10/5(월)` / 문서 scrollWidth 390 · 섹션 높이 1 **1,746**·6 **1,567** · 문서 11,699(기준 901·866·10,153) ·
  1280 01 S `scrollLeft 2458 = 3280−822 · at-end · at-start 없음 · 첫 화면 10일 9/26(토)~10/5(월)` · 맨 왼쪽에서 = 기준(`chartArea [64.2, 24, 3206.7, 221.4] · 첫 화면 10일 8/26~9/4 · 라벨 82/82 · 뱃지 · 3280×280`) / 06 S `2843 = 3280−437 · 첫 화면 6일 9/30~10/5` · 맨 왼쪽 = 기준(`[42.7, 28.4, 3255.9, 211.6] · 5일 8/26~8/30 · 0/41 · 3280×240`) · 섹션 841/589 = 기준 ·
  회전 390→844 `01 x · 41 · 박스 762/3280 · scrollLeft 2518(끝) · 뱃지 · at-end` · 06 `x · 41 · 뱃지` → 390 복귀 = 로드와 같음(`y · 41 · 82/82 · 0 · 0 · 0 · 1156 · minWidth 0px · 10/5 · 328×1156`, 래퍼 at-end·at-start 둘 다, 뱃지 0) ·
  인쇄 390(A4 · 0.4in): beforeprint 01 높이 **1000**(비트맵 656×2000)·06 972 · 인쇄 중 mq change `(False, docW 720) → (True, 390)` 은 잠금으로 무시 · afterprint 1156/972 · **PDF 16쪽 — 01 벡터 행 41/41 이 2쪽 한 쪽에, 06 41/41 이 8쪽 한 쪽에, 둘 다 최신 위 순서** · 1280 PDF 13쪽 이미지 구성 = 기준(`[3280, 280]` 1 · `[3280, 240]` 6, 보이는 비율 0.1948) · 8 캔버스·pageerror 0 · **외부 요청 허용 2 · 차단 0**.
  캡처 `work/R3/shots/390_sec1.png`(dfa4ea69) · `390_sec6.png`(26677d7b) · `1280_sec1.png`(3fe596a5) · `1280_sec6.png`(e18f2b1a) · PDF `390.pdf`·`1280.pdf`·`base_1280.pdf`(md5 는 실행마다 다름 — PDF 생성 시각).
  전후 비교 `"$PY" work/P/mk_compare.py --old work/index.html --new work/R3/index.html --out work/R3/compare.html --sections 1,6 --online` → **`work/R3/compare.html`(d021661a)** · 390 01 901 → 1,746 · 06 866 → 1,567 · 문서 닫힘 10,153 → 11,699px(12.0 → 13.9장) · 1280 01·06 841/589 그대로.
- **R5** `mutation_test.py work/R3/index.html` + CSV 4 → exit 0 **"전부 살아 있음"** · 기준 24/24 · 커버리지 24/24 · **[OK] 52** · config 실험 4(ctr 4→5 · date_sections [1,6]→[1] · layout_id → FAIL 1 · **mobile.max_px 640→641 → FAIL 1**) · MISS/UNCOVERED/SKIP 0 · 원본 md5 동일(`work/R3/mutation.log`) / test_apply **Ran 19 OK**(ApplyRehearsal R3 포함, skip 0) · test_deploy `-k layout_gate` **Ran 4 OK** · test_compare_sections × R3 **5경우 전부 맞음** · test_narrative_check **Ran 7 OK** · test_validate_07 **Ran 6 OK**(`-W error::ResourceWarning`).
- **R6** 역검증(`work/R4/r6.py`) 14건 + 원본 md5 **전부 기대대로**: (1) 새 validate × 기준 사본(meta B) → "레이아웃 판" FAIL(meta ≠ config · 분기 0 · matchMedia 0 · M 줄 0) (2)(3) 분기 06·01 주석 제거 → `분기 표지 … 합 1 ≠ config 2` (4)(5) M 줄 maxPx 641 · printMaxH 999 → `M 줄 (…) ≠ config mobile (640, 1000, 26, 22, 90, 70)` (6) CSS 640 → 641 → `CSS @media … [641] ≠ config max_px [640]` (7) matchMedia 하드코딩 꼴 → FAIL (8) matchMedia 둘째 → FAIL (9) meta 만 C 로 바꾼 B 판 → 분기 0 FAIL (10) P_A 프로토타입 → FAIL (11) C 판 그대로 → PASS 24/24 (12) **묵은 M 줄(641/999) → `apply`(--layout 없이) → R3 와 바이트 같음**(M 줄은 compute 가 아니라 config 에서 온다) (13) 분기 하나 빠진 C 판 + `--layout` → `[FAIL] apply: ApplyError: 레이아웃 판 r2026-10-C 인데 분기 표지 1개(01 1 · 06 0) ≠ config 2 — 손으로 바꾼 판으로 보임` · 파일 그대로 (14) B 판 + `--layout` 없음 → `레이아웃 판 meta r2026-10-B ≠ config r2026-10-C — --layout 을 붙여 r2026-10-B → r2026-10-C` · 파일 그대로. 옛 판 fixture → B → C 사슬은 test_apply ApplyLayoutC.
- **R7** 다음 회차 재현: `cp R3/index.html → R4/{prev,index}.html` → 같은 compute 로 `apply --layout` → `레이아웃 판 r2026-10-C(변환 건너뜀) (변경 없음)` · R4/index = R3/index 바이트 같음(M 줄 그대로) → validate **24/24** · compare **OK 99/DIFF 0**(직접 — precheck.sh 는 md5 가드가 정상 FAIL 이라 쓰지 않음).
- **R8** 끝 상태: 아래 마무리 기록(커밋 뒤 `status --short` 0줄 · materials 19/19 OK + fixture 원본 f89b159d · 외부 요청 = CDN 2 · 스킬 저장소 fetch·push 1·재clone 1 · deploy.py 실행 0).

## 기준선 리허설과 다르게 한 곳
- 설계 A JSON rehearsal 의 R7 `deploy.py push --dry-run` → **실행하지 않고 test_deploy 게이트 4건(`-k layout_gate`)으로 대체**(지시 제약 — deploy 실행 0, dry-run 포함). 자기 검토(흐름 렌즈)가 실물 R3(판 C)·R3/prev(판 B)로 하네스 5 시나리오를 따로 재현: 첫 적용 전 데이터 회차 dry-run `[주의]`·PUT 0 → 실제 push `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함` 요청 0 · `--layout-change` PUT 1(본문 = 4492c1f4) · C↔C 문구 0·PUT 1 · PUT 결과 모름 재실행 안전 · 보류 중 배포본 바뀜 → base FAIL.
- 리허설 번호는 지시대로 R1~R8(기준선 4절·결정 블록의 "R1~R9" 는 초안 번호).
- R4 의 1280 "= base" 는 chart_check 가 `--base` 를 같은 도구로 잰 값과 대조(첫 화면 10일·5일 · 섹션 841/589 · 라벨 82/0 — 위 실행 출력). S 때문에 로드 상태 첫 화면은 최신 쪽(9/26~10/5)이라, PC 모양 대조는 박스를 맨 왼쪽으로 되돌려서 한다(임의 결정 10).
- 인쇄 판정: 탐색 F 실험은 PDF 를 pdf.js 로 PNG 렌더해 눈으로 봤다(CDN 한 곳 더). 구현 chart_check 는 CDN 2건 원칙 때문에 렌더 대신 pypdf 로 읽는다 — 판 C 의 390 PDF 는 01·06 이 이미지가 아니라 **벡터**로 실려(이미지 0) 텍스트 행 41개로 판정했다(임의 결정 10).
- 첫 실측(지시 값 그대로)의 390 01 글자 겹침 1·제목 띠 1, 06 제목 띠 1 → 라벨 자리(임의 결정 6·7) 뒤 0.

**자기 검토**(지시의 [검토 깊이 규칙] — 워크플로 에이전트 4: 코드·검사 / 화면·인쇄·런타임 / 배포 흐름 반박·문서 + 기계 확인(haiku)): **막음 0** — 셋 다 "다음 단계로 가도 된다", 기계 확인 사실 목록 일치. 근거 [실측]: 판 32경우(판 16 × `--layout` 유무) 문구·FAIL·파일 불변 · 기간 n=1·3·8·42·90·120 과 값 13배에서 apply·compare·validate 01/06 1벌 · 320·360·390·430·640·641·1280·회전 3회·1280↔600 축소 2회 누락 0 · A4 여백 0·0.4in·0.5in·1cm 인쇄 41/41 벡터 한 쪽 · 두 번 연속 인쇄·인쇄 뒤 회전 복원 · 템플릿 예외 주입 시 그 차트만 PC/빈 캔버스·나머지 7 정상 · 게이트 5 시나리오 · 할 일 6 목록 빠짐 0. **같이(이번에 쓴 줄 안 글자)**: css-and-layout "인쇄는 scrollLeft 와 무관하다" → PC 인쇄는 scrollLeft 를 따른다(실측 — 아래 이월 1) · report-structure 판 C 문단 "PC 는 지금 그대로(≈8.9일)" → 일수 그대로·구간은 S 를 따라 최신 쪽 · chart_check docstring 인쇄 판정에 벡터/비트맵 둘 다(코드와 같게) — 고친 뒤 리허설 R1~R7 재실행 같은 md5. 나머지는 아래 이월.

## 검증 회차가 볼 것(완료 기준 표 줄로 — 판정만, 쓰기 0)
준비: 새 clone(위 명령) + 작업 clone `D:\saero\feat-20261006-dailychart\work\` 에서 **읽기만으로 사본**: `index.html`(46e15c8a — 배포 014472d·meta B) · `compute.json`(2446b7c0) · `combined/` 4 · `materials.md5` · `P/mk_compare.py`(622cb68a) · `P/P_A.html`(76593db4) · 리허설 스크립트 `R3/rehearse.sh`(2383519c)·`R4/r6.py`(e035926e) · 비교용 산출 `R3/index.html`(4492c1f4)·`R3/compare.html`(d021661a)·`R3/shots/*.png`. 운영 폴더·작업 clone 은 읽기만.
1. **HTML 숫자·배열 = compute(1벌)·apply 멱등·서술 표지 36 불변** — R2(4492c1f4 · 두 번째·`--layout` 없음 바이트 같음 · 표지 36) · compare 99/0 · validate 날짜축 2×41·min-width 2곳 · `labels: [` 날짜형 2개.
2. **모바일 390 누락 0** — chart_check 390(01 41·82/82·밖 0·글자 0·padding ≤ 기준 1·제목 띠 0 / 06 41·41/41).
3. **PC 1280 = 직전 배포본 측정값 + S 끝 시작** — chart_check 1280 두 줄씩(S · 맨 왼쪽 = 기준) · 섹션 841/589.
4. **회전 390→844→390 복원** — chart_check 회전 두 줄.
5. **인쇄 page.pdf 실물** — 390 01·06 벡터 41/41 한 쪽·최신 위 · beforeprint ≤ 1000 · afterprint 복구 · 1280 이미지 구성 = 기준(일수 그대로 — 구간은 이월 1).
6. **8 캔버스·pageerror 0** · 템플릿 try/catch + 큐(도우미 정의 순서) · 외부 요청 허용 2·차단 0.
7. **meta C·분기 주석 2·M 줄·CSS 경계 = config** — validate "레이아웃 판" · R6 14건 · mutation 변조·가드·config 실험(`[OK] 52`·실험 4) · apply 판 사슬·손 수정 FAIL(test_apply ApplyLayoutC).
8. **첫 적용 게이트(M4)** — deploy.py 변경 0 · test_deploy `-k layout_gate` 4 · code-tab 4절 판 C 첫 적용 문단 · 아래 첫 적용 본보기.
9. **원칙** — 새 색 0(hex 18 → 18, rgba 는 기존 ::after 와 같은 값) · `<script src` 2 · 단일 파일 · 범례 bottom · 01 박스·섹션 HTML·서술 표지 바이트 불변 · overflow 3폭 넘침 0 · 컨테이너 HTML 에 `data-*`·여분 min-width 0.
10. **문서 = 코드** — 개수(24·99·[OK] 52·config 실험 4)·출력 문구(apply 3꼴·B 판 FAIL·분기 FAIL·validate PASS)가 글자 그대로 · 할 일 6 목록.
11. **리허설** — `rehearse.sh` 다시 돌려 같은 md5(R3 index 4492c1f4 · compute 2446b7c0 · R4 index 4492c1f4) + chart_check 18/18 + R6 전부 기대대로.
12. **검증 폴더** `D:\saero-verify\<clone>` · 쓰기는 사본에서만.

## 이월(한 줄씩 — 막음 아님, 첫 적용 보류 회차·첫 실사용 뒤 또는 점검 회차)
1. **PC 인쇄 구간이 S(최신 쪽 시작)를 따른다** — 1280 창·A4 0.4in 에서 01 은 9/26 무렵~10/3·10/4(최신 10/5 는 종이 폭 밖), 06 은 9/28~10/5(판 B 는 둘 다 8/26 부터). 일수는 같아 손실 아님. chart_check 의 "PC PDF = 기준" 은 구간(첫/끝 날짜)을 대조하지 않는다(문서는 이번에 정정).
2. **모바일 인쇄가 Chart.js 애니메이션 중(로드·회전·탭 뒤 약 1초 안)이면** beforeprint 의 resize 가 다음 그리기로 미뤄져 01 이 1,156px 비트맵 그대로 1,000px 에서 잘린다 — 약 37/41일(기준 ≈8.9일보다 많음 — 손실 아님). F 규약 "41일 한 쪽" 이 이 길에서는 안 지켜짐 · chart_check 는 1.8초 뒤만 본다.
3. **쪽 높이가 ≈1,010px 보다 작은 인쇄 설정**(Letter, A4 여백 0.6in 이상)에서 모바일 01(설정에 따라 06 도)이 PDF 에서 통째로 빠진다 — 같은 설정의 기준은 ≈7~8일. A4 기본 여백(0·0.4in·0.5in·1cm)은 41/41 [실측 자기 검토]. 한국 A4·기본 여백이 정상 흐름이라 막음은 아니나 여유가 ≈36px — 첫 적용 보류 회차의 실기기 "인쇄 미리보기" 확인 항목 · `print_max_height_px` 를 낮출지(예: 900)는 사용자 결정 몫.
4. chart_check: "캔버스 밖" 이 padding 상자 기준이라 값이 지금의 ≈13배(하루 비용 ≈29만 원)인 날 0.2px 거짓 FAIL(요란 — 글자 잘림 0) · `--base` 없이 돌리면 기준 대조 생략으로 PASS(문서 명령은 전부 `--base` 를 붙임).
5. 문서: code-tab 3절 5단계 행·checklist [되돌리면 안 되는 것] "레이아웃 판" 행 문구가 옛 판 변환만 적음(B → C 빠짐 — 게이트가 PUT 0 으로 멈춰 틀린 쓰기 없음) · code-tab ⓑ "레이아웃 판이 바뀜" 행·SKILL 7단계 게이트 문단에 chart_check 를 같이 보이라는 말 없음(4절에만).
6. config `mobile.row_px`·`pad_px`·`print_max_height_px` 를 바꾸면 판 id 는 그대로 M 줄만 바뀌어 게이트 없이 자동 배포된다(`max_px` 만 CSS 대조로 FAIL) — 설계 회차가 바꿀 때 판 id 도 올릴지.
7. 이 절 아래 탐색 기준선 "사용자 결정" 블록의 지시문 검토자 대조 줄(887b43c)에서 `\n});\n</script>\n` 리터럴이 실제 줄바꿈으로 풀려 4줄로 쪼개져 있다(기준선 절은 그대로 둠 — 문구만의 문제, 이 PC Bash heredoc 역슬래시 함정).
8. 탐색 기준선 6절 이월(A: 높이가 n 에 비례 · 인쇄 F 의 n 상한 · 첫 화면 순서 등)·10/06 회차 1·2 이월·검증 이월(mk_compare 저장소화 — 이번에 네 번째 사본 사용)은 그대로.

## 마무리 기록(이번 회차)
- 커밋(경로 지정 add, `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`, 전역 설정 변경 0): `9bbfd2c` apply·config·test_apply·fixture · `48fc991` validate·mutation · `57cf58b` chart_check · `073647c` 문서 · 그리고 이 절(기록 커밋 — 해시는 자기 참조라 적지 않는다).
- 끝 확인(커밋 뒤): `git fetch` → origin/main 확인 · 브랜치 push 1회(`git -c credential.interactive=false push origin feat-20261006-dailychart`, main 아님) · 스크래치 `git clone -c core.autocrlf=false -b feat-20261006-dailychart --single-branch` 로 HEAD·md5 대조 — 결과는 채팅 보고(자기 참조).
- work/ 재료 md5 19개 시작과 같음(`work/materials.md5`) + fixture 원본 f89b159d(`work/materials_fixture_orig.md5`, 887b43c) · 배포 PUT 0 · 네이버 0 · 키 파일 0 · deploy.py 실행 0 · 운영 작업 폴더 열기 0 · 10/06 회차 2 clone 열기 0.
- 다음 단계([넘길 때]): ④ 첫 검증 `D:\saero-verify` 새 세션 **Fable 5.1 · ultracode**(위 검증용 clone, 운영 폴더·작업 clone 읽기만, 판정만·쓰기 0 — 지시문은 이 세션이 `D:\saero\saero-ad-report_01차트_검증지시_회차1_2026-10-06.md` 로 씀) / ⑤ 수정(막음이 있을 때만) 새 세션 **Opus 5.5 · xhigh · ultracode 끔**(③ 세션을 이어 쓰지 않음, 같은 결함으로 2번을 넘으면 Fable 로 올릴지는 사용자) / 재검증 새 세션 · 바뀐 것만 · **Fable 5.1 · xhigh** / ⑥ 병합은 ④ 검증 세션에 이어서(갱신 회차가 돌지 않을 때 — last-audit 맨 위 충돌은 main 회차 절을 위에, **그날 아침 데이터 회차 뒤에 병합하고 첫 적용을 바로 붙임**) / 첫 실사용 운영 세션 `/saero-run` **Opus 5.5 · high · ultracode 끔** — 아래 본보기.

## 첫 적용 본보기(운영 세션이 그대로 쓴다)
- **경로 C**(사용자 결정 5 — 모양만 바꾸는 별도 배포 회차): 그날 평일 아침 데이터 회차가 끝난 뒤, 같은 합본으로 2-1 같음 → "다시 계산". 운영 세션 `/saero-run`(**Opus 5.5 · high · ultracode 끔**), 첫 말 **"01 차트 판 C 첫 적용 — 경로 C — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함"**.
- 흐름: S0 → (수집·ingest 생략 — 아침 회차 합본 그대로) → 4 `deploy.py fetch --out work/prev.html && cp work/prev.html work/index.html`(직전 배포본 = 판 B, meta r2026-10-B) → 5a compute → 2-1 같음 → 사용자 "다시 계산" → 3 → 5-0a(pull · propose `--since` 그대로) → ⓐ 해당만 → **5 = `"$PY" scripts/apply.py --layout --html work/index.html --compute work/compute.json`**(출력 `레이아웃 판 변환(r2026-10-B → r2026-10-C, 분기 2)` — B → C 변환 + 값, 글은 같은 기간이라 그대로·서술 스크립트 없음) → 6 `scripts/precheck.sh work/index.html work/combined work/prev.html`(기대: validate 24/24 · "레이아웃 판 … r2026-10-C · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · CSS 640" · compare OK 99/DIFF 0 · 3폭 · narrative `[주의] 같은 기간` · 도장) → **보류 멈춤**: 운영 세션이 `"$PY" tests/chart_check.py work/index.html work/compute.json --base work/prev.html --out work/chart_<날짜>`(기대 PASS 18/FAIL 0 · 외부 요청 허용 2·차단 0) + 전후 비교 `"$PY" /d/saero/feat-20261006-dailychart/work/P/mk_compare.py --old work/prev.html --new work/index.html --out work/compare_<날짜>.html --sections 1,6 --online`(저장소 밖 작업 clone 의 사본 — md5 **622cb68a**, 그 clone 을 지우지 말 것; 같은 생성기가 `D:\saero\feat-20261006-layout\work\R1\` 에도 있다)을 만들어 보이고, 사용자는 `work/index.html` 을 폰(390 세로 · 844 회전 · 접기 펼침 03·07·08 · 인쇄 미리보기 — 이월 3 의 용지·여백 포함)과 PC 로 본다 — **이때 결정 11 ①~④ 를 한 번에 묻는다**(① 사장님 주 화면이 모바일인지 ② 인쇄·PDF 를 쓰는지 ③ 10/06 회차 2 시크릿 창 확인(03·07·08 접기) 결과 ④ 01 의 "선이 세로로 흐르는" 모양이 괜찮은지) · 답은 기록 "사용자 결정" 아래 한 줄 → 사용자 **"배포"** → 7 `deploy.py push --file work/index.html --base work/prev.html --message "레이아웃 판 r2026-10-C 첫 적용" --dry-run`(`[주의] 레이아웃 판이 바뀜`) → **`push … --layout-change`** → `verify --ref <커밋>` → 8 기록.
- 미리보기 재료(보류 회차 전에 사용자가 미리 볼 수 있음): `D:\saero\feat-20261006-dailychart\work\R3\compare.html`(d021661a — 기준 ↔ 판 C, 01·06 × 1280·390) · `work\R3\shots\390_sec1.png`·`390_sec6.png`·`1280_sec1.png`·`1280_sec6.png` — 위 R4 명령으로 만듦.
- **병합은 그날 아침 데이터 회차 뒤에 하고 첫 적용을 바로 붙인다** — 병합 뒤 첫 적용 전에 데이터 회차가 먼저 돌면 5단계 `apply --layout` 이 모양을 바꾸고(B → C) 게이트가 PUT 을 막는다: 그때는 PUT 0 으로 멈추고 사용자에게 묻는다(chart_check·전후 비교를 보인 뒤 "배포" 답이 있을 때만 `--layout-change`).
- 그 다음 회차부터: 직전 배포본이 판 C — `apply --layout` 은 변환을 건너뛰고 값·M 줄만, 게이트는 조용히 통과(자동 배포 그대로), 서술은 표지 기반(ⓑ). chart_check 는 데이터 회차 6단계에 없다(precheck 밖 — 검증·정기점검·다음 모양 회차 몫).

---

# 기능 추가 탐색 기준선(01 일별 추이 모바일 차트, 2026-10-06)

점검일: 2026-10-06 (기능 추가 회차 — **탐색·설계만**. 데스크톱 앱 Code 탭, 이 PC, 작업 폴더 `D:\saero`로 연 세션, 모델 Fable 5.1 · ultracode — 워크플로 에이전트 37: 설계 3 + 검토자 6 + 막음 검증 27 + 완결성 비평 1). 사실 기준 10/06 18:59 KST · 운영 main 작업 폴더 HEAD **`f799bb6`** = origin/main(시작 때 새 clone 으로 대조 — 달라진 것 0) · 작업 트리 깨끗. 작업 clone `D:\saero\feat-20261006-dailychart`(브랜치 같은 이름, push 0). 기준 사본: main `work/index.html`(md5 **46e15c8a** = 배포 014472d · meta r2026-10-B)·`work/compute.json`(2446b7c0)·`work/combined/*.csv`(검색어 e3a352a2 · 상세지역 e70e5023 · 시간대별 faac5a0a · 키워드 b7d91858, 41일 8/26~10/5)을 clone `work/` 로 복사. `work/prev.html`(002233ee, meta 없는 옛 판)은 복사하지 않았다(리허설의 "직전 배포본" 역할은 기준 사본 자신). 운영 작업 폴더 쓰기 0(`git --no-optional-locks` 읽기만) · 기존 코드·문서·config·data/·registry 변경 0 · 외부 쓰기 0(push·네이버 POST·배포 PUT 0 — deploy.py(fetch 포함)·exclusions·fetch_reports·ingest·archive·precheck 실행 0, 키 파일·자격 증명 열지 않음). 10/06 회차 2 시크릿 창 확인(03·07·08 접기) 답: **아직(미확인)**. 구현은 사용자가 아래 "내가 고를 항목"을 고른 뒤 별도 회차.
추가할 기능: 리포트 01 "일별 추이" 차트(dailyChart — 노출 막대 + 총비용 선)가 모바일에서 한 화면에 3~4일만 보여 추세를 못 읽는다 → PC(한 화면 약 10일)는 그대로 두고 모바일만 추세를 한눈에 읽는 시각화로. 숫자는 빠뜨리지 않는다(접힌 안·누르면 보이는 자리라도 전부 남아야 함 — 툴팁은 인쇄가 안 되므로 "남아 있음" 으로 안 친다). **사용자 원문(2026-10-06)**: "피씨에서는 가로로 10개 정도 보이고 있는데 모바일에서는 3~4개만 보이고 있어서 상당히 가독성이 떨어지고 있어 … 가독성 좋게 다른 방법으로 시각화하고 싶어" — 10/06 "리포트 읽기 쉽게" 고를 항목 6(차트 폭 per_day_px 80 그대로 — 첫 실사용 뒤 판단, 이월)·16-④(3,280px 가로 스크롤이 불편했는지)의 첫 실사용 답.

## 0. 시작 확인과 환경 실측 [실측]
- 실측·프로토타입·비교 페이지는 전부 clone `work/`(gitignore)에: `work/M0/`(기준 실측 `measure.py`·`base_measure.json`·캡처 `base_390_sec1_start.png`/`_end.png`/`_full.png`·`base_1280_*`·PDF `base_390.pdf`/`base_1280.pdf` · Chart.js 프로브 `probe.html`/`probe.py`/`probe.json`/`probe_390.png` · 06 캡처 `sec6.py`) · `work/P/`(프로토타입 생성기 `make_protos.py` → `P_S.html`/`P_A.html`/`P_B.html`/`P_C.html`, 설계 에이전트 보정판 `P_B2.html`(= work/W/B/B2.html)·`P_C2.html`(= work/W/C/P_C2.html) · 실측 `<X>_measure.json`·캡처 `<X>_390_sec1_start.png`·`A_390_sec6.png`·`B_390_sec6.png` · **전후 비교 `compare_S/A/B/B2/C/C2.html`**(기준 ↔ 프로토타입, 01·06 × 1280·390, mk_compare.py 사본 622cb68a `--sections 1,6 --online`) · 사실 묶음 `FACTS.md`(하위 에이전트 공용 — 1-3 인쇄 행은 아래 1-3 으로 정정됨) · 주별 값 `weekly.json` · 워크플로 결과 `workflow_result.json`/`workflow_result_inner.json`(설계 A·B·C JSON 전문 · 검토자 6 발견 전문 · 막음 검증 27표 · 비평) · 초안 `baseline_draft_*.md`) · `work/W/<에이전트 라벨>/`(검토자·검증자 실험 사본·스크립트·PDF·PNG — 이 절이 인용하는 실측의 원본).
- 실측 방식: venv 파이썬 + playwright chromium(새 임시 프로필 — 수집 프로필 아님) · CDN 허용(외부 요청 = cdnjs 둘뿐) · `networkidle` + 1.8초(Chart.js 애니메이션 1초) 대기 · 390×844(dpr 2·모바일 UA)·1280×900 · `Chart.getChart` 로 tick·datalabel(플러그인 `$datalabels._labels[].$layout._visible`·`._box._rect` — 보이는 라벨 수·상자 겹침·캔버스 밖)·스크롤 박스 clientWidth/scrollWidth/scrollLeft · 인쇄는 `page.pdf()`(A4) 실물을 pypdf 로 읽음(검토자·검증자) — `emulate_media('print')` 값은 레이아웃 폭이 안 바뀌어 인쇄 실물과 다르다(아래 1-3).
- 기준 사본에 대한 현행 검사: validate **24/24 PASS** · compute(경쟁사표 = 기준 사본 자신) → compare **OK 99 / DIFF 0**(compute.json 2446b7c0 = 운영 것과 같음) · overflow 360/390/430 넘침 0.

## 1. 지금 상태 [실측 — 원문 확인, 지시의 사실과 다른 곳은 굵게]
### 1-1 차트 자리(배포본 = `work/index.html` 2,371행)
- L5 `<meta name="report-layout" content="r2026-10-B">` · L23~24 외부 스크립트 둘(Chart.js 4.4.1 · datalabels 2.2.0, cdnjs) · L109 `canvas{max-width:100%}` · L137 `.scroll-x{overflow-x:auto;}` · L139~152 뱃지 `.scroll-hint` · 페이드 `.scroll-fade::after`(**오른쪽만**, `.at-end` 로 숨김) · L175 태블릿 `@media (max-width:900px) and (min-width:641px)` · L182 모바일 `@media (max-width:640px)`. css-and-layout.md "반응형" 의 `@media (max-width:420px)` 는 **배포본에 없다**(grep 0 — 문서가 코드보다 많음).
- L263 `<!-- Section 1: Daily trend -->` · L271~275 `<div class="scroll-x" style="overflow-x:auto;"><div style="height:280px; min-width:3280px;"><canvas id="dailyChart"></canvas></div></div>` · L277~ 인사이트 박스(① 표 5행 10/1~10/5 · ② 순위 5칸 · ③ note-mint, 서술 표지 01-rank·01-mint) — 범위 밖.
- L985 `<!-- Section 6: -->` · L990 section-desc `노원역필라테스 평균 2.47위 · 낮을수록 상단 노출`(표지 06-desc 고정 — "상단" 은 광고 노출 위치) · L994~996 `<div style="height:240px; min-width:3280px;"><canvas id="rankChart">`(grid-2 왼쪽 카드 — 1280 에서 카드 폭 437px).
- L1797~1798 09 hourlyChart 컨테이너 `height:280px; min-width:650px;`(고정, config 대상 아님 — [의도된 동작] 12).
- L1954~2294 **한 `<script>` 안에 `new Chart` 8개(01·02 둘·05 둘·06·09·10)가 직렬** — 앞 블록의 런타임 예외 하나가 뒤 차트 생성을 전부 막는 구조는 지금도 같다(검토자 [실측] rankChart 앞에 예외 한 줄 → 06·09·10 None). L1963 `Chart.defaults.set('plugins.datalabels', { display: false });` · L1965 `// 1. Daily trend - combo` · L1966~2031 `new Chart(document.getElementById('dailyChart'), {type:'bar', data:{labels:[41 × 'M/D(요일)' 오름차순], datasets:[bar '노출수'(datalabels anchor start·align top = 막대 하단) · line '총비용(원)'(yAxisID y1 · datalabels align top·anchor end·clip:false)]}, options:{responsive, maintainAspectRatio:false, layout.padding.top 24, legend bottom, x ticks maxRotation 0·autoSkip false, y 왼쪽·y1 오른쪽}})` · L2033 `// 2. Campaign-type`. L2164~2199 rankChart(type line · 같은 labels · y reverse·min 1 · x grid off — **autoSkip:false 없음**(3,280 폭에선 41 tick 전부 나옴) · datalabels 없음 · 제목 `… 일별 평균순위 · 낮을수록 상단`) · L2242 `// 7b. Hourly`.
- L2302~2369 안내 스크립트(별도 `<script>`): `sync()` 가 `.wide-table, .scroll-x` 마다 `scrollWidth > clientWidth + 4` 면 뱃지 삽입 + **`.scroll-fade` 래퍼로 감싼다(insertBefore/appendChild — DOM 이동으로 그 박스의 scrollLeft 가 0 으로 돌아간다 [실측 S 프로토타입: load 리스너로 scrollLeft 를 끝으로 보내면 sync 가 뒤에 돌며 0 — setTimeout 0 로 sync 뒤에 옮기면 10/3~10/5 가 보임])** · scroll 때 `.at-end`. `load`·`resize`(200ms)·details `toggle` 에 sync. L2363~2367 `beforeprint` 에 닫힌 details 전부 열고 `afterprint` 되돌림. **scrollLeft 를 정하는 코드는 없다** — 모바일·PC 모두 첫 화면은 8/26부터.
### 1-2 값을 쓰는 코드·검사(지시의 사실은 원문 일치, 보탠 것만)
- compute.py L88 `minwidth = max(nd×per_day_px, floor_px)` · L89 `nlabels` · L102~109 `01{labels, 노출, 총비용, …}` · L156 `06.rankChart`. config `chart_min_width{80, 650, [1,6]}` · `report_layout{r2026-10-B, recent_days 7, markers.details 5}`.
- apply.py L189~194 min-width 2곳(치환 2 regex + 개수 ≠ 2 면 ApplyError — 컨테이너에 다른 속성(`data-*`)을 덧붙이면 앵커 0곳 FAIL [실측 P_B·P_C 의 data-minwidth]) · L197~214 `chart()`/`labels()`: `getElementById('<id>')` 부터 **다음 `new Chart` 전까지**에서 `label: '<라벨>', data: [`/`labels: [` **첫 하나만** 치환(`re.subn(count=1)` — 없으면 FAIL, 둘이어도 FAIL 하지 않고 첫 것만 바꾼다; "정확히 하나" 요구는 `once()` 뿐 — docstring L17 과 다름) · L163~179 판 고르기(meta ≠ config → `ApplyError 이 판에서 바꾸는 변환은 없음`, meta = config 인데 details 수 ≠ markers → `접기를 손으로 바꾼 판으로 보임` [실측 P_B 7개·P_C 6개 FAIL, 작업본 불변]) · L101~148 `convert_layout`(meta 없음 → B 만; **L106~107 이 config `layout_id` 를 meta 에 쓰고 L145~147 이 config `markers.details` 와 대조하므로 config 를 C 로 올린 채 그대로 부르면 옛 판 → B 단계가 FAIL** — 옛 → B → C 사슬은 B 단계 값을 명시해야 한다, 세 설계 공통). **B → C 변환 경로는 없다 — 새로 만들어야 한다.**
- validate L214~224 `check_chart_width`: 섹션의 min-width 를 **전부** 모아 기대값이 그 안에 있으면 PASS(여분 min-width 허용 — 접기 안 컨테이너의 min-width 3000 도 통과 [실측 검토자 e1]) · L227~238 `check_date_labels`: **HTML 전체**(섹션 무관)에서 항목이 모두 `'\d+/\d+\(.\)'` 인 `labels:[…]` 배열마다 길이 = 일수(짧은 날짜 배열 추가 = FAIL · 두 줄 배열·`'9/29~10/5'` 같은 다른 꼴은 검사 밖 · 0건 FAIL). checklist 회귀 표의 "날짜축 라벨 검사가 date_based_sections 순회" 문구는 **check_date_labels 코드와 다르다**(check_chart_width 만 순회). L373~388 `check_layout`(meta = config · `<details` 수 = markers.details · 짝).
- compare L65~70 `_s01`: "01 dailyChart 노출·총비용"(`getElementById('dailyChart')` 뒤 첫 `label:'노출수', data:[`) · "01/06 labels"(문서 전체 `labels:['M/D(요일)',…]` 배열 **정확히 2개** + 첫 라벨·길이 — 셋이면 DIFF [실측 검토자 e8]) · "01 min-width"(섹션 1 **첫** min-width) · L116 06 둘. 항목 99.
- deploy.py L178~185 `layout_of` · L262~273 게이트(--file·--base meta 다르면 실제 push `[FAIL] … PUT 안 함`, `--layout-change` 만 통과, dry-run `[주의]` — meta 값이 무엇이든 "다름" 만 본다 [실측 test_deploy 21 OK]) · tests/test_deploy.py 게이트 4건. tests/test_apply.py L140~141(min-width 2곳 · 01 labels 문자열) · **L338 `content="r2026-10-B"` assert**(판을 올리면 리허설 R1 산출로 돌리는 ApplyRehearsal 이 FAIL — 갱신 대상) · mutation_test.py L259~267(min-width −60 · 라벨 첫 항목 제거) · L322(라벨 형식 변조 가드) · L331~333(min-width 제거 가드) · L345(config date_based_sections 실험) · overflow_check.py(Chart.js 미로드 · details 열고 3폭).
- 문서: report-structure.md "레이아웃 판 r2026-10-B" 절("이 판도 설계 회차·사용자 결정 없이 바꾸지 않는다" · "01 표 5행·순위 5칸·차트 labels 는 시간 오름차순 그대로") · "01. 일별 추이"(막대 라벨 하단·선 라벨 위·범례 bottom·컨테이너 규칙·x ticks — 값축 눈금 규칙은 없음) · "06"(정의: 노원역필라테스 그룹 전체 가중순위 **전 기간**) / css-and-layout.md 버그 4(고정 높이, "8개 차트 전부 이 패턴")·5("라벨을 줄이거나 숨기는 것보다 … 스크롤 … 정보 손실이 없어 우선")·6·8("매주 늘어나는 폭 = config")·11 · "가로 스크롤 안내 자동화"·"접기 안내"(details 5)·"반응형"(420px — 코드에 없음)·"PWA"(service-worker network-first) / SKILL.md 원칙·체크 3·4·검산 24·compare 99 / checklist [의도된 동작] 2·12·17·27 · 16(24개·99항목·mutation [OK] 50) · 회귀 표 / apply.py FOLD_CSS 주석 L82~83("03 … 08 TOP 10 밖" 5곳 — 배포본 `<style>` 에 그대로 실림)·docstring L8.
### 1-3 화면·인쇄 실측(`work/M0/base_measure.json` · 검토자 pypdf)
| 폭 | 01 dailyChart | 06 rankChart |
|---|---|---|
| **390×844** | canvas 3,280×280 · 스크롤 박스 clientWidth **328** · 76.6px/일(80 − 축 여백) · **첫 화면 3일 8/26(수)~8/28(금)**(8/29 일부) · 끝 화면 10/3~10/5 · ticks 41 · datalabels 82 전부 그려짐(겹침 1 = 8/26 `497원`/`150`) · 뱃지·오른쪽 페이드 있음 · 섹션 높이 901px | 3,280×240 · 첫 화면 **4일 8/26~8/29** · 866px |
| **1280×900** | clientWidth 822 · **첫 화면 10일 8/26~9/4** · 끝 9/26~10/5 · 섹션 841px | clientWidth 437 · 첫 화면 **5일** · 589px |
- 라벨 폭(렌더 폰트): tick `M/D(요일)` 최대 39px(10.5px) · 비용 라벨 최대 `22,597원` 44px(11px) · 노출 라벨 최대 `957` 19px → 80px/일은 한 줄 라벨에 여유 · **7일을 328px 에 넣으면 ~28~33px/일(두 줄 라벨 ~25px 필요)** · 10일이면 01 겹침 13·06 tick 건너뜀, 14일이면 겹침 19 [실측 B10·B14].
- **인쇄(page.pdf A4 실물, pypdf 로 이미지·클립 읽음 — 검토자 4명 독립 재현)**: Chromium 은 page.pdf 때 **레이아웃을 종이 폭 794px 로 다시 짜고** `matchMedia('(max-width:640px)')` 가 false 로 바뀌는 change 가 beforeprint 직후에 온다(docW 794 · 인쇄 뒤 true 로 복귀, window `resize` 는 안 옴) [실측 work/W/revA/print_events.json]. Chart.js 4.4.1 은 window 에 `resize` 만 걸고 beforeprint 를 안 듣는다 [실측 probe listened]. 기준 배포본 PDF 는 **390·1280 모두 01 캔버스(3,280 폭)가 종이 폭 박스에 잘려 가장 오래된 ≈8.9일(8/26~9/3 일부, 클립 비율 0.2174)만 찍히고 32일은 표시 없이 빠진다**(03 표에는 총비용 41일이 전부 찍힘) [실측 base_390.pdf·base_1280.pdf]. `emulate_media('print')` 로 재면 박스 폭 328/822 그대로라 "첫 3일/10일" 로 나오는데 그 값은 실물과 다르다 — 이 절 아래의 인쇄 수치는 전부 page.pdf 실물 기준. 문서 details 는 beforeprint 에 열리고 afterprint 에 닫힘(10/06 실측 그대로). iOS 공유→PDF·실기기 인쇄 대화상자는 [추론](10/06 과 같음). 사장님이 인쇄·PDF 를 쓰는지는 **미확인**(고를 항목 11).

## 2. 대상 조사 — Chart.js 4.4.1 에서 가능한 것(`work/M0/probe.html`·`probe.json` 390·1280 + 프로토타입·검토자 실험 [실측])
| 할 일 | 가능 여부 | 근거 |
|---|---|---|
| 폭에 따른 분기(차트·축 방향) | **가능** — `matchMedia('(max-width:640px)')` 로 판정해 `indexAxis:'y'`(가로 콤보 — 막대 + 선, 값축 x/x1) 또는 다른 options 로 생성. 생성 뒤 `options.indexAxis` 를 바꾸고 `update()` 해도 됨(scales 세트·axisID·datalabels anchor/align·컨테이너 높이·min-width 를 같이 바꿔야 로드와 같은 모양 [실측 revA flip.json 390_same_as_load true]). `onResize` 는 뷰포트 변경·print 미디어 전환 때 옴 | probe c2(41행·높이 1,100 → 24.7px/행 · 라벨 82 전부 캔버스 안) · flipAxis ok |
| 분기 재판정 | load 1회 판정은 회전(390→844 가로 막대 유지)·창 축소(1280→600 세로 유지)에서 어긋난다 [실측 A rotate.json] → `mq.addEventListener('change', …)`(구형 iOS `addListener` 폴백)로 재판정. **인쇄 중에도 change 가 오므로**(위 1-3) 재판정 핸들러는 인쇄 분기(`printing` 잠금 또는 인쇄 전용 모양)를 명시해야 한다 — C 설계안 그대로(잠금 없음)는 모바일 PDF 01 이 빈 캔버스 [실측 RC-1] | revA·RC·SK 실험 |
| 기간 접기(보이는 창) | **가능** — 카테고리 축 `scales.x.min`/`max` 에 **숫자 인덱스 또는 라벨 문자열**(`min: n−7` → ticks 7, 막대 41 중 영역 안 7). 주의: datalabels 는 창 밖 점에도 만들어지고 `clip:false` 면 **차트 영역 왼쪽에 샌다** → `display:(ctx)=>ctx.dataIndex>=min` 으로 끈다 | probe c1 · switchWin7 · B 프로토타입 |
| 주 단위 묶음 | Chart.js 에 집계 기능 없음 — 값은 **밖에서**(compute 키) 만들어 별도 배열로 | C 프로토타입(생성기 합산, 합 = 일별 합) |
| 라벨 표시 조건 | **가능** — `ticks.callback` 이 배열을 돌려주면 두 줄 라벨(`'9/29'`/`'(화)'` — 배열은 그대로, 브라우저가 나눔) · `autoSkip:true + maxTicksLimit` 는 라벨을 건너뜀(41 → 6~7, 버그 5 와 충돌) · datalabels `display`·`offset`·`align` 은 스크립터블(index·폭 조건·이웃 라벨 자리 계획) | probe c3 · B2·C2 |
| 스크롤 시작 위치 | Chart.js 기능 아님 — DOM `box.scrollLeft = box.scrollWidth`. 안내 스크립트 sync 의 래퍼 감싸기 **뒤**(setTimeout 0 또는 sync 안)여야 한다 · 인쇄는 scrollLeft 와 무관하게 왼쪽부터 찍힌다 | S 프로토타입 [실측] |
| 인쇄(beforeprint 때 어느 분기·숫자) | Chart.js 는 beforeprint 를 안 듣는다 · page.pdf 는 794px 재배치 + mq change → **분기 코드가 정한 대로** 찍힌다: 세로 콤보 3,280px 는 종이 폭에 잘려 ≈8.9일(지금) · 가로 막대 1,156px 는 한 쪽(≈1,050px)을 넘어 **쪽 나눔에서 통째로 빠진다**(2쪽 빈 카드 + 3쪽 눈금 한 줄 — load 1회 판정 A 프로토타입 [실측 revA A390_p2/p3.png]) → mq change 때 PC 모양으로 돌리고 **동기 `chart.resize()`** 하면 기준과 같은 ≈8.9일, beforeprint 에서 높이를 한 쪽 안(≈1,000px)으로 캡하면 **41일 전부 한 쪽** [실측 skep3r R·F 변형] · 창(x.min)은 창 7일만 · `.m-only{display:none}` + `@media (max-width:640px)` 로 보이는 접기는 **인쇄 레이아웃(794px)에서 숨어 PDF 에 없다**, `html.mob` 클래스로 바꿔도 beforeprint 안에서 만든 캔버스는 Chromium 이 래스터화하지 않아 PDF 에 0개(사용자가 미리 펼쳐 둔 경우에만 ≈8.9일) [실측 B-R1·SK2R1·skep3_BR1] | 검토자 실험 |
| 겹침·누락 자동 검사 | **가능** — `chart.$datalabels._labels[].$layout._visible`/`._box._rect` 로 그려진 라벨 수·상자 좌표 → 겹침·캔버스 밖·창 밖 수(상자는 padding 4px 포함 — 글자 겹침은 padding 을 뺀 상자로 따로 센다 [실측 SK1 glyph_overlap]) · 인쇄는 page.pdf → pypdf 이미지 크기·클립·그려진 픽셀(venv 에 pypdf 6.18·pillow 12.3 있음) | measure.py · 검토자 스크립트 |
| 못 하는 것·[추론] | 외부 플러그인(zoom 등) 0 — 새 CDN 금지 · iOS Safari 의 `beforeprint`(공유 → PDF)·실기기 폰트 폭·터치 스크롤·회전 타이밍·PWA standalone 은 headless 에서 못 봄 [추론] | — |

## 3. 설계안(≤3, 반박 반영판 — 채택은 사용자)
### 3.0 공통 뼈대(세 안 모두)
- **판 올리기 r2026-10-B → r2026-10-C**(막음 M4): config `report_layout.layout_id` C · apply `convert_b_to_c(h, lay)` 신설 + 판 고르기를 사슬로(옛 판(meta 없음) + `--layout` → `convert_layout(h, LAYOUT_B)`(**B 단계 값 상수 `{layout_id:"r2026-10-B", markers:{details:5}}` 를 넘긴다** — 지금 L106~107·L145~147 이 config 값을 그대로 쓰므로 안 넘기면 B 단계에서 FAIL [실측 F5·A-4·C-R2·RC-4]) → `convert_b_to_c` · meta B + `--layout` → B→C 만 · meta = C → 값만(멱등) · 그 밖 FAIL 그대로) · details 수 검사는 사슬 끝 한 번 · main 출력 "레이아웃 판 변환(r2026-10-B → r2026-10-C, …)" · FOLD_CSS/FOLD_JS 주석의 "r2026-10-B" 리터럴은 "r2026-10-B 이후" 로. 첫 적용 = 다음 `/saero-run` 을 **"보류" 로 시작**(4 fetch 배포본 B → 5 `apply.py --layout` B→C + 값 → 6 precheck 도장 → 작업본 390·1280 캡처 + 전후 비교 HTML(mk_compare.py 류, 01·06) + 시크릿 창 → 사용자 "배포" → 7 `push --layout-change` PUT 1회 → 그 뒤 데이터 회차는 base·file 둘 다 C 라 게이트 문구 0, 자동 배포 그대로). 판을 안 올리는 길은 세 안 모두 **권하지 않음** — meta B 그대로 스크립트만 바꾸면 validate(details·meta)·compare·deploy 어디에도 걸리지 않아 데이터 회차에 사람이 안 본 새 모양이 자동 배포된다(M4 위반). 역방향 가드: config 가 B 인 채 C 파일이 오면 apply·validate 가 요란하게 멈춤 [실측 E3b].
- **숫자·배열은 1벌**: 01 `labels`·'노출수'·'총비용(원)', 06 `labels`·'평균노출순위' 배열과 `min-width:3280px` 텍스트는 그대로(apply L189~194·L216~222 · compare "01/06 labels" 정확히 2개 · validate 2×41 그대로) — 접기 안·창·가로 분기는 같은 data 객체를 재사용한다(배열 2벌 구현은 compare "01/06 labels" 가 DIFF 로 잡는다 [실측 e8]). 접기 안 컨테이너·캔버스 컨테이너에 `min-width`·`data-*` 속성을 더하지 않는다(apply 앵커 0곳 FAIL [실측]) — 접기 안 차트 폭은 JS 가 본 컨테이너의 inline 값을 읽어 옮긴다.
- **분기 = `matchMedia('(max-width: 640px)')`**(배포본 모바일 CSS 경계와 같은 값) · load 판정 + `change` 재판정(구형 iOS `addListener` 폴백) · 재판정 핸들러는 **상태 비교**(mq.matches ↔ 현재 모양; 로드 직후·afterprint 뒤에도 change 가 한 번 더 온다 [실측 A-3])·**동기 완료 뒤 `sync()` 직접 호출**(resize 디바운스에 기대지 않음 [실측 A-8]) · **인쇄 규약 명시**(안마다 아래 "인쇄" 행 — 잠금 또는 인쇄 전용 모양 + 동기 `chart.resize()`) · 분기 JS 는 차트 스크립트 **끝**(placementChart 뒤, 별도 `<script>` 또는 try/catch — 예외 하나가 뒤 차트를 못 막게, 기능 감지 `'matchMedia' in window`) · 모바일에서만 보이는 요소는 `@media` 가 아니라 JS 가 붙이는 `html.mob` 클래스로(인쇄 레이아웃 794px 가 뒤집지 못하게 [실측 B-R1]).
- **검사(공통)**: validate `check_layout` 확장(meta C + 분기 표지 — 전용 주석 `/* saero:mobile-branch 01 */`·`06` 수 = config `markers.mobile_branch`(JS 의 `if (M)` 수를 세지 않는다 [R6]) + matchMedia 리터럴·CSS `@media (max-width: 640px)` 각 1건 = config `mobile_max_px`(고를 항목 9)) · mutation 변조·0건 가드·config 실험 각 +1 · test_apply ApplyLayoutC(옛→B→C 사슬·B→C·멱등·손 수정 FAIL·서술 표지 36 바이트 불변) + L255·L338 리터럴 · **`tests/chart_check.py` 신설**(playwright chromium 임시 프로필 · CDN 2건 allow-list · 인자 index.html + compute.json [+ --base 직전 배포본] · 390·1280(+360 선택) × 01·06: tick = n(또는 창 k·묶음 수) · 보이는 datalabels 수 · 글자 상자 겹침 0(padding 상자 겹침은 기준 배포본 값 이하) · 캔버스 밖 0 · 제목 띠 침범 0 · 문서 scrollWidth = 폭 · 8 캔버스 전부 `Chart.getChart` 존재 · pageerror 0 · 회전 390→844→390(tick·minWidth 복원·뱃지·at-end·접기 안 차트 존재) · **인쇄는 page.pdf 실물**(pypdf: 01·06 캔버스 이미지 존재·그려진 픽셀 > 0·클립으로 보이는 일수·summary 글자) — 자리(precheck 안/밖)·CDN 불가 정책은 고를 항목 8) · overflow_check 그대로(Chart.js 미로드 — details 열고 3폭) · test_deploy 그대로(게이트 4건이 B→C 를 이미 시험).
- **공통 선택 요소 S(스크롤 시작 최신 쪽)**: PC 및 접기 안 전 기간 차트의 가로 스크롤을 오른쪽 끝(최신)에서 시작 — sync 래퍼 감싸기 뒤 `scrollLeft = scrollWidth`(load → setTimeout 0, toggle → sync 뒤) + 왼쪽 페이드 `.scroll-fade::before` + `.at-start` 규약 + 뱃지 문구(`← 좌우로 밀어서 전체 보기` 그대로 또는 `→ 왼쪽으로 밀면 이전 날짜`) — 숫자·배열·검사 변경 0, 인쇄 무관(scrollLeft 0 기준) [실측 S]. 어느 안에도 붙일 수 있다(고를 항목 6).
- 범례 bottom · 팔레트(ink·mintDark·#cdeee7) 그대로 · 새 CDN 0 · 01 인사이트 박스 ①②③·서술 표지 바이트 불변(변환은 표지 밖만) · 06 제목 문구 '낮을수록 상단' 그대로(광고 노출 위치 — desc 와 짝 [A-5·R8]).

### 3.1 설계안 비교(프로토타입·보정판 실측 — work/P, work/W)

| | **A 모바일 가로 막대**(날짜 세로축, 01+06) | **B 최근 7일 창 + 접기 안 전 기간 차트**(01+06) | **C 주 단위 묶음 + 접기 안 일별 전 기간**(01 만) |
|---|---|---|---|
| 핵심 | ≤640px 에서 dailyChart 를 `indexAxis:'y'` 가로 콤보(노출 막대 + 총비용 점·선, 값축 x 상단 '노출수'·x1 하단 '비용(원)'), rankChart 도 가로(순위축 x reverse·min 1 상단) · 컨테이너 height·min-width 는 JS 가 런타임에(01 `26n+90`·06 `22n+70`, minWidth 0 — 원래 값은 `box.dataset.minwidth` 에 보관해 PC 복귀 때 복원) · HTML 마크업·배열 변경 0 | ≤640px 에서 같은 canvas 가 최근 k=7일만(category `x.min = n−k`) · tick 두 줄 `'9/29'`/`'(화)'` · 창 밖 datalabel 숨김 · 비용 라벨 자리 계획(planCost — 이웃 라벨과 18px 이상, 막대 라벨 상자도 회피 [F3]) · 01 y·y1 제목 숨김(범례가 대신) · 카드 아래 `<details class="fold" id="dailyFold">` summary `이전 N일(M/D~M/D) 펼치기 — 전 기간 차트`(기계 자리) → 안에 `dailyChartAll`(같은 배열, 3,280 폭 스크롤, 펼칠 때·beforeprint 때 생성) · 06 같은 꼴(`rankFold`·`rankChartAll`, 창에 순위 라벨 7개) · PC 는 접기 숨김(`html.mob`) | ≤640px 에서 dailyChart 를 주별 콤보(묶음 6: 노출 합 막대 + 총비용 합 선, 라벨 `M/D~M/D` 두 줄, 부분 묶음 `(N일)`) · y·y1 눈금 숨김(제목 유지, 44.9px/묶음) · 카드 아래 `dailyFold` summary `일별 N일(M/D~M/D) 펼치기 — 전 기간 차트` → `dailyChartAll`(일별 41일 3,280 스크롤) · 06 그대로(주별 가중순위는 compute 키 없이 못 만듦) |
| 모바일 390 [실측] | 41일 전부 한 화면 폭 안(canvas 328×1,156 · 24.6px/행) · datalabels 82/82 · 겹침 1(8/26 `497원`/`150`, 기준에도 있음) · 밖 0 · 뱃지·페이드 없음 · 섹션 1 높이 901 → **1,746(+845)** · 06 328×972 · 라벨 41/41 겹침 0 · 866 → 1,567(+701) · 첫 화면(844)에 8/26~9/6 ≈12행, **10/5 는 머리에서 1,132px 아래**(배열 순서 그대로 위 8/26 → 아래 10/5; `scales.y.reverse` 로 최신 위 가능 [실측 런타임 전환]) · 문서 높이 10,153 → 11,699 | 창 9/29~10/5 7일 · 33.5px/일 · tick 7 두 줄 · 보이는 datalabels 14(+06 순위 7) · **겹침 0 · 밖 0**(B2 보정판; 360 폭 → 겹침 1·320 → 6 [B-R3]) · 섹션 1 894 / 펼침 1,213 · 06 859 / 1,138 · 펼친 전 기간 차트는 8/26 부터(sync 래퍼로 scrollLeft 0 — S 를 붙이면 끝부터) · k=10 → 겹침 13·06 tick 5/10, k=14 → 19·7/14(**390 에서 겹침 0 은 7 뿐**) | 6묶음 `8/26~8/31(6일)`…`9/29~10/5` · 노출 합 [2357, 2797, 1510, 1878, 1804, 1876] · 비용 합 [36397, 72749, 76907, 95827, 90869, 70635](합 = 일별 합) · datalabels 12/12 · C2 보정 뒤 겹침 1·밖 1(`95,827원` 상단 잘림 — y1 grace 로 0, 글자 겹침 1쌍 `36,397원`×`72,749원`) · 섹션 894 / 1,213 · **묶음은 회차마다 +1**: 8묶음(10/20) padding 접촉 9·글자 겹침 0, 10묶음(11/2) 글자·tick 겹침(`2,3572,797…`) [실측 Crev fix_8a·fix_10a] |
| PC 1280 [실측] | 기준과 동일(canvas 3,280×280 · 첫 화면 10일 · 섹션 841/589 · datalabels 82/0) — PC 분기 옵션 값 = 현재 L2014~2027·L2164~2192 | 기준과 동일 · 접기는 DOM 에 있고 숨김(validate 는 details 7 셈) | 기준과 동일 · HTML 에 주별 배열 3개가 더 들어감(그려지는 모양 동일) |
| 바뀌는 파일·함수·config | config: `layout_id` C · `markers{details 5, mobile_branch 2}` · `mobile_max_px 640`(고를 항목 9) · (행 높이 26/22 는 템플릿 리터럴, report-structure 에 적음) / apply: `CHART01_C`·`CHART06_C` 템플릿(≈90행 — `new Chart(document.getElementById('dailyChart'), {` 부터 다음 `\n});\n` 까지를 통째로 교체, 배열 자리는 빈 `[]` 를 같은 회차 값 교체가 채움; labels·두 dataset 선언이 블록 첫 `new Chart` 앞 — chart()/labels() 앵커 생존 [실측 apply "변경 없음"·md5 동일]) · `convert_b_to_c`(≈25) · 사슬 ≈15 / compute·compare·deploy 변경 0 / validate `check_layout` +≈12 / mutation +3 / test_apply +≈45 + 리터럴 2 / chart_check 신설 ≈120 / 배포본 index.html: L5 meta + 01·06 스크립트 블록만(서술 표지 36 바이트 동일·섹션 HTML 동일 [실측 R_code diff]) | config: `layout_id` C · `markers.details 7` · 창 일수 = `recent_days` 재사용 또는 **별도 키 `mobile_window_days: 7` + 정적 상한**(03 의 recent_days 를 올리면 창도 커져 겹침 [F4] — 고를 항목 3) / apply: `MONLY_CSS`(`.m-only{display:none}` `html.mob .m-only{display:block}`) · `FOLD1`/`FOLD6` 마크업 · `M01_JS`(≈75행 — Chart.getChart 로 기존 차트를 읽어 x.min·tick 두 줄·datalabels·padding 전환, planCost, make(접기 안 차트 — datalabels 는 리터럴 덮개, 함수 0 [F6·B-R7]), judge, beforeprint 동기 생성) · `convert_b_to_c`(5 앵커 once: meta · `</style>` 앞 · dailyChart `.scroll-x` 닫힘 뒤 · rankChart 닫힘 뒤 · 차트 스크립트 끝) · 매 회차 summary 2곳(03 L254~255 꼴 once_in) + `const RECENT_DAYS = k` 1곳 / compute·deploy 0 / validate `check_layout`(details 7 · RECENT_DAYS = config · canvas All 2) + 신설 "01·06 접기 summary = CSV 일수 − k"(독립 검산) / compare +2(01·06 summary = labels − k; "03 행 수" 대조는 min(k,n) 아니면 넣지 않음 [F8]) → 101 / mutation 변조 3·가드 1 / test_apply(+ApplyBtoC·summary stale·리터럴 2) / chart_check / 배포본 +≈93행 | config: `layout_id` C · `markers.details 6` · `weekly_block_days 7` · **묶음 규칙 키**(고를 항목 3-C: `per_block_px`(min-width 스크롤, 버그 8 방식) 또는 `max_blocks`) / compute `01.주별{block_days, blocks, labels, 노출, 총비용}`(≈15) / apply: `C_CSS`·`FOLD1`·`C_CHART_JS` 템플릿(≈55, 주별 라벨 키는 `wlabels:` 로 두어 블록 안 `labels: [` 를 하나로 [C-R3]) · `convert_b_to_c`(≈30) · 값 교체 3 앵커 + summary 1 · 옛 compute 에 `01.주별` 없으면 ApplyError / validate 신설 `check_weekly_blocks`(CSV 로 묶음 재계산 — 라벨·합·Σ = KPI·summary N·**묶음 수 ≤ max**)(≈40) / compare +5(주별 labels·노출·총비용·합 = 일별 합·summary) → 104 / mutation 변조 1·가드 1·config 실험 1 / fixture compute.json 에 `01.주별` / test_apply +≈45 / chart_check |
| 검사 변경 — validate `check_date_labels` · compare "01/06 labels" | **둘 다 그대로**(날짜형 배열 2개 × 41 [실측 PASS·OK]) · `check_chart_width` 그대로(HTML min-width 텍스트 유지) · `check_layout` 만 확장 · validate 24 그대로(이름 변경 0) · compare 99 그대로 — **가장 적음** | **둘 다 그대로**(배열 1벌 재사용) · `check_chart_width` 그대로(접기 컨테이너에 min-width 없음) · `check_layout` 확장 + 신설 1 → validate 25 · compare 101 | `check_date_labels` 그대로(주별 라벨은 `'M/D~M/D'` 꼴이라 검사 밖) · "01/06 labels" 그대로(정규식이 주별을 안 잡음 [실측 OK]) · validate 25(주별 묶음) · compare 104 |
| 레이아웃 판·게이트 | 3.0 공통 — C 판 표지 = 분기 주석 2 | 3.0 공통 — details 7 + RECENT_DAYS + canvas All | 3.0 공통 — details 6 + `wlabels` + summary |
| 06 포함 | **포함**(390 첫 화면 4일로 같은 문제) — compute `06.rankChart` 41값·labels·정의(그룹 전체 가중순위 전 기간) 그대로, 축 방향만 → [의도된 동작] 2·SKILL.md 계산 규칙·06 절 **안 깨짐**(결정 고침 없음; 모바일에만 순위 라벨 41개 = 같은 배열 표시) | **포함** — 값·정의 그대로, **보이는 기간**만 창 7일 + 접기 안 전 기간 → 안 깨짐(06 절에 "모바일 창은 보이는 기간만" 한 줄) · 모바일 창 순위 라벨 7개는 선택 | **제외(기본)** — 주별 가중순위는 `06.주별` compute 키·정의·검사 한 벌이 더 들고 06 은 선 하나라 4일 화면에서도 추세는 읽힘(숫자 손실 0). 포함하면 [의도된 동작] 2 에 "일별 차트(접기 안)에만, 모바일 주별 값은 06 절 '주별 가중순위' 정의" 를 명시해 결정을 고친다 |
| 숫자 (가)/(나) | **(가)** — 파생도 없음: HTML 새 숫자 0, compute·compare 변경 0 | **(가)** — 창·접기 안 차트 모두 같은 배열 · 새 값은 `const RECENT_DAYS = k`(config 를 apply 가 옮기는 기계 자리)와 summary 의 N·날짜(labels 와 k 에서 apply 계산) | **(나)** — 주별 노출 합·비용 합·라벨 = compute `01.주별` + apply + compare 5 + validate 독립 검산 + mutation(네 겹) · summary N·날짜는 기계 자리 |
| 접기 규약 | 해당 없음(details 5 그대로 · beforeprint FOLD_JS 그대로) | summary 2곳 매 회차(apply, 막음 M2) · markers.details 7 · validate 짝·summary 검사 · overflow details 7 열고 3폭 [실측 PASS] · **접기 안 차트는 toggle(첫 펼침) 또는 beforeprint 에서 동기 생성(`animation:false`)** — toggle 만 믿으면 인쇄 중에 안 만들어진다(toggle 은 비동기 태스크 [실측]) · toggle → sync 가 뱃지·페이드를 붙임 · PC 에선 안 만듦 · 회전으로 PC → 모바일 복귀 때 열려 있으면 다시 생성(`if (det.open) makeAll()` [RC-2]) | summary 1곳 매 회차 · markers.details 6 · 나머지 B 와 같음 |
| 인쇄(page.pdf 실물 [실측]) | load 1회 판정 그대로면 모바일 PDF 에서 01 캔버스(1,156px)가 **쪽 나눔에 통째로 빠짐**(2쪽 빈 카드·3쪽 눈금 한 줄 — 기준 ≈8.9일보다 나쁨) · 재판정을 mq change 에 걸고 동기 `chart.resize()` 면 기준과 같은 ≈8.9일 · **beforeprint 에 가로 모양 유지 + 높이 ≤ ≈1,000px 캡 + resize, afterprint 복구(F 변형)면 41일·라벨 82 전부 한 쪽**(06 도 같은 캡, 46일부터 한 쪽 초과) [실측 skep3r F390_p2] · PC 는 지금과 같음(≈8.9일) · 고를 항목 10 | 모바일 PDF = **창 7일만**(접기는 `html.mob` 라도 beforeprint 안에서 만든 캔버스를 Chromium 이 래스터화하지 않음 — 사용자가 미리 펼쳐 둔 경우에만 ≈8.9일 · 03 표에 총비용 41일은 찍힘) · 기준(≈8.9일, 가장 오래된 쪽)과 같은 크기의 손실이 날짜만 바뀜 · PC 그대로 · 41일 전부를 원하면 인쇄 전용 가로 막대(A 의 F 변형)를 beforeprint 에 더하는 길뿐(+≈25행) | 설계 그대로(mq change 재판정, 잠금 없음)면 **빈 캔버스**(RC-1, 막음) → `printing` 플래그 한 줄(beforeprint true·afterprint false·build() 가 무시)로 주별 6묶음·12 라벨이 찍힘 [실측 C_rc_g2] · 접기 안 일별은 B 와 같이 PDF 에 없음 · PC 그대로 |
| 분기 재판정 | load + mq change(상태 비교·동기 완료·sync 직접) · 컨테이너 height/minWidth 복원(`dataset.minwidth`) · 06 두 분기 x/y 날짜축 `autoSkip:false` 명시 · 인쇄 잠금 또는 F 변형 | load + mq change(B 설계는 resize 200ms 였음 — page.pdf 중 resize 는 안 오므로 mq change 로 통일) · setMode(min-width 0 ↔ 원래 값 · x.min · tick callback · 제목 · padding · planCost 재계산) · 인쇄: 창 유지(mq change 가 PC 로 뒤집으면 3,280 폭으로 ≈8.9일이 찍히는 것도 선택지) | load + mq change(destroy → 재생성) · `printing` 잠금 · 접기 열림 상태 재생성 |
| "보이는 숫자 누락 0" 검사 | chart_check: 390 01 tick 41·라벨 82/82·밖 0·글자 겹침 ≤ 기준 / 06 41·41/41 / 1280 = --base 측정값 / 회전 390→844(tick 41·scrollWidth 3,280·06 ticks 41·뱃지·at-end) → 390(로드와 동일) / **인쇄 = page.pdf 실물**(01·06 이미지 존재·그려진 픽셀·클립 일수 — F 변형이면 41일) / 8 캔버스·pageerror 0 · HTML = compute: compare 99·validate 2×41·apply 멱등(그대로) · 못 지키는 것 = 실기기 폰트·회전 체감·공유→PDF·PWA 오프라인 캐시(온라인은 network-first 라 첫 열기에 새 판 [A-9]) → **사용자 시크릿 창 몫** | chart_check: 390 창 tick k·라벨 2k(+06 k)·글자 겹침 0·밖 0·제목 띠 침범 0·뱃지 0 / 접기 열림 All 폭 = minwidth·tick n·라벨 2n·밖 0·겹침 ≤ 기준 / 1280 = --base / 회전 n ↔ k·minWidth 복원·접기 none ↔ block / 인쇄 = page.pdf 실물(창 캔버스 이미지 + summary 글자) / 8+2 캔버스·pageerror 0 · summary = labels − k(validate CSV 독립 + compare) · 360 폭 추가 여부는 고를 항목 8 · 못 지키는 것 = 실기기·공유→PDF → 시크릿 창 몫 | chart_check: 390 주별 labels/data = compute `01.주별`·라벨 2×묶음·글자 겹침 0·밖 0 / 접기 열림 일별 41·82 / 1280 = --base / 인쇄 = page.pdf 실물(afterprint 뒤 상태 + 01 이미지 픽셀 > 0) · validate 주별 독립 검산(CSV) + 묶음 수 ≤ max(정적·CDN 무관) · compare 5 · 못 지키는 것 → 시크릿 창 몫 |
| 리스크 | 세로 +845/+701px(인사이트 박스·06 매칭표가 1.5화면 아래) · **높이가 누적 기간에 비례해 는다**(90일 ≈ 2,430px = 3화면 — 행 높이 하한·모바일 기간 창 규칙이 아직 없음, 이월 A-6) · 총비용 선이 세로로 흐르는 모양이 낯설 수 있음(사용자 화면 확인이 유일한 판정) · 첫 행 겹침 1 잔존 · 인쇄 규약을 안 넣으면 모바일 PDF 01 소실(검사가 잡음) · 변환 앵커(`new Chart(…dailyChart…{` ~ `\n});\n`)가 손으로 바뀐 판이면 시끄러운 FAIL | 접기 안 차트가 PDF 에 안 찍힘(기존 한계와 같은 크기) · 접기를 열면 8/26 부터(S 없이는 최근 주가 가장 멂 [B-R4]) · planCost 가 데이터·폭(360·320)·네 자리 노출(`1,234`)에서 겹침 1~6 [B-R3] — chart_check 임계를 "글자 겹침 0" 으로 두면 저소진 회차가 6단계에서 멈출 수 있음(F3 — 기준 배포본 값 이하로 완화) · 창 k 와 03 recent_days 결합 · M01 ≈75행이 배포본에 들어감 · 접기 7개 규약 유지 비용 | 묶음 수가 매 회차 +1 → 10묶음(11/2)부터 글자·tick 겹침(묶음 규칙 없으면 확실) · 마지막 날 기준 묶음은 회차마다 과거 라벨·합이 바뀜(`9/1~9/7 72,749원` 이 다음 날 `9/2~9/8`) [C-R4] → **open_date 기준 앞에서부터 7일, 마지막 묶음만 부분** 이 권장(과거 고정) · 주별 = 새 숫자라 검사 4겹 · 값축 눈금 숨김이 버그 5 와 닿음(문서로 못 박음) · 01 블록 템플릿 교체 · 06 미포함이면 06 만 3,280 스크롤로 남음 |
| 예상 비용(구현 1회차) [추론] | 코드 ≈ 220행(apply 130 · validate 12 · mutation 10 · test_apply 45 · config 4) + chart_check 120 · 문서 ≈ 60행 · 배포본 변경 = meta + 스크립트 블록 2 | 코드 ≈ 250행(apply 125 · validate 30 · compare 10 · mutation 12 · test_apply 40 · config 3) + chart_check 130 · 문서 ≈ 80행 · 배포본 +≈93행 | 코드 ≈ 300행(apply 120 · compute 15 · validate 40 · compare 10 · mutation 15 · test_apply 45 · fixture 8 · config 6) + chart_check 130 · 문서 ≈ 75행 |
| 반박 결과(6절) | 막음 후보 3(R1·A-1·A-2) → 검증 뒤 **막음 0**(셋 다 "프로토타입 load 1회 판정" 또는 "검사 커버리지" 문제 — 설계 줄에 반영) · 이월 10 | 막음 후보 2(F1·B-R1) → **막음 0**(F1 = 기존 구조, B-R1 = 기존 한계 크기와 같음 — 설계 줄 정정) · 이월 13 | 막음 후보 4(RC-1·RC-2·RC-3·C-R1) → **막음 1(RC-1)** + 같이 1(`printing` 플래그 줄) · 이월 9 |

### 3.2 조정자 의견(한 줄, 결정은 사용자)
**A 가로 막대를 뼈대로** — 세 안 중 유일하게 검사(validate 24·compare 99)·apply 앵커·숫자 자리가 **변경 0** 으로 통과했고(기준 사본에 프로토타입을 얹어 validate 24/24·compare 99/0·apply 멱등 [실측]), 모바일에서 41일·숫자 82개가 접기 없이 전부 보이며, 인쇄도 F 변형(beforeprint 높이 캡)으로 41일 전부를 찍을 수 있는 유일한 안이다. 비용은 세로 +845/+701px 와 "선이 세로로 흐르는" 낯섦 — 첫 적용 "보류" 회차의 390 화면 확인이 판정 자리. B 는 익숙한 모양을 지키고 최근 7일 창이 또렷하지만(겹침 0) 접기·summary·RECENT_DAYS·planCost 등 움직이는 부분이 가장 많고 접기 안이 PDF 에 안 실린다. C 는 새 숫자(나)라 검사 4겹이 더 들고 묶음 수가 매 회차 자라 10/20~11/2 회차부터 묶음 규칙 없이는 겹친다 — 2회차 후보. 어느 안이든 3.0 공통(판 C · 사슬 LAYOUT_B · mq change 재판정 + 인쇄 규약 · chart_check page.pdf 실물)은 같이 간다.

## 4. 완료 기준 표(이후 회차는 이 표로만 판정 — 공통 행 + 채택 안의 3.1 "누락 0 검사" 행)

| 무엇이 | 왜 | 어느 코드·시험이 지키나 |
|---|---|---|
| HTML 숫자·배열 = compute(01/06 labels 날짜형 배열 정확히 2개 × 일수 · 노출·총비용·rankChart · min-width 2곳) · apply 멱등 · 서술 표지 36 블록 바이트 불변 | 기계 자리 보존 · 배열 2벌이면 한쪽만 갱신되는 묵은 숫자 | compare "01/06 labels"·"01 dailyChart"·"06 rankChart"·min-width 2 · validate 날짜축·min-width · test_apply(멱등·표지) · (B·C) 접기 안 컨테이너 min-width 0건 = validate check_chart_width 를 "정확히 1개" 로 바꾸거나 이월 F2 |
| **모바일 390 에서 날짜·숫자 누락 0** — 채택 안의 tick·datalabels 수 = 정의값, 캔버스 밖 0, 글자 겹침 0(padding 상자 겹침은 기준 배포본 값 이하), 제목 띠 침범 0, 접기가 있으면 열었을 때 전 기간 n·2n | 막음 기준(데이터 손실) · 사용자 목표 | **tests/chart_check.py**(신설 — CDN 허용, 자리는 고를 항목 8) · overflow_check 3폭(Chart.js 미로드) |
| PC 1280: tick·datalabels·첫 화면 일수·섹션 높이·뱃지 = 직전 배포본 측정값 | "PC 그대로" 를 수치로 | chart_check `--base` 대조 |
| 회전 390→844→390: 분기·tick·컨테이너 minWidth 복원·뱃지·at-end·(접기 열림 차트) 가 로드 때와 같음 | load 1회 판정의 구멍 [실측] | chart_check 회전 항목 · 재판정 = mq change 상태 비교·동기·sync 직접 |
| **인쇄(page.pdf 실물) — 모바일·PC 모두 지금 배포본(≈8.9일)보다 나빠지지 않음**, 채택 안의 인쇄 규약대로(A-F 41일 / B 창 7일 + 03 표 / C 주별 6묶음) · afterprint 뒤 화면 복구 | 인쇄 중 mq change 로 빈 캔버스·쪽 나눔 소실 [실측] — emulate_media 값은 판정에 쓰지 않는다 | chart_check 인쇄 항목(pypdf 이미지 존재·그려진 픽셀·클립 일수·summary 글자) · 분기 JS 의 printing 잠금/beforeprint 규약 |
| 8(+접기) 캔버스 전부 `Chart.getChart` 존재 · pageerror 0 — 분기 JS 는 차트 스크립트 끝 + try/catch(실패 시 PC 모양) | 예외 하나가 뒤 차트를 전부 막는 구조(기존과 같음) | chart_check · 템플릿 규약 |
| meta = r2026-10-C = config · 분기 표지 2 · (B·C) details 수·짝·summary·RECENT_DAYS/wlabels · matchMedia 리터럴·CSS 경계 = config | 옛 모양·반쪽 변환으로 조용히 되돌아가지 않음 | validate `check_layout` 확장 · apply 판 가드·사슬 · mutation 변조·0건 가드·config 실험 |
| (B·C) summary 의 N·날짜 = labels − k / nlabels 매 회차 | 막음 M2(머리 묵음) | apply once_in · compare summary 항목 · validate CSV 독립 검산 · mutation 변조 · test_apply stale 시험 |
| (C) 주별 값 = compute `01.주별` 만(라벨·합·Σ = KPI) · 묶음 수 ≤ max 또는 per_block_px 폭 | 새 숫자는 compute 키만(checklist 16) · 묶음 증가 | compute · apply 3 앵커 · compare 5 · validate `check_weekly_blocks` · mutation 3 |
| **첫 적용은 사람이 작업본(390·1280 캡처 + 전후 비교 HTML + 시크릿 창)을 본 뒤에만 PUT** | 막음 M4 | deploy.py 게이트(base B ≠ file C → FAIL, `--layout-change`) · test_deploy 4건 · /saero-run "보류" 회차 · code-tab.md 4절 |
| 팔레트 밖 색 0 · 새 CDN 0 · 단일 파일 · 범례 bottom · 01 박스 ①②③·compare 서술 불변 · 문서 가로 넘침 0 | 리포트 원칙 | chart_check(외부 요청 = CDN 2) · overflow_check · 검증 회차 grep |
| 문서 = 코드(report-structure "레이아웃 판 r2026-10-C"·01·06 / css-and-layout 반응형·접기·버그 4·5·8·12 / SKILL.md 원칙·체크 3·4·검산 수·compare 수 / checklist 2·16·17·27·회귀 표 / apply·test_apply docstring·FOLD_CSS 주석 / code-tab 6단계) | 7절 충돌 표 | 검증 회차 대조 |
| **실제 환경 리허설 한 줄**: 구현 끝에 clone 사본(`work/R3`)에서 외부 쓰기 0 으로 — `cp work/index.html work/R3/{index,prev}.html` → compute → `apply.py --layout`(B→C 변환 + 값, 두 번째 실행 바이트 동일) → validate 전부 PASS → compare DIFF 0 → overflow 3폭 → chart_check 390/1280(+회전·page.pdf) → mutation 전부 살아 있음 → test_apply·test_deploy·test_compare_sections·test_narrative_check → 390·1280 캡처 + 전후 비교 HTML(mk_compare.py 류) — deploy.py 는 구현 회차에도 돌리지 않는다(첫 적용 /saero-run 7단계의 dry-run `[주의] 레이아웃 판이 바뀜` 이 그 자리) | 제약 | 구현 회차 R1~R9(채택 안의 설계 JSON `rehearsal` 초안을 지시문에서 확정) |

## 5. 막음 기준
막음 기준 : 정상 흐름에서 조용히 틀린 외부 쓰기 · 데이터 손실(이 작업에서는 **리포트에서 날짜·숫자가 조용히 빠져 보이지 않게 되는 것**도 포함 — 화면과 인쇄(PDF) 둘 다, 단 인쇄는 "지금 배포본 ≈8.9일보다 나빠지는 것" 이 손실) · 자격 증명 노출(작업 알고리즘 5절 saero 줄). 공개 배포본이 바뀌므로 "실수 둘 이하". 회차 중에 넓히지 않는다 — 라벨 상자 겹침·세로 길이·접기 안이 PDF 에 안 실리는 기존 한계는 막음이 아니라 완료 기준 표·이월로 다룬다.

## 6. 스스로 반박 — 독립 검토자 6(안마다 D 코드·검사·배포 경로 / E 사장님 화면·실기기·인쇄·원칙·문서, 전부 사본에서 실측) → 막음 후보 9건을 회의론자 3명씩(27표)이 재검증 → 비평자 1
**막음 검증 표**(살아남음 = 3표 중 2표 이상 "반박 안 됨"):

| 안 | 후보 | 내용 | 표 | 결과 · 이유 한 줄 | 설계 반영 |
|---|---|---|---|---|---|
| A | R1 | 가로 캔버스가 PDF 쪽 경계에서 잘려 최신 행부터 빠짐 | 반박 3/3 | 기전이 틀림(잘리는 게 아니라 load 1회 판정 상태에선 통째로 빠짐) · 기준 배포본도 32일을 못 찍는 기존 한계 · 재판정 + 동기 resize 로 기준과 같음, F 변형으로 41일 | 3.0 재판정·인쇄 규약, chart_check 는 page.pdf 실물 |
| A | A-1 | 모바일 PDF 에서 01 차트 통째 소실 | 반박 2/3 | 현상은 맞으나 프로토타입(load 1회)의 성질 — 설계가 약속한 재판정을 mq change + 동기 resize 로 구현하면 ≈8.9일, F 변형이면 41일 [실측] | 위와 같음(인쇄 규약을 설계 줄에 명시) |
| A | A-2 | 회전 뒤 min-width 복원이 검사 밖 — 06 날짜 절반 빠짐 | 반박 3/3 | 설계 원문에 보관·복원이 있고 그대로면 손실 0 [실측] · 검사 커버리지 공백일 뿐 | chart_check 회전 항목에 scrollWidth·06 ticks 41·뱃지 |
| B | F1 | M01 블록 예외 하나로 09·10 차트가 빈 캔버스 | 반박 3/3 | 인위 예외로만 재현 · 배포본도 한 `<script>` 에 직렬인 기존 구조 · chart_check tick 판정이 이미 잡음 | 3.0: 분기 JS 는 스크립트 끝 + try/catch |
| B | B-R1 | `.m-only` 가 인쇄 레이아웃에서 숨어 접기 안 차트가 PDF 에 없음 | 반박 3/3 | 현상 맞음 · 그러나 기준 PDF 도 ≈8.9일만 찍는 같은 크기의 기존 한계 · 제안한 fix(html.mob)로도 beforeprint 생성 캔버스는 PDF 에 0개 [실측] | 설계 인쇄 행 정정("창 7일만") · chart_check 인쇄 = page.pdf 실물 · html.mob 은 summary 글자가 찍혀 가치 있음 |
| C | **RC-1** | 인쇄 중 mq change 로 build() 재생성 → 모바일 PDF 01 빈 캔버스(접기도 숨김) | **반박 0/3 — 막음** | 설계 그대로면 인쇄 한 번에 매번 · 기준(≈8.9일)보다 나쁨 · 설계의 chart_check (4) 는 beforeprint 시점이라 통과시킴 | **같이**: `printing` 플래그 한 줄(beforeprint true · afterprint false · build 무시) [실측 g2 주별 6묶음 찍힘] + 인쇄 검사를 afterprint·PDF 픽셀 기준으로 |
| C | RC-2 | 접기 펼친 뒤 회전 왕복하면 접기 안 차트 빈 캔버스 | 반박 3/3 | 눈에 띄는 빈 상자 · summary 닫았다 열면 복구 · 세 단계 조작 | 3.0 접기 규약 `if (det.open) makeAll()` |
| C | RC-3 | 묶음 수 무제한 → 8묶음부터 겹침, precheck 가 못 봄 | 반박 3/3 | 라벨은 전부 그려짐(padding 접촉) · 기준도 겹침 1 안고 배포 · 기준 넓히기 | 묶음 규칙 키(고를 항목 3-C) + validate 상한 |
| C | C-R1 | 주별 라벨 겹침이 지금도 남고 매 회차 커지는데 매 회차 검사가 없음 | 반박 2/3 | 글자 겹침은 6~8묶음 1쌍, 10묶음(11/2)부터 여러 쌍 · 숫자는 전부 그려짐 | 위와 같음 + chart_check 자리(고를 항목 8) |

**이월**(한 줄씩 — 설계 줄에 넣지 않음, 첫 실사용 뒤 또는 채택 안 구현 지시문에서 "(반영)" 표시된 것만 설계 줄로):
- 공통: 옛→B→C 사슬은 `LAYOUT_B` 상수(반영 3.0) · test_apply L338·L255 리터럴, SKILL.md 검산 수·compare 수(L292·L513·L548)·checklist 16·21·회귀 표 "순회" 문구·css-and-layout 버그 4("8개 차트")·5(예외 한 줄)·접기 안내 5(details 수)·반응형 420px·apply docstring L8·L17·FOLD_CSS 주석 — 리터럴 갱신 통합 목록(반영 4절 문서 행) · chart_check 의 자리·CDN 불가 정책·보류 회차 절차(고를 항목 8) · `work/prev.html` 이 clone 에 없음 → 리허설은 `cp work/index.html` 로(반영 4절) · 분기 JS 가 한 `<script>` 안이라 예외 폭발 반경(반영 3.0 try/catch) · 실기기 [추론] 묶음(iOS Safari/PWA 회전·공유→PDF·beforeprint 안 오는 경로·첫 페인트 깜빡임)은 첫 적용 보류 회차 체크리스트(390 세로 · 844 회전 · 접기 펼침 · 인쇄 미리보기)로 — 사용자 실기기 몫 · beforeprint 동기 생성 캔버스가 PDF 에 실리는지(B 실험 0개 vs C g2 실림 — animation·클래스 토글 시점 차이 미확인)는 구현 회차 실측 · 기준값 자리 표(mobile_max_px·행 높이·창 일수·묶음 키)를 config 로 둘지(고를 항목 9) · compare 첫 일치·validate 여분 min-width 허용(F2 — "정확히 1개" 규칙 후보) · 10/06 이월 D5(toggle sync 실기기)·검증 이월 4(mk_compare 저장소화 — 이번에 세 번째로 사본 사용) 그대로.
- A: 높이가 n 에 비례(A-6 — 행 높이 하한 또는 모바일 기간 창 규칙, ≈90일 전 정기점검) · 첫 화면에 10/5 없음(A-10 → 고를 항목 2 (나) reverse) · 06 제목 '오른쪽' 안은 **철회**(A-5·R8 — 그대로) · mobile_max_px 와 CSS 경계 대조(A-7·R5 — validate 가 CSS `@media` 도 셈, 반영 3.0) · `if (M)` 토큰 규약 대신 주석 표지(R6, 반영) · 재판정은 동기 + sync 직접(A-8, 반영) · PWA 문구 정정(A-9) · 인쇄 F 변형의 n 상한(≈90일이면 940/n 행이 11px 아래) · 첫 행 `497원`/`150` 겹침(구현 때 offset).
- B: 접기 열면 8/26 부터(B-R4 → 고를 항목 6 S) · planCost 가 막대 라벨·360/320 폭·네 자리 노출을 못 피함(F3·B-R3 — 글자 겹침 기준·기준 값 이하 완화) · 창 k 와 03 recent_days 결합(F4 → 별도 키 + 정적 상한, 고를 항목 3) · make() 덮개 리터럴(F6·B-R7, 반영) · compare "03 행 수" 는 min(k,n)(F8, 반영) · 06 창 순위 라벨 7개는 PC 에 없는 비대칭(선택) · 접기 7개 유지 비용 · 모바일 load 때 3,280 → 0 전환의 첫 페인트 [추론].
- C: 묶음 규칙 — 마지막 날 기준은 과거 라벨이 매 회차 바뀜(C-R4 → open_date 기준 앞에서부터, 권장 변경) · 주별 라벨 키 `wlabels`(C-R3, 반영) · 값축 눈금 숨김을 01 절·버그 5 에 못 박기(C-R6) · 접기 5곳 리터럴(C-R7) · RC-5 인쇄 검사 시점(반영 4절) · 06 포함 안(`06.주별` 정의) · 주별 비용 라벨 `72,749원`×`76,907원` 1쌍(y1 grace·짝홀 align).
- '죽음' 부류(강제 종료·응답 잃음·절전): 기존 공통 안전망(precheck 도장·deploy base 대조·재개 판정은 대상 상태) 그대로 — 시나리오별 추가 없음.

## 7. checklist·문서와 설계안이 닿는 곳(풀려면 사용자 결정)

| 문서·규칙 | 설계안이 닿는 자리 | 어떻게 |
|---|---|---|
| SKILL.md "가장 중요한 원칙"(레이아웃 판은 설계 회차·사용자 결정으로만) · report-structure.md "레이아웃 판 r2026-10-B" 절("이 판도 … 바꾸지 않는다") | 01(·06) 차트 자리의 모바일 모양·스크립트·CSS 변경 전부 | **사용자 원문 인용 + 판 r2026-10-C 절**(고를 항목 4) |
| report-structure.md "01. 일별 추이"(막대 라벨 하단·선 라벨 위·범례 bottom·컨테이너·x ticks) · 값축 눈금 규칙 없음 | A: 모바일은 가로(라벨 자리·축 이름 다름) / B: 창·두 줄 tick·y 제목 숨김 / C: 주별·눈금 숨김 | 절을 "PC 모양" 으로 두고 "모바일 모양(판 C)" 문단 추가 · (C) 눈금 숨김 조건 명시 |
| report-structure.md "레이아웃 판" 절 "01 … 차트 labels 는 시간 오름차순 그대로" | 배열은 전부 오름차순 그대로 — A 의 "최신 위" 는 `scales.y.reverse` 로 화면만 | 고를 항목 2 (나)일 때 "(화면 순서는 판 C 모바일 가로 막대만 reverse)" 한 줄 |
| css-and-layout.md 버그 5("라벨을 줄이거나 숨기는 것보다 … 스크롤 — 정보 손실 0") | B·C 두 줄 tick(나눔이지 줄임 아님) · B 창 밖 숨김(접기 안 전 기간) · C 값축 눈금 숨김 · 툴팁 안 채택 안 함 | 버그 5 에 예외 한 줄 |
| css-and-layout.md 버그 4(고정 높이, "8개 차트 전부") · 8(매주 늘어나는 폭 = config) | A: 모바일 높이 = 날짜 수 × 행 높이(폭이 아니라 **높이**가 는다) / B·C: 모바일 min-width 0 · C 묶음 폭 규칙 | 버그 4 캔버스 수 · 버그 8 에 모바일 줄 · 버그 12 신설(load 1회 판정·인쇄 중 mq change·toggle 비동기·컨테이너 속성 금지 [실측]) |
| css-and-layout.md "가로 스크롤 안내 자동화"(오른쪽 페이드만) · "반응형"(420px) · "PWA"(network-first) | S(시작 위치·왼쪽 페이드·at-start) · 분기 = JS `html.mob` 단일 출처 · 420px 정정 · PWA 문구 | "시작 위치" 항목 신설(고를 항목 6) · 반응형 절 개정 |
| css-and-layout.md "접기 안내" · 버그 11 · report-structure 접기 5 표 · config `markers.details 5` · apply FOLD_CSS 주석·docstring | B: details +2(01·06) / C: +1(01) → markers 7/6 · summary 기계 자리 행 · beforeprint 동기 생성·회전 재생성 | 표에 행 추가 · config markers · validate 기대값 · 주석·docstring 갱신 |
| checklist [의도된 동작] 2 · SKILL.md 계산 규칙(06 rankChart = 그룹 전체 가중순위 **전 기간**) · report-structure 06 정의 | A·B 의 06 포함: 배열·정의 그대로(전 기간 값이 HTML 에 전부), 화면만 가로/창 → 안 깨짐 / C 의 06 주별 가중순위는 새 정의 → 기본 제외 | 포함이면 [의도된 동작] 2 에 "모바일 화면 표시는 판 C" 한 줄 |
| checklist [의도된 동작] 17(overflow 는 Chart.js 미로드 · 라이브 차트 넘침은 시크릿 창 몫) · 14(라이브 판정) | `tests/chart_check.py`(CDN 허용·Chart.getChart·page.pdf)로 "시크릿 창 몫" 범위가 줄어든다 — 실기기만 남음 | 17 개정(고를 항목 8) |
| checklist 회귀 표 "06번 min-width·날짜축 라벨 검사가 date_based_sections 순회" | check_date_labels 는 HTML 전체(순회 아님) — 지금도 코드와 다름 | 문구 정정(설계안과 무관) |
| apply.py docstring L17 "앵커는 전부 정확히 하나" | chart()/labels() 는 count=1(둘이어도 첫 것만) | docstring 정정 또는 "정확히 하나" 검사 추가(C 는 필수에 가까움) |
| SKILL.md 체크 3·4 · 배포 전 검산 목록(24개·99항목) · code-tab.md 3절 6단계 · checklist 16·21 | 새 검사·compare 항목 수·chart_check 한 줄 | 숫자·문구 갱신 |
| 10/06 사용자 결정 6 "차트 폭 per_day_px 80 그대로(첫 실사용 뒤 판단)" · 16-④ | 이 회차가 그 판단 — 80 은 PC·접기 안 전 기간 차트 용으로 유지 | 결정 블록에 "16-④ 답 = 이 회차" 기록 |

## 내가 고를 항목
1. **설계안**: A 모바일 가로 막대(01+06) / B 최근 7일 창 + 접기(01+06) / C 주 단위 묶음 + 접기(01) / 보류. (조정자 의견 3.2: **A** — B 는 익숙한 모양 우선일 때, C 는 2회차 후보)
2. **A 의 세로 순서**: (가) 배열 그대로 위 8/26 → 아래 10/5 / (나) `scales.y.reverse` 로 **최신 위**(desc 의 10/5 가 첫 화면에 — 검토자 A-10 권장, 배열·검사 영향 0). 
3. **보이는 기본 일수·규칙**: A — 41일 전부(행 높이 26/22px — 20px 안도 가능, n 규칙은 이월) · B — k = **7**(390 에서 겹침 0 은 7 뿐 [실측]; 키 = `recent_days` 재사용 / **별도 `mobile_window_days` + 정적 상한**) · C — 묶음 7일, 규칙 **open_date 기준 앞에서부터(과거 라벨 고정, 마지막 묶음만 부분)** / 마지막 날 기준 · 묶음 증가 = per_block_px 스크롤 / max_blocks + 접기.
4. **레이아웃 판 올리기**: **r2026-10-C**(apply B→C 변환 + LAYOUT_B 사슬 + validate 기대값 + deploy `--layout-change` 첫 적용) / 판 유지(세 안 모두 비권장 — M4 를 막는 장치가 없음).
5. **첫 적용 범위**: **경로 C**(다음 /saero-run 을 "보류" 로 시작 · 5 교체 → 6 도장 · 390·1280 캡처 + 전후 비교 HTML(01·06) + 시크릿 창·실기기 확인(390 세로·844 회전·접기 펼침·인쇄 미리보기) → "배포" → `--layout-change`) / 같은 날 데이터 회차와 묶기. 날짜(평일 아침 데이터 회차와 겹치지 않게).
6. **스크롤 시작 위치(공통 S)**: PC 차트·접기 안 전 기간 차트를 **최신 쪽(오른쪽 끝)에서 시작**(왼쪽 페이드 `::before`·at-start·뱃지 문구 규약) / 지금처럼 8/26 부터. (B 를 고르면 B-R4 때문에 권장)
7. **06 rankChart**: **포함**(A·B — 정의 그대로, 화면만) / 01 만 · (B) 모바일 창 순위 라벨 7개 표시 / 없음.
8. **"보이는 숫자 누락 0" 검사 `tests/chart_check.py`**: 자리 = **precheck 밖(리허설·검증·첫 적용 보류 회차·정기점검)** / precheck 안(이 PC 는 CDN 가능 — 그러면 CDN 불가 시 FAIL 로 멈춤·[의도된 동작] 17 개정) · 폭 = 390·1280(+회전·page.pdf) / 360 추가 · 겹침 임계 = 글자 겹침 0 + padding 겹침 ≤ 기준 배포본 값.
9. **인쇄 규약**(채택 안의 3.1 "인쇄" 행): A — **F 변형(beforeprint 높이 캡 → 41일 한 쪽)** / mq change 재판정으로 기준과 같은 ≈8.9일 · B — 창 7일(+03 표) 그대로 / 인쇄 전용 가로 막대 추가 · C — `printing` 잠금(필수, 막음 RC-1). 사장님이 인쇄·PDF 를 쓰는지 답(11-②)이 이 항목의 무게를 정한다.
10. **기준값 자리**: `mobile_max_px 640`(config + validate 가 JS·CSS 리터럴 대조) / 리터럴 640 · 행 높이(A)·창 일수(B)·묶음 키(C) 를 config 에 둘지 · chart_check 폭 목록.
11. **더 물을 것**: ① 사장님 주 화면이 모바일인지(10/06 미확인 그대로 — A 의 세로 길이·B 의 접기 사용에 직결) ② 인쇄·PDF 를 쓰는지(A 는 41일, B·C 는 창·주만) ③ 10/06 회차 2 시크릿 창 확인(03·07·08 접기) 결과 ④ A 의 "선이 세로로 흐르는" 모양이 괜찮은지(work/P/compare_A.html 390 캡처).
12. **문서 개정 승인**: 7절 표 전부 + 정정 3(420px · 회귀 표 "순회" · apply docstring L17) + 리터럴 갱신 목록(6절 공통 이월 첫 줄).

**[넘길 때]** — 다음 세션에 붙일 글과 함께 단계의 모델·effort 를 같이 적는다(모델만 적지 않는다):

| 단계 | 세션·폴더 | 모델 · effort · 설정 |
|---|---|---|
| ③ 구현 | 작업 폴더 clone `D:\saero\feat-20261006-dailychart` 이어 쓰기(또는 새 clone) · 끝에 리허설 R1~R9 | **Opus 5.5 · ultracode** |
| ④ 첫 검증 | **`D:\saero-verify` 새 세션**, 새 clone(운영 폴더 읽기만) | **Fable 5.1 · ultracode** / 수정 뒤 재검증은 새 세션 · 바뀐 것만 · **Fable 5.1 · xhigh** |
| ⑤ 수정(막음이 있을 때만) | 새 세션(③ 세션을 이어 쓰지 않음) | **Opus 5.5 · xhigh · ultracode 끔**(같은 결함으로 2번을 넘으면 Fable 로 올릴지는 사용자) |
| ⑥ 병합 · 첫 실사용 | ④ 검증 세션에 이어서(갱신 회차가 돌지 않을 때 — last-audit 맨 위 충돌은 main 회차 절을 위에) → 운영 세션 `/saero-run` "보류" 시작 | **Opus 5.5 · high · ultracode 끔** |

## 마무리 기록(이번 회차)
- 커밋 = 이 절만(`audit/last-audit.md` 맨 위, 경로 지정 add, `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`, 전역 설정 변경 0). **push 0**(② 고르기 답을 이 세션에서 받은 뒤 "사용자 결정" 블록을 더해 다시 커밋). 커밋 해시는 자기 참조라 적지 않는다.
- 실측·프로토타입·비교 페이지·하위 에이전트 원문은 clone `work/M0/`·`work/P/`·`work/W/`(gitignore)에만 — 0절 목록. 워크플로 에이전트 37(하위 토큰 약 586만 · 도구 호출 986 · 69분).
- 운영 main 작업 폴더 HEAD `f799bb6` · `git status` 빈 것 · clone 추적 파일 변경 = 이 절뿐 · 네이버·API·배포 저장소 요청 0(무인증 fetch 도 안 함) · 키 파일 0 · SKILL.md·scripts·config·tests·data·registry 변경 0 · 10/06 기능 clone `D:\saero\feat-20261006-layout` 쓰기 0(mk_compare.py 읽어 복사만).


## 사용자 결정(2026-10-06 — ② 고르기, 탐색 세션에서 받음)
"추천안을 전부" → 내가 고를 항목 1~12 전부 권장안. 권장을 적지 않았던 자리는 설계안 A 원안·안전한 기본값으로 두고 여기 밝힌다(바꾸려면 사용자 한마디).
- 1 **설계안 A 모바일 가로 막대(01+06)** · 2 세로 순서 **(나) `scales.y.reverse:true` 로 최신 위**(배열은 오름차순 그대로 — 화면만, 06 도 같은 순서) · 3 41일 전부 · 행 높이 01 26px·06 22px(+90/+70) 그대로 — n 규칙(행 높이 하한·모바일 기간 창)은 이월(≈90일 전 정기점검) · 4 **판 r2026-10-C**(apply `convert_b_to_c` + `LAYOUT_B` 사슬 + validate 기대값 + deploy `--layout-change` 첫 적용) · 5 **경로 C "보류" 회차**(날짜는 병합 뒤 운영 세션에서 — 평일 아침 데이터 회차 뒤 같은 날, 2-1 같음 "다시 계산") · 6 **S 스크롤 시작 최신 쪽** — PC 분기(01·06, 회전 뒤 PC 복귀 포함)의 가로 스크롤을 오른쪽 끝에서 시작(sync 래퍼 감싸기 뒤 · 왼쪽 페이드 `::before` + `.at-start` · 뱃지 문구 그대로). PC 첫 화면 날짜가 8/26~9/4 → 9/26~10/5 로 바뀐다(PC 모양은 그대로) · 7 **06 포함**(배열·정의 그대로, 화면만 가로 + 모바일 순위 라벨 41개) · 8 `tests/chart_check.py` 는 **precheck 밖**(리허설·검증·첫 적용 보류 회차·정기점검 — 이 PC 에서 CDN 허용, CDN 미로드면 exit 2 = 통과 아님) · 폭 390·1280 + 회전 390→844→390 + page.pdf 실물 · 겹침 임계 = 글자 겹침 0, padding 상자 겹침 ≤ 기준 배포본 값(1) · 9 인쇄 = **F 변형**(beforeprint: 모바일 모양 유지 + 01·06 컨테이너 높이 ≤ config `print_max_height_px` + 동기 `chart.resize()` · afterprint: 높이 복구 + resize · 인쇄 중 재판정 잠금 `printing`; PC 는 지금처럼 ≈8.9일) · 10 기준값 = config `report_layout.mobile{max_px 640, print_max_height_px 1000, row_px{01 26, 06 22}, pad_px{01 90, 06 70}}` — apply 가 매 회차 템플릿 리터럴 한 줄(`var M = {…}`)로 쓰고 validate 가 `matchMedia` 리터럴·CSS `@media (max-width: …px)`·`M` 줄을 config 와 대조 · `markers.mobile_branch 2`(전용 주석 `/* saero:mobile-branch 01 */`·`06`) · 11 더 물을 것 ①~④ 는 **답 없음** — 사장님 주 화면·인쇄 사용 여부·10/06 회차 2 시크릿 창·A 의 세로 선 모양은 첫 적용 보류 회차에서 본다(미확인 그대로) · 12 문서 개정 전부 가(7절 표 + 정정 3 + 리터럴 갱신 목록).
- 설계안 A 안의 세부(3.0·3.1 A 열·6절 반영분 그대로): 06 모바일 제목 '낮을수록 상단' **그대로**('오른쪽' 안 철회) · PC 분기 옵션 값 = 현재 L2014~2027·L2185~2190 · 모바일 분기 = `indexAxis:'y'`, 값축 x 상단 '노출수'·x1 하단 '비용(원)'(06 은 x reverse·min 1·상단), 날짜축 `autoSkip:false`, 범례 bottom · 원래 `min-width` 는 `box.dataset.minwidth` 보관·PC 복귀 때 복원 · 재판정 = load + `matchMedia` change(상태 비교 · 동기 완료 · `sync()` 직접 · 구형 iOS `addListener` 폴백 · 기능 감지) · 차트 생성 블록은 제자리(apply 앵커 생존)에 try/catch(실패 시 PC 모양), 분기 도우미는 차트 스크립트 끝 · validate·compare 의 `check_date_labels`·"01/06 labels"·min-width 2곳은 그대로 · 10/06 결정 6·16-④ 의 답 = 이 회차(`per_day_px` 80 은 PC 용으로 유지).
- 다음 단계: ③ 구현 새 세션 **Opus 5.5 · ultracode** — 지시문은 탐색 세션이 이 블록 뒤에 만들어 준다. 이 블록만 추가 커밋(push 0).
- 지시문(탐색 세션이 작성, 2026-10-06): 저장소 밖 `D:\saero\saero-ad-report_01차트_구현지시_회차1_2026-10-06.md` — 프롬프트 B 구현 양식, 사실 기준 = 이 브랜치 HEAD(기록 커밋 2), 할 일 1~8(config · apply 템플릿·변환·사슬 · validate · mutation·test_apply · chart_check · 안내 스크립트 S · 문서 · 미리보기), 리허설 R1~R9, [넘길 때] 모델·effort. 보내기 전 검토자 2(결정·막음 완결성 / 코드·앵커 대조)로 대조해 반영 — 결과는 지시문 끝 "검토자 대조" 줄.
- 지시문 검토자 대조 결과(2026-10-06): 렌즈 1 결정·막음 완결성 13건(막음 1 · 빠짐 6 · 문구 6) · 렌즈 2 코드·앵커 10건(틀림 2 · 빠짐 1 · 문구 7) — 전부 반영. 큰 것: 분기 도우미 정의 순서(01·06 블록은 제자리 PC 생성 + 큐, 도우미가 차트 스크립트 끝에서 큐를 비움 — 즉시 호출이면 TypeError 로 뒤 차트 5개가 비는 막음) · convert_b_to_c ⑤ 앵커 `
});
</script>
` · fixture 안내 발췌 2줄 보강 · `window.__saeroSync` 노출 · 막음 기준은 5절 원문 그대로 · 첫 적용 본보기에 결정 11 ①~④ 질문 · test_deploy 는 `-k layout_gate` · chart_check 외부 요청 차단 0 판정.
- **결정 11 답(2026-10-06 23:47 무렵, 판 C 첫 적용 보류 회차 — 사용자 채팅 원문)**: ① "주로 모바일" ② "아니"(인쇄·PDF 안 씀 → 이월 3 Letter·여백 0.6in 한계는 막음 아님, `print_max_height_px` 1000 그대로) ③ "좋았어"(10/06 회차 2 시크릿 창 03·07·08 접기) ④ "괜찮은거같아"(01 세로 흐름 모양).

---

## 갱신 회차 (2026-10-06 16:58~17:05 KST — Code 탭 `/saero-run`, main 작업 폴더, **리포트 읽기 쉽게 회차 2(모양) 첫 적용 · 경로 C**) · **배포 완료 `014472d`**
합본 `일별` 2026.08.26 — 10.05 (41일) · 배포 커밋 `014472db`(직전 `037aca8`, 파일 sha 624b770 → 74a46bf) · 집계 기간 `2026.08.26 — 10.05 (41일)`
사용자 첫 말 "회차 2(모양) 첫 적용 — 경로 C — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함"(위 "첫 적용 본보기" 그대로). S0 전 `git pull --ff-only origin main`(사용자 승인 — e265a17 → **14c2374**, 작업 트리 깨끗) → S0 PASS → 수집·ingest 생략(오전 합본 그대로) → 4 fetch(배포본 `037aca8` = **002233ee**, meta 없음·서술 표지 36) → `cp` → 5a compute(**2446b7c0**) → 2-1 같음(41일) → 사용자 답(첫 말 안) "다시 계산" → 3 신규 0(노원키즈필라테스 최근 3일 [0,0,0]은 09-17 규칙대로 `excluded_groups` 밖) → 5-0a pull(3그룹 각 294개 · registry 884행 바이트 불변 665ad61f)·propose `--since 2026-10-06`(`[주의] 빈 창`, 후보 0) → ⓐ 해당 0(질문 없음) → **5 = `apply.py --layout` 1회**(`레이아웃 판 변환(meta 없음 → r2026-10-B, details 5)` · 91,064 → 93,339자, 서술 스크립트 없음) → 작업본 **46e15c8a = 검증 리허설 R1 과 바이트 동일** → 6 precheck → **보류**(작업본 + 전후 비교 페이지 사용자 확인) → 사용자 "배포" → 7 dry-run(`[주의] 레이아웃 판이 바뀜`) → `push … --layout-change` 1회 → `verify --ref 014472db…` 1회째 일치(재수령 sha 74a46bf · md5 46e15c8a).
validate.py 검사 24개 전부 PASS · compare.py 차이 0(항목 99, 직전 배포본 인자 002233ee) · overflow 360/390/430 넘침 0(details 5개 연 상태) · narrative `[주의] 같은 기간 — 대조 생략(표지 36개 중 매회차 24개)` · 도장 full · 재수령본 md5 일치
`--pending` 사용: 아니오 — 채팅 질문 0건(2-1 답은 사용자 첫 말에 있음)
**효율: 벽시계 약 7분 · 도구 호출 약 40회 · 즉석 코드 약 27행**(3단계 그룹 판정 12 · compute 키 확인 4 · 비교 페이지 값 뽑기 7 · 서술 표지 전후 대조 4 — 비교 페이지 생성은 기능 clone `mk_compare.py`(md5 622cb68a, 읽어 쓰기만))
2-1단계 같음(경로 C) / 제외 그룹 신규 후보 0 / 서술 그대로(표지 36개 옛 판과 바이트 같음 — 손 수정 0, summary 는 apply 값 그대로) / 11·12번 판정·이월 변경 없음(같은 데이터) / 경쟁사 신규 변형 후보 [] / 사용자에게 요청한 값 없음
제외 검색어(5-0단계): 후보 0 → 승인 0 → 등록 0 · verified 0 · 실패 0 / registry 884행
propose 창 2026-10-06~2026-10-05(빈 창) · 등록 미룸(사용자): 아니오
- **전후 비교**(`work/compare_1006d.html`, gitignore — 온라인 캡처·차트 그려짐, 구역 03·07·08): 높이 px(옛 → 새 닫힘/열림) — 03: 1280 1,659 → 459/1,760 · 390 1,334 → 440/1,458 · 07: 1280 3,903 → 1,557/3,925 · 390 4,106 → 1,697/4,128 · 08: 1280 791 → 625/791 · 390 1,051 → 671/1,051. 보이는 글자(표 제외, 옛 → 새 닫힘): 03 91 → 113(1280)·107 → 129(390, 합계 줄 위로) · 07 2,736 → 975 · 08 1,248 → 576. HTML 글자(접기 안 포함): 07 2,718 → 2,751 · 08 1,247 → 1,253(누락 0). 문서 전체 390 폭: 13,836 → 닫힘 10,153 / 열림 13,982px · 1280 폭: 11,626 → 7,914 / 11,749px. 03 표 tbody 옛 [42] → 새 [8, 34](summary "이전 34일(8/26~9/28) 펼치기").
- **다음 회차**: 직전 배포본이 레이아웃 판(meta r2026-10-B)이라 `apply --layout` 은 변환을 건너뛰고(값·summary 만) 레이아웃 판 게이트는 조용히 통과한다(자동 배포 그대로) — `--layout-change` 는 쓰지 않는다. 서술은 표지 기반(ⓑ). propose `--since 2026-10-06` · `--prev ~/saero-fetch/downloads/2026-10-06`.
- **마감**: 기록 커밋 `eac6c80`(재clone 대조 일치). 라이브 시크릿 창 확인(03·07·08 접기·차트)은 요청했으나 마감까지 답 없음 — 다음 세션 첫머리에 사용자에게 확인. 운영 작업 폴더 HEAD = origin/main · 기능 clone `D:\saero\feat-20261006-layout` 쓰기 0 · `D:\saero-verify` 열기 0 · 네이버 쓰기 0.

---

## 검증·병합 기록(2026-10-06 — 리포트 읽기 쉽게 회차 2 모양: 검증 1(막음 0) → main 병합)

**병합**: `feat-20261006-layout`(`6bfd77c` — e265a17 위 6커밋: ea2c8ef apply·config·test_apply·fixture · 32f7be5 validate·mutation·overflow · eae81ef compare·test_compare_sections · 9ca1862 deploy·test_deploy · 70a096b 문서 · 6bfd77c 구현 기준선)을 main(`e265a17` — 분기 뒤 main 변경 0, 16:47 KST `ls-remote` 확인 · 갱신 회차 돌지 않는 시각 · 운영 작업 폴더 HEAD e265a17 깨끗)에 `git merge --no-ff` → 병합 커밋 **`ef39d2a`**(부모 e265a17 · 6bfd77c, 트리 = 6bfd77c 와 동일 — `git diff --stat 6bfd77c HEAD` 0). 충돌 0(audit/last-audit.md 포함 — main 이 움직이지 않아 자동 병합). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`(전역 설정 변경 0). clone `D:\saero-verify\merge-20261006-layout`(`git clone -c core.autocrlf=false`). 사용자 병합 지시(2026-10-06 16:45 무렵, 검증 세션 채팅 원문 "지금 병합") 뒤 병합 — 조건 "그날 데이터 회차 뒤 + 첫 적용 바로"(오늘 데이터 회차 09:24·15:02 끝, 첫 적용은 이 뒤 바로 운영 세션 몫). 브랜치 `feat-20261006-layout` 은 지우지 않고 둔다. 코드·문서·config·data 재수정 없음(이 절 추가만). 아래 회차 2 구현 기준선 "마무리 기록"의 `브랜치 push 1회(… main 아님)` 는 당시 사실 — 원문 보존, 이 절로 정정(**2026-10-06 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고에).

**검증 1**(`D:\saero-verify\saero-ad-report_검증_리포트읽기쉽게_회차2_2026-10-06.md`, 별도 세션 — Code 탭·이 PC, Fable 5.1 · ultracode, clone `D:\saero-verify\feat-20261006-layout-1`, 대상 6bfd77c, 워크플로 에이전트 5 = 검토자 4(apply 코드 · 배포 흐름 반박 · 검사 가드 반박 · 화면·문서·사용자 결정) + 기계 확인 1): 아래 구현 기준선 "검증 회차가 볼 것" 1~13 전부 참 · 리허설 R1·R2l·R3·R4·R5 재실행 md5 전부 기록과 일치(R1 index 46e15c8a · compute 2446b7c0 · R2l new40 ad760ced · index 744cfb4b · compute f24ecb6f · PNG b62d5382·7e80810e · R4 `[OK]` 14 · mutation `[OK]` 50) · 사본 변조 실험(접힌 안 누락 13종 · 판 고르기 · 게이트 시나리오 13건 · recent_days×일수 36조합) 전부 validate/compare FAIL·apply FAIL(파일 불변)·게이트 rc 1·요청 0 으로 요란하게 멈춤 · **막음 0** → "다음 단계로 가도 된다". 이월 14건은 보고 전문에(아래 이월에 일부만).

**병합 main에서 전체 세트 재실행** [실측] — 이 PC(venv `D:\saero\.venv` Python 3.12.10), `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1`, `-W error::ResourceWarning`, test_deploy 는 GIT_* unset·`GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`·`GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`(실제 자격 증명 0). 재료는 검증 clone `work/` 에서 읽기만으로 사본(병합 clone `work/R1/` = R1 index 46e15c8a·compute.json 2446b7c0 · `work/mt/` = R2l index 744cfb4b·compute.json f24ecb6f + combined 4 검색어 e3a352a2·상세지역 e70e5023·시간대별 faac5a0a·키워드 b7d91858):
- 전체 시험 4: `tests/test_exclusions.py` **Ran 49 OK** rc 0(1.0초, registry md5 665ad61f 전후 동일) · `tests/test_deploy.py` **Ran 21 OK** rc 0(34초 — 17 + 레이아웃 게이트 4) · `tests/test_ingest.py` **Ran 10 OK** rc 0(61초, data/ md5 12파일 동일) · `tests/test_fetch_reports.py` **Ran 15 OK** rc 0(79초, "OK" 줄로 판정, data/2026-09·config md5 동일). skipped 0.
- 회차 시험 4: `tests/test_apply.py` **Ran 14 OK**(9.7초 — ApplyRehearsal `work/R1/` 레이아웃 판 meta assert 포함, skip 없음) · `tests/test_narrative_check.py` **Ran 7 OK** · `tests/test_validate_07.py` **Ran 6 OK** · `tests/test_compare_sections.py work/mt/index.html work/mt/compute.json` **5/5** rc 0(기준 exit 0 · OK 99 · DIFF 0 · 원본 md5 그대로 · "전부 맞음" — 03 오름차순 복귀 → DIFF 2 · 07 summary +1 → DIFF 1). md5 도우미 ResourceWarning 4줄은 회차 1 검증·병합 기록 이월 그대로(rc·판정 영향 0).
- `tests/mutation_test.py work/mt/index.html <combined 4>` rc 0 **"전부 살아 있음"** — 기준 24/24 · 커버리지 24/24 · `[OK]` 50(변조 25 + 0건 가드 18 + archive 7) · config 실험 3(ctr · date_sections · layout_id → 기준 사본 "레이아웃 판" FAIL 1) · MISS/UNCOVERED/SKIP 0 · 원본 md5(html·CSV 4·data/ 12개) 전부 동일. 배포 저장소 현재 배포본(037aca8 = 회차 1 판, meta 없음)으로는 돌리지 않음(24번째 "레이아웃 판" FAIL 이 정상). deploy.py 는 test_deploy 안에서만.
- `py_compile` scripts 10 · tests 10 = **20/20**(cfile 스크래치) · `bash -n` ingest.sh·precheck.sh 통과 · config `json.load` 통과.
- md5: `cat data/*/*.csv audit/exclusions.csv | md5sum` 병합 전 main = 병합 뒤 = 전체 세트 뒤 **`aa89297c`** · config/report-config.json **`07562fde`**(158행 — e265a17 cd6afefa 와 차이는 `report_layout` 8줄 추가뿐) · local/·data/·registry 변경 0(`git diff --stat e265a17 HEAD -- local/ data/ audit/exclusions.csv` 빈 출력) · 작업 트리 변경 0(무시 파일 `work/` 뿐). 배포 PUT 0 · 네이버 0 · fetch_reports 실제 실행 0(시험 fixture 만) · 실제 자격 증명 0 · 운영 작업 폴더·작업 clone 열기 0(읽기만).

**이월**(한 줄씩 — 나머지는 보고 전문 4절 14건):
- (검증 이월 4) 전후 비교 페이지 생성기 `mk_compare.py`(622cb68a)가 저장소 밖 작업 clone `D:\saero\feat-20261006-layout\work\R1\` 에만 — 문서는 "보이고"라고만. 저장소화(tests/ 또는 scripts/) 또는 code-tab 한 줄 후보.
- (검증 이월 3) 같은 판인데 `--layout-change` 가 붙으면 문구 0(임의 결정 10) — `[주의] --layout-change 가 있지만 판이 같음` 한 줄 후보.
- (검증 이월 6) 데이터 회차에서 dry-run 이 `[주의] 레이아웃 판이 바뀜` rc 0 으로 지나가 실제 push 1회가 게이트에서 헛돎(요청 0·무해) — 세션이 dry-run [주의] 를 보면 push 전에 멈추라는 문구 후보.
- (검증 이월 8) compare 07 summary 클릭1·클릭0 regex 가 `<summary` 를 요구하지 않음 — 두 접기만 div 로 풀린 판은 compare 통과(validate details 3 ≠ 5 가 잡음).
- (검증 이월 11·12, 문서) css-and-layout "접기 안내" 2 JS 한 줄 표기(arrow ↔ function) · SKILL.md 원칙 1문장의 deploy 설명(게이트는 config 를 안 읽고 --file·--base 동일성만).
- (검증 이월 14, 기록) `work/materials.md5` 는 work/ 안에서 `md5sum -c` · `R4/apply_e265a17.py` 는 clone 절대 경로가 박혀 md5 가 clone 마다 다름.

**병합 뒤**(이 병합 세션은 하지 않았다): ① main 작업 폴더 `D:\saero\saero-ad-report-skill` `git pull --ff-only`(운영 세션 몫, 첫 적용 전 — ingest 시작 검사 "HEAD = origin/main" 이 막는다) ② local/ 변경 0 → 설치본(`D:\saero\CLAUDE.md` · `D:\saero\.claude\skills\saero-run\SKILL.md`) 갱신 불필요 ③ **첫 적용 = 회차 2(모양) 첫 적용을 바로**(오늘, 데이터 회차 뒤 — 병합 뒤 첫 적용 전에 데이터 회차가 먼저 돌면 5단계 `apply --layout` 이 모양을 바꾸고 게이트가 PUT 0 으로 멈추고 묻는다, 경로 A 는 쓰지 않는다) — 운영 세션 `/saero-run` Opus 5.5 · high · ultracode 끔, 첫 말 "회차 2(모양) 첫 적용 — 경로 C — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함", 본보기 = 아래 회차 2 구현 기준선 "첫 적용 본보기" 절(4 fetch(직전 배포본 037aca8 = 회차 1 판, meta 없음) → 5 `"$PY" scripts/apply.py --layout --html work/index.html --compute work/compute.json` → 6 precheck 기대 validate 24/24 · compare OK 99/DIFF 0 · 3폭(details 열고) · narrative `[주의] 같은 기간` · 도장 → **보류 멈춤**: 작업본 + 전후 비교 `"$PY" /d/saero/feat-20261006-layout/work/R1/mk_compare.py --old work/prev.html --new work/index.html --out work/compare_<날짜>.html --online` → 사용자 "배포" → 7 dry-run `[주의] 레이아웃 판이 바뀜` → `push … --layout-change` → `verify --ref` → 8 기록) ④ 그 다음 회차부터 직전 배포본이 레이아웃 판 — `apply --layout` 은 변환 건너뛰고 값·summary 만, 게이트 조용히 통과(자동 배포 그대로).
효율: 벽시계 약 12분(16:47 ls-remote → 16:48 clone·병합 → 전체 세트 16:49~16:53 → 기록·push) · 도구 호출 약 10회 · 하위 에이전트 0 · 즉석 코드 약 20행(시험 러너·py_compile 조각 — 스크래치).

---

# 기능 추가 구현 기준선(리포트 읽기 쉽게 — 회차 2 모양, 2026-10-06)
점검일: 2026-10-06 (기능 추가 회차 — **구현, 회차 2 = 모양**. 데스크톱 앱 Code 탭, 이 PC, 작업 폴더 `D:\saero`로 연 세션, Opus 5.5 · ultracode). 작업 clone `D:\saero\feat-20261006-layout` 브랜치 `feat-20261006-layout`(`git clone -c core.autocrlf=false` → `git switch -c`). 시작 확인 [실측]: origin/main = **`e265a17`**(지시문의 마감 값 그대로 — 그 뒤 갱신 회차 기록 커밋 없음, `ls-remote`) · 재료 md5 14개 = 지시(회차 1 clone `work/` 에서 **읽기만으로 사본**: `R1/index.html` 002233ee → `work/index.html` · `R1/prev.html` 6aaa2472 → `work/prev_f7bc605.html` · combined 4 e3a352a2·e70e5023·faac5a0a·b7d91858 · c40 CSV 4 d6830103·a8c5eb81·1db13563·a4f54006 + `c40/compute.json` 81f475fb · `R2/new40.html` 3da35369 · `narr_lib.py` 18dd9c39 · `R2/n1006b.py` a64eef31 — 목록 `work/materials.md5`) · 참고 사본 `work/D/`·`r12`·`r12b`. 운영 main 작업 폴더 열기 0 · data/·registry·local/ 변경 0 · 외부 쓰기 0(네이버·API·배포 저장소 요청 0, 키 파일·자격 증명 열지 않음, fetch_reports·exclusions·deploy(dry-run 포함)·ingest·archive 실행 0 — deploy 는 test_deploy 하네스 안에서만).
설계: 탐색 기준선 3.1 설계안 비교 표 **B 접기형 열** + 사용자 결정(2026-10-06 — ② 고르기) 1·4·5·6·9·12·13·14 의 **회차 2 몫** — `scripts/apply.py --layout`(레이아웃 판 변환 + 03 두 표 + summary 기계 자리, 막음 M2) · validate "레이아웃 판" · compare 03 역순 + summary 4항목 · deploy.py 레이아웃 게이트(막음 M4) · overflow details 열기 · mutation 변조·가드·config 실험 · config `report_layout` · 문서(회차 2 절만) · 미리보기(PNG + 전후 비교 페이지). **글(서술 표지 블록 바이트)·C 안·차트 폭(`per_day_px` 80 그대로)·validate 길이 상한·01 표·순위 5칸 순서·회차 1 이월 1~10·local/ 은 건드리지 않았다.**
검증용 clone: `git clone -c core.autocrlf=false -b feat-20261006-layout --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill D:\saero-verify\feat-20261006-layout-1`
효율: 벽시계 약 55분(15:33 무렵 시작 확인 → 15:50 코드 → 15:55 리허설 R1~R5 → 16:02~16:12 자기 검토 → 커밋·기록·push) · 도구 호출 조정자 약 100회 + 자기 검토 워크플로 에이전트 4개(검토 3 + 기계 확인 1, 151회) · 즉석 코드 약 900행(패치 스크립트 스크래치 ≈ 440 · clone `work/` 스크래치 `R1/mk_compare.py` 189 · `R4/r4.py` 145 · `R5/measure.py` 82 · `R5/chars.py` 18 · `rehearse_R2.sh` 25).
표기: [실측] 이번에 파일·명령으로 확인 / [추론] 확인 못 함. 행 번호는 이 브랜치 커밋 기준.

## 바뀐 것(파일별, `wc -l` 전 → 후 · md5 앞 8자리) [실측]

| 파일 | 행 | md5 | 무엇 |
|---|---|---|---|
| `scripts/apply.py` | 249 → 375 | 871d6e87 | `--layout` · 판 고르기(meta = config → 값만 · meta 없음 → `--layout` 일 때 `convert_layout`, 아니면 `[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout …` · meta 다름·meta 없는데 details 있음·details 수 ≠ 5 → FAIL) · `convert_layout`(meta · CSS 3줄 · toggle/beforeprint/afterprint 스크립트 · 03 접힌 표 뼈대 · 07 목록 2·경쟁사표·08 목록을 details/summary 로, 서술 표지·각주는 밖) · 03 위 표 = 합계 + 최근 `recent_days` 최신 위, 접힌 표 = 03 첫 `<summary` 뒤 첫 tbody(구역 밖이면 FAIL — `tbody(start, stop)`) · summary 교체 03·07 셋(08 은 기존 `(N개 지역·클릭 M건)` once) · `bounds`·`once_in` |
| `scripts/validate.py` | 455 → 478 | 9a2d241f | 검사 **"레이아웃 판(meta report-layout = config · 접기 details 수·짝)"**(`check_layout` — meta 정확히 하나 = `report_layout.layout_id` · `<details` 수 = `markers.details` · summary 수 = details 수 · details 바로 안 summary, 0건 FAIL) → **23 → 24개**(출력 맨 끝) |
| `scripts/compare.py` | 207 → 219 | 9e7fd01a | "03 일별 표 전체 행" 두 표 이어 읽어 `[::-1]` · summary 4항목 신설(07 클릭1건·클릭0·경쟁사표 개수 = compute 목록 길이 · 03 "이전 N일·기간" = 접힌 표 자기 일치, 각 구역 함수 끝) → **항목 수 N = 99** |
| `scripts/deploy.py` | 338 → 364 | 2deda144 | `layout_of`(bytes 의 meta) · push `--layout-change` · 게이트(도장 검사 다음 · `get()` 앞): 다르면 `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함(…)` exit 1 / dry-run `[주의] 레이아웃 판이 바뀜 — 실제 push 에는 --layout-change(…)` / 같으면 문구 0 |
| `tests/overflow_check.py` | 59 → 62 | d6b83692 | goto·400ms 뒤 details 전부 `open=true` → 100ms → scrollWidth(출력에 "details N개 연 상태") |
| `tests/mutation_test.py` | 386 → 405 | f5984482 | 변조 2(meta 값 · 03 접기 하나 풀기) + 0건 가드 2(meta 제거 · 접기 전부 풀기 = summary → 머리글 div 로 옛 모양 복원 흉내) + config 실험(`report_layout.layout_id` → 기준 사본 "레이아웃 판" FAIL) |
| `tests/test_apply.py` | 212 → 343 | de0d1e9f | 판 고르기(옛 판 + --layout 없음 FAIL · meta 다름 · details 4 · meta 없는데 details) · 변환 뼈대(meta 1·details 5·짝·`line-height:1.9;">` 3·앵커 뒤 첫 일치 = 목록·CSS·스크립트·각주 밖) · 서술 표지 4개 안쪽 바이트 불변·접기 밖 · **03 행 분배(10일 = 위 7 + 접힌 3, 합계 맨 위)** · summary 5개 옛 값 → 다시 씀 · 짧은 기간(5일 → 빈 접힌 표 + "이전 0일") · CLI 두 번 바이트 같음 · 접기 CSS/스크립트 자리 없음·03 표 둘 FAIL · 접힌 경쟁사표 compute 그대로 · ApplyRehearsal(A.apply 직접 + meta assert) |
| `tests/fixtures/layout_old.html` · `layout_old.compute.json` | 460 → 475 · 594 → 636 | f89b159d · f7d60129 | html: `<style>`·가로 안내 스크립트(resize 줄)·08 note 발췌 · json: `03.rows` 10일(12/29~12/31 앞에 붙임, 03 합계 재계산 — 다른 키는 7일 그대로, 이름·숫자 가짜) |
| `tests/test_compare_sections.py` | 115 → 142 | 754557d3 | 경우 2 추가: 03 날짜 행 오름차순 복귀 → "03 일별 표 전체 행" DIFF(그 구역만) · 07 summary 클릭 1건 +1 → "07 summary 클릭1건 개수" DIFF |
| `tests/test_deploy.py` | 399 → 453 | 5a60e3a6 | 게이트 4건(`run_deploy` 하네스): meta 다름(옛 판·값 다름) → FAIL·요청 0 · `--layout-change` → PUT 1(본문 = 작업본) · 같음 → 문구 0·PUT 1(기존 PREV·WORK 도) · dry-run → [주의]·PUT 0 |
| `config/report-config.json` | 150 → 158 | 07562fde | `report_layout{_comment, layout_id "r2026-10-B", recent_days 7, markers{details 5}}` |
| `SKILL.md` | 584 → 600 | 5cfa3ee2 | 원칙 1문장(레이아웃 판은 설계 회차·사용자 결정으로만) · 5단계 `apply.py --layout`(매 회차·summary 기계 자리) · 6단계 compare 99·overflow 접기 열고 · 7단계 게이트(`--layout-change` 는 첫 적용 "배포" 답 뒤만, 데이터 회차에서 나면 멈추고 묻기) · 배포 전 검산 24 · 참고 |
| `references/report-structure.md` | 525 → 561 | c04a00e8 | 2~4행 아래 **"레이아웃 판 r2026-10-B(사용자 결정 2026-10-06)"** 절(사용자 원문 두 문장 · 접기 5 표 · 기계 자리 규칙 · 누락 0 · 01 오름차순) · 03 "마지막 행은 전체 합계" 개정 → 합계 맨 위 + 최근 7일 + 접기 · 07 (2)(3)·경쟁사 · 08 접기 줄 |
| `references/css-and-layout.md` | 201 → 234 | 07bc85e3 | 유틸리티 `.fold`·`.fold-more` · 밀도표 한 줄 · **"접기 안내"** 절(CSS·toggle sync·beforeprint·기준점·검사) · 버그 기록 **11**(접기 안은 검사·인쇄·찾기에서 빠지기 쉽다) |
| `references/code-tab.md` | 240 → 243 | 7e1e2045 | 3절 5행(`--layout`)·7행(게이트) · 4절 첫 적용 문단(레이아웃 판 첫 적용 = 전후 비교 페이지 + "배포" 답 뒤 `--layout-change`) · ⓑ 표 `[FAIL] 레이아웃 판이 바뀜` 행 · 5절 deploy exit 1 줄 |
| `audit/checklist.md` | 511 → 519 | 2fd9cc06 | 갱신 이력 한 줄 · 16 "23개" → 24 · compare 99 · mutation [OK] 50 · [의도된 동작] 27 회차 2 몫 · [되돌리면 안 되는 것] 2행(레이아웃 판 · 03 순서). 대상 파일 목록은 새 파일 없음(그대로) |
| `audit/last-audit.md` | — | (커밋 뒤) | 이 절 |

지시 밖 변경 0: `scripts/compute.py`·`narrative_check.py`·`precheck.sh`·`reportlib.py`·`exclusions.py`·`fetch_reports.py`·`archive.py`·`ingest.sh`·`references/exclusion-ui.md`·`report-fetch.md`·`local/`(saero-run · CLAUDE.md · prompt-polish — apply·deploy 명령 문자열 없음, code-tab 정본을 따름)·`data/`·`audit/exclusions.csv` 불변.

## 임의 결정(번호 = 사용자가 바꿀 단위)
1. **meta 없음 + `--layout` 없음 → `[FAIL] apply`**(옛 배치 유지 안 함) — 03 경로를 B 하나로 두고, 운영 세션이 `--layout` 을 빠뜨리면 apply 에서 바로 요란하게 멈추게. `tests/test_apply.py` 옛 107~108행 기대값(오름차순·합계 맨 아래)은 B 배치(합계 맨 위 + 최신 위 + 접힌 표)로 바꿈, `ApplyRehearsal` 은 `A.apply()` 직접(meta 로 판 선택 — `--layout` 불필요) + meta assert.
2. **meta 가 다른 값이면 변환하지 않고 FAIL** — 지시 "meta 가 없거나 다를 때 변환" 중 "다를 때"는 다른 판에서 B 로 바꾸는 변환이 없어(판 변경은 설계 회차 몫) FAIL 로. 같은 이유로 meta 없는데 `<details>` 있음 → FAIL, meta 같은데 details 수 ≠ 5 → FAIL.
3. **일수 ≤ `recent_days` → details 그대로 + 빈 tbody + "이전 0일 펼치기"**(validate details 5 와 맞게 — FAIL 로 두면 새 기간 첫 주에 배포가 막힘). 지금은 41일이라 안 남.
4. **compare summary 항목**: 07 셋 = compute 목록 길이 · 03 = 접힌 표 자기 일치(행 수·첫/끝 날짜 — compare 는 config 를 읽지 않아 `recent_days` 를 모름) · **08 은 신설하지 않음**(기존 "08 컴팩트 개수·클릭"의 구역 첫 일치가 summary 의 `(N개 지역·클릭 M건)` — apply 는 문서 전체에서 정확히 하나를 요구). N = 95 + 4 = **99**. summary 4항목은 각 구역 함수 끝(형식이 깨져도 그 구역 데이터 항목은 먼저 대조).
5. config `report_layout` 에 **`notes07` 넣지 않음**(3.1 B config 줄의 notes07 은 회차 1 서술 표지·validate "07 각주 세 자리"로 대체).
6. css-and-layout.md **버그 기록 번호 11**(기준선 3.1 의 "12" 는 A 안 버그 11 `.vbox` 를 앞에 둔 번호).
7. **summary 마크업·CSS**: 07 목록 summary = 옛 머리글 div 의 인라인 style 그대로(모양 유지) · 클릭 0 summary `(노출 5회 이상 N개 · 펼치기)`(옛 "(노출 5회 이상만)" 조건을 남김) · 08 = `class="sub-head"` 그대로 · 03·경쟁사 = 새 클래스 `.fold-more`(12px 굵게 진한민트) · CSS 3줄(`.fold > summary` cursor · `.fold-more` · `.fold[open] > .fold-more` 아래 8px) · 03 접기 `margin-top:10px` 인라인. 새 색 0, `.ctr-high` 미사용.
8. **변환 자리**: meta = `<meta charset="UTF-8">` 바로 뒤 · CSS = `</style>` 앞 · 스크립트 = 가로 안내 IIFE 의 `resize` 줄 뒤(같은 스코프의 `sync` 를 부르려고). **CSS·JS 주석에 태그 꺾쇠 금지** — 첫 시운전에서 CSS 주석의 `<details class="fold">` 가 details 6 으로 세어져 apply 자기 검사가 FAIL 로 잡음(validate 태그 짝도 셀 자리) [실측].
9. validate "레이아웃 판" 은 출력 **맨 끝(24번째)** — 문서는 이름으로 부름. "짝" = summary 수 = details 수 + details 바로 안 summary(TAGS 열고 닫기 수는 검사 1 몫). validate docstring 목록은 기존 꼴대로 "23." 번호.
10. **deploy 게이트 세부**: `--base` 없는 dry-run 은 게이트 생략(대조 불가 — 기존 `[dry-run] --base 없음` 줄, 실제 push 는 `--base` 필수라 열리는 PUT 경로 없음) · `--layout-change` 인데 같음 → 문구 0 · 다름 + `--layout-change` → 한 줄 알림 뒤 진행. 출력은 지시 리터럴로 시작(`[FAIL] 레이아웃 판이 바뀜 — PUT 안 함(…)` · `[주의] 레이아웃 판이 바뀜 — 실제 push 에는 --layout-change(…)`).
11. **mutation 0건 가드 2개**(지시 "0건 가드" 보다 하나 많음) — "접기 전부 풀기"는 summary 를 머리글 div 로 돌려 옛 모양 복원을 흉내(다른 검사는 그대로 PASS, "레이아웃 판"만 FAIL) → `[OK]` 50(변조 25 + 0건 가드 18 + archive 7) · config 실험 3.
12. `tests/test_compare_sections.py` 에 2경우 추가(지시 밖 — 양방향 시험을 저장소 시험으로 고정).
13. fixture 확장 방식: `03.rows` 만 10일(앞에 3일 붙이고 03 합계 재계산 — apply 는 키 사이를 대조하지 않음), html 은 접기 앵커 발췌(style·스크립트·08 note). 이름·숫자 전부 가짜.
14. 리허설 폴더 `work/R1`·`R2l`·`R4`·`R5`(R3 mutation 로그 = `R2l/mutation.log`) · 전후 비교 생성 스크립트 `work/R1/mk_compare.py`(`--online` 이면 밖 요청 허용 + networkidle — 첫 적용용).
15. 문서·docstring 의 출력 문구는 실제 출력과 글자 그대로(자기 검토 뒤 같이 — apply `[FAIL] apply: ApplyError: …`, deploy [주의] 줄 print 순서).

## 리허설 결과(전부 clone 안 사본, 최종 코드 — `work/rehearse_R2.sh` 재실행 md5 같음) [실측]
- **R1 첫 적용(경로 C 모양)**: compute(prev = 회차 1 판 002233ee) 40행·후보 [] **2446b7c0**(= 회차 1 R1 바이트 동일) → `apply --layout` 변환(91,064 → 93,339자, details 5) **46e15c8a** → 두 번째 `(변환 건너뜀) (변경 없음)` 같은 md5 → 서술 표지 36개 안쪽 바이트 전부 같음(`narrative_check.blocks`) → precheck: **validate 24/24 · compare OK 99/DIFF 0 · overflow 360/390/430 넘침 0(details 5개 연 상태, 밖 요청 6건 차단) · narrative `[주의] 같은 기간`(표지 36 중 매회차 24) · 도장**(46e15c8a · 002233ee · full).
- **R2l 다음 회차**: c40.json 39행 = 81f475fb(c40/compute.json 바이트 동일) → new40 `apply --layout` 변환 **ad760ced**(summary `이전 33일(8/26~9/27)` · 33 · 노출 5회 이상 75 · 표 39행 · (39개 지역·클릭 104건)) → compute(prev = new40) **40행·후보 ['노원부티필라테스']** f24ecb6f(접힌 경쟁사표도 그대로 읽힘) → index `apply --layout`(변환 건너뜀) summary **`이전 34일(8/26~9/28)` · 35 · 77 · 표 40행 · (39개 지역·클릭 104건)** → `R2l/n1006b.py`(ⓑ, judged (7,6,1,0)) 표지 36 → precheck **validate 24/24 · compare 99/0 · 넘침 0 · narrative `[PASS]`(40일 → 41일) · 도장**(744cfb4b · ad760ced) → 자기 기준 compute **40행·후보 []** 2446b7c0. **R1 ↔ R2l 바이트 차이는 11번 판정 한 줄뿐**(회차 1 R1↔R2 와 같은 차이 — 첫 적용 경로와 표지 기반 경로가 summary 까지 같은 리포트).
- **R3** `mutation_test.py work/R2l/index.html` + CSV 4 → exit 0 **"전부 살아 있음"** · 기준 24/24 · `[OK]` 50 · config 실험 3(ctr 4→5 · date_sections [1,6]→[1] · layout_id → 기준 사본 "레이아웃 판" FAIL 1) · 커버리지 24/24 · UNCOVERED·MISS·SKIP 0 · 원본 md5 동일.
- **R4 역검증**(`work/R4/r4.py` → `r4.log`, 13건 + 원본 md5 = `[OK]` 14): (1) 새 validate × 회차 1 판 → "레이아웃 판" FAIL(23/24) (2) × f7bc605 판 → "레이아웃 판"·"07 각주 세 자리" FAIL(22/24) (3) 07 클릭 1건 접기 하나 → div → `details 4개 ≠ config 5` (4) meta r2026-10-A → FAIL (5) 03 날짜 행 오름차순 복귀 → compare DIFF 2(03 행 · 03 summary) (5b) 회차 1 판 × 새 compare → DIFF 3 (6) 07 summary 35→36 → DIFF 1 (6b) 08 summary 39→40개 지역 → "08 컴팩트 개수·클릭" DIFF (6c) 경쟁사 40→39·클릭0 77→76 → DIFF 2 (7a) 03 summary 옛 값(이전 33일(8/26~9/27)) → DIFF (7b) `apply --layout` 재실행(변환 건너뜀)이 고쳐 써 744cfb4b 로 복원 (8) R2l 07-notes 를 new40 것으로 → narrative `[FAIL] 서술 미교체 07-notes` (9) 옛 apply(e265a17 판) × 새 판 → apply exit 0 이지만 compare "03 일별 표 전체 행" DIFF(validate 24/24 — compare 가 잡는 자리). + test_deploy 게이트 4 OK · test_apply 14 OK(03 행 분배 10일 = 위 7 + 접힌 3 · ApplyRehearsal 포함).
- **R5 화면**(관찰값 — `work/R5/measure.py` → `measure.json`, `chars.py` → `chars.json`, file:// 만·밖 요청 8건 차단·Chart.js 미로드): **390×844** 회차 1 판 13,836px(16.4장) → 회차 2 판 **닫힘 10,153px = 12.03장** / 열림 13,982px(16.57장) · **1280×900** 11,626(12.9장) → **닫힘 7,914 = 8.79장** / 열림 11,749(13.05장). 구역(390 옛 → 닫힘/열림): 03 1,334 → 440/1,458 · 07 4,106 → 1,697/4,128 · 08 1,051 → 671/1,051(1280: 1,659 → 459/1,760 · 3,903 → 1,557/3,925 · 791 → 625/791). 글자 수(표 제외, 회차 1 방식) 8,215 → 8,276(07 2,721 → 2,754 — summary 문구만큼, 접힌 안 포함) · 닫힌 화면에 보이는 글자(compare.html) 07 2,752 → 975(390). **뱃지**: headless chromium 은 닫힌 details 안 `.wide-table` 에도 load 때 뱃지가 이미 붙음(390 전체 9 · details 안 [1,0,0,1,0]) → toggle 뒤 같음 — toggle sync 효과는 headless 로 못 봄 [추론 — 이월 D5]. **인쇄**: `page.pdf()`(headless chromium 인쇄 경로)에서 beforeprint 순간 열린 details **5** · afterprint 뒤 **0** [실측, 390·1280 둘 다]. **미리보기**: `work/R1/preview_390x844.png`(b62d5382) · `preview_1280x900.png`(7e80810e)(닫힘·전체 페이지·차트 빈 칸) · **전후 비교 `work/R1/compare.html`**(9d962977, 03·07·08 × 1280·390, 옛 판 ↔ 새 판(닫힘) 이미지 base64 + 높이 닫힘·열림 + 글자 수 — 문구는 두 HTML 원문에서 뽑은 제목·summary·tbody 행 수만) ← **`work/R1/mk_compare.py`(622cb68a)**.
- **R6 끝 상태**: 아래 마무리 기록.
- **시험**(`-W error::ResourceWarning`): test_apply **14 OK** · test_narrative_check **7 OK** · test_validate_07 **6 OK** · test_deploy `-k layout_gate` **4 OK** · test_compare_sections × R2l **5경우 전부 맞음**. test_exclusions·test_fetch_reports·test_ingest·test_deploy 전체는 지시대로 돌리지 않음(병합 전 전체 시험).

## 기준선 리허설과 다르게 한 곳
- R1 의 `deploy.py push --dry-run` 게이트 확인 → **실행하지 않고 test_deploy 하네스 4건으로 대체**(지시 제약 — deploy 실행 0, dry-run 포함). 자기 검토(흐름 반박)가 R1 실제 도장으로 하네스 자동 흐름을 따로 재현: dry-run rc 0·[주의]·PUT 0 → 실제 push rc 1·요청 0.
- R5 뱃지는 headless 한계로 [추론](위).
- 폴더 이름: 기준선 R2 → **R2l**(재료 폴더 `work/R2/` 와 구분), R3 은 폴더 없이 `R2l/mutation.log`.
- R4 에 지시 밖 4건: (5b) 회차 1 판 × 새 compare · (6b) 08 summary · (6c) 경쟁사·클릭0 summary · (9) 옛 apply(e265a17) × 새 판.

**자기 검토**(지시의 [검토 깊이 규칙] — 워크플로 에이전트 4: 코드·검사 / 화면·문서 / 배포 흐름 반박 + 기계 확인(haiku)): **막음 0** — 넷 다 "다음 단계로 가도 된다". 흐름 반박 근거 [실측]: 병합 뒤 첫 적용 전 데이터 회차 → precheck 는 도장까지 통과하지만 실제 push 가 게이트에서 rc 1·요청 0 · "보류" 없이 시작한 첫 적용도 게이트에서 멈춤 · 첫 적용 뒤 데이터 회차(B ↔ B)는 문구 0·PUT 1 · 첫 적용 PUT 결과 모름 → 플래그 없이 재실행은 게이트 rc 1, 붙이면 "앞 PUT이 이미 반영됨" exit 0. 같이(이번에 쓴 줄 안 글자): 문서·docstring 의 출력 문구 두 곳을 실제 출력과 같게(임의 결정 15 — 게이트 시험 4·test_apply 14 다시 OK). 나머지는 아래 이월.

## 검증 회차가 볼 것(완료 기준 표 회차 2 줄로 — 판정만, 쓰기 0)
준비: 새 clone(위 명령) + 작업 clone `D:\saero\feat-20261006-layout\work\` 에서 **읽기만으로 사본**: `index.html`(002233ee — 회차 1 판) · `prev_f7bc605.html`(6aaa2472) · `combined/` 4 · `c40/` CSV 4 + compute.json(81f475fb) · `R2/new40.html`(3da35369)·`R2/n1006b.py`(a64eef31) · `narr_lib.py`(18dd9c39) · 스크립트 `rehearse_R2.sh`·`R4/r4.py`·`R5/measure.py`·`R5/chars.py`·`R1/mk_compare.py`. 운영 폴더·작업 clone·회차 1 clone 은 읽기만.
1. **누락 0(접힌 안 포함)** — R1·R2l 에서 03 41일(위 7 + 접힌 34) · 07 정식표 24·클릭1 35·클릭0 77·경쟁사표 40 · 08 TOP10 밖 39 가 HTML 에 전부(compare 집합·직접 셈).
2. **숫자는 compute.json** — precheck R1·R2l(validate 24/24 · compare 99/0 · 3폭 · narrative · 도장).
3. **summary 기계 자리(M2)** — summary 5개 = compute 값, 변환을 건너뛴 회차에도 다시 씀(R4 7b · test_apply `test_summaries_rewritten_every_run`) · compare summary 4 + "08 컴팩트 개수·클릭".
4. **화면 원칙** — details 열고 overflow 3폭 · 새 `#색` 0 · `.ctr-high` 다른 용도 0 · 외부 css/js 추가 0 · 표 `display:block` 0 · 07 ①②③·08 note·서술 표지 접기 밖 · 경쟁사 머리글 리터럴 · 미리보기 PNG 2장·compare.html.
5. **`line-height:1.9;">` 기준점 셋** — R1·R2l 3곳, 앵커 뒤 첫 일치 = 목록 div(validate click1/click0 · compare · apply listblock).
6. **옛 모양으로 조용히 되돌아가지 않음** — validate "레이아웃 판"(R4 1~4) · compare 03 역순 양방향(R4 5·5b·9) · mutation 변조 2·가드 2·config 실험(R3) · apply 판 고르기(옛 판 + `--layout` 없음 FAIL).
7. **첫 적용에 사람이 본 뒤에만 PUT(M4)** — deploy 게이트 위치(도장 다음·`get()` 앞) · test_deploy 게이트 4 · SKILL.md 7단계·code-tab 4절·ⓑ 문구("데이터 회차에서 나면 PUT 0 으로 멈추고 묻는다" · 세션이 스스로 `--layout-change` 를 붙이지 않음).
8. **compare 생략 없음** — test_compare_sections 5경우(구역별 try · summary 는 구역 끝).
9. **회차 1 몫이 깨지지 않음** — 서술 표지 36개 안쪽 바이트 불변(R1) · narrative R2l `[PASS]` · 07-notes 미교체 FAIL(R4 8) · validate "07 각주 세 자리" 그대로.
10. **세로 길이·글자 수 관찰값** — 390×844 닫힘 12.03장(열림 16.57) · 1280×900 8.79장(열림 13.05) · 글자 수 8,276 · 07 2,754(관찰용, FAIL 아님).
11. **리허설 한 줄** — `rehearse_R2.sh` 다시 돌려 같은 md5(R1 46e15c8a · R2l new40 ad760ced · index 744cfb4b · c_self 2446b7c0) + R4 `r4.py` `[OK]` 14 + mutation `[OK]` 50.
12. **문서 = 코드** — SKILL.md·report-structure(원문 두 문장)·css-and-layout·code-tab·checklist 의 문구·개수(24·99·[OK] 50) ↔ 스크립트 출력 · local/·data/·registry 변경 0.
13. **검증 폴더** `D:\saero-verify\<clone>`.

## 이월(한 줄씩 — 막음 아님, 첫 실사용 뒤 또는 점검 회차)
1. compare 는 03 위 표/접힌 표 경계(정확히 `recent_days`)와 합계 맨 위를 보지 않는다 — 분배는 apply 결정 코드 + test_apply 만(손으로 행을 옮기고 summary 까지 맞추면 통과 · 숫자 틀림 없음 · 여러 우연).
2. apply 03 첫 tbody 교체에는 stop 검사가 없다 — 위 표가 손편집으로 사라진 판이면 두 쓰기가 접힌 tbody 에 겹침(compare DIFF·파싱 실패로 요란 · 정상 흐름 밖).
3. validate "레이아웃 판"은 details 를 문서 전체로 센다 — 08 접기를 풀고 다른 곳에 하나 더한 손편집 판은 통과(모양 차이만 · 정상 흐름 밖).
4. deploy 게이트는 첫 meta 문자열만 읽는다 — 옛 base 의 주석·스크립트 안에 meta 문자열이 있으면 "같음"(지금 배포본 0회, FOLD_CSS·JS·서술 표지에도 없음 · 여러 우연).
5. toggle → 가로 뱃지 sync 효과는 headless chromium 에서 재현 안 됨 — 실기기(iOS Safari·Android Chrome) 확인(탐색 이월 D5 그대로) · iOS 공유→PDF 에서 beforeprint 가 오는지 [추론].
6. `.fold-more`(진한민트 굵게)가 07 범례("진한 민트색 클릭률 = 4% 이상") 바로 아래 경쟁사 summary 에 쓰임 — `.ctr-high` 는 아니지만 첫 적용 미리보기 때 사용자가 볼 거리.
7. SKILL.md "누락 금지"·"매번 함께 바꿔야 할 텍스트" 9항목에 "접힌 안 포함"·summary 기계 자리 한 줄 후보(정본은 report-structure "레이아웃 판"·SKILL 5단계).
8. validate.py docstring 은 새 검사를 "23." 번호로 적음(출력은 24번째 — 문서 번호와 출력 순서 차이).
9. 390×844 닫힘 **12.03장** — 탐색 기준 "≤ 12장"(관찰용)을 0.03장 넘음. 더 줄이려면 07 정식표·08 TOP10 표 접기 등은 설계 회차 몫.
10. 회차 1 이월 1~11 · 검증 1 이월은 그대로(이번에 손대지 않음 — 11 높이는 위 9 로 관찰값 갱신).

## 마무리 기록(이번 회차)
- 커밋(경로 지정 add, `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`, 전역 설정 변경 0): `ea2c8ef` apply·config·test_apply·fixture · `32f7be5` validate·mutation·overflow · `eae81ef` compare·test_compare_sections · `9ca1862` deploy·test_deploy · `70a096b` 문서 · 그리고 이 절(기록 커밋 — 해시는 자기 참조라 적지 않는다).
- 끝 확인(커밋 뒤): `git fetch` → origin/main 확인 · 브랜치 push 1회(`git -c credential.interactive=false push origin feat-20261006-layout`, main 아님) · 스크래치 `git clone -c core.autocrlf=false -b feat-20261006-layout --single-branch` 로 HEAD·md5 대조 — 결과는 채팅 보고(자기 참조).
- work/ 재료 md5 14개 시작과 같음(`work/materials.md5`, `R2/` 포함) · 배포 PUT 0 · 네이버 0 · 키 파일 0 · 운영 작업 폴더 열기 0 · 회차 1 clone 쓰기 0.
- 다음 단계([넘길 때]): ④ 첫 검증 `D:\saero-verify` 새 세션 **Fable 5.1 · ultracode**(위 검증용 clone, 운영 폴더·작업 clone·회차 1 clone 읽기만, 판정만·쓰기 0) / 수정 뒤 재검증 새 세션 · 바뀐 것만 · **Fable 5.1 · xhigh** / ⑤ 수정(막음 있을 때만) 새 세션 **Opus 5.5 · xhigh · ultracode 끔** / ⑥ 병합은 ④ 세션에 이어서(갱신 회차가 돌지 않을 때 — last-audit 맨 위는 main 쪽 회차 절을 살림, **그날 아침 데이터 회차 뒤에 병합하고 첫 적용을 바로 붙임**) / 첫 적용 운영 세션 `/saero-run` **Opus 5.5 · high · ultracode 끔** — 아래 본보기.

## 첫 적용 본보기(운영 세션이 그대로 쓴다)
- **경로 C**(사용자 결정 10 — 모양만 바꾸는 별도 배포 회차): 그날 평일 아침 데이터 회차가 끝난 뒤, 같은 합본으로 2-1 같음 → "다시 계산". 운영 세션 `/saero-run`(Opus 5.5 · high · ultracode 끔), 첫 말 **"회차 2(모양) 첫 적용 — 경로 C — 보류로 시작 — 6단계 도장까지만, 배포는 내가 말함"**.
- 흐름: S0 → (수집·ingest 생략 — 아침 회차 합본 그대로) → 4 `deploy.py fetch --out work/prev.html && cp work/prev.html work/index.html`(직전 배포본 = meta 없는 옛 판) → 5a compute → 2-1 같음 → 사용자 "다시 계산" → 3 → 5-0a(pull · propose `--since` 그대로) → ⓐ 해당만 → **5 = `"$PY" scripts/apply.py --layout --html work/index.html --compute work/compute.json`**(변환 + 값 — 글은 같은 기간이라 그대로, 서술 스크립트 없음) → 6 `scripts/precheck.sh work/index.html work/combined work/prev.html`(기대: validate 24/24 · compare OK 99/DIFF 0 · 3폭(details 열고) · narrative `[주의] 같은 기간` · 도장) → **보류 멈춤**: 작업본 `work/index.html` + 전후 비교 페이지 `"$PY" /d/saero/feat-20261006-layout/work/R1/mk_compare.py --old work/prev.html --new work/index.html --out work/compare_<날짜>.html --online`(본보기 md5 622cb68a — 그때는 밖 요청 허용, 차트까지) 을 사용자에게 보인다 → 사용자 **"배포"** → 7 `deploy.py push --file work/index.html --base work/prev.html --message "레이아웃 판 r2026-10-B 첫 적용" --dry-run`(`[주의] 레이아웃 판이 바뀜`) → **`push … --layout-change`** → `verify --ref <커밋>` → 8 기록.
- **병합은 그날 아침 데이터 회차 뒤에 하고 첫 적용을 바로 붙인다** — 병합 뒤 첫 적용 전에 데이터 회차가 먼저 돌면 5단계 `apply --layout` 이 모양을 바꾸고 게이트가 PUT 을 막는다: 그때는 PUT 0 으로 멈추고 사용자에게 묻는다(경로 A 는 사용자 결정 없이 쓰지 않는다).
- 그 다음 회차부터: 직전 배포본이 레이아웃 판(meta 있음) — `apply --layout` 은 변환을 건너뛰고 값·summary 만, 게이트는 조용히 통과(자동 배포 그대로), 서술은 표지 기반(ⓑ).

---

## 갱신 회차 (2026-10-06 15:02~15:09 KST — Code 탭 `/saero-run`, main 작업 폴더, **리포트 읽기 쉽게 회차 1(글) 첫 적용 · 경로 C**) · **배포 완료 `037aca8`**
상세 = 아래 "## 2026-10-06 오후 갱신 회차" 절(대조 목록 표 아래). 사용자 첫 말 "보류로 시작 — 6단계 도장까지만, 배포는 내가 말함". S0 PASS → 수집·ingest 생략(오전 `cb0a3b1` 합본 그대로 — 2-1 "다시 계산") → 4 fetch(배포본 `f7bc605` = 6aaa2472, 옛 글·표지 0) → compute(2446b7c0 = 리허설 R1 바이트 동일) → 2-1 같음(41일) → 사용자 "경로 C" = "다시 계산" → 3 신규 0 → 5-0a pull(registry 바이트 불변)·propose `--since 2026-10-06`(빈 창, 후보 0) → ⓐ 해당 0(질문 없음) → 5 apply(변경 없음) + `work/n1006c.py`(본보기 wrap_old → 글 → rep_all, 표지 36) → 작업본 **002233ee = 리허설 R1 산출과 바이트 동일** → 6 precheck(validate 23/23 · compare OK 95/DIFF 0 · 넘침 0 · narrative `[주의] 같은 기간` · 도장 full) → **보류**(작업본 사용자 확인) → 사용자 "배포" → 7 dry-run → PUT `037aca8` → `verify --ref` 1회째 일치.
- **다음 회차**: 새 모양(서술 표지 있음)이 직전 배포본 — 서술은 표지 기반(ⓑ, 본보기 `R2/n1006b.py`)으로 `rep_all`, narrative 가 매회차 24자리 미교체를 막는다. propose `--since 2026-10-06` · `--prev ~/saero-fetch/downloads/2026-10-06`. 10/5 등록분은 10/6부터, 10/6 등록분은 10/7부터 판정.
- **다음에 볼 것(후보)**: 같은 기간 재배포의 "N회차 연속"은 늘리지 않았음(자동매칭 25 · 최다 시간 22 — 같은 데이터라 새 관찰 아님). 다음 데이터 회차는 이 배포본 + 1(26 · 23).
- **배포 뒤 전후 비교(사용자 요청)**: playwright로 옛(6aaa2472)·새(002233ee) 01·07 섹션을 1280·390 폭에서 캡처해 나란히 놓은 비교 페이지 `work/compare_1006c.html`(gitignore)를 만들었다. canvas 8/8은 두 판 모두 그려짐. 표 제외 글자 수: 01은 1,643 → 457, 07은 4,553 → 2,318. 390 폭 높이: 01은 1,522 → 901px, 07은 5,294 → 4,106px, 전체는 18,001 → 13,836px. **옛 배포본 01 머리글 굵은 줄이 "10/4(일) … 9/30 하루 최다 타이"(하루 전 문장)로 남아 있었다** — validate·compare가 읽지 않는 자리라 못 잡은 것이고, 이번에 그 줄을 지우면서 해소됐다(R4 (7) 유형 — 이제는 narrative가 매회차 표지로 막는다). 후보: 글·모양을 바꾸는 회차(회차 2 첫 적용)는 보류 멈춤 때 이 비교 페이지를 처음부터 함께 낸다.

---

## 검증·병합 기록(2026-10-06 — 리포트 읽기 쉽게 회차 1 글: 검증 1(막음 0) → main 병합)

**병합**: `feat-20261006-readable`(`0b04530` — eae71fc 위 9커밋: 09bf9d3·04d85c1·848e236 탐색 기록 · 21da210 compute·compare · cc8d119 validate·mutation · b7bc67b apply·config·test_apply·fixture · 5e7fd95 narrative_check·precheck·시험 · 5d8513f 문서 · 0b04530 구현 기준선)을 main(`eae71fc` — 분기 뒤 main 변경 0, 14:50 KST `ls-remote` 확인 · 갱신 회차 돌지 않는 시각)에 `git merge --no-ff` → 병합 커밋 **`9d66578`**(부모 eae71fc · 0b04530, 트리 = 0b04530 과 동일 — `git diff --stat 0b04530 HEAD` 0). 충돌 0(audit/last-audit.md 포함 — main 이 움직이지 않아 자동 병합). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`(전역 설정 변경 0). clone `D:\saero-verify\merge-20261006-readable`(`git clone -c core.autocrlf=false`). 사용자 병합 지시(2026-10-06, 병합 지시문 — "리포트 읽기 쉽게 회차 1(글) — 병합(⑥)") 뒤 병합. 브랜치 `feat-20261006-readable` 은 지우지 않고 둔다. 코드·문서·config·data 재수정 없음(이 절 추가만). 아래 구현 기준선 "마무리 기록"의 `브랜치 push 1회(… main 아님)` 는 당시 사실 — 원문 보존, 이 절로 정정(**2026-10-06 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고에).

**검증 1**(`D:\saero-verify\saero-ad-report_검증_리포트읽기쉽게_회차1_2026-10-06.md`, 별도 세션 — Code 탭·이 PC, Fable 5.1 · ultracode, clone `D:\saero-verify\feat-20261006-readable-1`, 대상 0b04530, 검토 에이전트 5): 아래 구현 기준선 "검증 회차가 볼 것" 1~14 전부 참 · 리허설 R0~R6 재실행 md5 전부 기록과 일치(R1 index 002233ee · R2 new40 3da35369 · R2 index 6f39dcf4 · R5 PNG 8f48840a·ee4da3c2) · **막음 0** → "다음 단계로 가도 된다". 이월 17건은 보고 전문에(아래 이월에 일부만).

**병합 main에서 전체 세트 재실행** [실측] — 이 PC(venv `D:\saero\.venv` Python 3.12.10), `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1`, `-W error::ResourceWarning`, test_deploy 는 `GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`·`GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`(실제 자격 증명 0). 재료는 검증 clone `work/` 에서 읽기만으로 사본(병합 clone `work/R1/` = v1 index 002233ee·compute.json 2446b7c0 · `work/mt/` = v2 index 6f39dcf4·compute.json f24ecb6f + combined 4 키워드 b7d91858·검색어 e3a352a2·시간대별 faac5a0a·상세지역 e70e5023):
- 전체 시험 4: `tests/test_exclusions.py` **Ran 49 OK** rc 0(1.0초) · `tests/test_deploy.py` **Ran 17 OK** rc 0(29초) · `tests/test_ingest.py` **Ran 10 OK** rc 0(62초 — 전체, 가짜 래퍼 패턴 `*narrative_check.py` 301행 포함) · `tests/test_fetch_reports.py` **Ran 15 OK** rc 0(79초, "OK" 줄로 판정). skipped 0 · ResourceWarning 0.
- 회차 1 시험 4: `tests/test_apply.py` **Ran 8 OK**(5.0초 — ApplyRehearsal skip 없이 `work/R1/`) · `tests/test_narrative_check.py` **Ran 7 OK**(0.1초) · `tests/test_validate_07.py` **Ran 6 OK**(0.001초) · `tests/test_compare_sections.py work/mt/index.html work/mt/compute.json` **3/3** rc 0(기준 exit 0 · OK 95 · DIFF 0 · 원본 md5 그대로 · "전부 맞음"). 단 이 시험은 자기 md5 도우미(71행 `open(p,"rb").read()`)에서 `Exception ignored … ResourceWarning: unclosed file` 4줄을 찍음(rc·판정 영향 0 — 아래 이월).
- `tests/mutation_test.py work/mt/index.html <combined 4>` rc 0(29초) **"전부 살아 있음"** — 기준 23/23 · 커버리지 23/23 · `[OK]` 46 · MISS/UNCOVERED/SKIP 0 · 원본 md5(html·CSV 4·data/ 12개) 전부 동일. 배포 저장소 현재 배포본(f7bc605, 옛 글)으로는 돌리지 않음(23번째 "07 각주 세 자리" FAIL 이 정상). deploy.py 는 test_deploy 안에서만.
- `py_compile` scripts 10 · tests 10 = **20/20**(cfile 스크래치) · `bash -n` ingest.sh·precheck.sh 통과 · config `json.load` 통과.
- md5: `cat data/*/*.csv audit/exclusions.csv | md5sum` 병합 전 main = 병합 뒤 = 전체 세트 뒤 **`aa89297c`** · config/report-config.json **`cd6afefa`**(150행 — eae71fc 와 차이는 competitor_defaults 5줄 추가뿐) · local/ 변경 0(`git diff --stat eae71fc HEAD -- local/` 빈 출력) · 작업 트리 변경 0(무시 파일 `work/` 뿐). 배포 PUT 0 · 네이버 0 · fetch_reports 실행 0 · 실제 자격 증명 0 · 운영 작업 폴더·작업 clone 열기 0.

**이월**(한 줄씩 — 나머지는 보고 전문):
- (검증 1 이월 1) apply.py main 의 예외 메시지 통일 — IndexError·TypeError 도 `[FAIL] apply:` 로(지금은 Traceback exit 1, 쓰기 전·무해).
- (검증 1 이월 2) compare `== 대조 결과` 줄에 기대 총수 `/95` 병기.
- (검증 1 이월 5) 07 ② 를 별도 서술 표지(07-excl 등)로 — ② 만 묵어도 ③ 이 바뀌면 narrative 가 못 잡음.
- (검증 1 이월 15, 문서) 구현 기준선 이월 7 문구 "미룬 등록만" → "2-1 같음 경로 전부".
- (검증 1 이월 12, 문서) narrative_check 메시지 6종(FAIL 2·[주의] 2 추가분)을 SKILL.md·code-tab.md 에.
- (병합 세트) `tests/test_compare_sections.py` 71행 md5 도우미가 파일을 닫지 않아 `-W error::ResourceWarning` 에서 "Exception ignored" 4줄(rc 0·3/3 — 판정 영향 0) → `with open` 후보(검증 1 이월 10 compare.py 29행과 같은 꼴).

**병합 뒤**(이 병합 세션은 하지 않았다): ① main 작업 폴더 `D:\saero\saero-ad-report-skill` `git pull --ff-only`(운영 세션 몫, 첫 실사용 전 — ingest 시작 검사 "HEAD = origin/main" 이 막는다) ② local/ 변경 0 → 설치본(`D:\saero\CLAUDE.md` · `D:\saero\.claude\skills\saero-run\SKILL.md`) 갱신 불필요 ③ 첫 실사용 = 회차 1 첫 적용(경로 C, "보류로 시작 — 6단계 도장까지만, 배포는 내가 말함") 운영 세션 `/saero-run` Opus 5.5 · high · ultracode 끔, 본보기 = 아래 구현 기준선 "본보기" 줄(`D:\saero\feat-20261006-readable\work\narr_lib.py` 18dd9c39 · `R1\n1006b.py` 2ccf4d99 · `R2\n1006b.py` a64eef31 — 그 회차 META·judged 만 바꿔 wrap_old → 글 → rep_all) ④ 회차 2(모양: details·03 역순·report-layout meta·deploy 게이트·summary·세로/접기)는 별도 탐색·구현 회차.
효율: 벽시계 약 10분(14:50 ls-remote → clone·병합 → 전체 세트 14:51~14:55 → 기록·push) · 도구 호출 약 20회 · 하위 에이전트 0 · 즉석 코드 약 25행(시험 러너·py_compile 조각 — 스크래치).

---

# 기능 추가 구현 기준선(리포트 읽기 쉽게 — 회차 1 글, 2026-10-06)
점검일: 2026-10-06 (기능 추가 회차 — **구현, 회차 1 = 글**. 데스크톱 앱 Code 탭, 이 PC, 작업 폴더 `D:\saero`로 연 세션, Opus 5.5 · ultracode). 작업 clone `D:\saero\feat-20261006-readable` 브랜치 `feat-20261006-readable`. 시작 확인 [실측]: HEAD `04d85c1`(= main `eae71fc` + 탐색 기록 2커밋, 코드 0) · work/ 사본 md5 9개 = 지시(index 6aaa2472 · prev 95c58082 · compute.json f60152d9 · 검색어 e3a352a2 · 상세지역 e70e5023 · 시간대별 faac5a0a · 키워드 b7d91858 · apply.py 702de83d · n1006.py 754921d7) · `git fetch` 뒤 origin/main = `eae71fc`(갱신 회차 없음). 작업 중 12:32 에 탐색 세션이 이 clone 에 기록 커밋 **`848e236`**(탐색 기준선 절 한 줄 — 구현 지시문 경로, 코드 0)을 넣었다 — 내 변경과 겹침 0, 이 브랜치에 그대로 둔다. 운영 main 작업 폴더 열기 0 · data/·registry 변경 0 · 외부 쓰기 0(네이버·API·배포 저장소 요청 0, 키 파일·자격 증명 열지 않음, fetch_reports·exclusions·deploy·ingest·archive 실행 0).
설계: 탐색 기준선 3.0 공통 뼈대 + 사용자 결정(2026-10-06 — ② 고르기) 11·12 의 **회차 1 몫만** — 글 줄이기 규칙(문서 + 리허설 적용본) · 서술 표지 + `scripts/narrative_check.py`(막음 M1) · validate "07 각주 세 자리" · `scripts/apply.py` 저장소화(E2) · compare 구역별 try + 10 나열 → 최근 7일 + 평균 · compute 경쟁사표 0행 FAIL · TAGS + details/summary(회차 2 선반영) · mutation 변조 1·가드 2. **회차 2(details·03 역순·합계 위·report-layout meta·validate "레이아웃 판"·deploy 게이트·summary·.fold/.vbox·세로/접기 규약·overflow details·차트 폭)는 건드리지 않았다.**
검증용 clone: `git clone -c core.autocrlf=false -b feat-20261006-readable --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill D:\saero-verify\feat-20261006-readable-1`
효율: 벽시계 약 1시간 50분(12:20 무렵 시작 확인 → 13:50 리허설 끝 → 기록·커밋·push) · 도구 호출 조정자 약 105회 + 자기 검토 워크플로 에이전트 4개(검토 3 + 기계 확인 1, 202회) · 즉석 코드 약 690행(전부 clone `work/` 스크래치 — `narr_lib.py` 458 · n 스크립트 3개 42 · R0 `mk_c40.py` 37 · R4 `r4.sh` 35 · R5 `measure.py` 51 · `rehearse_R12.sh` 17 · 기타 조각).
표기: [실측] 이번에 파일·명령으로 확인 / [추론] 확인 못 함. 행 번호는 이 브랜치 커밋 기준.

## 바뀐 것(파일별, `wc -l` 전 → 후 · md5 앞 8자리) [실측]

| 파일 | 행 | md5 | 무엇 |
|---|---|---|---|
| `scripts/compute.py` | 251 → 261 | 1bf268a8 | `--competitors-html` 경쟁사표 0행 → `[FAIL] 직전 배포본 경쟁사표 0행 — 머리글 "경쟁사 브랜드명 검색어" 또는 행 마크업 확인` exit 1(합본 읽기 전, `-o` 안 씀) · 새 키 `06.카드30회이상일`(카드 dict 와 분리 — compare "06 카드" 대조 보호) · `10.최근7일노출`·`최근7일클릭`·`최근7일` |
| `scripts/compare.py` | 181 → 207 | b6c41f70 | 47~178행 try 하나 → **구역 함수 12개 + 구역별 try**(실패 = `파싱 실패 [구역]` DIFF, 다음 구역 계속 — 공유값 `S["kpi"]`→07 · `S["got4"]`→06) · 10 항목 3 새 형식(`최근 7일 노출은 …회, 클릭은 …건(M/D~M/D)` · `9/6 이후 N일 하루 평균 N건(N일 평균 N건)`). 다른 항목 이름·정규식·대조 값은 글자 그대로(자기 검토가 04d85c1 본문과 기계 diff — 차이 = S 3줄 + 10 항목 3). **항목 수 N = 95**(그대로) |
| `scripts/validate.py` | 424 → 455 | 5742a513 | 검사 **"07 각주 세 자리(경쟁사 판정·제외 검색어·클릭 0 전체)"**(`check_07_footnotes`: 07 `class="note"` 전부 이어 붙여 ① `경쟁사 판정\(` · ② `제외 검색어: .*?등록 (\d+)개 · 확인 (\d+)/(\d+) · 실패 (\d+)` · ③ `클릭 0인 검색어 전체는 (\d+)개·노출 ([\d,]+)회` + b = 등록 × `exclusions.targets` 수 · a ≤ b + `click0_items` ≥ 1) → **22 → 23개** · TAGS + `details`·`summary` |
| `scripts/apply.py` (신규) | 0 → 249 | d1fafedf | `work/apply.py` 저장소화 — `--html`(기본 work/index.html)·`--compute`(기본 work/compute.json) · 앵커 정확히 하나(`once`) · 실패 `[FAIL] apply:` exit 1 + 작업본 그대로(끝에 한 번만 씀) · `NEWC` → config `competitor_defaults` · 01 순위 5칸 끝 앵커 `\n      </div>\n      <div class="note">`(서술 무관) · min-width 개수는 01·06 컨테이너만 · 10 표 4행 아니면 FAIL · 경쟁사 행이 직전 행도 신규 후보도 아니면 FAIL |
| `scripts/narrative_check.py` (신규) | 0 → 84 | 8057832c | `<작업본> <직전 배포본>` — ① 작업본 표지 0 → FAIL · 표지 짝·이름 중복 → FAIL ② 같은 기간 → `[주의] 같은 기간 — 대조 생략` exit 0 ③ 직전에 표지 없음 → `[주의] 직전 배포본에 표지 없음 — 대조 생략` exit 0 ④ 매회차 블록이 직전 같은 이름 블록과 바이트 같으면 `[FAIL] 서술 미교체 <자리>` exit 1 |
| `scripts/precheck.sh` | 37 → 38 | 7b40aefc | overflow 뒤·md5 재확인 전 `run "$PY" scripts/narrative_check.py "$HTML" "$PREV"`(FAIL 전문, 실패면 도장 없음) |
| `tests/mutation_test.py` | 379 → 386 | ef300789 | 변조 "07 각주 ② 문구 변조(제외 검색어: → 제외검색어:)" + 0건 가드 "07 ②③ 각주 블록 제거"·"07 ① 경쟁사 판정 줄 제거" |
| `tests/test_ingest.py` | 383 → 383 | 218a532e | 가짜 파이썬 래퍼 패턴에 `*narrative_check.py`(precheck 한 줄 때문에 PrecheckTests 가 깨지지 않게) — **지시대로 이번엔 돌리지 않음**, 병합 전 전체 시험에서 |
| `tests/test_apply.py` (신규) | 0 → 212 | 2262405e | 멱등(표지 없음·표지 있음 fixture, 리허설 R1 산출이 있으면 그것도) · 값·행 수(03 날짜+합계·07 정식표·동률 직전 순서·경쟁사 신규 = config 기본값·08·10) · 시끄러운 실패 5종 + 새 04 그룹 + 후보 밖 경쟁사 · compute 경쟁사표 0행 FAIL(소제목만 바꾼 fixture — r10 유형) |
| `tests/fixtures/layout_old.html`·`layout_old.compute.json` (신규) | 0 → 460 · 0 → 594 | f29b1c71 · 08b2c31a | 10/6 배포본의 apply 앵커 마크업 발췌 — 숫자·검색어·경쟁사·그룹 이름 **전부 가짜**, 7일 가짜 compute |
| `tests/test_narrative_check.py` (신규) | 0 → 97 | a7e4ccfe | 미교체 FAIL · 전부 교체 PASS · 표지 0 FAIL(같은 기간에도) · 직전 표지 없음 [주의] · 같은 기간 [주의] · 짝·중복 FAIL · CLI exit |
| `tests/test_validate_07.py` (신규) | 0 → 90 | f365c604 | 평상 PASS · exclusion-ui 9절 예외 회차 문구 6꼴 PASS · a > b · b ≠ N × 그룹 · ①②③·클릭0 목록 각각 없음 · note 0 → FAIL |
| `tests/test_compare_sections.py` (신규) | 0 → 115 | 00960abe | 인자형(`<index.html> <compute.json>` — 배포본을 저장소에 넣지 않으려고, mutation_test 와 같은 꼴): 01 해석·07 ②③·10 최근 7일 문장 하나씩 지운 사본 → DIFF 는 그 구역만, 다른 구역 기준 OK 전부 다시 OK |
| `config/report-config.json` | 145 → 150 | cd6afefa | `competitor_defaults{_comment, district "노원구", match "확장"}` |
| `SKILL.md` | 561 → 584 | a8fd4d4e | 5단계 교체 명령(apply.py + n<날짜>.py, 서술 표지 정본 = report-structure) · 6단계 넷째 narrative · 9항목 7 "박스 머리글 줄 없음" · 배포 전 검산 23개 + "07 각주 세 자리" + precheck 가 함께 돌리는 것 · 참고(apply·narrative_check·시험 4) |
| `references/report-structure.md` | 410 → 525 | 6b8874b4 | 01·04·06·07·08·09·10·11·12 "길이" 줄(3.0 표 그대로) · 06 `카드30회이상일` 정의 · 10 정의(최근 7일 + 평균, 302행 개정) · 07 각주 ①②③ 두 블록 자리 · 12 철회 사유 자리 · **"서술 공통 규칙"** · **"서술 표지"** 절(자리 36 · 매회차/고정 · 자리별 compare 리터럴 · 공개 무해 · 첫 적용) |
| `references/code-tab.md` | 235 → 240 | a7bb7b39 | 3절 5행(apply + n<날짜>.py · ② 형식) · 6행(narrative) · "2-1 같음" narrative 생략 한 줄 · 4절 "보류 뒤 같은 세션 재개 = 7단계부터(도장 유효)" + 첫 적용 회차 첫 말 예문 |
| `references/exclusion-ui.md` | 160 → 173 | 5b504b93 | 9절 07 ② 형식 + 예외 회차 고정 문구 표(등록 0 · "등록은 나중에" · 부분 실패 a/b · 등록돼 있는데도 노출 · 등록 누락 → 후보 · 미확인 — 전부 ② 정규식 꼴) |
| `audit/checklist.md` | 507 → 511 | d676df93 | 갱신 이력 한 줄 · [의도된 동작] **27**(글 규칙 — 사용자 결정 원문 두 문장 인용) · 16 "22개" → 23·mutation [OK] 46 · [되돌리면 안 되는 것] 2행(07 각주 세 자리 · 서술 미교체 검사) · 대상 파일 목록 |
| `audit/last-audit.md` | — | (커밋 뒤) | 이 절 + E2 정의 줄(2264행 근처) 현행화 |

지시 밖 변경 0: `scripts/deploy.py`·`exclusions.py`·`fetch_reports.py`·`archive.py`·`reportlib.py`·`ingest.sh`·`references/css-and-layout.md`·`report-fetch.md`·`local/`(saero-run · CLAUDE.md · prompt-polish)·`data/`·`audit/exclusions.csv` 불변.

## 임의 결정(번호 = 사용자가 바꿀 단위)
1. **서술 표지 36개 = 매회차 24 · 고정 12**(자리 표는 report-structure.md "서술 표지"). 고정 = 표 설명·규칙 5(04-foot·07-src·07-legend·12-desc·12-basis) + **compare 가 숫자를 대조하는 한 줄 7**(02·05·06·07·08·10 desc · 09-foot — 문구가 같아도 되는 자리라 narrative 대조 밖, 교체 대상으로만 표지). 지시의 "고정 = 표 설명·규칙"을 넓힌 것. 표지 밖 숫자는 apply 기계 자리뿐.
2. **04-desc 는 매회차**(`… — M/D까지 격차 A → B배, 그대로`) — 첫 판은 고정이었으나 자기 검토 막음(아래 "자기 검토")으로 바꿨다. 규칙: compare 가 읽지 않는 지난 회차 값·방향어를 쓰는 한 줄은 매회차 + `M/D까지`.
3. 매회차 블록에는 마지막 날짜·일차·회차 수가 들어가게 썼다(04-mint·07-right·08-note·10-mint 에 `M/D까지`) — 값이 같아도 문구가 바뀌게.
4. 12-1·12-2 표지는 **상태 태그까지 안**(상태가 바뀌면 태그도 바뀌므로), 11-list 는 `<ul>` 밖(지시).
5. **01 ① 표 아래 하루 분해 각주(옛 L338)도 지웠다** — 3.0 "뺄 것: 하루 분해 서술"을 블록 통째로. 01 박스 = ① 표 · ② 순위 5칸 + 각주 · ③ 해석.
6. **집계 기준**의 회차 숫자("포함된 값(노출 N회)")를 빼고 "차이는 08·09번 각주"로 — 고정이 되게.
7. 서술 숫자 = compute 키(+ 지난 회차 compute)만 → 옛 서술의 하루 분해·"8/27 이후 가장 낮음"·그룹 하루 노출 나열·"0.7건 많아" 같은 파생 수를 뺐다. compute 키 신설 2: `06.카드30회이상일`(상계동 승격 조건 판정 원천 — 카드 dict 밖에 둔 이유: compare "06 카드" 항목이 dict 전체를 대조) · `10.최근7일*`. 예외 원천: 제외 검색어 등록·확인·실패 수 = exclusions.py 출력(registry), "N회차 연속" = 직전 배포본 + 1.
8. **compare 10 항목 3**: 지시 정규식보다 넓혀 `(M/D~M/D)` 기간과 `(N일 평균 N건)` 까지 대조(같은 항목 안 — 수 그대로 95). 항목 이름: "10 최근7일 노출 나열" · "10 최근7일 클릭 나열·기간" · "10 9/6이후 일수·하루평균클릭(전체 평균 포함)".
9. **narrative 판정 순서**: 표지 0 FAIL 을 "같은 기간 생략"보다 먼저(같은 기간이어도 표지 잃은 작업본은 막음) + 표지 짝·이름 중복 FAIL 추가(지시 밖 두 가드).
10. **validate 검사 번호 대응**: 기준선 4절·3.1 의 "24 07 각주 세 자리"는 회차 2 의 "23 레이아웃 판"을 앞에 둔 번호 — 이번 판에서는 출력 23번째(23개). 회차 2 가 들어오면 24개. 문서·기록은 이름으로 부른다.
11. **apply.py 를 옛 판보다 엄격하게**: `once` = 정확히 하나(옛 판은 첫 일치만 확인) · min-width 개수를 01·06 컨테이너로(옛 판은 문서 전체 — 기간 8일 이하면 바닥값 650px 이 09번 고정 650px 과 겹쳐 3이 되는 숨은 결함, fixture 가 드러냄) · 10 표 4행·경쟁사 행 원천 검사. 실값 경로는 옛 판과 바이트 동치(10/5 배포본 + 41일 compute → 신규 변형 행 포함 같은 바이트 [실측]). tbody·목록은 옛 판처럼 앵커 뒤 첫 일치(엉뚱한 자리는 compare·validate 가 요란하게 잡음).
12. **첫 적용 변환(ⓐ) 앵커 = 옛 글 시작 문구 중 숫자 없는 리터럴 + 여는 태그**(`→ 콘텐츠 지면 없는 날이`·`<div class="note">닷새 동안`·`다만 두 광고는 성격이 달라` 등 — 10/5·10/6 두 배포본 모두 구역 안에서 정확히 하나 [실측]). 지시의 "옛 숫자 리터럴 앵커"를 숫자 없는 문구로 바꿔 첫 실사용 회차의 옛 배포본에도 그대로 맞게 했다. 흐름 = `wrap_old`(표지 뼈대 + 5블록 삭제) → `rep_all`(표지 이름으로 교체, 빠진 자리·남는 글이면 멈춤).
13. R2 의 `n1005b.py` 는 new40 에 표지가 없어서 `wrap_old`(ⓐ 앵커) 뒤 `rep_all`(ⓑ) — 지시의 "ⓑ 표지 기반"은 글 교체 부분. `R2/n1006b.py` 는 순수 ⓑ(표지 없으면 멈춤).
14. 지난 회차 값 출처: 10/6 글 = 40일 compute(`work/c40/compute.json` — 10/5 배포본이 통과한 값과 같음, 10/5 배포본 × c40 compare OK 90/DIFF 1(10 새 형식만)) · 10/5 글 = 10/5 배포본 원문에 적힌 "지난 회차" 값(`narr_lib.PREV_1005`).
15. 시험 둘을 지시 밖으로 더했다: `test_validate_07.py`(지시 "validate 시험에 그 문구 1건" → 6꼴) · `test_compare_sections.py` 는 인자형. compute 0행 시험은 `test_apply.py` 안.
16. 리허설 경로는 지시 그대로 `work/R1·R2·R4·R5` — 아래 "사건" 2 참고.

## 리허설 결과(전부 clone 안 사본, 최종 코드) [실측]
- **R0** `work/c40/`(스크래치 `work/R0/mk_c40.py`): 키워드 631행·검색어 2,203·상세지역 1,738(일별 2026.08.26.~10.04.) · 시간대별 = data/2026-08·09 + `git show 0e9ba66:data/2026-10/시간대별.csv` 를 archive.py 방식으로 합산(노출 12,009 = 키워드 전체 12,009 · 클릭 383 = 383) · 첫 줄 `(2026.08.26.~2026.10.04.)`. `compute.py work/c40 --competitors-html work/prev.html` → **"2026.08.26 — 10.04 (40일)" · 경쟁사 39행 · 후보 []** (md5 c40/compute.json 81f475fb).
- **R1 첫 적용(경로 C 글만)**: compute(prev = 10/6 옛 글) 40행·후보 [] → apply "(변경 없음)" → `work/R1/n1006b.py` 표지 36 → precheck: **validate 23/23 · compare OK 95/DIFF 0 · overflow 360/390/430 넘침 0 · narrative `[주의] 같은 기간 — 대조 생략(… 표지 36개 중 매회차 24개)` · 도장**(작업본 002233ee · 직전 6aaa2472 · full).
- **R2 다음 회차**: new40(10/5 배포본 사본) + c40 → apply 변경 없음 → `n1005b.py` 표지 36 → c40.json **39행 = c40/compute.json 바이트 동일**(새 글이 직전 배포본이어도 경쟁사표 그대로 읽힘) → compute(prev = new40) **40행·후보 ['노원부티필라테스']** → index 에 apply(신규 변형 행 = config 기본값 노원구·확장) + `R2/n1006b.py`(ⓑ) → precheck **validate 23/23 · compare 95/0 · 넘침 0 · narrative `[PASS] 서술 표지 36개 · 매회차 24개 전부 직전 배포본과 다름` · 도장**(6f39dcf4 · 3da35369) → 자기 자신 기준 compute **40행·후보 []**.
- **R1 ↔ R2 바이트 대조**: 11번 판정 줄 한 줄만 다름(지난 회차가 10/5 배포본 8개 vs new40 7개 — 당연한 차이). 목록 동률 순서·경쟁사 행까지 같음 — 첫 적용 경로와 표지 기반 경로가 같은 리포트를 만든다.
- **R3** `mutation_test.py work/R2/index.html` + CSV 4 → **exit 0 "전부 살아 있음"** · 기준 23/23 · [OK] 46(변조 23 + 0건 가드 16 + archive 7) · 커버리지 23/23 · UNCOVERED·MISS·SKIP 0 · 원본 md5 동일.
- **R4 역검증**(`work/R4/r4.sh` → `r4_final.log`): (1) 새 validate × 옛 글(work/index.html) → "07 각주 세 자리" FAIL(① ② 0건), 22/23 (2) ② 문구 변조 → 같은 검사 FAIL (3) 07-notes 를 new40 것으로 → narrative `[FAIL] 서술 미교체 07-notes` exit 1 (4) 표지 전부 제거 → `[FAIL] 작업본에 서술 표지 0개` (5) 경쟁사 소제목 "경쟁사 검색어 (40개)" → compute `[FAIL] … 0행` exit 1 (6) 새 compare × 옛 글 → OK 90/DIFF 1(`파싱 실패 [10]` — 11·12 는 계속 대조) (7) **compare 가 안 읽는 12-note·06 카드를 지난 회차 그대로 → validate 23/23·compare 95/0 인데 narrative FAIL 2 · 도장 없음**(10/6 01 머리글 사고 유형 — 이전엔 자동 배포됐을 자리) (8) 04-desc(지난 회차 값) 그대로 → narrative FAIL · 도장 없음 (9) **test_compare_sections 3/3**: 01 해석 삭제 → DIFF 1(`파싱 실패 [01]`)·다른 구역 기준 OK 81 중 81 다시 OK · 07 ②③ 삭제 → 82/82 · 10 문장 삭제 → 87/87.
- **R5 화면**(관찰값 — 기준선 0절 방식, `work/R5/measure.py` → `measure.json`): 글자 수(표 제외) **16,493 → 8,215**(01 2,049 → 575 · 04 1,345 → 438 · 06 794 → 379 · **07 5,422 → 2,721** · 08 1,644 → 1,249 · 09 487 → 396 · 10 1,053 → 483 · 11 2,208 → 968 · 12 1,303 → 818, 12 칸 본문 1,535 → 420). 높이(Chart.js 미로드): **390×844 18,001 → 13,836px(21.3 → 16.4장)** · 1280×900 13,431 → 11,626px(14.9 → 12.9장) — 07 5,294 → 4,106(390). 12장·9장은 회차 2(03·07 접기) 몫. overflow 3폭 넘침 0. **미리보기 PNG**(file:// 만, 밖 요청 abort, 전체 페이지·차트 빈 칸): `D:\saero\feat-20261006-readable\work\R1\preview_390x844.png`(8f48840a) · `preview_1280x900.png`(ee4da3c2) — 사본 `work/R1/index.html` 을 브라우저로 열면 차트까지.
- **시험**(`-W error::ResourceWarning`): test_apply **8 OK**(리허설 R1 멱등 포함) · test_narrative_check **7 OK** · test_validate_07 **6 OK** · test_compare_sections **3/3**. test_exclusions·test_deploy·test_fetch_reports·test_ingest 는 지시대로 돌리지 않음.
- **본보기(첫 실사용 세션이 쓸 것, 저장소 밖 — gitignore)**: ⓐ 첫 적용 변환 `D:\saero\feat-20261006-readable\work\R1\n1006b.py`(2ccf4d99) + `D:\saero\feat-20261006-readable\work\narr_lib.py`(18dd9c39 — `SPANS`·`DELETE` 앵커 · `wrap_old` · `rep_all` · 글 함수 `blocks`·`items_common` · 회차 사실 `META_*`) / ⓑ 표지 기반 `work\R2\n1006b.py`(a64eef31) · 40일판 `work\R2\n1005b.py`(d264e98d) · 한 번에 `work\rehearse_R12.sh`. 첫 실사용은 그 회차 `META`(등록·경쟁사 판정·연속 회차 수)와 지난 회차 11번 판정(`judged`)만 바꾸고 `wrap_old → 글 → rep_all` 흐름 그대로.

**자기 검토**(지시의 [검토 깊이 규칙] — 워크플로 에이전트 4: 코드·검사 / 리포트 글·원칙 / 문서·범위 + 기계 확인(haiku)): 막음 **1건**(리포트·문서 검토자가 각각 재현) — 04-desc 를 고정으로 둬서 지난 회차 문장("격차 3.57 → 3.55배, 줄어듦")이 그대로 남아도 validate 23/23 · compare 95/0 · narrative PASS · 도장 → 자동 PUT(가끔 · 조용) → **고침**(임의 결정 2 — 매회차 + `M/D까지`, report-structure 고정 정의에 규칙 한 줄 같이). 고친 뒤 같은 재현 사본은 narrative `[FAIL] 서술 미교체 04-desc`·도장 없음 [실측]. 코드·검사 검토자 "가도 된다"(막음 0). 기계 확인: work/ md5 9개 그대로 · 시험 넷 OK · `line-height:1.9;">` 3곳(옛·R1·R2) · R1 `<details` 0 · 새 색 0(18개 같음) · data/·registry·local/ diff 0 · 도장 md5 = 파일 md5. 고친 뒤 판정: **다음 단계로 가도 된다**(막음 0).

**사건(사실대로)**:
1. 12:53 무렵 옛 `work/apply.py` 를 경로 바꾸지 않고 한 번 돌려(비교 실험 중 명령 실수) **`work/index.html` 을 다시 씀** — 같은 compute 라 바이트 동일(md5 6aaa2472 그대로, 수정 시각만 바뀜). 그 뒤 옛 스크립트는 경로를 바꾼 사본으로만(exec) 돌렸다. 지시 "덮어쓰지 않는다"를 글자로는 어긴 것.
2. **Windows 는 폴더 대소문자를 구분하지 않아** 지시의 `work/R1·R2·R4·R5` 가 탐색 프로브 `work/r1·r2·r4·r5` 와 같은 폴더다. 리허설이 그 안의 탐색 프로브 사본(r1·r2 의 index.html·prev.html, r4 index.html)을 덮어썼고, 같은 폴더의 compare.log·validate.log·overflow.log·heights.json(10:30 탐색 산출)은 남아 있다 — **리허설 근거는 위 R*·로그 이름(r4_final.log·rehearse_after_fix.log·mutation.log·measure.json)만**. 탐색 근거 전문은 저장소 밖 `D:\saero\saero-ad-report_리포트읽기쉽게_탐색_2026-10-06.md` 에 그대로. 다음 리허설 폴더는 소문자 프로브와 겹치지 않는 이름으로.
3. 작업 중 탐색 세션이 이 clone 에 `848e236`(기록 한 줄)을 커밋 — 위 머리.

## 검증 회차가 볼 것(완료 기준 표 회차 1 줄로 — 판정만, 쓰기 0)
준비: 새 clone(위 명령) + 이 clone 의 `work/` 에서 **읽기만으로 사본**: index.html(6aaa2472 — 10/6 배포본) · prev.html(95c58082 — 10/5) · combined/ 4(e3a352a2·e70e5023·faac5a0a·b7d91858) · c40/ 4(d6830103·a8c5eb81·1db13563·a4f54006) · 본보기 narr_lib.py·R1/n1006b.py·R2/n1005b.py·R2/n1006b.py·rehearse_R12.sh · R0/hourly_2026-10_0e9ba66.csv. 운영 폴더(`D:\saero\saero-ad-report-skill`)는 읽기만.
1. **누락 0** — R1·R2 에서 07 정식표 24·클릭1 35·클릭0 77·경쟁사표 40·08 TOP10 밖 39(compare 07 집합 4·08 컴팩트 2 + 직접 세기).
2. **숫자는 compute.json 만** — precheck(validate 23/23 · compare OK 95/DIFF 0 · overflow 3폭 · narrative · 도장) R1·R2 둘 다. 서술 표지 블록의 숫자가 compute(지난 회차 = c40)에 있는지.
3. **① 에 compute 키 없는 숫자 0** — 07-comp 첫 줄.
4. **서술 표지 미교체 0(M1)** — `narrative_check` R2 PASS · 매회차 블록 하나(compare 가 안 읽는 것)를 지난 회차로 되돌리면 precheck 가 narrative 에서 FAIL·도장 없음 · 04-desc 재현 · `test_narrative_check` 7. 고정 12개 중 지난 회차 값·방향어를 담은 블록이 남았는지.
5. **07 각주 셋** — validate "07 각주 세 자리"(옛 글 FAIL · ② 변조 FAIL · exclusion-ui 9절 예외 6꼴 PASS — `test_validate_07`) · mutation 변조 1·가드 2.
6. **8·9 각주 · 뒤집힌 결론 · "~로 보임" · 09 긍정 톤 · 9항목 자리 · 11·12 작성 기준** — R1 글(11 ≤ 8 + (참고) ≤ 2, 항목당 결론 1문장 + 괄호, 12 상태 줄·다음 회차 판정·이월 판정 줄, 날짜별 등록 나열 없음).
7. **화면 원칙** — 새 `#색` 0 · `.ctr-high` 다른 용도 0 · 표 `display:block` 0 · 외부 css/js 추가 0 · 01 머리글 2줄·L338 각주·07 ✓·⚠️ 없음 · 미리보기 PNG 2장.
8. **`line-height:1.9;">` 기준점 셋** — 옛·R1·R2 각 3곳, validate click1/click0 · compare · apply 그대로.
9. **옛 모양 복귀 가드 회차 1 몫** — validate "07 각주 세 자리" · `scripts/apply.py`(test_apply 8 · 옛 apply 와 바이트 동치) · compute 0행 FAIL · TAGS + details/summary · mutation 변조 1·가드 2(R3 [OK] 46·23/23).
10. **compare 생략 없음** — `test_compare_sections` 3/3 + compare 본문이 04d85c1 과 10 항목 3·S 3줄 말고 글자 그대로인지(diff).
11. **글자 수 관찰값**(16,493 → 8,215 · 07 5,422 → 2,721 — 기준 ≤ 8,500/≤ 2,800 은 관찰용) · 높이 21.3 → 16.4장(390, 12장은 회차 2).
12. **검증 폴더** `D:\saero-verify\<clone>` · **리허설 한 줄**(R0~R6 다시 — 같은 md5 가 나오는지: R1 002233ee · R2 new40 3da35369 · index 6f39dcf4).
13. 문서 = 코드: report-structure "서술 표지" 표 ↔ R1 실제 표지 36 ↔ `narr_lib.KIND` · SKILL.md·code-tab·exclusion-ui·checklist 문구 ↔ 스크립트 · 회차 2 항목을 건드린 곳 0 · local/·data/·registry 변경 0.
14. `test_ingest.py` 래퍼 한 줄 — 병합 전 전체 시험(test_exclusions·test_deploy·test_fetch_reports·test_ingest)에서 확인.

## 이월(한 줄씩 — 막음 아님, 점검 회차 또는 회차 2 와 함께)
1. narrative_check: 작업본에서 매회차 표지 **이름이 바뀌거나 종류가 고정으로 바뀌거나 표지를 잃으면**(직전에만 있는 이름) `[주의]`·무표시로 통과 — 가드 후보 "기간이 다르면 직전 매회차 이름 ⊆ 작업본 매회차 이름 · 종류 불변" (여러 우연 · 조용).
2. 표지 이름 `12-1`·`12-2` 가 위치 기준 — 앞에 새 항목이 끼면 다른 항목끼리 대조(가끔 + 실수 1 · 조용) → 항목 정체 이름(`12-exclusions` 등) 후보.
3. 날짜 없는 매회차 문구(뒤집힘 0 회차의 11-verdict 등)가 두 회차 같으면 거짓 FAIL(요란) → 판정 줄에 `M/D` 넣는 규칙 후보.
4. 07-desc 의 상위 2 검색어 이름·04-desc "1/3 이하"는 compare 밖(여러 우연 — 3위 58 vs 2위 83건).
5. apply `once` 가 엄격해져 서술에 apply 앵커 문구(`클릭당 평균 N원`·`광고비 비중 (총 N원)`·`(N개 지역·클릭 N건)`)를 다시 쓰면 apply FAIL(요란) → "서술 공통 규칙"에 금지 문구 목록 후보. SKILL.md 5단계·code-tab 3절 5행 "앵커가 하나가 아니면" 은 `once` 자리만 해당(표·목록은 첫 일치) — 문구 정밀화.
6. narrative 는 표지 집합을 문서 표(36)와 대조하지 않음 — 첫 적용에서 빠진 표지는 이후 검사 밖(여러 우연).
7. 2-1 같음 "미룬 등록만" 경로는 narrative 생략 — 07 ② 갱신은 사람 몫(설계상 예외, 드묾).
8. 문서: "서술 공통 규칙"의 "~로 보임" 자리 = 01 순위 각주만 vs 11 작성 기준 1) · SKILL.md (1-1) "12번 액션 표" vs report-structure "12 표 아래 note" 표기 차이.
9. `test_narrative_check.test_cli_exit_codes` 임시 폴더를 지우지 않음(무해).
10. 리허설 본보기 글의 11 첫 항목 근거·(참고) 경쟁사 줄은 이번에 스크래치에서 바로잡음 — 첫 실사용 글은 그 회차 사실로 새로(META·judged).
11. 높이 390×844 16.4장 — 12장·9장 목표는 회차 2.

## 마무리 기록(이번 회차)
- 커밋(경로 지정 add, `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`, 전역 설정 변경 0): `21da210` compute·compare(구역별 try·10 새 형식·0행 FAIL) · `cc8d119` validate·mutation(07 각주 세 자리·TAGS) · `b7bc67b` apply 저장소화·config·test_apply·fixture · `5e7fd95` narrative_check·precheck·시험 · `5d8513f` 문서 · 그리고 이 절 + E2 정의 줄(기록 커밋 — 해시는 자기 참조라 적지 않는다). 브랜치에는 탐색 기록 `09bf9d3`·`04d85c1`·`848e236` 도 함께 있다.
- 끝 확인(커밋 뒤): `git fetch` → origin/main 확인 · 브랜치 push 1회(`git -c credential.interactive=false push origin feat-20261006-readable`, main 아님) · 스크래치 `git clone -c core.autocrlf=false -b feat-20261006-readable --single-branch` 로 HEAD·md5 대조 — 결과는 채팅 보고(자기 참조).
- work/ 사본(index 6aaa2472 · prev 95c58082 · compute.json f60152d9 · combined 4 · apply.py 702de83d · n1006.py 754921d7) md5 시작과 같음 [실측] — 사건 1(index.html 수정 시각) 위 참조. 배포 PUT 0 · 네이버 0 · 키 파일 0 · 운영 작업 폴더 열기 0.
- 다음 단계([넘길 때] 그대로): ④ 첫 검증 `D:\saero-verify` 새 세션 **Fable 5.1 · ultracode**(위 검증용 clone, 운영 폴더 읽기만, 판정만·쓰기 0) / 수정 뒤 재검증 새 세션 · 바뀐 것만 · **Fable 5.1 · xhigh** / ⑤ 수정(막음 있을 때만) 새 세션 **Opus 5.5 · xhigh · ultracode 끔** / ⑥ 병합은 ④ 세션에 이어서(갱신 회차가 돌지 않을 때 — last-audit 맨 위는 main 쪽 회차 절을 살림) / 첫 실사용(회차 1 첫 적용 = 경로 C, "보류로 시작 — 6단계 도장까지만, 배포는 내가 말함") 운영 세션 `/saero-run` **Opus 5.5 · high · ultracode 끔** — 본보기 = 위 "본보기" 줄.

---

# 기능 추가 탐색 기준선(리포트 읽기 쉽게, 2026-10-06)
점검일: 2026-10-06 (기능 추가 회차 — **탐색·설계만**. 데스크톱 앱 Code 탭, 이 PC, 작업 폴더 `D:\saero`로 연 세션, 모델 Fable 5.1 · ultracode). 사실 기준 10/06 10:00 KST · 운영 main 작업 폴더 HEAD **`eae71fc`** = origin/main(별도 clone 결과 같음) · 작업 트리 깨끗 · 파일별 마지막 커밋이 지시문과 전부 일치(report-structure.md 587026e · css-and-layout.md ea597d4 · compare.py 4e38b95 · validate.py e220079 · compute.py e220079 · SKILL.md c64adbe). 운영 작업 폴더 쓰기 0(git 은 `--no-optional-locks log/show/diff` 만) · 기존 코드·문서·config·data/·registry 변경 0 · 외부 쓰기 0(push·네이버 POST·배포 PUT 0, dry-run 포함 fetch_reports·exclusions·deploy·ingest·archive 실행 0, 키 파일·자격 증명 열지 않음). 구현은 사용자가 아래 "내가 고를 항목"을 고른 뒤 별도 회차.
추가할 기능: 사장님들이 리포트를 빨리 훑고 필요한 정보만 얻게 — (1) 글 설명을 줄인다(숫자와 결론 한 줄 중심) (2) 41일이 쌓여 세로로 길어진 03 "일별 광고비"·07 "실제 검색어 분석"을 짧게 보이게 (3) 같은 원인의 다른 자리(10번 나열·08 목록·01·06 차트 폭·01 인사이트 박스·06 카드)를 후보로. **사용자 결정 원문(2026-10-06)**: "지금 광고 보고서에 텍스트로 된 설명이 너무 많아 … 필요한 정보만 딱딱 전달이 됐으면 좋겠어" · "2개의 섹터의 데이터가 세로로 너무 길게 나열이 되어있어서 이걸 수정했으면 싶어" — 레이아웃 변경은 SKILL.md "가장 중요한 원칙"(18~25행, 레이아웃 임의 재해석 금지·배포본이 유일한 원본)에 닿으므로 이 두 문장을 사용자 결정으로 남긴다(적을 자리는 3절 공통 뼈대).
방법: 별도 clone `D:\saero\feat-20261006-readable`(브랜치 같은 이름, `git clone -c core.autocrlf=false`)에 운영 `work/`의 index.html(md5 6aaa2472)·prev.html(95c58082)·compute.json(f60152d9)·combined/ CSV 4개를 복사하고 임시 폴더의 5단계 교체 코드 apply.py(702de83d)·n1006.py(754921d7)를 clone `work/`로 옮겨 두었다(사라질 수 있는 스크래치 보존 — E2 자리). 조사 2(글 기능 분류·코드 의존 목록 / 배포 경로·리허설·높이 실측) → 설계 1 → 독립 반박 2(코드·검사 / 화면·원칙·완결성)를 워크플로 에이전트 5개로 돌리고 조정자가 핵심을 재실측했다. 실행은 전부 clone `work/r*`·`work/D/` 사본(compute·compare·validate·overflow·precheck·mutation_test — 프로브 약 30종, playwright 는 file:// 만 · 밖 요청 route.abort).
효율: 벽시계 약 2시간(10:00 시작 확인 → 10:14~11:36 워크플로 → 기록) · 도구 호출 조정자 약 45회 + 하위 에이전트 228회 · 즉석 코드 약 700행(전부 스크래치 — 측정·프로브·높이·검사 사본 패치, 저장소 0행).
표기: [실측] 이번에 파일·명령으로 확인 / [실측·기록] 저장소 기록 원문 / [추론] 확인 못 함. 행 번호는 eae71fc 파일 기준, index.html 행은 10/6 배포본(f7bc605) 사본 기준.

## 0. 시작 확인과 환경 실측 [실측]

| 항목 | 값 |
|---|---|
| 저장소 | 운영 main `eae71fc` = origin/main, 작업 트리 깨끗. clone 브랜치 `feat-20261006-readable`(이 절 커밋 1개, push 0) |
| work/ 사본 md5 | index 6aaa2472 · prev 95c58082 · compute.json f60152d9 · 검색어 e3a352a2 · 상세지역 e70e5023 · 시간대별 faac5a0a · 키워드 b7d91858 · apply.py 702de83d · n1006.py 754921d7 — 시작·끝 같음(운영 회차 돌지 않음) |
| 10/6 배포본 기준 검사 | `precheck.sh work/r0/index.html work/combined work/r0/prev.html` exit 0 — validate 22/22 · compute(prev 기준) 경쟁사 40행(신규 변형 후보 ['노원부티필라테스']) · compare OK 95/DIFF 0 · overflow 360/390/430 넘침 0 · 도장. `mutation_test` "전부 살아 있음"([OK] 43 · UNCOVERED 0). 지금 배포본을 직전 배포본으로 넣으면(`--competitors-html work/r0/index.html`) 경쟁사 40행·후보 [] |
| 글자 수(표 제외 — 섹션 HTML → `<table>` 제거 → 태그 제거 → 공백 정규화) | 01 2,045 · 02 49 · 03 91 · 04 1,341 · 05 48 · 06 794 · 07 5,416 · 08 1,642 · 09 487 · 10 993 · 11 2,208 · 12 1,291(액션 표 td 본문 1,529 별도) — 합 **16,405**(지시문 16,500 과 공백 처리 차이). 내역: **매 회차 n<날짜>.py 가 다시 쓰는 서술 ≈ 11,650** · apply.py 기계 자리 ≈ 2,790(KPI·순위 5칸·카드 머리글·07 목록 2·08 목록) · 고정 글 ≈ 1,280(+제목 180) · **이번 회차에 안 바뀐 채 남은 서술 644**(1절 (c)) |
| 마크업 수 | HTML 123,360B · 2,340줄 · 인라인 `style="` 123 · `class="note"` 16(07 에 4: L1044·L1292·L1310·L1657) · `line-height:1.9;">` **3곳**(L1283 클릭1 · L1289 클릭0 · L1750 08 목록) · wrapper `class="wide-table"` 8 · `class="scroll-x"` 3 · `·<wbr>` 58(10번 두 줄 × 29) · `<details` 0 |
| 행·항목 수 | **03 tbody 42행**(날짜 41 = 8/26~10/5 오름차순 + 합계 — 지시문 메모의 "44" 는 thead 2행 포함 수, "41일 행 + 합계" 가 맞음) · 07 정식표 24 · 클릭1 35 · 클릭0(노출 5회 이상) 77 · 경쟁사표 40(config 이름 밖 어순 변형 4행 포함) · 08 TOP10 밖 39 · 10번 나열 30 · 01·06 min-width 3,280(41×80) · labels 41×2 · 06 카드 2(8/31 36일차 · 9/2 34일차) |
| 높이(playwright, Chart.js 미로드, `work/r*/heights.json`) | **390×844: 문서 18,001px = 21.3장** / 1280×900: 13,431 = 14.9장. 07 **5,294**(29%)/4,420 · 03 1,334/1,659 · 01 1,522 · 11 1,632 · 08 1,211 · 12 1,030 · 06 1,019 · 10 983. 07 안: 정식표 819 · 클릭1 428 · 클릭0 618 · 각주 4개 36+481+214+695 · 우측 카드 433 · 경쟁사표 1,347 · 경쟁사 각주 695. 03 표 한 행 28px(1280 에선 37) |
| 파이썬·도구 | venv `D:\saero\.venv`(3.12.10, pandas·playwright) · `PYTHONUTF8=1` 매 호출 · 검증 폴더 `D:\saero-verify` 존재(옛 사본·검증 보고 4개) |

## 1. 지금 상태

### (a) 구역마다 글이 하는 일 [실측 — 블록 93개 문장 단위 분류, 전문은 저장소 밖 전문 파일 조사 A 1절]

| 구역 | 글(표 제외) | 결론 | 근거 숫자 | 판정·등록 기록·이력 되풀이 | 해석 | 표 설명·고정 | 비고 |
|---|---|---|---|---|---|---|---|
| 01 | 2,045 | desc 1줄·해석 블록 머리 | 표 5행·순위 5칸·note 3개의 대부분 | 해석 블록 s04 178자("2026.09.19·09.20 사장님 확인"·"09.21 회차 완료 건") | 순위 각주 127자("~어려워 보임") | 소제목 2 | **L272·L273 머리글 2줄 512자는 10/6 에 안 바뀜**(prev 동일, n1006.py 교체 0) — report-structure.md 01 박스 구성(①표 ②순위 ③해석)에 없는 추가물 |
| 02·03·05 | 49·91·48 | desc | desc | — | — | — | 전부 compare 가 읽는 한 줄 |
| 04 | 1,341 | desc·note-mint 머리 | note-mint 54%·note 67% | note-mint s04 189자·note s04 52자(사장님 결정 날짜) · 그룹별 누적 서술 4문장(04 표가 이미 보여 줌) | note 126자(단정 금지 규칙) | ※ 163 고정 | compare 는 desc `→ N배`·note `비중은 A → B%` 두 곳만 |
| 06 | 794 | → 1줄(25회차 연속) | 카드 note 2개 ≈ 400 | 카드 note "승격 조건 … 카드로 유지" | — | 머리글·라벨 | 카드 note 는 compare 미독 |
| 07 | 5,416 | desc 28 | 목록 2 = 1,792(기계) · 각주 ② s02·s04 290 · ④ s03·s04 ≈ 220 | **각주 4 + 우측 note = 3,186자 중 판정 이력·등록 기록 되풀이 ≈ 1,664(31%)** — ② s05~s10 등록 날짜별 나열·판정(663+127), ④ s07~s19 과거 판정 전문(657+), ③ s02 "2026.09.12 결정", ✓ L1307 132자(날짜 박힌 고정문, 10/6 에 안 바뀜) | ④ s05 67 · ⚠️ 63 | 머리글·범례·note ① 76 | compare 가 읽는 서술은 ③ 자리(클릭 0 전체 N개·N회 · 행 단위 확장 3일)와 desc 뿐 — ①②(판정 한 줄·등록 n/verified n/실패 n·재노출)는 사람 몫 |
| 08 | 1,642 | note-mint s06 176(전국 유지·재상정 조건) | note-mint 499 · note 각주 | "2026.09.20 사장님 확인" | — | sub-head·"TOP 10 + 위 목록으로 전부 표시" | compare 가 note·note-mint 에서 9항목 읽음 |
| 09 | 487 | 톤 문장 67 | 콜아웃 253 | — | — | 각주 N회 | 콜아웃 한 문장이 어순·구두점까지 compare 리터럴 |
| 10 | 993 | note-mint 101·조치 판단 92 | 나열 237·일수 | "2026.09.20 접수·09.24 결정" 98 | — | sub-head | compare 가 나열 30개·일수·파트너 마지막날 읽음 |
| 11 | 2,208 | li 10개(항목당 100~440자) | 괄호 근거 | li6(② 되풀이 193) · li7(① 되풀이) · (참고)1(③ 되풀이) | — | 판정 줄 284 | validate 19~21·compare 금칙어·판정 줄 |
| 12 | 1,291(+td 1,529) | td 상태 줄 | — | **td1 1,084자 중 등록 기록·판정 85%**(날짜별 등록 개수 나열 436) · note 705 중 경쟁사 되풀이 36% | — | desc·집계 기준 480·footer 54 | validate 20·21 범위(집계 기준·footer 포함) |

같은 사실이 반복되는 자리(글자): 토브필라테스 경쟁사 아님 ≈ 398(6곳) · 10/6 등록 10개 ≈ 728(4곳) · 9/20~10/4 등록분 재노출 0 ≈ 771(5곳) · 플레이스 일예산 상향 유지 ≈ 919(4곳) · 상계동 카드 유지 ≈ 446(4곳) · 경쟁사 과거 판정 ≈ 729(2곳). compare 95항목 중 **서술을 정규식으로 읽는 것 43**(01 6 · 02 1 · 03 1 · 04 2 · 05 1 · 06 2 · 07 4 · 08 10 · 09 6 · 10 5 · 11 1 · masthead·og·KPI sub 4) — 나머지 서술(01 desc·L272·L273·L338 · 04 note-mint · 06 note 2 · 07 ③④ · 10 note-mint · 11 본문 숫자 · 12 전체 · 집계 기준)은 어느 검사도 읽지 않는다.

**(c) 10/6 배포본에서 실제로 난 것 [실측 grep]**: `10/4(일) 노출 200회·클릭 7건`(01 L272) index 1 · prev 2 · n1006.py 0 / `9/6부터 10/4까지 29일`(01 L273) 1·1·0 / `"상계동필라테스"(8/31), "노원산전필라테스"(9/2)는 후보`(07 ✓ L1307) 1·1·0 — masthead 는 10/5 까지인데 01 머리글이 "10/4(일)…29일" 인 채 validate 22/22 · compare 95/0 · precheck 통과 · 자동 PUT. compare 가 읽는 자리는 요란하게 막히고(10/6 기록 "서술 형식 3곳 DIFF") 안 읽는 자리는 조용히 빠진다 → 6절 막음 M1.

### (b) 배포본 HTML 을 읽는 코드가 기대는 문구·마크업·행 순서 — 구역별 [실측, 전문은 조사 A 2절]

전역: `reportlib.section(html,N)` = `<!-- Section N:` ~ `<!-- Section N+1:`(없으면 그 뒤 첫 `<script>` — 12 는 집계 기준·footer 포함) · validate 1 `check_tags` 는 `div table tr td th thead tbody ul li span script style` **12종만**(details·summary·b·br·wbr 안 셈) · 11 `<!-- Section 1~12:` 존재 · 10 `labels:[…]` 중 전부 `'M/D(요일)'` 꼴인 배열 길이 = 일수 · 9 config `date_based_sections`(01·06) 안 `min-width:\s*(\d+)px` · 12 `노출 합계는 ([\d,]+)회로 상단 KPI\(([\d,]+)회\)와 (\d+)회 차이` 전체 findall · 6 `집계 기간<b>([^<]+)</b>` · 7 `<div class="label">…</div>\s*<div class="value">…<span class="unit">` · compare `chart_data` = `getElementById('<id>')` ~ 다음 `new Chart` 안 `label:\s*'<이름>'\s*,\s*data:\s*\[…\]` · KPI sub 는 문서 전체 `<div class="sub">` 순서 [0][1][3] · overflow_check = 360·390·430 에서 `document.documentElement.scrollWidth ≤ 폭`(file:// 밖 차단 — 세로·접힘은 안 봄) · 가로 안내 스크립트(L2279~2338) = `.wide-table, .scroll-x` 에 load·resize 때만 `scrollWidth > clientWidth+4` 면 앞에 `.scroll-hint` + `.scroll-fade` 래퍼. **앵커는 전부 첫 일치**(`find`·`grp`·`index`) — 같은 문구를 앞쪽에 복제하면 조용히 다른 곳을 읽는다.

| 구역 | compare cmp 항목 이름(행 순서 대조 = **굵게**, 집합+정렬 = ⟨⟩) | validate 함수 · 정규식 | compute · apply.py 기준점 · mutation 표지 |
|---|---|---|---|
| 전역 | masthead · og:description · KPI 노출/클릭/CTR/광고비 · **KPI sub 일평균노출/일평균클릭/클릭당** · 01/06 labels | check_masthead · parse_kpi_tiles · check_chart_width · check_date_labels · check_section_comments · check_diff_footnotes · check_tags | apply `once()`(assert n==1) masthead·og·KPI 4+sub 3·min-width 2곳(`min-width:\s*\d+px;">(\s*<canvas id="(?:dailyChart\|rankChart)"` assert count==2)·차트 9·labels 2 / mutation `집계 기간<b>`·`<div class="label">`·`회로 상단 KPI(`·라벨 `'M/D(요일)'`·Section 5/11/12 주석 |
| 01 | 01 dailyChart 노출·총비용 · 01 min-width · **01 표 5일** · 01 표 .ctr-high · **01 플레이스 순위 5칸** · 01 순위 민트 칸 · 01 검색지면 CTR · 01 검색지면 노출·클릭 · 01 상향후 평균 · 01 상향전 평균 · 01 누적 가중순위 · 01 콘텐츠 누적 노출 | parse_ctr_cells `<td class="num([^"]*)">([\d.]+)%</td>`(섹션 전체) · min-width | compare 서술 regex: `검색 지면만 계산하면 <b>([\d.]+)%</b>\(노출 ([\d,]+)·클릭 (\d+)\)` · `하루 평균은 ([\d,]+)원·클릭 ([\d.]+)건·CPC ([\d,]+)원으로, 상향 전 9/1~9/16\(하루 평균 …\)`(리터럴 '9/1~9/16') · `누적 가중평균은 [\d.]+ → ([\d.]+)위` · `콘텐츠 노출 ([\d,]+)회` · 순위 5칸 `margin-bottom:2px;">([^<]+)</div>\s*<div style="font-size:15px;font-weight:800;(color:var\(--mint-dark\);)?">([\d.]+)위` / apply tbody 앵커 `① 일별 지표` · grid 리터럴 ~ `\n      </div>\n      <div class="note">닷새` / mutation 01 첫 `class="num ctr-high"` · min-width |
| 02 | 02 desc 플레이스 비중 `예산의 ([\d.]+)%` · 02 groupChart 노출/클릭 · 02 costPie | — | apply chart·`광고비 비중 (총 N원)` |
| 03 | **03 일별 표 전체 행**(`rows(sec(3))` 중 첫 칸≠'합계' 전부 == compute `03.rows` 오름차순 — **DOM 전체 `<tr>` 순서**) · 03 합계 행(위치 무관) · 03 desc 최고일 `최고치 (\S+) ([\d,]+)원` | **없음** | compute `03.rows` 오름차순 / apply L67~72 `<!-- Section 3` 뒤 **첫 `<tbody>` 통째**를 오름차순 41행 + 합계(`style="font-weight:800;"`)로 매 회차 새로 생성 / mutation 03 변조 없음 |
| 04 | **04 표**(유형·그룹·9칸) · 04 CPC 격차 desc `→ ([\d.]+)배`(섹션 첫 일치 = desc) · 04 파워링크 비중 `비중은 [\d.]+ → ([\d.]+)%` | parse_04_rows(`<tr>` 안 `<td class="num[^"]*">` ≥7 & cells[5] 가 `%`) · check_budget_share · check_cards_vs_04 | apply `<!-- Section 4` 첫 tbody + 앞 2칸(유형 뱃지·이름 메모) 직전 행 복사(새 그룹이면 KeyError) / mutation 04 첫 `\d+\.\d%` · `<td class="num` |
| 05 | **05 mediaChart top5 라벨/값/색** · 05 deviceChart · 05 desc 모바일 비중 `모바일이 노출의 ([\d.]+)%` | check_media_top5(`getElementById('mediaChart')` 뒤 3000자 `labels:\s*\[(.*?)\],\n`·`label:\s*'노출수'…data`·`backgroundColor`) | mutation `mediaChart` id · data 첫 값 |
| 06 | 06 rankChart · 06 min-width · 06 desc 노원역 순위 `평균 ([\d.]+)위` · **06 직접 등록 · 06 자동매칭**(`rows(s6)[0]·[1]`) · 06 마지막날 직접/자동 `직접 (\d+)·자동 (\d+)회` · 06 카드(그룹·등록일·일차·큰숫자) · 06 카드 큰 숫자 = 04 셀 | check_cards_vs_04 `color:var\(--ink-soft\);">(\S+) <span style="color:var\(--mint-dark\);font-weight:700;">\(([\d/]+) 등록, (\d+)일차\)</span></div>.*?font-weight:800;color:var\(--mint-dark\);">([\d.]+)위`(0건 → FAIL "config 로 끄는 설계 필요") | apply `직접 등록 키워드<br>`·`자동매칭( - )<br>` 뒤 4칸 regex · 카드 regex / mutation ` 등록, ` · `font-weight:800;color:var(--mint-dark);">N위` |
| 07 | **07 정식표 행수 · 07 정식표 값**(범위 `s7[:find("클릭 1건 검색어")]`, regex `name-cell → tag → num → num → num( ctr-high)?% → N원 → N원`) · ⟨07 클릭1건 목록(집합)⟩ · 07 클릭1건 노출 내림차순 · ⟨07 클릭0 목록(집합)⟩ · 07 클릭0 목록 노출 내림차순 · 07 클릭0 전체 각주 `클릭 0인 검색어 전체는 (\d+)개·노출 ([\d,]+)회` · 07 확장·클릭0 행단위 3일 · 07 확장·클릭0 마지막날 개수 `행 단위 확장·클릭 0 노출은 (\S+) (\d+)회 → (\S+) (\d+)회 → (\S+) <b>(\d+)회</b>\((\d+)개` · ⟨07 경쟁사표(집합)⟩ · 07 경쟁사표 정렬 · 07 desc 상위2 비중 `클릭의 (\d+)% 차지` · 07 클릭 합계(정식+1건+경쟁사) — 목록 2개는 앵커 `클릭 1건 검색어`·`노출은 있으나 클릭 0건인` 뒤 **첫 `line-height:1\.9;">(.*?)</div>`** → ` · ` split → `(.+?)\((\d+)회/([\d,]+)원\)` / `(.+?)\((\d+)회\)` · 경쟁사표 `s7[find("경쟁사 브랜드명 검색어"):]` 안 `name-cell → <td>[^<]*</td> → tag → num → num → N원` | parse_main_rows(s7 전체) · click1_items(앵커 뒤 첫 `line-height:1\.9;">(.*?)</div>` — **click0_items 는 정의만, 호출 0**) · competitor_rows(`find("경쟁사 브랜드명")` — 첫 일치는 각주 ② L1293 문장, 결과 같음) · check_competitors(16 순방향·17 값) · check_11_12 의 notes7 `<(?:p\|div)[^>]*class="note"[^>]*>(.*?)</(?:p\|div)>`(리터럴 `class="note"`, 07 에 ≥1 아니면 21 FAIL) | **compute `deployed_competitors`(66~70행)** `section(html,7)` → `find("경쟁사 브랜드명 검색어")` 뒤 `<td class="name-cell">([^<]+)</td>\s*<td>[^<]*</td>\s*<td><span class="tag` — **못 찾으면 오류 없이 빈 목록** / apply `<!-- Section 7` 첫 tbody · `listblock`(앵커 → 첫 `line-height:1.9;">` → 첫 `</div>`, 동률은 옛 목록 순서 `keep_order`) · tbody 앵커 **`경쟁사 브랜드명 검색어</div>`**(닫는 태그까지) + 소재구·매칭 직전 행 복사 + 신규 변형 `노원구`·`확장` 고정값 / mutation 정식표 1행 클릭·ctr-high·`class="name-cell"` ×2·`경쟁사 브랜드명` 뒤 첫 num |
| 08 | **08 TOP10** · 08 컴팩트 개수·클릭 `\((\d+)개 지역·클릭 (\d+)건\)` · ⟨08 컴팩트 목록(집합, 지역명 축약)⟩ · 08 컴팩트 정렬 · 08 클릭0 각주 `클릭 0인 (\d+)개 지역에서 노출 ([\d,]+)회` · 08 각주 N회 · 08 노원 비중 `노원구 단독으로 전체 노출의 (\d+)%·클릭의 (\d+)%` · 08 desc 타겟 비중 `노출 비중 (\d+)%·클릭 (\d+)%` · 08 확인불가 `확인불가"는 노출 …·클릭 …·비용 …원.*?비용 비중이 [\d.]+% → <b>([\d.]+)%</b>, CTR은 [\d.]+% → ([\d.]+)%` · 08 타겟 밖 서울 · 08 타겟 CTR `타겟 밖 서울\(노출 …·클릭 …\)의 CTR …%는 타겟 5개 구\(…%\)` · 08 서울·경기 밖 비용% `비용 비중 5%는 [\d.]+ → ([\d.]+)%` · 08 11위 `11위 (\S+)는 .*?(\d+)회·(\d+)건이 돼` — 목록은 `TOP 10 외` 뒤 첫 `line-height:1\.9;">` → `(.+?)\(노출(\d+)·클릭(\d+)\)`, `short()` 축약 | check_diff_footnotes | apply `<!-- Section 8` 첫 tbody · listblock `TOP 10 외` · once `\(\d+개 지역·클릭 \d+건\)` / mutation `(와 )(\d+)(회 차이)` 전체 첫 일치 |
| 09 | 09 hourlyChart 노출/클릭 · 09 심야 콜아웃 `심야\(22시~09시\)에도 노출 ([\d,]+)회·클릭 (\d+)회\(전체 클릭의 (\d+)%\)·비용 ([\d,]+)원 발생. 노출 비중은 (\d+)%, 클릭 비중은 (\d+)%` · 09 심야 클릭% (괄호) · 09 최다 `최다 클릭 시간대는 (\d+)시 (\d+)회` · 09 2위 `2위는 (\d+)시 (\d+)회` · 09 desc 최다 `(\d+)시대 클릭 최다\((\d+)회` · 09 각주 N회 | check_diff_footnotes | apply chart |
| 10 | **10 A/B/C/D 표**(칸 [2][3][4]) · 10 placementChart 노출/클릭 · 10 9/6이후 노출 나열 · 10 9/6이후 클릭 나열 · 10 일수·하루평균클릭 `(\d+)일간 노출은 (.*?)회, 클릭은 (.*?)건으로 하루 평균 ([\d.]+)건`(`<wbr>` 제거 뒤 `·` split, 순서 포함) · 10 desc 콘텐츠 N일 연속 0·클릭 A `콘텐츠 지면 (\d+)일 연속 0회 — 클릭 (\d+)건 중 (\d+)건` · 10 파트너 마지막날 `— \d+/\d+는 (\d+)회`(섹션 첫 일치) | — | apply `<!-- Section 10` 첫 tbody 3칸 regex × 4행 순서 |
| 11·12 | 11 항목 수(본문 ≤8, 참고 ≤2) · 11·12 금칙어 '필요'·'시점'·'할 것'·'검토'·'주째' ×5 · 11 판정 줄 유지+뒤집힘+소멸 = 직전 항목 수 `지난 회차 11번 (\d+)개 항목 판정: 유지 (\d+) · 뒤집힘 (\d+) · 근거 소멸 (\d+)` | check_11_12: `<li>(.*?)</li>`(sec 11, `(참고)` 는 `x[:30]` 안) · 판정 줄 · 금칙어(sec 11+12 태그 제거) · 잔존 문구 5종(07 notes7 + 11·12) | n1006.py: 11 은 `<!-- Section 11` 뒤 `<ul>`~`</ul>` 통째 재생성 / mutation `<li><b>` 첫 일치 · `<td><span class="tag tag-mint">`(12 첫 일치) · `항목 판정: 유지` |

**n<날짜>.py 방식** [실측 ast: rep 27 · one 8 · 11 ul 재생성]: `rep(start,end,new)` = 옛 문단의 첫 20~50자(숫자 포함 리터럴, 예 `<div class="note">닷새 동안 3.13`) ~ 닫는 마크업(`</span>`·`\n      </div>`(들여쓰기 포함)·`<br><br>`·`</td>`·`<div class="note"`) 사이를 통째 교체, `assert count==1`. 03·07 표·목록·차트·KPI 는 안 건드림(apply 몫). 표지가 옛 숫자 문구라 매 회차 새로 쓰고, **교체를 빠뜨린 블록은 어느 검사도 못 본다**(위 (c)).

**프로브 결과(코드 읽기 예측 → 사본 실행) [실측, 전문은 조사 B 2d·설계 C 0.1]**: 03 역순 → compare `03 일별 표 전체 행` DIFF 1(배포 막힘) / 03·07 목록·경쟁사표를 세로 상자(`max-height;overflow:auto`)나 `<details>` 로 감쌈 → validate 22/22 · compare 95/0 · overflow 3폭 PASS · `deployed_competitors` 40행 · 옛 apply 멱등 — 즉 **현행 검사는 모양을 전혀 보지 않는다**(되돌아가도 못 잡음) / 07 `class="note"` 4 → 1 통과, 0 → validate 21 FAIL + compare 파싱 실패(OK 52 에서 멈춤) / 10 나열 문장 삭제 → compare 파싱 실패(OK 83 에서 멈춤, 이후 11항목 미대조) / 01 해석 문단 삭제 → OK 17 에서 멈춤(78항목 미대조 — compare 47~178행이 try 하나) / 경쟁사표 소제목을 "경쟁사 검색어 (40개)" 로 바꾸면 compute **36행 exit 0**(어순 변형 4행이 리포트에서 조용히 사라짐 — 신호는 `신규 변형 후보` 36개뿐) / `<details>` 짝이 틀려도 validate 1 통과(TAGS 밖) / `line-height:1.9;` 뒤에 속성을 덧붙이면 compare 파싱 실패 + validate 2 FAIL + apply ValueError(셋 동시).

## 2. 배포본까지 가는 길 [실측 code-tab.md 3절 · precheck.sh · deploy.py · apply.py]

흐름: 4 `deploy.py fetch --out work/prev.html && cp work/prev.html work/index.html`(작업본 = 직전 배포본 사본) → 5 교체(저장소 밖 apply.py + n<날짜>.py — E2 일곱 번째 재사용) → 6 precheck(md5 작업본≠prev → validate(작업본) → compute `--competitors-html prev.html` → compare(작업본) → overflow → 도장) → 7 `push --dry-run` → 남은 질문 0 이면 **묻지 않고 PUT** → `verify --ref`. deploy.py 는 도장 md5·`--base` md5 만 대조하고 모양은 보지 않는다(240~247·291~299행). **사람이 화면을 보는 단계는 없음**(배포 뒤 시크릿 창).

| 물음 | 답 |
|---|---|
| (a) 새 모양이 처음 들어가는 회차 | 경로 **C** "모양만 바꾸는 별도 배포 회차"(권장): 같은 합본 → 4 fetch(prev = 옛 모양) → 5a compute → **2-1 같음 → "다시 계산"** → 3 → 5-0a propose(`[주의] 빈 창`, pull 은 registry verified_at 갱신 → 8단계 커밋) → ⓐ 해당 0 이면 생략 → 5 `scripts/apply.py --layout`(옛→새 변환 + 값 교체, 숫자 변동 0) + n<날짜>.py(줄인 서술) → 6 precheck(3번째 = 옛 모양 prev — md5 다름 통과 · compute 가 옛 마크업 정규식으로 옛 prev 를 읽어 40행 = 정상) → 7. compare 가 **모양 변경만** 검증하고 데이터 회차와 분리된다. 경로 A(다음 데이터 회차에 같은 날 병합·적용)는 같은 코드로 2-1 "다름" 으로 들어가는 점만 다르며, 새 compare 가 먼저 main 에 들어가고 첫 적용이 늦으면 그 사이 데이터 회차가 precheck FAIL 로 막히므로 **병합·첫 적용 한 묶음**. 경로 B(구현 회차가 새 모양 index.html 을 미리 만들어 둠)는 그 사이 회차의 서술이 빠져 "배포본이 유일한 원본" 위배 → 제외 |
| (b) 그 뒤 회차 · apply.py(E2) | 새 모양은 앵커가 바뀌어 apply.py 새 판이 필연 → **이번에 `scripts/apply.py` 로 들인다**(E2, last-audit 2022행 정의는 "행 고정 자리만"인데 현행 스크래치 판은 07 가변 구간·08 컴팩트까지 — 정의를 현행대로 고침). `--layout`: `<meta name="report-layout">` 가 없거나 옛 값이면 변환, 이미 새 값이면 건너뜀(멱등 — r12·r14 applied md5 = 작업본 [실측]). 기준점(현행 → 새 판): `once`·`tbody(after)`(앵커 뒤 첫 tbody) · masthead·og·KPI · min-width 2 · chart/labels · 01 `① 일별 지표`+grid 리터럴+`닷새` · 03(역순·합계 위 / B 는 tbody 둘 — 둘째 앵커 `<summary`) · 04 · 06 · 07 정식표(`<!-- Section 7` 첫 tbody — 앞에 다른 table 금지) · 07 목록 `listblock`(앵커·`line-height:1.9;">` 그대로, summary 가 머리글이어도 됨 [실측]) · 07 경쟁사표 `경쟁사 브랜드명 검색어</div>` 리터럴(머리글 div 는 텍스트만, 행 수는 summary 에) + `NEWC` 고정값은 config `competitor_defaults` 로 · 08 · 10 · **summary 개수·날짜(새 기계 자리, 6절 M2)**. 시험 `tests/test_apply.py` + fixture `tests/fixtures/layout_old.html`(Section 3·7 발췌, 숫자·검색어 실명은 가짜 — 공개 저장소). n<날짜>.py 는 방식 그대로 쓰되 표지를 주석 표지로(6절 M1) |
| (c) 옛 모양으로 조용히 되돌아가지 않음 | 성립 조건: 4단계 fetch+cp 매 회차 실행 · 5단계가 wrapper·순서·각주 수를 안 건드림 · **validate/compare 가 새 모양을 요구**. 지금은 셋째가 없다 — 옛 사본으로 통째 교체·세션의 "복원" 은 validate 22/22·compare 95/0 로 통과(r2·r4·r5·r6·r12·r14 전부 [실측]). 지키는 것(설계·D 사본 [실측]): ① validate **23 "레이아웃 판 = config report_layout"** — `<meta name="report-layout" content="…">` = config `layout_id` + 표지 수(`<details` 5 / `vbox`) 불일치·0건 FAIL(옛 모양 r0 → FAIL · details→div 복원 → FAIL · config 값 바꾸면 FAIL = config 를 읽음) ② **24 "07 각주 세 자리"**(①②③ 정규식 0건 FAIL) ③ compare `03 일별 표 전체 행` 에 `[::-1]` — 역순을 요구하므로 옛 apply 가 오름차순으로 되돌리면 DIFF(양방향 [실측]) ④ `scripts/apply.py` 저장소화로 "옛 스크래치 재사용" 경로 자체 제거 ⑤ mutation_test UNCOVERED 규칙이 23·24 겨냥 변조를 강제(추가 전 exit 1 [실측]) ⑥ compute `deployed_competitors` 0행 → `[FAIL]` exit 1 ⑦ TAGS 에 details·summary |
| (d) 새 모양이 "직전 배포본"이 된 다음 회차의 deployed_competitors | 조건: Section 7 주석 · 문자열 "경쟁사 브랜드명 검색어" 가 표 앞에 그대로 · 각 행 앞 세 칸 = name-cell → `<td>소재구</td>` → `<td><span class="tag`. 상자·`<details>`(닫힘 포함)로 감싸도 **40행 그대로** [실측 r5·r5b·r12·b03 `--competitors-html <새 사본>` → 40행·후보 []]. 소제목 문구를 바꾸면 36행·exit 0(1절 프로브) → ⑥ 가드 |
| (e) 첫 공개 전 사용자 미리보기(390px·데스크톱) | 지금 흐름엔 자리가 없다. 둘 수 있는 곳: **(1) 구현·검증 회차 산출** — `work/R*/index.html` 새 모양 + playwright PNG 390×844·1280×900(차트는 빈 캔버스, 사본을 브라우저로 열면 차트까지) **(2) 첫 적용 회차를 "보류" 로 시작** → 6 도장까지 → PUT 없이 멈춤(code-tab.md 3절 77행·4절 101행) → `work/index.html` 확인 → "배포" → 7(도장은 작업본·prev 불변이면 유효, deploy.py 148~172행) — 문서 한 줄 필요("보류 뒤 같은 세션 재개 = 7단계부터") **(3) 코드 게이트(6절 M4)** — deploy.py 실제 push 에서 `--file`·`--base` 의 `<meta name="report-layout">` 가 다르면(한쪽 없음 포함) `--layout-change` 없이는 `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함`(dry-run 은 `[주의]`). 레이아웃 회차에만 걸려 2026-09-30 자동 배포 결정과 충돌 없음. (4) dry-run 뒤 확인 질문은 그 결정과 정면 충돌 → 사용자만 결정. (5) 배포 저장소에 preview.html PUT 은 외부 쓰기·공개 URL → 제외 |

## 3. 설계안(≤3, 반박 반영판 — 채택은 사용자)

### 3.0 공통 뼈대(세 안 모두)
- **글 줄이기 공통 규칙**: 숫자 한 줄 + 결론 한 줄. 날짜 박힌 판정·등록 **이력**("2026.09.xx 사장님 확인/결정/완료")은 리포트에서 빼고 정본 표로 — 경쟁사는 last-audit `## 경쟁사 판정 이력`(SKILL.md (1-1)), 제외 검색어는 `## 등록 제외 검색어 대조 목록`(회차별 요약 행), 예산·지역·매체 결정은 checklist [의도된 동작] 10. 리포트에는 **현재 상태 한 줄**("상향 유지 결론 그대로(재상정 조건 미달)"). **줄인 뒤에도 남는 자리**: "매번 함께 바꿔야 할 텍스트" 9항목(1·2·3·4·9 기계 / 5 09 콜아웃 / 6 11 날짜 문장 / 7 01 표·순위·해석 / 8 각주) · compare 가 읽는 서술 43 문구(1절 (b) 표 — A·B 는 **리터럴 그대로** 한 문장씩, 앞뒤 수식만 뺌) · validate 19~21 · 07 각주 ①②③ · 08·09 `※ … N회 차이` · 11 첫 항목 `<li><b>지난 회차 관찰이 뒤집힘 — …` + 판정 줄 · "~로 보임"(01 순위 각주·11 해석) · 09 긍정 톤 문장 · 12 이월 판정(철회 사유 한 줄은 "이월 판정" 줄에)·성공 판정 조건 note · 11 ≤8+(참고)≤2.
- **구역별 남길 것·뺄 것·옮길 곳·예상 글자 수**(현재 → 예상, 전부 10/6 값 예문 — 전문 파일 설계 C 1.1):

| 구역 | 남길 것(예문 또는 규칙) | 뺄 것 → 옮길 곳 | 현재 → 예상 |
|---|---|---|---|
| 01 | desc 그대로("10/5(월) 노출 219회·클릭 6건·CTR 2.74% — 나흘 연속 감소 뒤 반등, 누적 CTR 3.19 → 3.18%") · 표 5행 · 순위 5칸 · 순위 각주 "닷새 3.32 → 3.97 → 3.38 → 3.76 → 4.18위(10/5 가 8/27 이후 가장 낮음) · 누적 가중평균은 3.10 → 3.12위 · 순위와 클릭이 같은 방향이 아닌 날이 이어져 순위 하나로 설명하기는 어려워 보임" · 해석 "콘텐츠 지면 없는 날 30일 · 누적 CTR 3.18%. 검색 지면만 계산하면 <b>3.71%</b>(노출 10,476·클릭 389). 상향 뒤 하루 평균은 11,529원·클릭 7.9건·CPC 1,460원으로, 상향 전 9/1~9/16(하루 평균 9,658원·7.2건·CPC 1,344원)보다 클릭 0.7건 많아 상향 유지 결론 그대로(재상정 조건 미달). 콘텐츠 노출 1,746회는 9/6 이후 0." | **L272·L273 머리글 2줄 512자 통째**(구성 밖 추가물·10/6 미교체) · 하루 분해 서술 · 결정 날짜 → checklist 10 | 2,045 → ≈ 760 |
| 02·03·05 | 그대로 | — | 49·91·48 |
| 04 | desc · ※ 1문장 · note-mint "→ 파워링크 "노원역필라테스" CPC 374원 vs 플레이스 1,328원 — 격차 3.55 → 3.55배 그대로 · 예산의 91.7% 플레이스(지난 회차 91.6%)" · note "두 광고는 성격이 달라 CPC만으로 우열을 가리기 어려움(플레이스 = 매장명·지도 검색 / 파워링크 = 저렴하지만 클릭 절대량 83건). 파워링크 10/5 노출 81회·클릭 1건·319원, 비중은 8.4 → 8.3%. 예산은 현행 유지(사용자 결정)." | 격차 5회차 나열 · 상향 경위 · 그룹별 누적 4문장(04 표) · 결정 날짜 | 1,341 → ≈ 500 |
| 06 | desc · "→ 노출 1,237 대 2,447·클릭 23건 대 60건으로 자동매칭 우위 25회차 연속 — 10/5 직접 12·자동 69회" · 카드 note "36일차 · 순위 2.58위 그대로(10/5 2.78위) · 10/1~10/5 노출 13·18·10·7·5회·클릭 0 · 하루 30회 초과는 9/18 하루뿐 → 승격 조건(이틀) 절반, 카드 유지(12번 2). (노출·클릭·비용은 04번 표 참고)" | 누적 클릭 날짜 나열 · 하루 평균 변화 | 794 → ≈ 440 |
| 07 | desc · 머리글·범례·note ① · 목록 2(기계) · **각주 ①②③ 한 블록**(아래) · 우측 카드 머리글·태그·note 2문장("확장매칭·인접 지역 검색으로 이미 클릭이 발생 중인 검색어들(관찰용 — 추가 등록 안 함, 사용자 결정). "필라테스"(91건)·"노원역필라테스"(83건)가 전체 389건의 45%(지난 회차 45%) · 경쟁사명 검색 클릭은 비교 검토 유입일 수 있어 참고만(아래 표)") · 경쟁사 머리글 · 경쟁사 각주 2문장("경쟁사·타 스튜디오 브랜드명으로 추정되는 검색어(노원·도봉구 인근 실제 업체 확인분). 젠필라테스 119회가 가장 크고 표 안 경쟁사는 대부분 클릭 0·비용 0원 — 채택·제외·종결 이력은 스킬 기록(경쟁사 판정 이력 표)에 둠.") | ✓ 줄(132, 날짜 박힌 고정문) · ⚠️(note 에 합침) · ② 등록 날짜별 나열·판정 이력 · ④ 과거 판정 전문 657자+ → 경쟁사 판정 이력 표·대조 목록 | 5,416 → ≈ 2,680(서술 ≈ 890) |
| 08 | desc · sub-head·목록(기계) · note "이 외 클릭 0인 150개 지역에서 노출 1,255회 발생. TOP 10 + 위 목록으로 전체 클릭 389건이 모두 표시됨. ※ 노출 합계는 12,228회로 상단 KPI(12,222회)와 6회 차이 …" · note-mint = compare 6문장(노원구 단독으로 전체 노출의 46%·클릭의 48% / 타겟 … CTR / "확인불가"는 노출 642·클릭 32·비용 40,569원 — 비용 비중이 8.7% → <b>9.1%</b>, CTR은 4.76% → 4.98% / 타겟 밖 서울(노출 1,742·클릭 69)의 CTR 3.96%는 타겟 5개 구(2.99%) / 비용 비중 5%는 3.2 → 3.2% / 11위 의정부시는 162회·5건이 돼 …) + "전국 설정 유지 — 재상정 조건 미달" | TOP10 순위 이동 서술 · 결정 날짜 | 1,642 → ≈ 1,200(서술 ≈ 525) |
| 09 | desc · 콜아웃 = 심야 compare 문장 + "최다 클릭 시간대는 15시 32회(22회차 연속), 2위는 9시 29회로 13시·20시와 같음" + 긍정 톤 1문장 · 각주 | 하루 분해 · 지난 회차 괄호 | 487 → ≈ 370 |
| 10 | desc · sub-head · note-mint · note "9/6 매체 설정 변경 뒤 콘텐츠 지면 30일 연속 0회(누적 1,746회에서 정지). 30일간 노출은 216·…·219회, 클릭은 10·…·6건으로 하루 평균 9.6건(41일 평균 9.5건). 클릭당 과금이라 예산 절감이 아니라 지표를 실제 성과에 맞춘 것. 파트너 매체(다음·네이트·Bing)는 "해제"인데도 누적 172회·클릭 2건 — 10/5는 1회(고객센터 답변 전까지 추적 안 함)." | 22회차 연속 서술 · 10/1~10/5 재나열 · 접수·결정 날짜 | 993 → ≈ 620(A, 나열 유지) / ≈ 390(B·C, 7일+평균) |
| 11 | ≤8 + (참고) ≤2, **항목당 굵은 결론 1문장 + 근거 괄호**(80자 안팎) · 판정 줄 1문장 | 둘째·셋째 문장 · "변화 없음" 은 값 나열만 | 2,208 → ≈ 860 |
| 12 | desc · td1 = 상태 줄(굵게, ② 와 같은 값) + "다음 회차 판정" note 1줄 · td2 = 상태 줄 + 판정 note · 아래 note = 정렬·이월 판정(철회 사유 자리)·신규 없음·경쟁사 각 1줄 · 집계 기준 5항목 각 1문장 · footer | 등록 날짜별 개수 나열(436) · 판정 되풀이 · 확장·클릭0 하루 서술 → 대조 목록 | 1,291(+td 1,529) → ≈ 610(+td ≈ 440) |
| 합 | | | **16,405 → ≈ 8,200**(그중 기계 목록 2,469) |

- **07 각주 ①②③ 예문**(`class="note"` 한 블록, 세 줄 `<br>` — r12·b03 에 넣어 compare OK 95 · validate 24/24 [실측]): `① 경쟁사 판정(10/6): "토브필라테스"는 사장님 확인으로 경쟁사 아님 — 클릭 1건 목록에 둠 · 부티필라테스 변형 "노원부티필라테스" 행 추가(표 40행).` / `② 제외 검색어: 10/6 등록 10개 · 확인 30/30 · 실패 0(10/7부터 판정) · 10/5 등록 10개는 10/6부터 판정 · 9/20~10/4 등록분은 10/5까지 재노출 0.` / `③ 클릭 0인 검색어 전체는 743개·노출 2,236회(경쟁사 포함 · 지난 회차 720개·2,179회) · 행 단위 확장·클릭 0 노출은 10/3 45회 → 10/4 31회 → 10/5 <b>68회</b>(36개 검색어).` ①의 자리는 (1-1) "07 경쟁사표 각주" 관행에 맞춰 **경쟁사표 아래 각주 첫 줄**로 두고 ②③ 은 클릭0 목록 아래(이월 F4 — 또는 (1-1) 문구 개정), 11 (참고) 한 줄·12 note 한 줄 유지(세 곳 각 한 줄). ② 는 code-tab.md 3절 5 "등록 n·verified n·실패 n" + exclusion-ui.md 6절 재노출 판정 — 재노출·누락·"등록은 나중에"·부분 실패(a/b) 회차의 고정 문구를 exclusion-ui.md 9절에 함께 정한다(이월 F5). ① 에 하루 수치("10/5 경쟁사명 검색 23회·클릭 0")는 compute 키가 없어 **넣지 않는다**(M2) — 넣으려면 `07.경쟁사마지막날` 키 + compare 항목 신설.
- **첫 적용 회차 경로 = C(모양만 바꾸는 별도 배포 회차)** + 미리보기 (2) "보류" 시작 + (3) deploy.py 레이아웃 게이트(2절).
- **apply.py = `scripts/apply.py` 로 저장소화(E2)** + `tests/test_apply.py`(2절 (b)).
- **옛 모양 복귀 가드** = validate 23·24 · compare 03 역순 · compute 0행 FAIL · TAGS +2 · overflow 가 details 를 전부 열고 재기(`pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")`) · mutation 변조 2 + 0건 가드 1(2절 (c)).
- **서술 자리 표지(M1, 필수)**: compare 가 안 읽는 서술 블록마다 `<!-- n:<자리> -->…<!-- /n -->` 주석 표지(≈30자리 — `<!-- Section` 으로 시작하지 않아 reportlib.section·mutation section()·validate 11 과 충돌 0, check_tags 는 주석 미집계 [추론 L47~55·L231~233]) + `scripts/narrative_check.py <작업본> <직전 배포본>`: 표지 블록이 직전 배포본과 바이트 동일하면 `[FAIL] 서술 미교체 <자리>` exit 1 — precheck.sh 에 한 줄(도장 없음). n<날짜>.py 는 `rep('01-desc', 새 문장)` 한 줄이 된다(표지 재작성 0). 주석이 공개 배포본에 실리는 점(무해)만 문서에.
- **compare 공통 개선**: 47~178행 try 하나 → 구역별 try(첫 파싱 실패 뒤 항목 생략 방지 — r9 OK 17 에서 멈춤). 글 줄이기 첫 회차에 regex 43 이 한꺼번에 닿으므로 같은 회차에.
- **사용자 결정 자리**: report-structure.md 2~4행 아래 "레이아웃 판 r2026-10(사용자 결정 2026-10-06)" 절에 **원문 두 문장 인용** + SKILL.md 18~25행에 "레이아웃 판은 설계 회차·사용자 결정으로만" 1문장 + checklist [의도된 동작] 27(원문 인용) + [되돌리면 안 되는 것] 3행(validate 23·24 / apply 03 순서 / 07 각주 세 자리) + code-tab.md 4절 "보류 뒤 같은 세션 재개 = 7단계부터".

### 3.1 설계안 비교

| | **A 최소 변경형** — 글 줄임 + 최신 위 + 세로 상자 | **B 접기형** — 글 줄임 + 최근 N일 펼침·나머지 `<details>` | **C 숫자 줄·결론 줄 분리형** — B + facts 블록(기계) + 상단 세 줄 |
|---|---|---|---|
| 핵심 | 3.0 그대로 · 03 역순(합계 맨 위) · `.wide-table` 자체에 `class="wide-table vbox" style="max-height:320px"`(sticky thead) · 07 클릭1·클릭0 목록 바깥 `.vbox` 160px · 경쟁사표 `.wide-table vbox` 360px · 08 목록 `.vbox` 160px · 10 나열 유지 | 3.0 그대로 · 03 = 표 B(합계 + 최근 7일 최신 위) + `<details>` "이전 34일(8/26~9/28) 펼치기"(표 A 34행 역순, DOM 전체 역순) · 07 클릭1·클릭0 블록 `<details><summary>클릭 1건 검색어 (35개)…` · 경쟁사표 머리글 div 그대로 + `<details>` · 08 목록 details(sub-head → summary) · 10 나열 → 최근 7일 + 30일 평균 | B 의 접기 + compare 가 읽는 서술 43 을 `.facts` 숫자 줄(apply 가 compute.json 으로 생성)로 분리, 사람은 결론 줄만 · 03 주별 소계 6행 + details 일별 · `<!-- Section 1:` 앞 "이번 회차 세 줄" 카드(11 첫 3항목 복제) · 11 자리 유지(위로 올리면 reportlib.section 이 1~10 을 삼킴) |
| 화면 예시 | `<div class="wide-table vbox" style="max-height:320px;"><table><thead>…(sticky)</thead><tbody><tr style="font-weight:800;"><td class="name-cell">합계</td>…</tr><tr><td class="name-cell">10/5(월)</td>…</tr>…8/26(수)</tbody></table></div>` · 목록: `<div class="vbox" style="max-height:160px;"><div style="…line-height:1.9;">스포츠(54회/1,215원) · …</div></div>` | `<div class="wide-table"><table>…<tbody>합계·10/5~9/29</tbody></table></div><details class="fold"><summary>이전 34일(8/26~9/28) 펼치기</summary><div class="wide-table"><table>…<tbody>9/28…8/26</tbody></table></div></details>` · `<details><summary>클릭 1건 검색어 <span>(35개 · 펼치기)</span></summary><div style="…line-height:1.9;">…</div></details>` · 경쟁사: 머리글 div "경쟁사 브랜드명 검색어" + `<details><summary>표 40행 · 펼치기</summary><div class="wide-table">표</div></details>` | B + `<div class="facts">누적 CTR 3.18%(지난 회차 3.19%) · 검색 지면만 계산하면 <b>3.71%</b>(노출 10,476·클릭 389) · …</div>` + desc 결론 1줄 |
| 390×844 높이(장) [실측 기반 추론] | ≈ 11,000 = **13장**(21.3 → 13) — r11 03 459 · r14 07 3,582−각주 ≈ 2,400 | ≈ 10,100 = **12장** — r12 07 1,737 · r3 03 438 · b03(글 미축소 뼈대) 13,169 = 15.6장(열림 20.1장) | ≈ 9,900 = 11.7장(+상단 198) |
| 1280×900 | ≈ 8,000 = 8.9장(14.9 → ) | ≈ 7,200 = 8.0장 | ≈ 7,000 = 7.8장 |
| 글자 수(표 제외) | ≈ 8,200 | ≈ 8,000 | ≈ 7,600(+상단 150) |
| 바뀌는 문서 절 | SKILL.md 18~25(1문장) · 240~258(5단계 명령 `scripts/apply.py --layout` + narrative_check) · 260~283(검사 24·narrative) · 469~484(7 항목에 "머리글 2줄 없음") · 486~535(23·24 줄) · 536~(apply) / report-structure.md 2~4 아래 "레이아웃 판" 절(원문 인용) · 66~87(01 머리글 제거) · 107~120(03 최신 위·합계 위·`.vbox` — 115행 "마지막 행은 전체 합계" 개정) · 196~243(07 ①②③·목록 상자·이력은 last-audit) · 245~261(08) · 324~378(11 1~2문장) · 388~410(12) / css-and-layout.md 38~53(`.vbox`) · 70~81(상한 px) · 83~104 아래 "세로 상자 안내" · 버그 11("상자는 `.wide-table` 자신에 — 바깥 div 면 뱃지가 안으로 들어가 함께 스크롤, r2 실측") / code-tab.md 75행·4절 보류 재개 / checklist 27·[되돌리면 안 되는 것] 3행 / exclusion-ui.md 9절(② 형식) / last-audit 2022행 E2 현행화 | A 와 같고 + report-structure.md 107~120(03 두 표·`recent_days`·details) · 290~308(10 나열 → 7일+평균, 302행 개정) · css-and-layout.md "접기 안내"(`.fold`·toggle sync·beforeprint)·버그 12 · checklist 27 은 r2026-10-B | B + report-structure.md 각 절 "정의(compute.py)" 옆 "facts 템플릿" 줄 · SKILL.md 469~484 의 5·7·8 기계화 · 486~535 "compare N항목" 갱신 · css `.facts` |
| 스크립트 함수 | compare `03 일별 표 전체 행` L81 `body[::-1]` · 구역별 try / validate `check_layout`(23)·`check_07_footnotes`(24)·TAGS+2·`click0_items` 호출(클릭0 목록 ≥1 가드) / compute `deployed_competitors` 0행 FAIL / `scripts/apply.py`(현행 146행 + `convert_layout` ≈ 30) / `scripts/narrative_check.py`(신설 ≈ 40) / precheck.sh +1 / deploy.py 레이아웃 게이트 + `--layout-change`(≈ 15) / mutation 변조 2·가드 1·config 실험 +1(`layout_id`) / overflow 0 / 배포본 CSS `.vbox{overflow:auto}`·sticky +4행, 안내 스크립트 `.vbox` 세로 뱃지 +12행 | A + compare 10 항목 3 새 regex(`최근 7일 노출은 (.*?)회, 클릭은 (.*?)건` · `9/6 이후 (\d+)일 하루 평균 ([\d.]+)건`) + **summary 개수 = 목록 길이 3항목(M2)** / apply 03 tbody 둘(`recent_days`, 둘째 앵커 `<summary`) + summary 개수·날짜 기계 생성 / overflow details 열기 +1 / 배포본 스크립트 details `toggle`→sync · `beforeprint/afterprint` +10 | B + `scripts/facts.py`(apply 만 import — **compare 는 독립 regex 유지, M3**) · compute `03.weeks` · compare `03 주별 소계`·tbody 단위 분리 · validate 25(상단 세 줄 = 11 첫 3 `<b>` 동일, 0건 FAIL) + 20·21 범위에 상단 블록 |
| config | `report_layout{layout_id:"r2026-10-A", vbox_px{03:320, 07_list:160, 07_competitors:360, 08_list:160}, markers{vbox_min:4 — 정규식 `class="(?:[^"]* )?vbox`}, notes07[3]}` · `competitor_defaults{district:"노원구", match:"확장"}` · (선택) `chart_min_width.per_day_px` 80 → 56 | `report_layout{layout_id:"r2026-10-B", recent_days:7, markers{details:5}, notes07}` + 위 둘 | B + `facts` 템플릿 키 목록 |
| 시험(역검증 포함) | ① r11+r14 합본 precheck(3번째 = r0/prev) 통과 ② 새 validate × 옛 모양 r0 → 23 FAIL ③ vbox 전부 제거 → 23 FAIL · ② 문구 변조 → 24 FAIL · 03 오름차순 복귀 → compare DIFF ④ mutation 전부 살아 있음 ⑤ test_apply: 옛 fixture → 변환 → 재변환 = 바이트 동일 ⑥ overflow 3폭 ⑦ heights 전후 ⑧ narrative_check: 한 블록 미교체 → FAIL · 전부 교체 → PASS ⑨ deploy 게이트 단위시험(meta 다름 → FAIL, `--layout-change` → 통과, 같음 → 통과) | A ①~⑨ + ⑩ details 전부 연 overflow 3폭 ⑪ details 짝 틀림 → validate 1 FAIL ⑫ 닫힌 details 열기 → 가로 뱃지(실기기 또는 playwright webkit — headless chromium 은 닫힌 채로도 붙음 [실측]) ⑬ 10 새 형식 OK + 옛 형식 DIFF ⑭ summary 개수 변조(35→36) → compare DIFF | B + ⑮ facts 기대 문장 fixture(`tests/fixtures/facts_expected.json`, 사람이 씀) vs `facts.write(compute.json)` 대조 ⑯ 상단 세 줄 ≠ 11 → 25 FAIL ⑰ 옛 서술 형식에 새 compare → DIFF |
| 리스크(한 줄씩) | **모바일 스크롤 갇힘·2축 제스처**(390 에서 `.vbox` 4곳 합 1,160px, 03·경쟁사표는 가로도 넘침 446 > 328 [실측]) · 세로 뱃지 규약 신설 · 데스크톱 세로 스크롤바 17px 만큼 가로 경계 이동 · 페이드 `::after` 가 세로 스크롤바 위를 덮음 | 닫힌 details 는 페이지 내 검색(iOS Safari)·인쇄·PDF 에 안 보임(beforeprint 로 열기, iOS 공유→PDF 는 [추론]) · 사장님이 펼쳐야 전체가 보임(클릭1 목록 기본 열림 선택지) · 03 두 tbody 규약 · summary 숫자는 기계 자리(M2) | 변경 폭 최대(compare 43항목 재작성 — "95항목" 기록 기준 전부 갱신) · 상단 카드는 section 밖(validate 25 필수) · 주별 소계는 새 표(report-structure 144~146 경고 — 기계 생성이라 불일치는 compare 로 닫힘) · 회차 둘로 나눌 것 |
| 메모 밖 후보 | 10 나열 유지 · 08 목록 vbox · 차트 폭 config 56(사용자 결정 — Chart.js 미로드라 라벨 겹침은 시크릿 창) · 01 박스 L272·L273 삭제(표·순위·해석 유지) · 06 카드 유지(note 1~2문장, [의도된 동작] 15) | 10 → 7일+평균 · 08 details · 나머지 A 와 같음 | 10 표 4행 보임 + 나열 details · 01 박스 = facts 2줄 + 표 + 순위 + 결론 1줄 · 06 카드 note = facts 1줄 |
| 첫 적용 회차 | 경로 C · 운영 세션 · precheck 3번째 = `work/prev.html`(옛 모양) · 통과 = validate 24/24 · compare OK 95(03 역순)/DIFF 0 · overflow 3폭 · narrative_check · 도장 · "보류" → 확인 → "배포"(게이트는 `--layout-change`) | 같음 · compare OK 98(10 항목 3 새 형식 + summary 3)/DIFF 0 | 같음 · compare 항목 수 바뀜 — 기록에 새 N |
| 작업량 [추론] | 코드 ≈ 350행(apply 175 · validate 40 · narrative_check 40 · deploy 15 · mutation 15 · compare 15 · compute 4 · config 10 · 배포본 CSS/JS 16 · test_apply 60 + fixture) · 문서 6개 ≈ 80행 | A + ≈ 60행 | B + ≈ 250행 |
| 반박 결과(6절) | 막음 0(① 하루 수치는 공통 M2 로 해결) · 이월 D4·F8·F9·F18 | 막음 1(D1 → M2 같이 반영) · 이월 D5·D8·F10·F11·F12 | 막음 2(D1 상속 + D2/F3 → M3) · 이월 D9/F13 |

조정자 의견(한 줄, 결정은 사용자): **B 접기형을 뼈대로** — r12 하나(각주 세 줄 + 목록·경쟁사표 접기)로 07 이 390 에서 5,294 → 1,737px 가 되고 현행 검사 전부·mutation·옛 apply 멱등·경쟁사 40행을 [실측]으로 통과했으며, A 의 2축 중첩 스크롤이 없다. 03 은 "최신 위" 가 01 표·순위 5칸(시간 오름차순)과 방향이 엇갈리므로(F9) 고를 항목 4 로 묻는다. C 는 한 회차 굳은 뒤 2회차 후보. 회차는 **둘로** — 회차 1 글(①②③·서술 표지·narrative_check·validate 24·apply 저장소화·compare 구역별 try) → 회차 2 모양(details·03·validate 23·deploy 게이트·summary·overflow) — 10/6 미교체 사고 유형(M1)을 먼저 닫고 모양은 미리보기와 함께 내보내기 위해서.

## 4. 완료 기준 표(이후 회차는 이 표로만 판정)

| 무엇 | 왜 | 어느 코드·시험이 지키나 |
|---|---|---|
| 누락 0 — 07 정식표 24·클릭1 35·클릭0(5회 이상) 77·경쟁사표 40·08 TOP10 밖 39 가 HTML 에 전부(접기·상자 안 포함) | 제약·SKILL.md 452~456 | compare 07 집합 4항목·08 컴팩트 2항목 · validate 2(클릭 합 = KPI) · 24(클릭0 목록 ≥1) |
| 숫자는 compute.json 재계산값만 — compare DIFF 0 · validate 전부 PASS · overflow 3폭 0 · 도장 | SKILL.md 240~283 | precheck.sh · deploy.py precheck_stamp |
| **summary·머리글의 개수·날짜(B·C)·① 하루 수치는 기계 자리이거나 리포트에 없음**(M2) | 첫 적용 다음 회차부터 35 → 36 이 조용히 틀림 | apply.py 가 compute.json 으로 생성 · compare "summary 개수 = 목록 길이" 3항목 · ① 에 compute 키 없는 숫자 0 |
| **서술 표지 블록 중 직전 배포본과 바이트 동일 0**(M1) | 10/6 01 L272·L273·07 ✓ 유형 | `scripts/narrative_check.py`(precheck.sh) · 시험 ⑧ |
| 07 각주 셋(경쟁사 판정 1줄 · 등록 n·확인 a/b·실패 n + 재노출 · 클릭 0 전체 N개·N회) 존재, 이력 전문은 last-audit 표 | 제약 · code-tab 75행 · exclusion-ui 6절 · [의도된 동작] 6 | validate 24(0건 FAIL) · mutation 변조 |
| 8·9 각주 · 뒤집힌 결론 줄 · "~로 보임" · 심야 긍정 톤 · 9항목 자리 · 11·12 작성 기준 | SKILL.md 429~484 · report-structure 324~410 | validate 12·19·20·21 · 사람(서술 검증 — 3.0 "남는 자리" 체크) |
| 화면: 팔레트 밖 색 0 · `.ctr-high` 전용 · 제거된 장식 0 · 민트/잉크 · 버그 3·7·10 · `·<wbr>` · 단일 파일 · service-worker 불변 | css-and-layout.md | validate 4·5 · overflow 3폭(B·C 는 details 열고) · 검증 회차 grep(`#` 색 추가 0 · 표 `display:block` 0 · 외부 css/js 0) |
| `line-height:1.9;">` 기준점 셋 동시 유지 | 제약 | compare 3곳·validate click1_items·apply listblock — r12·r14 무변경 [실측] |
| 옛 모양으로 조용히 되돌아가지 않음 | 2절 (c) | validate 23(표지·표지 수) · compare 03 역순 · `scripts/apply.py`(옛 스크래치 경로 제거) · compute 0행 FAIL · TAGS+2 · mutation 변조 2·가드 1·config 실험(`layout_id`) |
| **첫 적용 회차에 사람이 화면을 본 뒤에만 PUT**(M4) | 자동 배포 + 모양 변경 | deploy.py 레이아웃 게이트(`--file`·`--base` meta 다르면 `--layout-change` 필수) + 단위시험 ⑨ · code-tab.md 4절 "보류 재개" 한 줄 |
| compare 가 첫 파싱 실패 뒤 항목을 생략하지 않음 | r9 OK 17 에서 멈춤 | compare 구역별 try · 시험: 01 해석 문단 삭제 → DIFF 가 01 항목만 |
| 세로 길이 390×844 ≤ 13장(A)/12장(B·C, **details 닫힘 기준·열림 값 병기**) · 데스크톱 ≤ 9장 / 글자 수(표 제외) ≤ 8,500(A·B)/8,000(C), 07 ≤ 2,800 | 사용자 요청 | `tests/heights_check.py`·글자 수 스크립트 — 관찰용(FAIL 아님, 숫자 기록) · validate 상한으로 둘지는 고를 항목 17 |
| 검증 세션 명령은 `D:\saero-verify\<clone>` 에서, 운영 폴더 읽기만 | 작업 알고리즘 1절 | 검증 지시문 |
| **실제 환경 리허설 한 줄**: clone 안에서만, 외부 쓰기 0 — 10/6 배포본 사본에 새 모양을 적용해 precheck.sh 전부 통과 + 새 모양을 직전 배포본(3번째 인자)으로 넣은 다음 회차 재현에서 경쟁사표 40행 그대로 + mutation_test 통과 + 교체 코드로 한 회차 갱신 재현 | 제약 | 아래 R0~R6 |

리허설 명령(구현 회차 끝 = 작업 clone / 검증 회차 = `D:\saero-verify\<clone>`, 매 호출 `export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1`):
```
# R0 40일 CSV(≤2026.10.04.)를 스크래치로 걸러 work/c40/ 에(pandas, archive.py 안 돌림) — 10/5 배포본 6829f71 = work/prev.html 이 그 짝
# R1 첫 적용(경로 C): prev = 10/6 배포본(옛 모양) · 같은 41일 CSV
mkdir -p work/R1 && cp work/index.html work/R1/prev.html && cp work/index.html work/R1/index.html
"$PY" scripts/compute.py work/combined --competitors-html work/R1/prev.html -o work/R1/compute.json              # 옛 모양 prev → 40행
"$PY" scripts/apply.py --layout --html work/R1/index.html --compute work/R1/compute.json && "$PY" work/R1/n1006b.py  # 변환 + 값(변동 0) + 줄인 서술
PY=$PY scripts/precheck.sh work/R1/index.html work/combined work/R1/prev.html                                       # validate 24/24 · compare DIFF 0 · 3폭 · narrative_check · 도장
"$PY" scripts/deploy.py push --file work/R1/index.html --base work/R1/prev.html --message x --dry-run              # 기대: [주의] 레이아웃 판이 바뀜(게이트) — PUT 0
# R2 다음 회차 재현(새 모양이 직전 배포본): 40일판을 새 모양으로 만들고 41일 데이터로 한 회차 갱신
mkdir -p work/R2 && cp work/prev.html work/R2/new40.html
"$PY" scripts/compute.py work/c40 --competitors-html work/R2/new40.html -o work/R2/c40.json                         # 39행
"$PY" scripts/apply.py --layout --html work/R2/new40.html --compute work/R2/c40.json && "$PY" work/R2/n1005b.py      # 새 모양 40일판
"$PY" scripts/compute.py work/combined --competitors-html work/R2/new40.html -o work/R2/compute.json                 # 기대: 39행 + 후보 ['노원부티필라테스']
cp work/R2/new40.html work/R2/index.html && "$PY" scripts/apply.py --layout --html work/R2/index.html --compute work/R2/compute.json && "$PY" work/R2/n1006b.py   # 변환 건너뜀(멱등) + 값
PY=$PY scripts/precheck.sh work/R2/index.html work/combined work/R2/new40.html                                      # 전부 통과 · 경쟁사표 40행 · 게이트 없음(meta 같음)
"$PY" scripts/compute.py work/combined --competitors-html work/R2/index.html -o work/R2/c_self.json                  # 40행 · 후보 []
# R3 "$PY" tests/mutation_test.py work/R2/index.html work/combined/{키워드,검색어,시간대별,상세지역}.csv              # 전부 살아 있음(변조 2·가드 1·config 실험 포함)
# R4 역검증: 새 validate × 옛 모양 work/index.html → 23·24 FAIL / vbox·details 제거·② 변조·03 복귀·경쟁사 소제목 변경(compute 0행 FAIL)·표지 블록 미교체(narrative FAIL)·summary 35→36(compare DIFF)
# R5 화면: overflow_check(details 열고) · heights · 뱃지 · PNG 390/1280 → 사용자 미리보기
# R6 끝 상태: git --no-optional-locks status --short 0줄(추적 파일은 브랜치 커밋만) · work/index.html·prev.html·compute.json md5 불변 · 외부 요청 0
```

## 5. 막음 기준
막음 기준 : 정상 흐름에서 조용히 틀린 외부 쓰기 · 데이터 손실 · 자격 증명 노출. 공개 배포본이 걸리므로 "실수 둘 이하"(작업 알고리즘 5절 예외). 회차 중에 넓히지 않는다.

## 6. 스스로 반박 — 독립 검토자 2(D 코드·검사·배포 경로 / E 사장님 화면·원칙·문서·완결성), 막음/같이/이월 · 언제 나나

**막음(설계 줄에 반영함)**

| # | 안 | 문제 | 언제 | 근거 | 반영 |
|---|---|---|---|---|---|
| M1 | 공통 | 서술 미교체가 조용히 배포되는 경로가 설계 뒤에도 남음 — n<날짜>.py 의 옛 숫자 리터럴 표지 + compare 가 안 읽는 서술 블록은 교체를 빠뜨려도 validate·compare·precheck 전부 통과 → 자동 PUT | 가끔(10/6 한 회차에 2곳 — 01 L272·L273 512자 · 07 ✓ L1307) | [실측] grep 1절 (c) · n1006.py assert 는 표지 중복만 · 10/6 기록 "읽는 자리는 DIFF 로 처음 알았음" | 3.0 서술 표지 **필수** + `narrative_check.py`(precheck) + 완료 기준 줄(같이 F2) |
| M2 | B·C(① 은 A 도) | summary 개수·날짜(`(35개 · 펼치기)`·`이전 34일(8/26~9/28)`)와 ① 하루 수치(`10/5 경쟁사명 검색 23회·클릭 0`)가 기계 자리도 검산 자리도 아님 — 옛 apply listblock 은 summary 를 안 건드리고 compare·validate 어느 것도 안 읽음 | 매일(첫 적용 다음 회차부터 36 → 35 로 남아 공개, 실수 0 으로 생기는 구조) | [실측 D4·D14] summary 35→36 변조 OK 95 · ① 수치 변조 24/24·OK 95 · compute 07 키에 하루 경쟁사 없음 | apply 가 summary 를 compute.json(`len(07.클릭1)`·`len(07.클릭0목록)`·`len(07.경쟁사표)`·`03.rows` 날짜)으로 쓰고 compare 에 "summary 개수 = 목록 길이" 3항목 · ① 에 compute 키 없는 숫자 0(넣으려면 `07.경쟁사마지막날` 키 + 항목) |
| M3 | C | `scripts/facts.py` 템플릿을 apply(쓰기)와 compare(읽기)가 공유하면 compare 가 동어반복 — 키 매핑 오류 1건이 매 회차 조용히 공개(checklist "값 계산 공유 금지 — 같은 오류를 두 번 통과" 와 같은 구도) | 매일(C 채택 시) | [추론] 설계 C 2.3 "compare 43 항목 → facts.read" · 시험 ⑫ "왕복 0 차이" 가 바로 그 동어반복 | compare 는 facts.py 를 import 하지 않고 독립 regex 유지 · 시험 ⑫ → 고정 기대 문장 fixture 대조(3.1 C 시험 ⑮) |
| M4 | 경로 | 첫 적용 회차의 사람 미리보기가 "사용자가 먼저 '보류'라고 말하는 것" 하나에 걸림 — 경로 C 흐름에서 질문 0 이면 도장 → dry-run → **자동 PUT**, deploy.py 는 모양을 안 봄, validate 24·compare·overflow 가 전부 통과해도 접힘 인쇄·중첩 스크롤·sticky 겹침은 어느 검사도 못 봄 | 가끔(첫 적용·이후 레이아웃 회차) | [실측 D11] b03 + 옛 prev 로 precheck exit 0 도장 — 멈추는 단계 없음 · deploy.py 240~247·291~299행 | deploy.py 실제 push 에 레이아웃 게이트(`--file`·`--base` 의 `<meta name="report-layout">` 다르면 `--layout-change` 없이는 `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함`, dry-run `[주의]`) + 단위시험 · "보류" 시작은 그대로 두되 코드가 뒤를 받침 · code-tab.md 4절 한 줄 |

**이월**(한 줄씩, 설계 줄에 넣지 않음 — 첫 실사용 뒤 한 번에): D4 [A] 검사 23 표지 `class="vbox"` ≥4 는 r11(`class="wide-table vbox"`)에서 0 — 정규식 `class="(?:[^"]* )?vbox` 로(가끔) · D5 [B] "닫힌 details 안 .wide-table 은 뱃지가 안 붙는다" 전제가 headless chromium 에서 재현 안 됨(닫힌 채 9개 붙음) — toggle sync 는 무해, 근거는 실기기/webkit 에서(여러 우연) · D6/F5 [공통] ② 형식이 "등록은 나중에"·부분 실패(a/b)·재노출·누락 회차 문구를 안 다룸 → exclusion-ui.md 9절에 고정 문구, validate 24 규칙 "b = 등록 × targets, a ≤ b"(가끔) · D7 [공통] 결론 줄 안 숫자(닷새 평균 3.72위 · 10/1~10/5 13·18·10·7·5회 · 11 괄호 근거)는 compute 에 없어 사람 몫 — "결론 줄은 숫자 0 또는 쓰는 숫자마다 compute 키" 규칙을 report-structure.md 에(매일, 오타 때만 드러남) · D8/F17 길이·글자 수 상한은 관찰용이라 완료 판정이 사람 눈에만 달림 → 고를 항목 17 · D9/F13 [C] 상단 세 줄은 section 밖 → validate 25 필수·mutation 변조(C 채택 시 매일) · D11 경로 C 의 pull verified_at 커밋(2절 (a) 에 반영) · fixture 실명 가짜화(반영) · D12 주석 표지 공개(무해, 문서에) · F4 ① 자리 vs (1-1) "경쟁사표 각주"(3.0 에 자리 못 박음 — 문구 개정 여부는 고를 항목 3) · F6 우측 note 예문의 "2026.09.12 결정" → "(사용자 결정)"(반영) · F7 원문 인용 자리(반영) · F8 [A] 모바일 스크롤 갇힘(390 에 `.vbox` 1,160px) → 모바일 주 화면이면 A 보다 B, A 면 `overscroll-behavior:contain` 과 상한 px config(매일) · F9 "최신 위" 방향 엇갈림(01 표 5행·순위 5칸·labels 전부 오름차순) → 고를 항목 4(매일) · F10 [B] 닫힌 details 와 페이지 내 검색(iOS Safari)·PDF → 고를 항목 5(가끔) · F11 [B] 03 두 tbody 교체는 둘째 앵커를 `<summary` 로 + test_apply 행 분배 검사(반영) · F14 보류 재개 문서 한 줄(반영) · F15 [넘길 때] 규칙·리허설 clone 경로(반영) · F16 메모 밖 후보를 "결정 필요 3(10 나열·차트 폭·03 합계 위) / 승인만 5(01 머리글 2줄·07 ✓·⚠️·12 날짜별 나열·06 note)" 로(반영, 고를 항목 6) · F18 `.vbox{overflow:auto}` 는 CSS 로(인라인은 max-height 만) · `.fold` 여백을 밀도표에 · 페이드 `::after` 가 세로 스크롤바 위를 덮음(여러 우연) · 조사 A: validate `click0_items` 정의만 있고 호출 0(24 에서 호출 — 반영) · compare `competitor_rows` 의 `find("경쟁사 브랜드명")` 첫 일치가 각주 문장(결과 같음, 무해) · 05 desc 가 n1006.py 없이 바뀜(손 편집 — 서술 표지로 흡수). '죽음' 부류(강제 종료·응답 잃음): 기존 공통 안전망(precheck 도장·deploy base 대조·재개 판정은 대상 상태)이 그대로 지킨다 — 시나리오별 추가 없음.

## 7. checklist·문서 충돌 표(풀려면 사용자 결정)

| 원문(짧게) | 이 기능과의 관계 | 사용자가 정할 것 |
|---|---|---|
| SKILL.md 18~25 "레이아웃·CSS·섹션 순서·디자인 요소를 임의로 재해석하면 … 깨진다" · report-structure.md 3~4 "섹션 순서·구조는 임의로 바꾸지 않는다" | 글 줄이기는 "문구" 범위 안(허용). 03·07·08 모양(상자·details·역순·합계 위)·세로 뱃지·facts 블록·상단 카드는 레이아웃 재해석 | **원문 두 문장 인용 + 레이아웃 판 절 승인**(고를 항목 14) |
| report-structure.md 115 "마지막 행은 전체 합계, 굵게" | A·B 합계 맨 위 · C 주별 소계 | 고를 항목 4 |
| report-structure.md 302 "표 아래 'N일간 노출 나열'은 9/6 이후 날짜" · compare 10 리터럴 | B·C 7일 + 평균 | 고를 항목 6 |
| css-and-layout.md 버그 8 `per_day_px` 80 근거(라벨 겹침) · [의도된 동작] 17(Chart.js 미로드) | 56 으로 줄이면 겹침은 시크릿 창에서만 보임 | 고를 항목 6 |
| css-and-layout.md 83~104 가로 스크롤 안내 "가로만" · 38~41 유틸리티 원칙 | 세로 상자·접기 규약 신설 · `.vbox`·`.fold` 클래스 | 고를 항목 5·14 |
| SKILL.md (1-1) "07 경쟁사표 각주 · 11 (참고) · 12 액션 세 곳 관행" | ① 한 줄을 세 곳에 각 한 줄로 유지(3.0) — 자리는 경쟁사표 각주 첫 줄 | 고를 항목 3 |
| [의도된 동작] 15 상계동 카드 유지 · report-structure.md 184~188 06 카드 · 231~233 07 우측 카드 · 66~78 01 박스 구성 · exclusion-ui.md 9절 "회차별 요약 행만" | 카드 유지·note 축소 · ✓·⚠️·01 머리글 2줄·12 날짜별 나열 삭제는 문서와 같은 방향(충돌 0) | 승인만(고를 항목 2) |
| SKILL.md 7단계 자동 배포(2026-09-30 결정) · code-tab.md 4절 ⓐ | 레이아웃 회차 한정 게이트(M4)는 데이터 회차엔 안 걸림 — 충돌 없음 · dry-run 뒤 질문(2절 (e)4)은 충돌 | 고를 항목 9 |
| checklist 16 "validate 22개" · compare "95항목" 기록 기준 | 24개 · 95+3(B) 또는 재작성(C) | 고를 항목 12·15 |
| last-audit 2022행 E2 정의 "행 고정 자리만 … 가변 구간·문장은 사람" | 현행 apply.py 는 07·08 가변 구간까지 — 정의를 현행대로 | 고를 항목 7 |

## 내가 고를 항목
1. **설계안**: A 최소 변경형(상자) / **B 접기형(details)** / C 숫자 줄·결론 줄 분리형 / 보류. (조정자 의견: B 뼈대, C 는 2회차 후보)
2. **구역별 남길 글**(3.0 표 승인 여부, 항목별 가·부): ① 01 머리글 2줄(L272·L273) 삭제 ② 07 ✓ 줄·⚠️ 삭제(04 표 메모·note 에 흡수) ③ 판정·등록 이력을 리포트에서 빼고 last-audit 표·대조 목록만(리포트엔 현재 상태 한 줄) ④ 11 항목당 결론 1문장 + 근거 괄호(80자 안팎) ⑤ 12 td1 날짜별 등록 개수 나열 삭제 ⑥ 04·06·08·09·10 예문대로(바꿀 자리가 있으면 그 구역 이름).
3. **07 각주 ①②③ 형식**(3.0 예문) 승인 · ① 자리 = 경쟁사표 각주 첫 줄(권장) / 클릭0 아래 ①②③ 한 블록((1-1) 문구 개정) · ① 을 11 (참고)·12 note 에도 각 한 줄 유지 / 07 한 곳만 · ② 에 "확인 30/30" 표기(verified 대신) · ① 에 하루 수치 넣지 않음(권장) / compute 키 신설.
4. **03 표 모양**: (가) 03 만 최신 위 + 합계 맨 위(권장) / (나) 01 표 5행·순위 5칸도 같이 최신 위 / (다) 오름차순 유지 + 합계만 위 / (라) 현행 — 그리고 A 상자 320px / B 최근 7일 + details / C 주별 소계 + details.
5. **07 표 모양**: 목록 2 = 상자 160px(A) / details(B·C) · 경쟁사표 = 상자 360px / details · details 기본 닫힘 승인(클릭 1건 목록만 기본 열림 선택지) · **사장님이 리포트를 인쇄·PDF·페이지 내 검색으로 쓰는지**(쓰면 iOS 에서 details 가 걸림 — A 상자 또는 beforeprint 열기) · **사장님 주 화면이 모바일인지**(A 의 2축 스크롤에 직결).
6. **메모 밖 후보** — 결정 필요 3: 10번 나열(유지 / 최근 7일 + 평균) · 01·06 차트 폭 `per_day_px` 80 → 56(또는 그대로) · 03 합계 맨 위 / 승인만 5: 01 머리글 2줄 삭제 · 07 ✓·⚠️ 삭제 · 12 날짜별 나열 삭제 · 06 카드 note 축소 · 08 TOP 10 밖 목록(상자 / 접기).
7. **apply.py 처리**: E2 — `scripts/apply.py` 저장소화 + `tests/test_apply.py` + fixture(실명 가짜)(권장) / 스크래치 유지(새 판만). last-audit 2022행 E2 정의 현행화.
8. **서술 자리 표지(M1)**: 주석 표지 `<!-- n:… -->` + `narrative_check.py`(precheck) — 막음이라 채택 권장 / 다른 가드 안.
9. **첫 공개 미리보기**: (1) 구현·검증 회차 PNG + 사본 열기 + (2) 첫 적용 회차 "보류" 시작 → 도장 → 확인 → "배포" + (3) deploy.py 레이아웃 게이트(M4, 권장 셋 다) / (4) dry-run 뒤 확인 질문(2026-09-30 결정과 충돌 — 사용자만 결정). 첫 적용 회차 첫 말 예문: "보류로 시작 — 6단계 도장까지만, 배포는 내가 말함".
10. **첫 적용 회차 범위**: 경로 C(모양만 바꾸는 별도 배포 회차, 2-1 "다시 계산", 권장) / 경로 A(다음 데이터 회차와 같은 날 병합·적용). 날짜(평일 아침 데이터 회차와 겹치지 않게).
11. **회차 분할**: 둘(회차 1 글 + 표지 + 24 + apply 저장소화 + compare try → 회차 2 모양 + 23 + 게이트 + summary, 권장) / 한 회차.
12. **가드 신설 승인**: validate 23(레이아웃 표지·표지 수)·24(07 각주 세 자리) · compute 경쟁사 0행 FAIL · TAGS details/summary · overflow 가 details 를 열고 재기 · mutation 변조 2·가드 1·config 실험 · deploy 게이트.
13. **config 새 값**: `report_layout{layout_id, recent_days 7, vbox_px{03 320·07_list 160·07_competitors 360·08_list 160}, markers, notes07}` · `competitor_defaults{노원구·확장}` · (선택) `per_day_px 56`.
14. **문서 개정 승인**: SKILL.md 18~25(1문장 + 원문 인용 자리)·240~258·260~283·469~484·486~535 / report-structure.md 2~4 아래 "레이아웃 판 r2026-10(사용자 결정 2026-10-06 — 원문 두 문장)" 절·01·03·07·08·10·11·12 / css-and-layout.md `.vbox`·`.fold`·세로/접기 안내·버그 11·12 / code-tab.md 75행·4절 보류 재개 / checklist [의도된 동작] 27(원문 인용)·[되돌리면 안 되는 것] 3행·16 "22개" → 24 / exclusion-ui.md 9절(② 형식·예외 회차 문구) / last-audit 2022행 E2.
15. **compare 공통 개선**: 구역별 try(첫 실패 뒤 생략 방지) 포함 / 제외 · "2026-09-27 95항목" 기록 기준 갱신 방식(B 98 / C 새 N).
16. **더 물을 것**: ① "필요한 정보"의 우선순위 — 03 에서 보고 싶은 것이 최근 며칠인지 주별인지 ② 경쟁사 각주 전문을 빼도 되는지(사장님이 리포트에서 이력을 읽어 왔는지) ③ 11번을 맨 위로 올리고 싶은지(복제 블록으로만 가능 — C 상단 카드) ④ 차트 폭 3,280px 가로 스크롤이 불편했는지.
17. 세로 길이·글자 수 상한을 validate 상한(FAIL)으로 둘지(config `report_layout.max_chars{07:2800,total:8500}`·`max_screens`) / 관찰용만.
18. 점검 회차로 넘길 것: 이월 목록(6절) · validate `click0_items` 미호출 · compare 첫 파싱 실패 생략(15 에서 안 고르면) · 05 desc 손 편집 경로.

**[넘길 때]** — 다음 세션에 붙일 글과 함께 단계의 모델·effort 를 같이 적는다(모델만 적지 않는다):

| 단계 | 세션·폴더 | 모델 · effort · 설정 |
|---|---|---|
| ③ 구현 | 작업 폴더 clone(`D:\saero\feat-20261006-readable` 이어 쓰거나 새 clone) · 끝에 리허설 R0~R6 | **Opus 5.5 · ultracode** |
| ④ 첫 검증 | **`D:\saero-verify` 새 세션**, 새 clone(운영 폴더 읽기만) | **Fable 5.1 · ultracode** / 수정 뒤 재검증은 새 세션 · 바뀐 것만 · **Fable 5.1 · xhigh** |
| ⑤ 수정(막음이 있을 때만) | 새 세션(③ 세션을 이어 쓰지 않음) | **Opus 5.5 · xhigh · ultracode 끔**(같은 결함으로 2번을 넘으면 Fable 로 올릴지는 사용자) |
| ⑥ 병합 | ④ 검증 세션에 이어서(갱신 회차가 돌지 않을 때, last-audit 맨 위는 main 쪽 회차 절을 살림) | — |
| 첫 실사용(첫 적용 회차) | 운영 세션 `/saero-run`, "보류" 시작 | **Opus 5.5 · high · ultracode 끔** |

## 마무리 기록(이번 회차)
- 커밋 = 이 절만(`audit/last-audit.md` 맨 위, 경로 지정 add, `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`, 전역 설정 변경 0). **push 0**(② 고르기 답을 이 세션에서 받은 뒤). 커밋 해시는 자기 참조라 적지 않는다.
- 전문(하위 에이전트 원문 A·B·C·D·E 부록 포함)은 저장소 밖 `D:\saero\saero-ad-report_리포트읽기쉽게_탐색_2026-10-06.md`. 프로브 사본·높이 JSON·검사 사본 패치는 clone `work/r0~r14·work/D/`(gitignore)와 스크래치에만.
- 운영 main 작업 폴더 HEAD `eae71fc` · `git status` 빈 것 · work/ md5 9개 시작과 같음 · 네이버·API·배포 저장소 요청 0 · 키 파일 0 · SKILL.md·scripts·config·tests·data·registry 변경 0. 임시 폴더 apply.py·n1006.py 는 clone `work/` 에 사본으로 보존(E2 자리).


## 사용자 결정(2026-10-06 — ② 고르기, 탐색 세션에서 받음)
"18개에 대해서 추천안대로 할꺼야" → 내가 고를 항목 1~18 전부 권장안. 권장을 적지 않았던 자리는 B 접기형 원안·안전한 기본값으로 두고 여기 밝힌다(바꾸려면 사용자 한마디).
- 1 **B 접기형** 뼈대(C 는 2회차 후보) · 2 ①~⑥ 전부 가(01 머리글 2줄 삭제 · 07 ✓·⚠️ 삭제 · 이력은 last-audit 표만, 리포트엔 현재 상태 한 줄 · 11 항목당 결론 1문장 + 근거 괄호 · 12 날짜별 나열 삭제 · 04·06·08·09·10 예문대로) · 3 ①②③ 형식 승인, ① 자리 = 경쟁사표 각주 첫 줄, 11 (참고)·12 note 에도 각 한 줄, "확인 a/b" 표기, ① 에 compute 키 없는 숫자 0 · 4 (가) 03 만 최신 위 + 합계 맨 위, B 최근 7일 + 접기 · 5 목록 2·경쟁사표 접기, 기본 닫힘(클릭 1건 목록도 닫힘 — B 원안, 기본 열림은 첫 실사용 뒤 판단), beforeprint/afterprint 열기 규약 포함, 인쇄·PDF·검색 사용 여부와 주 화면은 미확인(첫 실사용 뒤) · 6 10번 나열 → 최근 7일 + 30일 평균(B 설계) · 차트 폭 `per_day_px` 80 **그대로**(56 은 라벨 겹침을 검사로 못 보므로 첫 실사용 뒤 판단 — 이월) · 03 합계 위(4) · 승인만 5 전부 가 · 7 **E2 저장소화**(`scripts/apply.py` + `tests/test_apply.py` + 가짜 fixture, 2022행 E2 정의 현행화) · 8 **주석 표지 + `narrative_check.py`** · 9 (1) PNG + (2) "보류" 시작 + (3) deploy 레이아웃 게이트 셋 다, (4) 안 함 · 10 **경로 C**(별도 배포 회차, 2-1 "다시 계산"), 날짜는 평일 아침 데이터 회차 뒤 · 11 **둘로** — 회차 1 글(①②③·서술 표지·narrative_check·validate "07 각주 세 자리"·apply 저장소화·compare 구역별 try·10 나열 7일+평균·11·12 축소) → 회차 2 모양(details·03·validate "레이아웃 판"·deploy 게이트·summary 기계 자리·overflow details 열기·세로/접기 규약) — 각 회차가 구현 → 검증 → 병합 → 첫 적용(보류 시작)을 한 벌로 · 12 가드 전부 승인(회차 1: 07 각주 세 자리·click0_items 호출·TAGS details/summary(선반영 가능)·compute 경쟁사 0행 FAIL / 회차 2: 레이아웃 판·overflow·mutation·deploy 게이트) · 13 config 값 승인(`per_day_px` 는 제외) · 14 문서 개정 전부 승인(회차별로 해당 절만) · 15 compare 구역별 try 포함, 기록 기준은 "항목 수 N" 을 회차 기록에 적는 방식 · 16 더 물을 것 넷은 첫 실사용 뒤 — 기본값: 03 최근 7일 · 경쟁사 각주 전문 뺌 · 11 자리 유지 · 차트 폭 유지 · 17 길이·글자 수는 **관찰용만**(validate 상한 없음) · 18 점검 회차로.
- 다음 단계: ③ 구현(회차 1 글) 새 세션 **Opus 5.5 · ultracode** — 지시문은 탐색 세션이 이 블록 뒤에 만들어 준다. 이 블록만 추가 커밋(push 0).
- 지시문(탐색 세션이 작성, 2026-10-06): 저장소 밖 `D:\saero\saero-ad-report_리포트읽기쉽게_구현지시_회차1_2026-10-06.md` — 프롬프트 B 구현 양식, 사실 기준 = 이 브랜치 HEAD(기록 커밋 2 + 이 줄), 할 일 1~7(글 규칙 · 서술 표지 + narrative_check · validate "07 각주 세 자리" · apply 저장소화 · compare 구역별 try · 문서 · PNG), 리허설 R0~R6, [넘길 때] 모델·effort. 보내기 전 검토자 2(결정·막음 완결성 / 코드 대조)로 대조해 19건 반영 — 큰 것: 43 리터럴 유지와 10 항목 3 새 형식의 충돌을 예외로 명시 · 01 순위 5칸 끝 앵커를 표지 무관(`닷새` 텍스트 없이)으로 · 같은 기간 재배포(2-1 같음 경로)에 narrative_check 예외 · 시간대별.csv 는 일별 열이 없어 40일판은 archive.py 합산 방식으로 · R2 기대값은 "경쟁사 40행(후보 ['노원부티필라테스']) = 직전 39 + 신규 1". 마감(2026-10-06): 이 브랜치는 **로컬 clone 에만**(원격 브랜치 없음, push 는 구현 회차 끝에) · origin/main = `eae71fc` 그대로(다른 세션 기록 없음) · 운영 작업 폴더 main 깨끗.

---

## 수정 기록(2026-10-06 — 질문 다듬기 스킬 정본 사본, 문서만) · 브랜치 `fix-20261006`
**사용자 요청**(원문): "D:\stock\.claude\skills\prompt-polish\SKILL.md 를 참고해서 이 폴더(saero)용 질문 다듬기 스킬을 .claude\skills\prompt-polish 에 만들어줘. 사실 확인·규칙 대조는 이 폴더의 CLAUDE.md 와 saero-ad-report-skill/references/code-tab.md 기준으로." → 설치본 `D:\saero\.claude\skills\prompt-polish\`(세 파일) 작성 뒤 "local/ 에 정본 사본도 만들어줘". 스킬은 메모를 읽기만 하고 붙여 넣을 프롬프트 상자로 다듬는다(프로젝트 파일 쓰기 · 저장소 스크립트 실행 0 — 상세는 사본의 `이력.md`).
**변경 파일**(`57006ab` → 커밋 ① `c64adbe`, 코드 0; `wc -l` · md5 앞 8자리): **local/prompt-polish/SKILL.md 197 33fa63a1 · 유난히큼.md 53 3f31c298 · 이력.md 15 183ea3af**(새 파일 — 설치본과 md5 같음) · references/code-tab.md 0절 local/ 목록 235 → f344dd9f · SKILL.md 참고 문서 local/ 줄 561 → 464f2638 · audit/checklist.md 대상 목록 local/ 줄 507 → 44477fc7 · 이 절.
**확인**: 설치본 = 사본 md5 3/3 · 줄바꿈 i/lf w/lf · scripts/ · tests/ · data/ · config · registry 변경 0. 외부 쓰기 = 스킬 저장소 `fix-20261006` push만(배포 PUT 0 · 네이버 0). **검토 판정**: 막음 0(문서만 — 외부 쓰기 경로 무관). 이월 : 스킬의 받는 세션 모델 · effort(작음 Opus 5.5 · medium · 큼 Opus 5.5 · xhigh)와 워크플로 n 은 `D:\stock` 값을 빌린 것 — saero 사용자 결정 · 실측 전.
**병합**: 사용자 "병합해"(2026-10-06) → 분기 뒤 main 변경 0(origin/main = `57006ab`, fetch 확인) → `git merge --no-ff` 병합 커밋 **`99e8dc0`**(부모 57006ab · ea1544d, 충돌 0, 트리 = ea1544d) → 이 줄 기록 커밋 → main push → main 작업 폴더 `git pull --ff-only`. 설치본 `D:\saero\.claude\skills\prompt-polish\` = 사본(md5 3/3 같음 — 설치는 이번에 함께 됨). clone `D:\saero\fix-20261006`은 둔다.

---

## 갱신 회차 (2026-10-06 09:24~09:33 KST — Code 탭 `/saero-run`, main 작업 폴더) · **배포 완료 `f7bc605`**
상세 = 아래 "## 2026-10-06 갱신 회차" 절(대조 목록 표 아래). S0 PASS → ① 수집(`--prev 2026-10-05`, 10/1~10/5) → ingest `cb0a3b1`(41일) → 4 fetch(배포본 10/4·40일 `6829f71`) → 2-1 다름(40 → 41일) → 3 신규 0 → 5-0a pull·propose(창 10/5) → ⓐ 승인 한 번(토브 "아님"·"등록 승인 10개") → 등록 10 × 3그룹 verified 30/30 `9e67e66` → 5 교체(apply.py 재사용 + n1006.py) → 6 precheck(full — compare 형식 맞춤 2회 재실행) → 7 dry-run → 자동 배포 PUT `f7bc605` → `verify --ref` 1회째 일치.
- **다음 회차**: propose `--since 2026-10-06` · `--prev ~/saero-fetch/downloads/2026-10-06`. 10/5 등록 10개는 10/6부터, 10/6 등록 10개는 10/7부터 판정.
- **다음에 볼 것(후보)**: compare.py가 읽는 서술 형식 3곳(05 "모바일이 노출의 N%" · 08 "비용 비중 5%는 A → B%" · 09 "2위는 H시 N회" — 동률 셋이면 첫 시만)을 서술 스크립트가 안 건드려 precheck DIFF로 처음 알았음 — 서술 스크립트 체크리스트 또는 compare 정규식 완화 후보.

---

## 갱신 회차 (2026-10-05 23:32~23:50 KST — Code 탭 `/saero-run`, main 작업 폴더) · **배포 완료 `6829f71`**
상세 = 아래 "## 2026-10-05 갱신 회차" 절(대조 목록 표 아래). S0 PASS → ① 수집(`--prev 2026-10-04`, 10/1~10/4) → ingest `0e9ba66`(40일) → 4 fetch(배포본 9/30·36일 그대로 — **10/4 세션은 등록 22개까지만 하고 배포·기록 없이 끝났음**) → 2-1 다름(36 → 40일) → 3 신규 0 → 5-0a pull·propose(창 10/1~10/4) → ⓐ 승인 한 번(보람상가 "아님"·"등록 승인 10개") → 등록 10 × 3그룹 verified 30/30 `6567a47` → 5 교체 → **compare.py 171행 정규식 수정(`— 9/\d+는` → `— \d+/\d+는`, 마지막 날이 10월이면 사실대로 써도 파싱 실패)** → 6 precheck(full) → 7 dry-run → 자동 배포 PUT `6829f71` → `verify --ref` 1회째 일치.
- **다음 회차**: propose `--since 2026-10-05` · `--prev ~/saero-fetch/downloads/2026-10-05`. 10/4 등록 22개는 10/5부터, 10/5 등록 10개는 10/6부터 판정.
- **다음에 볼 것(후보)**: 세션이 등록 뒤 끊기면(10/4) 기록·배포가 빠진 채 남음 — 다음 회차 S0 뒤 "배포본 기간 < 보관본 끝"이면 알리는 한 줄 후보. compare.py의 날짜 고정 정규식(9월)은 이번 1곳뿐(grep).

---

## 갱신 회차 (2026-10-01 08:03~08:17 KST — Code 탭 `/saero-run`, main 작업 폴더, 월초) · **배포 완료 `4855509`**
상세 = 아래 "## 2026-10-01 갱신 회차" 절(대조 목록 표 아래). S0 PASS → ① 수집(`--prev` 생략·`--debug`, **`지난달` 프리셋 첫 실측 9/1~9/30 PASS**) → ingest `f931162`(9/1~9/29 값 불변, 9/30만 추가) → 2-1 다름(35 → 36일) → 3 신규 0 → 5-0a pull·propose(창 9/30) → ⓐ 승인 한 번(써니 채택·플로우·비비 아님·"등록 승인 9개") → config `7c02571` → propose 재실행(후보 9 불변) → 등록 9 × 3그룹 verified 27/27 `440c357` → 5 교체 → 6 precheck(full, compare 형식 맞춤 3회 재실행) → 7 dry-run → **자동 배포(배포 질문 없음 — 첫 실측, 자동 모드 판단기 거부 없음)** PUT `4855509` → `verify --ref` 1회째 일치.
- **다음 회차(10/2)**: `이번달` 프리셋이 10/1 하루만 받게 됨 — `data/2026-10` 새 폴더(`--prev ~/saero-fetch/downloads/2026-10-01`), propose `--since 2026-10-01`.
- **다음에 볼 것(후보)**: 서술 교체 스크립트(n1001.py)를 줄 번호 대신 원문 표지 찾기로 바꿈 — compare.py 파싱 형식("A → B위"·"비용 비중이 A% → <b>B%</b>, CTR은"·"11위 X는 … N회·M건이 돼"·"— 9/D는 N회")에 맞춰야 해 세 번 다시 돌림. 어순이 다른 경쟁사 변형(노원역정원필라테스)은 compute 집합(config 이름 포함 ∪ 직전 표) 밖이라 첫 회차엔 표에 못 넣음 — 이월 후보.

---

## 수정·병합 기록(2026-09-30 — 자동 배포: 배포 질문 폐지, 문서만) · 브랜치 `fix-20260930` → main
**사용자 결정**(2026-09-30 갱신 회차 배포 뒤, 원문): "제외검색어 및 기타 등등 나에게 물어봐야하는거 다 물어보면은 자동으로 배포까지해줘". → 7단계 "배포할까요? — 배포 / 보류" 고정 질문(2026-09-29 `fix-20260929`)을 **자동 배포**로 대체: 사람 질문(2-1 같음·승인 묶음 ⓐ·모호한 답 되묻기·등록 실패 재시도 등 code-tab.md 4절 ⓐ)에 모두 답을 받아 남은 것이 없고 6단계 precheck·7단계 dry-run이 통과하면 바로 PUT → `verify --ref`. 검사 FAIL·남은 질문·사용자 "보류"면 PUT 0.
**변경 파일**(`8c8630e` → 커밋 ①, 코드 0): SKILL.md 7단계 문단·"승인이 필요한 지점" 배포 단락 · references/code-tab.md 3절 7단계 행(명령·멈춤 칸)·4절 ⓐ 배포 단락 · **local/saero-run/SKILL.md 31행 → md5 cbfc63c4**(설치본 `D:\saero\.claude\skills\saero-run\SKILL.md` 갱신 대상 — 사용자) · audit/checklist.md 26번·갱신 이력 · 이 절.
**확인**: 옛 문구 "배포할까요"는 "옛 규칙 … 대체" 설명 2곳과 checklist 26번 이력에만 남음(grep) · tests/·scripts/에 배포 질문 의존 0(grep) · test_exclusions 49 OK(registry md5 동일) · deploy.py는 원래 질문·답을 모름(가드 = precheck 도장·base 대조·권한 — 그대로). **검토 판정(막음/같이/이월)**: 막음 0(외부 쓰기 가드 코드 불변, 사람 확인 한 단계만 사용자 결정으로 뺌) · 이월 1 — 자동 배포는 문서 규칙이라 세션이 남은 질문을 놓치면 배포될 수 있음(코드 강제 예: `deploy.py push --require-no-pending` 같은 표지는 없음, 두 가지 이상 겹쳐야 남).
**병합**: 사용자 요청에 따른 바로 병합(`git merge --no-ff`, 분기 뒤 main 변경 0). 병합 뒤 main 작업 폴더 `git pull --ff-only`.
**결과(2026-10-01 마감 때 채움)**: 커밋 ① `307767b`(브랜치 `fix-20260930` push) → 병합 커밋 **`db3d791`**(부모 8c8630e · 307767b, 충돌 0) → main 작업 폴더 pull(`db3d791`, 작업 트리 깨끗). 설치본 `D:\saero\.claude\skills\saero-run\SKILL.md`를 사용자 지시("복사해")로 `local/saero-run/SKILL.md`로 교체 — md5 8f8c5908 → **cbfc63c4**(같음 확인). `D:\saero\CLAUDE.md` = `local/CLAUDE.md` af47cb28(변경 없음). clone `D:\saero\fix-20260930`은 둔다.
**경위(권한)**: 첫 병합 시도(커밋·push·merge 한 명령)는 Claude Code **자동 모드 판단기가 거부**(사람 확인 단계를 없애는 규칙 변경의 main 반영으로 보임) → 세션은 우회하지 않고 멈춰 보고 → 사용자가 권한 모드를 "수동"으로 바꿔 명령마다 "한 번만 허용" → 커밋·push·병합·pull 완료. 사용자 질문 "매일 수동/자동 반복해야 해?" → 아니오(이번 한 번), 다만 **자동 모드에서 사람 답 없는 첫 자동 배포 PUT을 판단기가 막을 수 있음 — 막히면 세션이 멈추고 사용자가 "배포" 한마디**(다음 회차 실측 대상).
**다음 회차(2026-10-01, 월초)**: `/saero-run` — `fetch_reports.py`(`--prev` 생략, `지난달` 프리셋 9/1~9/30 확정본, `--debug` 권장)로 `data/2026-09` 덮어쓰기, propose `--since 2026-09-30`, 배포는 새 규칙(자동). 볼 것: 자동 배포 PUT이 자동 모드에서 막히는지.

---
## 갱신 회차 (2026-09-30 07:49~08:34 KST — Code 탭 `/saero-run`, main 작업 폴더) · **배포 완료 `961789d`**
상세 = 아래 "## 2026-09-30 갱신 회차" 절(대조 목록 표 아래). S0 PASS → ① 수집(9/1~9/29) → ingest `87028d3` → 2-1 다름(34 → 35일) → 3 신규 0 → 5-0a pull·propose(창 9/29) → ⓐ 승인(경쟁사 시소·솔라 채택 → config `8ea8c14` → propose 재실행, 블루창동점 되물음 → "B") → 등록 10 × 3그룹 verified 30/30 `04e7205` → 5 교체 → 6 precheck 통과(full) → 7 dry-run → "배포" → PUT `961789d` → `verify --ref` 1회째 일치.
- **다음 회차(10/1)**: 매월 1일 — `fetch_reports.py`(`--prev` 생략, `지난달` 프리셋 9/1~9/30, `--debug` 권장 — `지난달` 첫 실측)로 `data/2026-09` 덮어쓰기, propose `--since 2026-09-30`.
- **다음에 볼 것(후보)**: apply.py(교체 기계 자리)가 네 회차째 재사용됨 — 이번엔 옛 스크래치에서 복사해 신규 경쟁사 행만 고침(E2 판단 근거 추가). 경쟁사 채택 전 제외 검색어로 등록된 이름(솔라필라테스상계주차)이 생김 — 채택 시 registry에 같은 이름이 registered면 알리는 한 줄 후보.

---
## 검증·병합 기록(2026-09-29 후속 — 첫 실사용 후속 3건: 검증(막음 0) → main 병합)

**검증**(`D:\saero-verify\saero-ad-report_검증_0929후속.md`, 별도 세션 — Code 탭·이 PC, 대상 `93026f5`(a944423 위 2커밋 af81b1b·93026f5), 하위 에이전트 0 — 조정자 직접 실행): 수정 기록 3항목(verify `--ref` · 배포 질문 고정 · 승인 답 예시) 전부 코드·시험·문서로 참 · checklist [되돌리면 안 되는 것] deploy·승인 목록·비출력 시험 행 여전히 참. 시험 49/17/10/15 OK rc 0 · mutation_test(무인증 재수령 7846ddf e869c1e8 + combine 34일) "전부 살아 있음" · 변이 7/7 잡힘(ref 무시·ref 형식 검사 제거·캐시 문구 제거·승인 숫자 예 제거·verify 밖 --ref 허용·커밋 7자만·후보 0에도 "그대로면") · `verify --ref` 실측(읽기) — `7846ddf…`(40자)·`7846ddf`(7자) 일치 rc 0, `32d8b05` 불일치 "커밋 고정 조회라 캐시 아님" rc 1, `--ref main`·`push --ref` GET 전 exit 2 · 배포 질문 문장 SKILL.md 2곳·code-tab.md 2곳·local·checklist 26 같은 뜻 · exclusion-ui 6절 승인 문구 인용 = `build_proposal` 출력(후보 0이면 "이 목록 그대로면" 없음 — 실측). **막음 0** → 병합.

**병합**: `fix-20260929`(`93026f5`)를 main(`a944423` — 분기 뒤 main 변경 0, `ls-remote` 확인)에 `git merge --no-ff` → 병합 커밋 **`d8fca3d`**(부모 a944423 · 93026f5, 트리 = 93026f5와 동일). 충돌 0. clone `D:\saero-verify\merge-0929`(`git clone -c core.autocrlf=false`). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`. 사용자 병합 지시(2026-09-29 10:1x KST, "막음 0이면 이어서 main에 병합한다") 뒤 병합. 브랜치 `fix-20260929`는 둔다. 코드·문서 재수정 없음(이 절만). 위 "수정 기록(2026-09-29 후속)"의 `main 미반영`은 당시 사실 — 이 절로 정정(**2026-09-29 main 반영**).

**병합 main에서 재실행** [실측] — venv, PYTHONUTF8 없이, `-W error::ResourceWarning`, test_deploy 격리 env: test_exclusions **49 OK**(1.1초, registry 6f58bf0c 전/후 동일) · test_deploy **17 OK**(33초) · test_ingest **10 OK**(69초, data/ 8파일 동일) · test_fetch_reports **15 OK** rc 0(81초) · py_compile 14/14 · `bash -n` 2 · combine PASS(2026.08.26.~09.28. 34일 · 10,352/326/372,749원) · mutation_test(재수령 배포본 7846ddf) rc 0 `[OK]` 43 · MISS/UNCOVERED/SKIP 0 · "전부 살아 있음" · data·config·registry 합 md5 병합 전후 `0a961bd7` 같음(registry 702행 6f58bf0c · config b826b388). 배포 저장소 HEAD `7846ddf` 그대로(PUT 0) · 네이버 0 · 실제 자격 증명 0 · main 작업 폴더 0.

**이월**(한 줄씩): `verify --ref`는 그 커밋의 본문만 본다(배포 저장소 HEAD·Pages 반영은 문서의 `ls-remote`) · 배포 질문 "배포"만 승인은 문서 규칙(코드 강제 없음) · 승인 답 모호 시 되묻기도 문서 규칙(코드 가드는 `--expect N`) · "다음에 볼 것" E2 교체용 즉석 코드(apply.py) 저장소에 두기.

**병합 뒤**: 설치본 `D:\saero\.claude\skills\saero-run\SKILL.md`를 `local/saero-run/SKILL.md`(31행 8f8c5908)로 갱신 + main 작업 폴더 `git pull --ff-only`(작업 폴더 세션 몫 — 이 병합 세션은 하지 않았다).
효율: 벽시계 약 25분(10:19 clone → 검증 → 10:3x 병합·push) · 도구 호출 약 15회 · 즉석 코드 약 30행(변이 7건 문자열 치환 — 스크래치).

---
## 수정 기록(2026-09-29 후속 — 첫 실사용 후속 작은 수정 3건) · 브랜치 `fix-20260929`, **main 미반영**
세션: 데스크톱 앱 Code 탭(이 PC), Opus 5.5. 기준 = 아래 "첫 실사용 회차" 절 "다음에 볼 것(후보)" + checklist v4.7 [되돌리면 안 되는 것]. clone `D:\saero\fix-20260929`(`git clone -c core.autocrlf=false`, `a944423` 위 커밋 2개: ① `af81b1b` 코드·시험·문서 ② 이 절·checklist — 자기 참조라 해시는 채팅 보고에).
외부 쓰기: 스킬 저장소 = `fix-20260929` push만 · 배포 저장소 = **무인증 읽기 GET 4회**(mutation_test용 fetch 1 + 새 `verify --ref` 실측 3) + `git ls-remote` 1 · PUT 0 · 네이버 0 · 실제 자격 증명 0 · main·main 작업 폴더·registry·data 변경 0 · `D:\saero` 설치 0(local/ 두 파일 중 saero-run만 바뀜 — 설치는 병합 뒤 사용자).
효율: 벽시계 약 25분(09:59 clone → 10:2x push KST) · 도구 호출 약 50회 · 즉석 코드: 변이 확인 러너 약 20행(스크래치 사본 — bash 함수 + 문자열 치환 파이썬).

**항목별**
1. **deploy verify 캐시**(09-29 실측 2회 — PUT 직후 ref 없는 contents GET이 옛 본문): `deploy.py` push 성공 줄 = `배포 완료 커밋 <전체 sha> · 파일 sha … ` + `다음(읽기): deploy.py verify --file <작업본> --ref <sha>` · `verify --ref <커밋>` → `get(token_file, url)`이 `…/contents/index.html?ref=<커밋>`(무인증 먼저, 403·429면 자격 증명 1회 — 종전 규칙 그대로) · `--ref`는 16진 7~40자(소문자로 바꿔 조회)·verify 전용 — 아니면 GET 전 exit 2(`[FAIL] --ref는 커밋 sha…`·`[FAIL] --ref는 verify에만`) · ref 404 = `[FAIL] ref …의 index.html을 찾지 못함` exit 1 · 불일치 문구 둘: ref 없이 = `[FAIL] 불일치 — PUT 직후라면 캐시일 수 있다: ls-remote HEAD와 --ref로 다시 verify(읽기). 재PUT 금지 (…)` + 확인 명령 줄, ref 조회 = `[FAIL] 불일치 — ref …의 본문이 로컬과 다름(커밋 고정 조회라 캐시 아님)…`. 요청의 `Cache-Control: no-cache` 주석을 실측대로 고침. 문서: code-tab.md 3절 7단계(push → `verify --ref <push가 찍은 커밋>`)·재개 판정(배포 = `verify --ref`)·4절 PUT 결과 모름·verify 불일치 행·5절 exit 1·2 / SKILL.md 7단계(명령·불일치 문단)·참고 목록 / local/saero-run 4항.
2. **배포 질문 고정**: 7단계 dry-run 결과를 보인 뒤 **"배포할까요? — 배포 / 보류(오늘 배포 안 함)"**, 답 "배포"일 때만 PUT — "마감"·다른 답은 배포 승인이 아니다(배포 없이 기록하고 끝냄, 배포 커밋 칸 `보류(사용자 답 "<원문>")`), 그 뒤 배포를 원하면 dry-run부터 다시 보이고 같은 질문. code-tab.md 3절 7단계 행·4절 ⓐ / SKILL.md 7단계·"승인이 필요한 지점"(묶음과 별개 단락) / local/saero-run 지키는 것. 문서 규칙(코드 강제 없음 — 아래 이월).
3. **승인 답 예시**: `build_proposal` 승인 문구 `답: "등록 승인 N개" — N은 숫자로 씁니다(예 "등록 승인 12개", 이 목록 그대로면 "등록 승인 <건수>개")`(후보 0이면 뒤 절 없음) + `N을 숫자로 쓰지 않았거나 "위 2가지만"처럼 둘 이상으로 읽히면 글자 그대로 읽은 dry-run 목록을 보이고 다시 묻습니다`. 문서: SKILL.md 5-0 3항 · code-tab.md 6절(새 항목 "답이 모호하면 되묻는다" — 09-29 실측 흐름) · exclusion-ui.md 6절 3항(인용 문구 = 코드) · local/saero-run.

**변경 파일**(`a944423` → `af81b1b`; `wc -l` · md5 앞 8자리) [실측]: scripts/deploy.py 314→338 9a5a7bee→6b72ed5e · scripts/exclusions.py 1355→1357 e3904e68→ee1e621c · tests/test_deploy.py 351→399 0d419c2e→9dd58641 · tests/test_exclusions.py 1099→1105 aed40d4b→336a4125 · SKILL.md 548→561 29b22c35→fabeb850 · references/code-tab.md 229→235 464fc9ad→0a0541bf · references/exclusion-ui.md 158→160 ee6033c8→fa554d87 · **local/saero-run/SKILL.md 28→31 7dd534c8→8f8c5908**(설치본 갱신 대상 — 병합 뒤 사용자) · local/CLAUDE.md 불변 af47cb28.

**실측** [실측] — venv `D:\saero\.venv`(Python 3.12.10), **PYTHONUTF8 없이**, `-W error::ResourceWarning`, test_deploy는 `GIT_CONFIG_NOSYSTEM=1`·`GIT_CONFIG_GLOBAL=/dev/null`·`GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`(격리 env — 시험 자체도 `GIT_*` 제거·가짜 도우미):
- `test_exclusions` **Ran 49 OK**(1초, 실제 registry md5 전/후 동일 6f58bf0c) · `test_deploy` **Ran 17 OK**(31초 — 15 + 새 2) · `test_ingest` **Ran 10 OK**(69초) · `test_fetch_reports` **Ran 15 OK**(106초). skip·ResourceWarning·Traceback 0. `compile` scripts 8·tests 6 = 14/14(pyc 안 씀) · config json · `bash -n` ingest.sh·precheck.sh.
- data·config·registry 합 md5 시험 전후 `0a961bd7` 같음 · 작업 트리 변경은 커밋 대상 8파일뿐.
- `tests/mutation_test.py <배포본 재수령(7846ddf, md5 e869c1e8, 2121행)> <합본 4종 — archive combine PASS 2026.08.26.~09.28. 34일 · 10,352/326/372,749원>` → rc 0 **"전부 살아 있음"** `[OK]` 43 · MISS/UNCOVERED/SKIP 0 · 원본 md5 전부 동일.
- 새 시험 변이 확인(스크래치 사본): deploy 7종(ref 무시·ref 형식 검사 제거·verify 밖 `--ref` 허용·커밋 7자만·ref 불일치에도 캐시 문구·캐시 문구 제거·소문자화 제거) + 승인 문구 3종(숫자 예 제거·후보 0에도 "그대로면"·모호 문장 제거) = **10/10 잡힘**.
- 실제 배포 저장소 읽기(무인증): `verify --file <재수령본> --ref 7846ddf…(40자)` 일치 rc 0 · `--ref 7846ddf`(7자) 일치 rc 0 · `--ref 32d8b05`(직전 배포) 파일 sha 1c52f70·md5 a3465ec0 → 불일치 "커밋 고정 조회라 캐시 아님" rc 1. `git ls-remote` 배포 저장소 HEAD = `7846ddf`.

**검토(검토 깊이 규칙 — 이번 회차에 바뀐 것만, 조정 세션 자체 검토 1회, 하위 에이전트 0)**: 판정 — checklist [되돌리면 안 되는 것] deploy 행(base 대조·`--base` 필수·권한·409/403/404·`***`·결과 모름·이미 반영·인자 오류 GET 전·`--token-file ''`·토큰 모양·dry-run PUT 0)·비출력 시험 행·승인 목록 행(참조 선택 모드·번호 = 줄)·요청 중단 행 **전부 여전히 참**(코드 경로 불변 + 시험 49/17 OK, 새 시험도 `run_deploy`의 값 0건 단언을 거친다). `--ref`는 읽기 전용 GET의 URL만 바꾸고 값은 16진만(쿼리 주입 없음), 자격 증명 경로·가림 불변. **막음 0** → 다음 단계로 가도 된다.
**이월 목록**(한 줄씩):
- `verify --ref`는 그 커밋의 본문만 본다 — 배포 저장소 HEAD·Pages가 그 커밋인지는 문서의 `ls-remote`(코드는 안 봄). 몇 분 안에 다른 배포가 겹칠 때만, 읽기 · 다음 4단계 `--base` 대조가 잡음.
- 배포 질문 "배포만 승인"은 문서 규칙 — `deploy.py push`는 질문·답을 모른다(코드 강제 예: `--confirm 배포`는 사용자 결정 몫).
- 승인 답 모호 시 되묻기도 문서 규칙 — 코드 가드는 종전대로 `--expect N` 합계 대조(N이 틀리면 쓰기 전 `[FAIL]`).
- (지시 범위 밖 — 그대로 이월) "다음에 볼 것" E2: 교체용 즉석 코드(apply.py) 저장소에 두기.

## 첫 실사용 회차 (2026-09-29 09:27~09:52 KST — Code 탭 `/saero-run`, main 작업 폴더) · **배포 완료 `7846ddf`(09:51, 마감 뒤 후속)**
상세 = 아래 "## 2026-09-29 갱신 회차" 절(대조 목록 표 아래). 사용자 입회("배포 전 dry-run을 보이고 '배포' 답을 기다려라"). 사용자가 처음엔 "배포" 대신 "마감"을 답해 PUT 없이 마감 기록(`94c8298`)을 올렸고, 이어 "배포 해야해"로 승인 → **7단계 실제 PUT 완료: 배포 커밋 `7846ddf`(직전 `32d8b05`, 파일 sha 1c52f70 → e755fc9)**. **첫 실제 PUT 실측**: 이 PC git 자격 증명으로 PUT 성공(403 없음). 직후 `verify` 2회(09:51)는 재수령본 sha 1c52f70 = 옛 본문으로 **불일치 exit 1** — `git ls-remote` HEAD = 7846ddf, `?ref=7846ddf` 조회 sha e755fc9·raw 본문 md5 e869c1e8 = 로컬이라 반영은 됨(ref 없는 contents GET 캐시로 보임) → 재PUT 없이 09:52:01 verify 3회째 **일치**. 아래 "남은 것"은 해소(당시 원문 보존).
- **완료**: S0 PASS(09:29) → ① 수집 PASS(9/1~9/28, 4개 노출합 7,989 일치) → 1 ingest(시작 검사 4개 통과, origin/main = HEAD 2회) `610864c` → 4 fetch → compute → 2-1 다름 → 3 신규 0 → 5-0a pull·propose(창 9/28) → ⓐ 승인 → 참조 선택 push 12개 × 3그룹 verified 36/36 `676359f` → 5 교체 → 6 precheck 통과(도장 mode full) → 7 dry-run 통과(권한 참).
- **남은 것(다음 세션 첫 일)**: 작업본 `work/index.html`(md5 e869c1e8, 도장 `work/precheck_ok.md5` = 작업본 e869c1e8 · 직전 배포본 a3465ec0 · full)이 준비돼 있다. **같은 날(9/29) 이어 가면** 4단계 배포본이 그대로인지 `deploy.py push --file work/index.html --base work/prev.html --message "리포트 갱신: 2026.08.26 — 09.28 (34일)" --dry-run` → 사용자 "배포" → 실제 push → `verify` → 아래 갱신 회차 절 배포 칸 채우기. **9/30 이후면** 새 데이터로 `/saero-run` 전 단계(2-1 다름 → 재계산 — 이번 작업본은 버린다. propose `--since`는 배포본 masthead 끝(09.27) + 1일 = 2026-09-28 — 9/28 이름 12개는 이미 registered라 후보로 다시 오르지 않는다. 11·12번 판정의 "지난 회차"는 배포본(09-27판) 기준).
- **"첫 실사용에서 볼 것" 결과**: 1 S0 실제 자격 증명 통과(`permissions.push` 참) · 2 10/1 `지난달` 실측은 아직 · 3 `[profile] 다운로드 기록 정리` 4건 · 4 ingest 시작 검사 4개·origin/main = HEAD 2회 통과 · 5 번호 붙은 승인 문구 → 답의 번호 그대로(`--industry-lines 1,3`), dry-run `[승인 목록] N개`·repr을 사용자에게 보임 · 6 승인 파일 `work/approved_2026-09-29_093447.txt`가 pull 재검사 뒤 첫 POST 전에 생김, verify 36/36, registry 커밋 · 7 도장 3줄 생김, **실제 PUT은 미실측** · 8 local/ md5 대조 = 설치본 같음(af47cb28·7dd534c8).
- **다음에 볼 것(후보)**: `deploy.py verify`가 PUT 직후 ref 없는 contents GET의 캐시(약 1분)로 옛 본문을 받아 불일치를 낼 수 있음(09-29 실측 — 2회 불일치 뒤 일치) — verify를 PUT 응답의 커밋으로 `?ref=` 조회하거나 불일치 문구에 "캐시일 수 있음 — ls-remote HEAD·`?ref=` 확인 뒤 다시 verify(읽기)"를 넣는 안(code-tab.md 4절 행). 사용자 승인 답이 "등록 승인 N개"(N 미기입) + "위 2가지만"처럼 모호하게 와서 세션이 해석을 dry-run으로 보이고 되물음 → 사용자 "오타" 정정(12개). `--expect`가 답의 N을 못 받는 경우의 문구·절차 한 줄(6절) 후보. 교체용 즉석 코드(apply.py 145행)가 세 회차 연속 다시 쓰임 — E2(저장소에 두기) 판단 대상.

## 검증·병합 기록 (2026-09-29 — Code 탭 전 단계 실행: 검증 1 → 수정 회차 2·3·4 → 검증 2(막음 0) → main 병합)

**병합**: `feat-code-tab`(최종 `7aa54af` — b4cc8b9 위 8커밋: f0520b5 구현 · df658f3 기록 · e220079 수정 2 · 77a2ba8 기록 · 0391e0f 수정 3 · 150d059 기록 · 1f726dc 수정 4 · 7aa54af 기록)을 main(`b4cc8b9` — 분기 뒤 main 변경 0, `ls-remote` 확인)에 `git merge --no-ff` → 병합 커밋 **`2ed6bcf`**(부모 b4cc8b9 · 7aa54af, 트리 = 7aa54af와 동일 — `git diff --stat 7aa54af HEAD` 0). 충돌 0(audit/last-audit.md 포함 — main이 움직이지 않아 자동 병합). 신원 `-c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com`. clone은 `D:\saero-verify\merge-code-tab`(`git clone -c core.autocrlf=false` + 로컬 `core.autocrlf=false`). 사용자 병합 지시(2026-09-29 00:0x KST, "검증 2 통과 — feat-code-tab을 main에 합친다") 뒤 병합. 브랜치 `feat-code-tab`은 지우지 않고 둔다. 코드·문서 재수정 없음(이 절 추가만). 아래 "수정 기록 2·3·4"·"구현 기록"의 `main 미반영`·`main 0`은 당시 사실 — 원문 보존, 이 절로 정정(**2026-09-29 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다(재clone 대조는 채팅 보고에).

**검증 1**(`D:\saero-verify\saero-ad-report_검증_Code탭_2026-09-28.md`, 별도 세션 — Code 탭·이 PC, 대상 df658f3, 하위 에이전트 51): 결론 **18건**(동작·보호 장치 8 · 기록 숫자·문구 7 · 옛 문구 3) → 수정 회차 2(V1~V6·N1~N4)·3(W1~W14)·4(X1~X13)에서 전부 반영, 구현 기록 "정정(검증 1)" 블록으로 기록 정정.
**검증 2**(`D:\saero-verify\saero-ad-report_검증2_Code탭_2026-09-28.md`, 별도 세션 — 대상 7aa54af, 하위 에이전트 5): "검증 2가 볼 것" 1~16 · checklist [되돌리면 안 되는 것] 이번 회차 행 · 검증 1 결론 1~18 전부 참·해소. 변이 50/50 잡힘 · 시험 49/15/10/15 OK · mutation_test 전부 살아 있음. **막음 0** → 병합 가. 이월 3 + 참고 1(아래 이월 목록).

**병합 main에서 전체 세트 재실행** [실측] — 이 PC(Windows 11 · venv `D:\saero\.venv` Python 3.12.10 · pandas 2.3.3 · Playwright 1.63.0), PYTHONUTF8 없이, `-W error::ResourceWarning`, test_deploy는 `GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`·`GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`:
- `tests/test_exclusions.py` **Ran 49 OK** rc 0(1.0초, 실제 registry md5 전/후 동일 ca642639) · `tests/test_deploy.py` **Ran 15 OK** rc 0(24초) · `tests/test_ingest.py` **Ran 10 OK** rc 0(67초, data/ 8파일 md5 동일) · `tests/test_fetch_reports.py` **Ran 15 OK** rc 0(80초, data/2026-09·config md5 동일). skipped 0 · ResourceWarning 0.
- `py_compile` scripts 8 · tests 6 = **14/14** · config `json.load` · `bash -n` ingest.sh·precheck.sh 통과.
- 합본 `archive.py combine` **PASS** — 2026.08.26.~09.27. 33일 · 9,991/309/351,299원. 배포본 무인증 재수령 `deploy.py fetch` → sha 1c52f70 · md5 a3465ec0 · 2101행(배포 저장소 HEAD `32d8b05` 그대로).
- `tests/mutation_test.py <재수령 배포본> <합본 4종>` → rc 0 **"전부 살아 있음"**: `[OK]` 43(validate 22 + 0건 가드 14 + archive 7) · MISS/UNCOVERED/SKIP 0 · 원본 md5(html·CSV 4·data/ 8) 전부 동일.
- data·config·registry md5 병합 전후 같음: `cat data/*/*.csv config/*.json audit/exclusions.csv | md5sum` = c0919eef(브랜치와 같음; 병합 전 main 968d7f9b와의 차이 = registry 시험 1행 f495f03b → ca642639, 666행) · config b826b388 · reportlib f29e64fc. 작업 트리 변경 0(`__pycache__`만 생겨 지움). PUT 0 · 네이버 0 · 광고주센터 0 · 실제 자격 증명 0.

**부트스트랩**: 설치본(`anthropic-skills:saero-ad-report`, 97a3e194 — 사용자 확인값)은 저장소 주소·받는 방법 그대로 → **재업로드 불필요(설치본 불변)**. 채팅 가드는 저장소 SKILL.md 맨 위 절이 맡는다(부트스트랩이 채팅에서 main을 받으면 그 가드가 멈춘다). 다음 회차부터 부트스트랩 clone이 main = 병합본을 받는다.

**이월 목록**(한 줄씩):
- (검증 2) `--extra-csv` 단독 경로(후보 0줄)는 propose 뒤 합본·registry md5 대조 없음 — `check_provenance`는 `--from-candidates`·`--industry`만(exclusions.py:1026·1044), 실수 2개 조건 · deploy.py `git_credential` 자식 env가 `GIT_*`를 안 지움(deploy.py:78 — askpass 2개만; `GIT_*` 전부 제거는 시험 `clean_env`만) · `exclusions.py:26` docstring 재개 판정 문구에 "(.md5)" 누락 · 손 폴백(8절)에서 바이트 절반으로 잘린 검색어 CSV가 archive store·combine 검사를 통과(b4cc8b9 이전부터 — 정상 수집은 `fetch_reports` 검사가 앞단에서 막음).
- (조정 대조) N 없는 답의 `--expect` 계산 · 보내는 도중(전송 단계) 타임아웃 문구(`네트워크 오류: timed out` vs `요청 결과 모름`) · 키 가림 정확 일치(부분 문자열만) · 재시도 문서 "propose부터 다시" 한 줄.
- (수정 기록 4) 제안 ID 대조·토큰 범위 헤더(보류 — 사용자 결정) · 2-1 대조 명령화·`ingest --from`·archive data/ 경로 차단(회차 2) · NFKC·keep 처리 주체·`blocked_reason` 공백·기호 변형(점검 회차) · 재개 판정 "이번 회차" 코드 강제(지금은 문서 규칙).
- (이전) "노원힐링장소."(마침표 원문, 미등록) 재상정(사용자) · verify note 결함 후보 · registry `verified_at` 전 행 재기록 · 탐색 기준선 5절 남은 문서 항목.

**첫 실사용에서 볼 것**(main 작업 폴더, Code 탭 세션):
1. 첫 S0(실제 자격 증명) — 배포 줄 `permissions.push: 참` · 스킬 저장소 `push --dry-run` 통과 · 줄바꿈 줄(8절 정리 뒤).
2. 10/1 `지난달` 프리셋 첫 실측 — `--debug`로 돌려 `debug/`·summary.json을 남긴다.
3. `[profile] 다운로드 기록 정리` 건수 추세(실행마다 summary.json `profile_cleanup`).
4. 첫 Code 탭 `ingest.sh` — 시작 검사 4개(HEAD = origin/main · data/ = HEAD · 추적 안 된 파일 0 · 줄바꿈 = 커밋) 통과와 `origin/main = HEAD` 2회.
5. 번호 붙은 승인 문구 → 답의 번호를 `--drop`·`--industry-lines`에 그대로, dry-run의 `[승인 목록] N개`·이름 repr을 사용자에게 보인다.
6. 첫 참조 선택 실제 push — 승인 파일이 pull 재검사 뒤 첫 POST 전에 생기는지(`work/approved_<날짜>_<시분초>.txt`), verify 결과·registry 커밋.
7. 첫 도장(`work/precheck_ok.md5` 3줄) → 첫 실제 PUT(자격 증명 권한 — 403이면 계정·토큰 범위) → verify 일치.
8. wrapup(마감) — local/ 두 파일 md5 대조(LF 판 7dd534c8·af47cb28).

**병합 뒤 할 일**(작업 폴더 세션 몫 — 이 병합 세션은 하지 않았다): main 작업 폴더 `D:\saero\saero-ad-report-skill`을 LF 재clone(`git clone -c core.autocrlf=false`)으로 교체(`work/` 파일은 옮겨 둔다 — 8절) · `local/CLAUDE.md` → `D:\saero\CLAUDE.md`, `local/saero-run/SKILL.md` → `D:\saero\.claude\skills\saero-run\SKILL.md` 설치(사용자) · S0 첫 실행(사용자 동의 — 실제 자격 증명 1회) · 메모리 정리(saero-merge-workflow·PC 시험 환경).
**병합 뒤 준비**(2026-09-29 KST — 교체·clone 00:21 · 설치 00:22 · S0 00:23 · 기록 00:28, 별도 Code 탭 세션 `D:\saero` — 운영 폴더 정리만, 코드 변경 0 · 수집·등록·배포 0): 확인 = `ls-remote` main `339e75f`(병합 기록 커밋) · 옛 작업 폴더 push 안 된 커밋 0(모든 브랜치)·변경 0(무시 파일 `__pycache__`·`work/`뿐) — 옛 폴더에서 `git fetch` 1회(원격 추적 ref만, 작업 트리·커밋 불변) · 교체 = 옛 폴더 → `D:\saero\saero-ad-report-skill.old-0929`(이름 바꾸기, 삭제 안 함) → 같은 경로에 `git clone -c core.autocrlf=false`(`339e75f`) · `work/approved_2026-09-28.txt`(b04b149d)·`work/exclusions_pull_2026-09-28.json`(002fbd08) 복사(md5 원본과 같음) · `ls-files --eol` 41개 전부 i/=w/(`audit/exclusions.csv`만 crlf/crlf·`-text` — 저장소 그대로) · status 0 · 설치 md5 = 저장소 `local/`: `D:\saero\CLAUDE.md` af47cb28d460004fce68d9560ed5406b · `D:\saero\.claude\skills\saero-run\SKILL.md` 7dd534c8d78119dcb3d41c3530584767 · **S0**(00:23 KST, 사용자 동의, 2절 블록 그대로) = 시각 줄만 FAIL(00:23 KST — 설계대로), 나머지 전부 통과, `permissions.push` 참, 값 출력 0(자격 증명 첫 사용 — 출처 git) · 메모리 = `saero-pc-autocrlf`·`saero-pc-shell-gotchas` 삭제(code-tab.md 1절·8절에 전부 있음 — 남는 것 0), 남은 메모리는 `saero-audit-round-stop-rule` 하나(`saero-merge-workflow`는 이 PC 메모리에 없었음).
효율: 벽시계 약 20분(00:08 ls-remote → 병합 → 전체 세트 → 기록·push) · 도구 호출 약 12회 · 즉석 코드 0행(py_compile 인라인 조각만).

---
# 기능 추가 탐색 기준선(Code 탭 전 단계 실행, 2026-09-28)
점검일: 2026-09-28 (기능 추가 회차 — **탐색·설계만**. 데스크톱 앱 Code 탭 세션, 이 PC, 작업 폴더 `D:\saero`로 열어 메모리 D--saero·wrapup이 붙은 상태. 모델 Opus 5.5 — 지시문은 Fable 기준). 기준 main `c5015c5`(시작 때 `git fetch` 뒤 `c5015c5..origin/main` 커밋 0 · 작업 트리 깨끗 · `pull --ff-only` 무변경). SKILL.md·scripts·config·tests·data·work **변경 없음**(이 절 추가만). 네이버 광고주센터·검색광고 API·배포 저장소 쓰기 0, 네이버 로그인 0, 실제 수집 프로필·다운로드 폴더 열기 0. 설치본 부트스트랩 불변(44행, md5 `97a3e194…` — 세션 중 확인). 구현은 사용자가 아래 "내가 고를 항목"을 고른 뒤 별도 회차.
추가할 기능: 지금 따로 도는 ① 보고서 CSV 4개 받기(`scripts/fetch_reports.py`) ② 보관·합본·리포트 갱신·배포(SKILL.md 1단계 보관·합본·보관본 push ~ 8단계, 5-0 제외) ③ 제외 검색어 등록(5-0단계, `scripts/exclusions.py`)을 Code 탭 세션 하나에서 한 번에 잇는다. 아래 "기능 추가 탐색 기준선(보고서 자동 수집)" 절 끝 **사용자 결정(2026-09-28 저녁)** 블록이 정한 다음 순서("Code 탭 전 단계 실행": 경로 규칙·pandas/playwright 의존성·토큰 파일 규약·Code 탭 진입점)다.
방법: 읽기 + 허용 명령만 — 버전·설치 확인, `fetch_reports.py --dry-run` 2회, `exclusions.py report` 1회·`push --dry-run` 4회, 시험 2종. 명령·시험은 전부 스크래치 LF clone(`git -c core.autocrlf=false clone`)에서. 탐침(CRLF 셸 스크립트·TZ·cp949 출력)은 저장소 밖 스크래치에서. 조사 5 · 설계 3 · 반박 검증 6(checklist 충돌 / 사실·실현성) · 완결성 점검 1을 병렬 하위 에이전트로 돌리고 조정자가 서로 대조·재실측했다.
효율: 벽시계 약 80분(13:38 fetch → 14:58 기록) · 도구 호출 조정자 약 50회 + 하위 에이전트 467회 · 즉석 코드 약 30행(결과 분리·탐침, 저장소 밖).
표기: [실측] 이번에 파일·명령으로 확인 / [실측·기록] 저장소 기록 원문 / [추론] 확인 못 함. 행 번호는 c5015c5 파일 기준. 사용자 폴더는 `~`·`C:\Users\<사용자>\…`, 토큰·키 파일은 역할로만 적는다.

## 0. 시작 확인과 환경 실측 [실측]

| 항목 | 값 |
|---|---|
| 저장소 | main `c5015c5` = origin/main, 새 커밋 0, 작업 트리 깨끗 |
| Desktop 사본(`references/report-fetch.md` 12·34행 cd 경로 `C:\Users\<사용자>\Desktop\Agent\claude\saero-ad-report-skill` = ① 문서상 실행 폴더) | `log -1` = `68028c8`(cd 줄 추가) · `status -sb` = `## feat-report-fetch...origin/feat-report-fetch`(원격 ref를 fetch 안 해 뒤처짐 표시 없음) · `merge-base --is-ancestor 53a1575 HEAD` → `fatal: Not a valid object name 53a1575`(exit 128) = **크래시 수정 53a1575와 파일명 수정 cb9f9e7이 없다**. 문서 절차의 `git pull`이면 feat-report-fetch `476ff7b`(수정 포함)를 받지만 main의 data·registry·exclusion-ui 3절은 못 받는다 [추론]. 결과 폴더는 두 사본 모두 `~/saero-fetch/…`(config 동일 b826b388 [실측·기록 64행]) — 다른 것은 코드 판뿐 |
| Python | 3.12.10(`py -0`에 3.12 하나) · pandas **없음** · playwright 1.63.0(번들 chromium-1243 설치됨) |
| `python3`(Git Bash) | WindowsApps의 Microsoft Store 스텁 → `python3 --version`·`python3 -c` exit 49. `python3` 호출: SKILL.md 10곳(89·95·160·178~180·203·226·240·241), ingest.sh 3(7·8·11), precheck.sh 4(14~16), references 2(exclusion-ui.md:68·report-fetch.md:100), checklist 2(66·275) |
| 출력 인코딩 | 도구 파이프의 stdout·stderr = cp949 → `print('—')` UnicodeEncodeError exit 1, `PYTHONUTF8=1`이면 통과(탐침). stdout을 utf-8로 바꾸는 스크립트는 `fetch_reports.py:61`·`exclusions.py:60` 둘뿐이고, `validate.py:353`은 정상 경로에서도 `—`를 찍는다 → 6단계가 인코딩으로 죽을 수 있음 [추론] |
| git | 시스템 설정 `core.autocrlf=true`, 저장소 로컬 설정·`.gitattributes` 없음 → 작업 폴더 34파일 i/lf w/crlf(data CSV 전 행 CRLF, `data/2026-09/키워드.csv` md5 4ebd1593 ≠ 커밋 1da83049) + `audit/exclusions.csv` i/crlf. **git 신원(user.name·email) 어느 범위에도 없음**. credential.helper = manager(시스템) |
| 셸 | Git Bash 5.3. CRLF 셸 스크립트는 `./x.sh`·`bash x.sh` 모두 정상(탐침) → `.sh`의 CRLF는 막는 요인 아님. `/home` 없음, `/home/claude/…` 인자는 `C:\Program Files\Git\home\claude\…`로 변환됨(그 폴더 ACL: Users = RX). zoneinfo 없음 → `TZ=Asia/Seoul date`는 **UTC**(05:42 GMT), `TZ=KST-9 date`가 KST |
| 토큰·키 | 스킬 저장소용/배포 저장소용 PAT 파일 1개(저장소 밖, **어느 저장소용인지 이름으로 모름**) · 네이버 API 키 파일(저장소 밖) · 수집 전용 프로필·다운로드 폴더(`~/saero-fetch/…`) — 존재만 이름으로 확인, 내용·폴더는 열지 않음 |
| 진입점 | 이 Code 탭(`D:\saero`) 세션 스킬 목록에 `wrapup`과 설치본 `anthropic-skills:saero-ad-report`(설명 "광고 CSV 넣어줘 … 반드시 이 스킬을 사용할 것")가 함께 뜬다. 설치본 1절 `cd /home/claude && rm -rf saero-skill && git clone …`은 Git Bash에서 cd가 실패해 사슬이 끊긴다 [추론]. 메모리 D--saero의 링크 `[[saero-code-tab-workflow]]`는 끊김. 저장소 폴더로 열면 메모리 폴더가 새로(빈 채로) 생기고 wrapup이 안 붙는다 [추론 — `~/.claude/projects/`에 D--saero·D--saero-verify만 있음] |
| 허용 명령(스크래치 clone) | `fetch_reports.py --dry-run`(오늘 / `--today 2026-10-01`) exit 0 · 표 4행 · 기대 `이번달` 2026.09.01.~09.27. / `지난달` 09.01.~09.30. · 두 폴더 생성 0 · `git status` 빈 출력. `exclusions.py report` exit 0(664행, 3그룹 registered 221 + deleted 1). `push --approved <9/28 승인 목록 사본> --dry-run` exit 0 "등록 예정 0 · registry에 이미 등록 6", registry md5 f495f03b 전후 동일. 둘 다 pandas 없이 돈다(폴백) |
| 시험(스크래치 LF clone) | `test_fetch_reports.py` Ran 15 · **FAILED 2**(날짜 고정 172·211·222행 — 브라우저 시험 6개는 ok, 78초) · `test_exclusions.py` Ran 29 · **FAILED 1·ERROR 3**, `PYTHONUTF8=1`이면 FAILED 1·ERROR 2(ERROR = pandas 없음 2 + cp949 subprocess 디코드 1, FAIL = 실제 registry 의존 `:509`·`:524` — `노원역맛집출구`가 이제 3그룹 등록). data·config·registry md5 전후 동일. = 병합 기록(19~20행)과 같은 결과 |
| registry 커밋 모양 | 9/28 `bf3089e`의 `audit/exclusions.csv` +663/−648은 줄바꿈 변경이 **아니다**(부모·자식 모두 CRLF·BOM, `--ignore-cr-at-eol`로도 같은 diff) — pull·verify가 모든 행의 `verified_at`을 그날로 다시 써서 매 회차 전 행이 바뀐다 |

## 1. 세 단계 지금 상태

| | ① 보고서 CSV 4개 받기 | ② 보관·합본·갱신·배포(1~8단계, 5-0 제외) | ③ 제외 검색어 등록(5-0) |
|---|---|---|---|
| 자동(코드) | 기대 기간 계산(평일 `이번달` 1일~어제, 1일 `지난달`) → 목록 → 보고서 4개 열기·기간 읽기·(다르면 프리셋·확인)·다운로드·돌아가기 → 검사 6종 + 3종 노출합 → 성공 폴더로 이동·summary.json (`cmd_fetch`·`fetch_one`·`check_file`·`cross_check`) [실측] | `archive.py store`(종류는 컬럼 `:69-76`, 달은 첫 줄 헤더) · `combine`(검사 5종) · `ingest.sh`(store→combine→data push) · `deploy.py fetch/push/verify` · `compute.py` · `precheck.sh`(validate·compare·overflow) [실측] | `propose`(후보·재노출 판정·승인 문구, 호출 0) · `push`(쓰기 전 pull → 그룹별로 없는 이름만 POST → verify, 금지 패턴 `[거부]`) · `verify` · `report` [실측] |
| 사람 손 | 실행 시각 01:00 KST 이후 고르기(코드 검사 없음) · `--login` 창에서 로그인·2단계 인증 · 팝업 닫기 · `--prev` 폴더 고르기(기본값 없음 `:958`) · **4개를 세션에 올리기**(`:920`) · 실패하면 `--debug` 재실행·첨부 | **CSV 업로드**(SKILL.md:52·89 `/mnt/user-data/uploads`) · **토큰 대화창 입력**(25행) · 2-1·3단계·(1)(2) 답 · 라이브 시크릿 창. 세션 손: 2-1 대조·3단계 신규 그룹 판정(스크립트 없음), 5단계 HTML 교체·서술(즉석 코드 400~480행 — 1267·1289행), costPie title, 8단계 기록 | "등록 승인 N개" 답 · **승인 목록 파일 전달**(present_files → Code 탭) · **결과 화면 전달** · (9/27) PowerShell에서 명령 실행 |
| 명령·절 | `python scripts\fetch_reports.py [--dry-run\|--login\|--prev <폴더>\|--debug]` · SKILL.md 66~68 · references/report-fetch.md | SKILL.md 84~100·160~161·203·219·240~241 — 전부 `python3`·`/home/claude/work/…`. `ingest.sh:6` `OUT=/home/claude/work/combined`, `:14` 토큰을 push URL에, `precheck.sh:11` `J=/home/claude/work/compute.json` | SKILL.md 171~195 · references/exclusion-ui.md 3·6·7절 |
| 입력 → 출력 | config `report_fetch` → `~/saero-fetch/downloads/YYYY-MM-DD/<이름> 보고서,2580077.csv`×4 + summary.json(+`debug/`), 실패는 `partial/YYYY-MM-DD/`. `~` = USERPROFILE(`:85`), `--prev`·상대 인자는 cwd 기준 | 업로드 CSV → `data/YYYY-MM/<종류>.csv`(ROOT 기준) → `/home/claude/work/combined/`·`prev.html`·`index.html`·`compute.json` → 배포 저장소 `index.html` | 합본 `검색어.csv` + registry → `ROOT/work/exclusions_proposal_<창끝>.md`·`_candidates.txt`(propose) · `work/approved_<날짜>.txt` · `work/exclusions_pull_<날짜>.json`(pull·verify, 같은 날이면 덮어씀) · registry |
| 필요한 것 | Python ≥3.9 · playwright · 설치 크롬(`browser_channel "chrome"`) · pandas 불필요(폴백 `:44-57`) · 토큰·키 없음 · 네이버 로그인(전용 프로필) | pandas(archive `:41`·compute `:18`·validate `:54-56`·compare·**deploy도 reportlib 경유 `:23`**) · playwright(overflow_check, 번들 크로미움) · bash·md5sum · 스킬 저장소 PAT(ingest)·배포 저장소 PAT(`deploy.py:54` required — fetch에도) | pandas는 propose만(`:509`) · 네이버 API 키 파일(`--key-file`, 기본값·expanduser 없음 `:344-346`) · API 호스트가 열린 셸(PC 일반 셸·Code 탭 O, 채팅 403) |
| 실제로 돈 곳 | 사용자 PowerShell · Desktop 사본(feat-report-fetch, 왕복 3 = `68028c8`). 병합 730aa45 뒤 실사용 0, Code 탭 도구로 실제 광고주센터를 돌린 기록 0 | 채팅(claude.ai 컨테이너 `/home/claude`, 부트스트랩이 main을 매번 clone — 9/28 clone 01:45Z) | 9/27: 채팅 propose + 사용자 PowerShell(Desktop 폴더 — 당시 git 저장소 아님, Python 3.14) / 9/28: 채팅 propose·dry-run·승인 목록 → **Code 탭(작업 폴더 main, python 3.12)** pull·push·verify·registry 커밋 `bf3089e`(+0900) |
| 결과 파일(git 밖) | `~/saero-fetch/downloads`(저장소 밖) | 컨테이너 `/home/claude/work`(세션이 끝나면 사라짐) + present_files 사본. 저장소엔 data·audit 커밋 | 작업 폴더 `work/`(`approved_2026-09-28.txt` 113B · `exclusions_pull_2026-09-28.json`) |
| 최근 실사용 | 왕복 3 성공(9/28, 4개 PASS·노출합 7,628×3, 수집본 = `data/2026-09` md5 동일 — 14·100행) | 9/28 배포 `e1df211`(1차 `0272498` 정정) · data `c8d4441`(토큰 1개만 와 403 → 후속 push) · 재배포 `32d8b05` — 약 18분·47~52회·즉석 400행 | 9/27 33×3 verified(`871ead7`) · 9/28 5×3 verify 15/15(`bf3089e`) · "노원힐링장소." 마침표 누락(1280·1282행) |

## 2. 단계 사이 이음새 — 사람이 옮기는 자리(없앨 대상) [실측]

| # | 자리 | 원문(파일:행) | 누가·무엇·어디 → 어디 | 없애려면 한 곳에 있어야 하는 것 |
|---|---|---|---|---|
| c1 | ①→② CSV 업로드 | SKILL.md:66-67 "사용자가 그 4개를 세션에 올린다" · report-fetch.md:51 "이 4개를 세션에 올리면 … store·push는 지금처럼 세션이 한다(2회차에 PC로 옮길지 결정)" · fetch_reports.py:920 · checklist.md:178([의도된 동작] 24) | 사용자 · CSV 4개 · `~/saero-fetch/downloads/<날짜>/` → 채팅 `/mnt/user-data/uploads/` | fetch 성공 폴더 · archive.py · pandas · 실제 파이썬 · 스킬 저장소 쓰기 수단이 한 셸에 |
| c2 | FAIL 뒤 다시 받기 | SKILL.md:91-92 "사용자에게 이번 달 1일~어제로 다시 받아 달라고 한다" · 113-114 · 128-132 "'사용자 지정 기간'을 선택하고 … 4개 파일을 다시 받아주세요"(문구도 낡음 — 표준은 프리셋, 58-59·72-73) · 147-148 | 사용자 · 손 다운로드 → 세션 | 세션이 fetch를 다시 돌릴 수 있는 곳(로그인 만료만 사람) |
| c3 | ②→③ 옛 모양(9/27) | SKILL.md:190-191 "`pull`·`push`·`verify`는 **사용자 PC의 PowerShell**에서 돈다 — 명령을 채팅에 그대로 적어 주고, 실행 뒤 … 받아 읽는다" · exclusion-ui.md:55 "(사용자 폴더 경유 또는 커밋)" — `work/`는 `.gitignore:3`이라 커밋으로 못 옮긴다 | 세션 → 사용자(명령) → PowerShell → 사용자 → 세션(결과 파일 2개) | API가 열린 셸 · 키 파일 · registry·`work/`가 같은 폴더 |
| c4 | ②→③ 9/28 모양 | 1280행 "승인 목록 `work/approved_2026-09-28.txt`(6줄)를 present_files로 전달. 실행은 … Code 탭" · "(사용자 화면 2장 + 세션 재pull·registry 실측)". 문서는 exclusion-ui.md:42-43만 반영(`c5c1136`), SKILL.md 5-0 4항·checklist.md:174([의도된 동작] 20)는 옛 문구 | 채팅 → present_files → 사용자 → Code 탭 세션 → 사용자 화면 → 채팅(재배포 32d8b05) | 승인 목록을 쓰는 세션 = push하는 세션 = 배포하는 세션 |
| c5 | 이름 원문 | exclusion-ui.md:44 "Claude Code 지시문에는 "이름은 원문 그대로(기호·마침표 포함)"를 명시한다" · 7절 115 "registry·승인 목록·CSV 이름은 원문대로" | 재현: 작업 폴더 승인 목록(11:21:12, 6줄, 마침표 0)을 등록 전 registry(`871ead7`) 사본으로 dry-run → "등록 예정 5 · 이미 등록 1 · 216 → 221". 마침표 복원본 → "6 · 0 · 216 → 222" = 채팅 기록 값(1280행). **채팅이 넘긴 목록엔 마침표가 있었고 Code 탭 쪽에서 파일을 다시 쓰며 빠졌다.** `read_approved`(`exclusions.py:653-662`)는 strip·주석·중복만 처리 → 코드가 아니라 사람(세션) 이음새 탓. 원문 "노원힐링장소."는 registry에 없어 다음 propose에서 어느 목록에도 안 오른다(`:583` first_seen_only) → 1282행 "사람이 재상정" | 승인 목록을 propose 산출물·CSV 원문에서 복사로만 만드는 규칙과 코드 가드 |
| c6 | 실행 폴더 둘 | report-fetch.md:12·34 cd = Desktop 사본(feat-report-fetch, 크래시 수정 없음) ≠ Code 탭 작업 폴더(main — ③ 9/28이 돈 곳, wrapup이 가정하는 곳) | 사람이 두 폴더를 오감. 두 사본에서 동시에 돌리면 같은 프로필을 동시에 씀(금지 report-fetch.md:87) | 작업 폴더 하나 |
| c7 | 토큰 | SKILL.md:25 "매번 대화창에서 입력받는다" — 9/27·9/28 모두 1개만 와 data push 403 → 후속 왕복(1268·1279·1292행) | 사용자 → 채팅 → 세션이 파일로 저장 | PC의 역할별 토큰 파일과 경로 인자 규약 |
| c8 | 첨부 | report-fetch.md:63·65 "`debug/` 전부 … + `summary.json`을 세션에 첨부" · 9절 105 | 사용자 · debug·summary → 세션 | 세션이 download_dir을 직접 읽음(로그인 실패 산출물 제외 — 4절 #15) |

## 3. 멈춤 자리

**ⓐ 사람 승인 = 남길 자리**(없애는 안은 내지 않는다) [실측]
- (1) 새 경쟁사 — SKILL.md:284-286 "승인받은 뒤에만 경쟁사 표에 추가", (1-1) 296-305 config·이력 표·리포트 세 곳을 같은 회차에.
- (2) 애매 후보 — 316 "표에 넣지 말고 짧게 언급한 뒤 확인받는다."
- (3) 새 제외 그룹 — 155 "새로운 후보가 감지되면 **멈추고 확인한다.**", 346-347. 판정 코드 없음(세션).
- (4) 제외 검색어 — 189·322 "'등록 승인 N개'(또는 뺄 이름) 답이 오기 전에는 `push`·`delete`·`test-roundtrip`을 돌리지 않는다." 승인 문구 = `exclusions.py:605-608`·exclusion-ui.md 6절.
- 2-1 — 146-150 "그래도 다시 계산할까요? … 답을 받기 전에 5단계로 넘어가지 않는다." 대조 코드 없음(세션).
- 공통 — 273 "리포트에 반영하지 말고, **배포도 하지 말고**, 채팅으로 보고한 뒤 승인을 기다린다."
- 그 밖 — 재시도·keep·한도 재승인(186·192, exclusion-ui.md:120) · delete/test-roundtrip `--confirm`(`exclusions.py:834·887`) · 12번 N주 미반영(report-structure.md:407-409).
- 사람만 할 수 있는 일(승인 아님, 남김) — 네이버 로그인·2단계 인증(`fetch_reports.py:791`) · 팝업 닫기(report-fetch.md:78) · 라이브 시크릿 창(checklist.md:168) · codegen 녹화.

**ⓑ 자동 검사 FAIL = 멈춤은 남기되 그 뒤 사람 손은 바꿀 수 있음**

| FAIL | 원문(파일:행) | 지금 그 뒤 사람 손 | Code 탭에서 바꿀 수 있는 것 |
|---|---|---|---|
| store 거부 | `archive.py:84` "…두 달에 걸침 — 달별로 나눠 받아야 함" · `:94-95` "…옛 다운로드로 보임. 맞으면 --force" | 손으로 다시 받아 업로드(SKILL.md:91-92) | 세션이 원인 보고 → fetch 재실행 제안(사용자 결정). `--force`·`--chunk` 자동 금지(report-fetch.md:86) |
| store 부분 적용 | `archive.py:79-100` 파일마다 remove → copy, 중간 fail이면 앞 파일은 data/에 남음 | 없음 | 멈추고 `git status data/` 보고, 되돌리기는 사용자 |
| combine FAIL | `archive.py:116·119·127·131·140·145·156` | "4개 파일을 다시 받아주세요"(128-132) | 위와 같음. 단 월초를 놓쳐 지난달 말일 구간이 비면 평일 fetch(`이번달`)로는 복구 불가 → 손 폴백 경로가 필요(`fetch_reports.py:102-110`) |
| registry 없음 | `exclusions.py:938-940` exit 1 | 저장소 확인 | 같은 폴더라 드묾 |
| precheck | `precheck.sh:12-16`(md5 가드 `:13`, validate·compare·overflow) | 세션이 고침(SKILL.md:235) | 그대로. FAIL 상세가 `tail -n 3`에 가려짐 → FAIL이면 전체 출력 |
| deploy verify 불일치 | `deploy.py:76-77` | SKILL.md에 대처 문구 없음 | 멈추고 재GET 비교 보고, 재PUT은 사용자 |
| fetch exit 2 부분 실패 | `fetch_reports.py:925-926` "…store 금지" | `--debug` 재실행 → summary·debug 첨부 | 세션이 `partial/<날짜>/summary.json`을 직접 읽음 — **재실행 전에**(재실행이 partial을 지움 `:812-813`) |
| fetch exit 1 금지 차단 | `:471`·`:485-486` | debug 첨부 | `--debug` 없이는 스크린샷도 summary도 없다(`:847-848`) → `--debug` 재실행은 사용자 결정 |
| fetch exit 1 로그인 | `:840-842` | 사용자가 `--login` | `--login` 실행은 세션(백그라운드), 로그인은 사람(ⓐ) |
| push 부분 실패 · verified:false | `exclusions.py:800-803`·`:825` | 채팅 보고 | 그룹×이름 보고 → 재시도는 ⓐ |
| 네트워크 차단 | `exclusions.py:271` "같은 명령을 PC에서 실행하세요" exit 2 | PowerShell로 옮김(= ⓒ) | Code 탭에선 안 남 [실측·기록 exclusion-ui.md:42] |
| data·registry·audit push 403 | `ingest.sh:14` · 1268행 | 채팅으로 토큰 재요청 | 사용자는 토큰 파일 자리만 고침(채팅 붙여넣기 0) |
| (코드 검사 없음) 01:00 KST · 프로필 사용 중 | report-fetch.md:38(코드는 헤더만 비교 `:225`, 일별은 ⊂ 검사 `:240` → 헤더가 어제까지면 덜 집계돼도 통과) · `:346` `[WARN]` 뒤 계속 launch | 사람이 시각을 고름 / 크롬 닫고 재실행 | 세션 사전 점검(`TZ=KST-9`·`profile_in_use`)으로 올릴 후보 |

exit 코드가 겹친다: fetch exit 1 = 로그인·금지 차단·환경, exit 2 = 부분 실패·argparse 사용법 오류 / exclusions exit 1 = 부분 실패·ApiError·전부 거부(후보 0), exit 2 = 네트워크 차단·argparse → **출력 줄로 가른다** [실측 코드].

**ⓒ 이음새 = 없앨 대상**: 2절 c1~c8.

## 4. Code 탭에서 돌리면 걸리는 것

| # | 항목 | 근거 | 막히는 곳 | 선택지(구현 안 함) |
|---|---|---|---|---|
| 1 | `python3` = Store 스텁 | 0절 | ②(명령 그대로면 1·4·5·6·7단계), ingest·precheck | `python` / `py -3.12` / PY 변수 |
| 2 | pandas 없음 | `reportlib.py:11`·`archive.py:41`·`compute.py:18`·`validate.py:54-56`·`compare.py:16`·**`deploy.py:23`(폴백 없음)**·`exclusions.py:509` | ② 전부(배포 포함) · ③ propose | 저장소 밖 venv(`--system-site-packages` + pandas<3 — 병합 회차 방식 17행) / 시스템 pip / deploy에 폴백 |
| 3 | cp949 | 0절 탐침 · `validate.py:353` · archive fail 메시지 7곳 | ② 6단계 · FAIL 메시지 · ingest 커밋 메시지(heredoc) [추론] | `PYTHONUTF8=1`(Bash 도구는 env가 이어지지 않아 **명령마다**) / 사용자 환경변수 / 로컬 settings env(사용자 설정) / 코드 reconfigure |
| 4 | 채팅 경로 | SKILL.md:51·52·89·95·100·160·161·178·203·219 · `ingest.sh:6` · `precheck.sh:11·13` | ② 1·4·5·6단계, ③ propose | 저장소 `work/`(gitignore) 규칙 — exclusions.py가 이미 `ROOT/work`에 씀 |
| 5 | 작업 폴더 CRLF | 0절 · test_config_columns가 작업 폴더에서 FAIL(42행) · store가 LF 파일을 섞음 · `*.csv -text` 도입 순간 기존 CRLF 파일이 modified로 보임 [추론] | 검증·md5 대조 | `.gitattributes`(`*.csv -text` + `*.sh text eol=lf`) + 작업 폴더 LF 재clone(`reset --hard`는 권한 분류기 거절 기록 — 메모리) / 로컬 `autocrlf=false`만 |
| 6 | git 신원 없음 | `ingest.sh:14` commit에 `-c user.*` 없음 | ② data push | checklist.md:438·wrapup:46의 값(`LeeKwanBeom` · noreply) |
| 7 | 01:00 관문 | 코드 검사 없음 · `TZ=Asia/Seoul`=UTC | ① | `TZ=KST-9` 또는 파이썬으로 KST |
| 8 | 토큰 규약 | SKILL.md:25(대화창) · 247(파일에서만) · `deploy.py:54` required · `ingest.sh:14` 토큰을 URL에(argv 노출·GCM 저장 가능 [추론]) · exclusion-ui.md:32 "이 세션에 연결되지 않은 PC 폴더" 전제가 Code 탭에서 깨짐 | ② 배포·push, ③ | 역할별 파일 2개(저장소·수집 폴더 밖) + 경로 인자, 세션은 존재만 확인 / 스킬 저장소는 GCM(계정 범위 — SKILL.md:28 "서로 통하지 않는다" 약화 [추론]) |
| 9 | `~` 미확장 | `exclusions.py:344-346`·`deploy.py:29-31` | ③·② (PowerShell에서 `~` 인자) | 절대 경로 / expanduser 한 줄 |
| 10 | 진입점 | 0절 | 전체 | `D:\saero`로 열기 + 저장소 밖 진입 규약(로컬 CLAUDE.md 또는 진입 스킬) + 부트스트랩 Windows 분기(재업로드, 사용자) |
| 11 | 사본 여럿 | 0절 Desktop 사본 | ① | 문서 cd 교체, 작업 폴더 하나 |
| 12 | 창·장시간 | Bash 도구 최대 10분 · `--login` 대기 600초(config 112) → run_in_background 필수 · 백그라운드는 끝날 때만 알림 → 도중 `[WARN] … 떠 있음`에서 못 멈춤 · 강제 종료 시 크롬이 남아 잠금 → 크래시 조건 [추론] | ① | 실행 **전** 프로필 사용 중 검사 · 첫 실사용 = 첫 실측 |
| 13 | 시험 이월 | 0절(②③) | 검증 | 날짜 = `data/` 헤더에서(음성 단언 183~186행 등 보존) · fixture registry · subprocess `encoding="utf-8"` |
| 14 | overflow 측정 조건 | checklist.md:171 "Chart.js 미로드 상태" vs PC는 cdnjs 열림 [추론] | ② 6단계 | 결정 |
| 15 | debug 산출물 | `fetch_reports.py:558` input value 60자 · 로그인 실패 때 강제 캡처 `:838` | ① | 로그인 실패 산출물(png·aria·inventory)은 열지 않기 · 마스킹은 별도 회차 |
| 16 | `.gitignore`에 `.claude/` 없음 | 5줄 | 커밋 | 진입 설정은 저장소 밖에 / `.claude/` 추가 |
| 17 | 권한 프롬프트 | push·pip·백그라운드마다 [추론] | 전체 | 허용 목록은 사용자 설정 — 외부 쓰기 명령은 빼는 것이 안전 |

## 5. 문서와 코드가 다른 곳 [실측]

1. propose "쓰기 0"(SKILL.md:178 · exclusion-ui.md:87 · `exclusions.py:12`) ↔ `ROOT/work`에 파일 2개를 씀(`:640`·`:644`), `_candidates.txt`는 문서에 없음. "쓰기 0"은 registry·계정 기준에서만 맞다.
2. SKILL.md 5-0 4항(190-191)·checklist.md:174 "사용자 PC의 PowerShell/일반 셸" ↔ exclusion-ui.md:42-43 "Code 탭 세션".
3. report-fetch.md:12·34 cd = Desktop 사본, :105 브랜치 checkout 절차(병합 뒤 낡음).
4. `fetch_reports.py:20` "사용법 … exit 1" ↔ argparse exit 2(부분 실패와 겹침).
5. report-fetch.md:38 "01:00 전이면 … FAIL" ↔ 코드는 헤더만 비교 — 헤더가 어제까지면 덜 집계돼도 통과.
6. report-fetch.md:61·65 금지 차단도 "debug·summary 첨부" ↔ 그 경로엔 summary·스크린샷이 없음(`--debug` 없을 때).
7. report-fetch.md:41 "자격 증명·쿠키는 없다" ↔ inventory에 input value(`:558`).
8. SKILL.md:64 원본 파일명 `필라테스_보고서_…` ↔ 스크립트 수집본 `필라테스 보고서,2580077.csv`.
9. SKILL.md:130-132·checklist.md:76 '사용자 지정 기간'으로 다시 받기 ↔ 프리셋 표준(58-59·72-73). `archive.py:5` docstring "최근 30일까지만"(임의 결정 11, 83행).
10. SKILL.md:139 2-1이 배포본을 읽는데 배포본은 4단계에서 받음(순서).
11. SKILL.md:261 "[PASS] 줄 세어" ↔ `precheck.sh:14` `tail -n 3`.
12. SKILL.md:35 "읽기는 토큰 없이" ↔ `deploy.py fetch`도 `--token-file` 필수(무토큰은 git clone 폴백뿐).
13. 7단계 verify 불일치 대처 문구 없음.
14. `validate.py:56` 설치 안내가 리눅스용(`--break-system-packages`).
15. verify가 note "등록 요청 성공(확인 전)"을 남김(1282행 ② 결함 후보 그대로).
16. keep: SKILL.md:186 "사용자가 뺀다" ↔ wrapup:28 "registry — 손으로 고치지 않는다", keep을 쓰는 명령 없음.
17. 시험 등록 회차: SKILL.md:195 "구현 검증 회차와 API 키가 바뀐 뒤에만. 검증·진단 회차는 propose·report·--dry-run만" ↔ exclusion-ui.md:126 "검증 회차는 같은 시험 1건을 재현" ↔ checklist.md:407 C①.
18. 순서: SKILL.md 5-0(171) → 7(237)·273 "배포도 하지 말고" ↔ 357행 결정 문장("리포트 갱신·배포 → 제외 검색어 후보·승인·등록·확인")·9/28 실제(배포 뒤 등록 → 재배포).

## 6. 설계안(≤3, 반박 검증 반영판 — 채택은 사용자)

**공통 뼈대**(세 안 모두): 실행 폴더 = PC 작업 폴더(main) 하나, Code 탭은 `D:\saero`로 연다. 순서 S0 사전 점검(쓰기 0: `git fetch`·`status`, 파이썬·pandas·playwright, KST 01:00(`TZ=KST-9`), 토큰·키 파일 존재만, 수집 프로필 사용 중 아님) → ① fetch(백그라운드, `--prev` 직전 성공 폴더) → 1 store·combine·data push(쓰기 뒤 `ls-remote`·`origin/main == HEAD`) → 4단계 fetch를 당겨(읽기) → 2-1 → 3 → 5-0 propose(`--since <직전 배포 끝+1일>` — 기본 창은 마지막 하루라 건너뛴 날의 첫 등장 이름이 빠진다 `:552-556`·`:583`) + (권장) pull + compute → **ⓐ 승인 묶음 한 번**((1)~(4) 중 0개인 항목만 뺀다) → 답으로 config(competitors·excluded_groups)가 바뀌면 config 커밋 + compute(·propose) 재실행 → 승인 목록은 **propose 산출물(후보·제안서 업종어 절)과 CSV 원문에서 복사로만**(재입력 0, 대조는 `K()`, 줄 수 = N) → push(pull → POST → verify) → registry push → 5단계 교체(12 → 11 순서) → 6 precheck → 7 `--dry-run` → push → verify → 8 기록 → push → 재clone.
**승인·등록·확인은 배포 앞**(세 안 공통): ① 배포·검증 세트 1회(9/28은 뒤에 두어 재배포 32d8b05·문구 7곳·fix2.py 14행·검증 세트 2회 — 1281행) ② 07·11·12번을 verify 숫자로 처음부터 ③ SKILL.md 순서(5-0 → 7)·273과 맞고 `--pending` 불필요 ④ 9/28에 뒤집힌 이유는 채팅의 API 403뿐, Code 탭은 등록 약 2분(11:21:12 → 11:22:48). 대가 = 배포가 답을 기다림. 예외 "등록은 나중에"(사용자가 말할 때만): 사실형 문구로 배포 → 등록 뒤 재배포는 4단계 재fetch + `--pending` 없이 엄격 검사. 357행 문장 순서와 달라 **사용자 확정 필요**.
**공통 보정**(반박 검증에서 나온 것 — 세 안 모두 반영): git 신원(`-c user.*`) · env는 명령마다(또는 한 호출 안 `export`) · 01:00은 `TZ=KST-9` · 재개·완료 판정은 대상 현재 상태(verify·`ls-remote`·`deploy verify`)로 — state 파일·registry note로 판정하지 않음 · 프로필 사용 중 검사는 fetch **전에** · exit 코드는 출력 줄로 구분 · 로그인 실패 산출물 열지 않음 · ingest의 "data/ 변경 없음 — push 생략" 분기에서도 `origin/main == HEAD` 확인(커밋만 되고 push 안 된 상태가 숨는다 `ingest.sh:10`) · 리허설은 스크래치 clone에서만, 입력은 `data/` 밖 사본(`archive.py:96-99`가 같은 경로면 원본을 지운 뒤 복사하다 소실) · 수동 폴백(손 다운로드 4개) 입력 경로를 명시.
**F11 ⑤(시험 1건 등록→확인→삭제)**: 네이버 = `test-roundtrip` 1건(충족) · 스킬 저장소 push = 시험 브랜치 push → `ls-remote` → 삭제 → 없음(충족 가능) · **배포 PUT = 삭제 경로 없음**(`deploy.py:26` `contents/index.html` 고정) → 대체안(배포 토큰으로 배포 저장소 `git push --dry-run` = 쓰기 권한만 확인·쓰기 0(1268행 방식) + `verify` 일치/불일치 시험 + 첫 실사용 입회 PUT 1회·재수령 md5). **세 안 모두 이 대체안의 사용자 승인이 있어야 "필수 설계 다 갖춤"이 된다.**

| | A 절차서형(최소 코드) | B 오케스트레이터형 | C 진입점·회차 분할형 |
|---|---|---|---|
| 핵심 | 새 스크립트 0. SKILL.md "Code 탭 실행" 절 + `references/code-tab.md`에 순서·명령·멈춤을 적고 세션이 Bash로 차례로 부른다 | `scripts/run_cycle.py`(표준 라이브러리, preflight·plan·step·state·audit-draft)가 기계 단계를 잇고 사람·세션 차례에서 정해진 exit 코드로 멈췄다가 다음 호출이 이어 받는다. 외부 쓰기는 step별 따로 호출(권한 프롬프트 = 승인 단위) | 저장소 밖 진입 스킬(`D:\saero\.claude\skills\saero-run`)이 저장소 `references/code-tab.md`를 가리킨다. 가드 2개(`ingest.sh --from <성공 폴더>` — summary result=ok·exit_code 0·partial 거부 / `exclusions.py push --candidates <선택 가능 목록> --expect N` — `K()` 대조) |
| 코드 변경 | ingest.sh·precheck.sh 경로·PY·신원·push 확인 · `.gitattributes`·`.gitignore` · (선택) 시험 이월 | run_cycle.py 신설 · exclusions.py `approve`(번호 선택, 업종어·원문 추가 허용) · precheck·ingest 변수화 · deploy.py 폴백·expanduser·API 주소 주입점(검증용) · compare 정규식은 import하지 않고 compute.json masthead 문자열 비교 | 회차 1: ingest·precheck·PY·신원·reconfigure·expanduser·`.gitattributes` / 회차 2: `ingest --from` / 회차 3: `--candidates`·`--expect`·propose `_selectable.txt` |
| 내가 치는 말 | 시작 문구(설치본 트리거와 겹치지 않는 말) · "등록 승인 N개"(+ 뺄 이름 등) · "마감" | `/saero-cycle` · 승인 답 · "마감" | `/saero-run`(리허설은 `/saero-run 리허설`) · 승인 답 · "마감" |
| 진입 | 로컬 `D:\saero\CLAUDE.md`(저장소 밖) | 진입 스킬 `/saero-cycle`(저장소 밖) | 진입 스킬 `/saero-run`(저장소 밖) + 부트스트랩 Windows 분기(재업로드) |
| dry-run | 명령별 기존 dry-run + 스크래치 리허설 | `plan`(쓰기 0) + 스크래치 전용 `--rehearsal` | 기존 dry-run + `/saero-run 리허설`(스크래치) + `ingest --no-push`(스크래치 전용) |
| 검증에서 나온 치명 → 보정 | 재개 판정이 registry에 없는 description 열 → 대상 판정 / 승인 목록 "후보에서 줄 빼기만"이 업종어·재상정을 막음 → 복사 규칙 확장 / 새 행 "성공 폴더만"이 손 폴백을 막음 → 폴백 경로 명시 / env 접두가 `&&` 사슬에 안 걸림 → export | config push 누락 → 포함 / 답 뒤 재계산 순서 없음 → 명시 / 리허설 가드 자기모순(repo 경로 없음)·`--from data/` 원본 소실 → 스크래치 marker·data 밖 사본 / V5(verified:false) 재현 불가 → 주입점 / approve 입력원 제한 → 번호 선택+추가 | `TZ=Asia/Seoul`=UTC → `TZ=KST-9` / 신원 없음 → `-c user.*` / compute 재실행 없음 → 명시 / "후보 0개면 생략" → "(1)~(4) 모두 0일 때만" / 가드 `strip()` 정확 일치가 checklist.md:216 `K()` 위반 → K() / [의도된 동작] 20 개정이 회차 3이라 회차 2 첫 실사용과 충돌 → 회차 1로 |
| 도구 호출·소요(갱신 1회, 검증 현실값) | 약 65~85회 · 40~60분 | 약 50~70회 · 35~50분 | 약 55~70회 · 35~50분 |
| 나눌 순서 | 회차 1 실행 기반 → 회차 2 전 단계 흐름 | 1 PC 실행 기반(preflight·plan) → 2a ①→보관·push → 2b 배포·기록 → 3 ③ 잇기 | 1 환경 기반(1A 코드·시험 / 1B 운영 규약으로 쪼갤 수 있음) → 2 ①→② → 3 ②↔③ |
| 리스크(요지) | 즉석 코드 400행 그대로 · 명령이 길어 세션마다 시행착오 | 코드가 커 검증 부담 · state와 실물 불일치 | 진입 스킬이 정본 저장소 밖(점검 대상에서 빠짐) · 회차 3개라 완료가 늦음 |

조정자 의견(한 줄, 결정은 사용자): **C를 뼈대로** — 회차 1이 357행이 이름 붙인 범위와 이월 ①에 그대로 맞아 "한 회차 기능 하나"에 가장 가깝다. 회차 1·2는 A처럼 새 스크립트 없이 하고, B의 step별 외부 쓰기 분리·state는 E2(apply.py 저장소화) 뒤 후보로 둔다.
검증 방법(공통 재현 목록): 시험 3종(`PYTHONUTF8` 없이·venv) · mutation_test 전부 살아 있음 · dry-run 무변경(전후 data·config·registry md5, `git status`, 두 저장소 `ls-remote` HEAD, fetch 폴더 미생성) · 금지 패턴 차단(`노원역운동`·경쟁사명·일반 1 → `[거부]` 2) · verified:false 실패 보고 · 이름 원문 가드(`노원힐링장소.`) · partial 거부 · 01:00·프로필 사용 중 멈춤 · 시험 1건(`test-roundtrip`, 입회) · 문서 = 코드 grep(`python3`·`/home/claude`·Desktop cd 0건).

## 7. 절대 하면 안 되는 항목 후보와 checklist 충돌

**금지 후보**(근거): partial·검사 실패·summary 없는 폴더를 store(checklist.md:219·220) · `store --force`·`--chunk` 자동(report-fetch.md:86) · 승인 이름을 세션이 다시 타이핑하거나 기호·마침표를 지움(exclusion-ui.md:44·115, 1280행) · "등록 승인 N개" 전 push·delete·test-roundtrip(SKILL.md:322) · 실제 이름·여러 건 시험(checklist.md:212) · 외부 쓰기 자동 재시도·자동 재PUT(SKILL.md:192) · 헤드리스·같은 프로필 동시 실행(report-fetch.md:87 — 두 사본 포함) · 로그인 폼 입력, 로그인 실패 산출물 열기(checklist.md:218) · 토큰·키 파일 열기·출력, 토큰을 채팅에 요구(SKILL.md:247) · 세션이 registry 손 편집(wrapup:28) · 이 PC에서 부트스트랩 1절 실행·`/home/claude` 생성 · `git add -A`(work/·키·`.claude/`) · 답을 반영한 재배포에 `--pending`(checklist.md:205) · precheck 3번째 인자에 작업본(:206) · 크래시 수정 없는 판(68028c8)으로 본 실행 · 01:00 KST 전 실행 · main 아닌 브랜치에서 ingest(`HEAD:main` push, `ingest.sh:14`) · 세션이 권한 허용 목록·env 설정 파일을 바꿈(사용자 설정).

**checklist 충돌**(세 안 공통, 풀려면 사용자 결정):

| checklist:행 원문(짧게) | 이 기능과의 관계 | 사용자가 정할 것 |
|---|---|---|
| :174 [의도된 동작] 20 "`pull`·`push`·`verify`·`test-roundtrip`은 **사용자 PC의 일반 셸**에서 돈다(경로 C)" | 세 안 모두 Code 탭 세션이 실행(exclusion-ui.md:42-43·9/28 실측은 이미 그렇게) | 문안 개정 승인과 시점(첫 실사용 전) |
| :178 [의도된 동작] 24 "검사 통과 파일도 store·push는 **세션이 지금처럼** 한다(PC에서 store·push는 2회차)" | **store·push를 누가 하나**: 지금 = 채팅 세션(업로드받아), 바뀐 뒤 = PC Code 탭 세션(수집 폴더에서 바로). 주체는 여전히 Claude 세션, 자리만 PC — 이 기능이 그 "2회차" | 357행 결정을 근거로 문안 개정 승인(report-fetch.md:51·`fetch_reports.py:21·920`도 함께) |
| :179 [의도된 동작] 25 "`[WARN]`만 내고 계속하는 것 … 정상" | 세션 사전 점검으로 멈춤을 더함(코드 동작은 그대로) | 사전 점검 채택 여부 |
| :171 [의도된 동작] 17 overflow "Chart.js 미로드 상태" | PC는 로드될 수 있음 | 조건 통일(외부 요청 차단) / 로드 상태 허용 |
| :169 [의도된 동작] 15 답 대기 배포 = `--pending` | 배포 앞 등록이면 쓰이지 않음 | "등록은 나중에" 때 사실형 문구 / `--pending` |
| :173 [의도된 동작] 19 업종어 포함은 사용자가 고르면 넣는다 | 승인 목록 가드가 막으면 안 됨 | 가드 입력원에 업종어·원문 추가 허용 |
| :216 "이름 대조는 전부 `K()`" | 새 가드도 K()여야 함(K()로도 마침표 사례를 잡음) | (가드는 K()로 — 결정 불필요, 원안 C만 해당) |
| :207·:219 근거 시험 | 이월 ②③을 고치면 음성 단언(예 test_fetch_reports 183~186행 기간 ≠ 기대 → FAIL)을 보존해야 함 | 이월 ②③을 이 기능 회차에 넣을지 |
| :212 · :407 C① · SKILL.md:195 · exclusion-ui.md:126 | 시험 1건을 어느 회차에 하는지 기존 문서끼리 어긋남 | 회차(구현 끝 / 검증 회차)와 고칠 문서 |
| SKILL.md:25·28·247 · exclusion-ui.md:32 | 토큰 대화창 입력 폐지, GCM이면 "두 토큰 서로 통하지 않음" 약화, 키 격리가 기술→정책 | 토큰 보관 방식·스킬 push 수단·격리 규칙 |
| SKILL.md:256·305 (1-1) | config는 리포트 배포와 같은 회차에 push(B 원안이 빠뜨림) | (보정됨 — 결정 불필요) |
| SKILL.md:273 ↔ 357행 문장 순서 | 등록→배포(세 안) vs 배포→등록(357행 문장·9/28) | 순서 확정 |

## 내가 고를 항목
1. 설계안: A 절차서형 / B 오케스트레이터형 / C 진입점·분할형(조정자 의견: C 뼈대 + 회차 1·2는 새 스크립트 없이) / 보류.
2. 나눌 순서: A 2회차 / B 4회차(1 → 2a → 2b → 3) / C 3회차(회차 1을 1A 코드·시험 / 1B 운영 규약으로 나눌지).
3. 단계 순서: 등록·확인 → 배포(SKILL.md 순서, 세 안 기본) / 배포 → 등록(357행 문장·9/28). "등록은 나중에" 예외 허용 여부와 그때 문구 방식(사실형 / `--pending`).
4. 실행 폴더: PC 작업 폴더(main) 하나로(세 안 공통). Desktop 사본 처리(이름 바꿔 보관 / 삭제 / 그대로 — 사용자 손). 작업 폴더를 LF로 다시 받을지(재clone — 기존 `work/`의 9/28 파일 2개 보관).
5. 과도기 운영(마지막 회차 병합 전, 10/1 `지난달` 첫 실측 포함): ① = Code 탭에서 main 작업 폴더 스크립트(`python`, pandas 불필요) 또는 Desktop 사본 `git pull` 뒤 PowerShell / ② = 채팅 업로드(현행) / ③ = Code 탭(9/28 방식). 10/1은 크래시 수정 판 + `--debug`.
6. checklist [의도된 동작] 20·24 개정 문안 승인(+ 25 사전 점검, 17 overflow 조건, 15 답 대기 배포, 19 업종어 경로).
7. pandas: 저장소 밖 venv(`--system-site-packages` + pandas<3) / 시스템 pip — 설치는 구현 회차에서 사용자 승인 뒤.
8. 토큰: 역할별 파일 2개(저장소·수집 폴더 밖, 만료일 설정) 상주 / 회차마다 두고 폐기 / 스킬 저장소는 GCM. 기존 PAT 파일이 어느 저장소용인지 사용자 확인.
9. 인코딩·PY: 명령마다 `PYTHONUTF8=1`·PY / 사용자 환경변수 / 로컬 settings env(영구 설정 — 사용자가 직접) / 코드 reconfigure.
10. 진입점: Code 탭은 `D:\saero`로 연다(세 안 공통). 진입 규약 = 로컬 CLAUDE.md / 진입 스킬. 설치본 부트스트랩에 Windows 분기를 넣어 재업로드할지. 첫 말(`/saero-run` 등).
11. `.gitattributes`: A `*.csv -text` + `*.sh text eol=lf` / B `* text=auto eol=lf` / C `*.sh`만 / D 로컬 `autocrlf=false`만.
12. config 값(공개 저장소라 `~`만, 실제 경로는 로컬에): python 경로 · 작업 폴더(`work/` 또는 `work/run-<날짜>/`) · `download_dir`·`profile_dir` 유지 · 토큰·키 파일 자리(역할별 — 이름은 로컬에만) · 수집 시작 가능 시각 01:00 · 스킬 push 방식 · git 신원 값을 둘 곳.
13. F11 ⑤ 대체안 승인: 배포 PUT = 배포 토큰 `git push --dry-run` + verify 일치/불일치 시험 + 첫 실사용 입회 PUT 1회 / 스킬 저장소 = 시험 브랜치 push → 확인 → 삭제.
14. 시험 항목: 제외 검색어 `saero제외테스트<MMDD>` 1건 — 그룹(targets 첫째 노원산전 / 9/27 선례 상계동) · description `saero test MM-DD` · 사용자 입회 · 등록 → 확인 → 삭제 → 없음 · registry `deleted` 1행 · 어느 회차(문서 모순 5절 17 정리 포함) · API 키 재발급 여부(기록 없음). fixture(`노원역운동`·경쟁사명·일반 1 / `노원힐링장소.`) · fetch `--dry-run --today 2026-10-01` · 배포 verify 일치/불일치.
15. 시험 이월 ②③을 회차 1에 넣을지 / 따로.
16. keep 처리 주체(사용자 손 편집 / 명령 신설 — 별도 회차).
17. 내가 칠 말(안): 첫 말 / "등록 승인 N개"(+ "빼: 이름" · "업종어 넣기: 이름" · 경쟁사 채택·보류 · 제외 그룹 예·아니오) / 2-1 "그래도 다시 계산" / 첫 실사용 "배포" / "마감".
18. 첫 실사용 범위: 마지막 구현 회차 병합 뒤 평일 01:00 KST 이후(10/1 피함), 사용자 입회, fetch `--debug`, 배포 "배포" 확인 1회, 등록은 실제 후보가 있을 때만. 손 다운로드 대조(결정 7, 129행)를 다시 할지.
19. "노원힐링장소."(마침표 원문, 미등록) 재상정 여부.
20. 점검 회차로 넘길 것: verify note 결함 후보(1282행 ②) · registry 전 행 `verified_at` 재기록(매 회차 전 행 diff) · 5절 문서·코드 어긋남 18건.

## 마무리 기록(이번 회차)
- 1차 커밋 = 이 절만(`audit/last-audit.md` 경로 지정 add, author `LeeKwanBeom <322668067+LeeKwanBeom@users.noreply.github.com>`). push는 이 PC의 git 설정 그대로(토큰 수령·사용 0), 직전 `git fetch`, 뒤 스크래치 재clone으로 행수·md5 대조. 커밋 해시는 자기 참조라 적지 않는다.
- 전문은 저장소 밖 사용자 폴더 `saero-ad-report_Code탭전단계_탐색_2026-09-28.md`(하위 에이전트 원문 부록 포함).
- 네이버 계정 읽기·쓰기 0 · 배포 저장소 0 · SKILL.md·scripts·config·tests·data md5 불변 · 부트스트랩 불변. 이 세션에서 받은 토큰 없음.

---

# 기능 추가 구현 기준선(보고서 자동 수집 C, 2026-09-28)
점검일: 2026-09-28 (기능 추가 회차 — **구현**, Fable, 웹 claude.ai 세션, 탐색과 다른 세션). 브랜치 **`feat-report-fetch`**(main `0a2bafb`에서 분기), **main 미반영**. 네이버 계정 접속 **0**(광고주센터·API 어느 쪽도 이 환경에서 못 연다 — 탐색 기준선 0절 그대로; 실제 화면 실행은 전부 사용자 PC). 리포트 갱신·배포 **없음**. 설치본 부트스트랩(`/mnt/skills/plugins/saero-ad-report/SKILL.md`) **불변**(44행, md5 `97a3e194388b2ee75ad8fc81f9e47f78` 세션 시작·끝 동일 [실측]).
설계: 탐색 기준선 6-6 **C(PC Playwright, 4개 전부)** + 재집계 감지(`--prev`, API 0). A(API 교차 검증)는 이월. 기준선 1절(UI CSV 형식·store 통과 조건)·6-5(UI 실물)·6-7(금지 후보)을 그대로 따랐다.
검증용 clone: `git clone -b feat-report-fetch --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill <별도 폴더>`
효율: 벽시계 약 40분(00:21 UTC clone → 00:48 1차 push(코드) → 2차 push(audit)는 아래 마무리 기록) · 도구 호출 약 55회 · 즉석 코드 0행(산출물은 전부 저장소 안: 스크립트 745·시험 393·가짜 화면 199·문서 97행. 세션 안 편집용 파이썬 조각은 산출 아님).
표기: [실측] 이 세션에서 직접 확인 / [문서] 저장소·공식 문서 원문 / [추론] 확인 못 함 / [미실측] 사용자 PC에서만 확인 가능 / [시험] 저장소 `tests/fixtures` 가짜 화면으로 확인(실제 사이트 아님).

## 검증·병합 기록 (2026-09-28 — 보고서 자동 수집 C: 검증 1 → 수정 회차 2 → 검증 2 → main 병합)

**병합**: `feat-report-fetch`(최종 `476ff7b` — 분기 뒤 11커밋: 79ad780 구현 … cb9f9e7 왕복 3 · 47a9f43 기록 · 53a1575 수정 2 · 476ff7b 기록 2)을 main(`aaa3ed7` — 분기 뒤 main 5커밋: c8d4441 data · bf3089e registry · 284c60a·aaa3ed7 audit · c5c1136 audit + `references/exclusion-ui.md` +3행)에 `git merge --no-ff` → 병합 커밋 **`730aa45`**(부모 aaa3ed7·476ff7b). **충돌 0** — `audit/last-audit.md`도 자동 병합(main 추가 32행·브랜치 추가 110행이 병합본에 전부 있음, main이 바꾼 1행은 새 문장으로; 2006 → 2147행). 병합 tree: 브랜치가 안 건드린 파일(`data/2026-09` 4·`audit/exclusions.csv`·`references/exclusion-ui.md`) = main, 그 밖 = 476ff7b(`git diff` 확인).
clone은 `git -c core.autocrlf=false clone` + clone 로컬 설정 `core.autocrlf=false`(이 PC는 Git 시스템 설정 `C:/Program Files/Git/etc/gitconfig`가 `autocrlf=true` — 병합 체크아웃도 LF), 병합 변경 9파일 CR 0 [실측].
사용자 병합 지시(2026-09-28, "검증이 끝난 브랜치를 main에 합쳐줘") 뒤 병합. 브랜치 `feat-report-fetch`는 지우지 않고 둔다. 코드·문서 재수정 없음(이 절 추가만). 위 표제와 "수정 기록 2"의 `main 미반영`·`main 0`은 당시 사실 — 원문 보존, 이 절로 정정(**2026-09-28 main 반영**). 이 절의 기록 커밋 해시는 자기 참조라 적지 않는다.

**검증 1**(`saero-ad-report_검증_2026-09-28.md`, 별도 세션 — 데스크톱 앱 Code 탭·사용자 PC, 대상 47a9f43): 목록 1·2·3·5·6·7·9·10·11 재현·일치(PC 수집 4개 = main `data/2026-09` 4개 md5 바이트 동일), 목록 8 확인 못 함(부트스트랩 설치본 없는 PC). **판정 2건** → ① 결함: 같은 전용 프로필 2회째 실행부터 다운로드 순간 크롬 크래시(0xC0000005 — 프로필 `History` `downloads`에 지워진 Playwright 임시 파일 경로가 남은 상태가 조건; 이 PC에서 시험 12개 중 9 OK·3 FAIL, 설치 크롬 창·같은 프로필 1회차만 성공) ② 기록 오류: 임의 결정 7 "설계 밖 config 키 4개"(실제 5개). 참고 1(main 앞선 변경에 `references/exclusion-ui.md`도 있음 — 충돌 0). "원래 제안·지시를 바꾼 곳"은 의도와 다른 구현 없음. → 사용자 지시 → **수정 회차 2**(`53a1575`·`476ff7b`, 아래 "수정 기록 2").
**검증 2**(별도 세션, 대상 476ff7b): 보고의 최종 해시 `476ff7b`(사용자 전달) = 원격 `feat-report-fetch` HEAD [실측] → 사용자 병합 지시. 보고 전문은 이 병합 세션 폴더에 없어 세부 항목은 옮겨 적지 않았다. "수정 기록 2"의 발견(지운 기록이 같은 id로 되살아남)은 결함 판정 없이 첫 실사용 관찰 항목으로(사용자 지시, 아래 2).

**병합 main에서 전체 세트 재실행** [실측] — 이 PC(Windows 11 · Python 3.12.10 · Playwright 1.63.0). PC에 pandas가 없어 합본·mutation_test는 회차 폴더의 격리 venv(`--system-site-packages` + pandas 2.3.3, 시스템 Python 불변)로:
- `py_compile` scripts 8 · tests 4 = **12/12** 통과 · config `json.load` 통과.
- `python -W error::ResourceWarning tests/test_fetch_reports.py` → **Ran 15 · FAILED 2**(78초). 실패 = `test_check_file_and_cross_on_real_data`(`키워드.csv` "기간 = 기대": 헤더 2026.09.01.~2026.09.27. ↔ 기대 ~09.26.) · `test_compare_prev_warns_on_recount`(`common_days` 27 ≠ 26). 원인: 시험 172·211행 `D(2026, 9, 26)`·222행 `common_days … 26`이 **실제 `data/2026-09`의 기간을 고정** — 브랜치의 data는 09-26판(f625fbc), main은 `c8d4441`(09-28 갱신 회차)에서 09-27판. 코드 결함 아님, 이번 달 파일이 갱신될 때마다 다시 깨지는 구조 → 이월(사용자 결정 2026-09-28: 기록하고 push). 나머지 13개 OK — 브라우저 시험 6개 전부(번들 크로미움, skip 0)·프로필 정리 2·channel 1 포함. 끝 줄 `실제 data/2026-09·config md5 전/후 동일: True (b826b388 등)`.
- `tests/test_exclusions.py` → Ran 29: 시스템 Python(pandas 없음) FAILED 1·ERROR 3 / venv FAILED 1·ERROR 1 / venv + `PYTHONUTF8=1` **FAILED 1**. ERROR = Windows 기본 인코딩(cp949)에서 subprocess 출력 디코드 실패(`r.stdout` None)·pandas 없음. FAILED 1 = `test_push_dry_run_zero_http_and_no_file_change`(실제 registry 사본을 쓰는데 `노원역맛집출구`가 이미 3그룹 등록 → "등록 예정 1 · registry에 이미 등록 1" 0회). **병합 전 main(aaa3ed7)·분기점(0a2bafb) 스냅샷에서도 같은 결과** — `exclusions.py`·`test_exclusions.py`는 브랜치가 안 건드려 이번 병합과 무관 → 이월. `audit/exclusions.csv` f495f03b 전후 동일.
- 합본 `archive.py combine`(회차 폴더) **PASS** — 2026.08.26.~09.27. 33일 · 9,991/309/351,299원(8월 조각 2,363/50/36,397 + 9월 7,628/259/314,902) = 09-28 갱신 회차 기록과 같음.
- `tests/mutation_test.py <배포본 32d8b05 index.html> <합본 4종>`(`PYTHONUTF8=1`) → exit 0 **"전부 살아 있음"**: 기준 22 PASS / 0 FAIL → 변조 22 [OK] + 0건 가드 14 [OK] + config 실험 2 + archive 7/7 [OK], 커버리지 22/22, [MISS]/[UNCOVERED]/[SKIP] 0, 원본 md5(html·CSV 4·data/ 8) 전부 동일.
- `data/2026-09` 4파일 md5 전후 동일(검색어 984ec818 · 상세지역 c6707c34 · 시간대별 a3b7e5c3 · 키워드 1da83049). 배포 저장소 HEAD `32d8b05` 그대로, PUT 없음. 네이버 계정·광고주센터 접속 0, 실제 프로필 `~/saero-fetch/chrome-profile` 접근 0.

**부트스트랩**: 설치본 SKILL.md는 저장소 주소·받는 방법 그대로 → **재업로드 불필요(설치본 불변)**. 다음 회차부터 부트스트랩 clone이 main = 병합본(1단계 `scripts/fetch_reports.py`·`references/report-fetch.md`·config `report_fetch`)을 받는다.

**첫 실사용에서 볼 것**(사용자 PC, 실제 프로필):
1. 첫 `[profile] 다운로드 기록 정리: …` 줄 — 왕복 1~3의 파일 없는 기록이 지워지고(실제 파일 있는 기록은 유지) 크래시 없이 4개가 받아지는지.
2. **지운 다운로드 기록이 같은 id로 되살아나는 현상 건수** — 실행마다 `[profile]` 정리 건수와 summary.json `profile_cleanup`을 적어 추세(수정 기록 2 ④: 실행마다 4건씩 증가)를 본다.
3. **10월 1일은 `지난달` 프리셋 첫 실측**(기간 텍스트 클릭 → 팝업 → `지난달` → `확인` → `조회하기` 활성) — 그날은 `--debug`로 돌려 `debug/`·summary.json을 남긴다.

**이월**: ① `.gitattributes`로 CSV CRLF 방지(이 PC Git 시스템 설정 `autocrlf=true`) → 다음 "Code 탭 전 단계 실행" 회차 ② `test_fetch_reports.py` 날짜 고정 2건(172·211·222행 — 이번 달 `data/` 갱신마다 FAIL) ③ `test_exclusions.py` 기존 실패(실제 registry 의존 1 · Windows 인코딩/pandas 없음 ERROR — 병합 전부터).
효율: 벽시계 약 50분(12:28 clone → 병합 → 전체 세트 → 기록·push) · 도구 호출 약 35회 · 즉석 코드 0행(저장소 산출 없음 — 대조용 셸·인라인 조각만).

## 다음에 볼 것 (순서대로)

1. ~~PC 왕복~~ 완료(3회, 성공). 2. 검증 회차(다른 세션, 위 목록 — 브랜치 최종 해시 기준) → "합쳐도 된다" 뒤 조정에서 main 병합. 3. 병합 뒤 첫 실사용은 **수동 1회**(결정 7): 같은 날 손으로 받은 4개와 대조(목록 6) → 결과를 "첫 실사용 기록"에; **10월 1일 실행**이 `지난달` 프리셋 경로(팝업·`확인`·`조회하기` 활성)의 첫 실측이므로 그날은 `--debug`로. 4. 2회차 후보: PC에서 store·push까지 / A(API 교차 검증) / archive.py docstring 문구 / `--prev` 기본값(직전 성공 폴더 자동 선택).

## 검증·병합 기록 (2026-09-27 — 제외 검색어 기능 추가 회차: 검증 1 → 수정 회차 2 → 검증 2 통과 → main 병합)

**병합**: `feat-exclusions`(최종 `fd5626a` = 53356d1 구현 · a615a84 기록 · a8c8c12 수정 2 · fd5626a 기록 2)을 main(`11c0bc2` — 분기 뒤 main 커밋 없음)에 `git merge --no-ff` → 병합 커밋 **`6a35abf`**(부모 11c0bc2·fd5626a). 충돌 0, 병합 tree = fd5626a tree(`git diff fd5626a` 0행).
사용자 명시 승인("main에 합쳐", 2026-09-27) 뒤 병합. 브랜치 `feat-exclusions`는 지우지 않고 둔다. 코드·문서 재수정 없음(이 절 + 대조 목록 머리말 한 구절 + "다음 점검에서 대조할 것" 추가만). 이 절의 기록 커밋 해시는 자기 참조라 본문에 적지 않는다.
위 "구현 기록"·"수정 기록 2" 표제의 `main 미반영`은 당시 사실 — 원문 보존, 이 절로 정정(**2026-09-27 main 반영**).

**검증 1**(`saero-ad-report_검증_2026-09-27.md` 143행, 별도 세션, 대상 a615a84): 기준값·재현 ①~⑨ 전부 재현. 판단 요청 4건(registry 없으면 조용히 진행 / failed 이름 소멸 / "이미 등록 m" 라벨≠값 / 남은 용량 문서>코드) + 참고 2건(스냅샷·`delete --confirm`) → 조정 세션(이 세션)이 브랜치 코드에서 실물 확인 → 사용자 "고쳐" → **수정 회차 2**(a8c8c12·fd5626a, 위 "수정 기록 2").
**검증 2**(`saero-ad-report_검증2_2026-09-27.md` 96행, 같은 검증 세션, 대상 fd5626a): **재현 실패 0건 → main 병합 승인.** 참고 4건(결함 아님): ① 첫 pull 뒤 재등록 후보 줄의 "미등록 …"이 그룹명 대신 그룹 ID로 찍힘(`registration_status` `g = group_id or group_name`, `fmt_groups`는 `*`만 치환) — 읽기 편의, 판정·건수 영향 0 → 이월 ② 승인 문구(propose, 오프라인)에는 용량이 없고 dry-run·push 출력에만 ③ SKILL 5-0 1항의 "멈추는 명령"은 셋만 적음(references·checklist는 여섯 — 부분집합) ④ dry-run의 "현재 registry 등록 n"은 UI 전사 기준 추정(첫 pull 뒤 API 기준으로 맞춰짐).

**병합 main에서 전체 세트 재실행** [실측] — 합본 = `data/` 보관본 `archive.py combine`(사본 폴더 `combined_merge`, 앞선 합본 4파일과 바이트 동일: 키워드 265f47fa·검색어 940600ac·상세지역 a08d0371·시간대별 5b2e7aaa), 작업본 = 배포본 `277889d`(git clone, md5 94b436f2…), 직전 배포본 = `ad48222`(md5 4defb16a…). 배포 저장소 HEAD `277889d` 그대로, **PUT 없음**:
combine **PASS**(32일 · 9,737/302/344,274원) → validate **22 PASS / 0 FAIL** → compute(`--competitors-html` ad48222: KPI 9,731/302/3.1%/344,274원, 경쟁사 25행, 신규 변형 후보 []) → compare **OK 95 / DIFF 0** → mutation_test **43 [OK]**([MISS]/[UNCOVERED]/[SKIP] 0) → precheck.sh(277889d · 합본 · ad48222) 6단계 전부 통과, overflow 360/390/430 넘침 0 → **`tests/test_exclusions.py` 20 OK**, `audit/exclusions.csv` 3c4c8232 불변. 병합 전(브랜치 tree)·병합 뒤(main) 두 번 돌려 같은 값.
네이버 계정 쓰기 0(이 회차 전체 — 탐색·구현·검증·병합 어디서도 등록·삭제 호출 없음). 저장소 push는 클라우드 git 프록시 403이라 전부 PC(device_bash)에서.

**부트스트랩**: 설치본 SKILL.md는 저장소 주소·받는 방법 그대로 → **재업로드 불필요(설치본 불변)**. 다음 갱신 회차부터 부트스트랩 clone이 main = 병합본(5-0단계·`scripts/exclusions.py`·registry)을 받는다.

**첫 실사용에서 볼 것**(전부 사용자 PC, 순서대로 — SKILL.md 5-0단계·references/exclusion-ui.md 3절):
1. **API 비밀키 재발급**(09-27 채팅에 키가 보이는 화면이 올라왔음) → `C:\Users\<사용자>\naver-api.keys.json`(연결 폴더·저장소·채팅 밖).
2. `python scripts\exclusions.py pull --key-file <keys>` **읽기만** → 출력의 그룹명 3개(= 탐색 기준선 2-3절 요청 3의 답)·`userLock`·`useAdvoost`·`[주의]` 줄 / registry `group_id` 채워졌는지·`*` 행 정리·`missing` 발생 이름(있으면 UI로 한 번 확인) → 결과를 이 파일 "첫 실사용 기록"에.
3. `test-roundtrip --keyword saero제외테스트<날짜> --group <adgroup_id> --key-file <keys> --confirm` **1건·사용자 입회**(제외 검색어 탭에서 생겼다 사라지는지) → `PASS`·registry `deleted` 1행.
4. 첫 자동 회차: `propose` → 승인 문구 → "등록 승인 N개"(미등록 33개 안팎) → `push --dry-run` → `push --key-file` → 출력(그룹별 성공·실패·verify)·`audit/exclusions.csv`·`work/exclusions_pull_<날짜>.json` → 대조 목록 표에 요약 행 → 다음 날부터 재노출 판정("등록돼 있는데도 노출" 0이어야 정상).
5. 이월: 검증 2 참고 ①(그룹 ID → 그룹명 표기) · 탐색 기준선 4절 236행(승인 문구에 그룹별 현재 개수 — propose가 오프라인이라 registry 기준 추정치로 넣을지) · `import-ui` 실사용 여부(API가 되면 안 쓰는 경로).


## 첫 실사용 기록 (2026-09-27~ — 제외 검색어 자동화, 사용자 PC 실행)

- **1. 환경(2026-09-27)**: 사용자 PC PowerShell에 `git` 없음(`git : 'git' 용어가 … 인식되지 않습니다`), Python은 3.14(`pythoncore-3.14-64`), pandas 없음. 조치 ① 저장소 clone 대신 **세션이 main 트리(30파일)를 연결 폴더 `Desktop\Agent\claude\saero-ad-report-skill\`에 직접 배치**(device_commit_files) — 이후 PC 실행 결과(registry·`work/` 스냅샷)는 그 폴더에서 세션이 읽어 저장소에 커밋한다. ② `scripts/exclusions.py`의 `from reportlib import ROOT, load_config`가 reportlib의 모듈 수준 `import pandas` 때문에 PC에서 실패하므로 **ImportError 폴백**(pandas·reportlib이 없으면 ROOT·load_config를 같은 동작으로 자체 정의) 추가 + 시험 `test_runs_without_pandas_for_pc_commands`(pandas를 막고 `report` 실행 exit 0, 시험 20→**21**). pull/push/verify/test-roundtrip은 표준 라이브러리만 쓰고 propose(pandas)는 세션에서 돈다. 검증 회차 밖의 코드 변경이므로 다음 점검 회차가 대조한다(변경 = import 블록 1곳·시험 1개, 다른 함수 불변).
- **2. 첫 `pull`(2026-09-27, 사용자 PC, 읽기만) [실측: 사용자 화면 + registry·스냅샷 파일]**: 3그룹 전부 `userLock=False · useExpSearch=True`, `[주의]` 0. **ID↔그룹명 확정(탐색 기준선 요청 3의 답)**: `grp-a001-01-000000072697414` = **노원산전필라테스** / `…072288536` = **노원역필라테스** / `…072587864` = **상계동필라테스**. 확장 검색 제외 검색어 **183개 × 3그룹, 세 집합 동일**(교집합 183 = 합집합 183 — 3그룹 동일 가정 실증). registry 340행 → **621행**(API 549 + 기록 `*` 37 + UI 미등록 35), `group_id` 빈 행 0. **미등록 33개 그대로 미등록**(API 세 그룹 어디에도 없음), 09-23 32개 중 API 등록 10개 = 탐색 회차 판정과 동일(재등록 7 + 노원역8번출구·노원역출구·노원역배스킨라빈스), 09-27 제안 14개 API 등록 0. `missing` 4건(1번출구·5번출구·정기주차·지도)은 09-10 기록의 **표기 축약**이었다 — API 실명은 노원역1번출구·노원역5번출구·노원역정기주차·노원역지도(전부 등록됨) → 기록 행 4개 삭제(아래 조치 ③). 09-17 기록의 어근 7개(맛집·우동·타이어·사진관·건물·까페·카페)는 API에 낱말 그대로 등록돼 있음(`우동`·`타이어`·`사진관`·`건물`·`까페`·`카페` 확인).
  등록일 분포(API `regTm` 날짜, UTC 그대로): 09-10 38 · 09-16 73 · 09-20 39 · 09-24 9 · 09-25 11 · 09-26 13 = 183. 기록의 등록일은 09-10 38 · **09-17** 67+어근 7 · **09-20 17 + 09-21 22** · 09-24 9 · 09-25 11 · 09-26 13 이라 **regTm은 UTC**(09:00 KST 이전 등록분이 하루 이르게 잡힘: 09-17 → 09-16, 09-21 → 09-20)로 판정 → 조치 ② `regtm_to_date`를 **KST 날짜**로 변환(등록 당일 판정은 검색어 CSV `일별`(KST)과 같은 기준이어야 함) + 스냅샷에 이름별 `id·regTm·registered_at(KST)` 기록 + 시험 `test_regtm_utc_to_kst_date`(시험 21→**22**).
  **재pull(2026-09-27, 읽기) [실측: 스냅샷 원문]**: `regTm` 실값 `2026-09-16T23:21:31.000Z`(= 09-17 08:21 KST, 73개 동일 시각) · `2026-09-20T22:57:44.000Z`~(= 09-21 07:57 KST, 22개) → **KST 등록일 = 09-10 38 · 09-17 73 · 09-20 17 · 09-21 22 · 09-24 9 · 09-25 11 · 09-26 13 = 기록의 목록 건수와 전부 일치**(UTC 시각 분포 01·03·04·05·22·23시). 판정 확정.
- **3. registry 커밋(2026-09-27)**: PC pull 결과(621행)를 저장소로 가져와 조치 ③ 09-10 축약 표기 `*` 행 4개(1번출구·5번출구·정기주차·지도) 삭제 + 실명 API 행 12개 note에 "축약 표기 실명" 주석 → 조치 ⑤ **`*` 행 해소**(`do_pull`: 3그룹을 다 읽었으면 기록 행을 그룹별 행으로 풀고 `*` 삭제 — 없는 그룹마다 `unregistered`/`missing`/`keep`, 시험 `test_pull_resolves_star_rows_into_group_rows`)를 스냅샷을 가짜 API로 삼아 오프라인 적용(네트워크 0, 같은 코드 경로) → **648행 = 등록 183×3 + 미등록 33×3, `*` 0, `group_id` 빈칸 0, `missing` 0**. `propose --day 2026-09-26` → 재등록 후보 33·등록돼 있는데도 노출 0·이미 등록 1(변화 없음). 조치 ④ 검증 2 참고 ① 채택 — `registration_status`가 그룹 ID 대신 그룹명을 돌려줘 제안서의 "미등록 …"이 그룹명으로 찍힌다(시험 `test_registration_status` 확장). 시험 22→**23**. 이 항의 코드 변경(② ④ ⑤)은 검증 회차 밖 — 다음 점검 회차 대조 대상.
- **3. 시험 1건(2026-09-27, 상계동필라테스 `…072587864`, 사용자 입회)** — 1차 시도 **실패**: `[FAIL] POST restricted-keywords grp-a001-01-000000072587864 → 400: {"code": 3721, "status": 400, "title": "The description of the negative search terms has reached its maximum length."}` [실측: 사용자 화면]. 원인 = `description` `saero-ad-report 시험 2026-09-27`(29자)가 API 설명 길이 한도 초과(한도 미공개, 오류 코드 표는 3721 = "description … maximum length"만). POST 자체가 거부돼 **등록 0·계정 변화 0**(registry 변화 0). 조치 ⑥: 기본 설명을 `saero 09-27`/`saero test 09-27`(config `description_prefix` → `saero`)로 줄이고, `add_restricted`에 **3721 폴백**(prefix만 → 설명 없음, `last_description` 기록·로그) + 시험 3개(`TestDescriptionFallback`, 시험 23→**26**).
  **2차 시도 — 등록은 성공, 판정이 틀림** [실측: 사용자 화면]: `[FAIL] 등록 실패: [{"nccAdgroupRestrictKwdId": "rst-a001-00-000002189707534", …, "keyword": "SAERO제외테스트0927", "description": "saero test 09-27", "type": "EXP_SEARCH", "delFlag": false, "regTm": "2026-09-27T04:58:36.914Z"}]` — POST는 200으로 등록됐고(설명 `saero test 09-27` 16자는 통과 → 한도는 16자 이상 29자 미만), **네이버가 영문을 대문자로 저장**해 응답 keyword가 `SAERO제외테스트0927`. `do_test_roundtrip`이 `x.get("keyword") == keyword`(대소문자 구분)로 찾다 못 찾아 "등록 실패"로 오판하고 **삭제 전에 멈춤 → 시험 검색어가 상계동필라테스에 남음**. 원상복구: 사용자가 `delete --group grp-a001-01-000000072587864 --ids rst-a001-00-000002189707534 --key-file … --confirm` 실행 → `[delete] …: 1개 삭제 요청 → registry deleted`(사용자 화면 확인) — `delete` 경로의 첫 실사용이기도 하다. registry에 `SAERO제외테스트0927` 상계동 `deleted` 1행 추가(id·경위 note).
  조치 ⑦ **대소문자 무시 대조** — `K(s) = strip().upper()`를 모든 이름 대조(`find_row`·`registration_status`·`blocked_reason`·`do_pull` 목록·`do_push` 응답/건너뜀·`do_verify`·`dry_run_plan`·`read_approved`·`do_test_roundtrip`)에 적용, 저장·표시는 원문 유지. 이 결함은 시험만이 아니라 **실제 push에서 영문 섞인 이름을 "실패/미확인"으로 오기록**할 결함이었다(`by_kw.get(k)`). FakeSender도 대문자로 저장·응답하게 바꾸고 시험 3개(`TestCaseInsensitive`: 영문 시험 문자열 roundtrip PASS, 영문 이름 push→verify 0 실패·중복 행 0·재push 건너뜀, pull 병합·경쟁사명 대소문자·승인 목록 중복) — 시험 26→**29**.
  **3차 시도 — PASS** [실측: 사용자 화면]: `[test] 등록 성공 id=rst-a001-00-000002189707543` → `[test] 다시 읽어 확인: 있음(verified)` → `[test] 삭제 뒤 확인: 없음 — 원상복구` → `[test] PASS — registry에 deleted 행으로 기록`. 등록→확인→삭제→없음 확인 4단계가 실제 계정에서 한 번 돌았고, description `saero test 09-27`은 폴백 없이 통과. registry `SAERO제외테스트0927` 상계동 `deleted` 1행(id 543, note에 2차 경위). **시험 1건 완료 — 첫 자동 회차(4항)로.**
- **4. 첫 자동 회차(2026-09-27) — 33개 × 3그룹 등록·확인 완료** [실측: 사용자 화면 + registry·스냅샷]. 순서: `propose --day 2026-09-26`(세션, 쓰기 0) → 승인 문구(신규 0 · 업종어 3 · 재등록 후보 33 · 뺀 것 5 · 이미 등록 1) → 사용자 **"등록 승인 33개"** → `work/approved_2026-09-27.txt`(33줄, 세션이 PC 폴더에 배치) → `push --dry-run`(세션·PC 양쪽: 3그룹 각 등록 예정 33·이미 등록 0·현재 183 → 216/950, HTTP 0) → PC `push`: pull(183×3) → 그룹마다 `요청 33 · 성공 33 · 이미 있음 0 · 실패 0` → 재pull(**216×3**) → `verify 33/33` ×3 → `[push] 완료: 그룹 3 · 실패/미확인 0 — 전부 다시 읽어 확인(verified)`. description `saero 09-27`(폴백 없이 통과), `regTm` 2026-09-27T05:08:19Z = **14:08 KST**, id `rst-a001-00-000002189707558`~(연번). 기호 든 이름(`노원]하루공간`·`노원역+9번출구`·`노원역;24시`·`노원역11-210`) 전부 그대로 등록됨(3723 없음, API 표기 = 원문). registry **649행 = 등록 216×3 + 시험 deleted 1**, 미등록·실패·pending 0, 세 그룹 목록 동일(216 = 216). 대조 목록 표에 요약 행 추가(아래), **재노출 판정은 9/28부터**(등록 당일 9/27 제외).
  이번 회차 사용자 명령: `pull` 2회(재pull 포함) · `test-roundtrip` 3회(1차 3721, 2차 대소문자 결함, 3차 PASS) · `delete` 1회(원상복구) · `push` 1회. 계정 쓰기: 시험 등록 2건(모두 삭제됨) + 본 등록 99건(33×3). 세션 쪽 코드 조치 ①~⑦은 전부 main에 커밋(bd7af16 · 61fe74a · 6633e2e · 75c7d46 · 087e77c · cd73cdf · 이 커밋) — **검증 회차 밖 변경이므로 다음 점검 회차가 시험 29개·[되돌리면 안 되는 것] 표와 함께 대조한다.**
- 5. 이월(첫 실사용에서 나온 것): ① PC에 git이 생겼으니 다음 회차부터 폴더 사본 대신 정식 clone(`git clone …`)으로 바꾸고 결과 파일 반영 경로를 확정 ② API description 한도 정확값(16자 통과·29자 거부 — 사이 미확인) ③ 승인 문구에 그룹별 현재 개수(propose가 오프라인이라 registry 기준 추정치) ④ `import-ui` 경로는 API가 되는 한 안 씀 — 유지 여부.

---

# 점검 기준선
점검일: 2026-09-26 (저녁 회차, Fable) — 진단만. 목표 ① 정확성(재현 시험) ② 갱신 회차 효율. 수정은 사용자가 고른 항목만, 검증은 별도 세션
결함 4건(D-10~D-13) / 개선안 5건(정확성) / 효율 개선안 4건(E1~E4) / 인용불가로 제외 0건 — **2026-09-26 수정 회차(같은 세션)에서 D-10~D-13·개선안 1~5·E1·E3·개정안 1~12·14(계획)·15 조치, E2·E4·개정안 13 이월. 아래 "수정 기록" 참고. 검증은 별도 세션**
직전 기준선(2026-09-07 저녁, 정정 2026-09-09, 커밋 cb95494 → 3cc21b6·dfc6a94) 대비: 해결 유지 3건(D-7·D-8·D-9), 미해결 2건(I-7·I-8), 이관 1건(I-9 → 점검표 개정안 2), 종결·대체 1건(I-10 → D-12), 근거없음 0건, 신규 결함 4건(D-10~D-13)

점검 대상(전부 저장소에서 받은 것): `saero-ad-report-skill` @a5ed6e0 — SKILL.md(361행) · README.md(2) · references/report-structure.md(368) ·
references/css-and-layout.md(201) · scripts/validate.py(371) · scripts/archive.py(196) · tests/mutation_test.py(249) · config/report-config.json(49) ·
audit/checklist.md(358, v4.3) · audit/last-audit.md(1,018) · .gitignore(2) · data/2026-08·2026-09 4종씩(8파일) /
`saero-pilates-report` @ad48222 index.html(**2,072행**, md5 4defb16a…, 집계 2026.08.26 — 09.25 31일) — 09-26 갱신 회차 재배포본 그대로 /
라이브 Pages: **미확인(사용자 시크릿 창 확인 요청, 답 전 결함 금지)** / 설치본 부트스트랩 SKILL.md 44행: 내용 검토(아래).
**실 CSV = 저장소 data/ 보관본 합본(기간 2026.08.26~09.25, 31일, `scripts/archive.py combine` PASS)** — 직전 갱신 회차(09-26, 배포 ad48222)와 같은 기간이라
I-9대로 CSV 실측 항목은 "직전 결과 재현"으로 갈음. 리포트 갱신·배포 없음. 실제 `data/`·config·배포본은 불변(사본에서만 실험, diff/md5 대조).
행 번호는 위 커밋의 파일 기준(view 도구 번호 = 실제 줄 번호). 바이트 수는 적지 않는다.

## 검증·병합 기록 (2026-09-27 — 검증 2 통과 → main 병합. SKILL.md·scripts·checklist 무변경)

**병합**: `fix-20260926`(최종 `587026e`)을 main(`64c7531` — 그 위 갱신 회차 커밋 없음)에 `git merge --no-ff` → 병합 커밋 **`159d2e1`**(부모 64c7531·587026e). 충돌 0 — main이 64c7531 그대로라 이 파일의 갱신 회차 절·수정 기록 절이 둘 다 브랜치 내용 그대로 살아 있음. 병합 tree = 587026e tree(diff 0 행). 브랜치 `fix-20260926`은 지우지 않고 둔다. 코드·문서 재수정 없음(이 절과 아래 "다음 점검에서 대조할 것" 3줄만). 이 절의 기록 커밋 해시는 자기 참조라 본문에 적지 않는다 — 채팅 보고·`saero-ad-report_병합_2026-09-27.md`에.
아래 "수정 기록"·"수정 기록 2" 표제의 `main 미반영`은 당시 사실 — 원문 보존, 이 절로 정정(**2026-09-27 main 반영**).

**검증 1**(`saero-ad-report_검증_2026-09-27.md`, 별도 세션): 재현 불일치 1건 — 코드가 아니라 **기록 숫자**(손 실험 `excluded_groups` 비우기 FAIL 2→3) / 판단 6건 → **수정 회차 2**(`587026e`, 아래 "수정 기록 2").
**검증 2**(`saero-ad-report_검증2_2026-09-27.md`, 별도 세션): **재현 실패 0건 → main 병합 승인.** 참고 2건(결함 아님): ① `4c08ab3`의 직전 배포는 `036080a`(재현 시험 3번째 인자 대조용 — ad48222 → 4c08ab3 → 036080a) ② `tests/mutation_test.py`에 검사 21의 **07 각주(`class="note"`) 잔존 문구 변조·0건 가드가 없음**(11·12번 본문만 덮음) → 다음 회차 후보.

**병합 main에서 전체 세트 1회 재실행** [실측] — 합본 = `data/` 보관본 combine(사본 폴더), 작업본 = 배포본 `ad48222`(git clone, md5 4defb16a…), 직전 배포본 = `4c08ab3`(md5 90288880…). 배포 저장소 HEAD `ad48222` 그대로, **PUT 없음**:
combine **PASS**(31일 · 9,525/298/338,197원 — 합본 md5 키워드 baa8e5a5·검색어 410fb327·상세지역 e3fad8b4·시간대별 d35dce58) → compute(`--competitors-html` 4c08ab3: KPI 9,519/298/3.13%/338,197원, 경쟁사 25행, 신규 변형 후보 []) → compare **OK 95 / DIFF 0** → validate **22 PASS / 0 FAIL**(출력 [PASS] 세어 22) → mutation_test 변조 22 + 0건 가드 14 + archive 7 = **43 [OK]**, [MISS]/[UNCOVERED]/[SKIP] 0, 원본 md5 전부 동일(15초) → precheck.sh(ad48222 · 합본 · 4c08ab3): validate 22 · compare 95/0 · overflow 360/390/430 넘침 0 → **"6단계 전부 통과"** exit 0(4초). 실제 `data/` 8파일·config(af2f8560)·배포본 index.html md5 전후 동일, `git status` 변경 0.
효율(재실행만, 8단계 양식 기준): 벽시계 약 30초 · 도구 호출 6회 · 즉석 코드 0행.

**부트스트랩**: 설치본 SKILL.md는 저장소 주소·받는 방법 그대로 → **재업로드 불필요(설치본 불변)**. 다음 갱신 회차부터 부트스트랩 clone이 main = 병합본(검사 22·compute/compare/precheck)을 받는다.

## 수정 기록 (2026-09-26 수정 회차, 진단과 같은 세션 — 브랜치 `fix-20260926`, main 미반영)

**브랜치·커밋**: 모든 변경은 `fix-20260926`에만 push. 코드·문서 커밋 `ea597d4`, 이 기록 커밋 `65caa1d`, 버전 줄 정정 `990bb4b`(수정 회차 1 최종 — 2026-09-27 검증 세션 확인 뒤 정정 기입). 수정 회차 2는 아래 "수정 기록 2".
main은 사용자가 검증 통과 뒤 별도 세션에서 합친다 — 그동안 갱신 회차는 main(현행 코드·검사 14개)으로 돈다.
검증 세션용: `git clone -b fix-20260926 --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill`
부트스트랩(설치본)은 손대지 않음(재업로드 없음). 실제 `data/`·config·배포본(ad48222) 변경 없음.
사용자 결정: 저장소 공개 유지(2026-09-27) → SKILL.md "원본 보관" 절에 한 줄. 라이브 시크릿 창 확인: **라이브 미확인**(답 비어 있음).
행 번호 인용은 수정 후 파일 기준을 붙였다(SKILL.md 428행·checklist 439행·report-structure 410행·validate.py 기준). 위치는 절·함수명으로.

### 조치 내역 (사용자 지정 항목만)
| 항목 | 조치(위치 = 절·함수명) | 실측 |
|---|---|---|
| D-10 | report-structure.md 01번 "차트 컨테이너" 줄 → `min-width:{max(날짜수×per_day_px, floor_px)}px` + config `chart_min_width` 참조 / 07번 `.ctr-high` 줄·04번 "CPC 값에 .ctr-high" 줄 → "클릭률 기준(config `ctr_high_threshold`, 현재 4%) 이상" / css-and-layout.md "같은 강조색" 문단·유틸 클래스 표 `.ctr-high` 행 → 같은 문구 / 버그 기록 8 `(12일 기준 960px)` → `(N일 × per_day_px, 01번과 같은 값)`. **남은 것(표)**: SKILL.md "배포 전 검산" 사고 기록 문장(`CTR 3.68%인데 4% 이상`)·css 버그 9 사고 기록(`4% 미만`)은 사고 기록 자리라 유지 / report-structure 09번 `min-width:650px`(고정값 — config 대상 아님, 그 자리에 명시) / css 버그 8 `(기본 80px / 650px)`는 config 키 병기 설명 자리라 유지 / report-structure 04번 129행 설명은 키 병기로 교체 | grep `4%\|80px\|960px\|650px` 재실행: 정의 자리 0건 [실측] |
| D-11 | report-structure.md 각 절에 "정의(compute.py 키)" 줄 12개 + 05번 top5 정의(⑬, 추가) / SKILL.md "반드시 지켜야 할 계산 규칙"에 "동률·경계·정의" 문단(07 검색어 단위 합산·동률 처리·심야 09시 배타·06 그룹 전체·10번 A/B·04 최대잔여법·07 각주 경쟁사 포함) | 문서 ↔ compute.py 대조표(아래) 13/13 일치, compare 99항목 차이 0 [실측] |
| D-12 | SKILL.md "배포 정보" 35행 문장에 `(git clone — API GET은 무인증이면 rate limit 403)` / 4단계를 `deploy.py fetch`로 바꾸고 "토큰이 없거나 API가 403이면 git clone …(진단·검증 회차)" 한 줄 | 09-11 기록(이 파일 "2026-09-11 갱신 회차" 절 `배포본은 git clone 공개 저장소로 받음(SKILL.md 4단계 대안)`)은 **당시 SKILL.md에 그 대안 문구가 없었다** — 원문 보존, 이 줄로 정정. 2026-09-26 수정으로 이제 4단계에 있음 |
| D-13 | SKILL.md 1단계 "받아야 할 파일" 표 아래 문단 → "4개 중 하나라도 없으면 combine이 FAIL로 멈춘다 — 빠진 보고서를 받아 store한 뒤 다시. 부분 갱신 경로는 없다". `--allow-missing` 류 옵션 없음 | grep `직전 데이터로 두고\|나머지만 갱신`: SKILL.md·references·checklist 0건(이 파일의 D-13 결함 표 인용 원문만 남음) [실측] |
| 개선안 1 | validate.py `check_media_top5`(라벨·값·순서·색 = 키워드 CSV `매체이름` 상위 5, 0건 가드)·`check_cards_vs_04`(카드 큰 숫자 = `parse_04_rows` 순위 셀, 0건 가드). mutation_test.py 변조 `05 mediaChart 첫 값 +1`·`06 첫 카드 큰 숫자 +0.01` + 가드 `mediaChart id 변조`·`06 카드 등록 문구 변조` | 역검증: feed999(29일) → `05번 mediaChart top5` FAIL(5위 에펨코리아 501 vs CSV 통합검색 PC) / 036080a(30일) → `06번 카드 큰 숫자` FAIL(노원산전 카드 1.70 vs 04번 1.69) / 4c08ab3 → 두 검사 PASS [실측] |
| 개선안 2 | validate.py `check_competitors`: (16) config `competitors` 이름을 포함하는 검색어가 경쟁사표 밖이면 FAIL(순방향만, 역방향 검사 없음 — 주석 명시) (17) 경쟁사표 각 행 노출·클릭 = 검색어 CSV. mutation 변조 `검색어 CSV 첫 행 검색어를 config 경쟁사명 포함으로`·`07 경쟁사표 첫 행 노출 +1` + 가드 `경쟁사표 name-cell 변조` | ad48222: 표 밖 0건·25행 일치 [실측] |
| 개선안 3 | validate.py 검사로 넣음(별도 스크립트 아님 — mutation이 덮게): `check_11_12` (19) 항목 수 ≤8·(참고) ≤2·판정 줄 합 (20) 금칙어 5종 0건 (21) 잔존 문구 5종 0건. 범위는 `reportlib.section`이 12번을 `<script>` 앞에서 끊음. mutation 변조 3 + 가드 3. SKILL.md "배포 전 검산"·report-structure 11번 수동 검사 문단 반영 | ad48222: 7+2, 7=6+1+0, 금칙어·잔존 0건 [실측] |
| 개선안 4 | validate.py (18) `검색어 CSV 클릭 합계 = KPI 클릭` — 종전 `참고` print 삭제. **지시문의 "기존 변조(검색어 CSV 클릭 −1)"는 없었음**(기존 것은 `시간대별 CSV 첫 행 클릭 −1`로 검사 3 대상 — FAIL 사유 그대로) → `검색어 CSV 첫 행 클릭 −1` 변조를 새로 추가 | 변조 → `검색어 CSV 클릭 합계` FAIL [실측] |
| 개선안 5 | mutation_test.py `archive_experiments()`: data/ 사본에서 기준 combine PASS 뒤 7종(store 옛 다운로드·두 달 걸침 / combine 시간대별 +1·개업 달 제거·헤더 빈틈·검색어 경계 불일치·검색어 종류 누락) 전부 `[FAIL]`, 끝에 실제 data/ 8파일 md5 대조. `tests/overflow_check.py`(playwright, 360/390/430px, 배포본 경로 인자). SKILL.md 6단계 3항·checklist 파괴 실험 절 반영 | 7/7 [OK], overflow 360/390/430 PASS, md5 전부 동일 [실측] |
| E1 | `scripts/compute.py`(합본 4종 + config [+ 직전 배포본] → JSON, 키 "KPI","01"~"10" 자리별) · `scripts/compare.py`(index.html vs JSON 99항목) · `scripts/reportlib.py`(공통 헬퍼 — 읽기·제외그룹 필터·일수·섹션 자르기까지, 값 계산 공유 금지를 docstring·validate.py docstring에 명시). SKILL.md 5단계 "compute.py 출력값만 — 즉석 계산 금지", 6단계에 compare(차이 0) | compute+compare로 ad48222 재현 **99 OK / 0 DIFF** [실측] |
| E3 | `scripts/ingest.sh`(store→combine→data push, `set -euo pipefail`) · `scripts/precheck.sh`(validate→compute+compare→overflow) · `scripts/deploy.py`(fetch/push/verify, sha 재조회 내장, 토큰은 파일, `--dry-run`, 계산 로직 없음). SKILL.md 1·4·6·7단계 | precheck.sh 통과 / deploy.py `push --dry-run`: 로컬 md5 4defb16a 전후 동일·배포 저장소 main ad48222 전후 동일·PUT 없음, `verify` 재수령본 md5 일치 [실측] |
| 개정안 8 | SKILL.md **8단계 신설**(audit 기록 양식: validate 개수·compare 차이·overflow·md5·**효율 3항목**) | — |
| 개정안 1~7·9~12·15 | checklist.md v4.4 — 머리말(2회 커밋·구조 변경 예정), [시작 전 확인 ②](합본·I-9), 1) 대상 목록, 라이브 절(web_fetch 대조군 삭제), 3) 설치본 매 회차, [의도된 동작] 16개, [되돌리면 안 되는 것] 18행, 실 CSV 항목 종결, 파괴 실험 절(archive 7종·overflow), [판정 기준](행수·md5·grep·직전 세션·효율), [마무리](2회 커밋·PC push·토큰 폐기·고를 항목), 기준선 양식(점검 대상·효율 기준선) | 개정안 13 미채택(그대로), 14는 계획만 |
| P6 | SKILL.md "원본 보관" 절 `사용자 결정(2026-09-27): 공개 유지` | — |

### D-11 문서 ↔ compute.py 대조 (수정 회차 규칙 1 — 같은 규칙인지 항목별로)
| # | 정의 | report-structure.md | compute.py | 일치 |
|---|---|---|---|---|
| ① | 06 rankChart = 노원역필라테스 그룹 전체 가중순위 | 06번 "정의(compute.py 06.rankChart)" | `nw = pw[광고그룹=="노원역필라테스"]`, `wrank(nw[일별==d])` | ✓ 31/31 |
| ② | 07 클릭0 각주 경쟁사 포함 / 목록은 제외 | 07번 (3) 정의 | `클릭0전체 = gs` 전체, `클릭0목록 = gen`(경쟁사 제외) | ✓ 563/1,885 |
| ③ | 10번 A = 검색 & `네이버` 접두 전부 | 10번 표 정의 | `isn = 매체이름.startswith("네이버")`, `iss & isn` | ✓ 7,639/296 |
| ④ | 09 심야 22·23·0~8시 | 09번 정의 | `night = [22, 23] + range(0, 9)` | ✓ 2,012/65 |
| ⑤ | 08 TOP10 노출↓(동률 클릭↓) | 08번 정의 | `gr.sort_values(["노출","클릭"], desc)` head(10) | ✓ |
| ⑥ | 06 카드 = 최근 7일 노출 있는 신규 그룹, OFF 제외 | 06번 카드 정의 | `pw[일별.isin(days[-7:])]["노출수"].sum() > 0` | ✓ 2개 |
| ⑦ | 동률: 정식표 노출↓·경쟁사표 클릭↓·목록 직전 순서 | 07·08번 정의 | `sort_values(["클릭","노출"])`·`(["노출","클릭"])`·compare는 집합+정렬 방향 | ✓ |
| ⑧ | 04 최대잔여법 | 04번 정의 | `lr_share()` | ✓ 92.8/3.8/1.5/1.0/0.9 |
| ⑨ | 01 순위 민트 = 닷새 최솟값 | 01번 ② 정의 | `순위민트 = min(rank5)` | ✓ 9/25 |
| ⑩ | 08 지역명 축약 | 08번 컴팩트 정의 | compare.py `short()` (compute는 원명) | ✓ |
| ⑪ | 06 매칭표 순위 1자리, 카드 N일차 = 등록일 포함 | 06번 정의 | `mrow` round 1, `(마지막날 − 첫 노출일).days + 1` | ✓ 3.0/2.0·26·24일차 |
| ⑫ | 07 검색어 단위 합산, 뱃지 노출 많은 유형, 동률 직전 뱃지 | 07번 (1) 정의 | `gs = sr.groupby("검색어")`, `badge` + `*동률` | ✓ 19행, 동률 0 |
| ⑬(추가) | 05 top5 = 매체이름 노출 상위 5, 색 = 캠페인 유형 | 05번 정의 | `m5.head(5)`, `mtype` | ✓ + validate 검사 14 |

### 검증 회차가 재현할 실측 (전부 이 세션 실측, 브랜치 코드로)
- `python3 scripts/compute.py /home/claude/work/combined --competitors-html <ad48222 index.html> -o compute.json` → `python3 scripts/compare.py <ad48222> compute.json` : **OK 99 / DIFF 0**, exit 0.
- `python3 scripts/validate.py <ad48222> <합본 4종>` : **검사 22개 PASS 22 / FAIL 0**(출력 세어 22 — 14 + 8: 05 top5·06 카드·경쟁사 순방향·경쟁사표 값·검색어 클릭합·11번 항목/판정·금칙어·잔존 문구). config `date_based_sections` [1]이면 21.
- `python3 tests/mutation_test.py <ad48222> <합본 4종>` : 기준 22 PASS → 변조 22 [OK] + 0건 가드 14 [OK] + config 실험 2 + **archive 7/7 [OK]**, 커버리지 22/22, [MISS]/[UNCOVERED]/[SKIP] 0, 원본 md5(html·CSV 4·data/ 8) 전부 동일, exit 0 (약 14초).
- `python3 tests/overflow_check.py <ad48222>` : 360·390·430 PASS(scrollWidth = 뷰포트), exit 0. `bash scripts/precheck.sh <ad48222>` : 전부 통과.
- `python3 scripts/deploy.py push --token-file <아무 유효 토큰> --file <ad48222> --message x --dry-run` : `[dry-run] PUT을 보내지 않음`, 로컬 md5 4defb16a… 전후 동일, 배포 저장소 main ad48222 전후 동일. `verify` : 재수령본 md5 일치.
- 역검증(과거 배포본 + 그 기간으로 자른 합본, 시간대별은 그 배포본 09번 배열): feed999 → 21 PASS / 1 FAIL(`05번 mediaChart top5`) · 036080a → 21/1(`06번 카드 큰 숫자` 1.70 vs 1.69) · 4c08ab3 → 21/1(`11·12번 잔존 문구` 확인 요청 1·판단 요청 2·확인 중 1 — 답 대기 배포라 정상, `--pending`이면 22 PASS).
- 손 실험(사본): config 삭제 → `설정 파일이 없습니다` exit 1 / `excluded_groups` 비우기 → KPI 9,519→9,525 FAIL **3건**(KPI 타일·08·09번 각주·05 top5 — 검사 14가 제외 그룹을 읽으므로. 2026-09-27 검증 판단 1로 2→3 정정, 재실측).
- 실제 `data/` 8파일·config·배포본 index.html md5 불변(mutation 마지막 줄 + `git status`에 data/·config 변경 없음 + 배포 저장소 HEAD ad48222).

### 효율 — 진단 회차 기준선 대비 (같은 재현 시험)
| 항목 | 진단 회차(즉석 코드) | 수정 회차(compute+compare) |
|---|---|---|
| 벽시계 | 약 5분(마크업 확인 → 대조 0건) | **약 15초**(precheck.sh 1회 — validate·compute·compare·overflow) |
| 도구 호출 | 17회(마크업 확인 9·작성 3·실행 5) | **1회**(precheck.sh) |
| 새로 쓴 코드 | 290행(회차 폴더에만) | **0행**(저장소 scripts/) |
(2026-09-27 검증 판단 2로 SKILL.md 8단계 문구와 통일: "precheck.sh 1회·약 15초·0행, 재현 시험 — 계산·대조만")
E2(기계 자리 자동 교체)·E4(부트스트랩 읽기 분량 축소, P5 분리와 짝)는 이월. E3의 실측은 다음 갱신 회차가 8단계 양식으로 벽시계·호출 수·즉석 코드를 적어야 생긴다.

### 원래 제안·지시를 바꾼 곳 (B 검증이 볼 것)
1. 검사 20(금칙어·잔존 문구 0건)을 **둘로 나누고** 잔존 문구 검사에 `--pending` 허용을 넣었다 — 역검증에서 4c08ab3(사용자 답을 기다리며 채팅 질문을 남긴 정상 배포)이 잔존 문구로 FAIL했기 때문. 기본은 엄격, 답을 반영한 재배포엔 붙이지 않는다(SKILL.md 6단계·[의도된 동작] 15).
2. 개선안 4 지시의 "기존 변조(검색어 CSV 클릭 −1)"는 존재하지 않았다(기존은 시간대별) → 검색어 변조를 신설했고 시간대별 변조는 그대로 검사 3을 겨냥.
3. 개선안 3은 별도 스크립트가 아니라 validate.py 검사 19~21로 넣었다(mutation_test가 덮고 개수를 세게).
4. [의도된 동작]은 15 + 이번 회차 산물 1(16번)로 16개. "되돌리면 안 되는 것" 18행.
5. compute.py에 05번 top5 정의(⑬)를 더했고 02번 비중도 최대잔여법으로 통일(값 동일 92.8/7.2). deploy.py에 `verify` 서브명령(재수령본 md5)을 더했다(지시엔 GET/sha/PUT만).
6. E1 헬퍼 공유 범위: reportlib에 `section()`(섹션 자르기, 12번은 `<script>` 앞에서)도 넣었다 — 값 계산이 아니라 자르기이므로 지시 범위 안으로 봄.
7. archive.py 코드·docstring은 바꾸지 않았다(변경 없음). validate.py docstring은 22개 목록으로 갱신.

### 다음 회차(검증 뒤 main 병합 후)에 볼 것
- 갱신 회차가 8단계 양식으로 효율 3항목을 적는지 / compute.py `신규변형후보`가 뜬 회차에 경쟁사표 행이 추가됐는지 / `--pending` 남용 여부(답 반영 재배포에 붙어 있으면 결함).
- E2·E4·개정안 13·14(파일 분리) 재상정.

## 수정 기록 2 (2026-09-27, 검증 회차 판단 6건 처리 — 브랜치 `fix-20260926`, main 미반영)

검증 보고 `saero-ad-report_검증_2026-09-27.md`는 이 세션에 첨부되지 않았다 — 사용자 메시지에 요약된 6건과 지정 위치로 처리했다.
커밋: 이 절을 포함한 커밋 해시는 자기 참조라 본문에 적지 않는다 — **검증 세션이 `git log -1 --oneline`으로 확인해 적는다.**
main 미반영, 배포(PUT) 없음, 실제 `data/`·config(af2f8560)·배포본 ad48222(4defb16a) 불변 [실측].

### 처리 내역
| # | 판단 | 조치(절·함수명) | 실측 |
|---|---|---|---|
| 1 | 10-2 FAIL 2→3 | 이 파일 수정 기록 1 "검증 회차가 재현할 실측" 손 실험 줄 정정 | `excluded_groups` 비우기 → KPI 타일·08·09번 각주·05 top5 FAIL 3건 재실측 |
| 2 | 효율 문구 통일 | SKILL.md 8단계 문단 + 수정 기록 1 효율표 → "precheck.sh 1회·약 15초·0행(재현 시험 — 계산·대조만)" | precheck.sh 1회 통과(아래) |
| — | 기록 커밋 정정 | 수정 기록 1 "이 기록 커밋 = 브랜치 HEAD" → `65caa1d`(+ 버전 줄 정정 `990bb4b`) | — |
| 3 | compare 08 컴팩트 | compare.py 08 절: 순서 대조 1항목 → **집합(지역명 축약) + 정렬 방향(클릭↓, 동률 노출↓)** 2항목. docstring "동률 자리" 줄과 일치 | 95 OK / 0 DIFF |
| 4 | 동률 원칙 한 문장 | report-structure.md 07번 (2) 클릭1건 정의 줄 · SKILL.md "동률·경계·정의" 문단 · checklist [의도된 동작] 4 · compute.py `07.클릭1` 주석 — 코드 변경 없음 | grep "동률 원칙(2026-09-27)" 3곳 + compute 주석 1곳 |
| 5 | `--pending` 일원화 | validate.py `check_11_12` 검사 21 범위 → 07번 각주(`class="note"`)·11·12번 본문(<script> 앞), 세 범위 중 하나라도 못 찾으면 0건 FAIL, 이름 `07 각주·11·12번 잔존 문구 0건` / compare.py 잔존 문구 5항목 삭제(99→95) / precheck.sh `[--pending]`을 validate에만 / SKILL.md 6단계 사용법·8단계 양식(`--pending` 사용: 아니오/예 — 채팅 질문 N건)·검산 목록 / checklist [되돌리면 안 되는 것] 행 / mutation_test 변조·가드 대상 문자열 `잔존 문구`(기준값 변화 없음: 변조 22·가드 14·archive 7) | 4c08ab3(그 기간 CSV): `--pending` 없이 21 PASS / 1 FAIL(07 각주 0건 + 11·12번 4건: 확인 요청 1·판단 요청 2·확인 중 1), 있으면 22 PASS. precheck.sh(직전 배포본 036080a): 없이 → validate에서 exit 1, 있으면 → validate 22·compare 95/0·overflow 0 "6단계 전부 통과" |
| 6 | precheck 직전 배포본 인자 | precheck.sh 인자 3개 필수 `<작업본> <합본폴더> <직전 배포본>` + md5 같으면 `[FAIL] 직전 배포본이 작업본과 같다 — 4단계 fetch 파일(/home/claude/work/prev.html)을 넣어라` exit 1, compute `--competitors-html`에 직전 배포본 / SKILL.md 4단계 fetch `--out /home/claude/work/prev.html` + `cp` 작업본, 5·6단계 사용법 통일, 진단 회차 재현 시험은 그 배포본의 직전 배포를 넣는다고 명시 | (c) 모의 재현: ad48222 사본 경쟁사표에 config 밖 브랜드 행 `RHA필라테스상계`(CSV 노출 1·클릭 0·0원) 추가 → 옛 호출(작업본을 `--competitors-html`로) validate 22 PASS·compare 95/0(무력화 재현) / **새 precheck.sh(직전 = ad48222 실물) → compare OK 94 / DIFF 1 `07 경쟁사표(집합)`, exit 1** / 작업본=직전 인자 → 즉시 exit 1 |
| 기록 | (c) 알림 없음 | "다음 점검에서 대조할 것"에 후보 추가(config 별칭 등) | — |
| 기록 | overflow Chart.js | checklist [의도된 동작] 17 | — |

### 전체 재실행 (브랜치 코드, 배포본 ad48222 + 합본 4종)
combine PASS(합본 4종 md5 09-26과 동일) → compute → compare **OK 95 / DIFF 0** → validate **22 PASS**(세어 22) → mutation_test 변조 22 + 0건 가드 14 + archive 7 = 43 [OK], [MISS]/[UNCOVERED]/[SKIP] 0, 원본 md5 전부 동일 → overflow 360/390/430 넘침 0 → precheck.sh(작업본 ad48222, 직전 배포본 **4c08ab3**) "6단계 전부 통과" exit 0 → 실제 data/·config·배포본 md5 불변, 배포 저장소 HEAD ad48222.

### 원래 제안·지시를 바꾼 곳
1. 검사 21의 "07 각주" 범위를 07번 섹션 전체가 아니라 `class="note"` 요소로 잡았다 — 정식표·목록 본문에 "대기"·"확인 중" 같은 검색어가 들어올 수 있어 오검출을 피하기 위해. 4c08ab3에서 07 각주는 0건이라 지시의 실측 결과(1 FAIL)는 같다.
2. compare 항목 수는 99 − 잔존 문구 5 + 08 컴팩트 정렬 1 = **95**(지시의 "99→N"의 N). 수정 기록 1의 99는 당시 사실이라 원문 보존.
3. precheck.sh를 진단 회차 재현 시험에 쓰려면 3번째 인자에 현재 배포본이 아니라 그 직전 배포(ad48222 → 4c08ab3)를 넣어야 한다 — 같은 파일 가드가 막으므로. SKILL.md 6단계·checklist 16에 명시.
4. 수정 회차 1의 효율표 수치(약 10초·1~2회)를 지시대로 "약 15초·1회"로 통일했다(precheck.sh 한 번이 validate·overflow까지 포함).

### 이월
E2·E4·개정안 13·14(파일 분리)는 그대로. config 별칭(아래 "다음 점검에서 대조할 것") 신설 여부는 다음 진단 회차가 올린다.

## 0. 시작 전 확인 [실측]
- 부트스트랩 44행: 41행 `설치 경로(`/mnt/skills/plugins/...`)`는 실제 경로 `/mnt/skills/plugins/saero-ad-report/SKILL.md`와 일치, 22~29행 받기 실패 절차 적절 → **그대로(재업로드 불필요)**. 설치 폴더의 references/report-structure.md(291행, md5 80854b7b…)·css-and-layout.md(179행)·scripts/validate.py(185행)는 저장소(368·201·371행)보다 낡았고 archive.py는 없음 — 부트스트랩 37행 "참조 문서·스크립트도 받은 저장소 안의 것을 쓴다"가 있어 결함 아님. 재업로드할 일이 생기면 그때 사본을 패키지에서 빼면 된다(선택).
- 점검표 1) 대상 목록(checklist 83~86행)에 없는데 실제 ls에 있는 것: `scripts/archive.py`·`data/`·`tests/` 폴더 자체. → 개정안 10.
- 배포본 clone: 커밋 `ad48222`, index.html 2,072행, masthead `2026.08.26 — 09.25 (31일)`, og `8/26~9/25 주간 성과 요약`. 라이브는 web_fetch를 쓰지 않았고(점검표 98~100행 규칙) 사용자에게 시크릿 창 확인을 요청함 — 확인 항목: masthead 위 문구 · KPI 9,519 / 298 / 3.13% / 338,197원 · 집계 기준 "클릭률 강조: 01·07번 표에서".
- 다른 세션의 push 여부: push 직전 `git pull --rebase`로 확인(아래 마무리).

## 1. 재현 시험 (P1) — 차이 0 [실측]
합본 4종으로 SKILL.md·report-structure.md 규칙(+ 갱신 회차 기록의 재현 정의)대로 12개 섹션 값을 전부 다시 계산해 배포본 ad48222와 항목별 대조: **99개 항목 OK / 차이 0**.
대조 항목: masthead·og:description·KPI 타일 4 + sub 3 / 01 dailyChart 노출·비용 31개·labels 31·min-width 2480·일별 표 5행(값+`.ctr-high` 3칸)·순위 5칸(3.11·3.61·3.22·2.98·2.38, 민트 = 9/25)·검색지면 3.83%(7,773·298)·상향 후/전 평균(14,052·9.3·1,506 / 9,658·7.2·1,344)·누적 가중순위 3.04·콘텐츠 1,746 / 02 92.8%·groupChart·costPie / 03 31행 전부 + 합계 행 + 최고일 9/22 22,597원 / 04 표 5행 전부(예산 비중 최대잔여법 92.8/3.8/1.5/1.0/0.9 = 이번엔 단순 반올림과 동일, CPC 격차 3.57, 파워링크 비중 7.2%) / 05 mediaChart top5 라벨·값·색(3796·2307·999·828·516)·deviceChart·모바일 80.8% / 06 rankChart **31개**(그룹 전체 가중)·min-width·매칭표 2행·9/25 직접 7·자동 50·카드 2개(등록일·일차·큰 숫자)·**카드 큰 숫자 = 04번 셀(2.59·1.67)** / 07 정식표 19행(값·뱃지·`.ctr-high` 전부)·클릭1건 22개 집합+노출 내림차순·클릭0 목록 집합+정렬·클릭0 각주 563/1,885·확장·클릭0 행단위 53/59/50(34개)·경쟁사표 25행 집합+정렬·상위2 46%·클릭 합 298 / 08 TOP10·컴팩트 32개·75건(순서 포함)·클릭0 153/1,146·각주 9,525/9,519/6·노원 46%·49%·타겟 62%·60%(CTR 3.02)·확인불가 447·23·28,975(8.6%, 5.15%)·타겟 밖 서울 1,351·54·4.00%·서울경기 밖 2.7%·11위 의정부 122 / 09 hourly 24×2·심야 2,012·65·60,112(21%·22%)·최다 15시 27·2위 13시 22·각주 / 10 A/B/C/D·placementChart·9/6 이후 20일 노출·클릭 나열·하루 평균 9.9·파트너 9/25 3회 / 11 항목 7+(참고)2·판정 줄 6+1+0=7·금칙어 5종 0건(11·12 본문 — `<script>` 주석의 `필요` 2건은 범위 밖) / 07·11·12 잔존 문구(확인 요청·판단 요청·기다림·확인 중·대기) 0건.
09-25(05번 5위)·09-26(06번 카드) 누락 유형 두 자리: 이번 배포본에선 둘 다 일치. 09-26 기록의 "합본 시간대별 − 직전 배포본 09번 = 194회·8건"도 036080a로 재현.

**갱신 회차 효율 기준선(이번 재계산 실측)**: 벽시계 약 5분(13:43 배포본 마크업 확인 시작 → 13:48 대조 0건), 도구 호출 17회(그중 배포본 마크업 확인 view/grep 9회·스크립트 작성 3회·실행/수정 5회), 새로 쓴 코드 290행(`recalc.py` 143 + `compare.py` 147, 회차 작업 디렉토리 `/home/claude/work/`에만 둠 — 저장소 미포함). 근거 인용: 09-25 갱신 회차 "첫 응답에서 계산·교체·validate까지 마치고 **도구 사용 한도에 걸려** 배포 직전 멈춤", 09-26 갱신 회차 "두 번째 응답에서 01~10번까지 반영 후 **도구 한도로 멈춤**", 09-23 갱신 회차 "**계산 스크립트는 회차 작업 디렉토리에만 둠**"(09-19·09-20·09-21도 같은 문구) — 매 회차 즉석 코드를 새로 쓰고 버린다.

**재현에서 드러난 것(차이는 0이지만 (c) 유형)**: 아래 정의 12개가 SKILL.md·report-structure.md에 없고 갱신 회차 기록에만 있다. 문서만 따르면 값이 갈리는 것을 실측함 → 결함 D-11.

## 2. 검사 생존 (P2) [실측]
- validate.py(합본 + ad48222): **[PASS] 14줄, exit 0**(세어서 14). 검색어 CSV 클릭합 298 = KPI → 참고 출력 없음.
- `tests/mutation_test.py`: 기준 14/14 PASS → 검사별 변조 14개 전부 [OK] FAIL, 0건 가드 8종 [OK], config 실험 2종(ctr 5% 라벨 2건 반영 · date_based_sections [1]→13개) [OK], **[MISS]/[UNCOVERED]/[SKIP] 0**, 원본 md5 전부 동일, exit 0 (8.0초).
- 손 실험(사본): config 삭제 → 검사 시작 전 `설정 파일이 없습니다` exit 1 / `excluded_groups` 비우기 → 기준 KPI 노출 9,519 → 9,525, `KPI 타일`·`08·09번 각주` FAIL 2건.
- archive.py 파괴 실험(사본 디렉토리, 실제 data/ diff 없음): ① 옛 다운로드(9월 헤더 끝 09.20) store → `기간 끝 2026-09-20가 보관본 키워드.csv의 끝 2026-09-25보다 앞섬` FAIL ② 시간대별 첫 행 노출 +1 → `시간대별 노출 7,163 ≠ 키워드 7,162` FAIL ③ 8월 폴더 제거 → `합본 일별 최솟값 2026.09.01. ≠ 개업일 2026.08.26.` FAIL ④ 검색어 헤더 09.02 시작 → `조각 2026-08-01~2026-08-31 다음이 2026-09-02~2026-09-25 — 빈틈 또는 겹침` FAIL ⑤(추가) 두 달 걸친 헤더(08.27~09.25) store → `두 달에 걸침` FAIL.
- **미실측 경로 `store --chunk` 첫 실측 — 통과.** 9월 4종을 1~24 + 25 조각으로 나눔(시간대별 9/25분은 9월 파일 − (직전 배포본 036080a 09번 배열 − 8월 파일)로 역산 = 194회·8건, 비용 12,014원은 클릭 비례 배분, 순위 열은 두 조각 모두 원본 값). 1~24 조각 store는 기간 끝이 보관본보다 이르다며 거부(정상, `--force`로 저장), 25 조각 `store --chunk` → `키워드_2.csv` 등 4개 생성. combine이 3조각(8/1~8/31, 9/1~9/24, 9/25)을 인식·PASS했고 **합본 4종이 단일 파일 combine과 전부 동일**(키워드·검색어·상세지역 행 집합, 시간대별 노출·클릭·비용·순위). 검색어만 23/24로 나누면 `검색어 조각 경계 … ≠ 키워드 …` FAIL → 경계 4종 대조 작동.
- **mutation_test.py는 archive.py를 덮지 않는다**: 82~84행이 `scripts/`·`config/`를 복사하지만 102행은 `validate.py`만 실행. combine 검사 5종·store 거부 2종은 위처럼 손으로 재현했다 → 개선안 5.

## 직전 기준선 판정
| 항목 | 판정 | 근거(지금 원문) |
|---|---|---|
| D-7 설정값 사본(SKILL.md) | 해결 유지 | SKILL.md 198행 `이미 확인된 경쟁사 목록은 `config/report-config.json`의 `competitors`다.` / 248행 `목록은 `config/report-config.json`의 `excluded_groups`` / 280행 `- 타겟 지역 = `config/report-config.json`의 `target_districts`` — references 쪽 잔여는 D-10 |
| D-8 검사 라벨 f-string | 해결 유지 | validate.py 322·331·339행 `f"07번 클릭률 {CTR_HIGH:g}% 이상에만 .ctr-high"` 등. mutation config 실험 `ctr_high_threshold 4.0→5.0: 라벨에 5% 반영 2건` [실측] |
| D-9 06번 min-width·라벨 검사 | 해결 유지 | validate.py 224행 `for num in DATE_SECTIONS:` / 235행 `def check_date_labels(html, ndays):`. 실행 출력 `01번 차트 min-width`·`06번 차트 min-width`·`날짜축 x축 라벨 개수 = 날짜수 — 배열 2개 [31, 31]` [실측] |
| I-7 검색어 클릭합 참고 출력 | 미해결(이월) | validate.py 356~358행 `if sr_clicks != kpi_clicks:` → `print(f"\n참고: …확인 필요")` — FAIL 아님, exit 0 |
| I-8 config competitors ↔ 07 표 대조 | 미해결(이월) | validate.py에 `competitors` 참조 0건(grep). 코드 소비자 없는 config 필드는 이제 **3개**(`competitors`·`target_districts`·`excluded_group_keywords`) — `open_date`는 archive.py 47행이 읽기 시작 |
| I-9 같은 기간 CSV → 재현 갈음 | 이번 회차 실적용(사용자 지시) → 개정안 2 | checklist 39~62행 [시작 전 확인 ②]는 여전히 "4종 업로드 없으면 멈춰라"만 있음 |
| I-10 4단계 GET `Authorization` "(선택)" 표기 | **종결·대체 → D-12** | 무인증 `api.github.com` GET은 rate limit **403**(이번 회차 실측 `API rate limit exceeded` + 09-11·09-21 기록) — "(선택)"으로 적으면 오히려 틀린다. 토큰 없는 경로는 `git clone`인데 SKILL.md에 없음 |
| 라이브 web_fetch 캐시 확정 | 유지 | 이번 회차 web_fetch 미사용(지시), 사용자 시크릿 창 확인 요청. 대조군 재확인(checklist 107~108행)은 개정안 9로 삭제 제안 |
| 노원M필라테스 자연 소멸 판단 | 해결(09-09 종결) | 경쟁사 판정 이력 표 `노원M필라테스 … **종결(자연 소멸)** — 09-09` · 09-14 `표 미복귀(사용자 결정)` |
| 제외그룹 노출 지속 | 변화 없음 | 합본 `노원필라테스(삭제)` 노출 6·클릭 0(8/26 5·8/31 1). validate 출력 `제외 전 전체 — 노출 9,525 / 클릭 298 (차이: 노출 6회 / 클릭 0회)` |
| 다음 점검 대조: 01·06 min-width 상향 | 해결(매 회차 검사) | 09-09~09-26 갱신 회차 기록 전부 `01·06 min-width N → N+80, 라벨 [d, d]` |
| 다음 점검 대조: 06 파괴 실험·`[1]`→13개·검사 14 | 재현 [실측] | mutation 출력 `06번 min-width −60px → FAIL` / `date_based_sections [1, 6]→[1]: 검사 14→13개, 사라진 섹션 검사 [6]` |
| 다음 점검 대조: masthead 형식·예산 비중 반올림 오탐 | 없음 | 14 PASS. 최대잔여법 표시값은 [의도된 동작] 1 |
| 미채택 개정안 6~10 재상정 | 6 → 개정안 2 / 7 → 개정안 9·11 / 8 → 재상정(개정안 13) / 9·10 → **종결**(v4.3 mutation_test.py에 06 min-width 변조·config 실험 포함, 이번 회차 [OK]) | mutation 출력 `06번 min-width −60px`·`ctr_high_threshold 4.0→5.0` |

## 결함 (미조치 — 사용자가 고른다)
| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 실측/추론 | 왜 틀렸는지 | 수정 방향 | 작업경로·반영 |
|---|---|---|---|---|---|---|---|---|
| D-10 | 하 | references/report-structure.md · references/css-and-layout.md | rs 63 · rs 198 · css 22–23 · css 44 · css 175 | rs 63 `` `<div style="height:280px; min-width:{날짜수×80}px;">`. 최소 650px `` / rs 198 `- 클릭률 4% 이상인 행만 `<td class="num ctr-high">`.` / css 22–23 `"클릭률 4% 이상"에 배정돼 있으므로 … 클릭률 4% 이상, 그 외 용도 금지.` / css 44 `.ctr-high     클릭률 4% 이상 강조` / css 175 `(12일 기준 960px)` | **실측** — mutation config 실험: `ctr_high_threshold` 5.0이면 validate 라벨은 `5% 이상`인데 문서는 4% 그대로. css 175의 예시값은 이미 낡음(지금 31일 2,480px) | SKILL.md 41~44행 규칙("값을 정의하는 자리는 값을 적지 않고 설정 파일의 키를 가리킨다")을 references가 어김. 09-07 D-7이 "이번 지시 범위(SKILL.md 세 곳) 밖 — 다음 회차 판단"으로 남긴 자리 그대로 | rs 63 → `min-width = max(날짜수×per_day_px, floor_px), 값은 config chart_min_width` / rs 198·css 22–23·44 → "클릭률 기준(config `ctr_high_threshold`, 현재 4%) 이상" 식으로 키 병기 / css 175 예시 삭제 또는 "N일 × per_day_px" | 스킬 저장소 push — 즉시 다음 갱신 회차에 반영 |
| D-11 | 중 | references/report-structure.md (+ SKILL.md 272~285) | rs 159–165 · 203–205 · 256–265 · 245 · 220 · 167–175 · 194 · 213–214 · 224 · 125 · 71–72 · 163·175 · 195–197 | rs 161 `라인 차트(`rankChart`) + 키워드 매칭 방식 비교표.` / 205 `끝에 클릭 0 검색어 전체 건수·노출 합계를 각주로.` / 256~265 10번 절에 "매체 변경 항목별 실제 성과" 표(A~D 4행) 정의 없음 / 245 `심야(22시~09시) 콜아웃은 노출·클릭·비중·비용을 매주 갱신.` / 220 `시/군/구 단위 노출·클릭·비용 TOP 10 표` / 167~175 신규 키워드 요약 카드 절에 OFF·제거 규칙 없음 / 194 `클릭 2건 이상인 검색어만, 클릭수 내림차순, **개수 제한 없이 전부**` / 213 `경쟁사 브랜드명 검색어 표 (소재구 컬럼 포함).` / 224 `형식: `지역명(노출N·클릭N)` 클릭수 내림차순.` / 125 `합이 100%인지 검산` / 72 `**② 플레이스 광고 평균노출순위** — 5칸 숫자 그리드.` | **실측** — 문서만으로 가능한 다른 해석의 산출값: ① 06 rankChart를 직접 등록 키워드만으로 → 31일 중 **일치 0**(배포본은 그룹 전체 가중) ② 07 클릭0 각주에서 경쟁사 제외 → **541개·1,798회**(배포 563·1,885) ③ 10번 A를 통합검색·플레이스 4매체만 → **7,618·293**(배포 7,639·296, `네이버 검색탭` 10·1건·`광고더보기` 11 포함해야 맞음) ④ 심야에 09시 포함 → **2,471·86·87,372원**(배포 2,012·65·60,112 — 09시 배타) ⑤ 08 TOP10을 클릭 기준 → 성남 수정구·강북구·영등포구 대신 서초·성동·중랑 ⑥ 06 카드에 OFF 그룹 유지 → 노원키즈 카드(1.95위·24일차) 추가 ⑦ 동률 정렬(07 정식표 노출↓·경쟁사표 클릭↓ 후 직전 순서·클릭1건/클릭0/컴팩트 목록) 미명시 — 이번엔 정식표 동률 없음, 경쟁사표 동률 8쌍은 직전 순서 ⑧ 04 최대잔여법(09-24 3.955→3.9, 09-25 92.545→92.6은 단순 반올림과 달랐음) ⑨ 01 순위 그리드 민트 = 닷새 중 최솟값 ⑩ 08 지역명 축약(`서울특별시 ` 생략·`전남광주통합특별시 북구`→`광주 북구`·`세종특별자치시`→`세종시`) ⑪ 06 매칭표 순위 소수 1자리(2.95→3.0)·04는 2자리, 카드 "N일차" = 등록일 포함 일수 ⑫ 07 검색어 단위 합산(유형 분리 시 정식표 20행 vs 19+경쟁사 2) | 이 정의들은 09-11~09-26 갱신 회차 기록("다음 회차가 같은 표를 재현하려면 필요")에만 있다. 기록을 읽지 않는 세션(또는 P5 분리 뒤)은 문서대로 계산해 값이 갈린다. 재현이 0 차이였던 건 기록을 읽었기 때문 | ①~⑫를 report-structure.md 해당 절에 한 줄씩 넣거나(정의 자리), E1을 채택하면 `scripts/`의 계산 스크립트가 정의를 담고 문서는 "규칙은 compute.py"로 가리킨다(둘 중 하나는 반드시) | 스킬 저장소 push — 즉시 반영 |
| D-12 | 하 | SKILL.md (+ audit 09-11 기록) | 35 · 150–153 | 35 `읽기는 두 저장소 모두 공개라 토큰 없이 된다. 토큰이 필요한 건 쓰기뿐이다.` / 150~153 4단계 `GET https://api.github.com/repos/…/contents/index.html` `Header: Authorization: token {토큰}` | **실측** — 이번 회차 무인증 GET → HTTP **403** `API rate limit exceeded`(09-11·09-21 기록도 403). 이번 회차 배포본은 `git clone`으로 받음(토큰 불필요). SKILL.md에 `clone`이라는 단어 0건(grep) | 4단계에 토큰 없는 경로가 없어 진단·검증 회차(토큰 안 줌)가 4단계를 그대로는 못 따른다. 09-11 기록 `배포본은 git clone 공개 저장소로 받음(SKILL.md 4단계 대안)`은 존재하지 않는 대안을 가리키는 **기록 문구 오류**. 35행은 API에는 맞지 않음 | 4단계에 "토큰이 없거나 API가 403이면 `git clone https://github.com/LeeKwanBeom/saero-pilates-report`로 받는다(진단·검증 회차)" 한 줄, 35행에 "(API GET은 무인증 rate limit — clone은 됨)" 병기. I-10의 "(선택)" 표기는 하지 않음 | 스킬 저장소 push — 즉시 반영 |
| D-13 | 중 | SKILL.md ↔ scripts/archive.py | SKILL 105–106 ↔ archive 128–131 · SKILL 85 | SKILL 105~106 `4개 중 하나라도 없으면 먼저 사용자에게 확인한다. 특정 보고서만 없으면 그 섹션은 직전 데이터로 두고 나머지만 갱신한 뒤, 그 사실을 안내한다.` / archive 130~131 `if bounds[k] != ref: fail(f"{k} 조각 경계 {bounds[k]} ≠ 키워드 {ref} — 같은 기간으로 받아야 함")` / SKILL 85 `2. 합본을 만든다. **FAIL이면 멈추고** 메시지대로 사용자에게 확인한다` | **실측** — 사본에서 `data/2026-09/검색어.csv` 제거 → combine `[FAIL] 검색어 조각 경계 [(8/1~8/31)] ≠ 키워드 [(8/1~8/31),(9/1~9/25)]` exit 1, 합본 미생성 | 09-26 1단계(보관→합본)가 생긴 뒤 "특정 보고서만 없으면 나머지만 갱신" 경로는 실행 불가능한데 문서엔 남아 있다. 한 보고서가 빠진 회차에 반드시 문서와 코드가 어긋난다 | 105~106행을 "4개 중 하나라도 없으면 combine이 FAIL로 멈춘다 — 빠진 보고서를 받아 store한 뒤 다시"로 교체(부분 갱신 경로 삭제). 부분 갱신을 남기려면 archive.py에 `--allow-missing <종류>` 같은 명시 옵션이 필요(설계 변경, 사용자 결정) | 스킬 저장소 push — 즉시 반영 |

## 개선안 (정확성, 최대 5 — I-7·I-8 이월 포함, 순위 갱신)
| # | 내용 | 이유·근거 | 우선순위 |
|---|---|---|---|
| 1 | **validate.py 검사 2개 추가 — 05번 mediaChart top5 = 키워드 CSV `매체이름` 노출 상위 5(라벨·값·순서·색) / 06번 카드 큰 숫자 = 04번 같은 그룹 평균순위 셀** (mutation_test.py에 변조 2개·0건 가드도 같은 회차에) | 09-25(05번 5위 에펨코리아→통합검색 PC)·09-26(06번 1.70 vs 1.67) 실사고 2건 — 둘 다 validate 밖에서 사람이 놓친 유형. 이번 회차 compare.py가 두 자리를 기계로 대조해 일치 확인 [실측], 규칙이 확정돼 있어 검사화 비용 낮음 | 1 |
| 2 | (이월 I-8) validate.py가 config `competitors`를 읽어 검색어 CSV에서 **이름을 포함하는 검색어가 07번 경쟁사표 밖(정식표·클릭1건·클릭0 목록)에 있으면 FAIL** + 경쟁사표 클릭 합 = 검산 | D-1 유형(배포본에만 있는 경쟁사)을 기계로 잡는 유일한 지점. 이번 CSV 실측: config 10개 이름을 포함하는 검색어 중 표 밖 **0건**. 주의: 표 25행 중 config 이름을 부분 문자열로 포함하지 않는 변형이 있음(`노원정원필라테스`·`노원구정원필라테스`·`필라테스노원와우점` — "필라테스정원"·"와우필라테스"와 어순이 다름) → 역방향(표 안 이름이 config에 있는지)은 검사하지 말고 순방향만 | 2 |
| 3 | **11·12번 수동 검사의 스크립트화** — 11번 `<li>` 수 ≤ 8 + `(참고)` ≤ 2, 판정 줄 `유지+뒤집힘+근거 소멸 = 직전 항목 수`, 금칙어(`필요`·`시점`·`할 것`·`검토`·`주째`) 0건, 잔존 문구(`확인 요청`·`판단 요청`·`기다림`·`확인 중`·`대기`) 0건 — 범위는 11·12 **본문**(`<script>` 앞에서 끊는다: 스크립트 주석에 `필요` 2건이 있음) | report-structure 327~334행 수동 검사 6항목 중 4개가 문자열 검사라 기계화 가능. compare.py로 이번 회차 전부 0건·7+2·6+1+0=7 확인 [실측]. 07번의 `검토` 3건은 조치 문장이 아니라 범위에 넣지 않음 | 3 |
| 4 | (이월 I-7) 검색어 CSV 클릭 합 ≠ KPI를 `참고` 출력이 아니라 FAIL(또는 15번째 검사)로 | validate.py 356~358행, exit 0. 검색어 보고서 기간이 다르면 07번 표가 조용히 틀린다. 합본 방식에선 combine이 경계를 잡지만 검색어 노출은 키워드와 원래 다르므로(콘텐츠 지면 미포함, 7,774 vs 9,525) 클릭만 대조 | 4 |
| 5 | (신규) `tests/mutation_test.py`에 archive.py 변조 7종 추가(옛 다운로드·두 달 걸침·시간대별 +1·개업 달 제거·헤더 빈틈·경계 불일치·종류 누락) + playwright 360/390/430px `scrollWidth == 뷰포트` 검사를 `tests/overflow_check.py`로(컨테이너에 playwright 있음, 실측 `import playwright` OK) | mutation_test.py는 validate.py만 돌린다(102행). archive.py 검사 7종은 이번 회차 손으로 재현했고 다음 회차도 사람이 해야 한다. 넘침 검사는 09-23~09-26 매 회차 즉석 코드로 돌림(기록 `playwright 360·390·430px scrollWidth = 뷰포트`) | 5 |

I-10은 종결·대체(D-12). I-9는 개정안 2로 이관.

## 효율 개선안 (최대 5 — 산출값 동일 실측 없이는 채택하지 말 것)
| # | 후보 | (a) 현재 코드·문서 인용 | (b) 실측 | (c) 예상 절감 | (d) 정확성 리스크·검증 방법 |
|---|---|---|---|---|---|
| E1 | **계산 코드 고정** — 회차 작업 디렉토리의 `recalc.py`(143행, 합본 4종 + config → 12개 섹션 값 JSON)를 `scripts/compute.py`로 저장소에 두고, SKILL.md 5단계를 "compute.py 출력값만 쓴다"로. validate.py와 겹치는 읽기·필터(validate 79~81 `read_csv(skiprows=1)`, 284~290 제외그룹·KPI 합, 168~171 일수)는 공통 헬퍼로 | SKILL.md 160 `숫자는 반드시 pandas로 계산한 값만 쓴다. 추측 금지.` / 09-19·09-20·09-21·09-23 기록 `계산 스크립트는 회차 작업 디렉토리에만 둠` | 이번 회차 recalc.py 산출값 = 배포본 **99항목 차이 0** [실측]. 스크립트 작성·디버그에 도구 호출 8회·약 4분 — 매 회차 반복되던 비용 | 갱신 회차마다 즉석 계산 코드 작성 제거(추정 도구 호출 −8~10회·−4분/회차 [추론]). D-11의 정의 12개가 코드에 고정돼 문서 결함도 같이 닫힘 | 스크립트가 틀리면 매 회차 같은 방향으로 틀린다 → validate.py는 **독립 계산으로 유지**(헬퍼 공유는 읽기·필터까지, 값 계산은 분리). 채택 검증: 별도 세션이 compute.py로 ad48222를 재현해 차이 0 |
| E2 | **기계 자리 자동 교체** — (2026-10-06 현행화: 저장소화된 `scripts/apply.py` 기준) compute.py JSON 으로 기계 자리 **전부**를 치환한다 — 행 고정 자리(KPI 4+sub 3, 01 표 5행·순위 5칸, 03 표 전체+합계, 04 표(앞 2칸 = 직전 행), 06 매칭표·카드 일차·큰 숫자, 10 표 4행, 차트 data 배열·labels, min-width 2개, 02 도넛 총액, masthead·og) **+ 행 수가 변하는 구간(07 정식표·클릭1건·클릭0 목록·경쟁사표(소재구·매칭 = 직전 행, 신규 변형 = config `competitor_defaults`), 08 TOP10·컴팩트 목록·개수 줄 — 동률은 직전 순서)**. 문장은 서술 표지(`<!-- n:<자리>:<매회차|고정> -->`) 안을 그 회차 n<날짜>.py(저장소 밖)가 바꾼다(08·09 각주 숫자도 표지 안). (옛 정의: "행 고정 자리만 — 07·08 가변 구간·문장은 사람", 이름 `scripts/patch.py` 안) | SKILL.md 13~15 `**리포트 HTML을 새로 만들지 말 것.** … "숫자와 문구만" 교체한다` | 배포본 기계 자리: `td.num` 셀 509개(03번 224·07번 170·04번 35·01·08번 각 30)·data 배열 12·labels 8·min-width 5 vs 문장 블록 40개(note 본문 9,181자). 행 고정 자리만 세면 약 330셀 + 배열·라벨·폭 | 갱신 회차의 str_replace/sed 반복을 스크립트 1회로(추정 −10회 이상 [추론]). 원칙과의 경계: 기계 자리만 치환하면 레이아웃·CSS·순서·문장 불변이라 원칙 준수 | 치환 위치를 잘못 잡으면 표가 어긋남 → 앵커가 정확히 하나가 아니면 `[FAIL] apply:` exit 1(작업본 그대로) · 치환 후 precheck(validate·compare·narrative) 필수 · 멱등·앵커는 tests/test_apply.py(2026-10-06 현행화) |
| E3 | **도구 호출 묶기** — 1단계 `store → combine → git push`를 bash 1회로, 6단계 `validate → playwright 넘침 → 재수령 md5`를 스크립트 1회로, 4·7단계 GET/PUT을 파이썬 1개로 | SKILL.md 77~91(1단계 3항목)·167~189(6·7단계) | 갱신 회차 기록엔 호출 수가 없어 실측 불가 — 근거는 09-25·09-26 "도구 한도로 멈춤" 2회뿐. 이번 회차 P1의 배포본 마크업 확인 9회는 compare.py 같은 파서가 있으면 0회 | [추론] 갱신 회차 bash 호출 절반 이하. 개정안 8(효율 기준선 표)을 먼저 채택해 다음 갱신 회차부터 호출 수·벽시계를 기록해야 실측이 생긴다 | 묶은 명령 중간 실패가 조용히 넘어가지 않게 `set -e`·단계별 exit 확인 |
| E4 | **부트스트랩 읽기 분량 축소(P5와 짝)** — last-audit.md에서 갱신 회차 기록·이전 기록을 분리하면 매 실행 읽는 분량이 1,948행 → 약 900행 | 부트스트랩 33~37행 `saero-skill/SKILL.md를 읽고 … audit/last-audit.md가 있으면 함께 읽는다` | 매 실행 읽기: SKILL.md 361행 + last-audit.md **1,018행** + references 368+201 = 1,948행. last-audit 구성: 진단 기준선 164행·운영 표 106행·갱신 회차 기록 421행·이전 기록 328행. 갱신 회차에 필요한 건 운영 표 + 직전 회차 기록 + "다음 회차 대조" ≈ 150행 | [추론] 약 55% 감소(361 + 150 + 368 = 879행, css-and-layout은 레이아웃 작업 때만). 분리 뒤 실측 필요 | 분리하면 운영 표 정본 위치가 바뀜 → 저장소 SKILL.md에 "읽을 audit 파일" 명시(부트스트랩은 저장소 SKILL.md를 따르므로 재업로드 불필요) |

## 설정 사본 전수 (P4) [실측 grep]
| 값 | 정의 자리(config 참조로 바꿔야 함) | 설명·예시 자리(유지) | 배포본 문구(config 변경 시 같이 바꿀 곳) |
|---|---|---|---|
| 개업일 8/26 | 없음(archive.py 47행은 코드 주석 `# "2026.08.26."` — 무해) | SKILL.md 57·117·137·256·308(예시) | index.html 1648 `개업일(2026.08.26)` |
| 제외 그룹 | 없음 | SKILL.md 251~252(설명, 키 병기) · report-structure.md 137 `키워드 10개` | index.html 825·1649 `"노원필라테스" 그룹`·`키워드 10개` |
| 경쟁사 목록 | 없음 | SKILL.md 208(표기 변형 예시) | 07번 표 25행(승인 때 갱신하는 자리) |
| 타겟 지역 | 없음 | SKILL.md 280(키 병기) | index.html 1404 section-desc·1651 집계 기준 |
| CTR 4% | **report-structure.md 198 · css-and-layout.md 22–23·44 → D-10** | SKILL.md 350(사고 기록) · report-structure.md 129(설명) · css 180(사고 기록) · checklist 149 | index.html 125(CSS 주석)·1133(범례)·1652(집계 기준) |
| 80px/650px | **report-structure.md 63 → D-10**, css 175 예시 낡음 | css 173(키 병기) · report-structure.md 240(09번 고정 650px는 config 대상 아님) · checklist 151 | index.html 266·868(값 자체, validate가 검사) |
SKILL.md 303~318 "매번 함께 바꿔야 할 텍스트"·320~347 "배포 전 검산"은 validate.py 14개(출력 세어 14)와 일치 — 344~347행 자동/수동 구분도 맞음. 다만 갱신 회차 실사고 2건(05 top5·06 카드)이 이 목록 어디에도 없다 → 개선안 1.

## P6. 저장소 공개 여부 — 결정은 사용자 (각 한 줄)
- 현재(공개): 부트스트랩·검증 세션 clone에 토큰 불필요. 대신 `data/`의 검색어 전수(클릭 0 563개 포함)·지역 전수·일별 비용·계정번호 2580077이 누구에게나 보인다. 배포본(index.html)도 공개라 KPI·상위 검색어·지역 TOP10은 이미 공개 상태.
- 비공개 전환: clone에 토큰 필요 → 부트스트랩 1단계 명령을 `https://x-access-token:<토큰>@github.com/…`로 바꾸고 **재업로드**, 진단·검증·갱신 매 회차 토큰 입력(대화에 남는 빈도 증가), 토큰 종류가 사실상 매 회차 2종.
- 절충 A: `data/`만 별도 비공개 저장소로 분리 — 스킬 본체는 공개 유지, 갱신 회차만 데이터 토큰. 진단 회차가 합본을 쓰려면 그때도 필요. archive.py의 `DATA` 경로·SKILL.md 1단계 수정.
- 절충 B: 공개 유지 + store 때 헤더의 계정번호만 마스킹 — combine의 "계정 동일" 검사(archive.py 117~120)와 충돌해 코드 변경 필요, 검색어·비용은 그대로 공개.
- 절충 C: 공개 유지, 저장소 이름·README에서 식별 정보 최소화 — 리포트가 이미 공개라 실익 작음.

## P7. [의도된 동작] 초안 — 점검표 신설 절(다음 회차가 결함으로 올리지 않게)
1. 04번 예산 비중은 **최대잔여법**(소수 1자리, 합 100.0) 표시값 — 단순 반올림과 다를 수 있음(09-24 3.955→3.9, 09-25 92.545→92.6). 02번 section-desc도 같은 값.
2. 06번 rankChart = 노원역필라테스 **그룹 전체(자동매칭 포함)** 노출 가중순위, 31일 전부. 직접 등록만이면 0/31 일치.
3. 10번 A = `검색/콘텐츠 매체 == 검색` 이고 `매체이름`이 `네이버`로 시작하는 매체 전부(통합검색·플레이스·검색탭·광고더보기), B = 검색이면서 네이버 외(`기타 매체`의 검색분 포함), C·D는 콘텐츠. C·D는 9/6 이후 고정(22·1,724).
4. 동률 처리: 07 정식표 클릭 동률 → 노출 내림차순 / 뱃지는 노출 많은 유형, 일치·확장 동률 → 직전 뱃지 유지 / 경쟁사표 노출 동률 → 클릭 내림차순, 그 안은 직전 순서(신규 행은 끝) / 클릭1건·클릭0·08 컴팩트 목록 동률 → 직전 순서 유지.
5. 08·09번 각주 "6회 차이"는 정상(제외 그룹 노출 6·클릭 0, 8/26 5·8/31 1). 클릭 차이 0이라 "클릭 N회 차이" 문구는 없음. 검색어 CSV 노출 합(7,774)이 키워드 전체(9,525)보다 작은 것도 정상(콘텐츠 지면 미포함) — 클릭은 298로 같다.
6. 07번 "클릭 0 검색어 전체 N개·N회" 각주는 **경쟁사 포함**, "노출 5회 이상" 컴팩트 목록은 경쟁사 제외. "확장·클릭 0 노출"은 **행 단위**(검색어 단위 아님).
7. 06번 카드: OFF 확정 그룹(노원키즈)은 카드 제거, 04번 행은 `(9/2 등록 · 9/17 OFF)`로 유지, `excluded_groups`에는 넣지 않음(실집행 있음). 카드 "N일차"는 등록일 포함 일수, 매칭표 순위는 소수 1자리(04번은 2자리).
8. 08번 컴팩트 목록 지역명 축약(`서울특별시 ` 생략, `전남광주통합특별시 북구`→`광주 북구`, `인천광역시`→`인천`, `세종특별자치시`→`세종시`).
9. "운동" 계열(창동역운동 등 6개)·산전·산후·임산부 계열은 제외 검색어 대상 아님(09-21·09-24 사용자 결정). "노원역운동"은 등록돼 있지 않음(09-25) — 둘 다 다시 묻지 않음.
10. 파트너 매체(다음·네이트·Bing)는 "해제"인데 노출이 잡힘 — 네이버 답변을 사용자가 전하기 전까지 12·11번에 올리지 않고 채팅으로도 묻지 않음(09-24). 파워링크 예산 현행 유지(09-17)·지역 설정 전국(09-20)·플레이스 일예산 상향 유지(09-21)는 각각 걸어둔 재상정 조건 전까지 다시 올리지 않음.
11. 노원M필라테스는 경쟁사표 미복귀(09-14 사용자 결정), 클릭 1건 목록에 둠. 필라테스안 계열은 제외 확정(09-26). 경쟁사 채택·제외·종결은 `## 경쟁사 판정 이력` 표가 정본.
12. 09번 심야 = 22·23·0~8시(09시 배타), 비중은 정수 반올림. 09번 min-width 650px은 고정(config 대상 아님). 심야 서술은 긍정 톤 유지.
13. 시간대별 CSV 클릭은 KPI가 아니라 **제외 전 전체**와 비교(D-4). 01번 순위 그리드 민트 = 닷새 중 최솟값.
14. 라이브 Pages는 web_fetch 결과로 판정하지 않는다(캐시). 사용자 시크릿 창 확인이 유일. 설치본 references/scripts 사본이 낡은 것은 정상(저장소 것을 쓴다).
15. 11번은 12번 확정 뒤 맨 마지막에 쓴다. 상계동필라테스는 하루 30회 이상 이틀 전까지 카드 유지.

## P8. 배민(v6)·쿠팡(v3) 점검표 ↔ 이 점검표(v4.3) 양방향 대조
| 배민·쿠팡에 있고 여기 없는 것 | 이식 → 개정안 |
|---|---|
| 1차 커밋(last-audit만) → 채택 후 2차 커밋(checklist) — 머리말과 [마무리]가 같은 말 | 1 |
| 행수·md5 기준, 바이트 수 금지, 행 번호 인용 시 파일 행수 기준 병기, 수정 기록은 절·함수명으로 | 6 |
| 문구 교체는 지목된 곳이 아니라 파일 전체 grep(자매 파일 포함) | 6 |
| "되돌리면 안 되는 것" 표 | 5 |
| [의도된 동작] 목록 | 4 |
| 채팅 보고 끝 토큰 폐기 안내(여기는 37행 시작 절에만) | 7 |
| 클라우드 push 403 시 PC(device_bash) push 절차 | 7 |
| 설치본 md5 대조를 매 회차(여기는 "재업로드했다고 말한 회차에만") | 3 |
| 직전 세션 판단을 결론으로 받지 마라 | 6 |
| 속도(효율) 기준선 표 상시화 | 8 |
| 여기에만 있는 것(배민·쿠팡 역이식 후보 — 그쪽 개정안으로만 기록) | |
| 검증 회차 A(동작)/B(의도) 이중 검증 문구 | 그쪽 회차에서 제안 |
| 두 저장소 구분 [운영 조건] (스킬 저장소 ↔ 배포 저장소) | 이 스킬 고유 |
| CSV 선확인 [시작 전 확인 ②] + I-9 | 이 스킬 고유(합본 방식으로 갱신) |
| `tests/mutation_test.py`로 검사 생존 자동 확인·0건 가드·config 실험 | 역이식 후보 |
| web_fetch 캐시 확정·라이브 시크릿 창 규칙, 설정값 사본 대조 | 이 스킬 고유 |

## 점검표 개정안 (개수 제한 없음 — 채택된 것만 2차 커밋에서 반영)
1. **커밋 규칙을 배민·쿠팡과 통일**: 머리말 6~8행 `같은 커밋으로` · 304~323행 [마무리] "같은 커밋으로"를 "1차 커밋 = last-audit.md만(진단 직후, 보고 전) / 2차 커밋 = checklist.md(채택 뒤; 수정 회차면 SKILL.md·scripts·config·수정 기록도)"로. 이번 회차가 이미 이 규칙으로 함.
2. **[시작 전 확인 ②]에 합본 방식 반영(I-9)**: "실 CSV = 저장소 `data/` 보관본 합본(`archive.py combine`)을 기본으로 하고, 업로드 요청은 data/가 없거나 combine FAIL일 때만. 합본 기간이 직전 갱신 회차와 같으면 CSV 실측 항목은 '직전 결과 재현'으로 갈음하고 파괴 실험·대조에 시간을 쓴다." 50~57행 요청 문구는 그 조건 아래로.
3. **3) 설치본 확인을 매 회차로**: 부트스트랩 44행 내용 검토(41행 경로·실패 절차) + references/scripts 사본 md5·행수 대조(낡음은 정상, 부트스트랩 37행 근거). 재업로드 필요 여부는 "그대로/필요"로 판정만.
4. **[의도된 동작] 절 신설** — 위 P7 초안 15개.
5. **"되돌리면 안 되는 것" 표 신설** — 후보: 0건 가드 8종·config 읽기(D-8)·06 min-width·라벨 검사(D-9)·시간대별 비교 대상 = 제외 전 전체(D-4)·07 검색어 단위 합산·11번 마지막 작성·archive.py combine 검사 5종·store 거부 2종·2-1단계 선확인·`body{overflow-wrap:anywhere}`+`<wbr>`(버그 기록 10)·`.ctr-high`는 새로 판단(버그 기록 9)·`.grid-2-07 > *{min-width:0}`(버그 7).
6. **[판정 기준]에 추가**: 바이트 수 금지·행수+md5 기준·행 번호 인용 시 파일 행수 병기 / 수정 기록은 절·함수명 / 문구 교체는 파일 전체 grep(SKILL.md·references·checklist·last-audit 자매 파일 포함) / 직전 세션 판단은 입력물이지 결론이 아님.
7. **[마무리]에 추가**: 채팅 보고 마지막 줄 토큰 폐기 안내 / 클라우드 push 403이면 PC(device_bash) 절차(배민 375~390행 형식) — 이번 회차 결과는 아래 마무리에 기록.
8. **효율 기준선 표 상시화**(배민 "속도 기준선"에 대응): 갱신 회차 기록에 벽시계·도구 호출 수·즉석 코드 줄 수 3개를 매번 적는다. 이번 회차 P1 값(약 5분·17회·290행)이 첫 기준선.
9. **매 회차 통과만 나는 항목 삭제**: 107~108행 web_fetch 대조군 재확인(3회차 연속 미실시·근거 금지 규칙과 모순) → 삭제하고 "라이브 = 사용자 시크릿 창" 한 줄만.
10. **1) 대상 목록 갱신**: `scripts/archive.py`·`data/YYYY-MM/`(4종×달)·`tests/` 추가, "실제 ls와 다르면 알려라"는 유지.
11. **162~166행 "실 CSV로만 확인 가능한 것"(인코딩·콤마·컬럼 구성·기간 불일치·빈 데이터)은 종결** — 합본 방식 도입으로 combine이 기간·합계를 검사하고 4회차 연속 UTF-8 BOM·콤마 없음. "data/ 파일 형식이 바뀐 회차에만"으로.
12. **파괴 실험 절(176~185행)에 archive.py 추가**: 개선안 5 채택 전엔 손 실험 7종 목록, 채택 뒤엔 "mutation_test.py PASS"로 대체.
13. (재상정) 미채택 개정안 8 — [검증 회차] 절을 `audit/verify.md`로 분리하거나 "진단 회차엔 적용하지 마라"로 문구 완화.
14. **last-audit.md 분리(P5, 다음 회차 구조 변경)**: `audit/last-audit.md`(진단 기준선 + 이전 기록) / `audit/updates.md`(갱신 회차 기록, 최근 것 위) / `audit/registry.md`(운영 표 3개: 등록 제외 검색어 대조 목록·경쟁사 판정 이력·개선안 이월 표). 저장소 SKILL.md에 "갱신 회차는 registry.md + updates.md 최근 절, 진단 회차는 셋 다"를 명시 → 부트스트랩 35행("last-audit.md가 있으면 함께 읽는다")은 저장소 SKILL.md가 우선이라 재업로드 없이 됨. 이번 회차엔 구조를 바꾸지 않았고 새 기준선만 맨 위에 넣음(지시).
15. checklist 336행 "점검 대상" 형식에 `실 CSV = 저장소 data/ 보관본 합본(기간 …)` 표기 예시 추가.

## 점검표 갱신 이력 (checklist.md)
- (이번 회차 변경 없음 — 1차 커밋은 last-audit.md만. 채택 후 2차 커밋에서 v4.4로.)

## 다음 점검에서 대조할 것
- (2026-09-27 제외 검색어 병합 `6a35abf`) **첫 실사용**(PC `pull` → 시험 1건 → 첫 `push`) 기록이 "첫 실사용 기록"에 있는지 · 그룹 ID↔그룹명 3개가 registry에 채워졌는지 · 대조 목록 표에 요약 행이 생겼는지 · `--registry` 없음 exit 1·dry-run 무변경·거부·verified:false(checklist [검증 회차] C) 재현 · 검증 2 참고 ①(그룹 ID 표기) 채택 여부.
- (2026-09-27 병합) **첫 실사용 갱신 회차**(병합본 main으로 도는 첫 회차)가 새 절차대로 돌았는지 기록으로 대조: 1단계 `scripts/ingest.sh`(store→combine→data push) · 4단계 `deploy.py fetch --out /home/claude/work/prev.html` + `cp` 작업본 · 5단계 `compute.py --competitors-html prev.html`(즉석 계산 0) · 6단계 `precheck.sh` **3인자**(작업본·합본·prev.html, 답 반영 재배포에 `--pending` 없음) · 8단계 양식(**효율 3항목** 벽시계·도구 호출·즉석 코드 + **`--pending` 사용: 아니오/예** 칸). 하나라도 빠지면 다음 진단 회차가 결함으로 올린다.
- (2026-09-27 검증 2 참고 ②) `tests/mutation_test.py`에 검사 21의 **07 각주(`class="note"`) 잔존 문구 변조 + 0건 가드 추가** — 지금은 11·12번 본문 변조·가드만 있다. 다음 회차 후보(코드 변경이라 진단 → 사용자 선택 → 수정 순서).
- (2026-09-27 병합) config 별칭(`competitor_aliases`) 후보 — 바로 아래 검증 (c) 줄 그대로 이월. 채택 여부는 다음 진단 회차가 올린다.
- (2026-09-27 검증 (c)) 07 경쟁사표에 **config에 없는 브랜드**의 행이 있거나 그 브랜드의 다른 표기가 검색어 CSV에 새로 나타나도 지금은 알림이 없다(compute.py `신규변형후보`·validate 검사 16은 config 이름 기준). 후보: config에 `competitor_aliases`(표 안 브랜드 → 표기 목록) 또는 경쟁사표 name-cell 브랜드를 config에 강제하는 검사. 다음 진단 회차가 채택 여부를 올린다.
- 이번 회차 결함 D-10~D-13·개선안 1~5·효율 E1~E4·개정안 1~15 중 사용자가 고른 것의 조치 여부(수정 회차) → 검증은 별도 세션(checklist [검증 회차] A/B).
- 라이브 시크릿 창 확인 결과(이번 회차 미수령이면 "라이브 미확인" 유지).
- E1을 채택하면: `scripts/compute.py`로 다음 갱신 회차 배포본을 재현해 차이 0인지 / validate.py 독립 계산 유지 여부 / D-11 정의 12개가 코드나 문서 어느 한쪽에 들어갔는지.
- 개정안 8을 채택하면: 다음 갱신 회차 기록에 벽시계·도구 호출·즉석 코드 줄 수가 적혔는지(E3 실측 기준선).
- archive.py `store --chunk` 실경로(10월 31일 → 11/1) 첫 실사용 때 이번 실험(1~24+25 조각 = 단일 합본)과 같은지.
- 검색어 CSV 노출 합 vs 키워드 검색 지면 노출(7,774 vs 7,779 — 5회 차) 원인은 미확인(콘텐츠 미포함 외 수회 차이는 09-24 기록 "1~2회 차"와 같은 유형). 결함 아님, 기록만.
- P6 결정(공개/비공개/절충) 결과와 그에 따른 부트스트랩 재업로드 여부.

## [수정 회차에 적용할 것 — 점검표에서 옮겨 적음]
- 같은 개념을 두 파일에서 고칠 때는 기준을 대조해라 — D-11을 문서로 닫든 E1로 닫든 validate.py·compute.py·report-structure.md·SKILL.md 272~285행이 한 규칙이다. 공통 헬퍼로 묶되 값 계산의 독립성(validate ↔ compute)은 남겨라.
- 검사 조건을 완화하는 수정을 했으면 `tests/mutation_test.py`를 전부 다시 돌려라(개선안 1·2·4로 검사가 늘면 변조·0건 가드도 같은 회차에).
- 새 설정값·새 필드를 추가했으면 같은 회차에 문서화하거나 빼라(I-8로 `competitors` 소비자가 생기면 config `_comment`·SKILL.md 39~48행도).
- 설계를 바꿨으면 그 자리의 주석도 같이 고쳐라(validate.py docstring 11~29행, archive.py docstring 12~30행).
- `--force`·`--chunk` 류 옵션은 정말 그 범위만 바꾸는지 실측해라(이번 회차 실측: `--chunk`는 `<종류>_2.csv`만 추가, `--force`는 덮어쓰기만).
- 수정과 검증은 다른 세션에서 한다. 검증 문구는 checklist.md `[검증 회차]` 절.

## 마무리 기록 (이번 회차)
- 1차 커밋: `audit/last-audit.md`만(이 기준선을 맨 위에, 09-07 기준선 이하는 "이전 기록" 표제 아래 원문 보존, 운영 표 세 개·갱신 회차 기록 위치·내용 그대로). checklist.md **변경 없음**(2차 커밋 대기). SKILL.md·scripts·config·data **변경 없음**.
- 진단 전문 파일: `saero-ad-report_last-audit_2026-09-26.md`(이 기준선 절 전문).
- push 결과·재clone md5·행수는 채팅 보고에.

---

# 이전 기록 (2026-09-07 저녁 기준선 — 원문 보존. 아래 `## 등록 제외 검색어 대조 목록`·`## 경쟁사 판정 이력`·`## 개선안` 표는 현행 운영 표이며 위치·내용 그대로다)

## 개선안 (최대 5 — I-6 조치완료, 나머지 이월. 순위 갱신: I-9 최우선)
| # | 내용 | 이유 | 우선순위 |
|---|---|---|---|
| I-9 | (이월·**최우선**) 진단 회차에 실 CSV가 직전 회차와 동일 기간이면 CSV 실측 항목은 "직전 결과 재현"으로 갈음 | 이번 회차 CSV 실측이 전부 재현이었다. 점검표 개정안 6과 짝 | 1 |
| I-7 | (이월) 검색어 CSV 클릭 합계 ≠ KPI를 명시 FAIL 또는 별도 검사로 | validate.py `참고` 출력만, exit 0 | 2 |
| I-8 | (이월) validate.py가 config `competitors`를 07번 경쟁사표와 대조. 코드 소비자 없는 config 필드: `competitors`·`target_districts`·`excluded_group_keywords`·`open_date` (date_based_sections는 이번에 사용 시작) | D-1 유형을 기계로 잡는 유일한 지점. D-7로 SKILL.md에서 목록을 뺐으니 config↔화면 대조가 더 중요해짐 | 3 |
| I-10 | (이월) SKILL.md 4단계 GET의 `Authorization` 헤더 "(선택)" 표기 | 읽기는 토큰 불필요(35행) | 4 |
| ~~I-6~~ | **조치완료(D-9와 함께)** — 아래 원문 보존 | | — |
| I-6 | (신규) validate.py: `date_based_sections` 순회로 01·06 min-width 검사 + 01·06 `labels:[…]` 개수 = 일수 검사. 라벨 배열은 index.html 1313·1511행(스크립트 영역, 섹션 슬라이스 밖)이라 전체 html에서 정규식으로 잡는다 | D-9의 코드 쪽 해법. SKILL.md 266행 3번·267행 4번(x축 라벨)이 수동 목록에서 빠질 수 있음 | 1 |
| I-7 | (이월) 검색어 CSV 클릭 합계 ≠ KPI를 `참고` 출력에서 명시 FAIL 또는 별도 검사로 | validate.py 332–334행. 검색어 기간이 짧아도 exit 0 "배포 진행 가능"(직전 기준선 39·173행) | 2 |
| I-8 | (신규) validate.py가 config `competitors`를 읽어 07번 경쟁사표 name-cell과 대조(표기 변형은 접두 일치 허용). 현재 config의 `competitors`·`target_districts`·`excluded_group_keywords`·`open_date`·`date_based_sections`는 코드 소비자 0건(grep) | D-1 유형(배포본에만 있는 경쟁사)을 기계로 잡을 수 있는 유일한 지점. config 필드 절반이 "문서 역할만" 하는 상태 | 3 |
| I-9 | (신규) 진단 회차에 실 CSV가 직전 회차와 동일 기간이면 CSV 실측 항목은 "직전 결과 재현"으로 갈음하고 시간을 파괴 실험·문서 대조에 쓴다 | 이번 회차 CSV 실측이 전부 직전과 동일 결과. 점검표 개정안 6과 짝 | 4 |
| I-10 | (이월·축소) SKILL.md 4단계 115–116행 GET에 `Authorization` 헤더 필수처럼 적혀 있으나 35행대로 읽기는 토큰 불필요 — "(선택)" 표기 | 배포 토큰 없이 진단만 하는 회차에서 4단계를 그대로 따르면 토큰을 요청하게 됨. 결함은 아님(있어도 동작) | 5 |

## 등록 제외 검색어 대조 목록 (현행 — 매 갱신 회차에 반드시 대조)

**사용자 지시(2026-09-20)**: "내일부터 해당 검색어가 잡히면 다시 말해줘." → 매 갱신 회차에 아래 목록을 검색어 CSV와 대조해,
**등록일 다음 날 이후** `검색 유형 == "확장"` 행에 이름이 잡히면 **이름·날짜·노출수를 채팅으로 보고**한다(리포트 07번 각주·12번 1번에도 기록).
- 대조는 **"확장" 행만**. 제외 검색어는 파워링크 그룹에만 등록돼 있어 "일치"(플레이스) 노출은 대상 밖이다(09-20 노원역운동 사례).
- 등록 당일 데이터는 시각 전후가 섞이므로 판정하지 않는다(보고할 때는 "등록 당일"이라고 표시만).
- 잡히지 않았으면 "등록 이후 재노출 0"을 한 줄로 보고. 조용히 넘어가지 말 것.
- **"확장" 유형 = 파워링크 자동매칭(키워드 `-`) 노출이다(09-24 실측).** 29일치 날마다 검색어 CSV `검색 유형=="확장"` 노출이 키워드 CSV 파워링크 `-` 노출과 같거나 1~2회 차(누적 1,801 대 1,806), 클릭은 39 대 39로 일치. 따라서 "확장"에서 나온 무관 검색어는 **파워링크 그룹에만** 등록하면 되고 플레이스 칸은 필요 없다. 플레이스 제외 검색어 칸은 가득 참(09-24 사용자) — 플레이스 쪽 등록을 제안하지 말 것.
- 사용자가 새 목록을 등록하면 **같은 회차에 이 표에 목록 원본을 추가**한다. 목록을 저장소에 안 남겨 67·79개 대조가 불가능했던 일(09-19~09-20)이 있었다.
- **(2026-09-27 기능 추가 회차 — main 병합 `6a35abf`, 적용 중)** 등록 여부는 **`audit/exclusions.csv`(registry)로 스킬이 판정하고 사용자에게 묻지 않는다** —
  재노출은 "등록돼 있는데도 노출 / 등록 누락 → 후보 / 미확인" 셋 중 하나로 보고(SKILL.md 5-0단계, `scripts/exclusions.py propose`). "탭 목록 확인 요청"은 하지 않는다.
  스킬이 등록한 회차는 이 표에 **요약 행만**(등록 n · verified n · 실패 n · description) 적고 이름 원본은 registry에 둔다. 사용자가 손으로 등록한 목록은 종전대로 원본을 적는다.

| 등록일 | 위치 | 목록(원본) | 비고 |
|---|---|---|---|
| **2026-10-07 01:25 자동 등록(스킬 `push` 참조 선택 모드, 사용자 승인 "등록승인3개" — Code 탭 `/saero-run`)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 3 · verified 3(9건) · 실패 0 · description `saero 10-07`**(이름 원본 = `audit/exclusions.csv`, 승인 파일 `work/approved_2026-10-07_012548.txt`) — propose 창 10/6 신규 후보 3개 그대로 | 3그룹 각 294 → 297. 재노출 판정(창 10/6) 0건 |
| **2026-10-06 09:28 자동 등록(스킬 `push` 참조 선택 모드, 사용자 승인 "등록 승인 10개" — Code 탭 `/saero-run`)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 10 · verified 10(30건) · 실패 0 · description `saero 10-06`**(이름 원본 = `audit/exclusions.csv`, 승인 파일 `work/approved_2026-10-06_092804.txt`) — 8번노원 · 노원역4호 · 노원역9출구 · 노원역네일새로오픈 · 노원역도착 · 노원역새로맛집 · 노원역화장 · 노원체험시설 · 노원체형교정필라 · 노원행사10월 | 10/5 첫 등장 각 1회·확장·클릭 0. 3그룹 284 → 294. 10/7부터 판정 |
| **2026-09-30 07:56 자동 등록(스킬 `push` 참조 선택 모드, 사용자 승인 "등록 승인 9개" + 블루창동점 "제외시켜줘" → 두 해석 dry-run(9·10개) 뒤 답 "B"(10개) — Code 탭 `/saero-run`)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 10 · verified 10(30건) · 실패 0 · description `saero 09-30`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-09-30` 행 30개 · 승인 파일 `work/approved_2026-09-30_075651.txt` 10줄: propose 창 9/29 `_candidates.txt` 1~9 + `_industry.txt` 1 = 노원필라테스블루창동점) | 네 번째 자동 회차, 커밋 `04e7205`. 등록 뒤 3그룹 각 243개. **대조 시작 10/1**(9/30은 등록 당일). propose는 경쟁사 채택(config `8ea8c14`) 뒤 다시 돌린 것 — 후보 9 번호 불변, 업종어 8 → 7(시소가 경쟁사명으로 빠짐) |
| **2026-10-05 23:41 자동 등록(스킬 `push` 참조 선택 모드, 사용자 승인 "등록 승인 10개" — Code 탭 `/saero-run`)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 10 · verified 10(30건) · 실패 0 · description `saero 10-05`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-10-05` 행 30개 · 승인 파일 `work/approved_2026-10-05_234157.txt` 10줄: propose 창 10/1~10/4 `_candidates.txt` 1~10) | 커밋 `6567a47`. 3그룹 274 → 284. **대조 시작 10/6** |
| **2026-10-04 07:51 자동 등록(스킬 `push` 참조 선택 모드 — 10/4 세션, last-audit 기록 없이 끝남. 이 행은 10/5 회차가 커밋·registry로 복원)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 22 · registry 3그룹 전부 registered(미등록·실패 0) · description `saero 10-04`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-10-04` 행 · 승인 파일 `work/approved_2026-10-04_075158.txt` 22줄: propose 창 10/1~10/3) | 커밋 `b46aa4c`. 3그룹 252 → 274. 사용자 승인 답 원문은 남지 않음. **대조 시작 10/5** |
| **2026-10-01 08:11 자동 등록(스킬 `push` 참조 선택 모드, 사용자 승인 "등록 승인 9개" — Code 탭 `/saero-run`)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 9 · verified 9(27건) · 실패 0 · description `saero 10-01`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-10-01` 행 27개 · 승인 파일 `work/approved_2026-10-01_081100.txt` 9줄: propose 창 9/30 `_candidates.txt` 1~9) | 다섯 번째 자동 회차, 커밋 `440c357`. 등록 뒤 3그룹 각 252개. **대조 시작 10/2**(10/1은 등록 당일). propose는 경쟁사 채택(config `7c02571`) 뒤 다시 돌린 것 — 후보 파일 바이트 동일(cmp), 업종어 10 그대로 |
| **2026-09-29 09:34 자동 등록(스킬 `push` 참조 선택 모드, 사용자 승인 "후보 10개 그대로 다 해줘" + 업종어 1·3 — 이 PC Code 탭 `/saero-run` 첫 실사용)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 12 · verified 12(36건) · 실패 0 · description `saero 09-29`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-09-29` 행 36개 · 승인 파일 `work/approved_2026-09-29_093447.txt` 12줄: propose 창 9/28 `_candidates.txt` 1~10 + `_industry.txt` 1·3 = 솔라필라테스상계주차·노원구필라테스47평) | 세 번째 자동 회차, 커밋 `676359f`. 원문 그대로("노원." 마침표 포함). 등록 뒤 3그룹 각 233개 동일, registry 701행. **대조 시작 9/30**(9/29는 등록 당일) |
| **2026-09-28 자동 등록(스킬 `push`, 사용자 승인 "등록 승인 6개 전부" — 실행은 사장님 PC 데스크톱 앱 Code 탭(Claude Code) 세션)** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 5 · verified 5 · 실패 0 · description `saero 09-28`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-09-28` 행 15개: 노원역24시간 · 노원역감성맛집 · 노원역근처건물 · 노원역스텝 · 노원우동집 × 3그룹) | 두 번째 자동 회차, 커밋 `bf3089e`. 승인 6개 중 "노원힐링장소."는 Code 탭 세션이 끝 마침표를 문장부호로 보고 "노원힐링장소"(09-17 3그룹 기등록)로 판정해 건너뜀 — **마침표 붙은 원문은 미등록**(규칙은 원문대로. 1회짜리라 재노출 없으면 그대로, 잡히면 수동 재상정). 등록 뒤 3그룹 각 221개 동일. **대조 시작 9/29**(9/28은 등록 당일). 판정은 registry로 |
| **2026-09-27 14:08 자동 등록(스킬 `push`, 사용자 승인 "등록 승인 33개")** | 파워링크 3그룹 "확장 검색" 칸(API) | **요약 행 — 등록 33 · verified 33 · 실패 0 · description `saero 09-27`**(이름 원본 = `audit/exclusions.csv` `registered_at=2026-09-27` 행 99개 = 09-23 목록 미등록 22 + 09-27 제안 11) | 첫 자동 회차. 등록 뒤 3그룹 216개 동일. **대조 시작 9/28**(9/27은 등록 당일). 재노출 판정은 registry로(SKILL 5-0단계) — 이 표에 이름은 다시 적지 않는다 |
| **2026-09-27 API 첫 읽기(pull, 등록 없음)** | 파워링크 3그룹(노원산전 `…072697414` · 노원역 `…072288536` · 상계동 `…072587864`) | (이름 원본은 `audit/exclusions.csv` — 확장 검색 제외 **183개 × 3그룹, 세 목록 동일**) | 등록일(KST) 09-10 38 · 09-17 73 · 09-20 17 · 09-21 22 · 09-24 9 · 09-25 11 · 09-26 13. 아래 09-23 행의 32개 중 API 등록 10개·미등록 22개, 09-27 제안 14개 미등록 → 재등록 후보 33개(첫 자동 회차). 09-10 행의 1번출구·5번출구·정기주차·지도는 실명 노원역1번출구·노원역5번출구·노원역정기주차·노원역지도로 등록돼 있음. 이 표는 이제 요약 행만, 판정은 registry |
| **2026-09-27 제안(미등록 — 사용자 답 대기 중)** | (등록 시 파워링크 3개 그룹 "확장 검색" 칸) | 무관 10: 노원역헬스장 · 노원식당맛집 · 새로클린노원 · 노원아띠 · 노원역24시간우동 · 노원역7번출구주차 · 노원역9번 · 노원역맛집출구 · 노원역보세 · 노원역새로오픈소고기 / 애매 1: 노원필테강사 / 재등록 제안 3(09-23 32개 중): 노원역10번출구 · 노원역배스킨 · 노원체험 | 9/26 첫 등장 16개 중 11개(전부 "확장"·클릭 0). 사용자가 등록하면 이 행에 등록일을 채우고 **다음 날부터 대조**. 등록 안 하면 행 유지(후보로 다시 올리지 말고 "미등록"으로만). **09-27 UI 실측: 14/14 세 그룹 어디에도 미등록** → registry `unregistered`, 첫 자동 회차 재등록 후보 33개에 포함 → **2026-09-27 14:08 스킬로 14개 전부 등록·확인 완료(위 요약 행)** |
| 2026-09-26 (사용자 등록 완료 확인) | 파워링크 3개 그룹 (사용자 확인 09-26) | 노원역에새건물 · 노원역추석영업 · 6세필라테스 · 노원역두 · 노원역월 · 노원역스튜디오 | 6개. 9/25 첫 등장 12개 중 무관 2 + 키즈 1 + 사용자 판단으로 뺀 애매 3. 전부 "확장"·클릭 0. **대조 시작 9/27**(9/26은 등록 당일) |
| 2026-09-26 (재등록, 사용자 확인) | 파워링크 3개 그룹 (사용자 확인 09-26) | 노원구어린이 · 노원역9번출구 · 노원9월행사 · 노원역추석 · 노원어린이체험 · 노원역6번출구 · 노원역테니스레슨 | 09-23 등록 32개 중 9/25에 재노출된 7개를 다시 등록. 탭 목록에 원래 있었는지는 사용자가 말하지 않음 — **다시 묻지 말 것**. **이 7개는 9/27부터 다시 판정**, 32개 중 나머지 25개는 계속 대조 |
| 2026-09-25 (13:13경 등록 완료, 사용자 확인) | 파워링크 3개 그룹 "확장 검색" 칸 (사용자 확인 09-25) | 노원구체험관 · 노원역생선구이새로오픈 · 노원역아기옷 · 노원역의류 · 노원역카페새로생긴 · 한스노원역 · 노원아기랑체험 · 노원스텝핑 · 노원역어깨 · 노원역쾌적한 · 노원역금호스 | 11개. 9/24 첫 등장 무관 6 + 키즈 1(노원아기랑체험, 누적 6) + 사용자 결정으로 제외한 애매 4(노원스텝핑 9회 등). 전부 "확장"·클릭 0. 메모장 파일로 전달(09-25). 사용자가 11개 원본을 채팅에 다시 붙여 등록 확인 — 위 목록과 일치. **대조 시작 9/26**(9/25는 등록 전후 혼재 — 판정 안 함, 잡히면 "등록 당일"로만 표시) |
| 2026-09-24 | 파워링크 3개 그룹 제외 검색어 "확장 검색" 칸 (사용자 등록 완료 확인 09-24) | 노원역24시 · 노원역7번출구식당 · 노원역위치 · 노원아기역 · 노원역아기역 · 7세필라테스 · 노원아기랑필라테스 · 노원새로필라테스경력 · 노원역다인원 | 9개. **대조 시작 9/25.** 9/23 첫 등장 무관 3 + 키즈 계열 3 + 사용자 결정으로 제외한 애매 3(09-24). 9개 전부 "확장" = 파워링크 자동매칭 유래. "노원역24시"는 09-23 목록의 "노원역;24시"와 다른 문자열 |
| 2026-09-23 | 파워링크 그룹 제외 검색어 "확장 검색" 칸(제안 위치. 사용자는 "그날 등록했어"라고만 함 — 09-24 확인) | 노원역9번출구 · 노원역+9번출구 · 노원역2번출구 · 노원역6번출구 · 노원역10번출구 · 노원역8번출구 · 노원역출구 · 노원체험 · 노원역세 · 노원역금 · 노원역거리 · 노원역혼자 · 노원역힐링공간 · 노원역추천장소 · 노원역추석 · 노원역;24시 · 노원역11-210 · 11번노원 · 노원9월행사 · 노원]하루공간 · 노원새로오픈술집 · 노원역새로오픈술집 · 노원새로오픈사우나 · 노원역테니스레슨 · 노원역배스킨라빈스 · 노원역배스킨 · 노원역아기 · 아기랑노원구 · 노원구어린이 · 노원구어린이체험 · 노원어린이체험 · 노원역키즈 | 32개. **대조 시작 9/24**(9/23은 등록 당일 — 6개 이름 9회 잡혔으나 판정 안 함). **9/24 첫 판정일에 6개·11회 재노출**(노원역6번출구 4·노원역추석 3·노원역거리·노원구어린이·노원어린이체험·노원역키즈 각 1) — 등록 위치는 파워링크 3개 그룹 "확장 검색" 칸으로 맞음(09-25 사용자 확인). 원인 미상, 9/25 이후에도 잡히면 제외 검색어 탭 목록 확인 요청. **9/25에도 7개·13회 재노출(이틀 연속) → 09-26 사용자가 7개 재등록(아래 09-26 재등록 행), 9/27부터 다시 판정.** 9/21·9/22 첫 등장 무관 검색어 + 키즈 새 이름 6 + 배스킨 표기 변형 2(9/21 등록분 "베스킨"과 다른 문자열). 8번출구·출구는 이전 목록 포함 가능(중복은 시스템이 거름). "운동" 계열은 사용자 판단으로 별도 문의. **09-27 UI 실측: 32개 중 22개가 세 그룹 어디에도 미등록**(재노출 원인 = 등록 누락, "등록돼 있는데도 노출" 0) — 10개만 등록돼 있음(09-26 재등록 7 + 노원역8번출구·노원역출구·노원역배스킨라빈스). 22개는 registry `unregistered`로 첫 자동 회차 재등록 후보 → **2026-09-27 14:08 스킬로 22개 전부 등록·확인 완료(위 요약 행, 대조 시작 9/28)** |
| 2026-09-21 | 파워링크 그룹 제외 검색어 "확장 검색" 칸 | 노원역오꼬 · 노원역역맛집 · 노원추석영업 · 노원추석행사 · 노원역정정 · 노원역운영중 · 노원역마음 · 노원구GODTK · 노원역락커 · 노원역가족 · 노원새로오픈한카페 · 노원역+맛집 · 노원역베스킨라빈스 · 노원맘카페 · 노원역신규맛집 · 노원우동전문 · 우동집노원역 · 노원구우동 · 노원구아기랑 · 노원역아이랑 · 노원역아이와체험 · 노원역체험 | 유효 22개(사용자는 노원역체험을 두 번 넣어 23개 입력, 중복은 시스템이 거름). 대조 시작 9/22. 사용자 등록 완료 확인 09-21. 노원역체험은 09-17 등록분 재노출 건이라 여기서 재등록으로 종결 — 이후 잡히면 09-21 등록분으로 판정 |
| 2026-09-20 | 파워링크 그룹 제외 검색어 "확장 검색" 칸 | 주차노원역 · 노원역11번출구 · 노원역뷰카페 · 노원역7번출구카페 · 노원카페뷰 · 노원역일요일영업 · 행사노원구 · 노원복싱레슨 · 시니어필라테스복 · 노원역우동짜장 · 노원역세차 · 노원역출발 · 노원역맛집내돈내산 · 노원구아기 · 노원역아기랑 · 노원키즈필라테스 · 노원필라테스강사 | 17개. 대조 시작 9/21. 사용자 등록 완료 확인 09-20 |
| 2026-09-10 | 파워링크 4그룹 "확장 검색" 칸 | 원본 미보관(38개). 이름을 아는 것: 나다운필라테스·노원역주차장·노원역주차·정기주차·지도·5번출구·1번출구(09-17 기록 표기 그대로 — 앞에 "노원역"이 붙은 형태인지 미확인)·노원역카페·수정역필라테스·새로오픈 | 이름 아는 것만 대조 |
| 2026-09-17 | 파워링크 4그룹 | 원본 미보관(개별 67개 + 어근 7개: 맛집·우동·타이어·사진관·건물·까페·카페). 이름을 아는 것: 노원역헬스·노원역데이트·노원역운동·노원역체험 | 어근은 부분일치로 작동 안 함(09-19 판정) |
| 2026-09-17~19 | 파워링크 그룹 | 원본 미보관(79개, 9/19 개별 목록, 키즈 계열) | 대조 불가. 이름 단위 판정 대상 아님 |

## 2026-10-06 오후 갱신 회차 (진단 아님 — 리포트 배포 회차, 리포트 읽기 쉽게 회차 1(글) 첫 적용 · 경로 C) · Code 탭 `/saero-run`
합본 `일별` 2026.08.26~10.05 (41일, 오전 `cb0a3b1` 그대로) · 배포 커밋 `037aca8`(직전 `f7bc605`, 파일 sha 95b9974 → 624b770, 본문 104,921바이트·2,323행) · 집계 기간 `2026.08.26 — 10.05 (41일)`
validate.py 검사 23개 전부 PASS(precheck 요약 `검사 23개: PASS 23 / FAIL 0` — "07 각주 세 자리" 포함 첫 실사용) · compare.py 차이 0(항목 95, 직전 배포본 인자 `f7bc605` = prev.html md5 6aaa2472) · overflow 360/390/430 넘침 0 · narrative `[주의] 같은 기간 — 대조 생략(표지 36개 중 매회차 24개)` · 도장 full(작업본 002233ee · 직전 6aaa2472) · 재수령본 md5 일치(002233ee…, `verify --ref 037aca8` 1회째 일치)
`--pending` 사용: 아니오 — 채팅 질문 0건(2-1 같음 질문은 사용자 첫 말 "경로 C"로 미리 답함 · 승인 묶음 ⓐ 해당 0) · 배포: 사용자 첫 말 "보류" → 작업본 확인 뒤 사용자 "배포" → 7단계부터(도장 유효 — 작업본·직전 배포본 md5 불변)
**효율: 벽시계 약 7분(15:02 S0 → 15:07 도장, 사용자 확인 대기 뒤 15:08 PUT·verify) · 도구 호출 약 25회 · 즉석 코드 약 32행**(스크래치 `work/n1006c.py` — 본보기 `R1/n1006b.py` 흐름 그대로 + 이번 회차 META. `work/narr_lib.py`(18dd9c39)·`work/c40/compute.json`(81f475fb — 지난 회차 값 = 10/5 배포본)은 `D:\saero\feat-20261006-readable\work\` 에서 사본. apply 는 저장소 `scripts/apply.py`(E2 저장소판 첫 운영 사용). 리포트 숫자는 전부 compute.json)
- 2-1단계 선확인 작동(배포본 41일 = 합본 41일 → 같음). 사용자 첫 말 "경로 C" = 답 "다시 계산". 수집·ingest 는 돌리지 않음(오전 회차 합본이 10/5까지 완전 — 10/6 은 미집계). 제외 그룹 신규 후보 없음(같은 데이터 — 오전 판정 그대로). 01·06 min-width·라벨 41 그대로(apply 변경 없음).
- **글 줄이기 첫 적용**: `wrap_old`(01 머리글 2줄 · 01 하루 분해 각주 · 07 ✓ · 07 ⚠️ 삭제 + 표지 뼈대) → `texts_1006` → `rep_all` — 표지 36(매회차 24 · 고정 12, 06 카드 2 포함). 결과가 검증 회차에서 확인한 리허설 R1(002233ee)과 바이트 동일 — 리허설 관찰값 그대로 글자 수(표 제외) 16,493 → 8,215 · 390×844 높이 21.3 → 16.4장.
- **이번 회차 META(사실 확인)**: 등록 = propose 빈 창(등록 0) → 최근 등록 10/6 오전 10개, `verify --approved work/approved_2026-10-06_092804.txt` 3그룹 각 10/10(30/30) · 실패 0 / 재노출 = 10/5 창 propose 판정 0건 → "9/20~10/4 등록분 10/5까지 재노출 0" / 경쟁사 = compute 40행·후보 [] → 새 판정 없음, 최근 판정 10/6(토브 아님 · 노원부티필라테스 행) / 연속 회차 수 = 같은 기간 재배포라 10/6 배포본 그대로(자동매칭 25 · 최다 시간 22 — 사용자에게 알림).
- **11번 판정**: 지난 회차(10/5 배포본) 8개 → 유지 7 · 뒤집힘 1 · 근거 소멸 0(10/6 배포본 판정 줄과 같음). 이번 요약은 본보기 규칙대로 결론 1문장 + 괄호.
- **12번 이월 판정**: 상시 유지 1(제외 검색어) · 보류 유지 1(상계동 — 30회 이상인 날 조건 미달) · 신규·철회 0.
- 제외 검색어(5-0단계): pull 3그룹 각 294(registry 바이트 불변 — 커밋 없음) · 재노출 판정 0건(빈 창) / 후보 0 → 승인 0 → 등록 0 / registry 885행
- propose 창 2026-10-06~2026-10-05(빈 창) · 등록 미룸(사용자): 아니오
- **사용자에게 요청한 값**: ① 작업본 미리보기(`work/index.html`) — 연속 회차 수를 늘리지 않은 판단을 함께 알림 ② 답 "배포" → 7단계 dry-run(도장·base·권한 참) → PUT `037aca8` → verify `--ref` 일치(15:08).
- 다음 회차 대조: 표지 기반 첫 데이터 회차(ⓑ — narrative 가 매회차 24자리 대조, 같은 기간 생략 아님) / propose `--since 2026-10-06` / 10/6 등록 10개는 10/7부터 판정 / "N회차 연속"은 이 배포본 + 1 / 회차 2(모양)는 별도 탐색·구현 회차.

## 2026-10-06 갱신 회차 (진단 아님 — 리포트 배포 회차) · Code 탭 `/saero-run`
합본 `일별` 2026.08.26~10.05 (41일) · 배포 커밋 `f7bc605`(직전 `6829f71`, 파일 sha 9d693d5 → 95b9974, 본문 123,360바이트·2,340행) · 집계 기간 `2026.08.26 — 10.05 (41일)`
validate.py 검사 22개 전부 PASS(precheck 요약 `검사 22개: PASS 22 / FAIL 0` — KPI 노출 12,222 / 클릭 389 / CTR 3.18% / 광고비 443,384원, 제외 전 전체 12,228 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 `6829f71` = prev.html md5 95c58082) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(6aaa2472…, `verify --ref f7bc605` 1회째 일치)
`--pending` 사용: 아니오 — 채팅 질문 1건(승인 묶음 ⓐ: (2) 토브필라테스 · (4) 제외 검색어 10개) · 되묻기 0 · 배포 질문 0(자동 배포)
**효율: 벽시계 약 10분(09:24 S0 → 09:33 verify, 사용자 답 대기 포함) · 도구 호출 약 45회 · 즉석 코드 약 240행**(스크래치: apply.py 재사용(수정 0 — **E2 일곱 번째 재사용**) / n1006.py 약 150 — 서술 교체(n1005 표지 그대로) / 인라인 약 90 — 제외 그룹·10/5 그룹·검색어·지역·시간대(옛 배포본 차)·경쟁사 집계. precheck DIFF 3곳은 작업본 sed 3줄. 리포트 숫자는 전부 compute.json)
- **1단계**: S0 PASS → `fetch_reports.py --prev ~/saero-fetch/downloads/2026-10-05`(백그라운드, `이번달` 10/1~10/5 — 4개 검사 PASS·노출합 1,219 일치) → `ingest.sh` 시작 검사 통과 → store 4종(`data/2026-10` 덮어쓰기) → combine PASS(8월 2,363/50/36,397 + 9월 8,646/301/366,466 + 10월 1,219/38/40,521 = 41일 12,228/389/443,384원) → push `cb0a3b1`.
- 2-1단계 선확인 작동(배포본 40일 ≠ 합본 41일). 제외 그룹 신규 후보 없음(노원키즈 최근 3일 노출 0은 09-17 규칙대로 04번 행 유지). 01·06 min-width 3280·라벨 41. 05 top5 순서 변동 없음.
- **10/5(월)**: 노출 219(플 138·파 81)·클릭 6(플 5·파 1)·CTR 2.74%·광고비 7,122원(플 6,803·CPC 1,361 / 파 319) — 나흘 연속 감소 뒤 반등. 플레이스 순위 4.18 = 8/27(4.63) 이후 최저, 누적 3.10 → 3.12. 상향 뒤 열아흐레 11,529원·7.9건·CPC 1,460(상향 전 9,658·7.2·1,344) → 상향 유지 결론 유지. 누적 CTR 3.19 → 3.18, 검색 지면 3.73 → 3.71%.
- **11번 판정**: 직전 8개 → 유지 7 · 뒤집힘 1(나흘 연속 감소 → 10/5 반등, 맨 위) · 근거 소멸 0. 이번 8개 + (참고) 2. 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어: 9/20~10/4 등록분 전부 10/5까지 재노출 0 — 10/4 등록 22개 판정 첫날 0, 10/5 등록 10개는 10/6부터, 10/6 등록 10개는 10/7부터) · 보류 유지 1(상계동 10/5 5회, 하루 평균 16.8 → 16.5). 신규·철회 0.
- **07번**: 정식표 24행 그대로 + 클릭1건 33 → 35(토브필라테스 첫 클릭·노원1:1필라테스체험 첫 등장) + 경쟁사 6 = 389. 상위2 45%. 클릭 0 전체 743개·2,236회(24회차 연속 증가). 행 단위 확장·클릭0 10/4 31 → 10/5 68회(36개 — 새로필라테스 13·부티 12·노해로 8).
- **08번**: 1~7위 같음, 성남 수정구 205(9 → 8)·남양주 203(8 → 9)·중구 167(10), 11위 의정부 162·5건. 노원 46%·48%, 타겟 62%·59%(CTR 2.99), 확인불가 642·32·40,569원(8.7 → 9.1%, CTR 4.98), 타겟 밖 서울 1,742·69·3.96%, 서울·경기 밖 3.2% → 전국 유지.
- **09·10번**: 15시 32회 22회차 연속, 2위 9시·13시·20시 29 동률(compare 형식상 "2위는 9시 29회로 13시·20시(각 29회)와 같아졌음"). 10/5 시간대는 옛 배포본 hourlyChart와의 차(1시 1·20시 2·23시 3 — 심야 4건). 심야 2,675·88·86,400원(22%·23%). 10번 A 10,304·387·442,226 / B 172(10/5 1회) / C 22 / D 1,724, 콘텐츠 30일 연속 0.
- **precheck 재실행 2회**: compare DIFF ① 05 "모바일이 노출의 80.3%"(서술 스크립트가 안 건드린 자리 → 80.4) ② 08 "비용 비중 5%는 3.2%로 미달" → "3.2 → 3.2%로"(파싱 형식) ③ 09 "2위는 9시·13시·20시 29회" → "2위는 9시 29회로 …"(파싱 형식). 작업본 sed로 고친 뒤 OK 95 / DIFF 0. 코드 변경 0.
- **제외 검색어(5-0단계)**: pull(3그룹 각 284, registry `verified_at` 갱신) → propose `--since 2026-10-05`: 재노출 판정 0건 / 신규 후보 10 · 업종어 포함 7 · 재등록 0 · 뺀 것 9 → dry-run 10개(`[주의]` 0) → **등록 10 · verified 10(30건) · 실패 0**, description `saero 10-06`, 3그룹 284 → 294, registry 885행 → 커밋 `9e67e66`.
- **경쟁사**: config 변경 없음. 07 표 39 → 40행(노원부티필라테스 9 — 부티 변형, compute `신규변형후보`). 10/5 경쟁사명 23회·클릭 0. **토브필라테스**(09-20 종결 뒤 10/5 일치 2·클릭 1, 웹 검색 특정 불가) → 승인 묶음 (2) → 사용자 **"아님"** → 경쟁사 아님 확정, 클릭1건 목록. 포인트(2)·아라·피오르(각 1) 1~2회짜리 보류. 포미·포레 10/5 추가 0.
- **사용자에게 요청한 값**: ① 승인 묶음 — 답 "토브 => 아님 / 등록 승인 10개"(N 숫자, 되묻기 0) ② 배포 — 묻지 않음: precheck·dry-run 통과 뒤 바로 PUT `f7bc605` → verify `--ref` 일치.
- 제외 검색어(5-0단계): 재노출 판정 0건(등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0) / 후보 10 → 승인 10 → 등록 10 · verified 10 · 실패 0(saero 10-06) / registry 885행
- propose 창 2026-10-05~2026-10-05 · 등록 미룸(사용자): 아니오
- 다음 회차 대조: propose `--since 2026-10-06` / 10/5 등록 10개는 10/6부터 · 10/6 등록 10개는 10/7부터 판정 / 9/20~10/4 등록분 0 유지 / 10/5 반등이 이어지는지 / 플레이스 순위 4위대가 이어지는지 / 확인불가 비용 비중 9%대 / 포인트·아라·피오르·포미·포레 추가 노출(없으면 종결) / 노원역정원필라테스·노원필라테스힐링정원(어순 변형, 표 밖) 재등장

## 2026-10-05 갱신 회차 (진단 아님 — 리포트 배포 회차) · Code 탭 `/saero-run`
합본 `일별` 2026.08.26~10.04 (40일) · 배포 커밋 `6829f71`(직전 `4855509`, 파일 sha 76e84e5 → 9d693d5, 본문 124,172바이트·2,322행) · 집계 기간 `2026.08.26 — 10.04 (40일)`
validate.py 검사 22개 전부 PASS(precheck 요약 `검사 22개: PASS 22 / FAIL 0` — KPI 노출 12,003 / 클릭 383 / CTR 3.19% / 광고비 436,262원, 제외 전 전체 12,009 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 `4855509` = prev.html md5 4abc773f) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(95c58082…, `verify --ref 6829f71` 1회째 일치)
`--pending` 사용: 아니오 — 채팅 질문 1건(승인 묶음 ⓐ: (2) 보람상가필라테스 · (4) 제외 검색어 10개) · 되묻기 0 · 배포 질문 0(자동 배포)
**효율: 벽시계 약 18분(23:32 S0 → 23:50 verify, 사용자 답 대기 포함) · 도구 호출 약 55회 · 즉석 코드 약 260행**(스크래치: apply.py 재사용(수정 0 — **E2 여섯 번째 재사용**) / n1005.py 약 150 — 서술 교체(표지 찾기) / 인라인 약 110 — 제외 그룹·창 검색어·창 일별·시간대(옛 배포본 차)·경쟁사 창 집계. 리포트 숫자는 전부 compute.json)
- **1단계**: S0 PASS → `fetch_reports.py --prev ~/saero-fetch/downloads/2026-10-04`(백그라운드, `이번달` 10/1~10/4 — 4개 검사 PASS·노출합 1,000 일치) → `ingest.sh` 시작 검사 통과 → store 4종(`data/2026-10` 덮어쓰기) → combine PASS(8월 2,363/50/36,397 + 9월 8,646/301/366,466 + 10월 1,000/32/33,399 = 40일 12,009/383/436,262원) → push `0e9ba66`.
- **10/4 세션(기록 없음)**: 커밋만 남음 — `0399244` 보관본(39일) · `02a2b64` config `competitors`에 "니드필라테스" 추가(사용자 확인 2026-10-04 "경쟁사") · `b46aa4c` registry 22개 등록·확인(3그룹 252 → 274, `saero 10-04`, 승인 파일 `work/approved_2026-10-04_075158.txt` 22줄, propose 창 10/1~10/3). 배포·last-audit 기록 없음 → 배포본은 9/30(36일) 그대로였고, 이번 회차가 그 데이터까지 한 번에 반영.
- 2-1단계 선확인 작동(배포본 36일 ≠ 합본 40일). 제외 그룹 신규 후보 없음(노원키즈 최근 3일 노출 0은 09-17 규칙대로 04번 행 유지). 01·06 min-width·라벨 40일로 갱신. 05 top5 순서 변동 없음.
- **10/1~10/4**: 노출 320 → 276 → 204 → 200(나흘 연속 감소, 9/30 342 뒤)·클릭 13 → 8 → 4 → 7·광고비 12,917 → 8,949 → 5,307 → 6,226원. 플레이스 693회·22건·28,829원(10/3 4,845·10/4 4,077원 = 상향 뒤 가장 적은 이틀), 파워링크 307회·10건·4,570원(10/2 클릭 0). 플레이스 순위 3.32·3.97(9/14 이후 최저)·3.38·3.76, 누적 3.06 → 3.10. 상향 뒤 평균 13,102 → 11,792원·8.8 → 8.1건·CPC 1,491 → 1,464원(상향 전 9,658·7.2·1,344) → 상향 유지 결론 유지.
- **11번 판정**: 직전 8개 → 유지 6 · 뒤집힘 2(9/30 하루 최다 → 나흘 연속 감소 / 플레이스 순위·클릭 같은 방향 → 이어지지 않음, 맨 위) · 근거 소멸 0. 이번 8개 + (참고) 2. 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어: 9/20~10/1 등록분 전부 10/1~10/4 재노출 0, 10/4 등록 22개는 10/5부터, 10/5 등록 10개는 10/6부터) · 보류 유지 1(상계동 나흘 13·18·10·7, 하루 평균 17.4 → 16.8). 신규·철회 0.
- **07번**: 정식표 23 → 24행(임산부필라테스노원 10/1 첫 등장 7회·3건) + 클릭1건 28 → 33(노원3:1필라테스·노원구역필라테스가격·노원역5번출구근처필라테스·시니어새로필라테스 첫 등장, 창동역운동 누적 48회 첫 클릭) + 경쟁사 6 = 383. 상위2 45%. 클릭 0 전체 720개·2,179회(23회차 연속 증가). 행 단위 확장·클릭0 10/2 65 → 10/3 45 → 10/4 31회(23개).
- **08번**: 1~6위 같음, 영등포 214(7)·남양주 201(8)·성남 수정구 199(7 → 9)·중구 166(10), 11위 의정부 160·5건. 노원 46%·48%, 타겟 62%·58%(CTR 2.99), 확인불가 630·30·37,795원(8.7%, CTR 4.76), 타겟 밖 서울 1,712·69·4.03%, 서울·경기 밖 3.2% → 전국 유지.
- **09·10번**: 15시 32회 21회차 연속, 2위 9시·13시 29 동률. 창 시간대는 옛 배포본 hourlyChart와의 차로 구함(심야 6건 — 2시 1·6시 2·7시 1·22시 1·23시 1). 심야 2,593·84·82,362원(22%·22%). 10번 A 10,086·381·435,104 / B 171(10/4 4회) / C 22 / D 1,724, 콘텐츠 29일 연속 0.
- **compare.py 수정(이 회차, 코드 1줄)**: 171행 `10 파트너 마지막날` 정규식 `— 9/\d+는 (\d+)회` → `— \d+/\d+는 (\d+)회`. 마지막 날이 10/4라 "— 10/4는 4회"로 쓰면 9월 고정 정규식이 못 찾아 precheck가 멈춤(사실과 다른 "9/30는" 문구로 맞추는 대신 정규식을 넓힘). 같은 꼴의 날짜 고정은 compare.py·validate.py에 이 1곳뿐(grep `9/`). 판정 기준(값 = compute `파트너마지막날`)은 그대로. 검토 판정: 막음 0 · 이월 0(tests는 compare를 가짜 래퍼로만 부름 — 문구 의존 없음).
- **제외 검색어(5-0단계)**: pull(3그룹 각 274, registry `verified_at` 갱신) → propose `--since 2026-10-01`: 재노출 판정 22건 = 전부 10/4 등록분의 **등록 전 노출(정상)** / 신규 후보 10 · 업종어 포함 25 · 재등록 0 · 뺀 것 26 → dry-run 10개(`[주의]` 0) → **등록 10 · verified 10(30건) · 실패 0**, description `saero 10-05`, 3그룹 274 → 284, registry 854행 → 커밋 `6567a47`.
- **경쟁사**: config 변경 없음(니드필라테스는 10/4 `02a2b64`). 07 표 31 → 39행 — 니드 2(노원니드필라테스·니드필라테스노원) + 부티 변형 4(노원구노해로부티·노원노원구부티·노원상계동부티·노원상계부티) + 노원구솔라필라테스 + 와우필라테스노원점(전부 노원구·확장, compute `신규변형후보`). 창 경쟁사명 54회·클릭 0. **보람상가필라테스**(10/3 일치 5, 누적 8·클릭 0, 웹 검색 특정 불가) → 승인 묶음 (2) → 사용자 **"아님"** → 제외 확정. 헤븐·클립뷰 종결(추가 0). 포미·포레(각 일치 1, 첫 등장) 1회짜리 — 리포트 미언급 보류.
- **사용자에게 요청한 값**: ① 승인 묶음 — 답 "보람상가필라테스 => 아님 / 등록 승인 10개"(N 숫자, 되묻기 0) ② 배포 — 묻지 않음: precheck·dry-run 통과 뒤 바로 PUT `6829f71` → verify `--ref` 일치(23:50).
- 제외 검색어(5-0단계): 재노출 판정 22건(등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0 — 22건 전부 등록 전 노출) / 후보 10 → 승인 10 → 등록 10 · verified 10 · 실패 0(saero 10-05) / registry 854행
- propose 창 2026-10-01~2026-10-04 · 등록 미룸(사용자): 아니오
- 다음 회차 대조: propose `--since 2026-10-05` / 10/4 등록 22개는 10/5부터 · 10/5 등록 10개는 10/6부터 판정 / 9/20~10/1 등록분 0 유지 / 노출 감소가 이어지는지(평일 회복 여부) / 플레이스 광고비 일예산 대비 / 니드 행 노출 / 포미·포레 추가 노출(없으면 종결) / 노원역정원필라테스·노원필라테스힐링정원(어순 변형, 표 밖) 재등장

## 2026-10-01 갱신 회차 (진단 아님 — 리포트 배포 회차) · Code 탭 `/saero-run` 세 번째 실사용 · 월초
합본 `일별` 2026.08.26~09.30 (36일) · 배포 커밋 `4855509`(직전 `961789d`, 파일 sha 563bdde → 76e84e5, 본문 121,951바이트·2,209행) · 집계 기간 `2026.08.26 — 09.30 (36일)`
validate.py 검사 22개 전부 PASS(precheck 요약 `검사 22개: PASS 22 / FAIL 0` — KPI 노출 11,003 / 클릭 351 / CTR 3.19% / 광고비 402,863원, 제외 전 전체 11,009 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 `961789d` = prev.html md5 fc2e48d3) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(4abc773f…, `verify --ref 4855509` 1회째 일치)
`--pending` 사용: 아니오 — 채팅 질문 1건(승인 묶음 ⓐ: (2) 써니·플로우·비비 · (4) 제외 검색어 9개) · 되묻기 0 · 배포 질문 0(자동 배포 첫 회차)
**효율: 벽시계 약 14분(08:03 S0 → 08:17 verify, 사용자 답 대기 포함) · 도구 호출 약 45회 · 즉석 코드 약 230행**(스크래치: apply.py 재사용(주석 1줄만 — **E2 다섯 번째 재사용**) / n1001.py 약 150 — 서술 교체(문구는 데이터, 이번부터 표지 찾기) / facts.py·facts2.py 재사용(날짜만 sed) / 인라인 약 80 — 9월 확정본 대조·제외 그룹·9/30 시간대(옛 CSV와 차)·목록 변동. 리포트 숫자는 전부 compute.json — 계산 코드 0행)
- **1단계**: S0 PASS(08:04) → `fetch_reports.py --debug`(`--prev` 생략, 백그라운드, **`지난달` 9/1~9/30 — 4개 검사 PASS·노출합 8,646 일치**) → `ingest.sh` 시작 검사 통과 → store 4종(`data/2026-09` 덮어쓰기) → combine PASS(8월 2,363/50/36,397 + 9월 8,646/301/366,466 = 36일 11,009/351/402,863원) → push `f931162`. 9월 확정본은 9/1~9/29 일별 값이 직전 보관본과 같음(키워드·검색어·상세지역 날짜별 대조, 시간대별은 합만) — 9/30 342·17·22,127원만 더해짐.
- 2-1단계 선확인 작동(배포본 35일 ≠ 합본 36일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·0.05% / 노원키즈 최근 3일 [0,0,0]은 09-17 규칙대로 04번 행 유지). 01·06 min-width 2800 → 2880, 라벨 `[36, 36]`. 05 top5 순서 변동 없음.
- **9/30(수)**: 노출 342(플 267·파 75)·클릭 17(플 12·파 5)·CTR 4.97%·광고비 22,127원(플 19,246·CPC 1,604 / 파 2,881·CPC 576). 클릭 17 = 9/22·9/28과 같은 하루 최다, 광고비 = 9/22(22,597) 다음 둘째. 파워링크 노출 92 → 75(이틀 연속 증가 끝), 클릭 5 = 9/13·9/7 다음 셋째, 전부 노원산전 자동매칭 → **노원산전 하루 5건 = 등록 이후 최다**(누적 20). 노원역필라테스 그룹 하루 순위 1.38 = 36일 최고. 플레이스 순위 3.55 → 3.13·CTR 4.49%. 누적 CTR 3.13 → 3.19, 검색 지면 3.75 → 3.79%. 상향 후 열나흘 13,102원·8.8건·CPC 1,491(9/30 하루 CPC 1,604 — 평균 기준 미달, 클릭 12건이라 재상정 아님).
- **11번 판정**: 직전 8개 → 유지 7 · 뒤집힘 1(파워링크 노출 이틀 연속 증가 → 9/30 감소, 맨 위) · 근거 소멸 0. 이번 8개 + (참고) 2. 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어: 9/29 등록 12개 판정 첫날 0, 그 앞 등록분 전부 0 유지, 9/30 등록 10개는 10/1부터, 10/1 등록 9개는 10/2부터) · 보류 유지 1(상계동 9/30 20회, 하루 평균 17.4). 신규·철회 0.
- **07번**: 정식표 21 → 23행(상계필라테스 둘째 클릭 진입·임산부필라테스노원구 첫 등장 2회·2건) + 클릭1건 28(마들역운동·벨필라테스 진입, 상계필라테스 이동) + 경쟁사 6(써니 1건 이동) = 351 중 정식 317·1건 28·경쟁사 6. 상위2 46 → 45%. 클릭 0 전체 646개·2,014회(22회차 연속 증가). 행 단위 확장·클릭0 54 → 43회(41개).
- **08번**: TOP 10 구성·순서 같음(영등포 183·남양주 171·중구 157), 11위 의정부 138. 컴팩트 37개·91건. 9/30 클릭 지역: 노원 8·중랑 2·도봉 1·서초·성동·종로 각 1·확인불가 2·해외 1. 노원 46%·49%, 타겟 63%·60%(CTR 3.08), 확인불가 563·28·34,829원(8.6%, CTR 4.97 — 9/30 46회), 타겟 밖 서울 1,581·62·3.92%, 서울·경기 밖 2.8% → 전국 유지.
- **09·10번**: 15시 29회 20회차 연속, 2위 9시 27 단독, 14시 26(9/30 3건) 3위. 9/30 시간대는 옛 보관본(9/1~9/29)과의 차로 구함 — 8시 4·9시 1·14시 3·15시 2·17시 2·20시 1·21시 3·22시 1. 심야 2,326·78·76,535원(21%·22%). 10번 A 9,102·349·401,705 / B 155(9/30 2회) / C 22 / D 1,724, 콘텐츠 25일 연속 0. 10번 파트너 문구는 compare 형식(`— 9/D는 N회`)이라 "9/30는".
- **제외 검색어(5-0단계)**: pull(3그룹 각 243, registry `verified_at` 갱신) → propose `--since 2026-09-30`: 재노출 판정 0건(등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0) / 신규 후보 9(무관 7·애매 2 — 노원구개인레슨·노원역주소) · 업종어 포함 10 · 재등록 0 · 뺀 것 10 → 경쟁사 채택 뒤 propose 재실행(후보 파일 바이트 동일) → dry-run 9개(`[주의]` 0) → **등록 9 · verified 9(27건) · 실패 0**, description `saero 10-01`, 그룹당 243 → 252, registry 731 → 758행, 커밋 `440c357`.
- **경쟁사**: **config 변경 `7c02571` — `competitors`에 "써니필라테스" 추가**(사용자 답 "노원 맞음"). 07 표 29 → 31행(노원써니필라테스 1·1건·338원 + 부티 변형 노원역부티필라테스 1 — 둘 다 노원구·확장, compute `신규변형후보`). 플로우(일치 4)·비비(일치 3) → 사용자 "노원 아님" → 표 미등재. 헤븐·클립뷰(각 1) 보류. 아워·미미·플러스·한국 종결(2회차 연속 0). 라임(2)·보니따·H·에반더 재등장 → 종결 유지. 노원M 변형(M필라테스노원역·노원M필라테스내돈내산후기 각 1) 표 미복귀 유지. 벨필라테스 9/30 첫 클릭(누적 7·1건) → 09-06 판정 유지, 클릭1건 목록. 9/30 젠 13(91 → 104)·이레 3·오운 2·스마일·퍼스트 각 1·정원 계열 3(표 안 29 → 32).
- **이월(작음)**: 어순 변형 "노원역정원필라테스"(9/30 확장 1) — config 이름(필라테스정원)을 포함하지 않고 직전 표에도 없어 compute 경쟁사 집합 밖 → 표에 넣으면 compare 차이. 이번엔 표 밖(07 각주에만 언급). 같은 이름이 다시 나오면 사람이 행을 넣는 경로(compute 집합 확장) 필요.
- **사용자에게 요청한 값**: ① 승인 묶음 — 답 "노원써니필라테스 => 노원 맞음 / 플로우필라테스·비비필라테스 => 노원 아님 / 등록 승인 9개"(N 숫자, 모호함 없음 — 되묻기 0) ② 배포 — 묻지 않음(2026-09-30 결정): precheck·dry-run 통과 뒤 바로 PUT `4855509` → verify `--ref` 일치(08:17). 자동 모드에서 판단기 거부 없음.
- propose 창 2026-09-30~2026-09-30 · 등록 미룸(사용자): 아니오
- 다음 회차 대조: **10/2는 `이번달` 첫 평일 — 10/1 하루치, `data/2026-10` 새 폴더**, propose `--since` = 2026-10-01 / 9/30 등록 10개는 10/1부터 · 10/1 등록 9개는 10/2부터 판정 / 9/29 등록 12개·9/28 5개·33·17·22·9·11·7·6개 0 유지 / 써니 행 노출·클릭 / 헤븐·클립뷰 추가 노출(없으면 종결) / 노원산전 하루 최다 뒤 / 파워링크 노출 방향 / 플레이스 순위·클릭 같은 방향 이어지는지 / 노원역정원필라테스 재등장.


## 2026-09-30 갱신 회차 (진단 아님 — 리포트 배포 회차) · Code 탭 `/saero-run` 두 번째 실사용
합본 `일별` 2026.08.26~09.29 (35일) · 배포 커밋 `961789d`(직전 `7846ddf`, 파일 sha e755fc9 → 563bdde, 본문 119,860바이트·2,165행) · 집계 기간 `2026.08.26 — 09.29 (35일)`
validate.py 검사 22개 전부 PASS(precheck 요약 `검사 22개: PASS 22 / FAIL 0` — KPI 노출 10,661 / 클릭 334 / CTR 3.13% / 광고비 380,736원, 제외 전 전체 10,667 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 `7846ddf` = prev.html md5 e869c1e8) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(fc2e48d3…, `verify --ref 961789d` 1회째 일치 — ls-remote HEAD = 961789d)
`--pending` 사용: 아니오 — 채팅 질문 1건(승인 묶음 ⓐ: (1) 시소 · (2) 블루창동점·솔라 · (4) 제외 검색어 9개) + 되묻기 1건(블루창동점 "제외시켜줘" 두 해석) + 배포 질문 1건(답 "배포")
**효율: 벽시계 약 45분(07:49 S0 → 08:34 verify, 사용자 답 대기 포함) · 도구 호출 약 50회 · 즉석 코드 약 200행**(스크래치: 09-29 apply.py 145행 재사용 + 신규 경쟁사 행 2행 수정 — **E2 네 번째 재사용**, 이번엔 새로 쓰지 않고 옛 스크래치에서 복사 / n0930.py 약 130 — 서술 교체(문구는 데이터) / facts.py·facts2.py 재사용(날짜만 sed) / 인라인 약 60 — 제외 그룹 판정·9/29 브랜드형 검색어·시간대·지역 사실. 리포트 숫자는 전부 compute.json — 계산 코드 0행)
- **1단계**: S0 PASS(07:50) → `fetch_reports.py --prev ~/saero-fetch/downloads/2026-09-29`(백그라운드, `이번달` 9/1~9/29, 4개 검사 PASS·노출합 8,304 일치, `[profile]` 정리 8건) → `ingest.sh` 시작 검사 통과 → store 4종 → combine PASS(8월 2,363/50/36,397 + 9월 8,304/284/344,339 = 35일 10,667/334/380,736원) → push `87028d3`(origin/main = HEAD 확인).
- 2-1단계 선확인 작동(배포본 34일 ≠ 합본 35일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·0.06% / 노원키즈 최근 3일 [0,0,0]은 09-17 규칙대로 04번 행 유지). 01·06 min-width 2720 → 2800, 라벨 `[35, 35]`. 05 top5 순서 변동 없음. 06 카드 큰 숫자 = 04 셀(상계동 2.58·노원산전 1.72).
- **9/29(화)**: 노출 315(플 223·파 92)·클릭 8(플 4·파 4)·CTR 2.54%·광고비 7,987원(플 5,423·CPC 1,356 / 파 2,564·CPC 641). 광고비는 9월 여섯째로 적은 날. **파워링크 92회 = 이틀 연속 증가, 9/22(110) 이후 최다**, 클릭 4 = 9/3과 같음(9/13 7·9/7 6 다음) — 노원역 직접 1(462) · 노원산전 자동매칭 3("노원그룹필라테스" 682·"노원산후필라테스" 715·"새로필라테스" 705). **노원산전 58회·3건 = 등록 이후 하루 최다**(노출 종전 9/21 47, 클릭은 9/13과 같음). 플레이스 순위 3.55(이틀 연속 하락, 닷새 최저)·CTR 1.79%(닷새 최저). 누적 CTR 3.15 → 3.13, 검색 지면 3.79 → 3.75%. 상향 후 열사흘 12,629원·8.5건·CPC 1,479.
- **11번 판정**: 직전 7개 → 유지 6 · 뒤집힘 1(플레이스 순위 낮은 날 클릭 많음 → 9/29 순위·클릭 같은 방향, 맨 위) · 근거 소멸 0. 이번 8개(새 항목 = 경쟁사 2곳 채택) + (참고) 2. 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어: 9/28 등록 5개 판정 첫날 0, 33·17·22·9·11·7·6개 0 유지, 9/29 등록 12개는 9/30부터, 9/29 첫 등장 10개 9/30 등록) · 보류 유지 1(상계동 9/29 14회, 하루 평균 17.3). 신규·철회 0.
- **07번**: 정식표 21행(노원산후필라테스 둘째 클릭으로 진입 — 16회·12.50%) + 클릭1건 27(노원그룹필라테스 진입·노원산후 이동) + 경쟁사 5 = 334 중 정식 302·1건 27·경쟁사 5. 상위2 45 → 46%. "필라테스" 9/29 79회·0건. 클릭 0 전체 625개·1,970회(21회차 연속 증가, 노출도 다시 증가 — 빠진 것 노원그룹필라테스 8회뿐). 행 단위 확장·클릭0 51 → 54회(38개, 그중 첫 등장 18).
- **08번**: TOP 10 구성 같음, 영등포 159 → 173(9/29 14회)으로 9 → 8위, 남양주 163 9위, 중구 155 10위. 11위 의정부 135. 컴팩트 36개·85건. 9/29 클릭 지역: 노원 3·중랑·양주·동작·송파·중구 각 1. 노원 46%·49%, 타겟 63%·60%(CTR 3.00), 확인불가 517·26·32,731원(8.6%, CTR 5.03), 타겟 밖 서울 1,510·59·3.91%, 서울·경기 밖 2.7% → 전국 유지.
- **09·10번**: 15시 27회 19회차 연속. **2위 9시 26회 단독**(9/29 4건 — 13시 25를 넘음), 14·20시 23. 심야 2,247·73·68,559원(21%·22%), 9/29 심야 클릭은 8시 1건. 10번 A 8,762·332·379,578 / B 153·2·1,158(9/29 10회) / C 22 / D 1,724, 콘텐츠 24일 연속 0.
- **제외 검색어(5-0단계)**: pull(3그룹 각 233, registry `verified_at` 갱신) → propose `--since 2026-09-29`: 재노출 판정 0건(등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0) / 신규 후보 9(무관 7·애매 2 — 노원발레레슨·노원인) · 업종어 포함 8 · 재등록 0 · 뺀 것 9 → 경쟁사 채택 뒤 propose 재실행(후보 9 불변 · 업종어 7 · 뺀 것 11) → 승인 10(후보 9 + 업종어 1) → **등록 10 · verified 10(30건) · 실패 0**, description `saero 09-30`, 그룹당 233 → 243, registry 701 → 731행, 커밋 `04e7205`.
- **경쟁사**: **config 변경 `8ea8c14` — `competitors`에 "필라테스시소"·"솔라필라테스" 추가**(사용자 답 "경쟁사 업체야"·"솔라필라테스 <= 노원 업체야"). 07 표 26 → 29행(노원필라테스시소·노원솔라필라테스·솔라필라테스상계주차 — 소재구 노원구·확장, apply.py 신규 행 처리). 9/29 젠 3(88 → 91)·와우 1·오운 1·노원필라테스정원 4(9 → 13, 정원 계열 25 → 29)·노원필라테스인 4(7 → 11)·필라테스인노원 1, 클릭 0. 블루창동점(확장 2, 웹 검색 특정 불가) → 사용자 "제외시켜줘" = 제외 검색어 등록(표 미등재). 모브 종결(2회차 연속 0). 아워·미미·플러스·한국 1회차째 보류. H·아름다운·체인지·에반더 재등장 → 종결 유지.
- **주의**: "솔라필라테스상계주차"는 채택 전(2026-09-29) 제외 검색어로 3그룹 등록돼 있다 — 경쟁사명은 원래 제외하지 않는 규칙(`never_exclude_competitors`)과 어긋나는 한 건. 사용자에게 알리고 그대로 둠(해제는 사용자 입회 `delete`만).
- **사용자에게 요청한 값**: ① 승인 묶음 — 답 "1. 경쟁사 업체야 / 2. 솔라필라테스 <= 노원 업체야 / 노원필라테스블루창동점 <= 창동에 있긴한데 제외시켜줘 / 4. 등록 승인 9개" → 블루창동점이 두 가지로 읽혀 9개·10개 dry-run을 보이고 A/B로 되물음 → 답 "B" → 10개 등록 ② 배포 — dry-run 뒤 고정 질문 → 답 "배포" → PUT `961789d` → verify `--ref` 일치(08:34). ③ 세션 중 사용자 지적 "왜 영어로 답해 한글로 해" — 진행 알림을 영어로 쓴 것, 이후 한글(메모리 기록).
- propose 창 2026-09-29~2026-09-29 · 등록 미룸(사용자): 아니오
- 다음 회차 대조: **10/1은 매월 1일 — `지난달` 프리셋(9/1~9/30 확정본, `--debug` 권장)으로 `data/2026-09` 덮어쓰기, `--prev` 생략**, propose `--since` = 2026-09-30 / 9/29 등록 12개는 9/30부터 · 9/30 등록 10개는 10/1부터 판정 / 9/28 등록 5개·33·17·22·9·11·7·6개 0 유지 / 시소·솔라 경쟁사 행 노출 / 아워·미미·플러스·한국 추가 노출(없으면 종결) / 플레이스 순위 하락 이틀 뒤 방향 / 파워링크 노출 증가 이어지는지 / 노원산전 하루 최다 뒤 / 2위 시간대 9시 / 영등포 8위.

## 2026-09-29 갱신 회차 (진단 아님 — 리포트 배포 회차) · **Code 탭 첫 실사용**(배포는 마감 뒤 사용자 "배포 해야해"로 후속 실행)
합본 `일별` 2026.08.26~09.28 (34일) · 배포 커밋 `7846ddf`(직전 `32d8b05`, 파일 sha 1c52f70 → e755fc9, 본문 117,923바이트·2,121행) · 집계 기간 `2026.08.26 — 09.28 (34일)`
validate.py 검사 22개 전부 PASS(precheck 요약 `검사 22개: PASS 22 / FAIL 0` — KPI 노출 10,346 / 클릭 326 / CTR 3.15% / 광고비 372,749원, 제외 전 전체 10,352 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 `32d8b05` = prev.html md5 a3465ec0) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(e869c1e8…, 3회째 verify — 앞 2회는 조회 캐시로 불일치, 맨 위 절)
`--pending` 사용: 아니오 — 채팅 질문 1건(승인 묶음 ⓐ: (2) 솔라·아워 애매 후보 + (4) 제외 검색어 10개 승인 문구). 솔라·아워는 답이 없어 보류로 적음
**효율: 벽시계 약 20분(09:27 시작 → 09:47 배포 dry-run, 사용자 답 대기 포함) · 도구 호출 약 75회 · 즉석 코드 약 230행**(스크래치: apply.py 145 — compute.json → HTML 기계 자리 교체(09-27·09-28에 이어 세 번째로 다시 씀) / facts.py 35·facts2.py 17 — 서술용 사실 / n11.py 20·n12.py 13 — 11·12번 문구 교체(문구는 데이터) / 인라인 약 15 — 제외 그룹 판정·9/28 검색어 목록. 리포트 숫자는 전부 compute.json — 계산 코드 0행. 직전 배포본 × 새 compute.json으로 `compare.py`를 돌려 바뀐 항목 74개를 한 번에 뽑은 것이 사실 확인을 줄였다)
- **1단계**: `fetch_reports.py --prev ~/saero-fetch/downloads/2026-09-28`(백그라운드, `이번달` 9/1~9/28, 4개 검사 PASS·노출합 7,989 일치, `[profile]` 정리 4건) → `ingest.sh` 시작 검사 통과 → store 4종 → combine PASS(8월 2,363/50/36,397 + 9월 7,989/276/336,352 = 34일 10,352/326/372,749원) → push `610864c`(origin/main = HEAD 확인).
- 2-1단계 선확인 작동(배포본 33일 ≠ 합본 34일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·0.06% / 노원키즈 최근 3일 [0,0,0]은 09-17 규칙대로 04번 행 유지). 01·06 min-width 2640 → 2720, 라벨 `[34, 34]`. 05 top5 순서 변동 없음. 06 카드 큰 숫자 = 04 셀(상계동 2.56·노원산전 1.70). costPie title 총액 372,749원(apply.py가 교체).
- **9/28(월)**: 노출 361(플 277·파 84)·클릭 17(플 14·파 3)·CTR 4.71%·광고비 21,450원(플 20,128·CPC 1,438 / 파 1,322·CPC 441). 클릭 17 = 9/22와 같은 개업 이후 하루 최다, 광고비 = 9/22(22,597) 다음 둘째, 노출 = 9/5(957) 이후 최다. **파워링크 84회 = 사흘 최저 갱신(57 → 46 → 42) 끊고 두 배**, 클릭 3(노원역필라테스 직접 2건 750원 · 노원산전 자동매칭 "노원필라테스추천" 572원). 플레이스 순위 3.22(닷새 중 최저)인데 클릭 14·하루 CTR 5.05%. 누적 CTR 3.09 → 3.15, 검색 지면 3.75 → 3.79%. 상향 후 열이틀 13,230원·8.9건·CPC 1,484.
- **11번 판정**: 직전 8개 → 유지 6 · 뒤집힘 1(플레이스 순위 2.83 → 3.22, 맨 위) · 근거 소멸 1("9/27 클릭 7건 전부 노원구" — 9/28은 노원 9·그 밖 8). 이번 7개 + (참고) 2. 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어: 33개 판정 첫날 0, 17·22·9·11·7·6개 0 유지, 9/28 등록 5개는 9/29부터, 9/28 첫 등장 12개 9/29 등록) · 보류 유지 1(상계동 9/28 23회, 하루 평균 17.4). 신규·철회 0.
- **07번**: 정식표 20행 294(마들필라테스 첫 클릭 2건으로 진입 — 클릭 0 목록 74회에서) + 클릭1건 27(신규 상계역운동·노원필라테스추천·노원구필라테스추천) + 경쟁사 5 = 326. 근처필라테스 4건·4.30%(강조 복귀). 중계역 16건·15.38%. 상위2 46 → 45%. 클릭 0 전체 608개·1,914회(개수 20회차 연속 증가, 노출 합계는 클릭이 붙어 빠진 94회 때문에 처음 감소), ≥5 목록 68개(퀸즈 6·노원필라테스안 6·노원시니어 5·라이프스포츠 5 진입). 행 단위 확장·클릭0 27 → 51회(32개).
- **08번**: TOP 10 구성 같음, 남양주 148 → 162(9/28 14회·1건)로 10위 → 8위, 영등포 159·중구 154가 9·10위. 11위 의정부 132. 컴팩트 36개·81건(광진 3 → 5, 신규 수원시 권선구 6·1). 9/28 클릭 지역: 노원 9·확인불가 3·광진 2·도봉·남양주·수원 권선 각 1. 노원 46%·50%, 타겟 63%·60%(CTR 3.04), 확인불가 501·26·32,731원(8.8%, CTR 5.19), 타겟 밖 서울 1,460·56·3.84%, 서울·경기 밖 2.8% → 전국 유지.
- **09·10번**: 15시 27회 18회차 연속. 2위 13시 25회 단독(9/28 3건 — 9시 22와의 동률 해소), 14시 23. 심야 2,174·72·67,652원(21%·22%), 9/28 심야 클릭은 8시 2건뿐. 10번 A 8,457·324·371,591 / B 143·2·1,158(9/28 3회) / C 22 / D 1,724, 콘텐츠 23일 연속 0.
- **제외 검색어(5-0단계)**: pull(3그룹 각 221, registry `verified_at` 갱신) → propose `--since 2026-09-28`: 재노출 판정 0건(등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0) / 신규 후보 10(무관 7·애매 3 — 노원예비맘·노원구맘은 산전 고객층일 수 있어 빼기를 권했으나 사용자가 전부 승인) · 업종어 포함 5 · 재등록 0 · 뺀 것 4(운동 2·산전 1·경쟁사명 1) → 승인 12(후보 10 + 업종어 1·3) → **등록 12 · verified 12(36건) · 실패 0**, description `saero 09-29`, 그룹당 221 → 233, registry 665 → 701행(등록 36행 — pull은 `verified_at`만 갱신), 커밋 `676359f`.
- **경쟁사**: config 변경 없음. 9/28 젠 5(83 → 88)·이레 2(8 → 10)·와우 1(26 → 27)·오운 1(16 → 17)·노원필라테스정원 3(6 → 9, 정원 계열 누적 25), 클릭 0, 26행 그대로. 이루다 종결(2회차 연속 0). 솔라 계열 재등장("솔라필라테스상계주차" 확장 2, 누적 3) → 보류 유지(웹 검색 특정 불가, 사용자 답 없음 — 그 검색어는 제외 등록됨). 신규 브랜드형 아워(일치 3)·미미·플러스·한국(각 1) 보류. 모브 1회차째. 노원엠 변형 2 → 4, 필라테스안 계열 8 → 10, 퀸즈 4 → 6, 고요 계열 1 재등장(종결 유지).
- **사용자에게 요청한 값**: ① 승인 묶음(솔라·아워 판단, 제외 검색어 승인) — 답 "등록 승인 N개 / 업종어 1·3 / 위 2가지만 등록" → 세션이 "2개만"으로 읽고 dry-run 2개를 보이며 확인 → 사용자 "후보 10개 그대로 다 해줘 오타났다" → 12개 dry-run → 등록 ② 배포 — dry-run 결과를 보이고 "배포" 답 대기 → 답 "마감"(배포 안 함, 마감 기록 `94c8298`) → 이어 "어떤 답을 원했던 거야? 배포 해야해" → 실제 push `7846ddf` → verify 일치(09:52). 교훈: 기다리는 답 단어를 질문 끝에 한 번 더 분명히 적는다.
- propose 창 2026-09-28~2026-09-28 · 등록 미룸(사용자): 아니오
- 다음 회차 대조: 이번 달 파일 9/1~어제로 덮어쓰기(propose `--since` = 2026-09-29) / 9/29 등록 12개는 9/30부터 판정 / 9/28 등록 5개는 9/29부터 / 33·17·22·9·11·7·6개 0 유지 / 솔라·아워·미미·플러스·한국·모브 추가 노출(없으면 종결) / 파워링크 노출 84회가 이어지는지 / 플레이스 순위·클릭 반대 방향 / 2위 시간대 13시 / 남양주 8위 / 10월 1일엔 9월 확정본(`지난달`, `--debug`)으로 `data/2026-09` 덮어쓰기.

## 경쟁사 판정 이력 (현행 — 10-07 갱신)
| 후보 | 판정 | 근거 | 일자 |
|---|---|---|---|
| 젠·이레·오운·스마일·와우·퍼스트필라테스 | 채택(표) | 노원·도봉구 실제 업체 | ~09-05 |
| 퍼스트필라테스아카데미노원 | 채택(표기 변형, 별도 승인 불필요) | SKILL.md 166–167행 규칙 | 09-05 |
| 노원M필라테스 (변형 M필라테스노원·노원엠필라테스·엠필라테스노원점) | **종결(자연 소멸)** — 09-09 표에서 제외, config `competitors`에서도 삭제 | 2주 연속 한 자릿수·클릭 0(09-07 CSV 4회 → 09-09 CSV 5회). 사용자 승인 09-09. 다시 후보로 올리지 말 것 | 09-09 |
| 모든날필라테스(6회) · 체인지필라테스(3회, 노원체인지·체인지필라테스노원) · 필라테스정원(2회, 노원·노원점) · 매직·모던·린·소중·H·리무브필라테스노원 등 1회짜리 | 보류(표 미등재) | 09-09 CSV 신규 등장. 전부 한 자릿수·클릭 0, 웹 검색으로 소재지 특정 불가. 11번 `(참고)`·07번 각주에만 언급. 다음 회차에 노출이 늘면 재상정, 한 자릿수 정체면 종결 | 09-09 |
| (위 후보들의 09-10 회차 판정) 모든날필라테스(6→9회) · 체인지필라테스(3회) · 필라테스정원(2회) | 보류 유지 | 09-10 CSV에서도 전부 한 자릿수·클릭 0. 노출이 늘어난 것은 모든날필라테스뿐이고 여전히 한 자릿수. 07번 각주·11번 `(참고)`에만 언급 | 09-10 |
| 매직 · 모던 · 린 · 소중 · H · 리무브필라테스노원 (각 1회) | **종결(자연 소멸)** | 2주 연속 1회·클릭 0. 리포트에서 더 언급하지 않음. 다시 후보로 올리지 말 것 | 09-10 |
| 고요필라테스(노원필라테스고요·상계필라테스고요 각 1회, 클릭 1) · 필라테스케이(노원필라테스케이·필라테스케이노원 각 1회) · 에비뉴 · 숲 · 결 · 무인 · 클래식필라테스 등 1회짜리 | 보류(표 미등재) | 09-10 CSV 신규 등장. 전부 한 자릿수, 소재지 특정 불가. 고요필라테스만 클릭 1건 있어 다음 회차에 노출이 늘면 재상정, 한 자릿수 정체면 종결 | 09-10 |
| 모든날필라테스(9회) · 체인지필라테스(노원체인지 2·체인지필라테스노원 1) | **종결(자연 소멸)** — 사용자 승인 09-11 | 3회차 연속 한 자릿수(모든날 6→9→9)·클릭 0. 리포트에서 더 언급하지 않음. 다시 후보로 올리지 말 것 | 09-11 |
| 필라테스정원(3회) · 필라테스케이(3회) · 고요필라테스(2회·클릭 1) | 보류 유지 | 09-11 CSV에서 2→3회 소폭 변동 또는 클릭 1건. 소재지 미특정. 다음 회차 한 자릿수 정체면 종결 | 09-11 |
| 노원센트럴 · 노원듀엣 · 노위 · 수정필라테스 (각 1회) | 보류(표·리포트 미언급) | 09-11 CSV 신규 1회짜리·클릭 0. 1회짜리는 리포트에 적지 않음. 2회차 연속 1회면 종결 | 09-11 |
| 모든날필라테스(9→13회) | **제외** — 09-11 "종결(자연 소멸)" 판정을 되돌림 | 09-12 CSV에서 처음 두 자릿수(9/11 하루 4회·클릭 0)라 재상정했더니 **사용자가 대구 소재 업체로 확인**. 상권 무관·확장검색 오매칭이므로 자연 소멸이 아니라 제외로 확정. 다시 후보로 올리지 말 것 | 09-12 |
| 필라테스정원(3회) · 필라테스케이(3회) · 고요필라테스(2회·클릭 1) · 체인지필라테스(3회) | 보류 유지 | 09-12 CSV에서도 한 자릿수·클릭 0(고요만 클릭 1). 소재지 미특정. 07번 각주에만 언급 | 09-12 |
| 결 · 노위 · 수정필라테스 등 1회짜리 | 보류(리포트 미언급) | 09-12 CSV에서도 1회·클릭 0. 1회짜리는 리포트에 적지 않음 | 09-12 |
| 노원M필라테스 (종결 건) | **재발 — 표 미복귀(사용자 결정)** | 09-14 CSV: 9/12 확장 노출 1회·**클릭 1건**(522원)으로 누적 5회·클릭 1. 종결 기준(한 자릿수·클릭 0)이 깨졌으나 사용자가 "그대로"로 결정. 07번 클릭 1건 목록에 두고 각주·11번 (참고)에 기록. config `competitors` 변경 없음. 클릭이 또 붙으면 재상정 | 09-14 |
| 체인지필라테스(3회) · 필라테스정원(3회) · 필라테스케이(3회) | **종결(자연 소멸)** | 09-14 CSV에서 9/12·9/13 노출 0. 3~4회차 연속 한 자릿수·클릭 0. 리포트 07번 각주에 종결 명시. 다시 후보로 올리지 말 것 | 09-14 |
| 고요필라테스(3회·클릭 1, 필라테스고요상계 9/12~13 1회 추가) | 보류 유지 | 유일하게 노출이 늘고 클릭 있음. 소재지 미특정. 다음 회차 한 자릿수 정체면 종결 | 09-14 |
| 노원센트럴 · 노원듀엣 · 노위 · 수정 · 결필라테스 (각 1회) | **종결(자연 소멸)** | 2회차 이상 1회 정체·클릭 0. 리포트 미언급 | 09-14 |
| 아르떼필라테스 · 노원오브필라테스 (각 1회) | 보류(리포트 미언급) | 09-14 CSV 신규 1회짜리·클릭 0. 2회차 연속 1회면 종결 | 09-14 |
| 모든날필라테스(13→14회) | 제외 유지 | 9/12 1회 추가. 09-12 제외 확정 그대로 | 09-14 |
| 나다운필라테스 | 제외 | 구로 신도림/인천 검단, 확장검색 오매칭 | 09-05 확정 |
| 트리니티·웰니스·퀸즈·나인·씨앤미·벨·수현·예일필라테스 | 제외 | 한 자릿수 노출, 상권 무관 | 09-06 |
| 에반더필라테스상계역점 · RHA필라테스상계·상계동 | 종결(자연 소멸) | 2주 연속 한 자릿수·클릭 0. 다시 묻지 않음 | 09-06 |
| 체인지필라테스 · 필라테스정원 · 필라테스케이 (종결 건) | **종결 유지 — 재등장에도 되돌리지 않음** | 09-15 CSV에서 각각 9/14 확장검색 1회 재등장(클릭 0). 09-14 종결 판정대로 추적하지 않음. 1회짜리 재등장은 재상정 사유가 아니다 | 09-15 |
| 오프닝필라테스(검색어 "노원오프닝필라테스" 4회 — 9/13 1·9/14 3) | **채택(표)** — 사용자 확인 09-15 | 노원 소재 업체로 확인. 클릭 0·비용 0원. config `competitors`에 "오프닝필라테스" 추가, 07번 표·각주·11번 (참고) 갱신. 12번 액션은 클릭·비용 0이라 올리지 않음 | 09-15 |
| 필라테스인(검색어 "필라테스인노원" 12 · "노원필라테스인" 4 = 16회) | **채택(표)** — 사용자 확인 09-15 | 노원 소재 업체로 확인. 클릭 0·비용 0원. config `competitors`에 "필라테스인" 추가. 그동안 07번 클릭 0 목록에 일반 검색어로 있던 것을 경쟁사 표로 옮김(목록 44 → 43개). 마지막 노출 9/13 | 09-15 |
| 노원M필라테스 | 표 미복귀 유지 | 09-15 CSV에서 9/14 추가 노출 0, 누적 5회·클릭 1 그대로. 09-14 사용자 결정 유지 | 09-15 |
| 고요필라테스(3회·클릭 1) | 보류 유지 | 9/14 추가 노출 0. 소재지 미특정. 다음 회차에도 정체면 종결 | 09-15 |
| 모든날필라테스(14회) | 제외 유지 | 9/14 추가 노출 0. 대구 소재, 09-12 제외 확정 그대로 | 09-15 |
| 아르떼필라테스 · 노원오브필라테스 (각 1회) | **종결(자연 소멸)** | 2회차 연속 1회·클릭 0. 리포트 미언급 | 09-15 |
| 고요필라테스(3회·클릭 1) | **종결(자연 소멸)** | 09-15·09-16 두 회차 연속 추가 노출 0(9/14·9/15). 09-14부터 "다음 회차에도 정체면 종결"로 걸어둔 조건 충족. 리포트 07번 각주·11번 (참고)에 종결 명시. 노출이 다시 늘면 재상정 | 09-16 |
| 그릿필라테스(1회, 일치, 9/15 첫 등장) | 보류(리포트 미언급) | 1회짜리·클릭 0. 웹 검색으로 소재지 특정 불가. 2회차 연속 1회면 종결 | 09-16 |
| 트리니티필라테스(누적 5회, 9/15 1회) | 제외 유지 | 09-06 제외 판정 이름이 누적 5회에 닿아 07번 "클릭 0·노출 5회 이상" 목록에 올라옴(나다운·모든날과 같은 처리). 표에는 넣지 않음 | 09-16 |
| 필라테스정원("노원역필라테스정원" 9/15 1회) | 종결 유지 | 09-14 종결 건의 1회 재등장. 재상정 사유 아님 | 09-16 |
| 그릿필라테스(1회, 9/15) | **종결(자연 소멸)** | 09-17 CSV에서 9/16 추가 노출 0 → 2회차 연속 1회·클릭 0. 리포트 미언급. 다시 후보로 올리지 말 것 | 09-17 |
| 보니따필라테스(검색어 "보니따필라테스노원상계" 확장 1회, 9/16 첫 등장) | 보류(리포트 미언급) | 1회짜리·클릭 0. 웹 검색으로 소재지 특정 불가. 2회차 연속 1회면 종결 | 09-17 |
| 모던필라테스노원 (09-10 1회짜리 종결 건) | 종결 유지 | 9/16 1회 재등장(누적 2회·클릭 0). 1회짜리 재등장은 재상정 사유 아님. 07번 각주에 한 줄 기록 | 09-17 |
| 모든날필라테스(14 → 17회) | 제외 유지 | 9/16 3회 추가·클릭 0. 대구 소재, 09-12 제외 확정 그대로 | 09-17 |
| 노원M필라테스 | 표 미복귀 유지 | 9/16 추가 노출 0, 누적 5회·클릭 1 그대로 | 09-17 |
| 젠(59)·오운(12)·필라테스인노원(13) 등 표 등재 경쟁사 | 채택 유지 | 9/16 노출 오운 4·젠 1·필라테스인노원 1, 전부 클릭 0. config 변경 없음 | 09-17 |
| 노원필라테스숲(누적 4회 — 8/27 1·9/17 3) | 보류(표 미등재) | 09-10 1회짜리 보류 건이 9/17 3회 재등장. 클릭 0, 웹 검색으로 소재지 특정 불가. 07번 각주·11번 (참고)에만 언급. 다음 회차 한 자릿수 정체면 종결 | 09-19 |
| 보니따필라테스(1회, 9/16) | **종결(자연 소멸)** | 09-19 CSV에서 9/17·9/18 추가 노출 0 → 2회차 연속 1회·클릭 0. 리포트 미언급. 다시 후보로 올리지 말 것 | 09-19 |
| 필라테스정원(9/17 2·9/18 1, 누적 7) · 필라테스케이노원(9/17 1) · 필라테스고요상계(9/17 1) · 에반더필라테스노원(9/18 1) · 매직필라테스노원(9/18 1) | 종결 유지 | 종결 건의 재등장. 전부 클릭 0·한 자릿수. 07번 각주에 한 줄. 재상정 사유 아님 | 09-19 |
| 토브필라테스 · 노원이나핏필라테스 · 아이필라테스(9/17 각 1회) · 유진필라테스 · 보람상가필라테스(9/18 각 1회) | 보류(리포트 미언급) | 신규 1회짜리·클릭 0. 보람상가는 랜드마크 조합. 2회차 연속 1회면 종결 | 09-19 |
| 노해로필라테스(2) · 노해로노원필라테스(1) (9/18) | **경쟁사 아님 — 자사 주소 도로명** | 매장 주소가 노원구 노해로 492라 우리 상호를 찾는 검색으로 판정. 07번 각주·11번 (참고)에 기록. 후보로 올리지 말 것 | 09-19 |
| 노원M필라테스 | 표 미복귀 유지 | 변형 "노원엠필라테스" 9/18 1회·클릭 0(변형 누적 2). 본명 누적 5회·클릭 1 그대로. 09-14 사용자 결정 유지 | 09-19 |
| 벨필라테스(9/17 1회, 누적 2) | 제외 유지 | 09-06 제외 판정 그대로. 07번 각주에 한 줄 | 09-19 |
| 모든날필라테스(17회) | 제외 유지 | 9/17·9/18 추가 노출 0. 대구 소재, 09-12 제외 확정 그대로 | 09-19 |
| 젠(66)·필라테스인노원(15)·와우(12)·이레(7)·스마일(6) 등 표 등재 경쟁사 | 채택 유지 | 이틀 노출 젠 7·필라테스인노원 2·와우 2·이레 1·스마일 1, 전부 클릭 0. config 변경 없음 | 09-19 |
| 노원필라테스숲(누적 4회 — 8/27 1·9/17 3) | **종결(자연 소멸)** | 09-20 CSV에서 9/18·9/19 추가 노출 0 → 한 자릿수 정체·클릭 0. 09-19 걸어둔 조건 충족. 리포트 07번 각주·11번 (참고)에 종결 명시. 다시 후보로 올리지 말 것 | 09-20 |
| 토브필라테스 · 노원이나핏필라테스 · 아이필라테스(9/17 각 1회) · 보람상가필라테스(9/18 1회) | **종결(자연 소멸)** | 09-20 CSV에서 추가 노출 0 → 2회차 연속 1회·클릭 0. 리포트 미언급. 다시 후보로 올리지 말 것 | 09-20 |
| 유진필라테스(9/18 1·9/19 1, 누적 2) | 보류 유지(리포트 미언급) | 1회 더 잡혀 종결 조건(2회차 연속 1회 정체) 미충족. 웹 검색으로 소재지 특정 불가. 다음 회차 추가 없으면 종결 | 09-20 |
| INTOPILATES(9/19 확장 1회) · 필라테스안(노원필라테스안 9/10 1·필라테스안노원 9/19 1) | 보류(리포트 미언급) | 신규 브랜드형 1회씩·클릭 0. 웹 검색으로 소재지 특정 불가. 2회차 연속 추가 없으면 종결 | 09-20 |
| 체인지필라테스노원 · 필라테스정원노원(9/19 각 1회) | 종결 유지 | 종결 건의 재등장, 클릭 0. 07번 각주에 한 줄. 재상정 사유 아님 | 09-20 |
| 벨필라테스(9/19 1회, 누적 3) | 제외 유지 | 09-06 제외 판정 그대로. 07번 각주에 한 줄 | 09-20 |
| 맨즈필라테스(9/19 일치 1회) | 경쟁사 후보 아님 | "맨즈필라테스노원"이 클릭 1건 목록에 일반 검색어로 있어 같은 처리(남성 대상 수업 검색으로 봄) | 09-20 |
| 와우(12 → 13) 외 표 등재 경쟁사 · 노원M(변형 포함) · 모든날(17) · 노해로 계열 | 채택·표 미복귀·제외·경쟁사 아님 각각 유지 | 9/19 경쟁사명 노출은 와우 1회·클릭 0뿐. 나머지 추가 노출 없음. config 변경 없음 | 09-20 |
| 노원구노원부티필라테스(9/20 확장 3회) | **채택(표)** — 사장님 확인 09-21 | 웹 검색 특정 불가였으나 사장님이 "매장 근처 필라테스"로 확인. 클릭 0·비용 0원. config `competitors`에 "부티필라테스" 추가(8 → 9개), 07번 표 11행·각주·11번 (참고)·12번 각주 갱신(재배포 `acac2d3`). 12번 액션은 클릭·비용 0이라 올리지 않음 | 09-21 |
| 노원니드필라테스 · 필라테스호(9/20 각 1회) | 보류(리포트 미언급) | 신규 1회짜리·클릭 0. 웹 검색 특정 불가. 2회차 연속 1회면 종결 | 09-21 |
| 유진필라테스(누적 2회) | **종결(자연 소멸)** | 09-21 CSV에서 9/20 추가 노출 0 → 09-20 걸어둔 조건 충족. 리포트 07번 각주에 종결 명시. 다시 후보로 올리지 말 것 | 09-21 |
| INTOPILATES(9/19 1·9/20 1, 누적 2) | 보류 유지(리포트 07번 각주·11번 (참고) 언급) | 1회 더 잡혀 종결 조건 미충족. 소재지 특정 불가. 다음 회차 추가 없으면 종결 | 09-21 |
| 필라테스안(누적 2, 9/20 0) | 보류 유지(리포트 미언급) | 9/20 추가 0(1회차째). 2회차 연속 0이면 종결 | 09-21 |
| 와우(13 → 15)·오운(12 → 13) 외 표 등재 경쟁사 · 노원M(변형 포함) · 모든날(17) · 노해로 계열 · 벨(3) · 체인지·정원 계열 | 채택·표 미복귀·제외·경쟁사 아님·종결 각각 유지 | 9/20 경쟁사명 노출은 와우 2·오운 1(클릭 0)뿐. 나머지 추가 노출 없음. config 변경 없음 | 09-21 |
| 필라테스노원와우점(9/21 확장 1) · 노원와우필라테스비추첰(9/22 확장 1) | 채택(와우필라테스 표기 변형, 별도 승인 불필요) | SKILL.md 표기 변형 규칙. 07번 표 13행. 후자는 비추천 후기 검색으로 보이나 브랜드명 검색이라 그대로 | 09-23 |
| 젠필라테스(66 → 72·클릭 1 → 2) · 와우필라테스(15 → 19·클릭 1 → 2) · 노원필라테스인(4 → 7) · 필라테스인노원(16) · 오운(14) | 채택 유지 | 9/22 젠·와우 클릭 1건씩(3,519원) — 하루 경쟁사명 클릭 2건은 개업 이후 처음. 11번 (참고)·12번 각주 기록. config 변경 없음 | 09-23 |
| INTOPILATES(누적 2) · 필라테스안(누적 2) · 노원니드필라테스(1) · 필라테스호(1) | **종결(자연 소멸)** | 09-23 CSV에서 9/21·9/22 추가 노출 0 → 걸어둔 조건 충족. 07번 각주에 종결 명시. 다시 후보로 올리지 말 것 | 09-23 |
| 필라테스정원 계열(노원정원필라테스 3·노원구필라테스정원·필라테스정원노원·필라테스정원노원점가격·노원필라테스정원 각 1 — 9/21·9/22 7회, 변형 8개 누적 16회·클릭 0) | **종결 건 재등장 — 채팅 확인 요청(표 미등재)** | 09-14 종결 뒤 1회짜리 재등장은 무시해 왔으나 이틀 7회는 그 범위를 넘음. 웹 검색(필라테스정원 노원) 소재지 특정 불가. 사장님이 노원 업체로 확인하면 채택(config 추가), 아니면 제외로 확정해 다시 묻지 않음 | 09-23 |
| 라임필라테스(9/22 일치 2회·클릭 0) | 보류(리포트 미언급) | 신규 브랜드형. 소재지 미확인. 2회차 연속 추가 없으면 종결 | 09-23 |
| 글램 · 노원라일락 · 요요(노원동) · 아트(노원) · 바비 · 달 · 노원VIP필라테스 · 필라테스아름다운상계점 · 필라테스혜윰오픈 · 와우스포츠 (각 1회) | 보류(리포트 미언급) | 09-23 CSV 신규 1회짜리·클릭 0. 2회차 연속 1회면 종결 | 09-23 |
| 상계동고요필라테스(9/21 1) · 재활엠필라테스노원(9/22 1) · 노원M필라테스(9/21 확장 1, 누적 6·클릭 1) | 종결 유지 · 표 미복귀 유지 | 종결 건·노원M 변형의 1회 재등장. 07번 각주 한 줄. 재상정 사유 아님 | 09-23 |
| 모든날(17) · 나다운(57) · 트리니티(5) · 벨(3) · 노해로 계열 · 체인지·케이·숲 계열 | 제외·종결 각각 유지 | 9/21·9/22 추가 노출 없음 | 09-23 |
| 필라테스인노원내돈내산(9/23 확장 1) | 채택(필라테스인 표기 변형, 별도 승인 불필요) | SKILL.md 표기 변형 규칙. 07번 표 14행. 이용 후기 검색으로 보이나 브랜드명 검색이라 그대로 | 09-24 |
| 와우(19 → 24) · 필라테스인노원(16 → 18) · 젠(72 → 73) · 오운(14 → 15) | 채택 유지 | 9/23 경쟁사명 클릭 0. config 변경 없음 | 09-24 |
| 필라테스정원 계열(누적 16) | 채팅 확인 대기 유지(표 미등재) | 9/23 추가 노출 0. 사장님 답 오면 채택(config 추가) 또는 제외 확정 | 09-24 |
| 라임필라테스(누적 2) · 글램·노원라일락·요요·아트·바비·달·노원VIP·필라테스아름다운상계점·필라테스혜윰오픈·와우스포츠(각 1) | 보류 유지(리포트 미언급) | 9/23 추가 노출 0(1회차째). 다음 회차에도 추가 없으면 종결 | 09-24 |
| 필라테스고요노원(9/23 확장 2, 고요 계열 누적 7) · 노원역필라테스안·노원필라테스안(9/23 각 1, 필라테스안 계열 누적 4) | 종결 유지 | 종결 건 재등장, 전부 클릭 0. 07번 각주 한 줄. 재상정 사유 아님 | 09-24 |
| 노원M(6·클릭 1) · 모든날(17) · 나다운(57) · 트리니티(5) · 노해로 계열 | 표 미복귀·제외·종결·경쟁사 아님 각각 유지 | 9/23 추가 노출 없음 | 09-24 |
| 필라테스정원(변형 8개 — 노원필라테스정원 4·필라테스정원노원 4·노원정원필라테스 3·나머지 5개 각 1, 누적 16·클릭 0) | **채택(표)** — 사용자 확인 09-24 "노원에 있어" | 09-14 종결 → 09-23 재등장·확인 요청 → 채택. config `competitors`에 "필라테스정원" 추가(9 → 10개), 07번 표 8행·각주·11번 (참고)·12번 각주 갱신(재배포 `8b738d7`). 클릭·비용 0이라 12번 액션 아님 | 09-24 |
| 노원필라테스정원내돈내산(9/24 확장 1) | 채택(필라테스정원 표기 변형, 별도 승인 불필요) | 07번 표 23행. 정원 변형 9개·누적 18 | 09-25 |
| 노원필라테스힐링정원내돈내산(9/24 확장 1) | **채택(필라테스정원 검색)** — 사용자 확인 09-25 "찾는 검색이 맞아" | 처음엔 정원 변형인지 불분명해 보류·확인 요청. 07번 표 24행(정원 변형 10개·누적 19). config 변경 없음 | 09-25 |
| 노원엠코필라테스(9/24 확장 1) | 보류(리포트 미언급) | 신규 1회짜리·클릭 0. 2회차 연속 추가 없으면 종결 | 09-25 |
| 라임필라테스(누적 2) · 글램·노원라일락·요요·바비·달·노원VIP·필라테스아름다운상계점·필라테스혜윰오픈·와우스포츠(각 1) | **종결(자연 소멸)** | 9/23·9/24 두 회차 연속 추가 노출 0. 라임만 07번 각주·11번 (참고)에 종결 명시. 다시 후보로 올리지 말 것 | 09-25 |
| 아트필라테스노원(9/24 확장 1, 아트 계열 누적 2) | 보류 유지(리포트 미언급) | 09-23 1회짜리가 재등장. 다음 회차 추가 없으면 종결 | 09-25 |
| 필라테스안노원(9/24 확장 1, 필라테스안 계열 누적 5) | 종결 유지 | 종결 건 재등장, 클릭 0. 07번 각주 한 줄 | 09-25 |
| 젠(73 → 75) · 오운(15 → 16) · 노원오프닝(4 → 5) · 노원필라테스정원(4 → 5) | 채택 유지 | 9/24 경쟁사명 클릭 0. config 변경 없음 | 09-25 |
| 필라테스정원노원산전필라테스(9/25 확장 1) | 채택(필라테스정원 표기 변형, 별도 승인 불필요) | 07번 표 25행. 정원 변형 11개·누적 21 | 09-26 |
| 필라테스안 계열(노원필라테스안 9/25 2 · 필라테스안노원역 9/25 1 신규 — 9/23~9/25 사흘 6회, 누적 8·클릭 0) | **제외 확정** — 사용자 확인 09-26 "노원에 없어" | 1회짜리 재등장 범위를 넘어 확인 요청 → 노원 업체 아님. config 변경 없음(채택 아님). 07번 각주·11번 (참고)·12번 각주에 기록(재배포 `ad48222`). **다시 후보로 올리지 말 것** | 09-26 |
| 아트필라테스노원 · 노원엠코필라테스 | 보류 유지(리포트 미언급) | 9/25 추가 노출 0(1회차째). 다음 회차에도 없으면 종결 | 09-26 |
| 젠(75 → 77) · 노원필라테스정원(5 → 6) | 채택 유지 | 9/25 경쟁사명 클릭 0. config 변경 없음 | 09-26 |
| 아트필라테스노원 · 노원엠코필라테스 | **종결(자연 소멸)** | 9/25·9/26 두 회차 연속 추가 노출 0 → 09-26 걸어둔 조건 충족. 07번 각주·11번 (참고)·12번 각주에 종결 명시. 다시 후보로 올리지 말 것 | 09-27 |
| 노원솔라필라테스(9/26 확장 1) · 이루다필라테스산전(9/26 확장 1) | 보류(표 미등재 — 07 각주에 1회짜리로만 언급) | 신규 브랜드형 1회씩·클릭 0. 웹 검색: 솔라 특정 불가, 이루다는 예약 앱만 확인되고 지점·소재지 불명. 2회차 연속 추가 없으면 종결 | 09-27 |
| 필라테스안 계열(제외 확정 건) · 노원M(6·클릭 1) · 모든날(17) · 나다운(57) · 트리니티(5) · 벨(3) · 노해로 계열 | 제외·표 미복귀·종결·경쟁사 아님 각각 유지 | 9/26 추가 노출 없음 | 09-27 |
| 젠(77 → 82, 9/26 일치 5) · 노원역필라테스정원(1 → 2) | 채택 유지 | 9/26 경쟁사명 클릭 0. config 변경 없음. 정원 변형 11개·누적 22 | 09-27 |
| 퍼스트필라테스노원점(9/27 확장 1) | 채택(퍼스트필라테스 표기 변형, 별도 승인 불필요) | compute `신규변형후보`. 07번 표 26행(소재구 노원구·확장). 클릭 0 | 09-28 |
| 젠(82 → 83) · 와우(24 → 26) · 이레(7 → 8) · 퍼스트필라테스(1 → 2) | 채택 유지 | 9/27 경쟁사명 클릭 0. config 변경 없음. 정원 변형 11개·누적 22 그대로 | 09-28 |
| 노원솔라필라테스 · 이루다필라테스산전 | 보류 유지(07 각주에만) | 9/27 추가 노출 0(1회차째). 09-27 조건대로 다음 회차에도 없으면 종결 | 09-28 |
| 모브필라테스(9/27 일치 1) | 보류(표 미등재 — 07 각주에 1회짜리로만 언급) | 신규 브랜드형 1회·클릭 0. 웹 검색 특정 불가. 2회차 연속 추가 없으면 종결 | 09-28 |
| 에반더필라테스상계역(9/27 확장 1) | **종결 유지** — 09-06 종결 건(에반더필라테스상계역점·09-19 에반더필라테스노원 재등장 종결 유지)의 재등장 | 클릭 0. 1차 배포(`0272498`)에 신규 후보로 잘못 적어 문구 4곳 정정 재배포(`e1df211`). 재상정 사유 아님 | 09-28 |
| 필라테스안 계열(제외 확정 건) · 노원M(6·클릭 1) · 모든날(17) · 나다운(57) · 트리니티(5) · 벨(3) · 노해로 계열 · 아트·엠코(종결) | 제외·표 미복귀·종결·경쟁사 아님 각각 유지 | 9/27 추가 노출 없음 | 09-28 |
| 이루다필라테스산전 | **종결(자연 소멸)** | 9/27·9/28 두 회차 연속 추가 노출 0 → 09-27 조건 충족. 작업본 07 각주·11번 (참고)·12번 각주에 종결 명시(배포는 미실행). 다시 후보로 올리지 말 것 | 09-29 |
| 솔라필라테스(노원솔라필라테스 9/26 1 · **솔라필라테스상계주차 9/28 확장 2**, 누적 3·클릭 0) | 보류 유지(표 미등재) | 1회짜리 보류 건의 재등장. 웹 검색("솔라필라테스 상계") 소재지 특정 불가. 승인 묶음 (2)로 채팅에 물었으나 답 없음 → 보류. "솔라필라테스상계주차"는 사용자가 업종어 1번으로 골라 **제외 검색어에 등록**(2026-09-29). 다음 회차 추가 노출 없으면 종결 | 09-29 |
| 아워필라테스(9/28 일치 3) · 미미·플러스·한국필라테스(9/28 일치 각 1) | 보류(표 미등재 — 07 각주에만) | 신규 브랜드형·클릭 0. 아워는 웹 검색("아워필라테스 노원") 특정 불가, 승인 묶음 (2)로 물었으나 답 없음. 2회차 연속 추가 없으면 종결 | 09-29 |
| 모브필라테스(9/27 일치 1) | 보류 유지 | 9/28 추가 노출 0(1회차째). 다음 회차에도 없으면 종결 | 09-29 |
| 젠(83 → 88) · 이레(8 → 10) · 와우(26 → 27) · 오운(16 → 17) · 노원필라테스정원(6 → 9, 정원 계열 누적 25) | 채택 유지 | 9/28 경쟁사명 클릭 0. config 변경 없음. 26행 그대로 | 09-29 |
| 필라테스안 계열(노원필라테스안 9/28 2, 누적 10) · 노원M(본명 6·클릭 1, 변형 노원엠 9/28 2 → 4) · 퀸즈(9/28 2, 누적 6 — 09-06 제외) · 고요 계열(필라테스고요상계 9/28 1) · 모든날(17) · 나다운(57) · 트리니티(5) · 벨(3) · 노해로 계열 | 제외·표 미복귀·제외·종결·경쟁사 아님 각각 유지 | 전부 클릭 0. 재상정 사유 아님 | 09-29 |
| 필라테스시소(노원필라테스시소 9/29 확장 2·클릭 0) | **채택(표)** — config `competitors`에 "필라테스시소" 추가(`8ea8c14`) | 웹 검색: 인스타그램 "노원필라테스시소"(필라테스·자이로토닉) — 노원구로 보임. 승인 묶음 (1) → **사용자 확인 "경쟁사 업체야"**. 07 표 행 추가(노원구·확장) | 09-30 |
| 솔라필라테스(노원솔라필라테스 9/26·9/29 각 1 · 솔라필라테스상계주차 9/28 2 — 누적 4·클릭 0) | **채택(표)** — config `competitors`에 "솔라필라테스" 추가(`8ea8c14`) | 보류 건 → **사용자 확인 "노원 업체야"**. 07 표 2행 추가(노원구·확장). "솔라필라테스상계주차"는 채택 전 09-29 제외 검색어로 등록돼 있음 — 그대로 둠(사용자에게 알림) | 09-30 |
| 노원필라테스블루창동점(9/29 확장 2·클릭 0) | **표 미등재 — 제외 검색어로 등록**(2026-09-30, 업종어 1번) | 창동(도봉구)으로 보이나 웹 검색 특정 불가. 사용자 "창동에 있긴한데 제외시켜줘" → 두 해석 되물음 → "B"(제외 검색어 등록). 다시 후보로 올리지 말 것 | 09-30 |
| 모브필라테스 | **종결(자연 소멸)** | 9/28·9/29 두 회차 연속 추가 노출 0 → 09-28 조건 충족. 다시 후보로 올리지 말 것 | 09-30 |
| 아워필라테스 · 미미·플러스·한국필라테스 | 보류 유지(07 각주에만) | 9/29 추가 노출 0(1회차째). 다음 회차에도 없으면 종결 | 09-30 |
| H·아름다운·체인지·에반더 계열(9/29 노원H필라테스·노원아름다운필라테스·노원체인지필라테스·에반더필라테스상계역점 각 1) | 종결 유지 | 종결 건의 재등장, 클릭 0. 재상정 사유 아님 | 09-30 |
| 젠(88 → 91) · 와우(27 → 28) · 오운(17 → 18) · 노원필라테스정원(9 → 13, 정원 계열 29) · 노원필라테스인(7 → 11) · 필라테스인노원(18 → 19) | 채택 유지 | 9/29 경쟁사명 클릭 0. 표 29행 | 09-30 |
| 써니필라테스(노원써니필라테스 9/30 확장 1·**클릭 1건 338원**) | **채택(표)** — config `competitors`에 "써니필라테스" 추가(`7c02571`) | 웹 검색 특정 불가 → 승인 묶음 (2) → **사용자 확인 "노원 맞음"**. 07 표 행 추가(노원구·확장) | 10-01 |
| 노원역부티필라테스(9/30 확장 1) | 채택(부티필라테스 표기 변형, 별도 승인 불필요) | compute `신규변형후보`. 07 표 행 추가(노원구·확장). 클릭 0 | 10-01 |
| 플로우필라테스(9/30 일치 4) · 비비필라테스(9/30 일치 3) | **제외 확정** — 사용자 확인 10-01 "노원 아님" | 신규 브랜드형·클릭 0. 웹 검색 특정 불가(비비는 부산 명지점만). 표 미등재·07 각주에 기록. **다시 후보로 올리지 말 것** | 10-01 |
| 노원헤븐필라테스 · 클립뷰필라테스(9/30 확장 각 1) | 보류(표 미등재 — 07 각주에만) | 신규 1회짜리·클릭 0, 웹 검색 특정 불가. 2회차 연속 추가 없으면 종결 | 10-01 |
| 아워필라테스 · 미미·플러스·한국필라테스 | **종결(자연 소멸)** | 9/29·9/30 두 회차 연속 추가 노출 0 → 09-29 조건 충족. 다시 후보로 올리지 말 것 | 10-01 |
| 라임(9/30 일치 2, 누적 4) · 보니따(노원상계점 1) · H(H필라테스노원 1) · 에반더(상계역점 1) · 노원M 변형(M필라테스노원역·노원M필라테스내돈내산후기 각 1) | 종결 유지 · 표 미복귀 유지 | 종결 건의 재등장, 전부 클릭 0. 재상정 사유 아님 | 10-01 |
| 벨필라테스(9/30 일치 4·**클릭 1건 1,560원**, 누적 7) | 제외 유지(09-06 판정) | 첫 클릭으로 클릭1건 목록에 들어감. 07 각주에 한 줄. 재상정 사유 아님(클릭 1건) | 10-01 |
| 노원역정원필라테스(9/30 확장 1) | 필라테스정원 어순 변형 — **표 미등재(도구 제약)** | config 이름 미포함·직전 표에 없어 compute 집합 밖 → 표에 넣으면 compare 차이. 07 각주에 언급, 이월 | 10-01 |
| 니드필라테스(노원니드필라테스 9/20 1 · 니드필라테스노원) | **채택(표)** — config `competitors`에 "니드필라테스" 추가(`02a2b64`, 사용자 확인 2026-10-04 "경쟁사") | 10/4 세션 결정(기록 없음 — 커밋 메시지로 복원). 09-23 종결한 "노원니드필라테스"도 표에 들어감. 07 표 2행(노원구·확장, 10/5 배포에서 반영) | 10-04 |
| 보람상가필라테스(10/3 일치 5, 누적 8·클릭 0) · 상계보람필라테스(10/3 확장 1) | **제외 확정** — 사용자 확인 10-05 "아님" | 09-20 종결(1회짜리) 뒤 하루 5회로 재등장 → 승인 묶음 (2). 웹 검색 특정 불가. 표 미등재·07 각주에 기록. **다시 후보로 올리지 말 것** | 10-05 |
| 부티 변형 4(노원상계동부티 5·노원구노해로부티 3·노원노원구부티·노원상계부티 각 1) · 노원구솔라필라테스 · 와우필라테스노원점(각 1) | 채택(표기 변형, 별도 승인 불필요) | compute `신규변형후보`. 07 표 31 → 39행(니드 2 포함, 전부 노원구·확장). 클릭 0 | 10-05 |
| 노원헤븐필라테스 · 클립뷰필라테스 | **종결(자연 소멸)** | 10/1~10/4 추가 노출 0. 다시 후보로 올리지 말 것 | 10-05 |
| 포미필라테스 · 포레필라테스(10/1 일치 각 1) | 보류(리포트 미언급) | 신규 1회짜리·클릭 0. 2회차 연속 추가 없으면 종결 | 10-05 |
| 노원필라테스힐링정원(10/2 확장 1) · 노원역정원필라테스(10/1~10/4 0) | 필라테스정원 어순 변형 — 표 미등재(도구 제약) 유지 | compute 집합 밖. 07 각주에 언급 | 10-05 |
| 라임(4) · 에반더(상계역점 3·상계점 1) · 필라테스안(7, 누적 17) · 플로우·비비(각 1) · 퀸즈(3, 누적 9) · 벨(2, 누적 9) · 노해로 계열(4) | 종결·제외·경쟁사 아님 각각 유지 | 10/1~10/4 재등장, 전부 클릭 0 | 10-05 |
| 토브필라테스(9/17 1 → 10/5 일치 2·클릭 1건 1,392원, 누적 4·1) | **경쟁사 아님** — 사용자 확인 10-06 "아님" | 09-20 종결(1회짜리) 뒤 재등장·첫 클릭. 웹 검색 소재 특정 불가 → 승인 묶음 (2). 07 클릭1건 목록에 둠 · 다시 후보로 올리지 말 것 | 10-06 |
| 노원부티필라테스(10/5 확장 9) | 채택(표 행 추가) — 부티 표기 변형 | compute `신규변형후보`. 07 표 39 → 40행 | 10-06 |
| 포인트필라테스(10/5 2) · 아라필라테스 · 피오르필라테스(10/5 각 1) | 보류(리포트 07 각주·11 (참고)에만) | 신규 1~2회·클릭 0. 2회차 연속 추가 없으면 종결 | 10-06 |
| 포미필라테스 · 포레필라테스 | 보류 유지 | 10/5 추가 0(1회차). 다음 회차도 0이면 종결 | 10-06 |
| 노원노부티필라테스(10/6 확장 1) | 채택(표 행 추가) — 부티 표기 변형 | compute `신규변형후보`. 07 표 40 → 41행 | 10-07 |
| 인투필라테스노원 1 · 필라테스하는날(노원필라테스하는날 2 · 필라테스하는날노원 1) · 필라테스천국의계단 2 · 필라테스듀엣룸 1(10/6 확장) | 보류(07 ①·11 (참고)에만) — 승인 묶음 (2), 사용자 답 "보류" | 신규·클릭 0, 웹 검색 소재 확인불가(듀엣룸은 방 이름일 수 있음). 2회차 연속 추가 없으면 종결 | 10-07 |
| 포미필라테스 · 포레필라테스 | **종결(자연 소멸)** | 10/5·10/6 두 회차 연속 추가 0. 다시 후보로 올리지 말 것 | 10-07 |
| 포인트필라테스 · 아라필라테스 · 피오르필라테스 | 보류 유지 | 10/6 추가 0(1회차). 다음 회차도 0이면 종결 | 10-07 |
| 젠(113 → 119) · 오운(29 → 30) · 부티 계열(+12) · 정원 계열(표 안 36 → 38) · 필라테스인(+1) · 와우노원점(+1) | 채택 유지 | 10/5 경쟁사명 23회·클릭 0. 표 40행 | 10-06 |
| 젠(104 → 113) · 오운(20 → 29) · 와우(28 → 34) · 이레(13 → 16) · 정원 계열(표 안 32 → 36) | 채택 유지 | 창 경쟁사명 54회·클릭 0. 표 39행 | 10-05 |
| 젠(91 → 104) · 이레(10 → 13) · 오운(18 → 20) · 스마일(6 → 7) · 퍼스트(2 → 3) · 정원 계열(표 안 29 → 32) | 채택 유지 | 9/30 경쟁사명 클릭은 써니 1건뿐. 표 31행 | 10-01 |

## 보관 파일(2026-10-07 — 검토 비용 줄이기 작업 2: 기록 보관 분리) · 이 절은 맨 끝에 둔다(새 회차 절은 종전대로 맨 위)
지난 회차 절을 `audit/archive/last-audit_~2026-10-05.md` 로 **글자 그대로** 옮겼다 — 그 파일은 아래 옛 행 구간을 순서대로 이은 것(머리말 · 구분 줄 추가 없음). 옛 파일 = `f2aec20` 의 이 파일 4256행 · md5 8b6b3ef6. 이 파일에 남긴 것: 2026-10-06 이후 회차 전부 · 본보기 절(2026-09-30 수정·병합 · 2026-09-29 후속 두 절 · "기능 추가 탐색 기준선(Code 탭 전 단계 실행, 2026-09-28)") · 운영 표("# 이전 기록" 머리 줄 · 개선안 · 등록 제외 검색어 대조 목록 · 경쟁사 판정 이력) · 최신 점검 기준선(2026-09-26 진단 — 개선안 · 효율 개선안 · 점검표 개정안 · 다음 점검에서 대조할 것) · 2026-09-27~10-05 회차의 이월 · 다음에 볼 것 · 첫 실사용에서 볼 것이 든 절(과 그 절이 "상세 = 아래 …" 로 가리키는 갱신 회차 상세 절). 남긴 절 안에서 옮긴 절을 가리키는 말(예 "수정 기록 3 W8" · "탐색 기준선 6-6")은 원문 그대로 두었다 — 아래 목록으로 보관 파일에서 찾는다. 따옴표로 "아래 … 절"이라 한 곳 중 옮긴 절을 가리키는 것은 하나: "기능 추가 탐색 기준선(Code 탭 전 단계 실행, 2026-09-28)" 머리의 "기능 추가 탐색 기준선(보고서 자동 수집)" 절 끝 사용자 결정(2026-09-28 저녁) 블록 → 보관 파일 1028행.
옮긴 구간(옛 행 → 보관 파일 행 · md5 앞 8자리 · 제목):
- 옛 1016–1724 → 보관 1–709 · a1c290be · # 수정 기록 4 · 3 · 2(Code 탭 회차 1, 2026-09-28) · # 기능 추가 구현 기록(Code 탭 전 단계 실행 — 설계안 C 회차 1, 2026-09-28)
- 옛 1958–2049 → 보관 710–801 · fc96ffb4 · "# 기능 추가 구현 기준선(보고서 자동 수집 C, 2026-09-28)" 안의 ## 수정 기록 2 ~ ## 원래 제안·지시를 바꾼 곳(머리 · 검증·병합 기록 · 다음에 볼 것은 남김)
- 옛 2054–2668 → 보관 802–1416 · c94302c7 · 같은 구현 기준선의 ## 마무리 기록 · # 기능 추가 탐색 기준선(보고서 자동 수집, 2026-09-28) 전부 · # 기능 추가 탐색 기준선(제외 검색어 등록 자동화, 2026-09-27) 0~5절·사용자 확인 요청·마무리 기록·내가 고를 항목·## 구현 기록(2026-09-27, 수정 기록 2 포함)(검증·병합 기록 · 첫 실사용 기록은 남김)
- 옛 3018–3141 → 보관 1417–1540 · 03f7a8a7 · 2026-09-07 저녁 # 점검 기준선 본문(이번 회차 조치 · 기록 문구 정정 09-09 · 직전 기준선 판정 · 결함 · 실측 요약 · 라이브 Pages 확인 — 그 위 "# 이전 기록" 머리 줄과 개선안 표 이하 운영 표는 남김)
- 옛 3310–3678 → 보관 1541–1909 · e531ac7b · ## 2026-09-28 ~ 2026-09-12 갱신 회차(진단 아님) 14개 — 대조 목록 표 아래 상세 기록
- 옛 3816–4256 → 보관 1910–2350 · 704b0c27 · 2026-09-07 저녁 기준선의 ## 점검표 개정안 · 점검표 갱신 이력 · 갱신 회차 기록(09-09~09-11) · 스킬 문서 변경(09-10 3차) · 계정 조치 기록(09-10) · 다음 점검에서 대조할 것 · [수정 회차에 적용할 것] · # 이전 기록(2026-09-07 오후 점검 기준선) · # 이전 기록(2026-09-07 오전 · 2026-09-06)
