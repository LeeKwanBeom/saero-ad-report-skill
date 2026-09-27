# 제외 검색어 자동화 — API·UI 실물·registry·판정 규칙 (정본)

`scripts/exclusions.py`가 하는 일의 값 정의다. **문서 = 코드**: 여기 적힌 규칙과 코드가 어긋나면 둘 다 고친다.
탐색 근거는 `audit/last-audit.md` "기능 추가 탐색 기준선(제외 검색어 등록 자동화, 2026-09-27)" 0~5절.
표기: [실측] 실물에서 확인 · [문서] 네이버 공식 문서 · [추론] 확인 안 됨.

## 1. 대상과 원칙

- 대상: `config/report-config.json` → `exclusions.targets` 의 파워링크 광고그룹 3개(ID·URL). **그룹명은 config에 없다** —
  첫 `pull` 때 API `GET /ncc/adgroups/{id}` 의 `name` 으로 채워 registry에 적는다(어느 ID가 어느 그룹인지 사람이 확인한 적이 없음 [실측 09-27]).
- 칸: **"확장 검색" 칸만**(API `type=EXP_SEARCH`). "일치(유사검색어)" 칸·플레이스 그룹은 대상 아님 — 코드가 `exclusions.type` 으로 강제.
- 순서: **후보 제시(propose) → 사용자 승인 → 쓰기 전 읽기(pull) → 등록(push) → 다시 읽어 확인(verify) → 기록(registry)**.
  확인이 안 된 이름은 성공이라고 쓰지 않는다(`status=failed`).
- "이미 등록했었냐"는 **사용자에게 묻지 않는다.** registry(API·UI 실물)로 판정한다.
- 읽기는 언제나, 쓰기(push·delete·test-roundtrip)는 승인 문구에 대한 답 뒤에만. 진단·검증·탐색 회차는 읽기 전용.

## 2. 네이버 검색광고 API [문서: naver/searchad-apidoc, api.searchad.naver.com]

| 항목 | 값 |
|---|---|
| base | `https://api.searchad.naver.com` (config `exclusions.api_base`) |
| 목록 | `GET /ncc/adgroups/{adgroupId}/restricted-keywords?type=EXP_SEARCH` — `type` 을 안 주면 기본이 `KEYWORD_PLUS_RESTRICT`(스마트블록·유사검색어 쪽)라 **확장 칸이 안 나온다** |
| 등록 | `POST /ncc/adgroups/{adgroupId}/restricted-keywords` body `[{"keyword","type":"EXP_SEARCH","description"}]` — 응답은 항목별 객체(`nccAdgroupRestrictKwdId`, `regTm`, 실패면 `resultStatus{code,message}`) |
| 삭제 | `DELETE /ncc/adgroups/{adgroupId}/restricted-keywords?ids=id1,id2` |
| 그룹 | `GET /ncc/adgroups/{adgroupId}` → `name`, `userLock`, `useExpSearch`, `useAdvoost` |
| `regTm` | 응답의 등록시각은 **UTC**(`…Z`) — registry에는 KST 날짜로(5절) |
| 인증 헤더 | `X-Timestamp`(ms) · `X-API-KEY`(엑세스라이선스) · `X-Customer`(CUSTOMER_ID) · `X-Signature` = base64(HMAC-SHA256(비밀키, `"{ts}.{METHOD}.{uri}"`)), **uri 는 쿼리 제외 경로** |
| CUSTOMER_ID | **4480035** (도구 > SA API 사용 관리 화면 표시값 [실측 09-27]) — 광고주센터 URL의 `ad-accounts/2580077` 나 보고서 CSV 헤더 계정번호와 **다르다** |
| 한도 | 그룹당 최대 개수 초과 = 오류 3716(숫자 미공개, UI 카운터 `0/950` 로 보아 950 [추론] → config `max_per_group`, push가 현재+예정으로 초과 예상만 경고) |
| 오류 | 3721~3723(문자·형식), 3728, ADVoost ON 그룹 3754/4422(등록 거부) — 항목별 `resultStatus` 로 온다 |
| 429 | 5초 쉬고 1회 재시도, 그래도 429면 중단 보고 |
| 키 | `keys.json` `{"api_key","secret_key","customer_id"}` — **저장소·채팅 금지**. 이 세션에 연결되지 않은 PC 폴더(예 `C:\Users\<사용자>\naver-api.keys.json`)에 두고 `--key-file` 경로만 넘긴다. 채팅에 키가 찍힌 화면을 올렸으면 **재발급** |

회차당 호출: pull GET 6(그룹 3 × adgroup+목록) · push POST 3(그룹당 50개씩 나눠 보냄) · verify GET 6.

## 3. 환경 차단 [실측 2026-09-27] → 실행은 사용자 PC

Claude in Chrome·내장 브라우저는 `ads.naver.com`·`manage.searchad.naver.com` 을 "safety restrictions" 로 거부하고,
클라우드 컨테이너와 PC 연결 셸(device_bash)은 `api.searchad.naver.com` 에 프록시 CONNECT 403. 설정 화면(Claude Code·Cowork·Chrome용 Claude)에
네트워크 허용 목록은 없다(사용자 화면 9장 [실측 09-27]). 그래서 **경로 C**: 스크립트는 저장소에, 실행은 사용자 PC의 일반 셸(PowerShell)에서.
스크립트는 프록시 403을 `NetworkBlocked` 로 잡아 `[FAIL] 네트워크 차단(프록시)…` 를 찍고 **exit 2** — 그 명령을 PC에서 그대로 실행한다.

PowerShell(저장소 루트에서, `python` 3.9+):
```
python scripts\exclusions.py pull --key-file C:\Users\<사용자>\naver-api.keys.json          # 첫 실행은 이것만(읽기 전용)
python scripts\exclusions.py push --approved work\approved_<날짜>.txt --dry-run              # 할 일 목록만, 호출 0
python scripts\exclusions.py push --approved work\approved_<날짜>.txt --key-file <keys>       # 승인 뒤에만. 등록 → 자동 verify
python scripts\exclusions.py verify --key-file <keys>                                        # pending 재확인
python scripts\exclusions.py delete --group <adgroup_id> --ids <id,id> --key-file <keys> --confirm   # 되돌리기(승인 뒤)
python scripts\exclusions.py test-roundtrip --keyword saero제외테스트<날짜> --group <adgroup_id> --key-file <keys> --confirm
```
`pull`·`push`·`verify` 뒤의 `audit/exclusions.csv` 와 `work/exclusions_pull_<날짜>.json`(세 명령 모두 마지막으로 읽은 목록을 쓴다) 을 Claude가 읽어 판정·기록한다(사용자 폴더 경유 또는 커밋).
registry 파일이 없으면 `pull`·`import-ui` 외 명령은 `[FAIL] registry 없음 … (미확인)` exit 1 — 저장소를 통째로 받았는지·`--registry` 경로부터 본다.

## 4. UI 실물 [실측: 사용자 화면 23장, 2026-09-27] — API를 못 쓸 때의 읽기 폴백과 금지 요소

광고그룹 상세 탭: `키워드` · **`제외 검색어`** · `소재` · `확장 소재`.
- 제외 검색어 탭: 파란 `+ 제외 검색어 추가` · 표 `검색어 | 유형 | 설명 | 등록시각`(10행/페이지, 유형 문자열 `확장 검색`, 등록시각 `2026.09.26. 13:18`, 배지 `적은검색량` 은 등록과 무관).
- `제외 검색어 추가` 대화상자: 직접 입력 칸 **`확장 검색 (0/950)`** · `일치(유사검색어) (0/50)`(placeholder `한 줄에 하나씩 입력하거나 아래에서 추가하세요.` → 줄 단위 입력) /
  `ADVoost Max는 제외 검색어 타게팅이 적용되지 않으며…` 안내 / **`기간의 검색어`** 표(30일 창 `2026.08.28. → 2026.09.26.`): 헤더 `+ 전체추가 | 검색어 | 검색 유형 | 노출수 | 클릭수 | 총비용`,
  행 첫 칸 **`+ 추가`**(미등록) 또는 **`이미등록`**(등록됨, 행 흐림) / `행표시: 10 ∨`(30으로 늘리면 페이지 수가 준다) / `다운로드`(엑셀 — **상태 열 없음**, 대조에 못 쓴다) /
  `이유를 입력하시겠습니까? (선택)` 라디오(API `description` 대응 [추론]) / `취소` · `저장`.
- 이미 등록된 검색어는 `이미등록` 으로 보이고 `+ 추가` 링크가 없다 → UI에서는 중복 등록이 불가.
- 읽기 폴백(`import-ui`): 기간의 검색어 표를 전사한 텍스트(`이미등록|검색어|확장` / `+추가|검색어|확장` 한 줄씩, 앞에 `페이지|` 허용)를
  `python3 scripts/exclusions.py import-ui <파일> --group <그룹명> --date <날짜>` — **확장 행만** 반영, `+추가` 는 registry에 이미 있는 이름만 미등록으로 적는다(그 외 `+추가` 는 일반 검색어).

**금지 요소(브라우저 자동화가 열려도)**: `+ 전체추가`(기간의 검색어 수백 개가 한 번에 제외됨) · `일치(유사검색어)` 칸 · 플레이스 그룹 · 좌표 클릭 · `다른 그룹으로 복사`.
저장은 입력 칸을 read-back 해 승인 목록과 정확히 같을 때만. 이 문서를 읽는 회차가 읽기 전용이면 대화상자는 `취소` 로만 닫는다.

## 5. registry — `audit/exclusions.csv` (기계 정본, utf-8-sig)

열: `keyword, group_id, group_name, type, status, source, registered_at, restrict_kwd_id, verified_at, note`.
- 한 행 = 이름 × 그룹. `group_name="*"` 는 그룹 미확인 기록 행(대조 목록 표에서 온 것) — **3그룹을 다 읽은 pull이 그룹별 행으로 풀고 지운다**(없는 그룹마다 `unregistered`, 등록 기록인데 없으면 `missing`, `keep`은 `keep`). 첫 pull(2026-09-27) 뒤 registry에 `*` 행은 없다(648행 = 등록 183×3 + 미등록 33×3).
- `registered_at`은 **KST 날짜**. API `regTm`은 UTC(예 `2026-09-16T23:21:31.000Z` = 09-17 08:21 KST)라 `regtm_to_date`가 +9h 해서 적는다 — 검색어 CSV `일별`(KST)과 같은 기준이어야 "등록 당일" 판정이 맞다(첫 실사용 실측: 기록의 09-17·09-21 등록분이 UTC로는 09-16·09-20).
- 스냅샷 `work/exclusions_pull_<날짜>.json`: 그룹별 `name`·`count`·`keywords`(정렬) + `items{이름: {id, regTm(UTC 원문), registered_at(KST)}}`.
- `status`: `registered`(등록 확인) · `unregistered`(미등록 확인) · `pending`(POST 성공, 재확인 전) · `failed`(등록 실패 또는 **확인 실패**) ·
  `missing`(등록 기록이 있는데 API 목록에 없음) · `deleted`(삭제·시험) · `keep`(사용자 결정으로 후보에서 뺀다 — 노출 유지, 또는 문자 제한처럼 등록이 반복 실패해 포기한 이름).
- `source`: `api` · `ui`(화면 전사) · `record`(대조 목록 표) · `skill`(push/verify/test가 씀).
- 초기값(2026-09-27): 3그룹 UI 전사 340행 — 노원역필라테스 등록 135·미등록 24 / 노원산전필라테스 36·8 / 상계동필라테스 14·3 / 기록 행 `*` 등록 87·미등록 33.
  **미등록 33개**(09-23 32개 중 22 + 09-27 제안 14, 겹침 3) 가 첫 자동 회차의 재등록 후보다.
- 이름 판정(`registration_status`): 미등록 증거만 → `unregistered` / 등록·미등록 증거 혼재 → `partial`(일부 그룹 누락) / 등록 증거만 → `registered` / `keep` / 없음 → `unknown`.
- 그룹명 대조는 공백만 무시(`norm_name`). pull 은 registry 그룹명이 API 그룹명과 하나도 안 맞으면 `[주의]` 를 찍는다 — 그대로 두면 상태가 영원히 어긋난다.

## 6. 후보·재노출 판정 규칙 (`propose`, 쓰기 0)

입력: 합본 `검색어.csv`(`--day` 하루 또는 `--since` 이후, 기본 마지막 날) 의 **`검색 유형 == "확장"` 행만**, 이름 **정확 일치**(`노원역;24시` ≠ `노원역24시`).
1. 등록 이력이 있는 이름(registry에 있음) → **재노출 판정**(묻지 않는다):
   - `registered` 이고 마지막 등록일(`max(registered_at)`) **다음 날 이후** 노출 → **"등록돼 있는데도 노출"**(등록일·노출일 명시; 원인은 "~일 수 있음" 으로만) → 07번 각주·12번 1번에 사실만.
   - 등록 당일 노출 → **"등록 당일(판정 안 함)"**(CSV가 일 단위). 등록일 이전 노출 → "등록 전 노출(정상)".
   - `partial` → **"일부 그룹 미등록 → 후보"**, `unregistered` → **"등록 누락 → 후보"** — 둘 다 재등록 후보에 자동 포함.
   - 등록일 미상 → "등록됨(등록일 미상)". `keep` → "노출 유지(사용자 결정)". registry에 없는 이름은 재노출 절에 오르지 않는다(신규 후보 규칙으로).
   - **"미확인" = registry 파일이 없거나 못 읽은 회차.** `load_registry`가 `RegistryUnavailable`을 내고 propose/push/verify/delete/test-roundtrip/report는
     `[FAIL] registry 없음: <경로> — 등록 상태를 판정할 수 없어(미확인) 멈춥니다` **exit 1** — 후보·등록·기록 0. 빈 registry로 진행하면 이력 있는 이름이 전부 신규 후보로 올라오기 때문이다.
     registry를 새로 만들 수 있는 명령은 `pull`·`import-ui`만(2026-09-27 검증 판단 1).
2. 등록 이력이 없는 이름: **클릭 > 0 이면 후보 아님**(07번 표에서 사람이 본다) → `never_exclude_patterns`(부분 일치: 운동·산전·산후·임산부)·
   `competitors`(config, `never_exclude_competitors=true`) 해당 → **"후보에서 뺀 것"**(이유와 함께 보고만) → 이전 CSV에 있었던 이름은 건너뜀(`--all` 로 포함) →
   `industry_terms`(필라테스·필테) 포함 → **"업종어 포함"** 묶음(기본 후보 아님, 사용자가 고르면 승인 목록에 넣는다) → 나머지 = **신규 후보**(무관/애매/키즈 분류는 채팅에서, 결정은 사용자).
3. 승인 문구(그대로 채팅에):
   > 제외 검색어 등록 승인 요청 — 대상: 파워링크 3그룹(…) "확장 검색" 칸 / 건수: N / 목록: 이름1 · 이름2 · … / 제외한 것: 금지 패턴·경쟁사 n · 이미 등록 m · 노출 유지(사용자 결정) k
   (m = 창 안에 나왔지만 registry에 등록 확인된 이름 수, k = `keep` 이름 수 — 2026-09-27 검증 판단 3)
   > 답: "등록 승인 N개" (뺄 이름이 있으면 적어 주세요 — 그만큼 뺀 뒤 다시 확인합니다). 답이 오기 전에는 아무것도 등록하지 않습니다.
   승인된 이름만 `work/approved_<날짜>.txt`(한 줄에 하나, `#` 주석 허용)에 남겨 `push --approved` 에 넘긴다.

## 7. 등록·확인·실패 처리 (`push` → `verify`)

- `push` 는 승인 목록에서 금지 패턴·경쟁사 이름을 **거부**(`[거부] …`, 승인 목록에 있어도 등록 안 함) → `pull`(쓰기 전 읽기) → 그룹별 `현재 N + 등록 예정 M = 합`을 찍고
  config `max_per_group`(950 추정) 초과 예상이면 `[주의]`(차단은 안 함) → **그룹마다 아직 없는 이름만** POST(50개씩) →
  응답 항목별 `resultStatus` 로 성공(`pending`)/실패(`failed`, 코드·문구 기록) → `verify`(다시 읽어 3그룹 모두 있으면 `registered`+`verified_at`, 없으면 `failed`) → `work/` 스냅샷.
  exit 0 = 전부 확인, 1 = 실패·미확인 있음(재시도는 사용자 결정), 2 = 네트워크 차단.
- **실패한 이름은 사라지지 않는다**: `failed` 이름은 재노출이 없어도 다음 `propose` "재등록 후보"에 `직전 실패: <사유>`와 함께 오르고 `report`에도 나온다.
  문자 제한(3721~3723)처럼 반복 실패할 이름은 사용자가 registry `status=keep`으로 바꿔 뺀다(2026-09-27 검증 판단 2).
- **이름 대조는 대소문자 무시**(`K()` = 공백 제거 + 대문자): 네이버는 영문을 **대문자로 저장·응답**한다(첫 실사용 실측 `saero제외테스트0927` → `SAERO제외테스트0927`). registry·승인 목록·CSV 이름은 원문대로 두고 대조만 대문자로.
- `description` = `<prefix> MM-DD`(예 `saero 09-27`, 시험은 `saero test 09-27`; config `description_prefix`) — UI 설명 열·API 로 스킬 등록분과 수동 등록분을 구분.
  **길이 한도는 문서에 없다** — 첫 실사용(2026-09-27) 시험에서 `saero-ad-report 시험 2026-09-27`(29자)가 **400 / 3721 "description … maximum length"** 로 거부됐다(POST 전체 거부, 등록 0).
  `NaverApi.add_restricted`는 3721이면 **prefix만 → 설명 없음** 순으로 물러서서 등록하고(`last_description`에 실제 값), push·test 로그에 그 사실을 찍는다. 다른 400·401은 즉시 실패.
- `--dry-run`: 승인 목록·거부·그룹별 계획(registry 기준: 등록 예정/이미 등록/현재 등록 수 → 등록 후 합/한도 추정)만 출력, **HTTP 호출 0·registry 변경 0**. 첫 pull 전에는 그룹 ID 매핑이 없어 registry 그룹명 기준으로 계획을 보인다.
- 부분 실패(그룹 일부·항목 일부): 성공/실패를 그룹×이름으로 나눠 보고, 조용히 넘어가지 않는다. 한도 초과(3716)는 항목별 `failed`로 남는다 — 남은 용량은 계산하지 않는다(공식 한도 미공개, 950은 UI 카운터 추정) → 노출 많은 순으로 잘라 **다시 승인** 받는다.
- 되돌리기: `delete --group <id> --ids <restrict_kwd_id,…> --key-file <keys> --confirm`(registry `deleted`). 삭제도 승인 대상 — `--confirm` 없이는 돌지 않고, `--dry-run`은 호출 0.

## 8. 시험 등록 (`test-roundtrip`, 사용자 입회, 1건)

`--confirm` 없이는 돌지 않는다. 순서: 그룹 1개에서 시험 문자열(예 `saero제외테스트0927`, 실제로 검색될 리 없는 것) **없음 확인 → POST → GET 확인(없으면 `verified:false` 실패) → DELETE → GET 없음 확인** →
registry `deleted` 행. 사용자는 같은 그룹의 제외 검색어 탭에서 생겼다 사라지는 것을 본다. 실제 이름으로 대량 시험 금지. 검증 회차는 같은 시험 1건을 재현한다.

## 9. 기록 (갱신 회차 8단계)

- 기계 정본 = registry. 사람이 읽는 표 = `audit/last-audit.md` "등록 제외 검색어 대조 목록" 에 **회차별 요약 행만**(등록 n · verified n · 실패 n · description) — 이름 원본은 registry에 있다.
- 재노출 판정 결과 세 가지("등록돼 있는데도 노출"/"등록 누락 → 후보"/"미확인")는 채팅 보고와 07번 각주·12번 1번에 그대로 쓴다.
- 이 기능으로 생긴 [의도된 동작]·"되돌리면 안 되는 것" 은 `audit/checklist.md` 18~20번·표 하단 9행(6행 + 수정 회차 2의 3행).
