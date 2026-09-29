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
# 수정 기록 4(Code 탭 회차 1 — 조정 재검토 3 X1~X13 반영, 2026-09-28)
세션: 데스크톱 앱 Code 탭(이 PC), Opus 5.5 — 수정 회차 2·3과 같은 세션이 조정 지시("수정 회차 4 …")를 받아 수정. 브랜치 **`feat-code-tab`**(`150d059` 위 커밋 2개: ① 코드·시험·문서 ② 이 절·checklist — 자기 참조라 해시는 적지 않는다), **main 미반영**. 이 회차 뒤에는 조정 대조만 하고 검증 2로 간다(사용자 결정).
검증용 clone: `git clone -c core.autocrlf=false -b feat-code-tab --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill <별도 폴더>`
사용자 결정(조정): 승인 문구에 번호 채택 · `--pending` 도장은 모드 표시 + `[주의]`만 · 제안 ID 대조·토큰 범위 헤더는 보류.
외부 쓰기: 스킬 저장소 = `feat-code-tab` push만 · 배포 저장소 = 무인증 읽기 GET 1회(리허설 1의 4단계 — 리허설 2는 가짜 API) · 네이버 0 · 실제 fetch 0 · **실제 자격 증명 사용 0**(리허설 배포는 가짜 도우미 + 가짜 API) · main·main 작업 폴더 0 · `D:\saero` 설치 0 · 토큰 수령 0.
효율: 벽시계 약 2시간 20분(20:41 지시 → 23:0x 보고 KST — 반박 리뷰 워크플로 약 19분 · 변이 실험 4분 30초 포함) · 도구 호출 약 300회(조정자) + 반박 리뷰 워크플로 하위 에이전트 4 · 즉석 코드: 리허설 러너 2개 약 90행(가짜 네이버·가짜 GitHub — 스크래치) + 리허설 2 스크립트 약 40행 + 변이 러너 갱신 약 70행.
표기: [실측] 이 세션에서 직접 확인 / [추론] 확인 못 함. X = 조정 재검토 3 번호.

## X별 — 절·함수 기준
- **X1 exclusions 요청 도중 끊김**: `NaverApi._send` — `except (OSError, http.client.HTTPException, ValueError)`(URLError·HTTPError 다음 — ValueError = 응답 본문을 못 읽음, 리뷰 반영) → `ApiError("요청 결과 모름(<종류>) — 반영됐을 수 있다, verify로 확인")`. `do_push`는 그 묶음을 `failed`(종전 ApiError 경로), `do_verify`가 실제 상태를 다시 읽는다. `cmd_push`는 `do_push`·`do_verify`를 `try/finally save_registry`로(어떤 예외에도 저장). `cmd_verify` "확인할 이름이 없습니다" → `[verify] registry에 pending 0 — 등록 여부 판정 아님(--approved <승인 파일>로 확인)`. 재개 판정 = `verify --key-file … --approved <이번 회차 propose(.md5) 뒤에 생긴 가장 최근 work/approved_*.txt>`(code-tab 3절·4절 행 · local 진입 스킬 · SKILL 5-0 4항 · exclusion-ui 3·7절 · docstring). 승인 파일은 `do_push(…, before_post=)` — pull·X6 재검사를 통과한 뒤 첫 POST 전에 쓴다(POST 0 FAIL이면 안 생김 · 첫 pull 실패는 `POST 전에 멈춤(POST 0 — 승인 파일 안 씀)`). 완료 줄: 요청 실패가 있었지만 verify가 전부 확인하면 "… 다시 읽은 목록엔 전부 있음(registry registered) — verify --approved로 확인, 재시도 안 함"(exit 1 유지 — code-tab 4·5절·exclusion-ui 7절).
- **X2 precheck 도장**: `scripts/precheck.sh` — 인자 수 확인 뒤 옛 도장부터 지우고(`rm -f` — 파일 없음 exit 2에도 안 남게, 리뷰 반영) 파일 확인 뒤 `M0`(작업본)·`P0`(직전 배포본) md5, `MODE=full|pending`, 끝에서 `M1 ≠ M0`면 `[FAIL] 작업본이 precheck 도중 바뀜`(도장 없음), 도장 = `<M0>  <이름>` / `<P0>  <이름>` / `mode <MODE>`. `deploy.py` `precheck_stamp(path, data, base)` → (통과, 사유, pending): 작업본 md5 · 형식(옛 1줄 도장 FAIL) · 직전 배포본 md5 = `--base`(아니면 "4단계를 다시 받았으면 5·6단계부터") · pending이면 호출한 쪽이 `[주의] --pending 통과본(답 대기 배포용)`(막지 않음, 실제 push·dry-run 둘 다).
- **X3** `build_approved` 쌍둥이 검색에 `_industry.txt` 줄(`<파일>:<줄>`).
- **X4** (a) `--from-candidates`와 `--industry`를 함께 주면 realpath에서 접미사를 뗀 앞부분이 같아야(같은 폴더·같은 `<창 이름>`) — 아니면 `[FAIL] --from-candidates와 --industry가 같은 propose 실행이 아님`. (b) `cmd_propose`가 `.md5`에 `<합본 검색어.csv md5>  combined`·`<registry md5>  registry` 두 줄을 더 쓰고, `check_provenance(…, reg_path)`는 지금 `work/combined/검색어.csv`·registry md5가 기록과 다르면 `[FAIL] propose 뒤 합본·registry가 바뀜 — propose부터 다시·재승인(<label>: …)`(지시 문구를 잇고 값은 끝에 — 리뷰 반영). (c) `under_work()` — 두 원천도 저장소 `work/` 밑(realpath·대소문자 무시)이어야(`--extra-csv`는 이미 `work/combined/검색어.csv`만).
- **X5** `build_proposal` 승인 문구 `목록(번호 = 후보 파일 줄): 1 이름 · 2 이름 …` + 답 예("등록 승인 N개" 그대로 · "3 빼고" · "업종어 2 넣기"), `render_proposal` 업종어 절 `- <번호> 이름`(= `_industry.txt` 줄). 문서: SKILL.md 5-0 3항 · code-tab.md 6절 · exclusion-ui.md 6절(세션은 답의 번호를 `--drop`·`--industry-lines`에 그대로).
- **X6** `do_push(…, stop_if_all_present)` — pull 직후 고른 이름 중 대상 그룹 전부에 이미 있는 이름이 있으면 `AlreadyPresent` → `cmd_push` `[FAIL] 고른 이름 중 n개가 방금 읽은(pull) 대상 그룹 전부에 이미 있음: … — registry가 낡아 dry-run이 못 본 것(9/28 유형). POST 0 · pull 결과는 registry에 저장 — propose부터 다시·재승인`(참조 모드 실제 push만).
- **X7** `build_approved` — `registration_status == "keep"`이면 `[FAIL] 이름 … : registry에 keep(사용자 결정 '노출 유지') — 등록하지 않는다`.
- **X8** `deploy.py` PUT status 0(요청 예외)·5xx → `[FAIL] PUT 결과 모름(<msg>) — 반영됐을 수 있다. 재PUT 금지, 먼저 deploy.py verify --file <작업본>` exit 1 · GET 본문 ≠ `--base`인데 = 작업본이면 `지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨(verify로 확인). PUT 안 함 (md5 …)` exit 0(지시 문구 그대로, md5는 끝 — 리뷰 반영). code-tab.md 4절 행 2개·5절.
- **X9** `deploy.py` 인자 오류를 GET 전에: `fetch`에 `--out` 없음 · `verify`에 `--file` 없음 · 실제 `push`에 `--file` 없음 → exit 2(요청 0). `credential()`은 `token_file is not None`(빈 문자열 `--token-file ''`도 token-file → 못 얻음 FAIL, git 자격 증명으로 넘어가지 않음). `usable()` = `re.fullmatch(r"[A-Za-z0-9_]+")`.
- **X10** `NaverApi._mask` — 오류 응답(4xx·5xx)·URLError 문구 속 `api_key`·`secret_key` 값을 `***`로(문자열·목록·사전을 따라). 오류 본문은 **가린 뒤에** 500자로 자른다(기본 sender·HTTPError 분기는 자르지 않고 `_send`가 가림 → 자름 — 리뷰: 500자 경계에 걸친 키 앞부분이 새던 것). 출력·registry note 둘 다.
- **X11** `precheck.sh` — 작업본·직전 배포본 파일이 없으면 md5 가드 전에 `[FAIL] 파일 없음: <경로>` exit 2.
- **X12** `tests/test_fetch_reports.py` 끝: `sys.exit(0 if 성공 and md5 같음 else 1)` · `exclusions.NOW`(승인 파일 시각) — 시험이 고정해 두 번째 파일이 반드시 `approved_2026-09-28_120000_2.txt` · X1~X11 짝 시험(아래 W12·X12 목록).
- **X13** 문서·기록: code-tab 5절 deploy exit 2(`[FAIL] --file을 읽을 수 없음` 등 GET 전 인자 오류 전부)·exit 0 행 · "이미 registered" → "고른 이름 중 하나라도"(code-tab·exclusion-ui·checklist·SKILL) · checklist 비출력 시험 행(`GIT_*` 전부 제거·`GIT_CEILING_DIRECTORIES` — test_deploy·test_ingest `clean_env`) · checklist 거부 행 위치 열 `build_approved`, C③ 참조 모드 `[FAIL]` · code-tab 4절 combine FAIL 뒤 되돌리기(`git restore --source=HEAD --staged --worktree -- data`, `??`는 `git clean -n` 확인 뒤) → 모든 폴더 한 번에 ingest · 재시도 줄 "`--industry`도 새 창 파일" · 5-0b "propose를 다시 돌리면 번호·출처 기록이 바뀌니 재승인" · propose 줄바꿈 이름은 `newline` 목록 → 승인 문구 "줄바꿈 이름 n"·제안서 repr · CSV 칸 줄바꿈: **그 행(여러 파일 줄)만 고르면 FAIL, 다른 행은 줄 번호 그대로 선택 가능**(`read_csv_terms`는 `newline="\n"`으로 읽어 줄 번호 = `grep -n` — 따옴표 칸 안 CR만 든 행도 그 한 줄만 FAIL, 뒤 행 번호는 안 어긋난다(리뷰 반영: `newline=""`이면 lone CR을 줄로 세 뒤 행이 밀렸다) — 종전 근거 문구가 틀렸다) · 409 문구 = 수정 기록 3 W8(`… PUT 안 됨, 4단계부터 다시 할지는 사용자가 정한다`) · 수정 기록 3 W12 "13개" → "12개(+7)".
- 시험(새 파일 0): `test_exclusions` 49개(+8: 요청 도중 끊김 2 · 응답 도중 끊김(IncompleteRead)·응답 못 읽음(JSONDecodeError — 가짜 sender·기본 sender) · 업종어 쌍둥이 · 같은 실행·합본/registry 변경 · pull 뒤 전부 있음(승인 파일 0 · 첫 pull 실패) · keep · 키 가림(500자 경계 포함), 기존 fixture = 원천 `work/` 밑·출처 기록 4줄·시계 고정·CSV 줄바꿈 행만 FAIL·번호 승인 문구) · `test_deploy` 15개(+3: 도장 prev·모드·옛 형식 · 결과 모름·이미 반영(문구 한 덩어리) · 인자 오류 GET 0·토큰 형식) · `test_ingest` 10개(PrecheckTests +1: pending 모드·도중 수정·파일 없음(직전 배포본·작업본 — 옛 도장도 지움), 도장 3줄 단언) · `test_fetch_reports` 15개(rc).

## 변경 파일(`150d059` → 커밋 ①; `wc -l` · md5 앞 8자리) [실측]

| 파일 | 행수 | md5 | 증감(+/−) |
|---|---|---|---|
| `SKILL.md` | 548 | 29b22c35 | +21 / −11 |
| `audit/checklist.md`(커밋 ②) | 505 | 5122076d | +8 / −6 |
| `local/saero-run/SKILL.md` | 28 | 7dd534c8 | +1 / −1 |
| `references/code-tab.md` | 229 | 464fc9ad | +38 / −22 |
| `references/exclusion-ui.md` | 158 | ee6033c8 | +20 / −10 |
| `scripts/deploy.py` | 314 | 9a5a7bee | +49 / −18 |
| `scripts/exclusions.py` | 1355 | e3904e68 | +159 / −50 |
| `scripts/precheck.sh` | 37 | 3d3f89b3 | +12 / −5 |
| `tests/test_deploy.py` | 351 | 0d419c2e | +67 / −6 |
| `tests/test_exclusions.py` | 1099 | aed40d4b | +258 / −23 |
| `tests/test_fetch_reports.py` | 607 | 8afa5ff4 | +4 / −1 |
| `tests/test_ingest.py` | 383 | ffa1098f | +35 / −8 |
| `audit/last-audit.md` | (이 절 포함 — 커밋 ②) | — | — |

## 임의 결정(수정 회차 4 번호)
1. **도장 3줄 형식** = `<md5>  <이름>` 두 줄 + `mode full|pending`(`md5sum` 형식 유지 — 사람이 `md5sum -c`처럼 읽기 쉽게). deploy는 1·2줄 첫 칸·3줄 끝 칸만 본다.
2. **옛 형식 도장(1줄)은 실패**(형식이 다르면 직전 배포본을 대조할 수 없다 — precheck를 다시).
3. **pending `[주의]`는 실제 push·dry-run 둘 다** 한 줄(막지 않음 — 사용자 결정 "모드 표시 + `[주의]`만").
4. **precheck의 P0(직전 배포본 md5)도 시작할 때 잰다**(M0와 같은 때 — 도중 수정 검사는 작업본만, 지시대로).
5. **X4(a) 같은 실행 판정** = realpath에서 `_candidates.txt`·`_industry.txt`를 뗀 앞부분이 같음(대소문자 무시). 한쪽만 주면 판정 없음.
6. **X4(b) 대조 대상** = 저장소 `work/combined/검색어.csv`(표준 합본 — propose가 다른 합본 폴더를 읽었어도 push는 표준 합본과 대조)와 push가 쓰는 registry. 기록에 줄이 없으면(옛 `.md5`) "없음"으로 FAIL.
7. **X6은 참조 모드 실제 push에만**(`--approved`는 dry-run 전용이라 해당 없음). 일부 그룹에만 있는 이름은 멈추지 않는다(그 그룹만 건너뜀 — 재등록 후보).
8. **X8 "이미 반영" 판정은 `--base`가 있을 때만**(GET 본문 ≠ base이고 = 작업본). dry-run도 같은 줄·exit 0.
9. **X9 `push --dry-run`에 `--file`이 없는 것은 그대로 허용**(S0 사전 점검). 종전 "…에는 --file 이 필요합니다"(GET 뒤)는 도달하지 않는 방어로 남겼다.
10. **X10 가림은 오류 응답(status ≥ 400)만**(성공 응답의 이름은 원문 그대로 — 키 문자열이 이름에 들어갈 일 없음).
11. **X13 CSV 줄바꿈 행** = 여러 파일 줄에 걸친 레코드의 **모든 줄 번호**를 막는다(시작 줄·끝 줄 어느 쪽을 골라도 FAIL). 쌍둥이 검색에서도 뺀다.
12. **X13 줄바꿈 이름**은 `newline` 목록으로 따로(승인 문구 "줄바꿈 이름 n", 제안서 `## 줄바꿈 이름 n개` repr). 재등록 후보 쪽도 같은 기준.
13. **X1 완료 줄 문구**(리허설에서 찾음): 요청 실패가 있었지만 verify가 전부 확인하면 "요청 실패·결과 모름이 있었지만 다시 읽은 목록엔 전부 있음(registry registered) — verify --approved로 확인, 재시도 안 함" — 종전 문구("실패 항목은 registry status=failed")가 실제 상태와 어긋났다. exit 1은 유지.
14. **X12 시계 고정** = 모듈 전역 `NOW`(= `dt.datetime.now`)를 시험이 바꿔 끼운다(`today()` 등 다른 시각은 그대로).
15. **409 문구**: 수정 기록 3 임의 결정 19("409 = 지시 문구 그대로")를 되돌려 기록 W8 문구로(X13 지시).
16. **승인 파일 쓰는 때**(리뷰 반영) = `do_push`의 pull·X6 재검사를 통과한 뒤 첫 POST 전(`before_post` 콜백 한 번). AlreadyPresent·첫 pull 실패(ApiError·NetworkBlocked)면 파일 0 — 재개 판정("가장 최근 승인 파일")이 보내지 않은 이름을 failed로 적지 않게. 첫 pull ApiError 문구 = `POST 전에 멈춤(POST 0 — 승인 파일 안 씀)`.
17. **재개 판정 한정**(리뷰 반영) = "이번 회차 propose(.md5) 뒤에 생긴 가장 최근 `work/approved_*.txt`" — 없으면 이번 회차 실제 push는 POST 전. 문서 규칙만(코드가 회차를 강제하지 않는다 — work/는 회차마다 쌓인다).
18. **응답 본문을 못 읽음(ValueError — JSONDecodeError·UnicodeDecodeError)도 `요청 결과 모름`**(리뷰 반영) — 200인데 본문이 JSON이 아니면 서버엔 반영됐을 수 있다. GET에서 나도 같은 문구(한 곳에서 판정).
19. **가린 뒤 자르기**: 오류 응답(≥ 400)의 `message`(문자열)를 `_mask` 뒤 500자로 — JSON 오류 본문의 message도 같이 자른다(종전엔 JSON 아닌 본문만 sender에서 잘랐다).
20. **CSV 줄 번호 = `\n`만**(`newline="\n"`): 따옴표 칸 안 CR만 든 행은 그 한 줄만 FAIL, 따옴표 없는 칸의 CR은 csv 오류로 파일 전체 FAIL(이름을 잘못 읽는 것보다 멈춤).
21. **precheck 옛 도장 지우기 = 인자 수 확인 뒤·파일 확인 전**(인자 수가 틀리면 도장 경로를 모른다 — 그때만 지우지 않는다).
22. **`--expect`의 N**(리뷰: 문서끼리 달랐다) = 답의 N, N 없는 번호 답이면 세션이 목록 수에서 계산하고 실제 push 전에 dry-run의 `[승인 목록] N개`·이름을 사용자에게 보인다(확인 왕복을 새로 두지는 않는다) — SKILL 5-0 4항·code-tab 6절·exclusion-ui 6절 같은 문장.
23. **문구 순서**: X8 "이미 반영"·X4(b) "합본·registry가 바뀜"은 지시 문구를 한 덩어리로 두고 값(md5·label)은 끝 괄호로 — 문서 인용이 부분 문자열로 그대로 걸리게. 시험도 한 덩어리로 단언.
24. **리뷰 지적 중 이월 1건**: `blocked_reason`이 공백·기호 변형('젠 필라테스'·'산 후 필라테스')을 못 잡음 — 이번 diff 밖 기존 코드, NFKC와 묶어 점검 회차(조정자 결정 몫).

## 원래 지시를 바꾼 곳과 이유
- X1 "do_push가 그 묶음을 failed로" → 완료 줄 문구도 바꿨다(임의 결정 13 — verify가 registered로 바로잡은 뒤에도 "failed"라고 말해서).
- X12 "X1은 POST 중 TimeoutError 가짜 sender → registry 저장·failed·exit 1" → **서버엔 반영됐는데 응답만 잃은 경우**(verify가 registered로 바로잡음)도 같은 시험에 넣었다 — "결과 모름"의 두 갈래.
- X12 "test_fetch_reports는 실패하면 rc ≠ 0" → 짝 변이는 시험 파일 쪽(옛 main)이라 변이 러너 밖에서 시연했다: 클릭 가드를 깨고 새 판 rc 1 / 옛 판 rc 0.
- X1 재개 판정 "`verify --approved <가장 최근 work/approved_*.txt>`" → "**이번 회차 propose(.md5) 뒤에 생긴** 가장 최근"(리뷰: 지난 회차 파일로 "전부 확인"이 나와 등록을 건너뛸 수 있다 — 임의 결정 17).
- 수정 회차 3 W3 "실제 push만 승인 파일을 쓴다(등록 전에)" → "실제 push 중 **pull 재검사를 통과한 것만**, 첫 POST 전에"(X6과 겹쳐 POST 0 FAIL 뒤 파일이 남던 것 — 임의 결정 16).
- X1 "`OSError·http.client.HTTPException`" → **ValueError(응답 못 읽음)도**(리뷰: POST가 반영된 뒤 JSON 아닌 본문이면 Traceback으로 멈추고 나머지 그룹을 건너뛰며 registry에 흔적이 없었다 — 임의 결정 18).
- X10 "(deploy mask와 같게)" → 가림을 **자르기 전에**(종전 코드는 sender가 먼저 500자로 잘라 경계에 걸친 키 앞부분이 샜다 — 임의 결정 19).

## 실측 [실측]
- **시험**(스크래치 LF clone = 작업본 코드 md5 같음, venv, PYTHONUTF8 없이, `-W error::ResourceWarning`, test_deploy는 `GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`): test_exclusions **Ran 49 OK** rc 0(2초) · test_deploy **Ran 15 OK** rc 0(23초) · test_ingest **Ran 10 OK** rc 0(67초) · test_fetch_reports **Ran 15 OK** rc 0(82초) — skipped 0
- **변이 실험 91/92 잡힘**(스크래치 LF clone, 271초 — 수정 회차 3의 54쌍 전부 + X 짝 27 + 리뷰 반영 R1~R11 — 대조군 먼저 전부 OK(test_deploy 13 · test_exclusions 23 · test_ingest 8 · 호출 환경 GIT_DIR) · 복원 뒤 status 깨끗). 놓침 1 = 92번(엉뚱한 GIT_DIR로는 `git credential fill`이 저장소 없이도 돼서 재현이 안 되는 변이 — 수정 회차 3과 같음), 제대로 된 시연(+ 행 — 다른 도우미를 가리키는 GIT_DIR)은 잡힘:

| # | 변이 | 결과 |
|---|---|---|
| 1 | E808 push return 0 | 잡힘(rc 1) |
| 2 | E830 verify return 0 | 잡힘(rc 1) |
| 3 | E673a split_blocked 경쟁사 거부만 빠짐 | 잡힘(rc 1) |
| 4 | E673b split_blocked 거부 전부 빠짐 | 잡힘(rc 1) |
| 5 | V1 합계≠N 검사 제거 | 잡힘(rc 1) |
| 6 | V1 이미 registered 검사 제거 | 잡힘(rc 1) |
| 7 | V1 K() 중복 검사 제거 | 잡힘(rc 1) |
| 8 | V1 범위 밖 검사 제거 | 잡힘(rc 1) |
| 9 | V1 쌍둥이 [주의] 제거 | 잡힘(rc 1) |
| 10 | V1 실제 push의 --approved 허용 | 잡힘(rc 1) |
| 11 | .gitattributes *.csv -text 줄 삭제 | 잡힘(rc 1) |
| 12 | .gitattributes 파일 삭제 | 잡힘(rc 1) |
| 13 | N3 시작 HEAD 검사 제거 | 잡힘(rc 1) |
| 14 | N3 줄바꿈 검사 제거 | 잡힘(rc 1) |
| 15 | precheck.sh b4cc8b9 판 통째(python3 고정) | 잡힘(rc 1) |
| 16 | precheck 옛 흐름(compute && compare / tail) + $PY | 잡힘(rc 1) |
| 17 | N2 base 대조 제거 | 잡힘(rc 1) |
| 18 | N2 --base 필수 제거 | 잡힘(rc 1) |
| 19 | N1 perm = True | 잡힘(rc 1) |
| 20 | V4 token_of 옛 판 | 잡힘(rc 1) |
| 21 | W1a registered 검사를 추가 이름만(옛 판) | 잡힘(rc 1) |
| 22 | W1a propose 기준(registration_status) 빠짐 | 잡힘(rc 1) |
| 23 | W1a 쌍둥이를 추가 이름만(옛 판) | 잡힘(rc 1) |
| 24 | W1b 출처 검사 끔 | 잡힘(rc 1) |
| 25 | W1b 접미사 검사 제거 | 잡힘(rc 1) |
| 26 | W1b md5 대조 제거 | 잡힘(rc 1) |
| 27 | W1b propose가 md5 기록을 안 씀 | 잡힘(rc 1) |
| 28 | W1c 참조 모드 거부 이름 FAIL 제거 | 잡힘(rc 1) |
| 29 | W3 dry-run도 승인 파일 씀 | 잡힘(rc 1) |
| 30 | W3 고정 이름 덮어쓰기(옛 판) | 잡힘(rc 1) |
| 31 | W4 isdecimal → isdigit | 잡힘(rc 1) |
| 32 | W4 후보 파일 읽기 오류를 안 잡음 | 잡힘(rc 1) |
| 33 | W4 CSV 칸 줄바꿈 검사 제거 | 잡힘(rc 1) |
| 34 | W5 빈 창을 lo > hi만 | 잡힘(rc 1) |
| 35 | W9 load_keys 형식 검사 제거 | 잡힘(rc 1) |
| 36 | W6 --base만(--file 없음) 허용 | 잡힘(rc 1) |
| 37 | 못 읽는 --base를 안 잡음 | 잡힘(rc 1) |
| 38 | W7 오류 문구 가림 제거 | 잡힘(rc 1) |
| 39 | W8 409 문구 제거 | 잡힘(rc 1) |
| 40 | W8 403 문구 제거 | 잡힘(rc 1) |
| 41 | permissions 필드 없음을 참으로 | 잡힘(rc 1) |
| 42 | W11 deploy 도장 검사 제거 | 잡힘(rc 1) |
| 43 | W11 precheck 도장 안 씀 | 잡힘(rc 1) |
| 44 | W11 precheck 옛 도장 안 지움 | 잡힘(rc 1) |
| 45 | W2 data/ HEAD diff 검사 제거 | 잡힘(rc 1) |
| 46 | W2 awk 옛 판($NF) | 잡힘(rc 1) |
| 47 | 리뷰 --extra-csv 출처(work/combined) 검사 제거 | 잡힘(rc 1) |
| 48 | 리뷰 deploy --file을 PUT 전에 다시 읽음(옛 판) | 잡힘(rc 1) |
| 49 | 리뷰 ingest 추적 안 된 파일 검사 제거 | 잡힘(rc 1) |
| 50 | 리뷰 propose 재등록 후보의 '전부 등록' 빼기 제거 | 잡힘(rc 1) |
| 51 | W12 원천 줄을 strip(앞뒤 공백 원문 훼손) | 잡힘(rc 1) |
| 52 | 리뷰 deploy 깨진 도장을 안 잡음 | 잡힘(rc 1) |
| 53 | 리뷰 propose 줄바꿈 든 이름 빼기 제거 | 잡힘(rc 1) |
| 54 | X1 요청 도중 끊김을 안 잡음 | 잡힘(rc 1) |
| 55 | X1 finally 저장 제거 | 잡힘(rc 1) |
| 56 | X1 verify pending 0 문구 옛 판 | 잡힘(rc 1) |
| 57 | X2 deploy 도장 직전 배포본 대조 제거 | 잡힘(rc 1) |
| 58 | X2 deploy 옛 형식 도장 허용 | 잡힘(rc 1) |
| 59 | X2 deploy pending [주의] 제거 | 잡힘(rc 1) |
| 60 | X2 precheck 도중 수정 검사 제거 | 잡힘(rc 1) |
| 61 | X2 precheck 모드 늘 full | 잡힘(rc 1) |
| 62 | X3 업종어 파일 쌍둥이 안 봄 | 잡힘(rc 1) |
| 63 | X4a 같은 propose 실행 검사 제거 | 잡힘(rc 1) |
| 64 | X4b 합본·registry md5 대조 제거 | 잡힘(rc 1) |
| 65 | X4b propose가 합본·registry md5를 안 씀 | 잡힘(rc 1) |
| 66 | X4c work/ 밑 검사 제거 | 잡힘(rc 1) |
| 67 | X5 승인 문구 번호 제거 | 잡힘(rc 1) |
| 68 | X5 업종어 절 번호 제거 | 잡힘(rc 1) |
| 69 | X6 pull 뒤 전부 있음 멈춤 제거 | 잡힘(rc 1) |
| 70 | X7 keep FAIL 제거 | 잡힘(rc 1) |
| 71 | X8 PUT 결과 모름 문구 제거 | 잡힘(rc 1) |
| 72 | X8 이미 반영 exit 0 제거 | 잡힘(rc 1) |
| 73 | X9 fetch --out 없음 GET 전 검사 제거 | 잡힘(rc 1) |
| 74 | X9 --token-file '' 이 git으로 넘어감(옛 판) | 잡힘(rc 1) |
| 75 | X9 usable 옛 판(공백·개행만) | 잡힘(rc 1) |
| 76 | X10 오류 응답 키 가림 제거 | 잡힘(rc 1) |
| 77 | X11 precheck 파일 없음 검사 제거 | 잡힘(rc 1) |
| 78 | X12 승인 파일 시각을 시계 고정 없이 | 잡힘(rc 1) |
| 79 | X13 CSV 줄바꿈 파일 전체 FAIL(옛 판) | 잡힘(rc 1) |
| 80 | X13 409 문구 옛 판 | 잡힘(rc 1) |
| 81 | R1 HTTPException(IncompleteRead) 안 잡음 | 잡힘(rc 1) |
| 82 | R2 응답 못 읽음(ValueError) 안 잡음(옛 판) | 잡힘(rc 1) |
| 83 | R3 자른 뒤 가림(옛 판 — 기본 sender에서 500자) | 잡힘(rc 1) |
| 84 | R4 승인 파일을 pull 전에 씀(옛 판) | 잡힘(rc 1) |
| 85 | R5 CSV를 newline=''로(CR도 줄로 셈 — 옛 판) | 잡힘(rc 1) |
| 86 | R6 --industry work/ 밖 검사 빠짐 | 잡힘(rc 1) |
| 87 | R7 X4b 문구 옛 판(괄호가 가운데) | 잡힘(rc 1) |
| 88 | R8 첫 pull 실패 문구 빠짐 | 잡힘(rc 1) |
| 89 | R9 X8 이미 반영 문구 옛 판(md5가 가운데) | 잡힘(rc 1) |
| 90 | R10 precheck 도장 지우기를 파일 확인 뒤로(옛 판) | 잡힘(rc 1) |
| 91 | R11 precheck 작업본 파일 확인 빠짐 | 잡힘(rc 1) |
| 92 | W10 자식 env에서 GIT_CONFIG만 지움(옛 판) + 호출 환경 GIT_DIR | 놓침(rc 0) |
| + | W10 제대로 된 시연(다른 도우미 GIT_DIR): [잡힘] W10 옛 판(GIT_CONFIG*만 지움) + 호출 환경 GIT_DIR(다른 도우미) → rc 1 · Ran 1 test in 1.155s FAILED (failures=1) | — |

- **X12 시연**: `fetch_reports.py` 클릭 가드(`if bad and bad in text:`)를 깨고 `PureTests.test_click_allowed_guard` — 새 판 시험 rc 1(FAILED) / 150d059 판 시험(exit=False) rc **0**(FAILED인데 성공으로 끝남).
- **리허설 2 — 리뷰 반영 뒤 최종 코드**(22:47:56 → 22:48:28, 스크래치 LF clone — 작업본 변경을 얹은 임시 main + 로컬 bare origin, exclusions·deploy·precheck md5 = 작업본, **네트워크 0 · 실제 자격 증명 0**):
  ingest(시작 검사 → `origin/main = HEAD` → 합본 PASS → push → `origin/main = HEAD`) → 4 fetch(가짜 GitHub API — 리허설 1이 받은 배포본 바이트, md5 a3465ec0) → compute → propose `--since 2026-09-27` = 승인 문구 `목록(번호 = 후보 파일 줄): 1 노원힐링장소.` · 답 예 줄 · 제안서 업종어 `- 1 노원역50대필라테스 … - 4 필라테스노원마라탕` · `.md5` 4줄(후보 30506405 · 업종어 2fade383 · combined f9657b32 · registry ca642639) →
  답 "등록 승인 1개" → 번호 그대로 `--from-candidates … --expect 1 --dry-run`: 쌍둥이 `[주의]` · `[승인 목록] 1개 = --expect 1 … dry-run: 파일 안 씀` · 3그룹 등록 예정 1(221 → 222/950) · 승인 파일 0 →
  실제 push(가짜 네이버 — POST 중 TimeoutError, 서버엔 반영): `[FAIL] 노원힐링장소.: 요청 결과 모름(TimeoutError) — 반영됐을 수 있다, verify로 확인` ×3(3그룹 모두 시도) → verify 3그룹 확인 1/1 → 끝 줄 `… 요청 실패·결과 모름이 있었지만 다시 읽은 목록엔 전부 있음(registry registered) — verify --approved로 확인, 재시도 안 함` rc 1 · registry 저장(ca642639 → abd65027, 3행 registered) · 승인 파일 1(pull 재검사 뒤) → `verify --approved <그 파일>` 3그룹 확인 rc 0 →
  precheck(작업본 = 배포본 + 주석 1줄) 통과 → 도장 3줄(`134d4de6… index.html` / `a3465ec0… prev.html` / `mode full`) →
  배포(가짜 GitHub API + 가짜 자격 증명 도우미): PUT 409 → `[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치) — PUT 안 됨, 4단계부터 다시 할지는 사용자가 정한다(PUT 409: …)` rc 1 →
  4단계만 다시(prev = 다른 배포본, md5 26c4c48a) → push → `[FAIL] precheck 통과본이 아님 — PUT 안 함(도장의 직전 배포본 md5 a3465ec0 ≠ --base md5 26c4c48a — 4단계를 다시 받았으면 5·6단계부터)` rc 1, **요청 0** →
  5·6단계 다시(compute → precheck — 도장 2줄 26c4c48a) → push → `배포 완료` rc 0(가짜 PUT 1) → (X8) 같은 push를 한 번 더(배포본 = 작업본) → `지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨(verify로 확인). PUT 안 함 (md5 134d4de6…)` rc 0, GET 1·PUT 0.
  (리허설 1 — 리뷰 반영 전 코드, 22:13:09 → 22:15:00: 같은 순서로 통과. 4단계 fetch만 무인증 실제 GET 1회.)
- **mutation_test**(리허설 2 clone, 배포본 = 리허설 prev): rc 0 · 32초 · `  [OK]` 43 · MISS·UNCOVERED·SKIP 0 · 원본 md5(html·CSV 4·data/ 8개) 전부 동일 · "전부 살아 있음".
- **전후**: 스킬 저장소 `ls-remote` HEAD·main b4cc8b9 · feat-code-tab 150d059(push 전) · test* 0 · 배포 32d8b05 · main 작업 폴더 HEAD b4cc8b9·status 0·md5 4dd3b0cf · `~/saero-fetch/downloads` 목록 ed69f294 같음.
- **반박 리뷰**: 워크플로 `wf_6735c7c3-ed9`(4관점 — 지시 준수·안전·셸/경로·문서 정합, 스크래치 사본에서 재현, 약 19분) → 26건(겹침 포함, medium 7 · low 19) = 고유 19건: **반영 18** · 이월 1(임의 결정 24).
  medium: X6 문서 "전부" ↔ 코드 "하나라도"(code-tab 3절·SKILL 5-0·docstring·시험 머리말) · POST 응답 해석 오류가 결과 모름이 아님(Traceback·나머지 그룹 건너뜀·registry 흔적 0) · POST 0 FAIL 뒤 승인 파일이 남아 재개 판정이 보내지 않은 이름을 failed로 적음 · 합본 CSV 칸 안 lone CR이면 뒤 행 번호가 밀려 이웃 행을 고름 · 재개 판정 "가장 최근"이 지난 회차 파일일 수 있음.
  low: X8 "이미 반영" 문구가 md5로 끊김 · X4(b) 문구 가운데 괄호 · HTTPException·`--industry` work/ 밖·작업본 없음 시험 없음(변이 생존 확인됨) · 파일 없음 exit 2가 옛 도장을 안 지움 · 500자 자르기가 가림보다 먼저 · load_keys 주석 · push 끝 줄 "전부 있음 — 재시도 안 함" 문서 없음 · exclusion-ui 3절·SKILL (4) 옛 답 형식·pending 재확인 명령 · `--expect` 출처 문서끼리 다름 · SKILL `--approved` 한정 · checklist deploy 행에 X8·X9 불변식 없음 · PUT 결과 모름 인용 글자.
  반영 뒤 짝 변이 R1~R11(아래 표) · 시험 +1(`test_post_cut_mid_response_or_unreadable_body_is_result_unknown`)·단언 보강 7곳(test_exclusions 5 · test_deploy 1 · test_ingest 1).
- **grep·문법**: py_compile 14파일 · 변경 13파일 UTF-8·CR 0 · 코드 울타리 짝수(SKILL 10·checklist 6·last-audit 4·code-tab 4·exclusion-ui 2) · `bash -n` scripts 2 · 옛 문구 grep 0(`가장 최근 work/approved`(한정 없는 것)·`고른 이름이 전부`·`전부 이미 있으면`·`"등록 승인 N개"만`·`raw[:500]`·`deploy.usable과 같은`·`뺄 이름)`·`= 답의 N)`·`PUT 결과 모름 — 재PUT`·`작업본(md5`·`바뀜({label}`·`시작할 때 옛 도장` — last-audit 옛 절 제외) · 문서 인용 FAIL·주의 문구 ↔ scripts 조각 대조: 새 불일치 0(남은 9건은 f-string·`[FAIL] {e}` 접두로 이어지는 조각 — 실제 출력에 있음) · "다시 계산" 흐름 4곳 같은 문장

## 검증 2가 볼 것(전체 — 이 절 하나로 돈다. 수정 기록 1~3의 해당 항목은 이것으로 대체)
1. **범위**: `git log --oneline b4cc8b9..HEAD` = 8커밋(f0520b5·df658f3·e220079·77a2ba8·0391e0f·150d059·이번 ①②) · `git diff b4cc8b9 --stat` · 불변(config·data/·reportlib·compute·validate·compare·archive 검사 로직, registry는 회차 1 시험 1행만 — `git diff b4cc8b9 -- audit/exclusions.csv` +1행 deleted).
2. **시험**(venv, PYTHONUTF8 없이, LF clone, test_deploy는 `GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`): test_exclusions 49 · test_deploy 15 · test_ingest 10 · test_fetch_reports 15(rc 0) OK, skipped 0 · mutation_test "전부 살아 있음"(배포본 무인증 재수령 + `archive.py combine` 합본).
3. **변이**: 위 표에서 최소 X1 셋·X2 다섯·X4 넷·X6·X7·X8 둘·X9 셋·X10·X11·X12(시계)·X13 CSV·R1~R11과 W1·W2·W3·W11 짝이 실패하는지 · W10(다른 도우미 GIT_DIR) · X12(fetch rc) 시연.
4. **S0 블록**(code-tab 2절): `bash -n` · 도우미 없는 임시 설정에서 배포 줄만 `[FAIL] 배포 저장소 점검 실패(… rc=1)` · `git diff --quiet HEAD -- data` 줄 · 줄바꿈 awk(탭 기준).
5. **ingest**: 시작 검사 넷(HEAD = origin/main · data/ = HEAD · 추적 안 된 파일 0 · 줄바꿈 = 커밋 — stat만 깨끗한 CRLF 포함) 모두 store 전·쓰기 0 · 끝 확인 2분기 · `-- data`만 커밋 · push 거부 `[FAIL]` · CRLF 입력 바이트 보존 · 되돌리기 `git restore --source=HEAD --staged --worktree -- data`(스테이징된 새 파일까지).
6. **propose**: 파일명 `<lo>_<hi>` · `_candidates.txt`·`_industry.txt`·`.md5`(4줄: 두 파일 + combined + registry) · 빈 창(행 0) `[주의]` · 번호 붙은 승인 문구·업종어 절 번호 · "줄바꿈 이름 n" · 재등록 후보에서 대상 그룹 전부 등록 이름 뺌.
7. **push 참조 선택 모드**(쓰기 전 `[FAIL]` — dry-run도, 승인 파일·HTTP·registry 0): 합계 ≠ N · 원천 없음·빈·못 읽음(UTF-16) · 번호 범위 밖(10진만) · 출처(work/ 밑 · 이름 접미사 · 같은 propose 실행 · 파일·combined·registry md5) · K() 중복 · CSV 줄바꿈 행(줄 번호 = `grep -n` — 따옴표 칸 안 lone CR 행도 그 줄만) · 고른 이름 중 하나라도 이미 registered(propose 기준 포함) · keep · 금지 패턴·경쟁사 · `--extra-csv`는 work/combined만. `[주의]` 쌍둥이(후보·업종어·합본·registry). dry-run 파일 0 · 실제 push만 `approved_<날짜>_<시분초>[_n].txt`(pull 재검사 뒤 첫 POST 전 — POST 0 FAIL이면 0개). push의 `--approved`는 dry-run 전용.
8. **실제 push 경로**(가짜 API): pull 뒤 고른 이름 중 하나라도 전부 있음 → POST 0 FAIL·pull 저장·승인 파일 0 · 첫 pull 실패 → `POST 전에 멈춤`·승인 파일 0 · 요청 도중 끊김(Timeout·IncompleteRead)·응답 못 읽음(JSONDecodeError — 기본 sender 포함) → 결과 모름·failed·나머지 그룹 시도·verify 재조회·registry 저장(예상 못 한 예외도) · 끝 줄 "다시 읽은 목록엔 전부 있음 — 재시도 안 함" · CLI push·verify exit 1(verified:false) · 재개 = `verify --approved <이번 회차 propose 뒤 가장 최근 승인 파일>` · pending 0 문구 · `X-API-KEY` 가림(500자 경계 — 가린 뒤 자름) · `load_keys` 형식.
9. **deploy**: 인자 오류 GET 전 exit 2(`--out`·`--file`·`--base`만·못 읽는 `--base`·`--file`) · `--token-file ''` FAIL · 토큰 형식 `[A-Za-z0-9_]+` · 도장 3줄(작업본·직전 배포본·모드, 옛 형식 FAIL, pending `[주의]`) · `--file` 한 번 읽기(PUT 본문 = 도장 바이트) · base 대조 · 이미 반영 exit 0(`지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨(verify로 확인). PUT 안 함 (md5 …)`) · PUT 결과 모름·409·403·404 · 오류 문구 `***` · dry-run 권한 확인(permissions.push — 계정 역할 기준) · 값 출력 0(stdout·stderr) · 자식 env 격리.
10. **precheck**: 파일 없음(작업본·직전 배포본) exit 2 — 옛 도장도 지움 · md5 가드 · compute 실패에서 멈춤 · 도중 수정 FAIL · 실패 실행은 도장 없음 · 도장 3줄·pending 모드.
11. **fetch_reports**: 금지 차단 문구(차단 순간 컷 없음 · partial 먼저 읽기) · docstring `$PY` · `--dry-run` 폴더 생성 0.
12. **문서 = 코드**: 인용 FAIL 문구 글자 대조(code-tab 4·5절, SKILL 5-0·6·7단계, exclusion-ui 6·7절) · "다시 계산" 흐름 4곳 같은 문장(5-0b 포함) · `--expect` N 문장 3곳 같음(SKILL 5-0 4항·code-tab 6절·exclusion-ui 6절) · 재개 판정 "이번 회차 propose 뒤" 5곳 · 옛 문구 grep 0(위 실측 목록) · report-fetch export 줄 = code-tab 1절.
13. **checklist**: v4.7 + 갱신 이력(회차 2·3·4) · [되돌리면 안 되는 것] 승인 가드·도장·ingest 두 행·deploy(X8·X9 불변식 포함)·비출력 시험·exclusions 요청 중단 행(ValueError 포함) · [의도된 동작] 9·19·22·26 · C③·C④.
14. **기록 정정**: 수정 기록 2(W14 — precheck 변이 행·"자격 증명 요청 0" 3곳) · 수정 기록 3(W12 "12개(+7)") · 구현 기록 "정정(검증 1)".
15. **다시 돌리지 않는 실측 대조**: 회차 1 네이버 시험 1건(registry 449행 deleted) · 회차 2 실제 자격 증명 1회(permissions.push 참) · 원격 스킬 main b4cc8b9·배포 32d8b05 불변 · main 작업 폴더 불변.
16. **의도 검증**: 임의 결정(회차 2 1~15 · 회차 3 1~23 · 회차 4 1~24) · "원래 지시를 바꾼 곳"(회차 2·3·4) — 지시 의도와 다른 구현이 있으면 그것만.

## 새로 내가 고를 항목
1. (이월) 병합과 10/1 · 병합 직후 main 작업 폴더 줄바꿈 정리 · `local/` 설치.
2. (보류 — 사용자 결정) 제안 ID 대조 · 토큰 범위 헤더.
3. (이월) 2-1 대조 명령화(회차 2) · NFKC·keep 처리 주체(점검 회차) · ingest `--from`·archive data/ 경로 차단(회차 2).
4. (리뷰 이월) `blocked_reason` 공백·기호 변형 대조(`twin_key`로 비교할지) — NFKC와 함께 점검 회차.
5. (리뷰 참고) 재개 판정의 "이번 회차" 한정을 코드로 강제할지(승인 파일에 창 이름을 넣는 등) — 지금은 문서 규칙.

## 마무리 기록(이번 회차)
- 커밋 ①(코드·시험·문서) + 커밋 ②(이 절·수정 기록 3 정정·checklist), `feat-code-tab`만 push(이 PC git 자격 증명). 재clone 대조는 보고에.
- 토큰 수령 0 · 네이버 0 · 배포 저장소 쓰기 0 · 실제 자격 증명 사용 0(push 제외) · main·main 작업 폴더 0 · 설치본 부트스트랩 불변.

---

# 수정 기록 3(Code 탭 회차 1 — 조정 재검토 W1~W14 반영, 2026-09-28)
세션: 데스크톱 앱 Code 탭(이 PC), Opus 5.5 — 수정 회차 2와 같은 세션이 조정 지시("수정 회차 3 …")를 받아 수정. 브랜치 **`feat-code-tab`**(`77a2ba8` 위 커밋 2개: ① 코드·시험·문서 ② 이 절·checklist — 자기 참조라 해시는 적지 않는다), **main 미반영**.
검증용 clone: `git clone -c core.autocrlf=false -b feat-code-tab --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill <별도 폴더>`
사용자 결정(조정): W1 후보 파일 출처 검사 채택 · W3 dry-run 무쓰기 채택 · W11 precheck 도장 채택 · 2-1 명령화는 회차 2, NFKC·keep은 점검 회차로 이월.
외부 쓰기: 스킬 저장소 = `feat-code-tab` push만 · 배포 저장소 = 무인증 읽기 GET만(리허설 fetch 1회·S0 1회) · 네이버 0 · 실제 fetch 0 · **실제 자격 증명 사용 0**(S0·배포 dry-run은 도우미 없는 임시 설정) · main·main 작업 폴더 0 · `D:\saero` 설치 0 · 토큰 수령 0.
효율: 벽시계 약 60분(20:41 지시 → 21:4x push) · 도구 호출 약 150회(조정자) + 반박 리뷰 워크플로 하위 에이전트 4 · 즉석 코드: 리허설 약 10행(S0 추출 2·입력 복사 1·CRLF 만들기 1·가짜 urlopen 러너 20행 중 판정 6) + 변이 실험 러너 약 190행(스크래치, 검증용 — 저장소 밖).
표기: [실측] 이 세션에서 직접 확인 / [추론] 확인 못 함. W = 조정 재검토 번호.

## W별 — 절·함수 기준
- **W1 승인 가드 우회 막기**(`scripts/exclusions.py`):
  (a) `build_approved` — "이미 registered" FAIL과 쌍둥이 `[주의]`를 **고른 이름 전부**에(옛 `extra and`·`not extra` 제거, 문구 "추가 이름" → "이름"). registered 판정 = `registered_everywhere(rows, k) or registration_status(rows, k)[0] == "registered"`(propose와 같은 기준 — `*` 기록·pending·비대상 그룹 행 포함). 쌍둥이 블록을 먼저 돌려 쌍둥이가 있을 때만 FAIL 문구에 "위 [주의] 참고".
  (b) 출처: `cmd_propose`가 `_candidates.txt`·`_industry.txt`의 md5를 `exclusions_proposal_<lo>_<hi>.md5`(`md5  파일명` 두 줄)에 쓴다. `check_provenance` — `--from-candidates`는 `_candidates.txt`, `--industry`는 `_industry.txt`로 끝나고 같은 폴더 `.md5`의 값 = 지금 파일 md5일 때만. 아니면 `[FAIL] [<옵션>] 후보 파일이 propose 산출물이 아님·propose 뒤 바뀜 — <사유>`.
  (c) 참조 모드에서 `blocked_reason`(금지 패턴·경쟁사)이 나오는 이름은 `[FAIL]`(승인 파일·POST에 들어가지 않음 — `[거부]`는 `--approved` dry-run에만 남음).
- **W2** `scripts/ingest.sh` 시작 검사: HEAD 확인 뒤·줄바꿈 검사 앞에 `git diff --quiet HEAD -- data` → 다르면 `[FAIL] data/가 HEAD와 다름(스테이징·미스테이징)` + `git status --short -- data`, exit 1(쓰기 0). 줄바꿈 검사 유지, awk = `-F'\t'` 탭 기준 경로 전체 · `w/` 빈 칸은 "(작업 폴더에 없음)" · 여러 줄은 들여써 한 줄씩. code-tab.md S0에 같은 diff 줄 + 같은 awk, 8절·4절 복구 명령 `git checkout HEAD -- data`.
- **W3** dry-run은 승인 파일을 쓰지 않는다(`[승인 목록] N개 = --expect N … — dry-run: 파일 안 씀`). 실제 push만 `api_from_args` 뒤·등록 전에 `approved_path()` = `work/approved_<날짜>_<시분초>.txt`(있으면 `_2`…, `open(…, "x")` — 덮어쓰기 없음). docstring·code-tab.md 1·3·6절·SKILL.md 5-0 4항·exclusion-ui.md 6·7절.
- **W4** `parse_numbers` `isdecimal()` · `read_name_file` 읽기·디코드 오류(OSError·UnicodeError) → `[FAIL] … 파일을 읽을 수 없음(<종류> — UTF-8이 아니거나 열 수 없음)` · `read_csv_terms` 같은 처리(+ csv.Error) · CSV 칸에 줄바꿈 → `[FAIL] 합본 CSV <파일>:<줄>에 줄바꿈이 든 칸이 있음`.
- **W5** `build_proposal`이 `n_rows`(창 안 행 수)를 돌려주고 `cmd_propose`가 `lo > hi` **또는 `n_rows == 0`**이면 `[주의] 빈 창(창 lo~hi 안 검색어 행 0 — --since·--day가 데이터 끝 뒤 등)`.
- **W6** `deploy.py` `--base`만(`--file` 없음) → `[FAIL] --base는 --file과 함께만` exit 2(요청 0). code-tab.md 9절 리허설 줄 = `deploy.py push --file work/index.html --base work/prev.html --dry-run`.
- **W7** `deploy.py` `api()` `mask()` — HTTPError 본문·URLError 문구에서 그 요청에 쓴 자격 증명 값을 `***`로(자르기 전에).
- **W8** PUT 409 = `[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치) — PUT 안 됨, 4단계부터 다시 할지는 사용자가 정한다` · 403 = `[FAIL] PUT 403 — 쓰기 권한 없음(…)` · 404 = `[FAIL] PUT 404 — 저장소·경로를 찾지 못함(… 권한이 없어도 404)` · 그 밖 `[FAIL] PUT <코드>`. code-tab.md 3·4·5절.
- **W9** `exclusions.py` `load_keys` — `api_key`·`secret_key`가 str·ASCII·공백 없음이 아니면 `SystemExit("키 파일의 <이름> 값 형식이 다릅니다(… — 값은 출력하지 않는다)")`.
- **W10** `tests/test_deploy.py` 자식 env: `GIT_`로 시작하는 변수 전부 제거 + `GIT_CONFIG_NOSYSTEM=1`·`GIT_CONFIG_GLOBAL`·`GIT_CEILING_DIRECTORIES=<임시 폴더의 부모>`.
- **W11** `scripts/precheck.sh` — 시작할 때 옛 도장 `rm -f`, 전부 통과하면 `$(dirname HTML)/precheck_ok.md5` = `<작업본 md5>  <파일명>`. `deploy.py` `precheck_stamp` — push에 `--file`이 있으면 네트워크 전에 도장 = `--file` md5인지: 실제 push면 아니면 `[FAIL] precheck 통과본이 아님 — PUT 안 함(<사유>)` exit 1, dry-run이면 `[주의]`. SKILL.md 6·7단계 · code-tab.md 1·3·4·5절 · checklist 행.
- **W12** 시험(새 파일 0): `test_exclusions` `TestApprovedReference` 12개(+7 — 수정 회차 4 정정: 종전 "13개"는 잘못 셈; 출처 기록 도우미 `stamp()`, 실제 push 파일 `approved_files()`) — 끝 마침표·앞뒤 공백 원문(실제 push 파일 바이트) · 두 번째 실제 push가 앞 파일을 안 덮음 · 쌍둥이 대소문자·후보 파일 안 쌍둥이 · 후보·`*` 기록·업종어 이름 registered FAIL · 금지 패턴·경쟁사명 FAIL(`[거부]` 없음) · 손으로 쓴 후보·md5 불일치·industry↔candidates 바꿔 넣기·.md5 없음 FAIL · `²`·UTF-16·CSV 칸 줄바꿈 FAIL · propose `.md5` 기록 + `--day` 빈 창 + propose → push 끝까지 · `load_keys` 형식.
  `test_deploy` 12개(+5, 리뷰 반영 1 포함): permissions 필드 없음 FAIL · 못 읽는 `--base`·`--base`만 exit 2·요청 0 · PUT 409·403 문구 + 되돌아온 헤더 값 `***` · 도장 없음·불일치 FAIL·요청 0, dry-run `[주의]` · (기존 시험에 도장 줄 단언).
  `test_ingest` 9개(+1): test_1 `origin/main = HEAD` 2회 · test_7을 **실제 상황**(속성 없던 커밋에서 CRLF로 풀린 CSV가 blob이 같아 안 바뀌어 `status`·`diff HEAD`는 깨끗, i/lf w/crlf — 공백 경로 포함)으로 · test_8 스테이징된 CRLF(i/crlf w/crlf라 줄바꿈 검사는 통과)·미스테이징 둘 다 diff FAIL + `git checkout HEAD -- data` 복구 · PrecheckTests 도장 = 작업본 md5, 실패 실행은 옛 도장 지움.
- **W13** 문서: "다시 계산" 흐름 4곳(SKILL.md 2-1 · code-tab.md 3절 · local/saero-run/SKILL.md · checklist 26)에 `5-0b(해당 시)` — 4곳 같은 문장(grep 각 1) · code-tab.md 5절 표(원천 없음·`--approved`와 함께·출처·registered·거부·CSV 줄바꿈·도장·409/403/404·`--base`만) · report-fetch.md 3절 export 줄 = 1절 전체 · SKILL.md 참고 목록 "승인 목록 참조 선택 모드" · exclusion-ui.md 3절 "번호 선택(승인 목록은 push가 씀)" · SKILL.md 1단계 ingest 설명에 시작 검사 3가지 · SKILL.md 4단계 폴백 `git clone -c core.autocrlf=false` · 권한 확인 = "계정 역할 기준 — 토큰 범위는 PUT이 최종 확인"(SKILL.md 배포 정보·7단계 · deploy.py docstring · checklist deploy 행 · code-tab.md 2절) · code-tab.md 4절 재시도 한 줄(같은 `--since`로 propose 다시 → 새 `_candidates.txt` → `--from-candidates … --expect <재승인 N>`).
- **W14** 이 절 아래 "수정 기록 2" 안에서 바로잡음: 변이 표 precheck 행(옛 판은 `python3` 고정 탓 — `$PY`로 고친 옛 흐름 변이가 실제 결함을 보임) · N2·N4·검증 2가 볼 것 10의 "자격 증명 요청 0" → "(무인증 GET이 403·429면 GET용 1회)" · checklist ingest 행 시험 열(끝 확인 = test_1 2회, "변경 없음" 분기 끝 확인은 코드만 — 실행 중 원격이 바뀔 때).

## 변경 파일(`77a2ba8` → 커밋 ①; `wc -l` · md5 앞 8자리) [실측]

| 파일 | 행수 | md5 |
|---|---|---|
| `scripts/exclusions.py` | 1179 → 1246 | a1fa8a73 → 27490231 |
| `scripts/deploy.py` | 232 → 283 | da626402 → ce49a0a2 |
| `scripts/ingest.sh` | 51 → 57 | 3e236b1e → b4da20a2 |
| `scripts/precheck.sh` | 26 → 30 | 9fbf78e2 → 54a869c7 |
| `tests/test_exclusions.py` | 693 → 864 | f518c75b → 584e183a |
| `tests/test_deploy.py` | 212 → 290 | 4865e5b3 → 56e75925 |
| `tests/test_ingest.py` | 274 → 356 | a899fa46 → cc3c82c2 |
| `SKILL.md` | 531 → 538 | 094d0ea7 → 7c231ccc |
| `references/code-tab.md` | 200 → 213 | 9609163b → e77c252f |
| `references/exclusion-ui.md` | 146 → 148 | 03564266 → 1aec4a88 |
| `references/report-fetch.md` | 112 → 112 | 529cbf26 → a03f0ef5 |
| `local/saero-run/SKILL.md` | 28 → 28 | a963e8eb → b80cd5ae |
| `audit/checklist.md`(커밋 ②) | 501 → 503 | b7519fe1 → 17a5f9ba |
| `audit/last-audit.md`(커밋 ②) | 이 절 + 수정 기록 2 정정 3곳 | (재clone 대조는 보고에) |

불변: `scripts/fetch_reports.py`·`archive.py`·`compute.py`·`validate.py`·`compare.py`·`reportlib.py` · `tests/test_fetch_reports.py`·`mutation_test.py`·`overflow_check.py` · config · data/ · registry(ca642639) · `local/CLAUDE.md` · `.gitattributes`·`.gitignore`.

## 임의 결정(수정 회차 3 번호)
1. **출처 기록 형식** = `md5sum` 형식 두 줄(`<md5>  <파일명>`), 파일 이름 = 제안서 md와 같은 `<창 이름>.md5`(`--out`을 주면 그 이름). 빈 후보 파일도 적는다.
2. **registered 판정** = `registered_everywhere or registration_status == "registered"` — 지시의 "propose와 같은 기준 포함"을 합집합으로(둘 중 하나면 FAIL).
3. **FAIL 문구의 "위 [주의] 참고"는 쌍둥이가 있을 때만**(리허설 (b)에서 쌍둥이 없는 FAIL에 붙어 있던 것을 고침 — 그래서 쌍둥이 블록을 FAIL 판정 앞으로 옮김).
4. **실제 push의 승인 파일은 `api_from_args` 뒤·`do_push` 앞에** 쓴다(키 파일 오류면 파일 없음, 등록 도중 실패해도 무엇을 보내려 했는지 남는다). 이름 = 로컬 시각 `%Y-%m-%d_%H%M%S`, 겹치면 `_2`부터.
5. **CSV 칸 줄바꿈은 파일 전체를 FAIL**(그 행만 빼지 않음 — 뒤 행 번호가 전부 어긋나므로).
6. **precheck 도장은 시작할 때 지우고 끝에서만 쓴다**(지시 밖 한 줄 — 실패한 재실행 뒤 옛 도장이 남으면 그 작업본이 통과본처럼 보인다). 도장은 작업본과 같은 폴더(`work/`)에 두고, deploy는 `--file`과 같은 폴더에서 읽는다.
7. **도장 검사 위치** = push에 `--file`이 있으면 GET보다 먼저(실제 push FAIL은 요청 0). dry-run의 `[주의]`도 같은 자리에서 한 줄.
8. **PUT 그 밖 코드**도 `[FAIL] PUT <코드>`로 통일(종전 "PUT <코드>: … 확인" 문구). 403·404 문구에 응답 message 앞 200자(`***` 가림 뒤).
9. `mask()`는 `api()`를 부른 그 요청의 자격 증명 값만 가린다(무인증 GET은 가릴 값 없음).
10. **ingest diff FAIL 때 `git status --short -- data`를 함께 찍는다**(무엇이 다른지 한 번에 보이게).
11. **test_7 재현법**: 임시 저장소에서 `.gitattributes`를 지운 커밋 → CSV를 지우고 `checkout`(autocrlf=true → CRLF) → 1.2초 쉬고 `status`(색인 stat 갱신) → `reset --keep HEAD~1`. 검증 1 10항(`clone -n` + 두 커밋 checkout)과 같은 상태(status 0줄, i/lf w/crlf).
12. **W10 짝 변이 시연**: 엉뚱한 `GIT_DIR`로는 `git credential fill`이 실패하지 않아(놓침 1건) 시연이 안 됐다 → 도우미 목록을 비우고(`credential.helper=` 빈 값) 다른 값을 주는 설정을 가진 저장소를 `GIT_DIR`로 → 옛 판은 그 값을 헤더에 싣고 실패, 새 판은 통과.
13. 참조 모드의 `[승인 목록] N개` 줄에 dry-run이면 "파일 안 씀(실제 push가 … 쓴다)"를 붙였다(세션이 파일을 찾지 않게).
14. (반박 리뷰 반영) **`--extra-csv` 출처 = 저장소 `work/combined/검색어.csv` 경로**(realpath·대소문자 무시 비교) — 손으로 쓴 CSV 하나로 실제 push·POST까지 가던 우회를 막는다. md5 기록 대신 경로로 한 것은 `--extra-csv`만 쓰는 경우(후보 0줄)에도 기준이 있게.
15. (리뷰) **deploy는 `--file`을 한 번만 읽는다** — 도장 대조 뒤 GET을 기다리는 사이 파일이 바뀌면 다른 본문이 PUT되던 것을 막는다(PUT 본문 = 도장 찍힌 바이트). 못 읽으면 `[FAIL] --file을 읽을 수 없음` exit 2(종전 Traceback).
16. (리뷰) **ingest 시작 검사에 추적 안 된 파일**(`ls-files --others --exclude-standard -- data`) — `git diff HEAD`는 못 보고 `git add data`는 커밋한다(store 부분 적용으로 남은 새 달 폴더 등).
17. (리뷰) **propose 재등록 후보에서 대상 그룹 전부 등록 확인된 이름을 뺀다**(`*` missing 기록만 남은 이름 — push가 "이미 registered"로 막는 이름을 propose가 내던 어긋남).
18. (리뷰) **test_ingest도 자식 env 정리**(`clean_env` — `GIT_*` 제거·시스템·전역 설정 끔, W10과 같은 방식). autocrlf는 임시 저장소 설정으로 켠다.
19. (리뷰) 문구: 출처 FAIL = `[FAIL] 후보 파일이 propose 산출물이 아님·propose 뒤 바뀜(<옵션>) — <사유>`(지시 문구를 `[FAIL]` 바로 뒤에) · 409 = 지시 문구 그대로 · deploy GET 실패 안내의 폴백 clone에 `-c core.autocrlf=false` · SKILL.md·exclusion-ui.md·checklist의 "`[거부]`" 설명을 참조 모드 FAIL로 · 빈 창 설명을 코드 조건대로 · local 진입 스킬 기본 순서에 5-0b · code-tab 5절 인용을 실제 출력 앞부분으로 · 7절에 `.md5`·도장 손으로 쓰기 금지 · 시험 docstring.
20. (리뷰) **data/가 HEAD와 다를 때의 되돌리기 = `git restore --source=HEAD --staged --worktree -- data`**(4절·ingest 메시지·S0 줄은 "4절") — `git checkout HEAD -- data`는 스테이징된 새 파일(ingest 커밋 실패로 남는 `A`)을 못 지워 FAIL이 계속 난다(리뷰 재현). 8절(줄바꿈 정리 — 추적 파일만)은 지시대로 `git checkout HEAD -- data`.
21. (리뷰) exit 128 판정·재개 판정에 "`git status --short -- data`가 빔"을 더했다(`== push data/` 뒤 128은 커밋 실패일 수도 — HEAD = origin/main인데 보관본 미완료).
22. (리뷰) `precheck_stamp`는 도장을 못 읽으면(UTF-8 아님 등) Traceback 대신 `도장을 읽을 수 없음(<종류>)`(실제 push FAIL·dry-run `[주의]`), 없으면 종전대로 `도장 없음`.
23. (리뷰) propose는 줄바꿈이 든 이름을 후보·업종어 파일에 쓰지 않고 "후보에서 뺀 것"에 사유와 함께(push의 CSV 칸 줄바꿈 FAIL과 같은 기준). test_ingest의 빈 전역 git 설정은 실행마다 새 임시 파일(`mkstemp` — 공용 이름이면 남은 내용이 설정이 된다).

## 원래 지시를 바꾼 곳과 이유
- W3 "실제 push만 `work/approved_<날짜>_<시분초>.txt`" → 같은 초에 두 번이면 `_2`를 붙인다("덮어쓰기 없음"을 코드로 — `open(…, "x")`).
- W11 "precheck가 전부 통과하면 도장" → **시작할 때 옛 도장을 지우는 줄을 더했다**(임의 결정 6).
- W12 "test_1이 origin/main = HEAD 두 번" → 첫 실행 출력에서 정확히 2회(`count == 2`) — 시작 검사·push 뒤.
- W12 "ingest 스테이징된 CRLF FAIL" → 미스테이징 CRLF도 같은 시험에서(둘 다 diff 검사가 잡는다). 기존 test_7(미스테이징 CRLF)은 diff 검사가 먼저 잡게 돼 **실제 상황(stat만 깨끗한 CRLF)** 재현으로 바꿨다 — 줄바꿈 검사의 짝 시험을 살리려고.
- W1(b) 출처 검사는 지시상 `--from-candidates`·`--industry`만 — 반박 리뷰가 `--extra-csv`(손으로 쓴 CSV)로 같은 우회가 된다는 것을 재현해 **경로 검사를 더했다**(임의 결정 14).
- W2 "`git diff --quiet HEAD -- data`" → 그 뒤에 **추적 안 된 파일 검사를 한 줄 더했다**(임의 결정 16 — diff가 못 보는 경로를 리뷰가 재현).
- W2 "8절 복구 명령 `git checkout HEAD -- data`" → 8절(줄바꿈 정리)은 그대로 두고, **diff FAIL의 되돌리기(4절·ingest 메시지)는 `git restore --source=HEAD --staged --worktree -- data`**로 — `checkout`은 스테이징된 새 파일을 남겨 FAIL이 반복된다(임의 결정 20, 리뷰 재현).
- W11 "도장 = --file md5일 때만 PUT" → deploy가 `--file`을 한 번만 읽게 바꿨다(임의 결정 15 — 두 번 읽으면 도장과 PUT 본문이 달라질 수 있음을 리뷰가 재현).
- 리허설 "precheck 통과 → 도장 → deploy push --file --base --dry-run(자격 증명 없는 설정 — 권한 줄 FAIL이 정상)" → 도우미가 없으면 권한 줄 전에 "자격 증명을 얻지 못함" FAIL이 먼저 난다(권한 조회까지 가지 않음 — 실제 자격 증명 0 조건).

## 실측 [실측]
- **시험**(스크래치 LF clone = 작업본 코드 md5 같음, venv, PYTHONUTF8 없이, `-W error::ResourceWarning`, test_deploy는 `GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`): 최종(리뷰 반영 뒤) test_exclusions **Ran 41 OK** · test_deploy **Ran 12 OK**(15초) · test_ingest **Ran 9 OK**(59초) · test_fetch_reports **Ran 15 OK**(81초) — `skipped` 0 · mutation_test **"전부 살아 있음"**(`  [OK]` 43, MISS·UNCOVERED·SKIP 0, 27초). 실제 registry(ca642639)·data·config md5 전/후 동일.
- **변이 실험 54/54 잡힘**(대조군 먼저 전부 OK · 복원 뒤 status 깨끗):

  | 변이(짝 시험 파일은 러너 표 — 스크래치 `mutate3.py`) | 결과 | 짝 시험 결과 |
  |---|---|---|
  | E808 push return 0 | 잡힘 | Ran 1 test in 0.028s FAILED (failures=1) |
  | E830 verify return 0 | 잡힘 | Ran 1 test in 0.040s FAILED (failures=1) |
  | E673a split_blocked 경쟁사 거부만 빠짐 | 잡힘 | Ran 2 tests in 0.012s FAILED (failures=1) |
  | E673b split_blocked 거부 전부 빠짐 | 잡힘 | Ran 1 test in 0.013s FAILED (failures=1) |
  | V1 합계≠N 검사 제거 | 잡힘 | Ran 1 test in 0.025s FAILED (errors=1) |
  | V1 이미 registered 검사 제거 | 잡힘 | Ran 1 test in 0.022s FAILED (failures=1) |
  | V1 K() 중복 검사 제거 | 잡힘 | Ran 1 test in 0.047s FAILED (errors=1) |
  | V1 범위 밖 검사 제거 | 잡힘 | Ran 1 test in 0.034s FAILED (failures=1) |
  | V1 쌍둥이 [주의] 제거 | 잡힘 | Ran 1 test in 0.024s FAILED (failures=1) |
  | V1 실제 push의 --approved 허용 | 잡힘 | Ran 1 test in 0.024s FAILED (failures=1) |
  | .gitattributes *.csv -text 줄 삭제 | 잡힘 | Ran 1 test in 6.896s FAILED (failures=1) |
  | .gitattributes 파일 삭제 | 잡힘 | Ran 1 test in 0.007s FAILED (errors=1) |
  | N3 시작 HEAD 검사 제거 | 잡힘 | Ran 3 tests in 22.188s FAILED (failures=3) |
  | N3 줄바꿈 검사 제거 | 잡힘 | Ran 1 test in 9.633s FAILED (failures=1) |
  | precheck.sh b4cc8b9 판 통째(python3 고정) | 잡힘 | Ran 1 test in 0.667s FAILED (failures=1) |
  | precheck 옛 흐름(compute && compare \| tail) + $PY | 잡힘 | Ran 1 test in 2.730s FAILED (failures=1) |
  | N2 base 대조 제거 | 잡힘 | Ran 1 test in 1.114s FAILED (failures=1) |
  | N2 --base 필수 제거 | 잡힘 | Ran 1 test in 1.109s FAILED (failures=1) |
  | N1 perm = True | 잡힘 | Ran 1 test in 1.076s FAILED (failures=1) |
  | V4 token_of 옛 판 | 잡힘 | Ran 1 test in 0.383s FAILED (errors=1) |
  | W1a registered 검사를 추가 이름만(옛 판) | 잡힘 | Ran 1 test in 0.027s FAILED (failures=1) |
  | W1a propose 기준(registration_status) 빠짐 | 잡힘 | Ran 1 test in 0.028s FAILED (failures=1) |
  | W1a 쌍둥이를 추가 이름만(옛 판) | 잡힘 | Ran 1 test in 0.026s FAILED (failures=1) |
  | W1b 출처 검사 끔 | 잡힘 | Ran 1 test in 0.023s FAILED (failures=1) |
  | W1b 접미사 검사 제거 | 잡힘 | Ran 1 test in 0.029s FAILED (failures=1) |
  | W1b md5 대조 제거 | 잡힘 | Ran 1 test in 0.030s FAILED (failures=1) |
  | W1b propose가 md5 기록을 안 씀 | 잡힘 | Ran 1 test in 0.045s FAILED (failures=1) |
  | W1c 참조 모드 거부 이름 FAIL 제거 | 잡힘 | Ran 1 test in 0.036s FAILED (failures=1) |
  | W3 dry-run도 승인 파일 씀 | 잡힘 | Ran 1 test in 0.030s FAILED (failures=1) |
  | W3 고정 이름 덮어쓰기(옛 판) | 잡힘 | Ran 1 test in 0.032s FAILED (failures=1) |
  | W4 isdecimal → isdigit | 잡힘 | Ran 1 test in 0.063s FAILED (errors=1) |
  | W4 후보 파일 읽기 오류를 안 잡음 | 잡힘 | Ran 1 test in 0.071s FAILED (errors=1) |
  | W4 CSV 칸 줄바꿈 검사 제거 | 잡힘 | Ran 1 test in 0.068s FAILED (failures=1) |
  | W5 빈 창을 lo > hi만 | 잡힘 | Ran 1 test in 0.039s FAILED (failures=1) |
  | W9 load_keys 형식 검사 제거 | 잡힘 | Ran 1 test in 0.019s FAILED (failures=1) |
  | W6 --base만(--file 없음) 허용 | 잡힘 | Ran 1 test in 1.660s FAILED (failures=1) |
  | 못 읽는 --base를 안 잡음 | 잡힘 | Ran 1 test in 0.927s FAILED (failures=1) |
  | W7 오류 문구 가림 제거 | 잡힘 | Ran 1 test in 1.103s FAILED (failures=1) |
  | W8 409 문구 제거 | 잡힘 | Ran 1 test in 1.093s FAILED (failures=1) |
  | W8 403 문구 제거 | 잡힘 | Ran 1 test in 1.824s FAILED (failures=1) |
  | permissions 필드 없음을 참으로 | 잡힘 | Ran 1 test in 1.076s FAILED (failures=1) |
  | W11 deploy 도장 검사 제거 | 잡힘 | Ran 1 test in 1.108s FAILED (failures=1) |
  | W11 precheck 도장 안 씀 | 잡힘 | Ran 1 test in 1.304s FAILED (errors=1) |
  | W11 precheck 옛 도장 안 지움 | 잡힘 | Ran 1 test in 2.336s FAILED (failures=1) |
  | W2 data/ HEAD diff 검사 제거 | 잡힘 | Ran 1 test in 6.946s FAILED (failures=1) |
  | W2 awk 옛 판($NF) | 잡힘 | Ran 1 test in 6.190s FAILED (failures=1) |
  | 리뷰 --extra-csv 출처(work/combined) 검사 제거 | 잡힘 | Ran 1 test in 0.034s FAILED (failures=1) |
  | 리뷰 deploy --file을 PUT 전에 다시 읽음(옛 판) | 잡힘 | Ran 1 test in 1.077s FAILED (failures=1) |
  | 리뷰 ingest 추적 안 된 파일 검사 제거 | 잡힘 | Ran 1 test in 9.745s FAILED (failures=1) |
  | 리뷰 propose 재등록 후보의 '전부 등록' 빼기 제거 | 잡힘 | Ran 1 test in 0.027s FAILED (failures=1) |
  | W12 원천 줄을 strip(앞뒤 공백 원문 훼손) | 잡힘 | Ran 1 test in 0.032s FAILED (failures=1) |
  | 리뷰 deploy 깨진 도장을 안 잡음 | 잡힘 | Ran 1 test in 2.852s FAILED (failures=1) |
  | 리뷰 propose 줄바꿈 든 이름 빼기 제거 | 잡힘 | Ran 1 test in 0.030s FAILED (failures=1) |
  | W10 옛 판(GIT_CONFIG*만 지움) + 호출 환경 GIT_DIR(다른 도우미) | 잡힘 | Ran 1 test in 1.032s FAILED (failures=1) |
  (W10은 처음에 엉뚱한 `GIT_DIR`로 시연해 "놓침"이었다 — `git credential fill`은 저장소 없이도 돈다. 도우미 목록을 비우고 다른 값을 주는 설정을 가진 저장소를 `GIT_DIR`로 준 시연으로 바꿨다: 새 판 통과·옛 판 실패. precheck 옛 판 통째는 `python3` 고정 탓 실패라 결함 시연이 아니다 — 같은 표의 "옛 흐름 + $PY"가 결함 시연.)

- **리허설**(20:58:46 → 약 21:10, 반박 리뷰와 겹쳐 진행, 스크래치 LF clone — 작업본 변경을 얹은 임시 main + 로컬 bare origin):
  S0 = 2절 블록 원문(14줄, 리허설 판 md5 b1bf3946 — 뒤에 FAIL 문구 한 곳("되돌리기는 8절" → "4절")만 바뀌어 최종 8fe73c95, `bash -n` OK, 치환 = cd·프로필 경로, 도우미 없는 임시 설정) → 배포 줄만 `[FAIL] 자격 증명을 얻지 못함` + `[FAIL] 배포 저장소 점검 실패(… rc=1)`, 새 diff 줄 포함 나머지 통과, ignored 0 →
  ingest 정상(시작 검사 → 33일 9,991/309/351,299원 PASS → push → `origin/main = HEAD` 시작·끝 2회) → **스테이징된 CRLF**(`data/2026-08/키워드.csv`, `i/crlf w/crlf`) → `[FAIL] data/가 HEAD와 다름` + `M  data/2026-08/키워드.csv`, rc 1·HEAD 불변 → `git checkout HEAD -- data`로 status 0 →
  deploy fetch 무인증(sha 1c52f70, md5 a3465ec0) → compute → propose `--since 2026-09-27` = `.md5` 기록 2줄 →
  (a) 후보 그대로 → 통과 + 쌍둥이 `[주의]`(registry 200·421·644행) + "dry-run: 파일 안 씀" / (b) 손으로 쓴 `hand_candidates.txt`(`노원힐링장소`) → `[FAIL] [--from-candidates] 후보 파일이 propose 산출물이 아님·propose 뒤 바뀜 — 출처 기록 …hand.md5을(를) 읽을 수 없음`(당시 문구 — 리뷰 뒤 `[FAIL] 후보 파일이 … 바뀜(--from-candidates) — …`) + `이미 registered` FAIL / (c) `.md5` 치운 뒤 → 출처 FAIL / (d) `--extra-rows 1164` → `이미 registered` FAIL(쌍둥이 1165 나란히) / (e) `--extra-rows 1165` → 통과 + `[주의]`. HTTP 0(프록시 127.0.0.1:9), registry ca642639 전후 같음, `approved_*` 0개 →
  precheck(작업본 = 배포본 + 주석 1줄) 22 PASS · 95 / DIFF 0 · 넘침 0 · 외부 요청 차단 6건 → `== 6단계 전부 통과 — 도장 work/precheck_ok.md5(작업본 md5 523a52b6…)`(= `md5sum` 값) →
  deploy `push --file --base --dry-run`(도우미 없음) → "precheck 도장 = 작업본 md5 523a52b6… 확인" · "배포본 = --base md5 a3465ec0… 확인" · `[FAIL] 자격 증명을 얻지 못함(출처: git)` rc 1 →
  작업본 1바이트 덧붙임 → 실제 push 경로(가짜 urlopen) `[FAIL] precheck 통과본이 아님 — PUT 안 함(도장 md5 523a52b6 ≠ 작업본 md5 c1f75f1f …)` rc 1, **가짜 urlopen 호출 0건** / 같은 파일 dry-run은 `[주의]`만.
- **전후**: 스킬 저장소 `ls-remote` HEAD·main b4cc8b9 · feat-code-tab 77a2ba8(push 전) · test* 0 · 배포 32d8b05 · main 작업 폴더 HEAD b4cc8b9·status 0·md5 4dd3b0cf · `~/saero-fetch/downloads` 목록 ed69f294 같음.
- **반박 리뷰**(워크플로 `saero-r3-review`, 하위 에이전트 4 — 지시 준수·쓰기 안전·셸/엣지·문서=코드, 읽기 전용·스크래치 실행, 23분·도구 212회): 30건(high 0 · medium 5 · low 25 — 관점끼리 겹친 것 포함).
  medium 5 = `--extra-csv` 손으로 쓴 CSV로 실제 push·POST(→ 임의 결정 14) · deploy가 `--file`을 두 번 읽어 도장과 다른 본문 PUT(→ 15) · 문서 되돌리기 명령이 스테이징된 새 파일을 못 지움(→ 20) · deploy GET 실패 안내의 폴백 clone · code-tab 5절 인용이 실제 출력과 다름(→ 19). 코드 결함은 재현 뒤 반영하고 짝 변이를 더했다.
  low는 반영(임의 결정 16~23·문서) 또는 고를 항목 2·5·6·7(지시 밖·추론).
- **grep 잔존**: `approved_<날짜>.txt`(시분초 없는) 0 · "추가(후보 밖) 이름이 이미" 0 · "이미 모든 대상 그룹 registered" 0 · `git checkout -- data` 0 · `print $NF` 0 · "다시 계산" 흐름 옛 문장(5-0b 없음) 0 · `--dry-run --base`(`--file` 없는 리허설 줄) 0 · "쓰기 권한은 첫" 0. 새 흐름 문장 4곳 각 1.
- **문법**: py_compile 14/14 · `bash -n` ingest·precheck·S0 블록 · 코드펜스 짝수(SKILL 16 · code-tab 4 · report-fetch 8 · exclusion-ui 2 · checklist 6 · local 0) · 변경 파일 14개 UTF-8 · CR 0.

## 검증 2가 볼 것(수정 기록 2의 16항목 중 바뀐 것 + W)
1. **변경 파일 = W 범위**: `git diff 77a2ba8 --stat` = 위 표 + last-audit.md·checklist.md. 불변 줄 md5.
2. **시험 4종 + mutation_test**(venv, PYTHONUTF8 없이, LF clone, test_deploy는 `GIT_CONFIG_NOSYSTEM=1`·빈 `GIT_CONFIG_GLOBAL`): 41 · 12 · 9 · 15 OK(skipped 0), "전부 살아 있음".
3. **변이 실험**: 위 표 54쌍 중 최소 W1 여섯·W3 둘·W11 셋·W2 둘·W10(다른 도우미 GIT_DIR)·precheck 옛 흐름 `$PY`에서 짝 시험이 실패하는지(수정 기록 2 3항 대체).
4. **W1 CLI 재현**(수정 기록 2 4항 대체): propose `--since 2026-09-27` → `.md5` 2줄 → (a)~(e) 위 리허설과 같은 결과, 승인 파일 0·HTTP 0·registry 불변. 손으로 `.md5`까지 같이 만들면 통과한다는 한계(아래 고를 항목 2).
5. **V2 흐름 4곳**(수정 기록 2 5항 갱신): "다시 계산" 흐름에 `5-0b(해당 시)`, 4곳 글자 대조.
6. **W2**: 스테이징된 CRLF·미스테이징 → `[FAIL] data/가 HEAD와 다름`(쓰기 0), stat만 깨끗한 CRLF → 줄바꿈 FAIL(공백 경로 전체), data/에 추적 안 된 파일 → `[FAIL]`, S0 블록 같은 두 줄, 되돌리기 4절 `git restore --source=HEAD --staged --worktree -- data`(스테이징된 새 파일까지) · 8절(줄바꿈) `git checkout HEAD -- data`.
7. **W3**: dry-run 뒤 `work/approved_*` 0, 실제 push(가짜 API)만 `approved_<날짜>_<시분초>[_n].txt`, 두 번째가 앞 파일을 안 덮음.
8. **W4·W5·W9**: `²`·UTF-16 후보 파일·CSV 칸 줄바꿈 → `[FAIL]`(Traceback 0) · `--day`가 데이터 끝 뒤면 `[주의] 빈 창` · 키 값 형식 SystemExit에 값 0.
9. **W6~W8**(수정 기록 2 10항 갱신): `--base`만·못 읽는 `--base` exit 2·요청 0 · 되돌아온 헤더 값 `***` · 409·403·404 문구.
10. **W10**: 호출 환경 `GIT_*`(GIT_DIR 등)가 자식에 안 넘어가는지.
11. **W11**: precheck 통과 → 도장 = 작업본 md5, 실패 재실행 → 도장 없음 · 도장 없음·불일치 → 실제 push FAIL·요청 0, dry-run `[주의]`.
12. **W13 문서**: 5절 표 새 줄 · report-fetch export · 권한 문구 3곳 · 재시도 한 줄 · 폴백 clone.
13. **W14**: 수정 기록 2 변이 표 precheck 행 정정·"자격 증명 요청 0" 정정 3곳 · checklist ingest 행 시험 열.
14. **checklist**: 승인 가드 행(고른 이름 전부·출처 md5·거부 FAIL·dry-run 파일 0) · precheck 도장 행(신규) · ingest 두 행 · deploy 행 · 26 흐름 · 갱신 이력 한 줄(v4.7 유지).
15. **의도 검증**: 임의 결정 1~23·"원래 지시를 바꾼 곳" 전부(리뷰 반영으로 지시보다 넓힌 곳 — `--extra-csv` 출처·추적 안 된 파일·`--file` 한 번 읽기·되돌리기 명령).
(수정 기록 2의 1·6·7·8·11~14·16항은 그대로 유효 — 이번에 바뀐 것은 위 항목으로 대체.)

## 새로 내가 고를 항목
1. (이월) 병합과 10/1 · 병합 직후 main 작업 폴더 줄바꿈 정리(S0·ingest 시작 검사가 멈춘다) · `local/` 설치.
2. **출처 검사의 한계**: `.md5`는 같은 폴더의 평문 기록이라 세션이 후보 파일과 `.md5`를 **둘 다** 손으로 만들면 통과한다(막는 것은 "모르고 손으로 쓴 파일·propose 뒤 바뀐 파일"). 더 막으려면 propose 출력에 md5를 찍고 사용자 답에 그 앞 8자를 받게 하거나, `.md5`를 registry처럼 커밋할지.
3. **권한 확인을 실제 push 직전에도**(수정 기록 2 고를 항목 5 그대로).
4. **ingest diff FAIL 때 자동 되돌리기는 하지 않는다**(지금은 보고만 — `git restore --source=HEAD --staged --worktree -- data`는 사용자와).
5. **(리뷰 — 추론, 지시 밖이라 안 고침)** 도장에 직전 배포본(`--base`) md5도 묶을지: 7단계 `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` 뒤 세션이 `prev.html`만 다시 받고 6단계를 건너뛰면 도장·base 대조가 둘 다 통과한다(문서는 "4단계부터 = 5·6·7 다시").
6. **(리뷰 — 추론)** exclusions.py 오류 문구의 `X-API-KEY` 가림(W7은 deploy만): 서버가 요청 헤더를 되돌려 주면 `[FAIL] … 400: {…}`에 키 값이 찍힐 수 있다(네이버가 실제로 되돌리는지는 미확인).
7. **(리뷰 — 추론)** `--pending`으로 통과한 precheck도 같은 도장을 쓴다 — 도장에 모드를 적어 실제 push가 `--pending` 통과본을 거부할지.
8. (이월 — 지시대로) 2-1 대조 명령화는 회차 2, NFKC·keep은 점검 회차.

## 마무리 기록(이번 회차)
- 커밋 ①(코드·시험·문서) + 커밋 ②(이 절·수정 기록 2 정정·checklist), `feat-code-tab`만 push(이 PC git 자격 증명). 재clone 대조는 보고에.
- 토큰 수령 0 · 네이버 0 · 배포 저장소 쓰기 0 · 실제 자격 증명 사용 0(push 제외) · main·main 작업 폴더 0 · 설치본 부트스트랩 불변.

---

# 수정 기록 2(Code 탭 회차 1 — 검증 1·조정 재확인 반영, 2026-09-28)
세션: 데스크톱 앱 Code 탭(이 PC), Opus 5.5 — 회차 1 구현과 같은 세션이 조정 지시("수정 회차 2 …")를 받아 수정. 브랜치 **`feat-code-tab`**(`df658f3` 위 커밋 2개: ① 코드·시험·문서 ② 이 절·checklist — 자기 참조라 해시는 적지 않는다), **main 미반영**.
검증용 clone: `git clone -c core.autocrlf=false -b feat-code-tab --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill <별도 폴더>`
사용자 결정(조정): 승인 목록 가드를 회차 2에서 이번으로 당긴다 · 실제 push는 참조 선택 모드만 · N1~N4 채택 · 회차 2에는 `ingest --from`·archive data/ 경로 차단만 남긴다. 근거 = `D:\saero-verify\saero-ad-report_검증_Code탭_2026-09-28.md`(검증 1) 결론 1~18 + 조정 N1~N4.
외부 쓰기: 스킬 저장소 = `feat-code-tab` push만 · 배포 저장소 = 읽기 GET만(무인증 contents + 사용자 승인 1회 인증 `/repos` — 20:08) · 네이버 0(시험 등록 재실행 안 함) · 실제 fetch 0 · main·main 작업 폴더 0 · `D:\saero` 설치 0 · 토큰 수령 0.
효율: 벽시계 약 55분(19:31 지시 → 20:2x push, 사용자 승인 대기 1회 포함) · 도구 호출 약 160회 · 즉석 코드: 리허설 약 7행(2-1 대조 4·S0 추출 2·입력 복사 1) + 변이 실험 러너 약 115행(스크래치, 검증용 — 저장소 밖). 리허설 기계 단계 약 12회·11분(시험 백그라운드·승인 대기 포함).
표기: [실측] 이 세션에서 직접 확인 / [추론] 확인 못 함. V = 검증 1 결론 번호, N = 조정 추가.

## V·N별 — 절·함수 기준
- **V1 승인 목록 가드(코드)** — `scripts/exclusions.py`: `push` 참조 선택 모드 `--from-candidates <_candidates.txt> [--drop 줄,…] [--industry <_industry.txt> --industry-lines 줄,…] [--extra-csv <합본 검색어.csv> --extra-rows 행,…] --expect N`.
  `build_approved`(원천 읽기·출처 출력·`뺀 것:`·FAIL 모음·쌍둥이) + `read_name_file`(줄 끝 CR·LF만 떼고 원문) · `read_csv_terms`(csv 모듈, `검색어` 칸만, 파일 줄 번호 = `line_num`) · `pick_lines`(범위 밖) · `parse_numbers` ·
  `registered_everywhere`(= `dry_run_plan` 등록 예정 0) · `twin_key`(글자·숫자만 + 대문자) · `registry_line_index`(쌍둥이 registry 줄 번호) · `approved_path`(`work/approved_<날짜>.txt`, LF). `cmd_push`: 참조 모드면 FAIL 전부 찍고 쓰기 0으로 멈춤,
  통과면 승인 파일을 쓰고 기존 흐름(거부 → dry-run 계획 | pull → POST → verify). `--approved`는 dry-run 전용(실제 push면 `[FAIL]` exit 1), 둘 다 주면·원천 없으면 `[FAIL]`. `cmd_propose`가 `_industry.txt`(업종어 포함 이름, 한 줄 하나)도 쓴다.
  문서: code-tab.md 6절 전면(인라인 복사 스크립트 삭제 → 옵션 사용법·FAIL·쌍둥이·9/28 사례) · 3절 5-0c 행 · 4절 멈춤 행 · 5절 exit 표 · 7절 금지 · SKILL.md 5-0 명령·4항 · exclusion-ui.md 3절(원칙·명령)·6절 3항·7절(dry-run·가드) · checklist [되돌리면 안 되는 것] 승인 목록 행 교체.
- **V2 2-1·"등록은 나중에"** — 같은 문장 4곳: SKILL.md 2-1(질문 인용에 "미룬 등록만" 선택지 한 줄 + 흐름 한 문장) · code-tab.md 3절 "2-1 같음" 문단(:83-86, 표 2-1 행은 여기로) · local/saero-run/SKILL.md :24-26 · checklist [의도된 동작] 26.
  propose `--since` 규칙(기본 = 직전 배포 masthead 끝 + 1일, 직전 회차가 "등록 미룸"이면 그 회차 창 시작 lo) = SKILL.md 5-0·code-tab.md 5-0a 행 · 8단계 양식에 `propose 창 lo~hi · 등록 미룸(사용자)` 줄(SKILL.md·code-tab.md 8 행) ·
  예외 문단(SKILL.md 승인 지점 · code-tab.md 3절). 코드: `cmd_propose` 파일명 `exclusions_proposal_<lo>_<hi>` · lo > hi면 `[주의] 빈 창(--since > 데이터 끝)`. 문서의 `<창끝>` 단독 표기 0(grep).
- **V3** `fetch_reports.py` `click_allowed` 금지 차단 메시지 괄호 → 지시 문구 그대로(강제 캡처는 넣지 않음) · code-tab.md 4절 행 · report-fetch.md 5절 행 = "메시지의 동작·요소 문구 · 재실행 전에 `partial/<날짜>/` · `--debug` 없이 `debug/`면 앞 보고서 실패 컷".
- **V4** `deploy.py` `token_of`: 바이트로 읽어 FF FE·FE FF면 UTF-16, 아니면 utf-8-sig, `OSError·UnicodeError` → None → 기존 `[FAIL] 자격 증명을 얻지 못함(출처: token-file)`. docstring 20~22행 = "요청 예외는 종류만(네트워크 연결 오류만 소켓 사유 문구 — 헤더 값 없음)". reason 출력 코드 그대로.
- **V5** code-tab.md 2절: 제목·본문 "외부 쓰기·작업 트리 변경 0(git이 `.git` 안 …, 파이썬이 `__pycache__` …)" · export 줄 `PYTHONDONTWRITEBYTECODE=1`(1절·2절·local) · 53행 = rc를 받아 `[FAIL] 배포 저장소 점검 실패(deploy.py push --dry-run rc=$r) — 원인은 바로 위 줄(GET = 조회 / 자격 증명 / 권한 / 파이썬)`(`tail -3`) ·
  5절 표: precheck(`[FAIL] 파이썬을 실행할 수 없음` · compute·overflow 예외는 `[FAIL]` 없이 Traceback — 마지막 `==` 줄이 멈춘 단계 · exit 2 사용법), ingest 128(`fatal:` — `== push data/` 뒤면 git fetch 뒤 HEAD = origin/main으로 다시 판정), exclusions·deploy 새 FAIL 줄.
- **V6** `tests/test_exclusions.py` `TestApprovedReference` 5개: CLI `main([... push --from-candidates …])` + FakeSender(drop_after_post) → rc 1·"실패/미확인 3", 이어 `verify --approved` rc 1(대조: 정상이면 0) · 참조 모드 출처·LF·쌍둥이 · 9/28 유형 FAIL · 합계·범위·빈·없음·중복·짝 옵션 FAIL(dry-run·실제 둘 다, 쓰기 0) · `--approved` 실제 push FAIL. `test_push_dry_run_zero_http_and_no_file_change` 승인 목록에 `젠필라테스노원점` → `[거부] … 경쟁사명 '젠필라테스'` 단언.
- **N1** `deploy.py` `push_permission_ok`(인증 GET `REPO_API` = `/repos/{deploy_repo}`, `permissions.push` 참/거짓만, 거짓·필드 없음·조회 실패는 `[FAIL]`) — `push --dry-run` 두 경로(`--file` 없음 = S0 · 있음 = 7단계). `api(url=…)` 인자 추가.
- **N2** `deploy.py` `--base`: 인자 검사(실제 push에 없으면 exit 2 · 못 읽으면 exit 2) → GET 본문 md5 ≠ base면 `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` exit 1(자격 증명 요청 0(무인증 GET이 403·429면 GET용 1회) · PUT 0 — 수정 회차 3 정정), 같으면 "배포본 = --base … 확인". SKILL.md 7단계·code-tab.md 3절 7행 명령에 `--base work/prev.html`.
- **N3** `scripts/ingest.sh` 시작 검사(store 전): `synced "시작 전 — store 전에 멈춤(쓰기 0) …"` · `ls-files --eol -- 'data/*.csv'` i/ ≠ w/면 `[FAIL] data/ CSV 줄바꿈이 커밋과 다름`. 두 분기의 끝 확인은 그대로.
- **N4** `tests/test_deploy.py`(신규 7): 자식 파이썬 + urlopen 가짜 + 가짜 도우미(`GIT_CONFIG_NOSYSTEM=1`·`GIT_CONFIG_GLOBAL`) — 값 출력 0(stdout·stderr, 전체·가운데 조각)·헤더에만 실림 · dry-run PUT 0 · base 불일치 FAIL·PUT 0·자격 증명 요청 0(무인증 GET이 403·429면 GET용 1회 — 수정 회차 3 정정) · `--base` 없음 exit 2·요청 0 · 권한 거짓·401 FAIL · 도우미 없음 FAIL · token_of UTF-16LE/BE·BOM·깨짐·없음(CLI Traceback 0).
  `tests/test_ingest.py`: 임시 저장소 `core.autocrlf=true` · test_5 CRLF 입력 → 원격 blob = 입력 · test_6 원격 앞섬 · test_7 줄바꿈 ≠ 커밋(둘 다 store 전 FAIL·HEAD 불변·data/2026-09 없음·스테이징 0) · test_3 두 번째 실행 기대 = 시작 검사에서 멈춤 · `PrecheckTests`(compute만 실패하는 sh 래퍼 → rc ≠ 0·"전부 통과" 없음, 통과 래퍼 대조군 rc 0).
- **V9~V15** 이 절 아래 "기능 추가 구현 기록" 절 안 "정정(검증 1)" 블록 + checklist 22.
- **V16~V18** docstring `python3` → `"$PY" scripts/…`(archive 2 · compare · compute · validate 2 · mutation_test · test_fetch_reports · test_exclusions) · fetch_reports.py 모드 줄(PowerShell·`python scripts\\` → Git Bash `$PY`) · archive.py 전제(프리셋 한 달 한 파일, 옛 "30일 제한"은 직접 입력 기간 — `--chunk` 폴백 설명도 SKILL.md와 같게) · test_exclusions 주석 · SKILL.md 6단계 md5 가드 인용 = `"[FAIL] 직전 배포본이 작업본과 같다 — …"` · report-fetch.md 1절 3.14 대처(playwright·venv 둘 다 `py -3.12`, 실행은 `$PY`).

## 변경 파일(`df658f3` → 커밋 ①; `wc -l` · md5 앞 8자리) [실측]

| 파일 | 행수 | md5 |
|---|---|---|
| `SKILL.md` | 515 → 531 | 8d63300e → 094d0ea7 |
| `references/code-tab.md` | 184 → 200 | 233bac4d → 9609163b |
| `references/exclusion-ui.md` | 139 → 146 | ec88e02d → 03564266 |
| `references/report-fetch.md` | 111 → 112 | bb9a5606 → 529cbf26 |
| `local/saero-run/SKILL.md` | 25 → 28 | b212888c → a963e8eb |
| `scripts/exclusions.py` | 949 → 1179 | 5b06e469 → a1fa8a73 |
| `scripts/deploy.py` | 182 → 232 | feaf5ba6 → da626402 |
| `scripts/ingest.sh` | 44 → 51 | 26953e48 → 3e236b1e |
| `scripts/fetch_reports.py` | 976 → 977 | a14766bc → 45d4fe44 |
| `scripts/archive.py` | 202 → 204 | e8fb93fc → c414a51a |
| `scripts/compare.py` · `compute.py` · `validate.py` | 181 · 251 · 424(행수 그대로) | 3184d1b7 → fc8acad1 · f2cd7f2d → 09b7039b · dd00bb11 → ec1158cf |
| `tests/test_exclusions.py` | 553 → 693 | 635a2d60 → f518c75b |
| `tests/test_ingest.py` | 167 → 274 | 7c2d6415 → a899fa46 |
| `tests/test_deploy.py`(신규) | 212 | 4865e5b3 |
| `tests/mutation_test.py` · `test_fetch_reports.py` | 379 · 604(행수 그대로) | 0a9dc9dc → 9d1b3bf2 · e0dc0695 → 0938a43e |
| `audit/checklist.md`(커밋 ②) | 497 → 501 | fdcb2027 → b7519fe1 |
| `audit/last-audit.md`(커밋 ②) | 이 절 + 정정 블록 | (재clone 대조는 보고에) |

불변: `scripts/precheck.sh`(9fbf78e2) · `scripts/reportlib.py` · config · data/ · registry(`audit/exclusions.csv` ca642639) · `local/CLAUDE.md` · `.gitattributes` · `.gitignore` · `tests/overflow_check.py`.

## 임의 결정(수정 회차 2 번호 — 사용자가 바꿀 단위)
1. **dry-run도 `work/approved_<날짜>.txt`를 쓴다**(참조 선택 모드) — 세션이 dry-run 뒤 그 파일을 사용자에게 보일 수 있게. "HTTP 0·registry 변경 0"은 그대로(문서 문구를 그렇게 한정).
2. **"추가(후보 밖) 이름" = `--industry`·`--extra-csv`에서 온 이름 전부.** "이미 모든 그룹 registered" FAIL과 쌍둥이 `[주의]`는 이 이름에만(지시 범위) — 후보 파일 이름은 propose가 방금 판정한 것이라 보지 않는다.
3. **쌍둥이 키** = `[\W_]+` 제거 + 대문자(한글·영문·숫자만 남김). 후보 파일 쌍둥이 검색은 뺀 줄까지 전체 줄, registry는 줄 번호·상태 개수로 보인다(최대 4곳 + "외 n").
4. **`--extra-rows` = 파일 줄 번호**(csv `line_num` — `grep -n`·`cat -n`과 같음). 1행 기간 헤더·2행 컬럼 줄은 범위 밖. 원천 줄은 줄 끝 CR·LF만 떼고 원문(앞뒤 공백도 유지), 빈 줄은 이름 아님, `#`은 특별 취급 안 함(`read_approved`와 다름).
5. **FAIL은 모아서 한 번에**, 출처 목록·`뺀 것:`·`[주의]`는 FAIL이어도 먼저 찍는다. 참조 모드 FAIL·`--approved` 실제 push·원천 없음·둘 다 줌은 전부 exit 1(`[FAIL]` 줄).
6. `_industry.txt` 순서 = 제안서 업종어 절 순서(노출 내림차순). propose 파일은 종전처럼 텍스트 모드(Windows CRLF) — 읽는 쪽이 CR을 뗀다.
7. **N2 base 대조 = PUT에 쓸 sha를 준 그 GET 본문**(PUT 직전 GET을 하나 더 보내지 않는다 — 같은 응답의 sha로 PUT하므로 그 뒤 변경은 GitHub가 sha 불일치로 막는다). dry-run도 `--base`가 있으면 대조, 없으면 안내 한 줄.
8. **N1 권한 확인은 dry-run 두 경로만**(실제 push에는 넣지 않음 — PUT 결과가 곧 확인). `permissions` 필드가 없으면 "거짓"으로 `[FAIL]`, 조회 실패는 따로 `[FAIL]`(응답 message 앞 120자 — 헤더 값 아님).
9. `--base` 없음(실제 push)·못 읽음 → **exit 2**(인자 오류 칸).
10. **ingest 시작 검사 순서** = 브랜치 → fetch·HEAD → 줄바꿈 → store. "data/ 변경 없음" 분기의 끝 확인은 남겼다 — test_3 두 번째 실행은 이제 시작 검사에서 멈춘다(그 분기 단독 시험은 원격이 실행 중에 바뀌는 경우뿐이라 두지 않음).
11. **test_ingest 임시 저장소 `core.autocrlf=true`**(시스템 설정과 무관하게 `.gitattributes` 효과를 본다). precheck 시험은 지시대로 test_ingest.py 안 `PrecheckTests` — PY 래퍼는 sh 스크립트(validate·compare·overflow 가짜 통과, compute만 실패) + 통과 대조군.
12. **test_deploy는 자식 파이썬 + runner**(urlopen 바꿔 끼움)로 실제 fd의 stdout·stderr를 잡는다. 값이 Authorization 헤더에 실렸는지도 단언(빈 시험 방지), 도우미 없음·token 파일 CLI 경로 포함.
13. 문구: deploy `--file` 없는 dry-run 줄 "자격 증명·쓰기 권한만 확인" · 참조 모드 FAIL "(… — 위 [주의] 참고)" · archive docstring "업로드 파일" → "수집 파일" · SKILL.md 참고 목록(push 참조 모드·ingest 시작 검사·deploy `--base`·test_deploy).
14. 지시 목록 밖 같은 뜻 맞추기: checklist [의도된 동작] 19(승인 목록 = 줄·행 번호) · 대상 파일 목록에 test_deploy · 검증 C④에 CLI exit · code-tab.md 4절 멈춤 행 5개·7절 금지 2줄·9절 리허설 순서·6절 "후보 0줄이면 `--from-candidates` 빼기".
15. SKILL.md 2-1 질문 인용에 셋째 선택지 한 줄("직전 회차 기록이 '등록 미룸'일 때만 덧붙인다").

## 원래 지시를 바꾼 곳과 이유
- V2 "SKILL.md 2-1(168행 뒤 한 문장)" → 한 문장 + **질문 인용에 선택지 한 줄**(임의 결정 15) — 질문에 "미룬 등록만"이 없으면 사용자가 그 답을 고를 수 없다.
- V6 "FakeSender로 CLI `main([... push ...])`" → **참조 선택 모드로** 불렀다 — 이번 V1로 실제 push의 `--approved`가 금지됐다.
- N2 "PUT 직전 GET 본문" → **PUT sha를 준 GET 본문**(임의 결정 7).
- V5 "compute·overflow 실패는 [FAIL] 줄 없이 Traceback" → **"예외로 끝나면"**으로 한정 — overflow는 넘침이면 `[FAIL] 360px …` 줄을 낸다.
- N4 ".gitattributes를 지우면 실패해야" → 파일 삭제는 시험 setUp 복사에서 error로 먼저 멈추므로, **`*.csv -text` 줄만 지운 변이도** 돌려 단언이 잡는 것을 보였다(둘 다 실패).
- 리허설 "S0 → …(권한은 실제 자격 증명 1회)" → **S0는 도우미 없는 임시 설정(`GIT_CONFIG_NOSYSTEM=1`·`GIT_CONFIG_GLOBAL`)으로** 돌렸다(배포 줄 FAIL이 정상) — N1 뒤 S0의 배포 줄도 인증 GET을 보내므로, 실제 자격 증명 사용을 7단계 1회로 맞추려고.

## 실측 [실측]
- **시험**(스크래치 LF clone — 코드 파일 md5가 작업본과 전부 같음, venv, PYTHONUTF8 없이, `-W error::ResourceWarning`): test_exclusions **Ran 34 OK** · test_deploy **Ran 7 OK**(8초) · test_ingest **Ran 8 OK**(44초) · test_fetch_reports **Ran 15 OK**(79초) ·
  mutation_test(배포본 = 무인증 재수령 sha 1c52f70·md5 a3465ec0, 합본 33일) **"전부 살아 있음"** · `  [OK]` 43줄 · MISS/UNCOVERED/SKIP 0 · 원본 md5 동일. 끝 줄 실제 registry(ca642639)·data·config md5 전/후 동일.
- **변이 실험**(짝 시험만, 스크래치에서 바꾸고 `git checkout`으로 복원 — 복원 뒤 status 깨끗, 대조군 3파일 먼저 OK): **19/19 잡힘**

  | 변이 | 짝 시험 | 결과 |
  |---|---|---|
  | exclusions `cmd_push` `return 1 if nfail else 0` → `return 0`(검증 1의 :808) | test_cli_push_and_verify_exit_1_when_not_verified | 실패 |
  | exclusions `cmd_verify` `return 1 if n else 0` → `return 0`(:830) | 같은 시험 | 실패 |
  | `split_blocked` 경쟁사 거부만 빠짐(:673) | test_push_dry_run_zero_http_and_no_file_change(+ test_blocked_reason은 통과 — 새 단언이 잡음) | 실패 |
  | `split_blocked` `why = None`(:673) | test_push_dry_run_zero_http_and_no_file_change | 실패 |
  | V1 합계 ≠ N 검사 제거 / K() 중복 검사 제거 | test_sum_range_empty_missing_duplicate_fail_before_writing | 실패(error — 가드가 없으면 비-dry-run 경우가 `api_from_args`까지 간다) |
  | V1 "이미 모든 그룹 registered" 제거 | test_9_28_type_extra_row_already_registered_everywhere_fails | 실패 |
  | V1 범위 밖 검사 제거 | test_sum_range… | 실패 |
  | V1 쌍둥이 `[주의]` 제거 | test_builds_list_from_sources_with_sources_printed | 실패 |
  | V1 실제 push의 `--approved` 허용 | test_approved_file_only_for_dry_run | 실패 |
  | `.gitattributes` `*.csv -text` 줄 삭제 / 파일 삭제 | test_5_crlf_input_bytes_preserved | 실패 / error(setUp 복사) |
  | N3 시작 HEAD 검사 제거 | test_6·test_3 | 둘 다 실패 |
  | N3 줄바꿈 검사 제거 | test_7 | 실패 |
  | precheck.sh를 b4cc8b9 판으로 | PrecheckTests.test_compute_failure_stops_before_compare | 실패 — **(수정 회차 3 정정)** 옛 판은 `python3` 고정이라 Store 스텁에서 먼저 실패했다(결함 때문이 아님). `"$PY"`로 고친 옛 흐름(`compute && compare \| tail`) 변이가 실제 결함(compute 실패인데 "전부 통과")을 보이며 실패한다 — 수정 기록 3 변이 표 |
  | N2 base 대조 제거 / `--base` 필수 제거 | test_base_mismatch_stops_before_put / test_real_push_requires_base… | 실패 / 실패 |
  | N1 `perm = True` | test_permission_false_or_lookup_error_fails | 실패 |
  | V4 token_of 옛 판(예외 안 잡음) | test_token_file_encodings_and_missing | 실패(error) |
- **리허설**(19:56:48 → 20:08:21, 스크래치 LF clone — 작업본 변경을 얹은 임시 main + 로컬 bare origin, code-tab.md 순서):
  S0 = 2절 블록 원문(md5 1fcef6f5, 치환 = cd 경로·프로필 경로 2곳, 도우미 없는 임시 설정) → 배포 줄만 `[FAIL] 자격 증명을 얻지 못함(출처: git)` + `[FAIL] 배포 저장소 점검 실패(… rc=1) — 원인은 바로 위 줄 …`, 나머지 줄 통과, 작업 트리·ignored 변경 0(`__pycache__` 0) →
  fetch `--dry-run` 오늘(`이번달` 09.01~09.27)·`--today 2026-10-01`(`지난달` 09.01~09.30) 폴더 생성 0 → ingest(쉼표·공백 이름 4개): 시작 검사 "origin/main = HEAD 확인"·"줄바꿈 = 커밋 확인" → combine 33일 9,991/309/351,299원 PASS → push → origin/main = HEAD, 재실행 "변경 없음" →
  deploy fetch 무인증(sha 1c52f70, 2101행, md5 a3465ec0) → compute → 2-1 = 같음(`2026.08.26 — 09.27 (33일)` 양쪽 — 실운영이면 여기서 앞 질문) → propose `--since 2026-09-27` = 후보 1 `노원힐링장소.`(CRLF)·업종어 4 / `--since 2026-09-28` = `[주의] 빈 창`, 파일 `…_2026-09-28_2026-09-27_*`(0바이트)로 09-27 파일 안 덮음 →
  참조 선택 dry-run: (a) `--drop 1 --extra-rows 1164`(마침표 없음) → 쌍둥이 `[주의]`(후보:1·검색어.csv:1165) + `[FAIL] 추가 이름 '노원힐링장소' … 이미 모든 대상 그룹 registered` exit 1·승인 파일 0 / (b) 후보 그대로 → `approved_2026-09-28.txt` = `노원힐링장소.` LF 1줄, 3그룹 "등록 예정 1 · 221 → 222" / (c) `--drop 1 --extra-rows 1165` → 통과 + `[주의]` 쌍둥이 `'노원힐링장소' ← 검색어.csv:1164·registry 200·421·644행(registered 3)` / (d) 업종어 2줄 더해 `--expect 2` → `[FAIL] 합계 3 ≠ --expect 2`. HTTP 0(프록시 127.0.0.1:9로 막고), registry md5 ca642639 전후 같음 →
  precheck(작업본 = 배포본 + 주석 1줄) 22 PASS · 95 / DIFF 0 · 360/390/430 PASS · 외부 요청 차단 6건 · 넘침 0 · 전부 통과 rc 0(6초) / md5 가드 rc 1 →
  deploy(자격 증명 없이): `--base work/index.html` → `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` rc 1 · 실제 push에 `--base` 없음 → rc 2 · verify 같은 파일 일치 rc 0 / 바꾼 사본 불일치 `[FAIL]` rc 1 →
  **실제 자격 증명 1회(사용자 승인, 20:08)** `push --file work/index.html --base work/prev.html --dry-run` → "배포본 = --base md5 a3465ec0 확인" · "자격 증명 확인됨(출처: git)" · **`permissions.push: 참`** · "[dry-run] PUT을 보내지 않음" rc 0, 출력 속 토큰 모양 문자열 0건.
- **전후**(19:56 → 20:14): 스킬 저장소 `ls-remote` HEAD·main b4cc8b9 · feat-code-tab df658f3(push 전) · test* 0 · 배포 32d8b05 · main 작업 폴더 HEAD b4cc8b9·status 0·md5 4dd3b0cf(`cat data/*/*.csv config/*.json audit/exclusions.csv | md5sum` — 검증 1 참고의 집계 방식) · `~/saero-fetch/downloads` 목록(`ls -laR` md5) ed69f294 같음 · `D:\saero` 설치 0.
- **grep 잔존**(SKILL.md·references·scripts/*.py·*.sh·tests/*.py·local·checklist): `<창끝>` 단독 0 · `python3 `(shebang·금지 문장 제외) 0 · "30일까지만" = 옛 전제 인용 2곳(SKILL.md 원본 보관·checklist 22)만 · "PC PowerShell" 0 · `python scripts\` 0 · "복사로만" 0 · "첫 PUT" = checklist 새 행 설명만 · `tail -2` 0 · 옛 금지 차단 괄호 0.
- **문법**: py_compile 14/14 · `bash -n` 2 · 코드펜스 짝수(SKILL 16 · code-tab 4 · report-fetch 8 · exclusion-ui 2 · checklist 6 · local 0) · 변경 파일 19개 UTF-8 · CR 0.

## 검증 2가 볼 것
1. **변경 파일 = V·N 범위**: `git diff df658f3 --stat` = 위 표 + last-audit.md, 불변 줄(precheck.sh·reportlib·config·data·registry·local/CLAUDE.md) md5.
2. **시험 4종 + mutation_test**(venv, PYTHONUTF8 없이, LF clone): 34 · 7 · 8 · 15 OK, "전부 살아 있음".
3. **변이 실험 재현**: 위 표의 짝 변이 중 최소 :808·:830·:673a·.gitattributes 줄·N3 둘·base·permission·precheck 옛 판에서 짝 시험이 실패하는지.
4. **V1 CLI 재현**: 스크래치에서 propose `--since 2026-09-27` → 참조 선택 dry-run (a) 1164 FAIL·승인 파일 0 (b) 후보 통과·LF (c) 1165 통과 + 쌍둥이 (d) 합계 ≠ N FAIL, HTTP 0·registry 불변. 실제 push에 `--approved` FAIL(키 파일 없이도 쓰기 전 멈춤).
5. **V2 같은 말 4곳**: SKILL.md 2-1 · code-tab.md "2-1 같음" · local :24-26 · checklist 26의 흐름 문장이 같은지(글자 대조), propose 파일명 `<lo>_<hi>`·빈 창 `[주의]`·다른 창 파일 안 덮음, 8단계 양식 줄, `--since` 규칙 2곳.
6. **V3**: fetch_reports.py 메시지 = 지시 문구, code-tab.md 4절·report-fetch.md 5절 행, 강제 캡처 코드 추가 0.
7. **V4**: `--token-file` 없는 경로·UTF-16LE(PowerShell 5.1 `>`)·UTF-16BE·깨진 바이트 → `[FAIL] 자격 증명을 얻지 못함(출처: token-file)`, Traceback 0.
8. **V5**: S0 블록 배포 줄 실패 원인별 출력(도우미 없음·PY 없음·네트워크) + `[FAIL] 배포 저장소 점검 실패(rc=…)` · `__pycache__` 0 · 2절 문구 · 5절 표 행.
9. **N1**: 가짜 시험(참·거짓·401) + 이 기록의 실측 1회 대조(실제 자격 증명으로 다시 돌리지 않는다).
10. **N2**: base 불일치 → exit 1·PUT 0·자격 증명 요청 0(무인증 GET이 403·429면 GET용 1회) · `--base` 없는 실제 push → exit 2·요청 0.
11. **N3**: 시작 검사 두 경로(원격 앞섬·CSV CRLF) — store 전 멈춤·HEAD·data·스테이징 불변.
12. **N4 격리**: test_deploy가 이 PC 자격 증명 관리자에 닿지 않는지(자식 env `GIT_CONFIG_NOSYSTEM=1`·`GIT_CONFIG_GLOBAL`), 가짜 값 출력 0 · 헤더에만.
13. **V9~V15 정정 블록**: 아래 구현 기록 절 "정정(검증 1)" 9줄이 검증 1 결론 9~15·V4와 맞는지.
14. **V16~V18 grep**(범위를 scripts/*.py·tests/*.py·local/까지): `python3 `·"30일까지만"(옛 전제 인용 제외)·"PC PowerShell"·`python scripts\` 0, SKILL.md md5 가드 인용 = 앞부분만.
15. **checklist**: 승인 목록 행 교체 + 3행 추가(deploy base·권한 / ingest 시작 검사 / 비출력 시험) · 26 2-1 예외 · 19·22 · v4.7 유지 + 갱신 이력 한 줄.
16. **의도 검증**: 임의 결정 1~15·"원래 지시를 바꾼 곳" 6줄 — 지시 의도와 다른 구현이 있으면 그것만.

## 새로 내가 고를 항목
1. (이월) **병합과 10/1**: 10/1(`지난달` 첫 실측)이 병합 전이면 main 작업 폴더에서 수집만 하고 ②는 병합 뒤 / 검증·병합을 10/1 전에.
2. (이월) **병합 직후 main 작업 폴더 줄바꿈 정리**(code-tab.md 8절) — 이제 S0에 더해 ingest 시작 검사도 그 폴더에서 멈춘다.
3. (이월) **local/ 설치**(사용자 복사, 마감 때 md5 대조) — 대조 기준은 LF 판(a963e8eb·af47cb28). autocrlf=true 폴더에서 복사하면 CRLF라 값이 다르다(검증 1 참고).
4. **dry-run이 승인 파일을 쓰는 것**(임의 결정 1) — 그대로 / dry-run은 화면 출력만.
5. **권한 확인을 실제 push 직전에도** 할지(임의 결정 8 — 지금은 dry-run만, 인증 GET 1회 추가).
6. **2-1 대조를 명령으로**: 지금은 세션 즉석 코드 4행(compute.json `masthead` ↔ prev.html `집계 기간`) — 회차 2에 작은 출력(예: compute가 prev와 같은지 한 줄)을 더할지(즉석 코드 0 목표).
7. **`--extra-rows` 찾기**: 세션이 `grep -n '<이름 일부>'`로 행 번호를 찾는다(이름 일부를 치는 것은 찾기용이고 목록은 push가 파일에서 읽는다) — 이대로 / propose가 07번 후보 행 번호표를 같이 쓰게.
8. (이월) keep 처리 주체 · "노원힐링장소."(마침표 원문, 미등록) 재상정 — 이번 리허설 (b)·(c)에서 9/27 창으로 올리면 3그룹 등록 예정 1로 나온다.

## 마무리 기록(이번 회차)
- 커밋 ①(코드·시험·문서 — SKILL.md·references·scripts·tests·local) + 커밋 ②(이 절·정정 블록·checklist), `feat-code-tab`만 push(이 PC git 자격 증명). 재clone 대조는 보고에(자기 참조라 이 절에 해시 없음).
- 토큰 수령 0 · 네이버 0 · 배포 저장소 쓰기 0(읽기 GET — 인증 1회는 사용자 승인) · main·main 작업 폴더 0 · 설치본 부트스트랩 불변.

---

# 기능 추가 구현 기록(Code 탭 전 단계 실행 — 설계안 C 회차 1, 2026-09-28)
세션: 데스크톱 앱 Code 탭(이 PC, `D:\saero`로 열림), Opus 5.5 — 탐색 기준선(아래 절)과 같은 세션이 조정 세션 지시(프롬프트 ② 형식)를 받아 구현. 브랜치 **`feat-code-tab`**(`b4cc8b9`에서 분기, `D:\saero\feat-code-tab` — `git -c core.autocrlf=false clone`), **main 미반영**. 커밋 1 `f0520b5`(코드·시험·references·SKILL.md·local/·.gitattributes·.gitignore) + 커밋 2(이 절 + checklist v4.7 + registry 시험 1행 — 자기 참조라 해시는 적지 않는다).
검증용 clone: `git clone -c core.autocrlf=false -b feat-code-tab --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill <별도 폴더>`
외부 쓰기: 스킬 저장소 = `feat-code-tab` push + 시험 브랜치 `test-push-0928` push·삭제(사용자 승인) · 네이버 = 시험 1건(`test-roundtrip`, 사용자 입회, 등록→확인→삭제) · 배포 저장소 0 · main 0 · main 작업 폴더(`D:\saero\saero-ad-report-skill`) 0 · `D:\saero` 아래 설치 = venv `D:\saero\.venv`만(사용자 승인, local/ 사본은 설치 안 함) · 토큰 수령 0(PC git 자격 증명).
효율: 벽시계 약 75분(15:20 clone → 16:3x push, 사용자 승인 대기 3회 포함) · 도구 호출 조정자 약 200회 + 리뷰 하위 에이전트 206회 · 즉석 코드 약 50행(저장소 밖 — 리허설 2-1 대조 6·승인 목록 복사 10·masthead 변조 5·CR/펜스 검사 등; 편집 보조 파이썬 제외). 리허설 기계 단계(S0 → 7 dry-run·verify)는 약 13회·4분 — 기준선 6절 C 추정 55~70회/회차 중 서술 교체(20~28)·기록(4~5)·실제 수집 대기를 뺀 몫(약 17~26)과 같은 크기.
표기: [실측] 이 세션에서 직접 확인 / [추론] 확인 못 함.

## 정정(검증 1 — 2026-09-28 수정 회차 2에서, 아래 본문은 그대로 두고 여기서 바로잡는다)
- D5 `local/saero-run/SKILL.md`**(23행)** → **25행**(이 절을 쓸 때의 판 b212888c. 수정 회차 2 뒤 28행).
- K10 `tests/test_ingest.py`**(신규, 3개)** → **4개**(지시 3경로 + data/만 커밋 1).
- K9 "`common_days = (e-s)+1`" → **`common_days == len(now[0]["by_date"])`**(행이 있는 날짜 수 — 임의 결정 9와 같은 선택. 지금 데이터에서는 둘 다 27).
- 임의 결정 13 "토큰 안내 **272행**" → checklist **"토큰 안내가 정확한지" 줄**(당시 274행, 옛 판 260 — 272행은 compute+compare 재현 항목).
- 실측 "test_exclusions Ran 29 OK(**종전 FAILED 1·ERROR 3**)" → **종전 venv FAILED 1·ERROR 1**(시스템 파이썬 — pandas 없음 — 이면 ERROR 3).
- 리허설 1 "masthead 변조본 exit 1 + 전체 출력(**22줄**)" → **32줄(검사 22 + 요약)**.
- 임의 결정 2·실측(mutation_test 줄)의 첫 실패 서술 → **디코드 실패**(자식 출력 utf-8을 부모가 cp949로 읽어 `UnicodeDecodeError` → `AttributeError … splitlines`) → subprocess `encoding` 뒤 **`—` EncodeError**(자신의 print) → reconfigure 뒤 통과. 두 고침이 다 있어야 통과한다는 결론은 그대로.
- 임의 결정 6·검증 12의 "요청 예외는 종류만" → **요청 예외는 종류만(네트워크 연결 오류만 소켓 사유 문구 — 헤더 값 없음)**(deploy.py docstring도 같은 말로 고침).
- checklist [의도된 동작] 22의 "SKILL.md 58행" → **SKILL.md "원본 보관 — data/" 절**(이번 회차 전부터 틀린 번호 — checklist에서 고침).

## 항목별(지시 K1~K10 · D1~D6) — 절·함수 기준
- **K1 `scripts/ingest.sh`**: 사용법 `PY=<venv 파이썬> scripts/ingest.sh <CSV> [...]`(토큰 인자 삭제, 인자 없으면 exit 2) · `PY="${PY:-python3}"`·`export PYTHONUTF8=1`·`OUT="$ROOT/work/combined"` · 쓰기 전 브랜치 검사(main 아니면 `[FAIL] 현재 브랜치가 main이 아님` exit 1) · git 신원이 없을 때만 `-c user.*`(`GITID` 배열) · push = `git push -q origin HEAD:main` · `synced()` = `git fetch -q origin main` 뒤 HEAD ≠ origin/main이면 `[FAIL] HEAD … ≠ origin/main` exit 1 — push 뒤와 "data/ 변경 없음" **두 분기 모두**.
- **K2 `scripts/precheck.sh`**: PY·PYTHONUTF8 같은 방식 · `J="$(dirname "$HTML")/compute.json"` · md5 가드 메시지 = "3번째 인자에는 4단계 deploy.py fetch가 저장한 직전 배포본(work/prev.html)을 넣어라"(뜻 유지) · `run()` = 통과면 끝 3줄, 실패면 전체 출력 뒤 같은 종료 코드(validate·compare). compute 출력은 종전처럼 전부.
- **K3 utf-8 reconfigure**(stdout·stderr, `for _s in (sys.stdout, sys.stderr): _s.reconfigure(encoding="utf-8")`): archive·compute·validate(pandas 검사 앞)·compare·deploy·tests/overflow_check.
- **K4 `~` 확장**: `exclusions.py` `load_keys` · `deploy.py` `token_of`(`os.path.expanduser`).
- **K5 `scripts/deploy.py`**: `--token-file` 선택 · `get()` = 무인증 GET → 403·429면 `credential()`로 1회 · `credential()` = token-file이면 그 파일, 없으면 `git_credential()`(`git credential fill`, stdin `protocol=https\nhost=github.com`, env `GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`, timeout 60, `password=` 줄만 — 값은 반환만) · PUT·`push --dry-run` 모두 자격 증명을 얻어 "자격 증명 확인됨(출처: token-file|git)"만 출력, 못 얻으면 `[FAIL] 자격 증명을 얻지 못함` exit 1 · verify 불일치 `[FAIL]` 안내(재PUT 안 함).
- **K6** `.gitattributes`(`*.csv -text` · `*.sh text eol=lf`) · `.gitignore` += `.claude/`. renormalize: 아래 실측.
- **K7 `tests/overflow_check.py`**: 페이지마다 `pg.route("**/*", only_file)` — `file:` 밖은 `route.abort()`, 끝에 "외부 요청 차단 N건" 출력.
- **K8 문구**: `validate.py` pandas 없음 안내 → venv(code-tab.md 1절) · `fetch_reports.py` docstring(인자 오류 = argparse exit 2, 출력 첫 줄 `usage:`로 구분 / store 이후 = Code 탭 1단계 ingest) · 성공 뒤 `다음:` 줄 = `PY=<venv 파이썬> scripts/ingest.sh "<성공 폴더>"/*.csv`.
- **K9** `test_fetch_reports.py` `real_period()`(실 `data/2026-09/키워드.csv` 첫 줄 HEAD_RE) — 실 데이터 검사 2곳과 `common_days = (e-s)+1`, 음성 단언은 "헤더 끝 + 1일 → 기간 = 기대 FAIL"로 보존 · `test_exclusions.py` `test_push_dry_run_zero_http_and_no_file_change`는 임시 fixture registry(새로오픈 3그룹 registered·group_id 채움, 노원역맛집출구 없음), `:377` subprocess `encoding="utf-8"`.
- **K10 `tests/test_ingest.py`**(신규, 3개): 임시 저장소(scripts 3·config·.gitattributes·.gitignore·data/2026-08) + `git clone --bare` origin, 입력 = data/2026-09 4개를 data 밖 `in 폴더/<이름> 보고서,2580077.csv`로 복사 — test_1 정상(push → origin/main = HEAD, 원격 CSV 바이트 = 입력, 같은 입력 재실행은 변경 없음 PASS) · test_2 main 아닌 브랜치(`[FAIL]`·store 전 멈춤·커밋 0·data 변경 0) · test_3 pre-receive hook 거부로 커밋만 된 상태 → 재실행 "변경 없음"에서 `≠ origin/main` exit 1.
- **D1 `references/code-tab.md`**(신규) 0 진입 · 1 환경 · 2 S0 블록 · 3 전 단계 순서 · 4 멈춤 표 · 5 exit 코드 판정 · 6 승인 목록 복사 규칙 · 7 금지 · 8 수동 폴백·작업 폴더 줄바꿈 · 9 리허설.
- **D2 SKILL.md**: 맨 위 "먼저 — 실행 환경(채팅 가드)" · 배포 정보(자격 증명 하나, "서로 통하지 않는다"는 PC에서 불성립) · 작업 폴더·work/·수집 성공 폴더 · 원본 보관(파일명·이번 달·직접 입력 기간) · 1단계(fetch → ingest, `$PY`) · 2단계 FAIL 문구(프리셋·폴백) · 2-1(4단계 fetch 당김·compute masthead) · 4단계(무인증 GET) · 5-0 명령·4항(Code 탭 세션·복사 규칙·키 경로만)·6항(시험 회차) · 5·6·7단계 명령(`$PY`, work/, verify 불일치 대처) · 8단계 [PASS] 세기 · 승인 지점(순서·묶음·"등록은 나중에") · 참고 문서(code-tab.md·test_ingest).
- **D3 references/report-fetch.md**: 1절(작업 폴더·venv) · 3절 명령 · 4절 51(ingest로) · 5절(금지 차단엔 summary·스크린샷 없음 · 세션이 partial을 재실행 전에 읽음 · 로그인 실패 산출물 안 엶 · 첨부 → 세션이 읽음) · 6절 · 8절 `$PY` · 9절 절차 삭제(기록만).
- **D4 references/exclusion-ui.md**: 2절 키 행 · 3절 전면(정식 경로 = Code 탭 세션, 명령 `$PY`·`~` 키 경로, 결과 파일은 같은 폴더) · 4절 import-ui `$PY` · 6절 제목·승인 목록 복사 · 8절 시험 회차.
- **D5 local/**: `saero-run/SKILL.md`(23행, frontmatter = wrapup 형식) · `CLAUDE.md`(3줄). 경로는 `D:\saero`(bash `/d/saero`)·`~`만, 토큰·키 값 0. 설치 안 함.
- **D6 audit/checklist.md**(커밋 2): v4.7 · [시작 전 확인 ①] Code 탭 한 문장 · ② 명령 `$PY`·work/·재수집 문구 · [의도된 동작] 15·17·19·20(개정)·21·22·24(개정)·25 보강·26 신설 · [되돌리면 안 되는 것] 5행 · C① 시험 회차 · mutation 명령 `$PY`.

## 임의 결정(번호 = 사용자가 바꿀 단위)
1. **stderr까지·대상 밖 파일까지 utf-8**: K3 6개 파일에 더해 `fetch_reports.py`·`exclusions.py`(기준이던 stdout만 → stdout·stderr — SystemExit 문구가 cp949 파이프에서 깨짐)·`tests/mutation_test.py`·`tests/test_ingest.py`에도 같은 줄.
2. **`tests/mutation_test.py` subprocess `encoding="utf-8"` 2곳** — K3 뒤 자식 출력이 utf-8이라 부모(cp949) 디코드가 깨진다. 리허설 첫 실행이 mutation_test 자신의 `—` 출력에서 UnicodeEncodeError로 멈췄고(1번과 함께 고친 뒤 전부 살아 있음) — "PYTHONUTF8 없이 mutation_test 전부 살아 있음" 조건을 채우려고.
3. **ingest·precheck의 `"$PY" -c 'import sys'` 실행 가능 검사**(Store 스텁 exit 49를 첫 줄 `[FAIL] 파이썬을 실행할 수 없음`으로) · ingest 인자 없음 exit 2.
4. **ingest 보강(반박 리뷰 반영)**: `GIT_TERMINAL_PROMPT=0`·`GCM_INTERACTIVE=never`·`unset GIT_ASKPASS SSH_ASKPASS`·`-c credential.interactive=false`(자격 증명 창으로 멈추지 않게) · 원격 비교는 `origin/main` 대신 `FETCH_HEAD`(single-branch clone에서도 방금 받은 값) · `git commit -- data`(data/ 밖 스테이징이 `data:` 커밋에 섞이지 않게) · push 거부 `[FAIL] push 실패 — 커밋 …는 로컬에만` exit 1(종전은 git의 코드).
5. **precheck**: compute를 `&&` 목록에서 떼어 실패하면 멈춘다(종전 `compute && compare | tail`은 compute 실패를 set -e가 못 잡아 "6단계 전부 통과"로 끝날 수 있었다 — 동작 변화) · md5 가드 `md5sum < 파일`(파일명에 `\`가 있으면 GNU md5sum이 출력 앞에 `\`를 붙여 같은 파일도 다르게 나옴 — 윈도 경로 vs 상대 경로 실측) · 가드 메시지는 뜻 유지.
6. **deploy.py 보강**: `push --dry-run`은 `--file` 없이도(S0용 — sha·자격 증명만) · `--file` 없는 push·verify exit 2 · 요청 예외(URLError·ValueError·HTTPException·OSError) → 종류만 출력(개행이 든 토큰은 http.client가 헤더 값을 예외 문구에 담는다 — 리뷰 보안 F1) · `usable()` 한 줄 토큰 형식 검사(token-file·git 자격 증명 둘 다, 아니면 "못 얻음") · token-file `utf-8-sig`(BOM) · GET `Cache-Control: no-cache`(무인증 응답 공용 캐시 60초 — PUT 직후 verify 거짓 불일치 방지 [추론]) · verify 출력에 sha, 불일치 `[FAIL]` 안내 · `git credential fill`에 `credential.interactive=false`·askpass 변수 제거.
7. overflow_check 끝에 "외부 요청 차단 N건" 출력(검증 11 근거).
8. **문구**: `fetch_reports.py` `다음:` 줄 경로를 `/`로(Git Bash glob), 금지 차단·로그인 만료 안내(첨부·PowerShell 경로 → Code 탭 표현) · `exclusions.py` docstring 사용법 `$PY`·`--since`·키 문장·propose 주석.
9. **시험 세부**: test_fetch_reports 합성 파일 검사는 고정 기간(09-01~09-26) 유지(합성 헤더가 고정), `common_days`는 "행이 있는 날짜 수"(달력 일수 대신 — 노출 0인 날 대비) · test_exclusions fixture = 새로오픈 3그룹 registered(group_id 채움)·노원역맛집출구 없음(원래 주석의 의도) · test_ingest 4번째 시험(data/만 커밋).
10. **code-tab.md**: compute를 2-1 앞으로(masthead 문자열 대조 — 탐색 반박 검증 B) · 2-1 "같음"이면 3·5-0a를 건너뛰고 그 질문 하나만(묶음 예외 — 같은 데이터라 다른 후보 무의미) · (권장) pull로 바뀐 registry는 5-0c, 없으면 8단계에서 경로 지정 커밋 · 재개 판정 규칙 · S0 추가 검사 3개(브랜치 main·작업 트리 깨끗·줄바꿈 i/·w/ — `core.quotepath=false`) · 프로필 검사 exit 3으로 "사용 중"과 "실행 오류" 구분 · 6절 승인 목록 복사 스크립트 예(리허설에서 쓴 것).
11. **SKILL.md**: 채팅 가드에 `/mnt/user-data`도 · 가드 밖 문서는 "컨테이너 작업 경로"로 표현(가드 외 0 규칙) · "채팅으로 보고" → "대화로" · "사용자 지정 기간" → "직접 입력(한) 기간"(SKILL·report-fetch·checklist — grep 0 규칙) · `--token-file`은 사용자 선택 폴백으로 명시 · 2-1 제목 "재계산·교체 전에 멈춘다" · compare·overflow 명령에 `$PY`.
12. **report-fetch.md** D3 지정 행 밖: 1절 설치 블록(venv)·2절 `--login` 명령·5절 첨부 → 세션이 읽음(63·66·71행)·8절 설명.
13. **checklist**: 점검 대상 목록 갱신(신규 + 기존 누락 파일) · 토큰 안내 272행·[마무리] 폐기 안내·"토큰을 못 받았으면"에 채팅/Code 탭 한정 · 21·22 문구 · overflow·mutation 명령 `$PY`.
14. registry 시험 1행은 커밋 2(기록)에 넣었다.

## 원래 설계·지시를 바꾼 곳(검증 15)
- K10 "임시 clone + 로컬 bare origin" → **작업 트리 사본 + `git init` 임시 저장소 + `git clone --bare` origin**(커밋 전 작업본 ingest.sh를 시험하려고). 시험은 지시 3경로 + data/만 커밋 1 = 4개.
- K1 "HEAD == origin/main" → **FETCH_HEAD 비교**(뜻 같음 — single-branch clone에서 origin/main이 갱신되지 않는 경우 대비, 리뷰 bugs F3).
- K6 "renormalize 변경 0": 이 브랜치 LF clone(autocrlf=false)에서 0 [실측]. 다만 autocrlf=true로 `.gitattributes` 이전에 풀린 폴더(= 병합 직후 main 작업 폴더)에서는 CSV 8개가 CRLF 바이트로 스테이징된다 [실측 — 스크래치 clone] → 그 폴더에서는 renormalize·`git add data` 금지, code-tab.md 8절 절차(S0 줄바꿈 검사가 먼저 멈춘다).
- D1 3 순서: 기준선 6절 공통 뼈대의 "2-1 → 3 → propose + pull + compute"에서 compute를 2-1 앞으로, 2-1 "같음"은 묶음 대신 즉시 단독 질문(임의 결정 10).
- K5 dry-run 확인 범위: "자격 증명 확인됨"은 값을 얻었다는 뜻까지 — 유효성·배포 저장소 쓰기 권한은 첫 PUT(F11 ⑤ 대체안의 한계로 문서에 명시).
- K2: compute를 떼어 종전 결함(compute 실패 무시)을 고쳤다 — 동작 변화(임의 결정 5).

## 실측 [실측]
- **venv**: `D:\saero\.venv`(`python -m venv --system-site-packages` → `pip install "pandas>=2.2,<3"`, 사용자 승인 뒤) = Python 3.12.10 · pandas 2.3.3 · playwright 1.63.0(시스템). 시스템 Python 불변(pandas 없음 그대로).
- **시험**(LF clone `D:\saero\feat-code-tab`, venv, PYTHONUTF8 없이, `-W error::ResourceWarning`): test_fetch_reports **Ran 15 OK**(85초 — 이월 ② 해소, 종전 FAILED 2) · test_exclusions **Ran 29 OK**(종전 FAILED 1·ERROR 3) · test_ingest **Ran 4 OK**(32초) · 끝 줄 실제 data·config·registry md5 전/후 동일.
- **mutation_test**(리허설 clone, venv, PYTHONUTF8 없이, 배포본 = 무인증 재수령 32d8b05 파일 sha 1c52f70·md5 a3465ec0, 합본 33일): **"전부 살아 있음"** · [OK] 43줄 · MISS/UNCOVERED/SKIP 0 · 원본 md5 전부 동일. 첫 실행은 mutation_test 자신의 `—` 출력에서 UnicodeEncodeError → 임의 결정 1·2 뒤 통과.
- **리허설 1**(15:46:44 → 15:50:30, 스크래치 LF clone + 로컬 bare origin, 도구 약 13회, code-tab.md 순서): S0 PASS(자격 증명 확인됨(출처: git) — 값 출력 0, 프로필 검사만 스크래치 폴더) → fetch `--dry-run` 오늘(`이번달` 09.01~09.27)·`--today 2026-10-01`(`지난달` 09.01~09.30) 폴더 생성 0 → ingest(입력 = data/2026-09 사본 4개를 data 밖 `<이름> 보고서,2580077.csv`로 — 쉼표·공백·Git Bash 경로 OK, combine 33일 9,991/309/351,299원 PASS, 변경 없음 → origin/main = HEAD) → deploy fetch 무인증(sha 1c52f70, 2101행, md5 a3465ec0 = 09-28 재수령 기록) → compute → 2-1 = 같음(실운영이면 여기서 단독 질문) → propose `--since 2026-09-28` = 빈 창 0건 / `--since 2026-09-27` = 신규 1 **"노원힐링장소."**(마침표 그대로 — `_candidates.txt`는 CRLF) → 6절 복사 규칙으로 승인 목록 1줄 = N → `push --dry-run` 3그룹 "등록 예정 1 · 221 → 222 · 등록: 노원힐링장소.", HTTP 0, registry md5 불변 → precheck(작업본 = 배포본 + 주석 1줄): validate 22 PASS · compare 95 / DIFF 0 · overflow 0 · 외부 요청 차단 6건 · md5 가드 exit 1 · masthead 변조본 exit 1 + 전체 출력(22줄) → `deploy.py push --dry-run --file`(자격 증명 확인됨) → verify 같은 파일 일치 exit 0 / 바꾼 사본 불일치 exit 1.
- **리허설 2**(반박 리뷰 반영 뒤, 16:23): 새 S0 블록 PASS · ingest 변경 없음 → FETCH_HEAD = HEAD · precheck 22/95/0 · md5 가드가 윈도 경로 vs 상대 경로로 넣은 같은 파일도 잡음 · verify 출력에 sha · 가짜 두 줄 토큰 파일 → `[FAIL] 자격 증명을 얻지 못함(출처: token-file)` exit 1, BOM 붙은 한 줄 → 확인됨, 출력 속 가짜 값 0건.
- **전후**(리허설·시험 전체): 실제 원격 스킬 main `b4cc8b9` · 배포 `32d8b05` 불변 · main 작업 폴더 md5(data·config·registry) 4dd3b0cf·status 0·HEAD b4cc8b9 불변 · 실제 수집 폴더 생성 0.
- **반박 리뷰**(하위 에이전트 5 — 지시 준수·자격 증명 보안·셸/엣지·문서=코드·회귀, 읽기 전용): 44건(high 0 · medium 8 · low 36), 회귀 0(되돌리면 안 되는 것 행 전부 유지). 반영하거나 이 절 임의 결정·바꾼 곳에 기록. 반영 안 한 것 2(고를 항목 4): deploy dry-run 인증 GET(유효성) · deploy 자격 증명 비출력 오프라인 시험.
- **GitHub 시험**(사용자 승인, 15:36:11 → 15:36:18): `test-push-0928` push → `ls-remote` b4cc8b9 → `push --delete` → 0줄, main b4cc8b9 불변.
- **네이버 시험 1건**(사용자 입회 — 상계동필라테스 제외 검색어 탭, 15:51:17, 브랜치 코드): `test-roundtrip --keyword saero제외테스트0928 --group grp-a001-01-000000072587864 --key-file ~/naver-api.keys.json --confirm`(description `saero test 09-28`) → `[test] 등록 성공 id=rst-a001-00-000002190250607` → `[test] 다시 읽어 확인: 있음(verified)` → `[test] 삭제 뒤 확인: 없음 — 원상복구` → `[test] PASS — registry에 deleted 행으로 기록` exit 0. registry 665 → 666줄(f495f03b → ca642639), diff +1행 `saero제외테스트0928,grp-a001-01-000000072587864,상계동필라테스,EXP_SEARCH,deleted,skill,2026-09-28,rst-a001-00-000002190250607,2026-09-28,2026-09-28 시험 등록→확인→삭제`. **병합 때 main registry가 바뀌어 있으면 "main 판 + 이 1행"으로 푼다.**
- **잔존 grep**(SKILL.md·scripts/*.sh·references·checklist): `python3 `(shebang 제외) 0 · `/home/claude`·`/mnt/user-data` = 채팅 가드 1줄 · Desktop\Agent 0 · x-access-token 0(local 포함) · "사용자 지정 기간" 0 · "사용자 PC의 PowerShell"·"일반 셸" 0 · local/에 두 경로 0.
- **문법**: py_compile 13/13 · bash -n 2 · 코드펜스 짝수(SKILL 16 · code-tab 4 · report-fetch 8 · exclusion-ui 2 · checklist 6) · UTF-8 · 변경 파일 CR 0(registry는 i/crlf 그대로).
- **K6**: 이 브랜치 LF clone `git add --renormalize .` 변경 0 · autocrlf=true 새 clone 대조는 push 뒤(아래 마무리).
- **불변**: config b826b388 · data/2026-08·09(키워드 5a05ca2a·1da83049 등) · reportlib f29e64fc · compute·validate·compare 계산·검사 로직 · archive store/combine 검사.

변경 파일(`b4cc8b9` → 작업본; `wc -l` · md5 앞 8자리):

| 파일 | 행수 | md5 |
|---|---|---|
| `.gitattributes`(신규) | 4 | 8071a8fe |
| `.gitignore` | 5 → 6 | c79498bf → 1ddfa2fc |
| `SKILL.md` | 480 → 515 | afcae73c → 8d63300e |
| `references/code-tab.md`(신규) | 184 | 233bac4d |
| `references/exclusion-ui.md` | 132 → 139 | 152df14e → ec88e02d |
| `references/report-fetch.md` | 111 → 111 | 29824cc1 → bb9a5606 |
| `scripts/archive.py` | 196 → 202 | 74ef5974 → e8fb93fc |
| `scripts/compare.py` | 175 → 181 | 93e4c36b → 3184d1b7 |
| `scripts/compute.py` | 244 → 251 | 75edfb5c → f2cd7f2d |
| `scripts/deploy.py` | 92 → 182 | 0cf691c9 → feaf5ba6 |
| `scripts/exclusions.py` | 944 → 949 | defaa980 → 5b06e469 |
| `scripts/fetch_reports.py` | 973 → 976 | 322ffe8b → a14766bc |
| `scripts/ingest.sh` | 15 → 44 | 60abfcf3 → 26953e48 |
| `scripts/precheck.sh` | 17 → 26 | ecf566cd → 9fbf78e2 |
| `scripts/validate.py` | 418 → 424 | e3d71975 → dd00bb11 |
| `tests/mutation_test.py` | 373 → 379 | 90fbc1e8 → 0a9dc9dc |
| `tests/overflow_check.py` | 41 → 59 | 1f41f4bb → a3ecd0f5 |
| `tests/test_exclusions.py` | 547 → 553 | 6c2992fe → 635a2d60 |
| `tests/test_fetch_reports.py` | 595 → 604 | 1ba3be2c → e0dc0695 |
| `tests/test_ingest.py`(신규) | 167 | 7c2d6415 |
| `local/CLAUDE.md`(신규) | 3 | af47cb28 |
| `local/saero-run/SKILL.md`(신규) | 25 | b212888c |
| `audit/checklist.md`(커밋 2) | 481 → 497 | 5b11f72c → fdcb2027 |
| `audit/exclusions.csv`(커밋 2, 시험 1행) | 665 → 666 | f495f03b → ca642639 |
| `audit/last-audit.md`(커밋 2) | 이 절 추가 | (재clone 대조는 보고에) |

## 검증 회차가 볼 것
1. **변경 파일 = K·D 범위**: `git diff b4cc8b9 --stat` = 위 표 + last-audit.md. data·config 불변(md5), registry는 시험 1행만(`git diff b4cc8b9 -- audit/exclusions.csv` = +1행 deleted). 지시 밖 변경은 임의 결정 1~14와 대조.
2. **시험 3종 + mutation_test**: venv 파이썬, PYTHONUTF8 없이, LF clone — test_fetch_reports 15 OK · test_exclusions 29 OK · test_ingest 4 OK · mutation_test "전부 살아 있음"(배포본 = 32d8b05 재수령, 합본 `archive.py combine`).
3. **grep 잔존**(SKILL.md·scripts/*.sh·references·checklist): `python3 `(shebang 제외) 0 · `/home/claude`·`/mnt/user-data` = 채팅 가드 1줄 · Desktop\Agent 0 · x-access-token 0 · "사용자 지정 기간" 0 · "사용자 PC의 PowerShell"·"일반 셸"(갱신 이력 제외) 0.
4. **dry-run 무변경**: `fetch_reports.py --dry-run`(오늘 · `--today 2026-10-01`, 새 폴더) · `exclusions.py push --dry-run` · `deploy.py push --dry-run`(`--file` 있음·없음) 전후 md5(data·config·registry)·`git status`·두 저장소 `ls-remote` HEAD 동일, fetch 폴더 미생성.
5. **ingest 경로**(test_ingest 4개 + 코드 대조): 정상 push → FETCH_HEAD = HEAD / main 아닌 브랜치 → store 전 `[FAIL]`·커밋 0 / push 거부 → `[FAIL] push 실패`, 재실행 "변경 없음"에서 `≠ origin/main` / data/ 밖 스테이징이 `data:` 커밋에 안 섞임.
6. **금지 패턴 차단**: 승인 목록에 `노원역운동`·config 경쟁사명 → `push --dry-run`에 `[거부]`(test_exclusions `test_push_dry_run_zero_http_and_no_file_change` — fixture registry로 바뀐 뒤에도 `[거부] 노원역운동`·"승인 2개"·"등록 예정 1 · registry에 이미 등록 1" ×3 단언 유지).
7. **verified:false 실패 보고**: test_exclusions `test_verified_false_is_failure`(drop_after_post) — `failed`·exit 1.
8. **시험 1건 기록 대조**(재실행 안 함): 위 실측의 출력 원문 4줄 · registry `deleted` 1행(id `rst-a001-00-000002190250607`) · description `saero test 09-28`.
9. **GitHub 시험 브랜치**: `test-push-0928`이 원격에 없음(`git ls-remote origin refs/heads/test-push-0928` 0줄) — push·삭제 기록은 위 실측.
10. **.gitattributes**: `git -c core.autocrlf=true clone -b feat-code-tab …`에서 data CSV 8개·registry·*.sh 작업 파일 md5 = `git show HEAD:<파일>` md5, `git add --renormalize .` 변경 0. 단 attributes 이전에 autocrlf=true로 풀린 폴더에서는 CSV가 CRLF로 스테이징되는 것이 정상 동작(바꾼 곳 3번째 줄, code-tab.md 8절).
11. **overflow 외부 요청 0**: `tests/overflow_check.py` `only_file` route — 출력 "외부 요청 차단 N건"(리허설 6건), 결과 PASS·넘침 0.
12. **deploy 자격 증명 비출력**: 코드(`usable`·`git_credential`·`credential`·`api` except — 값은 반환·헤더에만, 예외는 종류만) + 실행 출력(리허설 1·2 dry-run·verify 출력, 가짜 토큰 파일 두 줄/BOM — 가짜 값 0건). `git credential fill`은 deploy.py 안에서만(`credential.interactive=false`·GCM_INTERACTIVE=never·GIT_TERMINAL_PROMPT=0·askpass 제거).
13. **문법**: py_compile 전부 · `bash -n` ingest·precheck · 코드펜스 짝수 · UTF-8 · CR 0(registry 제외).
14. **local/ 사본**: 토큰·키 값 0, 경로는 `~`·`D:\saero`(bash `/d/saero`)만, `saero-run/SKILL.md` frontmatter(name·description) = wrapup 형식, ≤40행(25) · CLAUDE.md 3줄. `D:\saero` 아래 설치 없음(`D:\saero\CLAUDE.md`·`D:\saero\.claude\skills\saero-run` 없음).
15. **의도 검증**: "원래 설계·지시를 바꾼 곳" 6줄과 임의 결정 1~14를 한 줄씩 — 지시 의도와 다른 구현이 있으면 그것만.

## 새로 내가 고를 항목
1. **병합과 10/1**: 10/1(`지난달` 첫 실측)이 병합 전이면 — (a) main 작업 폴더에서 수집만(`python scripts/fetch_reports.py --debug`, pandas 불필요)하고 ②는 병합 뒤 / (b) 검증·병합을 10/1 전에.
2. **병합 직후 main 작업 폴더 줄바꿈 정리 한 번**(code-tab.md 8절 — S0가 이름을 댄 CSV를 지우고 `git checkout -- data` / 새 LF clone으로 교체) — 사용자와 함께.
3. **local/ 설치**: 병합 뒤 `local/CLAUDE.md` → `D:\saero\CLAUDE.md`, `local/saero-run/SKILL.md` → `D:\saero\.claude\skills\saero-run\SKILL.md` 복사(사용자, 마감 때 md5 대조).
4. **이번에 반영하지 않은 리뷰 2건**: deploy `push --dry-run`에 인증 GET(자격 증명 유효성)을 더할지 · deploy 자격 증명 비출력 오프라인 시험(`tests/test_deploy.py` — 새 시험 파일 1개 제한으로 이번엔 안 함).
5. **회차 2 범위 확인**: `ingest.sh --from <성공 폴더>`(summary result=ok·exit_code 0·partial 거부) + `exclusions.py push --candidates … --expect N`(K() 대조, `_candidates.txt` CR 처리) + archive store에 data/ 안 파일을 넘기는 경우 차단(같은 경로면 원본 소실 — `archive.py:96-99`)을 넣을지.
6. **회차 1 병합 뒤 첫 실사용 범위**: 전 단계 1회(사용자 입회, 평일 01:00 KST 뒤, 10/1 피함) / 회차 2 병합 뒤로.
7. (이월) keep 처리 주체 · "노원힐링장소."(마침표 원문, 미등록) 재상정 — 리허설에서 9/27 창이면 신규 후보로 다시 뜨는 것을 확인.

## 마무리 기록(이번 회차)
- 커밋 1 `f0520b5` + 커밋 2(이 절·checklist v4.7·registry 시험 1행), 브랜치 `feat-code-tab`만 push(이 PC git 자격 증명), main 0. push 뒤 재clone·autocrlf=true clone 대조는 채팅 보고에(이 절의 해시는 자기 참조라 적지 않는다).
- 토큰 수령 0 · 네이버 쓰기 = 시험 1건(등록→삭제, 원상복구 확인) · 배포 저장소 0 · main 작업 폴더 0 · 설치본 부트스트랩 불변.

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

## 수정 기록 2 (2026-09-28 수정 회차 2 — 결함 1: 같은 크롬 프로필 2회째 실행 크래시)

세션: Claude Code 데스크톱(사용자 Windows 11 PC, 사용자 입회), Opus 5.5. 지시 범위 = 검증 보고(2026-09-28)의 결함 1 + 기록 오류 1건, 나머지 이월. 브랜치 `feat-report-fetch`만 push, main 0. 네이버 계정·광고주센터 접속 0, 실제 프로필 `~/saero-fetch/chrome-profile` 접근 0. 커밋: **`53a1575`**(코드·시험·문서) + 이 절(기록).

- **원인**(검증 보고): 설치 크롬이 전용 프로필 다운로드 기록(`Default/History` `downloads`)에 Playwright 임시 파일 경로(`…\playwright-artifacts-XXXX\<guid>`)를 남기고, 컨텍스트가 닫히면 Playwright가 그 파일을 지운다 → 같은 프로필 2회째 실행부터 `다운로드` 순간 크롬 0xC0000005. 기록만 지우면 정상, 번들 헤드리스는 기록을 안 남김. 이 회차에 더 찾은 것: 옛 `launch()`의 `rf.get("browser_channel") or "chrome"` 때문에 **시험(`browser_channel: None`)도 설치 크롬으로 돌아** 이 PC 수정 전 실행이 12개 중 실패 4(1개는 아래 CRLF, 3개는 브라우저 시험의 `TargetClosedError: Download.save_as: … has been closed` — 프로필을 두 번 쓰는 test_1·4·6 [추론]) [실측].
- **변경 함수**(`scripts/fetch_reports.py`): 신설 `history_db`(`Default/History` → 없으면 프로필 바로 밑 `History`) · `profile_in_use`(`SingletonLock` 또는 Windows `lockfile`이 열리지 않음) · `clean_download_history`(`BEGIN IMMEDIATE`로 쓰기 잠금 → `downloads`에서 target_path 파일이 없는 행 + 딸린 `downloads_url_chains`·`downloads_slices` 삭제, 파일 있는 행 유지; DB 없음·떠 있음·잠김·오류는 `[WARN]` 뒤 계속) / 변경 `launch`(config `browser_channel` 그대로 — null이면 channel 인자 없이 번들 크로미움, `"chrome"`이면 설치 크롬 → 실패 시 번들 크로미움) · `cmd_login`·`cmd_fetch`(launch 전에 정리, 콘솔 `[profile] 다운로드 기록 정리: …` + summary.json `steps`·`profile_cleanup`). config 불변(`browser_channel "chrome"`, md5 b826b388).
- **임의 결정**(수정 2): ① `downloads_slices`(열 `download_id`)도 함께 지운다 — 크롬이 기록을 지울 때와 같은 범위(지시는 url_chains만 명시) ② target_path가 빈 행도 "파일 없음"으로 지운다 ③ 떠 있음 판정은 잠금 파일 + DB 쓰기 잠금(1초) 두 겹 ④ 기록 DB가 없는 첫 실행의 `[WARN]` 한 줄은 지시 (다) 그대로.
- **시험**: 12 → **15개**(`test_clean_download_history_removes_only_missing_files` — (가) 없는 경로 행·url_chains 2·slices 삭제 (나) 있는 경로 행·파일 유지, 프로필 밑 `History` 폴백, 2회째 0건 / `test_clean_download_history_no_db_or_locked_warns` — (다) DB 없음 무동작 WARN·없는 프로필 폴더 안 만듦, 잠김 WARN·행 그대로, `SingletonLock`(심볼릭 링크를 만들 수 있는 환경에서만) / `test_launch_channel_respects_config`). `python -W error::ResourceWarning tests/test_fetch_reports.py` → **Ran 15 tests · OK**(78초, 수정 전 282초) · `실제 data/2026-09·config md5 전/후 동일: True`(aade0da0·1d697d8a·024233a2·11c61476 · config b826b388) — `core.autocrlf=false`로 새로 clone한 `53a1575`에서 [실측]. 브라우저 시험 6개는 번들 크로미움(chromium-1243·Playwright 1.63.0). 이 PC 작업 폴더는 git 전역 `core.autocrlf=true`라 CSV가 CRLF로 풀려 `test_config_columns_match_real_csv`만 실패 — 저장소는 LF(i/lf), 환경 탓.
- **④ 실측**(이 PC, 설치 크롬 154.0.8037.57 **창**, 임시 프로필 + 가짜 화면 `tests/fixtures`(127.0.0.1), `--login`(auto) 1회 뒤 같은 프로필로 본 실행 4회) [실측]:

| 코드 | 1회 | 2회 | 3회 | 4회 | 성공 |
|---|---|---|---|---|---|
| 수정 전(`47a9f43`) | exit 0 | exit 2(다운로드 순간 창 꺼짐, `has been closed`) | exit 2 | exit 2 | **1/4** |
| 수정 후(`53a1575`) | exit 0 · 정리 0건 | exit 0 · 4건 | exit 0 · 8건 | exit 0 · 12건 | **4/4** |

  실행 전 `downloads` 행(전체/파일 없음): 수정 전 0/0 → 4/4 → 4/4 → 4/4 · 수정 후 0/0 → 4/4 → 8/8 → 12/12(끝 16/16). **발견**: 지운 행을 크롬이 다음 실행 중 **같은 id·GUID로 되살린다**(끝 DB id 1~16 = 1~4회 기록 전부, state 1) — History 밖 다운로드 캐시(`shared_proto_db` 추정 [추론])에서 복원하는 것으로 보이고, 정리 건수가 실행마다 4건씩 는다. 크래시는 없다(4/4). 가드: 같은 임시 프로필을 설치 크롬으로 띄운 상태에서 `profile_in_use` True · 정리 → `[WARN] … 브라우저가 떠 있음`·0건, 닫은 뒤 False(`lockfile`은 종료 때 사라짐).
- 규칙 [실측]: `.click(` 1건 · `mouse.`·`.fill(`·`.type(`·`.press(`·`drag_to`·`password`·`비밀번호` 0건 · 자격 증명·토큰 문자열 0 · py_compile 2파일 · config json.load · 코드펜스 짝수(들여쓴 펜스 포함 SKILL 16·report-fetch 8·checklist 6·last-audit 4) · UTF-8 · 커밋 내용 CR 0.
- 기록 오류 정정: 임의 결정 7 "설계 밖 config 키 4개" → **5개**.
- 효율: 도구 호출 약 50회 · 즉석 코드 81행(④ 하네스 `measure4.py`, 저장소 밖) · 사용자 권한 대기 1회(checklist 읽기).
- **검증 2가 볼 것**: ① 브랜치 diff(`47a9f43..`) = `53a1575`의 4파일(fetch_reports.py·test_fetch_reports.py·report-fetch.md·checklist.md) + 기록 커밋의 last-audit.md, config·data·다른 스크립트 불변 ② 시험 15 OK(아래 "검증 회차가 대조할 목록" 4의 "12 OK"를 대신한다; 브라우저 시험이 skip되면 적을 것; Windows clone은 `core.autocrlf=false`) ③ `clean_download_history`가 파일 있는 행을 지우지 않는지(시험 (나))·떠 있는 브라우저·잠김에서 0건인지·summary.json `steps`에 건수가 있는지 ④ `launch()`에 `or "chrome"`이 없고 config `browser_channel`이 `"chrome"`인지 ⑤ 위 "되살아남"이 결함인지 판단(크래시 재발 없음·건수 증가만) ⑥ 다음 실사용(실제 프로필) 첫 `[profile]` 줄 — 왕복 1~3 기록이 파일 없는 행으로 지워지고 실제 파일 있는 기록은 유지되는지 ⑦ 수정 전 1/4 → 4/4 재현은 설치 크롬 창이 있는 PC에서만 — 컨테이너 검증이면 시험 15개로 대신.

## 변경 파일 (브랜치 = 0a2bafb + 아래; 행수 `wc -l` · md5 앞 8자리) [실측]

| 파일 | 행수 | md5 | 무엇 |
|---|---|---|---|
| `scripts/fetch_reports.py` (신규) | 745 → 851(왕복 1) → 892(왕복 2) → 898(왕복 3) → **973**(수정 2) | 573d9720 → f963328f → c5e2f81b → 191fedca → **322ffe8b** | Playwright sync, PC 전용. `--dry-run`(브라우저 0·폴더 0, 할 일 표) / `--login`(전용 프로필 창, 폼 입력 0, 목록 URL 도달 확인 뒤 닫음) / 기본 실행(목록 → 링크 클릭 → 기간 읽기 → 다르면 프리셋 → `확인` → 다시 읽어 확인 → `조회하기` → `다운로드`(expect_download) → 저장 → `돌아가기` ×4 → 검사 → summary.json) / `--debug`(단계마다 스크린샷) / `--prev`(재집계 WARN) / `--today`(시험용). 클릭 호출 **`click_allowed` 한 곳**(`.click(` 1건), `allowed_actions` 밖·`forbidden_actions` 문구 → 클릭 안 하고 exit 1. 로케이터 role·text만(`locate`·`name_ok`). exit 0 성공 · 1 사용법/로그인 필요/금지 차단 · 2 보고서 하나라도 실패(`partial/`) |
| `tests/test_fetch_reports.py` (신규) | 393 → 441 → 467 → 468 → **595**(수정 2) | 3041b685 → 9d764993 → 44e1b3bb → 33368cd8 → **1ba3be2c** | 9개 → 11개 → 12개 → **15개**(수정 2: 프로필 정리 2·channel 1) 시험(아래 실측; 왕복 1 뒤 test_4 RangePicker형·지연, test_5 왕복 1 재현, 왕복 2 뒤 test_6 `조회하기` 비활성 추가). 끝에 실제 `data/2026-09` 4파일·config md5 전/후 출력 |
| `tests/fixtures/report-ui-fixture.html`·`login.html` (신규) | 177 → 192 → **201** · 22 | 1f0fe0d8 → 5de8b2ad → 5fe7110a → **dc4347dd** · 0614acb9 | 광고주센터 문구·흐름을 흉내 낸 로컬 가짜 화면(6-5 실물 기준: 목록 4행·`+ 새 보고서`·행마다 `삭제` / `← 돌아가기`·`보고서 형식 저장 ∨`·`다운로드`·기간 텍스트·달력·`조회하기` / 프리셋 12개·입력칸·`취소`·`확인`). 다운로드는 현재 기간으로 UI 형식 CSV(첫 줄·컬럼 원문·BOM·LF) 생성. `login.html`은 `?auto=1`이면 1.5초 뒤 "사용자가 로그인한 것"으로 처리. 실제 사이트와 무관 |
| `references/report-fetch.md` (신규) | 97 → 100 → 103 → 110 → **111**(수정 2) | 6074d1ba → fe822828 → c73a62fb → 9bb416a4 → **29824cc1** | 값 정의 정본 — PC 설치(3.14 대처법)·`--login`·매일 실행·결과·오류 대처·codegen 녹화 명령·금지 사항·UI 실물·시험·왕복 절차 |
| `config/report-config.json` | 140 (83→140) → **141**(왕복 2: `timeout_sec.click 15`) | bcf26fb7 → **b826b388** | `report_fetch` 블록 추가(기존 키 불변, diff 삽입만): `_comment`·`list_url`·`account_no 2580077`·`report_names`(시간대별 보고서·상세지역 보고서·검색어 보고서·필라테스 보고서 ↔ 시간대별·상세지역·검색어·키워드)·`period_rule`(other `이번달`·day1 `지난달`)·`columns`(4종 2행 원문 — `data/2026-09` 실물에서 복사)·`download_dir`·`profile_dir`(`~/saero-fetch/…`)·`browser_channel chrome`·`period_opener null`·`download_menu_item null`·`settle_sec 1.5`·`timeout_sec`(page 40·download 90·login 600)·`allowed_actions` 7·`forbidden_actions` 14 |
| `SKILL.md` | 480 (472→480) | afcae73c | 43행 "읽는 코드"에 `fetch_reports.py`(`report_fetch`) / **58~61행** "최근 30일까지만" → "`이번달`·`지난달` 프리셋으로 받는다(31일 달도 한 파일, 두 달 전 데이터도 조회됨 — 09-28 실측; 옛 전제 설명)" / **66~68행** "이번 달" 문장 → "PC에서 `scripts/fetch_reports.py`가 받아 오면 사용자가 4개를 올린다(수동 폴백: 보고서 형식에 `이번달`이 저장돼 있어 열기 → 다운로드)" / **72~74행** chunk 규칙 → "사용자 지정 기간이 30일로 잘릴 때만 쓰는 폴백" / 참고 문서·스크립트 절에 report-fetch.md·fetch_reports.py·test_fetch_reports.py 3항목. 63·127~129(현 64·130~132)행 유지. `archive.py` 코드 불변 |
| `audit/checklist.md` | 477 (465→477) → **481**(수정 2) | 49bc5252 → 515aa5da(왕복 2: 21 문구) → 3160128d(왕복 3: 24 파일명) → **5b11f72c**(수정 2: 갱신 이력·25·되돌리면 1행) | 버전 줄 **v4.6** / [의도된 동작] **21~24**(저장된 `이번달` 프리셋 의존 · 1일엔 `지난달`·58행 옛 전제 · 재집계 WARN 비차단·01:00 KST 이후 · 다운로드 파일명 규칙·partial·store는 세션) / [되돌리면 안 되는 것] **5행**(설정 변경 요소 클릭 금지·자격 증명 0·검사 전 store 금지·부분 실패 store 금지·좌표 클릭 금지) |
| `audit/last-audit.md` | (커밋 뒤 보고) | | 이 절 |

지시 밖 변경 0: `scripts/archive.py`·`compute.py`·`validate.py`·`compare.py`·`deploy.py`·`exclusions.py`·`data/`·`references/report-structure.md`·`exclusion-ui.md`·`css-and-layout.md` 불변(`git diff 0a2bafb --stat` = 위 8파일 + 이 파일).

## 임의 결정 (번호 = 사용자가 바꿀 단위)

1. **`columns`의 자리 = `report_fetch.columns`**(지시 2의 "config `columns`"를 최상위가 아니라 `report_fetch` 블록 안에). 값은 `data/2026-09` 4파일 2행에서 복사했고 시험 `test_config_columns_match_real_csv`가 실 CSV와 대조한다.
2. **저장 폴더·프로필 = `~/saero-fetch/downloads`·`~/saero-fetch/chrome-profile`**(`~` = `C:\Users\<사용자>`) — 저장소가 공개라 Windows 사용자명을 config에 적지 않으려고 `~` 표기. CLI `--download-dir`·`--profile-dir`로 덮어쓸 수 있다.
3. **임시 폴더 방식**: 다운로드는 먼저 `download_dir/partial/<날짜>/`에 받고, 4개 전부 검사 통과 + 노출합 일치일 때만 `download_dir/<날짜>/`로 옮긴다(지시 3의 "받은 파일은 partial/로 옮기고 정상 폴더에 남기지 않는다"와 결과 같음 — 실행 중 끊겨도 정상 폴더에 반쪽 상태가 안 남는다). 같은 날 재실행은 partial을 비우고 시작. 같은 날 앞선 **성공** 폴더는 건드리지 않는다(검사 통과본).
4. **exit 코드**: 로그인 필요·사용법·playwright 없음·금지 클릭 시도 차단 = 1 / 보고서 하나라도 실패(이름 틀림·기간 불일치·다운로드 없음·검사 FAIL·노출합 불일치) = 2. 지시 9의 "이름 하나 틀리게 → exit 2"에 맞췄다.
5. **라벨 판정은 파이썬 쪽 `name_ok`**: 요소 문구 = 라벨이거나 앞뒤에 기호·공백만 붙은 것(`← 돌아가기`·`다운로드 ∨`)까지 같은 요소로 본다. Playwright에 정규식을 넘기면 JS `\W`가 한글을 비단어로 취급해 `보고서 형식 저장 ∨`가 `저장`에 걸리는 것을 시험에서 확인해 이렇게 했다 [시험].
6. **URL 폴링은 `page.evaluate("location.href")`**: sync API의 `page.url`은 다른 호출이 있어야 갱신돼 `--login` 대기가 끝나지 않았다(시험에서 실측) [시험].
7. **설계 밖 config 키 5개**(첫 왕복에서 화면이 예상과 다를 때 코드 수정 없이 맞추려고): `period_opener`(null = 기간 텍스트 클릭, 문자열이면 달력 아이콘 등 그 이름 요소)·`download_menu_item`(null = 버튼 하나, 문자열이면 다운로드 뒤 그 메뉴 항목 — 같은 동작 키 `download`)·`settle_sec`·`timeout_sec`·`browser_channel`. 전부 `allowed_actions` 안에서만 동작한다.
8. **시험·가짜 화면을 저장소에 넣었다**(지시 12의 산출물 2개 외 추가): 검증 회차가 네이버 접속 없이 dry-run 무변경·금지 차단·부분 실패·미로그인 경로를 재현할 수 있게. 컨테이너에 크롬 141(`/opt/google/chrome`)·번들 크로미움(`/opt/pw-browsers`)·Playwright 1.56.0이 있어 헤드리스로 돈다 [실측] — 없는 환경이면 브라우저 시험만 skip(순수 시험 6개는 돈다).
9. **재집계 감지의 대상 = 날짜 컬럼이 있는 3종**(키워드·검색어·상세지역)의 겹치는 날짜 일별 노출·클릭·비용. 시간대별은 날짜가 없어 비교 안 함. `--prev`는 직전 다운로드 폴더(원본 이름)든 저장소 `data/YYYY-MM`(키워드.csv 이름)이든 컬럼으로 종류를 판별해 받는다.
10. **첫 줄 이름 검사 추가**(헤더 `"<보고서 이름>(…"` = `report_names` 키) — 지시 2 목록에 없던 검사. 링크를 잘못 눌러 다른 보고서를 받았을 때 잡힌다.
11. **`archive.py` docstring 5·16~17행의 "최근 30일까지만" 문구는 손대지 않았다**(지시 6 범위 = SKILL.md, "archive.py --chunk 코드는 유지") — 같은 옛 전제가 남아 있으니 조정에서 문구만 고칠지 결정(코드 변경 없음, 검증 회차 grep 잔존 목록에 넣었다).
12. `_playwright()`의 `PWTimeout` import는 쓰지 않는다(noqa) — 정리는 다음 수정 때.

## 실측 (이 세션, 브랜치 코드) [실측]

- `python3 -m py_compile` 2파일 통과 · config `json.load` 통과(`report_fetch` 15키) · md 코드펜스 짝수(SKILL 10·report-fetch 8·checklist 6) · UTF-8·CRLF 0.
- `python3 -W error::ResourceWarning tests/test_fetch_reports.py` → **Ran 9 tests · OK**(34초), "실제 data/2026-09·config md5 전/후 동일: True". 시험 내용: ① config `columns` = 실 CSV 4파일 2행, 계정 2580077 ② 기대 기간: 09-28 → `이번달` 09-01~09-27 · 10-01 → `지난달` 09-01~09-30 · 09-01 → 08-01~08-31 · 03-01 → 02-01~02-28 ③ `--dry-run`: 가짜 `playwright` 패키지(import 즉시 실패)를 앞에 두고 exit 0·표 4행·폴더 0개 생성, 같은 환경 `--login`은 exit 1 "playwright가 없습니다" ④ `check_file`·`cross_check`: 실 4파일(09-01~09-26) 전부 PASS·노출합 3종 동일, 기대를 09-27로 주면 "기간 = 기대" FAIL, 이름 다르면 FAIL, 합성 파일(행 0·컬럼 추가·계정 다름·헤더 형식) 전부 FAIL ⑤ `--prev`: 사본 동일 → WARN 0(겹침 26일), 9/10 노출 +1 → `[WARN] 키워드 … 2026.09.10.` 1건 ⑥ `click_allowed`: `보고서 형식 저장 ∨`·`+ 새 보고서 ∨`·`삭제`·`로그인`·`×` → SystemExit "금지 요소", 클릭 0 / 모르는 동작 `save_format` → "허용 목록 밖" / config에 모르는 동작을 넣으면 시작부터 거부 / 소스 `.click(` 1건·`mouse.`·`fill(`·`type(`·`press(`·`drag_to`·`password`·`비밀번호` 0건 ⑦ [시험] 가짜 화면: `--login`(auto) → "목록 URL 도달 · 4/4개" → 본 실행 exit 0, `2026-09-28/` 4개(원본 이름)+summary.json+debug/, partial 없음, 4개 모두 `preset_clicked false`(저장된 `이번달`), 키워드 파일 BOM·LF·첫 줄 `"필라테스 보고서(2026.09.01.~2026.09.27.),2580077"`·컬럼 원문·54행 ⑧ [시험] `--today 2026-10-01` → 기대 `지난달`, 4개 모두 프리셋 클릭 → 헤더 09-01~09-30, 노출합 일치 ⑨ [시험] `--prev` = 09-28 폴더 → WARN 0(겹침 27일), 검색어 9/10 노출을 바꾼 사본 → `[WARN] 검색어` 1건, exit 0(막지 않음) ⑩ [시험] `report_names`에 `검색어 보고서X` → **exit 2**, 정상 폴더 없음, `partial/2026-09-28/` CSV 3개+summary.json(`result partial`·`exit_code 2`·성공 3), `*_no_link.png` 스크린샷 ⑪ [시험] 로그인 안 된 프로필 → exit 1 "--login", CSV 0, `--login`도 시간 안에 실패 exit 1.
- 수동 `--debug` 실행(가짜 화면, 10-01 경로): 스크린샷 17장(`01_list` → `_opened`·`_period_popup`·`_queried`·`_back` ×4), summary.json에 `steps`·`period_read`(how `range-text`)·검사 결과·합계. 저장소 `data/2026-09`를 `--prev`로 주면 값이 달라 WARN 3건(가짜 데이터라 정상).
- 컨테이너에서 `pip install playwright` 성공(1.56.0), `playwright install chromium`은 경고 없이 끝났고 브라우저는 `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`의 chromium-1194 + `/opt/google/chrome`(channel chrome, 141.0.7390.37) — 이 세션 환경 [실측]. 광고주센터 접속은 시도하지 않았다(0절 차단 + 설계상 PC 실행).
- 하지 않은 것(PC 몫): 실제 광고주센터 실행·실제 DOM 문구 확인·같은 날 손으로 받은 4개와의 바이트 대조.

## PC 왕복 기록 (지시 8 — 최대 3회, 결과가 오면 여기에 추가)

- **왕복 1 결과(2026-09-28, 사용자 콘솔 화면 2장)** [실측]: PC Python 3.12(cp312 휠)·pip 25.0.1·Playwright **1.63.0**·`playwright install chromium` = Chrome for Testing 153(v1243)·설치된 크롬 channel 사용. `--dry-run` 표 4행(경로 `C:\Users\<사용자>\saero-fetch\…`) OK · `--login` → `[OK] 목록 URL 도달 · 보고서 이름 4/4개 보임` · 본 실행 `--debug`: `클릭 open_report: '시간대별 보고서'` → `[시간대별] 보고서 열림`(= `돌아가기` 확인) → **`fail (기간을 읽지 못함(기간 텍스트를 찾지 못함))`** → 상세지역·검색어·키워드 **`목록에 보고서 링크 '…' 없음`** → `[FAIL] 4개 중 성공 0 · 실패 4`, partial에만, store 금지(부분 실패 경로는 의도대로 동작). 확정된 것: 목록 링크 텍스트 = `report_names` 키 · `돌아가기` 문구 존재 · 로그인 프로필 재사용 OK. 미확정: 기간 표시 DOM(텍스트가 아니거나 늦게 그려짐 [추론]) — summary.json·스크린샷은 미수령.
- **왕복 1 뒤 수정(커밋 `0c2f51c`, 같은 브랜치)**: ① **코드 결함** — 보고서 하나가 실패하면 목록으로 돌아가지 않아 나머지가 연쇄 실패 → `back_to_list()` 신설(성공·실패 모두 다음 보고서 전에 `돌아가기` 클릭 → 목록 판정 `on_list` = 목록 URL + 보고서 링크 **2개 이상**(제목 글자는 세지 않음) → 안 되면 목록 URL로 이동). 시험 `test_5`가 이 결함을 재현(첫 보고서 기간 없음 → exit 2, 나머지 3개 다운로드). ② `read_period` 3단계(가장 짧은 기간 텍스트 → 날짜 값을 가진 보이는 input 2개(evaluate 1회) → 본문 한 줄의 날짜 2개) + 표시 지연 대기(`timeout_sec.page`) + `DATE_RE` 끝 점·`RANGE_RE` 구분자 선택(아이콘 화살표 대비). 팝업 열기 대상 `period_target`(텍스트 → 날짜 textbox → config `period_opener`). ③ 스크린샷마다 `.aria.txt`(접근성 트리)·`.inventory.json`(날짜 요소·input·button·link 목록) 저장 — 왕복 2에서 DOM 확정용, 화면 문구만. ④ `click_allowed` 가드가 `inner_text`+`aria-label`+`title`+`input_value`를 본다. ⑤ `locate(text_fallback=False)`로 링크·버튼 역할 우선. 시험 **11개 OK**(`-W error::ResourceWarning`), `.click(` 1건·입력/좌표 API 0건 유지.
- **왕복 2 결과(2026-09-28, 콘솔 전문)** [실측]: `git pull` f059458→0bffa8f. 4개 모두 `보고서 열림` → **`기간 읽음 2026.09.01.~2026.09.27. (range-text)`** → `기간 = 기대(저장된 프리셋)` → 목록 복귀 정상(왕복 1의 두 문제 해결 확인: 기간 표시는 지연 렌더링이었고 표기는 기간 텍스트). 실패 4/4: `클릭 query: '조회하기'` → `TimeoutError: Locator.click: Timeout 30000ms exceeded.`(클릭 가능해지길 30초 대기 = 버튼 비활성 [추론]; 첫 줄만 출력해 원인이 안 보였다). partial에만·store 금지 유지. summary.json·debug는 미수령.
- **왕복 2 뒤 수정(커밋 `08136a9`)**: ① `조회하기`는 **활성일 때만** 클릭 — 저장된 형식으로 열면 결과가 자동 조회되고 버튼이 비활성(회색)이라고 판정(6-5 "회색 — 조회 전"·수동 흐름 "열기 → 다운로드"·메모리 09-28 "열기 → 다운로드만"과 일치); 비활성이면 `조회하기 비활성 → 건너뜀`을 steps에 남기고 다운로드로. 기간을 바꿔 `확인`한 뒤(매월 1일)는 활성이면 클릭. ② 모든 클릭에 `timeout_sec.click`(기본 15초, config에 명시) — 30초 기본값 제거. ③ 클릭 실패 원인을 호출 로그에서 골라 출력(`click_reason`: 비활성/가림/안 보임/움직임/사라짐) + `summary.json` `error_detail`(호출 로그 800자). ④ 가짜 화면 `query=disabled` 모드(자동 조회·비활성·`확인` 뒤 활성, 다운로드는 **조회된 기간**으로 만들어 조회하기를 잘못 건너뛰면 기간 검사에 걸림) + `test_6`(평일 건너뜀·`queried false` / 1일 `확인` 뒤 4회 클릭·헤더 09-01~09-30). 시험 **12개 OK**. `.click(` 1건·입력/좌표 0건 유지. checklist [의도된 동작] 21 문구에 반영.
- **왕복 3 결과(2026-09-28, 콘솔 전문) — 성공** [실측]: `git pull` 0bffa8f→68028c8 · 4개 모두 `보고서 열림 → 기간 읽음 09.01~09.27 (range-text) → 기간 = 기대 → 조회하기 비활성(저장된 형식으로 이미 조회됨) → 건너뜀 → 클릭 download → 저장 → 클릭 back → downloaded` · 검사 전부 PASS · `[PASS] 4개 다운로드·검사 통과 → C:\Users\<사용자>\saero-fetch\downloads\2026-09-28`. WARN 4건 = 파일명(실제 `시간대별 보고서,2580077.csv` ≠ 옛 기대 `_보고서_`) → 아래 수정으로 해소. (사용자가 스크립트를 Downloads 폴더에서 실행해 한 번 헛돎 → 지시문에 `cd` 추가, `68028c8`.)
- **최종 실행 결과(왕복 3, 2026-09-28 KST 아침)**: 왕복 횟수 **3**(1: 기간 못 읽음·목록 미복귀 / 2: 조회하기 30초 초과 / 3: 성공). 4개 헤더 `"시간대별 보고서(2026.09.01.~2026.09.27.),2580077"` · `"상세지역 보고서(…)"` · `"검색어 보고서(…)"` · `"필라테스 보고서(…)"` 전부 계정 2580077 · 기간 09-01~09-27. 행수·합계(노출·클릭·비용): 시간대별 24행 7,628·259·314,904 / 상세지역 1,017행 7,628·259·314,910 / 검색어 1,532행 6,451·259·314,906 / 키워드 462행 7,628·259·314,902 — 노출합 3종 일치, 클릭 4종 모두 259, 비용은 보고서마다 몇 원 차이(행 단위 반올림, 탐색 기준선 1절 ±1원/일 실측과 같은 유형, 검사 대상 아님). 실제 DOM에서 확정한 것: 기간 = 텍스트(지연 렌더) · `돌아가기`로 보고서 화면 판정 · 자동 조회로 `조회하기` 비활성 · `다운로드` 버튼 하나(메뉴 없음) · 파일명 `<이름>,2580077.csv`. 손으로 받은 같은 날 4개와의 바이트·합계 대조(검증 목록 6)는 **미실측**(사용자가 오늘 손으로 받은 파일이 있으면 검증 회차에서).
- **왕복 3 뒤 수정(커밋 `cb9f9e7`)**: `expected_filenames()` — 기대 파일명을 실측 `<이름>,<계정>.csv`로, 손으로 받은 `<보고서명>_보고서_<계정>.csv`도 정상(둘 밖만 WARN). 가짜 화면 다운로드 이름·시험 기대값 갱신(12개 OK). references 4·7·9절·checklist [의도된 동작] 24 갱신. 코드 흐름 변경 0.
- 왕복 0 지시(참고, 완료됨): **왕복 1 지시**(references/report-fetch.md 1·2·3·9절): PC 저장소 폴더에서 `git fetch && git checkout feat-report-fetch && git pull` → `pip install playwright` → `python -m playwright install chromium` → `python scripts\fetch_reports.py --dry-run` → `python scripts\fetch_reports.py --login`(창에서 직접 로그인·`로그인 상태 유지`) → `python scripts\fetch_reports.py --debug` → 콘솔 출력 전문·`downloads\<날짜>\`(또는 `partial\<날짜>\`)의 `summary.json`·`debug\` 스크린샷·성공 시 CSV 4개를 세션에 첨부. 첨부에 아이디·비밀번호가 없는지 확인.
- 최종 실행 결과(왕복 뒤 기록할 것): 왕복 횟수 __ · 4개 헤더 `…(2026.09.01.~2026.09.__.),2580077` · 노출·클릭·비용 합계 4줄 · 손으로 받은 같은 날 4개와 바이트(md5)·합계 대조 결과 · 실제 DOM에서 확정한 문구(기간 팝업 여는 요소·`돌아가기` 역할·다운로드 메뉴 유무).

## 검증 회차가 대조할 목록 (브랜치 clone에서, 토큰·API 키·네이버 로그인 없음)

1. 기준값: 위 표의 행수·md5, `git diff 0a2bafb --stat` = 8파일 + last-audit.md. 문법 `py_compile` 2파일·config `json.load`·코드펜스 짝수·UTF-8.
2. **코드 grep**: `scripts/fetch_reports.py`에서 `.click(` **1건**(`click_allowed` 안), `mouse.`·`.fill(`·`.type(`·`.press(`·`drag_to`·`password`·`비밀번호` **0건**; config `forbidden_actions`에 `+ 새 보고서`·`보고서 형식 저장`·`삭제`·`×`·`로그인`·`비밀번호`가 있고 `allowed_actions` 7키가 코드 `ACTIONS`와 같음; 저장소 전체에 자격 증명·쿠키·토큰 문자열 0(`*.keys.json`·`secrets/`는 .gitignore).
3. **dry-run 브라우저 0**: `python3 scripts/fetch_reports.py --dry-run --today 2026-09-28 --download-dir <새 폴더> --profile-dir <새 폴더>` → exit 0, 표 4행(기대 `이번달` 2026.09.01.~2026.09.27.), 두 폴더 생성 안 됨, `git status` 변경 0. `--today 2026-10-01` → `지난달` 2026.09.01.~2026.09.30. 시험 `test_dry_run_no_browser_no_files`(가짜 playwright 패키지)도 통과.
4. `python3 -W error::ResourceWarning tests/test_fetch_reports.py` → **12 OK**(왕복 2 뒤; 왕복 1 뒤 11, 처음 9), 실제 data·config md5 동일. 왕복 2 재현 `test_6_query_button_disabled_when_already_queried`(`query=disabled`: 평일 `조회하기` 클릭 0·`queried false`·성공, 1일 `확인` 뒤 클릭 4회·헤더 09-01~09-30)가 포함됐는지. 브라우저 시험이 skip되면 그 사실을 적는다(환경에 크로미움 없음). 왕복 1 재현 `test_5_period_missing_on_one_report_others_still_downloaded`(첫 보고서 기간 없음 → exit 2·partial 3개·`_no_period.aria.txt`·`.inventory.json` 생성)와 `test_4_inputs_ui_with_delay_and_day1_preset`(input 2개형·900ms 지연 → `period_read.how == "inputs"`, 1일엔 textbox 클릭 → 프리셋)이 포함됐는지.
5. **실행 4개 파일 첫 줄·컬럼·노출합**: (가) 가짜 화면 시험 ⑦의 파일 4개 첫 줄 `"<이름> 보고서(2026.09.01.~2026.09.27.),2580077"`·2행 = config `columns`·키워드=시간대별=상세지역 노출합 (나) PC 왕복 결과가 있으면 그 `summary.json`의 `check.checks` 전부 `ok true`·`cross.ok true`, 4개 헤더가 실행일 기준 1일~어제.
6. **같은 날 손으로 받은 4개와 대조**(PC 결과 수령 뒤): 사용자가 같은 날 광고주센터에서 직접 받은 4개와 스크립트 결과 4개의 md5·행수·노출/클릭/비용 합계가 같은지(행 순서가 같으면 바이트 동일, 다르면 합계 동일 — 탐색 기준선 1절 "행 순서 무관").
7. **부분 실패 시험**: config 사본에서 `report_names`의 `검색어 보고서`를 `검색어 보고서X`로 바꿔 가짜 화면 실행(시험 ⑩ `test_2_partial_failure_wrong_name_exit2`) → **exit 2**, `download_dir/<날짜>/` **없음**, `partial/<날짜>/`에 CSV 3개+summary.json, 콘솔 "성공 3 · 실패 1 … store 금지". 미로그인 → exit 1(시험 ⑪).
8. **부트스트랩 md5 불변**: `/mnt/skills/plugins/saero-ad-report/SKILL.md` 44행 md5 `97a3e194388b2ee75ad8fc81f9e47f78`.
9. **checklist 대조**: 버전 줄 v4.6 / [의도된 동작] 21~24 / [되돌리면 안 되는 것] 표에 fetch_reports 5행(설정 변경 요소·자격 증명 0·검사 전 store·부분 실패·좌표 클릭) — 각 행의 "위치"가 실제 함수명과 맞는지(`click_allowed`·`locate`·`name_ok`·`cmd_login`·`check_file`·`cross_check`·`cmd_fetch`).
10. 문서 = 코드: SKILL.md 66~68행 ↔ report-fetch.md 3절 ↔ `cmd_fetch`/`fetch_one` 순서 / 옛 문구 grep: SKILL.md에 "최근 30일까지만 내려준다" 0건(59행의 "옛 전제" 설명 인용은 정상), "다음 달 1일에 한 달치(31일)가 30일 제한에 걸려" 0건 / 잔존 목록: `scripts/archive.py` 5·16~17행 docstring(임의 결정 11, 조정 판단).
11. 지시 밖 변경 0: `data/`·`compute.py`·`validate.py`·`archive.py`·배포본 불변(md5).

## 원래 제안·지시를 바꾼 곳 (B 검증이 볼 것)

- `columns`를 `report_fetch` 블록 안에(임의 결정 1). 설계 밖 config 키 `period_opener`·`download_menu_item`·`settle_sec`·`timeout_sec`·`browser_channel`(7). 시험·가짜 화면 추가(8). 첫 줄 이름 검사 추가(10). SKILL.md 43행·참고 절 3항목은 지시 6의 행 목록 밖 추가(새 파일을 가리키는 자리가 없으면 고아가 되므로).
- 지시 3 "받은 파일은 partial/로 옮기고"를 "partial/에서 받아 성공 시에만 옮김"으로(3) — 결과 상태는 같다.
- 지시 1의 "기간 텍스트를 읽어 … 프리셋 클릭 → 확인 → 조회하기"에 **"확인 뒤 다시 읽어 기대와 같은지"** 한 단계를 넣었다(설계안 필수 "쓰기 후 다시 읽어 확인"과 같은 방향; 다르면 그 보고서는 조회·다운로드 없이 실패).
- 탐색 기준선 6-6의 "기간 입력칸 타이핑 또는 프리셋" 중 **프리셋만** 구현(지시대로 폼 입력 0 — 두 달 걸친 기간을 만들 수 있는 코드 자체가 없다).

## 다음에 볼 것 (순서대로)

1. ~~PC 왕복~~ 완료(3회, 성공). 2. 검증 회차(다른 세션, 위 목록 — 브랜치 최종 해시 기준) → "합쳐도 된다" 뒤 조정에서 main 병합. 3. 병합 뒤 첫 실사용은 **수동 1회**(결정 7): 같은 날 손으로 받은 4개와 대조(목록 6) → 결과를 "첫 실사용 기록"에; **10월 1일 실행**이 `지난달` 프리셋 경로(팝업·`확인`·`조회하기` 활성)의 첫 실측이므로 그날은 `--debug`로. 4. 2회차 후보: PC에서 store·push까지 / A(API 교차 검증) / archive.py docstring 문구 / `--prev` 기본값(직전 성공 폴더 자동 선택).

## 마무리 기록(이번 회차)

- 커밋 1 `79ad780`(코드·config·references·tests·SKILL.md), 커밋 2 `f059458` = 이 절 + checklist v4.6, 커밋 3 `0c2f51c` = 왕복 1 반영(코드·시험·가짜 화면·references), 커밋 4 `0bffa8f` = 이 절 갱신, 커밋 5 `08136a9` = 왕복 2 반영(코드·시험·가짜 화면·references·config·checklist 21), 커밋 6 `8c697d8` = 이 절 갱신, 커밋 7 `68028c8` = 지시문 cd 줄, 커밋 8 `cb9f9e7` = 왕복 3 반영(파일명 실측), 커밋 9 = 이 절 갱신(최종)(author `LeeKwanBeom <322668067+LeeKwanBeom@users.noreply.github.com>`). 브랜치 `feat-report-fetch`만 push(클라우드 push 성공 — 프록시 403 없음 [실측]), main 0. 토큰은 첨부 파일에서 credential helper로만 읽었고(2개 줄 중 4번째 줄만 유효, 1번째 줄은 403) 옮겨 적지 않았다.
- 네이버 계정: 읽기·쓰기 0. 배포 저장소 0. 부트스트랩 md5 불변.

---

# 기능 추가 탐색 기준선(보고서 자동 수집, 2026-09-28)
점검일: 2026-09-28 (기능 추가 회차 — **탐색·설계만**, Fable, 웹 claude.ai 세션). SKILL.md·scripts·config·data·checklist.md **변경 없음**. 네이버 계정 쓰기 호출 **0**(API·UI 어느 쪽도 호출 자체가 안 됨 — 0절). 리포트 갱신·배포 **없음**. 산출물은 이 절(1차 커밋, 이 파일만)과 사용자 폴더 사본 `saero-ad-report_보고서자동수집_탐색_2026-09-28.md`, PC 실행용 프로브 `naver_report_probe.py`·대조 `compare_ab.py`(회차 폴더·사용자 폴더에만, 저장소 미포함). 구현은 사용자가 아래 "내가 고를 항목"을 고른 뒤 별도 회차(브랜치 `feat-report-fetch`).
추가할 기능: 1단계 "CSV 받기"의 수동 부분(광고주센터 로그인 → 다차원 보고서 4개 기간을 이번 달 1일~어제로 조회 → CSV 다운로드)을 자동화해 사람 손 없이 4개 파일이 `data/YYYY-MM/`에 놓이게 한다. store 이후(combine·compute·배포)는 그대로.
점검 대상(전부 저장소에서 받은 것): `saero-ad-report-skill` @c273bd5(main) — SKILL.md(472행, md5 9c618593…) · audit/checklist.md(465행, v4.5) · audit/last-audit.md(1,785행) · references/exclusion-ui.md(129행) · scripts/archive.py(196행) · scripts/exclusions.py(944행) · scripts/ingest.sh(15행) · config/report-config.json · data/2026-08·2026-09 4종씩 / 공식 API 문서 = `naver/searchad-apidoc` gh-pages @ed3174a(2026-09-16) `assets/json/ncc-report.json`·`master-report.json`·`ncc-heroes-ncc.json`·`assets/i18n/markdown-en-US.json`(`#/tags/StatReport` 보고서 사양)·`_posts/`(공지 33건 중 보고서 관련) + master @0aa7a76(php·java·python 샘플) git clone / 광고주센터 화면·API 호출: **직접 접속 전부 미실측(0절)**, 사용자 스크린샷 **미수령**.
효율: 벽시계 약 55분(16:48 UTC clone → 17:16 1차 push → 17:43 2차 push, 사용자 PC 프로브 대기 포함) · 도구 호출 약 80회 · 즉석 코드 512행(`ui_csv_facts.py` 58 — UI CSV 형식 실물·09-25 A측 / `naver_report_probe.py` 319 — PC 실행 API 프로브 / `compare_ab.py` 135 — A/B 대조표. 전부 회차 폴더, 저장소 미포함).
표기: [실측] 이 세션에서 직접 확인 / [문서] 공식 API 문서·저장소 원문 / [기록] 이 파일의 과거 회차 / [추론] 확인 못 함 / [미실측] 차단·미수령으로 시도 실패.

## 0. 결정적 실측 — 이 세션(웹)의 경로와 첨부 [실측]

| 경로 | 시도 | 결과(원문) |
|---|---|---|
| 클라우드 컨테이너 curl | `api.searchad.naver.com/stat-reports`·`/master-reports` · `ads.naver.com/manage/ad-accounts/2580077/sa/reports` · `manage.searchad.naver.com/` (대조군 `github.com`) | 4개 전부 **HTTP 403 `x-deny-reason: host_not_allowed`** / github 200. 프로브 스크립트로 보내도 같은 403(`Host not in allowlist: api.searchad.naver.com`) |
| web_fetch(근거 아님 — 채널 확인만) | 보고서 목록 URL | `SITE_BLOCKED` |
| Claude in Chrome · 내장 브라우저 · PC 셸(device_bash) | — | **이 세션 도구 목록에 없음** → 시도 불가(09-27 기준선 0절의 4경로 중 3개는 재실측 못 함) |
| GitHub API·gist(master-report 컬럼 사양) | `api.github.com/gists/186ca42e…` · `gist.githubusercontent.com` | rate limit 403 / 프록시 403 → **master-report 파일 컬럼 사양 미열람** |
| 첨부 | `/mnt/user-data/uploads/` 16:48·16:56·16:58 UTC | **비어 있음** — push 토큰·스크린샷(목록 화면) 모두 미수령 → 1차 커밋은 로컬 작성까지, push·재clone 확인 못 함 |

- 뜻: 09-27과 같다 — 스킬이 도는 환경에서는 API도 화면도 못 연다. **경로 C(사용자 PC PowerShell 실행)가 유일한 실측 통로**이며, 이번 회차의 실측(A/B의 B측·이름 매핑·파일 형식·집계 시각)은 아래 프로브를 PC에서 돌린 결과 파일로 채운다.

## 1. 끼어들 자리와 지금 사용자에게 묻는 문구 [실측: @c273bd5 원문]

| 파일·행 | 원문 | 자동화 뒤 |
|---|---|---|
| SKILL.md 65 | `- **이번 달**: 사용자가 매일 **이번 달 1일~어제**로 4개를 받아 준다. 같은 달 파일을 덮어쓴다.` | "PC 스크립트가 만든다"로 바뀔 문장 |
| SKILL.md 63 | `(네이버 원본 그대로, 첫 줄 기간 헤더 포함. 키워드 보고서 원본 파일명은 \`필라테스_보고서_…\`)` | 원본 = "UI 형식과 같은 생성 CSV"로 정의 갱신(설계안 A) |
| SKILL.md 81~82 | `한 번에: \`scripts/ingest.sh <스킬 저장소 토큰파일> <업로드CSV> [...]\`` | 입력이 업로드 CSV → 생성 CSV 4개(경로만 바뀜, ingest.sh 불변 가능) |
| SKILL.md 84~89 (1단계 1항) | `업로드 파일을 보관한다(종류는 컬럼으로, 달은 첫 줄 기간 헤더로 판별)` … `두 달에 걸친 파일(예: "최근 30일")은 거부된다 → 사용자에게 **이번 달 1일~어제**로 다시 받아 달라고 한다. 기간 끝이 보관본보다 이른 파일(옛 다운로드)도 거부된다.` | 거부 규칙은 그대로 두고, 생성기가 애초에 그런 파일을 만들지 않게 한다(4절 2·3) |
| SKILL.md 127~129 | `> 이번 파일이 '최근 30일' 같은 자동 기간으로 받아진 것 같습니다. 네이버 광고시스템 다운로드 화면에서 '사용자 지정 기간'을 선택하고 **이번 달 1일 ~ 어제**로 맞춰서 4개 파일을 다시 받아주세요.` | 자동 수집이 정상이면 나올 일 없음 — 수동 폴백 문구로 유지 |
| SKILL.md 69~71 | `**31일로 끝나는 달**: … **말일 하루치 4개**를 따로 받아 \`store --chunk\`로 조각을 더한다.` | API는 하루 단위라 이 예외가 사라짐(설계안 A는 달 안의 날짜를 모아 한 파일로 만들 수 있다) |
| SKILL.md 108 | `모든 CSV는 첫 줄이 기간 헤더이므로 \`pandas.read_csv(path, skiprows=1)\`로 읽는다.` | 유지(생성 CSV도 같은 헤더) |
| last-audit.md 923(09-27 갱신 회차) | `- 다음 회차 대조: 이번 달 파일 9/1~어제로 덮어쓰기 / …` | 매 회차 첫 줄이 이 수동 단계 |
| archive.py 51 `HEAD_RE` | `\((\d{4})\.(\d{2})\.(\d{2})\.~(\d{4})\.(\d{2})\.(\d{2})\.\)\s*\"?,\s*(\d+)` | 생성 CSV 첫 줄이 이 정규식에 맞아야 함 |
| archive.py 59~66 `read_head` / 69~76 `kind_of` | utf-8-sig로 첫 줄 읽기 / `{"광고그룹","키워드"} ⊂ 컬럼 → 키워드`, 그 외 `검색어`·`상세지역`·`시간대별` 컬럼명으로 판별 | 컬럼명이 정확히 같아야 함 |
| archive.py 79~100 `store` | 83~84 두 달 걸침 → FAIL / 91~95 기간 끝이 보관본보다 앞이면 FAIL(`--force`) / 96~99 같은 달·종류 덮어쓰기 | 생성기는 `--force`를 쓰지 않는다(4절 3) |
| archive.py 111~181 `combine` | 조각 경계 4종 일치·시간대별·상세지역 노출합 = 키워드·일별 최솟값 = open_date·계정 동일 | 생성 CSV 4개가 이 검사를 통과해야 store 이후 무변경 |

**자동 생성 파일이 store·combine을 그대로 통과하는 조건**(UI CSV 실물 = `data/2026-09` 4파일 [실측]):
- 첫 줄 `"<이름> 보고서(YYYY.MM.DD.~YYYY.MM.DD.),2580077"` — 이름은 `필라테스`(키워드 보고서의 저장 이름)·`검색어`·`상세지역`·`시간대별`. 계정번호 **2580077**(광고주센터 URL 번호 = CSV 헤더; API `CUSTOMER_ID` 4480035와 다름 — [의도된 동작] 20).
- 인코딩 **utf-8-sig(BOM)**, 줄바꿈 **LF**(CRLF 0), 값에 따옴표 0(첫 줄만 따옴표). 2행 컬럼명 정확 일치: 키워드 13열 `캠페인,광고그룹,키워드,일별,매체이름,PC/모바일 매체,검색/콘텐츠 매체,노출수,클릭수,클릭률(%),평균 CPC,총비용,평균노출순위` / 검색어 16열(`검색어,검색 유형,일별,노출수,클릭수,클릭률(%),평균 CPC,총비용` + 전환 8열) / 상세지역 20열(`상세지역,일별,노출수,클릭수,클릭률(%),평균 CPC,총비용,평균노출순위` + 전환 12열) / 시간대별 10열(`시간대별,노출수,클릭수,클릭률(%),평균 CPC,총비용,평균노출순위,총 전환수,총 전환율(%),총 전환매출액(원)`). **전환 관련 열은 세 파일 모두 전부 0**(이 계정은 전환 추적 없음) [실측].
- 일별 `YYYY.MM.DD.`(끝에 점). 숫자: 노출·클릭·CPC·비용 정수, 클릭률 `0`/`6.5`/`6.33`(최대 2자리, 후행 0 없음), 평균노출순위 `2`/`1.3`(최대 1자리). 시간대별 라벨 `00시~01시` … `23시~00시` 24행.
- **행 순서는 무관**(combine은 pandas 합산·groupby, store는 복사) — 키워드 파일은 캠페인 순만 확인되고 그룹·일자 순서는 코드포인트 정렬이 아님(UI 내부 순서) [실측] → 생성 CSV가 UI와 바이트 동일할 필요는 없다. 단 `일별` 컬럼의 조각 경계는 헤더 기간 안이어야 한다.
- combine이 요구하는 정합: 조각(=달)마다 시간대별·상세지역 노출합 = 키워드 노출합. UI 09-25 하루치는 194/194/194로 맞지만 **총비용은 키워드 12,014 vs 검색어·상세지역 12,015로 1원 어긋남**(행 단위 반올림) [실측] — 비용 정합은 combine·validate가 보지 않으므로 통과에는 영향 없음. A/B 판정 기준(결정 4)에 반영.

## 2. 대상 조사

### 2-a. 공식 API [문서] — 대용량 보고서(STAT-REPORT) + 요약 통계(/stats) + 마스터

| 항목 | 값 | 표기 |
|---|---|---|
| base·인증 | `https://api.searchad.naver.com`, 헤더 `X-Timestamp`·`X-API-KEY`·`X-Customer`(4480035)·`X-Signature`=base64(HMAC-SHA256(secret, `"{ts}.{METHOD}.{uri}"`)) — exclusions.py `NaverApi.sign`과 동일 | [문서·코드] |
| 보고서 작업 생성 | `POST /stat-reports` body `{"reportTp": …, "statDt": "YYYYMMDD"(KST)}` → `{reportJobId, reportTp, statDt, status, updateTm, downloadUrl}` | [문서 ncc-report.json] |
| 상태 | `GET /stat-reports/{reportJobId}` — status `REGIST`·`RUNNING`·`WAITING` → `BUILT`(완료) / `NONE`(데이터 없음) / `ERROR` / **`AGGREGATING`(집계 미완)** | [문서] |
| 다운로드 | `downloadUrl`을 GET — 서명 uri는 **`/report-download`**(php `restapi.php` DOWNLOAD 245행 `getHeader("GET", "/report-download")`) | [문서: 샘플 코드] |
| 정리 | `DELETE /stat-reports/{reportJobId}` 204 · `GET /stat-reports` 목록 | [문서] |
| **하루 = 작업 1개** | `statDt`가 단일 일자 → 이번 달 1일~어제(오늘 기준 27일) × 종류 2 = **54작업**(첫 회차), 이후 **매일 2작업**(전날 증분) | [문서·추론] |
| 제공 기간 | AD_DETAIL은 "요청 시점부터 과거 30일"(2017-06-21 릴리스 노트) — **UI 30일 창과 같음**. 생성된 파일은 **생성 30일 뒤 자동 삭제**(같은 노트) → 영구 보관은 이 저장소 `data/`가 계속 맡는다 | [문서] |
| 비용 | **2026-03-30 데이터부터 COST가 long·정수(소수 첫째 자리 반올림)·VAT 포함**(2026-02-11 공지). 같은 공지: "stat-report의 지표와 광고주 센터의 합산 지표를 비교하는 경우 정확히 일치하지 않을 수 있습니다" → UI 총비용의 VAT 포함 여부·반올림 단위는 **A/B로만 판정** | [문서] / VAT 대응 [미실측] |
| 집계 시각 | UI 문구 `최근 집계 완료 시간: 2026.09.28. 00:20`(사용자 전언). API 쪽 숫자는 문서에 없음 — 2023-07-11 공지에 "EXPKEYWORD 평소 생성 시간 오전 2시 전후"(당시), `AGGREGATING` 상태가 정의돼 있음. `GET /stats` 응답 `cycleBaseTm`(yyyyMMddHHmm, "The latest datetime available")이 **자동 실행 시각 조건의 실측 근거** → 프로브가 기록 | [문서]·시각 [미실측] |
| 429·호출 한도 | 숫자 없음(09-27 기준선 1절과 같음). 프로브가 54작업을 5초 폴링으로 순차 실행하며 429 여부를 calls.jsonl에 남긴다 | [미실측] |
| 파일 형식 | 샘플이 `.tsv`로 저장 — **헤더 유무·인코딩·CRLF 미확인** → 프로브가 첫 3줄·BOM·CRLF·바이트 수 기록 | [미실측] |

**reportTp ↔ UI 보고서 대응과 컬럼 1:1 표**(`#/tags/StatReport` 원문 컬럼 번호; UI 열은 1절 실물):

| UI 보고서 | reportTp | API 컬럼(번호:이름) → UI 열 | 변환 |
|---|---|---|---|
| 키워드(필라테스) | **AD_DETAIL** | 1 Date→일별 · 3 Campaign ID→캠페인 · 4 AD Group ID→광고그룹 · 5 AD keyword ID→키워드 · 10 Media code→매체이름·검색/콘텐츠 매체 · 11 PC Mobile Type→PC/모바일 매체 · 12 Impression→노출수 · 13 Click→클릭수 · 14 Cost→총비용 · 15 Sum of AD rank→평균노출순위(=합/노출) | 8 Hours·9 Region code·6 AD ID·7 Channel ID로 갈라진 행을 **(캠페인·그룹·키워드·매체·PC/모바일·일자)로 합산**. 클릭률=클릭/노출×100, CPC=비용/클릭, 순위=순위합/노출 |
| 검색어 | **EXPKEYWORD** | 1 Date→일별 · 5 Search Keyword→검색어 · 8 Search Keyword Type→검색 유형(**0 일치 / 1 확장 / 2 일치(유사검색어)**, 2025-07-01부터; 그 전 5도 일치) · 9~11→노출·클릭·총비용 | 6 Media code·7 PC/모바일·3·4 캠페인·그룹으로 갈라진 행을 (검색어·유형·일자)로 합산. 전환 8열 = 0 |
| 상세지역 | AD_DETAIL | 9 Region code→상세지역(코드→이름 매핑 필요) · 1 Date · 12~15 | (지역·일자) 합산, 순위=합/노출 |
| 시간대별 | AD_DETAIL | 8 Hours→시간대별(`00시~01시` 라벨로 변환) · 12~15 | (시간) 합산 — **기간 전체 24행**(일자 없음, UI와 같음) |

- `AD`(reportTp)는 AD_DETAIL에서 시간·지역만 뺀 것 — 키워드 보고서만이면 AD로도 되지만 세 UI 보고서를 한 원본에서 만들려면 **AD_DETAIL 하나로 충분**(호출 수 절감) [문서·추론].
- **EXPKEYWORD의 범위 리스크(핵심)**: 이름이 "Powerlink search term report"(2023-05-29 개명)인데, UI 검색어 보고서의 09-25 노출 194는 **플레이스 137을 포함**(키워드 보고서 총합과 같음) [실측]. API 검색어 보고서가 플레이스 광고의 검색어를 담는지 **미실측** — 안 담기면 설계안 A로 검색어 보고서를 못 만들고(validate "검색어 CSV 클릭 합계 = KPI 클릭" FAIL), `GET /stats?id&statType=NPLA_SCH_KEYWORD`(StatTypeResponse `schKeyword`·impCnt·clkCnt·salesAmt — 문서 예시값 그대로, 기간 파라미터 없음) 같은 별도 경로를 조사해야 한다 [문서·추론]. **A/B 1순위 판정 항목.**
- `GET /stats`(요약): `ids`(캠페인·그룹·키워드 ID)·`fields`·`timeRange{since,until}`·`timeIncrement 1|allDays`·`breakdown pcMblTp|dayw|hh24|regnNo`(하나만). `regnNo`는 문서 예시가 `Gangwon-do, Gyeonggi-do`(시/도) → **상세지역(시·군·구)을 대체하지 못한다** [문서]. 용도는 `cycleBaseTm` 확인과 교차 검산(그룹별 하루 합계) 정도.

**ID·코드 → 이름 매핑**(생성 CSV의 문자열이 compute.py의 그룹 기준이므로 전부 정확해야 함 — compute.py 85~86 `검색/콘텐츠 매체==검색`, 133 `매체이름` top5, 134·211 `캠페인` 접두 `플레이스`·`매체이름` 접두 `네이버`, reportlib 제외 그룹 `excluded_groups` 이름 일치):

| 대상 | 방법 | 표기 |
|---|---|---|
| 캠페인·광고그룹·키워드 이름 | ① master-reports `item=Campaign/Adgroup/Keyword`(POST → BUILT → TSV, **컬럼 사양은 gist 미열람**) ② 대안 읽기 `GET /ncc/campaigns`·`GET /ncc/adgroups?nccCampaignId=`·`GET /ncc/keywords?nccAdgroupId=`(JSON `name`·`keyword`, swagger 확인) — ②는 이번 회차 허용 목록 밖(결정 2) | ① [문서 일부] ② [문서] |
| 삭제/OFF 그룹 표기 | UI는 `노원필라테스(삭제)`(config `excluded_groups` 값 그대로) — API 이름에 `(삭제)`가 붙는지, 삭제 그룹이 master·목록에 나오는지 **미실측**. 생성기가 UI 규칙을 재현 못 하면 제외 그룹 판정이 깨지므로 A/B 필수 항목(월 전체 이름 집합 대조) | [미실측] |
| 키워드 `-` 행(316/450행, 자동매칭·플레이스) | AD_DETAIL의 AD keyword ID가 빈값/특수값일 것 → `-`로 변환 | [추론] |
| 매체코드 → 매체이름·PC/모바일·검색/콘텐츠 | master `item=Media`("Media info") — UI 매체이름 21종(`네이버 통합검색 - 모바일`·`네이버 플레이스 - PC`·`다음-모바일`·`기타 매체`…)과 대응·표기가 같은지 미실측. `PC Mobile Type` 값 형식도 미실측 | [문서 일부]·[미실측] |
| 지역코드 → 상세지역명 | 후보 `GET /ncc/criterion-dictionary/RL`(지역 타게팅 사전: `dictionaryCode`·`name`) — AD_DETAIL Region code와 같은 코드계인지 미확인. UI 특수값 `-`·`국내 - 상세 위치 확인불가`의 코드 표기도 미확인 | [추론] |
| Hours → `HH시~HH시` | Hours 값 형식(`0`~`23`? `00`?) 미실측 → 라벨 변환표 config | [미실측] |
| 검색 유형 | 0→일치, 1→확장, 2→일치(유사검색어), 5→일치(2025-07-01 이전) — UI 값 집합 `확장 945·일치 526·일치(유사검색어) 6`과 이름이 같음 | [문서]·[실측] |

### 2-b. A/B 실측 1일치(2026-09-25) — A측 [실측], B측 [미실측: 프로브 대기]

| 종류 | A(UI CSV `data/2026-09` 09-25 행) | B(API) | 판정 |
|---|---|---|---|
| 키워드 | 8행 · 노출 194 · 클릭 8 · 총비용 **12,014** (파워링크 6행 71회·0클릭 / 플레이스 2행 137회·8클릭 12,014원; 매체 4종) | 대기 — `AD_DETAIL-20260925.tsv` | — |
| 검색어 | 51행(확장 34·일치 17) · 194 · 8 · **12,015** | 대기 — `EXPKEYWORD-20260925.tsv` | 플레이스 포함 여부가 1순위 |
| 상세지역 | 25행 · 194 · 8 · **12,015**(클릭 행: 의정부 2·확인불가 1·강남 1·노원 2·도봉 2) | 대기 — AD_DETAIL Region code 합산 + RL 사전 | — |
| 시간대별 | **하루치 UI 파일 없음**(보관본은 9/1~9/26 합계) → 사용자가 UI에서 9/25~9/25로 받은 시간대별 CSV 1개 필요(결정 5) | 대기 — AD_DETAIL Hours 합산 | — |

- 09-25 A측 행은 회차 폴더 `ui_<종류>_20260925.csv`로 떼어 두었고, `compare_ab.py`가 B 파일이 오면 합계·행 집합(검색어×유형·지역명·시간·키워드 ID 조합)·공통 행 값 차이(노출·클릭 불일치, 비용 ±1 초과)·유형 코드 분포·매핑 커버리지를 표로 낸다(지금은 B 전부 `[미실측]`으로 출력됨 [실측]).
- 차이가 나면 원인 후보: 비용 VAT/반올림(2026-03-30 변경) · EXPKEYWORD 매체 범위(2023-11-13 공지 "다차원 보고서와 대용량 보고서의 매체 기준을 통합"·2025-07-01 검색 지면 기준) · 플레이스 캠페인 포함 여부 · 순위 반올림(행 단위 1자리 vs 합/노출) · 지역 `-`/확인불가 코드.

### 2-c. UI 실물(차선용) — [미수령]
스크린샷이 오지 않았다. 요청: ① 목록 화면(4개 이름·기본 통계기간 `최근 7일 (오늘 제외)`·"조회일 기준 전일까지의 지표"·"최근 집계 완료 시간" 문구 — 사용자 전언은 있으나 화면 미수령) ② 보고서 하나를 연 화면의 **기간 선택 UI**(사용자 지정 기간 입력 방식)·`조회`·`다운로드` 버튼·완료 확인 방법 ③ 다운로드된 파일명 형식(현재 저장 이름 `필라테스_보고서_…`만 기록). 설계안 C의 셀렉터·완료 판정은 이 실물 없이는 못 적는다.

### 2-d. 그 밖의 내보내기 — [미실측]
- 안내문의 "정기적으로 조회"가 예약 생성·이메일 발송을 뜻하는지: 화면 미수령으로 판정 못 함. web_fetch·검색은 근거로 쓰지 않았다.
- API 공지들이 말하는 "대용량 (다운로드) 보고서" = **STAT-REPORT API 자체**(2019-04-30·2023-07-09 공지의 명칭) [문서] — UI에 같은 이름의 기능이 있다면 같은 데이터일 가능성이 높다 [추론]. 있어도 "안으로 올린다"는 설계안 A(API)와 결과가 같다.

## 3. 설계안(≤3, 채택은 사용자)

| | **A) API → UI와 같은 형식의 CSV 4개**(PC 스크립트) → store 이후 무변경 | B) API TSV 원본 보관 + archive.py 새 입력 경로 | C) PC 브라우저 자동화(Playwright, 로그인 세션 재사용) |
|---|---|---|---|
| 흐름 | 승인(첫 실사용·월 백필은 사용자 승인, 매일 증분은 승인 없이) → **읽기**(`GET /stats` cycleBaseTm으로 어제 집계 완료 확인 · 캐시 `data/api/YYYY-MM/`에 없는 날짜 목록) → **쓰기(파일 생성만)**: 날짜×종류마다 POST /stat-reports → 폴링 → 다운로드 → DELETE → 캐시 저장; 매핑(master 또는 ncc 읽기)으로 이름 채워 4개 CSV 생성 → **확인**: 4개 자체 검사(노출합 3종 일치·일별 범위·계정번호·컬럼) PASS → `archive.py store` → `combine` PASS → **기록**(생성 로그 `work/report_fetch_<날짜>.json`: 작업 ID·상태·바이트·집계 시각·매핑 미해결 0건) | A와 같되 CSV 변환 없이 TSV를 `data/api/`에 두고 combine이 TSV도 읽음 | 승인 → 읽기(목록 화면 4개 이름 확인) → 4개마다 기간 입력·조회·다운로드 → 확인(파일 4개 존재·첫 줄 기간 = 1일~어제) → `store` → `combine` → 기록 |
| config | `report_fetch`: `api_base` · `customer_id`(4480035) · `account_no`(2580077, 헤더용) · **`allowed_endpoints`**(GET /stats·/stat-reports·/master-reports·/report-download, POST /stat-reports·/master-reports, DELETE 둘 — 이 밖은 코드가 차단) · `report_types`(AD_DETAIL·EXPKEYWORD) · `csv_names`(필라테스·검색어·상세지역·시간대별) · `columns`(4종 헤더 문자열 원문) · `kw_type_map`(0 일치·1 확장·2 유사·5 일치) · `hour_labels` · `mapping`(master items / RL 사전 / 삭제 그룹 접미 규칙) · `cache_dir` · `refetch_days`(재집계 대비 0~3) · `poll_sec 5`·`poll_max_sec 600` · `run_after_kst` · `key_file` 경로는 **config에도 두지 않음**(인자만) | A + `raw_format`(TSV 컬럼 표) | `report_names`·`list_url`·셀렉터·`download_dir`·프로필 경로 |
| dry-run | 호출 0 — 캐시 대비 **받을 날짜×종류 목록·예상 호출 수·소요**·생성할 파일명·매핑 사전 유무만 출력(프로브 `--dry-run`과 같은 방식) | 같음 | 브라우저 안 열고 할 일 목록만 |
| 부분 실패 | 날짜×종류 단위로 성공/실패(status NONE·ERROR·AGGREGATING·429·다운로드 실패·매핑 미해결)를 표로 보고. **하나라도 빠지면 4개 CSV를 만들지 않고 store 금지**(SKILL.md 110~112 "부분 갱신 경로 없음"과 일치). 재시도는 사용자 결정. 이미 캐시된 날짜는 재요청 안 함 | 같음 | 4개 중 일부만 받아지면 store 금지 |
| 리스크 | ① EXPKEYWORD가 플레이스 검색어를 안 담을 수 있음(2-a) ② 비용 VAT·반올림 차이 ③ 이름 매핑(삭제 그룹 `(삭제)`·매체 표기·지역 특수값) ④ 재집계된 과거 일자를 캐시가 못 따라감(`refetch_days`) ⑤ 집계 전 실행(AGGREGATING) ⑥ 키 파일 권한 = 계정 전체(09-27 기준선 1절) ⑦ 54작업 429 | A의 ①~⑦ + archive.py·validate.py가 두 형식을 알아야 해 "되돌리면 안 되는 것" archive 5종 검사(checklist 187행)를 건드림 | 화면 구조 무예고 변경·로그인 만료/2차 인증(비밀번호는 Claude가 못 침)·다운로드 완료 판정·기간 입력 실수 → 하지만 **바이트 동일 CSV**라 변환 리스크 0 |
| 검증 | 첫 실사용 전: 프로브 결과로 A/B 4종 판정(결정 4) → 구현 검증 회차: 같은 날짜 재생성 → `store`·`combine` PASS · 생성 4개 vs UI 4개 **합산값 동일**(compute.json 차이 0) · dry-run 무변경(캐시·data md5) · 허용 목록 밖 호출 차단(단위 시험) · 부분 실패 시 store 안 됨 · 키 값 미출력 grep | 같음 + combine TSV 경로 시험 | 셀렉터 시험·다운로드 파일 첫 줄 검사 |
| 호출·소요 | 매일: GET /stats 1 + (POST 1·GET 폴링 ~2·다운로드 1·DELETE 1)×2 ≈ **11회, 1분 안팎** [추론]. 첫 백필(27일): ≈ 27×2×5 = **270회 + master 5×4 = 20회, 5초 폴링 순차 약 10~15분** [추론] | 같음 | 페이지 4개 × (열기·기간·조회·다운로드) 왕복 수십 회, 렌더링 대기 포함 3~5분 [추론] |
| 분담 | **PC**: 수집·생성·자체 검사(표준 라이브러리만 — PC는 pandas 없음, exclusions.py 선례) / **세션**: store·combine·push·이후 단계(생성 CSV 4개를 사용자가 채팅에 올리거나 PC에서 커밋). 스케줄은 PC 작업 스케줄러(사용자 결정) | 같음 | 전부 PC(브라우저), 세션은 이후 단계 |

**추천 순서(근거 한 줄)**: A — 공식 API·문서로 관리되는 스키마·store 이후 무변경(SKILL.md·archive.py 불변, 점검표 archive 행 유지). B는 "되돌리면 안 되는 것" 표를 건드려 미채택 권고. C는 A/B 실측에서 ①~③이 해결 안 될 때의 차선(실물 스크린샷 필수).

## 4. 절대 하면 안 되는 항목 후보와 근거

| 후보(config `report_fetch.forbidden`/코드 차단) | 근거 | 기존 표와의 충돌 |
|---|---|---|
| 1. 허용 끝점 밖 호출 금지 — `allowed_endpoints`에 GET /stats·/stat-reports(+/{id})·/master-reports(+/{id})·/report-download, POST /stat-reports·/master-reports, DELETE 그 둘만. **PUT 전면 금지**, `/ncc/*` 쓰기 금지(캠페인·그룹·키워드·제외 검색어·예산·소재) | 키 하나가 계정 전체 쓰기 권한(09-27 기준선 1절). 프로브가 이미 이 방식(표 밖이면 보내기 전 exit 3) | 없음 — [되돌리면 안 되는 것] 197·201행(exclusions dry-run 0·쓰기 전 읽기)과 같은 방향 |
| 2. 두 달에 걸친 기간의 파일 생성 금지 — 생성기는 달 단위로만 헤더·행을 만든다(1일~어제, 달이 바뀌면 지난달 파일은 안 건드림) | archive.py 83~84 거부 규칙·SKILL.md 64 "지난달 확정본" | 없음 — store 거부 2종 유지 |
| 3. 보관본 기간 축소 덮어쓰기 금지 — 생성기는 `--force`를 절대 붙이지 않고, 캐시 날짜 수 < 보관본 날짜 수면 FAIL | archive.py 91~95 | 없음 |
| 4. 키 값·키 파일 위치 출력·기록 금지 — 로그엔 경로만, 저장소·config·채팅·연결 폴더 밖 | exclusion-ui.md 2절 키 규칙·checklist 절대 규칙 | 없음 |
| 5. 당일(`statDt`=오늘)·`cycleBaseTm` 이후 날짜 요청 금지 | 부분 집계 데이터가 "확정" 파일이 됨(UI도 전일까지만) | 없음 |
| 6. 생성한 보고서 작업 잔존 금지 — 다운로드 뒤 DELETE, 끝에 목록 GET으로 0 확인(30일 자동 삭제가 있어도) | 문서 30일 삭제·계정 정돈 | 없음 |
| 7. 4개 중 일부만 성공했을 때 store 금지·부분 갱신 금지 | SKILL.md 110~112·checklist 188행 | 없음 — 같은 규칙 |
| 8. 이름 매핑 미해결 행을 `-`·빈칸으로 채우지 않는다 → FAIL | compute 05·10·제외 그룹 판정이 이름 문자열 기준 | 없음 |
| 9. 생성 CSV를 store 없이 계산에 쓰지 않는다 | SKILL.md 53~54 | 없음 |
| 10. 결정 2 전까지 `GET /ncc/campaigns·adgroups·keywords` 읽기도 금지(허용 목록에 없음) | 이번 회차 지시 | exclusions.py `GET /ncc/adgroups/{id}`는 5-0단계 전용 — 충돌 아님 |

[의도된 동작] 후보(구현 회차에 checklist 21~로): 생성 CSV의 행 순서가 UI와 다를 수 있음(합산 동일) · 총비용 ±1원은 반올림(UI 안에서도 1원 차이 실측) · 당일 데이터 미포함 · API `CUSTOMER_ID`≠헤더 계정번호(20번 그대로).

## 5. 리스크(각 한 줄)
- EXPKEYWORD 플레이스 미포함이면 A는 검색어 보고서에서 막힌다 → 프로브 첫 판정, 대안 `statType=NPLA_SCH_KEYWORD` 조사 또는 검색어만 C.
- 비용이 VAT·반올림으로 UI와 어긋나면 리포트 광고비가 과거 배포본과 불연속 → 결정 4의 허용 오차, 안 맞으면 지난달 확정본은 UI 원본 유지.
- 매핑 사전(master·RL)이 UI 표기와 다르면 compute 05·08·10이 조용히 틀린다 → 생성 검사에 "이름 집합 = 직전 달 UI 이름 집합 ⊆" 대조 추가.
- 재집계(공지 사례 다수)를 캐시가 못 따라감 → `refetch_days` 또는 월 1회 전체 재수집.
- 키 유출 시 계정 전체 쓰기 → 재발급 절차·키 파일 위치 규칙 유지.

## 6. B측 실측 결과 — 프로브 결과 수령 뒤 갱신(같은 회차, 사용자 PC 2026-09-28 02:24~02:25 KST 실행) [실측: 결과 파일 18개]

**6-1. 실행**: `--dry-run`(호출 0) 뒤 본 실행 `--modes list,stats,statreport,master,dict` — 실호출 **55건, 50초**(02:24:56~02:25:46), 429 0. 계정 설정 쓰기 0 — POST는 보고서 작업 생성 7건(stat 2·master 5, 200/201), DELETE 7건 전부 204, 삭제 뒤 GET 404 2건(stat). `calls.jsonl`·`probe_log.txt`에 키·authtoken 문자열 0건(grep). 수령: TSV 7(AD_DETAIL·EXPKEYWORD·master Campaign/Adgroup/Keyword/BusinessChannel·Media 필터본)·JSON 8·로그 2·UI 하루치 시간대별 CSV(9/25~9/25) 1·스크린샷 3장. 회차 폴더 `probe_out/`(저장소 미포함, 다운로드 URL의 authtoken·loginId는 이 기록에 옮기지 않는다).

**6-2. API 실물**

| 항목 | 실측 |
|---|---|
| stat-reports | POST 200 `{reportJobId, statDt "2026-09-24T15:00:00Z"(=09-25 00:00 KST), status REGIST}` → 폴링 RUNNING → **BUILT +5s(AD_DETAIL)·+15s(EXPKEYWORD)** → `downloadUrl …/report-download?authtoken=…&fileVersion=v2`를 서명 uri `/report-download`로 GET 200 `application/octet-stream` → DELETE 204 → GET 404. 시작 전 목록 `null`(작업 0) |
| 파일 형식 | **헤더 없음·BOM 없음·LF·탭 구분**. AD_DETAIL 83행 × 16열, EXPKEYWORD 37행 × 12열 — 문서 컬럼 순서 그대로(일자 `20260925`·고객 4480035·`cmp-…`·`grp-…`·키워드 `nkw-…` 또는 `-`·`nad-…`·`bsn-…`·시간 `21`·지역 `09`·매체 `8753`·`M`/`P`·정수 3개·순위합·view 0). 비용 정수(예 3193) |
| `GET /stats` | `ids`를 JSON 배열 문자열로 주면 **400 11001 "유효하지 않은 ID 형식입니다"**(쉼표 구분이어야 할 것 [추론]); `id` 단건은 200 — breakdown `hh24` name **`08시~09시`(UI 라벨과 동일)**, `regnNo` name 시/도(`서울특별시`·`국내 - 상세 위치 확인불가`), `pcMblTp` `모바일`, 월 일별(`timeIncrement=1`) 25일 OK. **`cycleBaseTm` 202609280100·compTm 202609280142** — 02:25 KST 실행 시점에 09-27 하루가 집계돼 있음(UI 띠 00:20, API 기준 01:00) |
| master-reports | POST 201 → BUILT +5s(Media는 즉시) → TSV 헤더 없음. Campaign 2행(3열 = 이름, 4열 = 유형 1/6) · Adgroup 6행(4열 = 이름, 6열 1/0 = 잠금 추정: `…072213027`·`…072697408`만 1) · Keyword 14행(4열 = 키워드) · BusinessChannel 2행 · **Media 873,717행 114.9MB**(`media`·코드·이름·URL·…) — 사용자가 코드 4개로 필터한 사본. 기존 목록에 09-05 생성 `Qi` 작업 1개(이번 회차 생성 7개는 전부 삭제) |
| RL 사전 | `GET /ncc/criterion-dictionary/RL` 5,354개 — 2자리 `RL01 강원특별자치도`·`RL02 경기도`·`RL09 서울특별시`·`RL99 국내 - 상세위치 확인 불가`, 하위 `RL09350 서울특별시 노원구`, 동 단위(`RL09350105 … 상계동`)까지 |

**6-3. A/B 대조표(2026-09-25, `compare_ab.py` 출력 `ab_result_2026-09-25.md`)**

| 종류 | A(UI CSV) | B(API) | 판정 |
|---|---|---|---|
| 키워드 | 8행 · 194/8/**12,014** | AD_DETAIL 83행 → (캠페인·그룹·키워드·매체·PC/M) 합산 **8행 · 194/8/12,015** | **일치** — 이름 매핑(master Campaign·Adgroup·Keyword + Media 4코드) 100%로 행 집합 8=8, 노출·클릭 8/8, 비용은 행 단위 ±1(플레이스 모바일 12,014 vs 12,015), **평균노출순위 = round(순위합/노출, 1) 8/8 일치** |
| 시간대별 | 하루치 UI 18행(노출 0 시간은 행 없음) · 194/8/12,015 | AD_DETAIL Hours 합산 18행 | **일치 18/18** — 라벨 `HH시~HH+1시`(23 → `23시~00시`), 노출·클릭·비용 ±0·순위 1자리 전부 |
| 상세지역 | 25행(시·군·구, `서울특별시 노원구` 91/2 …) | Region code **2자리 8종 = RL 시/도**(`09` 서울 147/5, `02` 경기 26/2, `99` 확인불가 15/1 …) | **재현 불가** — 시/도 합산은 9/9 일치하지만 시·군·구는 API에 없다(swagger `regnNo`도 시/도). 표기도 `국내 - 상세위치 확인 불가`(RL) ≠ `국내 - 상세 위치 확인불가`(UI) |
| 검색어 | 51행 · 194/8/12,015(확장 34·일치 17) | EXPKEYWORD 37행 · **57/0/0 — 파워링크 캠페인만** | **부분** — 파워링크 36행(검색어×유형, 0→일치·1→확장)은 노출·클릭·비용 전부 일치·B만 0. **플레이스 검색어 137회/8클릭/12,015원(UI 17행 전부 `일치`)이 API에 없다** — 문서 이름 그대로 "Powerlink search term report" |

**6-4. 이름·표기 실측**
- config `excluded_group_keywords` 10개 = master Keyword의 그룹 `grp-a001-01-000000072213027` 키워드 10개(정확히 같은 집합) → OFF 그룹은 이 ID이고 **API 이름은 `새로필라테스 파워링크`(6열 1)**, UI 8월 CSV 표기는 `노원필라테스(삭제)`(8/26·8/31 6회, 9월 0회). 불일치 원인(개명·삭제 표시 규칙)은 [미실측] — API 이름으로 CSV를 만들면 이름 기반 제외(reportlib `excluded_groups`)가 어긋난다 → ID 매핑이 필요.
- 캠페인 `새로필라테스 파워링크`·`플레이스#1`, 활성 그룹 4개·플레이스 그룹 `새로필라테스`, 키워드 이름, 매체 4코드(8753 `네이버 통합검색 - 모바일`·401113 `네이버 플레이스 - 모바일`·401114 `네이버 플레이스 - PC`·612594 `다음-모바일`)는 UI 표기와 **문자열 동일**. `노원키즈필라테스` 그룹 `…072697408`도 잠금 1(9/18~ 노출 0의 원인 후보 [추론]).

**6-5. UI 실물(스크린샷 3장, 사용자 화면)** [실측]
- 목록(`…/sa/reports`): 제목 `다차원 보고서` · 안내 "사전 정의된 보고서를 통해 빠르고 쉽게 조회를 할 수 있고 자주 사용하는 보고서는 직접 나만의 보고서 형식을 만들어 정기적으로 조회하실 수 있습니다", "조회일 기준 전일까지의 지표" · 주황 띠 `보고서는 실시간이 아닙니다. 최근 집계 완료 시간 : 2026.09.28. 00:20` · 버튼 `+ 새 보고서 ∨` · 표 `보고서 이름 | 통계기간 | 생성일 | 최근 열람일 | 생성자` 4행(시간대별·상세지역·검색어·필라테스 보고서, 통계기간 전부 `최근 7일 (오늘 제외)`, 생성일 08.31/08.31/08.31/08.30) · `행표시: 10`. **예약·이메일·대용량 다운로드 버튼 없음.**
- 보고서 화면(시간대별): `← 돌아가기` · 버튼 `보고서 형식 저장 ∨`(파란 드롭다운)·`다운로드` · 오른쪽 기간 `2026.09.21. → 2026.09.27.` + 달력 아이콘 + `<` `>` + `∧ 접기` · 왼쪽 `보고서 항목 목록`(캠페인·캠페인 유형·광고그룹·광고그룹 유형·키워드·소재(비활성)·소재 유형(비활성)·비즈채널…) · 가운데 `보고서 설정하기`(항목 `시간대별` + 지표 칩 9개) · 아래 `조회하기`(회색 — 조회 전) · 하단 띠 "전환 성과를 확인할 수 없습니다. '전환 추적 서비스(무료)'를 신청하면…"(전환 열이 전부 0인 이유).
- 기간 팝업: 프리셋 `어제·이번주·지난주·전 영업주·최근 7일 (오늘 제외)·이번달·지난달·이번 분기·지난 분기·최근 30일 (오늘 제외)·최근 90일 (오늘 제외)·최근 365일 (오늘 제외)` · 시작/끝 **텍스트 입력칸**(`2026.09.21.` `2026.09.27.`) · 달력(오늘 28일 회색 = 선택 불가, 어제 27일까지) · `취소`·`확인`. → 자동화 경로: 입력칸에 `YYYY.MM.01.`·어제를 타이핑하거나 프리셋 `이번달`(어제까지로 추정 [추론]) → `확인` → `조회하기` → `다운로드`.
- 2-d 판정: "정기적으로 조회"는 저장한 보고서 형식을 반복 조회한다는 뜻이고 예약·발송 문구는 없다 [실측: 화면 문구]. `보고서 형식 저장`에 **기간이 함께 저장되는지**(되면 `이번달`을 한 번 저장해 두는 것만으로 수동 단계가 "열기 → 다운로드"로 준다)는 [미실측] → 요청 2.

**6-6. 설계안 갱신(실측 반영)**

| | 갱신 판정 |
|---|---|
| A) API → UI 형식 CSV 4개 | **단독 불가** [실측] — 키워드·시간대별 2개만 완전 재현, 검색어는 파워링크분만, 상세지역은 시/도까지만. 역할을 **교차 검증**으로 바꾼다: 매일 AD_DETAIL 1작업(호출 ≈ 6)으로 어제 노출·클릭·비용·순위·시간·시/도를 받아, 다운로드된 UI CSV 4개와 대조해 잘못된 기간·빠진 파일·재집계를 사람 없이 잡는다 |
| B) TSV 원본 + 새 입력 경로 | 폐기(A 전제) |
| **C) PC Playwright(4개 전부, 바이트 동일 UI CSV)** | **추천** — 로그인된 전용 크롬 프로필(persistent context, 로그인 입력 자동화 없음) → 목록 URL → 보고서 링크(이름 = config `report_names` 4개) → 기간 입력칸 타이핑(`YYYY.MM.01.`·어제) 또는 프리셋 `이번달` → `확인` → `조회하기` → `다운로드`(download 이벤트 완료 대기) → 파일 첫 줄(기간 = 1일~어제·계정 2580077)·2행 컬럼 검사 → 4개 전부 통과 시 `archive.py store` → `combine`. 셀렉터·완료 판정은 구현 회차에 PC 실물 DOM으로 확정(Playwright codegen·텍스트 셀렉터, 좌표 클릭 금지). 리스크: 세션 만료·2단계 인증(재로그인은 사용자), 화면 변경, 다운로드 파일명 규칙. 부분 실패: 4개 중 하나라도 실패면 store 안 함. dry-run: 브라우저 안 열고 할 일 목록(4개 이름·기간·저장 경로)만 |
| D) (보조, 코드 0) 보고서 형식에 기간 저장 | `보고서 형식 저장`이 기간을 함께 저장하면 `이번달`을 4개에 한 번 저장 — C 이전에도 수동 단계 축소, C의 클릭 수도 감소 [미실측] |

추천 조합: **C + A(교차 검증) (+ D 가능하면)**. 4단계 흐름(승인 → 읽기 → 쓰기(파일 생성만) → 확인 → 기록)은 C가 맡고, A는 "확인" 단계의 독립 근거가 된다.

**6-7. 금지 후보 추가(C용)**: 좌표 클릭 금지 · `+ 새 보고서`·`보고서 형식 저장`·항목 끌어놓기·삭제 등 **설정 변경 요소 클릭 금지**(허용 = 보고서 열기·기간·확인·조회하기·다운로드·돌아가기) · 로그인 폼 자동 입력·비밀번호 저장 금지 · 첫 줄·컬럼 검사 전 store 금지 · 두 달 걸친 기간 입력 금지 · 4절 1~10은 A(검증)에 그대로.

## 사용자 확인 요청(이번 회차)
1. push 토큰(파일 첨부) — 1차 커밋 push용. 2. 스크린샷 3장(2-c ①②③). 3. 프로브 실행 결과 폴더 `probe_out\`(키 없음) — 명령은 references 아닌 이 절 아래 "PC 실행" 참고. 4. 9/25~9/25 하루치 시간대별 UI CSV(결정 5).

**PC 실행(경로 C, 저장소 밖 아무 폴더)**:
```
python naver_report_probe.py --key-file C:\Users\<사용자>\naver-api.keys.json --day 2026-09-25 --out probe_out --dry-run      # 호출 0, 계획 44건 출력
python naver_report_probe.py --key-file C:\Users\<사용자>\naver-api.keys.json --day 2026-09-25 --out probe_out                # list·stats(11 GET)·statreport(AD_DETAIL·EXPKEYWORD 각 POST→폴링→다운로드→DELETE→삭제 확인)
python naver_report_probe.py --key-file ... --day 2026-09-25 --out probe_out --modes master,dict                              # 결정 2 뒤에만: master 5작업(Campaign·Adgroup·Keyword·Media·BusinessChannel)+RL 사전
```
프로브 실측(이 세션): `py_compile` OK · `--dry-run` 44호출 계획·HTTP 0 · 키 문자열이 로그·calls.jsonl에 없음 · modes=stats에서 POST /stat-reports·PUT·DELETE /ncc/*·GET /ncc/campaigns 전부 차단 · 컨테이너 실호출은 403(0절).

## 마무리 기록(이번 회차)
- 커밋: 이 절을 last-audit.md 맨 위에 붙인 1차 커밋(author `LeeKwanBeom <322668067+LeeKwanBeom@users.noreply.github.com>`). 토큰은 세션 중 수령(파일로 저장, 옮겨 적지 않음) → `git pull --rebase` → push → 재clone 대조. 결과는 채팅 보고·사용자 폴더 사본에(이 절의 커밋 해시는 자기 참조라 적지 않는다).
- 네이버 계정: 쓰기 0·읽기 0(호출 불가). 저장소 SKILL.md·scripts·config·data md5 불변(변경 파일 = audit/last-audit.md만).

## 내가 고를 항목 (갱신 — 6절 실측 반영; 1차 목록 1~8은 아래로 대체)
1. 설계안: **C(브라우저 4개) + A(API 교차 검증)** / C만 / A 부분(키워드·시간대별만 API, 검색어·상세지역은 수동) / 보류.
2. D 확인(사용자 직접 — 설정 변경이라 회차에서 하지 않음): 보고서 하나에서 기간 `이번달` 선택 → `보고서 형식 저장` → 목록의 통계기간 열이 바뀌는지 스크린샷.
3. 프리셋 `이번달`의 실제 범위(1일~어제인지) — 선택 뒤 입력칸 값 스크린샷.
4. C의 로그인 세션: 전용 크롬 프로필(한 번 로그인, 이후 재사용) / 기존 프로필 재사용 — 2단계 인증·재로그인은 사용자.
5. A 교차 검증 허용 오차: 노출·클릭 완전 일치 · 총비용 ±1원/보고서 · 순위 1자리 · 시/도 합산 일치.
6. OFF 그룹(`…072213027`) 표기: A 검증 그룹명 대조용 ID 매핑 `{"grp-a001-01-000000072213027": "노원필라테스(삭제)"}`를 config에 둘지 / 제외 그룹 판정을 ID로도 받게 할지(reportlib 변경 — 별도 회차).
7. 첫 실사용 범위·시각: 전날 하루치만 / 이번 달 전체(UI 원본과 대체) · PC 스케줄러 **01:00 KST 이후**(cycleBaseTm 01:00 실측, UI 00:20) / 수동.
8. NPLA_SCH_KEYWORD(`GET /stats?id&statType`) 추가 프로브 여부 — 플레이스 검색어 API 경로 조사(A를 3/4로 올릴 뿐 상세지역은 여전히 불가 → 우선순위 낮음).
9. 매체 코드→이름은 Media 마스터(115MB)를 받지 않고 config 표(현재 21종 이름 + 코드 4개 실측)로 두고 미지 코드는 보고만 / 매번 마스터 수신.
10. config 값: `report_names`(시간대별 보고서·상세지역 보고서·검색어 보고서·필라테스 보고서) · `list_url`(`…/ad-accounts/2580077/sa/reports`) · `download_dir` · `account_no 2580077` · A용 `customer_id 4480035`·`allowed_endpoints`·`report_types ["AD_DETAIL"]`.

토큰은 이 회차가 끝나면 GitHub에서 폐기해 주세요(이번 세션에는 수령·사용된 토큰 없음).

**사용자 결정(2026-09-28 저녁, 리포트 갱신 세션에서) — 실행 위치 = 데스크톱 앱 Code 탭(Claude Code) 한곳.** "채팅에서 다 하든 Code 탭에서 다 하든 한군데서 해야 자동화가 의미가 있다" → 수집(보고서 4개) → store·combine → 리포트 갱신·배포 → 제외 검색어 후보·승인·등록·확인 → audit 기록·push까지 **전부 PC 저장소 폴더를 연 Code 탭 세션에서** 한다. 채팅(웹·데스크톱 Cowork)은 네이버 API 403이라 한곳이 될 수 없음(09-27·09-28 실측). 이에 따라 위 3절 분담 열의 "**세션**: store·combine·push·이후 단계"는 폐지, 항목 7(수동/스케줄러)은 "Code 탭 세션 실행"으로 대체. 순서: **feat-report-fetch 검증·병합 먼저(한 회차 한 기능)** → 다음 기능 추가 회차 = "Code 탭 전 단계 실행"(SKILL.md 경로 규칙·pandas/playwright 의존성·토큰 파일 규약·Code 탭 진입점) → 첫 실사용은 그 뒤. 근거 실측: 2026-09-28 Code 탭에서 `exclusions.py pull` exit 0·`push` 15/15(references/exclusion-ui.md 3절).

---

# 기능 추가 탐색 기준선(제외 검색어 등록 자동화, 2026-09-27)
점검일: 2026-09-27 (기능 추가 회차 — **탐색·설계만**, Fable). SKILL.md·scripts·config·data·checklist.md **변경 없음**. 제외 검색어 추가·삭제·저장 버튼 클릭 **없음**(읽기도 못 했다 — 아래 0). 리포트 갱신·배포 **없음**. 산출물은 이 절(1차 커밋, 이 파일만)과 사용자 폴더 사본 `saero-ad-report_제외검색어_탐색_2026-09-27.md`. 구현은 사용자가 아래 "내가 고를 항목"을 고른 뒤 별도 회차.
점검 대상(전부 저장소에서 받은 것): `saero-ad-report-skill` @5e8c055(main) — SKILL.md(438행) · audit/checklist.md(444행, v4.4 — 안전 규칙·[의도된 동작] 9·10 읽음) · audit/last-audit.md(1,352행 — "등록 제외 검색어 대조 목록" 절·09-27 제안 행 읽음) · config/report-config.json(49행) / 합본 = `data/` combine PASS(2026.08.26~09.26, 32일, 9,737/302/344,274원) / 공식 API 문서 = `naver/searchad-apidoc` master(README.md·NaverSA_API_Error_Code_MAP.md·python-sample) + gh-pages(`assets/json/ncc-heroes-ncc.json` swagger 65경로, `_posts/2024-09-13-release-note.md`·`2024-08-19-notice1.md`·`2026-09-16-release-note.md`·`2020-12-18-notice.md`) git clone / **광고시스템 화면·API 사용 관리 화면·API 호출: 직접 접속 전부 미실측(0절)** — UI는 사용자 스크린샷 23장(09-27 세션 중 회신)으로 3그룹 전부 실측.
효율: 벽시계 약 __분(10:42 clone → __ push) · 도구 호출 약 __회 · 즉석 코드 약 225행(`registry_check.py` 45 — 대조 목록 ↔ 합본 검색어 CSV / `ui_vs_registry.py` 55 · `ui_vs_registry2.py` 75 · `ui_vs_registry3.py` 50 — 스크린샷 전사 ↔ 대조 목록·교차, 전부 회차 폴더에만, 저장소 미포함) — 총 약 225행.
표기: [실측] 이 세션에서 직접 확인 / [문서] 공식 API 문서·저장소 원문에서 확인 / [기록] 이 파일의 과거 회차 기록에서 가져옴 / [추론] 확인 못 함 / [미실측] 차단으로 시도 실패.

## 0. 결정적 실측 — 광고시스템·검색광고 API 호스트가 이 환경의 네 경로 전부에서 차단됨 [실측]

| 경로 | 시도한 것 | 결과(원문) |
|---|---|---|
| Claude in Chrome(선호 브라우저, 사용자 실제 크롬) | `navigate` → 그룹 1 URL(`ads.naver.com/manage/ad-accounts/2580077/sa/adgroups/grp-a001-01-000000072697414`), 이어 `manage.searchad.naver.com/` | 둘 다 `This site is not allowed due to safety restrictions.` — 페이지 로드 자체가 안 됨(확장프로그램 단계 거부) |
| 내장 브라우저(Claude Browser, 데스크톱 앱 패널) | `preview_start` → 같은 그룹 1 URL | `… is not allowed due to safety restrictions and cannot be opened in the browser pane.` |
| 클라우드 컨테이너 `curl` | `api.searchad.naver.com/ncc/adgroups/…/restricted-keywords` · `ads.naver.com` · `manage.searchad.naver.com` · `searchad.naver.com` | 4개 전부 프록시 **CONNECT 403** — `__agentproxy/status` recentRelayFailures에 `gateway answered 403 to CONNECT (policy denial or upstream failure)` 4건 |
| 사용자 PC 셸(`device_bash`, PC 안의 VM) | `api.searchad.naver.com` · `ads.naver.com` (대조군 `github.com`) | 두 호스트 `Received HTTP code 403 from proxy after CONNECT` / github.com **200** — 이 VM도 같은 허용 목록을 탄다 |

- 뜻: **지금 스킬이 도는 Cowork 환경에서는 DOM 자동화(Claude in Chrome)도, 공식 API 직접 호출(컨테이너·PC VM)도 열려 있지 않다.** "후보 제시 → 승인 → 등록 → 읽기 확인 → 기록" 중 등록·읽기 두 단계를 스킬이 수행할 경로가 **현재 0개**다. 이번 회차 지시의 항목 2(UI 실물 3페이지)·3(등록 목록 3그룹 전량 읽기)·1 후반(API 사용 관리 화면)은 그래서 직접 실측하지 못했고, 2·3은 사용자가 세션 중 보낸 스크린샷 23장(탭 목록 1·대화상자 22 = 노원산전 6·노원역 11·상계동 3 + 초기 2)으로 3그룹 전부 채웠다.
- 차단 주체 판별은 못 했다 [추론]: 브라우저 두 개는 "safety restrictions"(사이트 안전 정책 문구), 셸 두 개는 프록시 "policy denial"(네트워크 허용 목록 문구)로 **문구가 다르다** — 별개 설정일 수 있어 한쪽이 풀려도 다른 쪽이 남을 수 있다. 조직 네트워크 허용 목록은 Team·Enterprise 관리자 설정(Admin settings → Capabilities)에서 다룬다고 안내돼 있으나, 이 계정에서 해제가 가능한지·브라우저 쪽 정책도 같은 곳에서 풀리는지는 **확인하지 못했다**(요청 4).
- 이 결과가 설계의 1번 입력이다. 4절은 경로가 **열리는 경우**(4-A API · 4-B DOM)와 **열리지 않는 경우**(4-C 사용자 실행 CLI · 4-D 현행 + 대조 자동화)를 나눠 적었다. 채택은 사용자.
- 읽기 채널 후보 하나 더 [추론, 미시도]: 데스크톱 앱 컴퓨터 사용(화면 캡처)은 사용자가 로그인된 크롬 화면을 **스크린샷으로 읽기만** 할 수 있다(이번 세션은 켜지 않음). 사용자가 페이지를 넘겨줘야 하고 좌표 클릭 금지 원칙상 조작은 못 한다 — 항목 2(화면 몇 장) 용도로는 가능, 항목 3(수백 행 페이지네이션) 용도로는 비현실적.

## 1. 공식 API — 광고그룹 제외 검색어 조회·등록·삭제 **있음** [문서]

출처: `naver/searchad-apidoc` gh-pages `assets/json/ncc-heroes-ncc.json`(swagger, `Heroes New Clickchoice API 2.0`), master `NaverSA_API_Error_Code_MAP.md`, `_posts/2024-09-13-release-note.md`. 기본 URL `https://api.searchad.naver.com`(python-sample `BASE_URL`). 문서상 경로 접두 `/api/ncc/…`는 샘플 코드에선 `/ncc/…`로 호출한다.

| 기능 | 메서드·경로 | 요청 | 응답 | 문서 원문(요지) |
|---|---|---|---|---|
| 조회 | `GET /ncc/adgroups/{adgroupId}/restricted-keywords?type=EXP_SEARCH` | `type` 쿼리(생략 시 기본 `KEYWORD_PLUS_RESTRICT` — **확장 검색 칸을 읽으려면 `type=EXP_SEARCH`를 반드시 붙여야 한다**) | `AdgroupRestrictKwd[]` | "Returns a list of impression-restricted keywords. This feature is only available for adgroups of website campaign types." |
| 등록 | `POST /ncc/adgroups/{adgroupId}/restricted-keywords` | body `AdgroupRestrictKwd[]` — 항목마다 `keyword`·`type`(·`description`) | 200 `AdgroupRestrictKwd[]`(항목마다 `nccAdgroupRestrictKwdId`·`regTm`·`resultStatus{code,message}`) | "Create impression-restricted keywords for the adgroup. This feature is only available for adgroups of website campaign types." |
| 삭제 | `DELETE /ncc/adgroups/{adgroupId}/restricted-keywords?ids=<id,id,…>` | `ids` 쿼리(필수) = `nccAdgroupRestrictKwdId` 목록 | 204 | "Remove impression-restricted keywords. …" |

- 오브젝트 `AdgroupRestrictKwd`: `keyword`(제외 검색어) · `type`(enum `KEYWORD_PLUS_RESTRICT` / `EXP_SEARCH`, 기본 `KEYWORD_PLUS_RESTRICT`) · `description` · `nccAdgroupId` · `nccAdgroupRestrictKwdId`(등록 뒤 부여, 삭제 시 필수) · `regTm`(등록 시각) · `delFlag` · `resultStatus{code,message}`("Registration failed when the error code/message" — 항목별 실패가 여기 담긴다).
- `type` 뜻(2024-09-13 릴리스 노트 원문): `EXP_SEARCH : 확장 검색` / `KEYWORD_PLUS_RESTRICT : 스마트블록 및 유사검색어`. 2024-10-02 파워링크 확장검색 도입 때 "노출제한키워드"가 "제외검색어"로 개명되며 `EXP_SEARCH`가 추가됐다. 예제 body: `{"nccAdgroupId":"grp-a001-00-…","keyword":"대출","type":"EXP_SEARCH"}`. → 우리가 쓰는 "확장 검색" 칸 = `EXP_SEARCH` [문서], "일치(유사검색어)" 칸 = `KEYWORD_PLUS_RESTRICT` [추론 — 이름 대응만, UI 미확인].
- 캠페인 유형 제한: 세 엔드포인트 모두 "only available for adgroups of **website** campaign types"(파워링크 `WEB_SITE`). 플레이스 그룹은 대상 아님 → 대조 목록 규칙 "플레이스 쪽 등록을 제안하지 말 것"과 방향이 같다. 오류 3728 `키워드 확장 노출 제외키워드를 지원하지 않는 캠페인 유형입니다.`
- 한도: 오류 3716 `광고그룹에 등록가능한 노출제한 키워드의 최대 개수를 초과하였습니다.` — **숫자는 문서 어디에도 없다**(swagger·공지·i18n grep 0건). UI 카운터 `(0/950)`(09-17 기록)의 950이 그룹당 최대인지 남은 용량인지 미확인 [추론]. 3721·3722 설명·키워드 최대 길이 초과, 3723 등록 불가 문자 — 길이·문자 규칙도 숫자 없음.
- 2026-09-16 릴리스 노트 [문서]: **ADVoost 플레이스 ON 그룹(`useAdvoost: true`)은 제외 검색어 등록이 400으로 거부**(3754 / 4422 `Restricted keywords cannot be registered for an AdVoost-on ad group.`). 이 계정 파워링크 3그룹의 `useAdvoost` 값은 미확인 → API 채택 시 첫 GET `/ncc/adgroups/{id}`로 확인할 항목.
- 인증 [문서·코드]: 헤더 `X-Timestamp`(ms) · `X-API-KEY`(라이선스) · `X-Customer`(2580077) · `X-Signature` = base64(HMAC-SHA256(secret, `"{timestamp}.{METHOD}.{uri}"`)) — uri는 쿼리 제외 경로(python-sample `signaturehelper.py`·java `RestClient.java`). 응답 헤더 `X-Transaction-ID`가 오류 추적용.
- 발급 [문서]: "광고주 센터 [도구 -> API 사용 관리] 메뉴를 통해 라이선스와 비밀키 발급 — 라이선스(`API-KEY`)는 요청에 첨부, 비밀키(`API_SECRET`)는 서명 생성용" / 절차 "3. 도구 > API 사용 관리 → 4. 네이버 검색광고 API 서비스 신청". **이 계정의 신청 여부·키 발급 여부는 화면 차단으로 미확인** → 요청 1.
- 호출 한도 [문서]: swagger·공지에 숫자 없음. 429 관련 공지는 키워드 도구 기준(2020-12-18: 429면 5~6배 긴 sleep, 짧은 시간 대량 429 유발 금지, 발생 시 5분 이상 중단). 우리 용도는 회차당 GET 3회(+ 등록 시 POST 3회, 재확인 GET 3회) 수준 [추론 — 한도 우려 낮음].
- 사용자 계정 API 사용 상태: **[미실측]** — 도구 > API 사용 관리 화면을 열 수 없었다.

**API ↔ DOM 트레이드오프(각 한 줄, 채택은 사용자)**

| 축 | API(`restricted-keywords`) | DOM(Claude in Chrome, 광고시스템 화면) |
|---|---|---|
| 안정성 | 스키마 변경이 공지·릴리스 노트로 관리됨(2024-08-19 명칭 변경·2024-09-13 type 추가·2026-09-16 ADVoost 이력) | 화면 구조는 무예고로 바뀜 — 배민·쿠팡 스킬 이력의 셀렉터 깨짐 유형이 그대로 재발 |
| 키·세션 보관 | 라이선스+비밀키 2개(+고객 ID)를 **스킬 밖**에 둬야 함(토큰처럼 매 회차 채팅 입력 또는 사용자 PC 파일) — 저장소 공개라 저장소엔 절대 금지 | 보관물 없음 — 사용자가 크롬에 로그인돼 있으면 됨(세션 만료 시 재로그인은 사용자 몫, Claude는 비밀번호 입력 불가) |
| 권한 범위 | 키 하나가 **계정 전체 쓰기**(캠페인·입찰가·소재 포함) — 유출 시 영향이 제외 검색어를 훨씬 넘음 → 폐기·재발급 절차 필요 | 로그인 세션도 계정 전체지만 대화에 남지 않고 만료로 소멸 |
| 호출 한도·속도 | 회차당 GET 3 + POST 3 + GET 3 ≈ 9회, 응답 즉시(JSON) | 그룹당 탭 열기·페이지네이션(10행/페이지, 그룹당 100~200행 → 10~20페이지) 왕복 수십 회 + 렌더링 대기 |
| 검증 근거 | 등록 응답에 `nccAdgroupRestrictKwdId`·`regTm`·항목별 `resultStatus` — **기록에 바로 옮길 원본** | 저장 뒤 목록을 다시 스크래핑해 이름 대조(등록 시각은 화면 표기 파싱) |
| 되돌리기 | `DELETE ?ids=` 1회(id는 등록 응답에 있음) | 목록에서 찾아 체크·삭제 클릭 |
| 이 환경 도달성(2026-09-27) | **0 — 프록시 403** | **0 — 브라우저 safety restrictions** |

## 2. UI 실물(3페이지) — 직접 접속은 [미실측], 사용자가 세션 중 보낸 스크린샷 23장(탭 목록 1 · 대화상자 22)으로 3그룹 실측 [실측: 사용자 화면 09-27]

**2-1. 광고그룹 상세 > "제외 검색어" 탭 (스크린샷 1 — 어느 그룹인지는 미표기, 요청 2-④)**
- 탭 줄: `키워드` · **`제외 검색어`**(선택 상태) · `소재` · `확장 소재` · `+ 타겟팅 탭 추가`.
- 탭 안 도구 줄: 파란 버튼 **`+ 제외 검색어 추가`** · 회색(비활성) `다른 그룹으로 복사`(행을 체크하면 활성될 것 [추론]) · 필터 입력창 `필터를 입력해 주세요`.
- 표 헤더: `[전체 선택 체크박스]` · `검색어 ⓘ` · `유형` · `설명 ⓘ` · `등록시각 ⓘ` — 검색어·유형·설명 열에 필터(깔때기)·정렬 아이콘, 등록시각 열에 정렬 아이콘. 행마다 체크박스.
- 행 값: 유형 = `확장 검색`(문자열 그대로), 등록시각 = `2026.09.26. 13:18` 형식(분 단위), 설명 열은 빈칸. 일부 검색어 옆에 회색 배지 **`적은검색량`**(노원9월행사·노원역추석·노원역에새건물·노원역추석영업·6세필라테스) — 등록과 무관한 검색량 표시 [추론].
- 보이는 10행 = 09-26 재등록 7개(13:18: 노원구어린이·노원역9번출구·노원9월행사·노원역추석·노원어린이체험·노원역6번출구·노원역테니스레슨) + 09-26 신규 6개 중 3개(13:20: 노원역에새건물·노원역추석영업·6세필라테스). **10행/페이지 재확인**(09-17 기록과 일치). 나머지 3개(노원역두·노원역월·노원역스튜디오)는 다음 페이지로 추정. 대조 목록 표 09-26 두 행의 이름이 UI에 있는 것이 이 그룹에서 확인됨 — **등록시각 13:18·13:20이라는 값은 표에 없던 정보**(기록엔 "09-26"까지만).
- 기본 정렬: 같은 날 등록분이 13:18 → 13:20 순으로 보이므로 등록시각 내림차순만은 아님 — 정렬 규칙 미확인 [추론]. 페이지네이션·전체 건수 표시는 잘려서 못 봄(요청 2-②).

**2-2. "제외 검색어 추가" 대화상자 > "기간의 검색어" 보기 (스크린샷 2 — 위쪽이 잘림)**
- 위: 잘린 선택 상자 2개(내용 미확인, 요청 2-③) / 기간 `2026.08.28. → 2026.09.26.` + 달력 아이콘 + `<` `>` 이동 + 라벨 `기간의 검색어`(30일 창으로 보임 [추론]) / 오른쪽 **`다운로드`** 버튼 / 필터 입력창.
- 표 헤더: **`+ 전체추가`**(첫 열 헤더 자리) · `검색어` · `검색 유형` · `노출수` · `클릭수` · `총비용`(오른쪽 잘림 — 열이 더 있을 수 있음).
- 행: 첫 칸이 **`+ 추가`**(파란 링크) 또는 **`이미등록`**(회색, 행 전체 흐림) 둘 중 하나. 보이는 8행: 11번노원(+추가) · 3:1필라테스(+추가) · **5번노원(이미등록)** · **6세필라테스(이미등록)** · **7세필라테스(이미등록)** · H필라테스노원(+추가) · INTOPILATES(+추가) · 그룹필테노원(+추가) — 전부 `확장`·노출 1·클릭 0·0원. 정렬은 검색어 오름차순(숫자 → 영문 → 한글)으로 보임.
- 아래: `취소` · 파란 `저장`. **(스크린샷 3, 09-27 추가)** 표 아래에 페이지네이션 `< 1 2 3 4 5 ··· 18 >`(이 그룹·이 기간은 **18페이지 ≈ 171~180개 검색어**)과 **`행표시: 10 ∨`** 선택 상자(페이지당 행 수 변경 가능 — 최댓값 미확인). 스크린샷 3의 추가 행: 근처산전필라테스(`+ 추가` — 산전 계열이 등록돼 있지 않음, [의도된 동작] 9와 일치) · **나다운필라테스(`이미등록`, 노출 4)** = 09-10 목록의 이름이 이 그룹 UI에 있음을 확인.
- **`다운로드` 파일 [실측: 사용자 09-27]**: 엑셀로 받아지지만 **`이미등록/추가` 상태 열이 없다**(사용자 확인) → 4-D의 '다운로드 파일 대조'는 성립하지 않고, 상태는 화면(표 텍스트 복사 또는 스크린샷)에서만 얻는다. 받은 엑셀은 '그 그룹에서 그 기간에 노출된 검색어 목록'으로는 쓸 수 있다(검색어 보고서 CSV에는 없는 **그룹별** 정보).
- **뜻(이번 회차의 두 번째 큰 발견)**: ① **"이미 있는 검색어를 넣으면 어떻게 되는지"에 대한 화면 답 — 넣을 수 없다. 이미 등록된 검색어는 `이미등록`으로 표시되고 `+ 추가` 링크 자체가 없다.** ② 이 표는 "그 기간에 노출된 검색어마다 등록 여부"를 그룹별로 보여 주므로, **"재노출된 검색어가 등록돼 있는가"를 판정하는 데는 제외 검색어 탭 전량보다 이 보기가 더 직접적**이다(재노출 검색어는 정의상 기간 안에 노출이 있으니 여기 반드시 나온다). ③ `다운로드` 엑셀에는 상태 열이 **없다**(사용자 확인) — 3절의 "UI 유무" 열은 이 표의 텍스트 복사(행표시 최대) 또는 스크린샷으로만 채울 수 있다(요청 2-①). ④ **`+ 전체추가`는 기간의 검색어 전부를 한 번에 추가하는 위험 버튼** — 자동화 어느 경로에서도 누르지 않는 요소로 references에 박아야 한다. ⑤ 6세필라테스(09-26 등록)·7세필라테스(09-24 등록)가 `이미등록`인 것은 대조 목록 표와 일치. **5번노원**은 표의 어느 원본 목록에도 없는 이름인데 `이미등록`이다 → 원본 미보관 191개(38·67·79) 중 하나로 추정 [추론] — "UI에 있는데 기록에 없는 것"의 첫 실례.
- 아직 못 본 것: 직접 입력 칸(`확장 검색 (0/950)` 카운터가 있던 곳)의 현재 모습·입력 구분자·저장 후 성공/오류 문구·`일치(유사검색어)` 칸(요청 2-③). API `type`과의 대응(확장 검색 = `EXP_SEARCH`)은 1절.

**2-2b. 대화상자 전체(스크린샷 4~9 = 6페이지 전체, 09-27 두 번째 회신) [실측: 사용자 화면]**
- 제목 `제외 검색어 추가` · 우상단 `×`. 안내 배너: `광고가 노출되었던 검색어에 대해 자세한 성과지표를 보기 원하면 다차원 보고서로 이동하세요. 다차원 보고서`.
- 설명 3줄: `일치 이외 검색어 중 노출을 원하지 않는 검색어를 추가합니다.` / `검색 유형에 따라 제어 가능한 검색어 개수가 상이하여 별개로 관리됩니다. 제외 검색어 도움말 바로가기` / `ADVoost Max는 제외 검색어 타게팅이 적용되지 않으며, 하단의 기간별 검색어 결과에도 집계되지 않습니다.`
- 직접 입력 칸 2개(나란히): **`확장 검색 (0/950)`** · **`일치(유사검색어) (0/50)`**, 둘 다 placeholder `한 줄에 하나씩 입력하거나 아래에서 추가하세요.` → **입력은 줄 단위**(한 줄에 하나) [실측]. "검색 유형에 따라 제어 가능한 검색어 개수가 상이" 문구와 950/50 두 숫자로 보아 **950·50은 유형별 한도**로 읽힌다 — 두 그룹(스크린샷 2·4) 모두 `0/950`이라 "남은 용량"이 아니라 고정 한도일 가능성이 높다 [추론]. 이 카운터가 기존 등록분을 포함하는지(등록 200개면 200/950로 시작하는지)는 여전히 미확인 — 09-17 기록은 "0/950 = 새로 입력 중인 항목 수".
- 기간 줄: `2026.08.28. → 2026.09.26.` 달력 · `<` `>` · `기간의 검색어` · 우측 `다운로드`. 필터 `필터를 입력해 주세요`. 표 헤더 `+ 전체추가 | 검색어 | 검색 유형 | 노출수 | 클릭수 | 총비용`(각 열 필터·정렬 아이콘). 행 첫 칸 `+ 추가`(파란 링크) / `이미등록`(회색, 행 흐림). 아래 `< 1 2 3 4 5 6 >` · `행표시: 30 ∨`(10 → 30으로 바꿔 6페이지 = 174행).
- 표 아래 문구: `전환 추적을 사용하지 않은 경우, 전환율이 집계되지 않습니다.` / `전환율 확인을 위해서 전환 추적 관리를 신청을 권장드립니다. 전환 추적 관리 바로가기`. 그 아래 **`이유를 입력하시겠습니까? (선택)`** — `제외 검색어로 등록하신 이유를 기록할 수 있습니다.` 라디오 `네 / ●아니오` → API `description`(1절)에 대응하는 UI 필드 [추론]. 맨 아래 `취소` · `저장`.
- 성공·오류 문구·저장 뒤 화면: 이번에도 미확인(저장을 누르지 않았으므로 — 구현 회차 시험 등록 때 기록).

**2-3. 그룹명 ↔ URL**: 세 URL의 그룹 ID `…072697414` / `…072288536` / `…072587864`의 페이지 제목은 못 읽었다(스크린샷의 그룹명은 흐림 처리). 스크린샷 목록 3세트는 사용자 확인으로 **노원산전필라테스(6장)·노원역필라테스(11장)·상계동필라테스(3장)**, 세 그룹 다 합계 대조로도 일치 — 어느 ID가 어느 그룹인지는 여전히 요청 3. 합본 키워드 CSV의 `새로필라테스 파워링크` 캠페인 활성 그룹은 **노원역필라테스·상계동필라테스·노원산전필라테스** 3개(노원키즈필라테스는 9/17 이후 노출 0 = OFF, 노원필라테스(삭제)는 제외 그룹)라 이 셋일 가능성이 높으나 **어느 ID가 어느 그룹인지는 사용자 확인**(요청 2-④) [추론]. 09-17 기록의 등록 위치는 "파워링크 4그룹"(노원키즈 포함) — OFF 그룹에도 9/17까지의 목록이 남아 있을 것이다 [추론]. config에 그룹명·ID·URL을 한 항목에 같이 두는 이유.
**2-4. references에 넣을 요소**: 위 2-1·2-2의 탭 이름·버튼 텍스트·표 헤더·행 상태 값(`+ 추가`/`이미등록`)·배지(`적은검색량`)·유형 문자열(`확장 검색`)·시각 형식은 구현 회차에 `references/exclusion-ui.md`로 옮긴다. `find()` 질의 후보: "제외 검색어 탭", "제외 검색어 추가 버튼", "기간의 검색어", "다운로드 버튼", "이미등록", "저장 버튼" — 좌표 클릭은 쓰지 않는다(배민 점검표 v19 원칙).

## 3. 등록 목록 ↔ 저장소 대조 목록 — CSV 쪽 [실측], UI 쪽 3그룹 전부 [실측: 사용자 화면 23장]

**기록 쪽(대조 목록 표, 1,352행 기준 457~469행)**: 09-20 17 · 09-21 22 · 09-23 32 · 09-24 9 · 09-25 11 · 09-26 신규 6 · 09-26 재등록 7(32의 부분집합) · 09-27 제안 14(9/26 첫 등장 11 + 32 중 재노출 3, **미등록**) · 09-10 38(이름 아는 것 10) · 09-17 개별 67 + 어근 7(이름 아는 것 3 — 노원역운동은 09-25에 미등록 판명) · 09-17~19 79(이름 없음). 원본이 있는 이름 = 17+22+32+9+11+6 = **97개**, 원본 없는 등록 = 38+67+7+79 = **191개**(이름 13개만 앎).
**UI 쪽**: 3그룹 각 목록 — **읽지 못함.** "기록에 있는데 UI에 없는 것 / UI에 있는데 기록에 없는 것 / 3그룹 간 차이" 세 열은 비어 있다. 이 표가 "등록했었냐" 질문을 없애는 근거라는 지시는 그대로 유효하고, 채울 수단은 요청 3(사용자가 붙이는 탭 목록 텍스트) 또는 4절의 읽기 경로다.

**CSV 쪽 [실측 — `registry_check.py`, 합본 검색어 CSV `검색 유형=="확장"` 행, 등록일 다음 날 이후]**

| 목록 | 항목 | 등록 후 확장 재노출 이름 | 상세(날짜·회) |
|---|---|---|---|
| 09-20 | 17 | **0** | 9/21~9/26 엿새 0 |
| 09-21 | 22 | **0** | 9/22~9/26 닷새 0 |
| 09-23 | 32 | **12** | 9/24 6개·11회 / 9/25 7개·13회 / 9/26 3개·3회(기록과 일치). 이름: 노원역9번출구(9/25 3) · 노원역6번출구(9/24·25, 5) · 노원역10번출구(9/26 1) · 노원체험(9/26 1) · 노원역거리(9/24 1) · 노원역추석(9/24·25, 5) · 노원9월행사(9/25 2) · 노원역테니스레슨(9/25 1) · 노원역배스킨(9/26 1) · 노원구어린이(9/24·25·26, 5) · 노원어린이체험(9/24·25, 2) · 노원역키즈(9/24 1) — 전부 클릭 0 |
| 09-24 | 9 | **0** | 9/25~9/26 이틀 0 |
| 09-25 | 11 | **0** | 9/26 첫날 0 |
| 09-26 신규 | 6 | — | 등록 당일만 있음(판정 시작 9/27) |
| 09-26 재등록 | 7 | — | 9/26 노원구어린이 1회 = 재등록 당일(판정 안 함), 나머지 0 |
| 09-27 제안 | 14 | (미등록) | 14개 전부 9/26 확장 노출(그래서 후보) — 재등록 제안 3개는 09-23 목록에도 있음(노원역10번출구 5회·노원역배스킨 4회·노원체험 8회는 전 기간 합) |
| 09-10 이름 10 | 10 | 0 | 9/11~9/26 0 |
| 09-17 이름 3 | 3 | 노원역체험 | 9/18·9/20 각 1 → 09-21 목록에 재등록으로 종결(465행) |

- (아래 "UI 쪽 첫 실측" 전에 쓴 보류 판정 — 원문 보존, 노원산전 그룹은 그 절에서 갱신) - 판정 ① "09-24·09-25 재노출 32개가 실제로 등록돼 있는지": **UI 미실측 → 판정 불가(보류).** 다만 같은 칸·같은 방식으로 등록했다고 기록된 여섯 목록(17·22·32·9·11·6) 중 **09-23 목록만** 재노출이 있고 나머지 다섯은 다음 날부터 0인 점은 "일부 그룹 또는 일부 이름의 등록 누락" 가설과 맞고 "등록돼 있는데도 노출" 가설과는 덜 맞는다 [추론 — UI 목록이 유일한 확정 근거]. 재등록한 7개가 9/27부터 0이면 누락 쪽이 더 굳어진다.
- 판정 ② 09-27 제안 14개: UI 미실측 → **"미등록" 유지**(표 현행 그대로, 등록일 칸 비움).
- 두 목록 이상에 걸친 이름(중복 등록 후보) [실측]: 노원9월행사·노원구어린이·노원어린이체험·노원역6번출구·노원역9번출구·노원역추석·노원역테니스레슨(09-23 ↔ 09-26 재등록) / 노원역10번출구·노원역배스킨·노원체험(09-23 ↔ 09-27 제안) / 노원역체험(09-17 ↔ 09-21). 자동화 시 "이미 UI에 있는 이름은 등록 후보에서 자동 제외"가 이 중복을 없앤다.

**UI 쪽 첫 실측 — 그룹 1(사용자 스크린샷 6장 전사 174행, `기간의 검색어` 2026.08.28.~09.26., 전사 파일은 회차 폴더 `group_period_terms_g1.txt`)** [실측: 사용자 화면 + `ui_vs_registry.py`]
- 그룹 판별: 전사 합계 노출 461 · 클릭 10 · 비용 5,155원 ↔ 합본 키워드 CSV 8/28~9/26 자동매칭(키워드 `-`) 그룹별 합 — **노원산전필라테스 466 · 10 · 5,155원**(노원역 921·17·6,987 / 상계동 165·3·1,927). 클릭·비용 정확 일치, 노출 5회 차(ADVoost 집계 제외 문구 또는 전사 오차 [추론]) → **노원산전필라테스 그룹**(사용자 확인 09-27 "노원산전이 맞아").
- 174행 = `이미등록` 36 · `+ 추가` 138(전부 `확장`). 다운로드 엑셀에 없는 상태 열을 화면에서 읽은 것.

| 대조 | 결과(노원산전 그룹, 이 기간에 노출된 이름만 판정 가능) |
|---|---|
| A. **UI에 있는데 기록에 없는 것**(`이미등록`인데 원본 있는 목록·이름 아는 것 어디에도 없음) | **14개**: 5번노원 · 노원구오픈 · 노원당구레슨 · 노원배드민턴레슨 · 노원새로오픈 · 노원새로오픈맛집 · 노원새로오픈횟집 · 노원오픈 · 노원힐링장소 · 노원힐링체험 · 동탄필라테스새로오픈 · 모든날필라테스 · 배드민턴레슨노원 · 새로오픈맛집노원 — 원본 미보관 191개(38·67·79) 유래로 추정 [추론] |
| B. **기록에 있는데 UI에 없는 것**(기록 이름이 `+ 추가` = 이 그룹에 미등록) | **8개, 그중 7개가 09-23 목록**: 11번노원 · 노원]하루공간 · 노원구어린이체험 · 노원새로오픈사우나 · 노원새로오픈술집 · 노원체험(7회, 09-27 재등록 제안에도 있음) · 아기랑노원구 / 09-27 제안: 노원필테강사(제안대로 미등록) |
| C. 기록 이름이 `이미등록` | 09-10 2(나다운필라테스·새로오픈) · 09-20 5 · 09-21 6 · **09-23 3(노원9월행사·노원구어린이·노원어린이체험 = 09-26 재등록 7개 중 이 그룹 노출이 있는 3개 전부)** · 09-24 3 · 09-25 2 · 09-26 1(6세필라테스) |
| D. 목록별(이 그룹 기간 목록에 등장한 이름 기준) | 09-10 2/2 등록 · 09-20 5/5 · 09-21 6/6 · **09-23 10개 중 등록 3 / 미등록 7** · 09-24 3/3 · 09-25 2/2 · 09-26 1/1 · 09-26 재등록 3/3 · 09-27 제안 2개 등장(노원체험·노원필테강사) 둘 다 미등록 |
| E. `never_exclude_patterns`(운동·산전·산후·임산부) 해당 이름 | 20개 전부 `+ 추가`(미등록) — [의도된 동작] 9 결정이 UI에서도 지켜지고 있음 |
| F. 경쟁사명(config `competitors`) 포함 이름 | 13개 전부 `+ 추가`(미등록) — 경쟁사명을 자동 제외 대상으로 두는 안(고를 항목 3)과 현 상태가 일치 |

- **판정 ① 갱신(노원산전 그룹 한정)**: 09-23 32개는 **이 그룹에 등록돼 있지 않다**. 근거 — 이 그룹 기간 목록에 나온 09-23 이름 10개 중 7개가 `+ 추가`, `이미등록`인 3개는 전부 09-26 재등록분이고, 다른 여섯 목록(09-10·20·21·24·25·26)은 등장 이름 19/19 전부 `이미등록`. 즉 09-24·25·26 재노출의 원인은 "등록돼 있는데도 노출"이 아니라 **등록 누락(적어도 이 그룹)**이다 [실측]. 재등록 7개 중 이 그룹 노출이 없던 4개(노원역9번출구·노원역추석·노원역6번출구·노원역테니스레슨)는 이 목록으로 판정 불가(다른 그룹 회신 대기). 09-24 기록 "위치는 맞는데 원인 미상"은 이 절로 정정(원문 보존).
- **판정 ② 갱신**: 09-27 제안 14개 중 이 그룹 목록에 나온 2개(노원체험·노원필테강사)는 **미등록 확인**. 나머지 12개(노원역헬스장 등 `노원역…` 계열 대부분)는 이 그룹 기간 목록에 없음 = 이 그룹 노출이 아님 → 노원역·상계동 그룹 회신으로 판정.
- 설계 함의: ① "기간의 검색어 + 이미등록" 보기가 **그룹별** 등록 여부를 정확히 알려 주므로 재노출 판정 규칙(4절)은 "어느 그룹에서 노출됐고 그 그룹에 등록돼 있는가"를 그룹 단위로 적어야 한다 — 검색어 보고서 CSV에는 그룹 열이 없어 CSV만으로는 그룹을 못 가르고, 자동매칭 노출은 그룹마다 따로 난다. ② 후보 자동 산출의 "이미 등록된 이름 제외"도 그룹별로 해야 한다(한 그룹만 빠진 이름을 잡아내려면). ③ 표기 변형 실례: `노원맘카페-`(끝에 하이픈, `+ 추가`)는 09-21 등록 `노원맘카페`와 다른 문자열 — 정확 일치 원칙 유지. ④ 기간의 검색어 표에는 `일치(유사검색어)` 유형 행도 섞여 나온다(노원역 그룹 5행) — 확장 검색 칸 후보·판정은 `검색 유형 == 확장` 행만.
- 노원역필라테스 그룹: 아래 "두 번째 실측". 상계동필라테스 그룹: 아래 "세 번째 실측" — 3그룹 완료.

**UI 쪽 두 번째 실측 — 노원역필라테스(사용자 확인, 스크린샷 11장 전사 309행 = 30×10 + 9, `기간의 검색어` 2026.08.28.~09.26., 전사 파일 `group_period_terms_g2.txt`)** [실측: 사용자 화면 + `ui_vs_registry2.py`]
- 그룹 판별 재확인: `확장` 행 304개 합계 노출 921 · 클릭 17 · 비용 6,985원 ↔ 키워드 CSV 8/28~9/26 노원역필라테스 자동매칭 **921 · 17 · 6,987원**(노출·클릭 정확 일치, 비용 2원 차 = 전사 오차 범위). 나머지 5행은 `일치(유사검색어)` 유형(노원구근처필라테스 27 · 노원역근처필라테스 9 · 노원구인근필라테스 6 · 필라테스노원역 3 · 필라테스노원역점 1 = 46회) — 파워링크 등록 키워드의 유사검색어 노출이라 자동매칭 합에 안 들어감 [추론]. **이 표에는 `일치(유사검색어)` 유형 행도 섞여 나오므로** 자동화에서 "확장 검색" 칸 후보는 `검색 유형 == 확장` 행으로 한정해야 한다.
- 309행 = `이미등록` 135 · `+ 추가` 174. 노원산전(174행)보다 목록이 크고 등록 비율도 높다(44% vs 21%) — 09-10·09-17의 대량 등록이 `노원역…` 이름 위주였기 때문 [추론].

| 대조 | 결과(노원역 그룹, 이 기간에 노출된 이름만 판정 가능) |
|---|---|
| A. UI에 있는데 기록에 없는 것 | **73개**(`이미등록`인데 원본 있는 목록·이름 아는 것 어디에도 없음) — 노원역1번출구·노원역5번출구·노원역정기주차·노원역지도(09-10 기록의 `1번출구·5번출구·정기주차·지도`가 **`노원역` 접두 형태로 등록돼 있었음** [추론 — 이미등록 상태로 판단, 467행의 "앞에 노원역이 붙은 형태인지 미확인" 해소]) · 노원역새로오픈/새로생긴/오픈/우동/까페/사진/단체 계열 다수 · 노원우동 19 · 노원역+헬스장 · 노원역+6번출구 · 노원역베스킨 등 — 38·67·79개 미보관분의 실물 [추론]. 전체 이름은 회차 폴더 `ui_g1g2_annotated.csv` |
| B. 기록에 있는데 UI에 없는 것 | **24개, 그중 09-23 목록 17개**: 노원역+9번출구(3) · 노원역2번출구(7) · 노원역10번출구(5) · 노원역세 · 노원역금 · 노원역거리(4) · 노원역혼자 · 노원역힐링공간 · 노원역추천장소 · 노원역;24시 · 노원역11-210 · 노원역새로오픈술집 · 노원역배스킨(4) · 노원역아기 · 노원역키즈 · 노원구어린이체험 · 노원체험 / 09-27 제안 10개(아래 판정 ②). 그 외 0 |
| C. 기록 이름이 `이미등록` | 09-10 **6/6**(나다운필라테스 28·노원역카페 35·노원역주차장 21·노원역주차 9·수정역필라테스 7·새로오픈) · 09-17 **3/3**(노원역헬스 17·노원역데이트 7·노원역체험 8) · 09-20 **12/12** · 09-21 **16/16** · 09-23 8(재등록 5: 노원역9번출구 28·노원역6번출구 7·노원역추석 9·노원역테니스레슨·노원어린이체험 + 재등록 아닌 3: **노원역8번출구·노원역출구·노원역배스킨라빈스** — 464행 "8번출구·출구는 이전 목록 포함 가능"과 일치, 배스킨라빈스도 미보관 목록에 있었을 가능성 [추론]) · 09-24 **6/6** · 09-25 **7/7** · 09-26 **5/5** · 09-26 재등록 5/5 |
| D. 목록별 | 09-23만 **25개 등장 중 등록 8 / 미등록 17**, 다른 아홉 목록은 등장 이름 **66/66 등록** |
| E. `never_exclude_patterns` 해당 | 17개 전부 `+ 추가`(미등록) — **노원역운동 12회 `+ 추가`** = 09-25 사용자 답("제외 안 했어")과 일치, [의도된 동작] 9 재확인 |
| F. 경쟁사명 포함 | 7개 전부 `+ 추가`(미등록) |

**두 그룹 교차 [실측]**: 두 그룹 모두에 등장한 이름 **47개의 상태가 47/47 동일**(예: 노원체험·노원구어린이체험 둘 다 `+ 추가`, 노원어린이체험 둘 다 `이미등록`, 나다운필라테스·새로오픈·5번노원·모든날필라테스·노원배드민턴레슨 둘 다 `이미등록`). 즉 "그룹마다 다르게 등록된" 사례는 두 그룹 사이엔 0 — 09-23 목록의 누락도 **두 그룹에서 같은 방향**이다.

**09-23 32개 최종 판정표(노원산전·노원역 두 그룹 기준, 상계동 대기)** [실측]

| 상태 | 개수 | 이름 |
|---|---|---|
| `이미등록`(두 그룹 중 등장한 곳에서) | **10** | 재등록 7 전부(노원역9번출구·노원역6번출구·노원역추석·노원역테니스레슨·노원9월행사·노원구어린이·노원어린이체험) + 재등록 아닌 3(노원역8번출구·노원역출구·노원역배스킨라빈스 — 이전 미보관 목록 유래 추정 [추론]) |
| `+ 추가`(등장한 그룹에서 미등록) | **22** | 노원역+9번출구·노원역2번출구·노원역10번출구·노원역세·노원역금·노원역거리·노원역혼자·노원역힐링공간·노원역추천장소·노원역;24시·노원역11-210·노원역새로오픈술집·노원역배스킨·노원역아기·노원역키즈(이상 노원역) · 11번노원·노원]하루공간·노원새로오픈술집·노원새로오픈사우나·아기랑노원구(이상 노원산전) · 노원체험·노원구어린이체험(두 그룹 다) |
| 두 그룹 모두 미등장 | 0 | — |

→ **판정 ① 확정(두 그룹)**: 09-23 32개 중 9/26 재등록 7개와 이전 목록 유래 3개를 뺀 **22개는 노원산전·노원역 어느 쪽에도 등록돼 있지 않다.** 09-24·25·26 재노출(12개 이름)은 전부 이 22개 + 재등록 전의 7개에서 나온 것 — **"등록돼 있는데도 노출"은 0건, 전부 등록 누락**. 사용자 09-24 답("9/23 등록했어")과 어긋나므로 그날 등록이 저장되지 않았거나 다른 그룹(노원키즈 OFF?)에 들어갔을 가능성 [추론 — UI로는 판별 불가]. 464행의 "원인 미상"은 이 절로 정정(원문 보존). 22개는 다음 등록 후보에 **자동 포함**(4절 규칙 (b))이 맞다.
→ **판정 ② 확정(두 그룹)**: 09-27 제안 14개 중 **12개 미등록 확인**(노원역 10: 노원역헬스장·노원식당맛집·노원역24시간우동·노원역7번출구주차·노원역9번·노원역맛집출구·노원역새로오픈소고기·노원역10번출구·노원역배스킨·노원체험 / 노원산전 2: 노원필테강사·노원체험). 나머지 **새로클린노원·노원아띠·노원역보세 3개는 두 그룹 어디에도 등장하지 않음** → 상계동 그룹에서 전부 `+ 추가`로 확인(아래 세 번째 실측). "미등록" 유지.
- 노원산전 절의 "재등록 7개 중 이 그룹 노출이 없던 4개는 판정 불가"는 노원역 그룹에서 전부 `이미등록`으로 해소.


**UI 쪽 세 번째 실측 — 상계동필라테스(사용자 확인, 스크린샷 3장 전사 63행 = 30+30+3, 전사 파일 `group_period_terms_g3.txt`)** [실측: 사용자 화면 + `ui_vs_registry3.py`]
- 그룹 판별 재확인: 합계 노출 165 · 클릭 3 · 비용 1,927원 = 키워드 CSV 8/28~9/26 상계동필라테스 자동매칭 **165 · 3 · 1,927원**(세 값 정확 일치). 63행 = `이미등록` 14 · `+ 추가` 49, `일치(유사검색어)` 행 0.
- A. UI에 있는데 기록에 없는 것 **8개**: 노원디자인새로 · 노원새로비트 · 노원새로생긴 · 노원새로오미자 · 노원새로이 · 노원역타이어 · 노원오미자새로 · 모든날필라테스. B. 기록에 있는데 UI에 없는 것: **09-27 제안 3개**(새로클린노원 2회 · 노원아띠 · 노원역보세 — 두 그룹에 없던 3개가 여기 있었고 전부 `+ 추가`). C. 기록 이름이 `이미등록`: 09-10 2(나다운필라테스 10·새로오픈) · 09-20 1(노원역세차) · 09-21 1(노원역정정) · 09-25 2(노원역금호스·한스노원역) — **6/6**. 09-23 32개 이름은 이 그룹 기간 목록에 **하나도 없음**(상계동 자동매칭에서 나온 적 없는 이름들). E. never_exclude 1개(상계산후필라테스) `+ 추가`. F. 경쟁사명 0개.

**3그룹 간 차이 [실측, 지시 항목 3의 마지막 열]**

| 항목 | 노원산전(174행) | 노원역(309행) | 상계동(63행) | 3그룹 합 |
|---|---|---|---|---|
| `이미등록` / `+ 추가` | 36 / 138 | 135 / 174 | 14 / 49 | 이름 종류 **494**, 어느 한 그룹이라도 `이미등록` **170** |
| UI에 있는데 기록에 없는 것(원본 미보관분 실물) | 14 | 73 | 8 | 중복 제외 약 90 [추론 — 세 그룹 합집합] |
| 기록에 있는데 UI에 없는 것 | 09-23 7 + 09-27 2 | 09-23 17 + 09-27 10 | 09-27 3 | 09-23 **22**(이름 기준) + 09-27 **14** |
| 09-10·17·20·21·24·25·26·재등록 목록 이름 | 19/19 등록 | 66/66 등록 | 6/6 등록 | **91/91 등록** — 09-23 목록만 예외 |
| 두 그룹 이상 등장한 이름의 상태 | 48개 중 **상태 다른 것 0** (세 그룹 모두 등장 4: 나다운필라테스·모든날필라테스·새로오픈 `이미등록`, 새로필라테스 `+ 추가`) | | | |

- 결론: **그룹 간 차이는 없다** — 같은 이름은 어느 그룹에서도 같은 상태이고, 등록 누락은 그룹이 아니라 **09-23 목록(회차) 단위**로 났다. 즉 "3그룹에 같은 목록을 넣는다"는 운영은 지켜졌고, 09-23 회차 하나가 통째로(재등록·이전 목록 유래 10개를 제외한 22개) 어느 그룹에도 없다.

**최종 판정(3그룹 완료)** [실측]
- **판정 ① — 09-24·09-25 재노출 32개**: 32개 중 **22개는 세 그룹 어디에도 등록돼 있지 않다**(노원역 17 · 노원산전 5, 노원체험·노원구어린이체험은 두 그룹 다 `+ 추가`). 나머지 10개는 `이미등록`이나 그중 7개는 9/26 재등록분, 3개(노원역8번출구·노원역출구·노원역배스킨라빈스)는 09-23 이전 미보관 목록 유래로 보인다 [추론]. 따라서 9/24·25·26 재노출은 **전부 "미등록"이 원인**이고 "등록돼 있는데도 노출"은 0건이다. 464행·545행의 "원인 미상"과 [의도된 동작] 9 옆에 이 사실을 두는 것이 다음 회차 판정 기준이다(원문 보존, 이 절로 정정). 22개 이름: 노원역+9번출구 · 노원역2번출구 · 노원역10번출구 · 노원역세 · 노원역금 · 노원역거리 · 노원역혼자 · 노원역힐링공간 · 노원역추천장소 · 노원역;24시 · 노원역11-210 · 노원역새로오픈술집 · 노원역배스킨 · 노원역아기 · 노원역키즈 · 11번노원 · 노원]하루공간 · 노원새로오픈술집 · 노원새로오픈사우나 · 아기랑노원구 · 노원체험 · 노원구어린이체험.
- **판정 ② — 09-27 제안 14개**: **14/14 미등록 확인**(노원역 10 · 노원산전 2 · 상계동 3, 노원체험은 두 그룹). 대조 목록 표의 "미등록" 그대로.
- 두 판정을 합치면 지금 등록 후보로 남은 이름은 22 + 14 − 3(겹침: 노원역10번출구·노원역배스킨·노원체험) = **33개**(등록은 사용자 승인 뒤, 이번 회차엔 손대지 않음 — 고를 항목 7).

## 4. 설계안(문서만 — 구현 없음. 경로 A~D 중 채택은 사용자)

**4-0. 경로와 무관한 공통 원칙**
- **쓰기(등록·삭제)는 승인 문구 뒤에만, 읽기는 언제나.** 승인 없는 회차(검증·진단·"읽기만")는 읽기 전용으로 돈다.
- 후보 산출은 지금 갱신 회차가 손으로 하던 것을 그대로 규칙화: 합본 검색어 CSV `확장`·클릭 0 행 중 **첫 등장**(직전 회차 CSV에 없던 이름) → `never_exclude_patterns` 해당 제외 → **UI(또는 pull 파일)에 이미 등록된 이름 제외** → 남은 것을 무관/애매/키즈로 분류해 채팅에 제시(분류는 제안, 결정은 사용자 — 현행과 같음). "경쟁사" 이름은 후보에서 자동 제외(경쟁사표 데이터가 사라지므로) — 채택 여부는 고를 항목 3.
- 승인 문구는 그대로 붙여 답하게 고정한다(다음 형식, 세부는 고를 항목 2):
  > 제외 검색어 등록 승인 요청 — 대상: 파워링크 3그룹(노원역·상계동·노원산전) "확장 검색" 칸 / 건수: N / 목록: 이름1 · 이름2 · … / 제외한 것: never_exclude 해당 n·이미 등록 m
  > 답: "등록 승인 N개" (또는 뺄 이름을 적어 주면 그만큼 뺀 뒤 다시 확인) — 이 답이 오기 전에는 아무것도 쓰지 않는다.
- 등록 → 읽기 확인 → 기록은 한 회차 안에서 끝내되, **기록의 `verified`는 읽기 확인을 통과한 이름에만** 붙인다. 읽기 확인이 안 되면(차단·오류) `registered / unverified`로 남기고 다음 회차 첫 일로 넘긴다.
- 어느 경로든 `+ 전체추가`(2-2 ④)와 `일치(유사검색어)` 칸·플레이스 그룹은 **금지 요소**로 references에 박고, 입력 내용을 저장 직전에 read-back 해 승인 목록과 정확히 같은지 대조한 뒤에만 저장한다.

**4-A. API 경로(경로가 열리면 1순위 후보 — 1절 트레이드오프)**
단계: ① 회차 시작 시 3그룹 `GET …/restricted-keywords?type=EXP_SEARCH` → registry 갱신(이름·`nccAdgroupRestrictKwdId`·`regTm`·그룹) → 재노출 판정(4절 규칙) ② 후보 산출·제시 ③ 승인 문구 ④ 그룹마다 `POST` body `[{"keyword":…, "type":"EXP_SEARCH", "description":"saero-ad-report YYYY-MM-DD"}]` — **`description`에 회차 표시를 넣어 스킬 등록분과 사용자 수동 등록분을 UI·API 양쪽에서 구분** ⑤ 응답의 항목별 `resultStatus`로 성공/실패 분리 → 성공분은 id 보관 ⑥ 읽기 확인: 3그룹 `GET` 재조회로 승인 목록 ⊆ 등록 목록 ⑦ 기록(4절 "기록 위치"). 회차당 호출 GET 3 + POST 3 + GET 3.
전제: `api.searchad.naver.com` 허용(0절) · 도구 > API 사용 관리에서 서비스 신청·라이선스/비밀키 발급(요청 1) · 3그룹 `useAdvoost` false(1절 2026-09-16 노트) · 첫 실행은 읽기 전용으로 GET만.
키 보관: **저장소 금지(공개 저장소)**. 배포 토큰과 같은 방식 — 매 회차 채팅 입력 → 파일로만 저장 → 회차 후 폐기 안내. 키가 계정 전체 쓰기 권한이라는 점을 승인 문구 옆에 한 번 적어 둔다. 대안(사용자 PC 파일)은 device_bash 네트워크가 403이라 지금은 의미 없음.
구현 형태: `scripts/exclusions.py`(`pull` / `propose` / `push --approved <파일>` / `verify` / `delete --ids`, `--dry-run`은 서명·본문 준비까지만 하고 전송 0 — deploy.py와 같은 원칙으로 "정말 아무것도 안 보내는지" 실측).

**4-B. DOM 경로(Claude in Chrome — 경로가 열리고 API를 쓰지 않을 때)**
단계: ① 그룹 페이지 3개 → `제외 검색어` 탭 → 목록 전량 읽기(페이지네이션, `find()`·ref, 10행/페이지) 또는 **`제외 검색어 추가 → 기간의 검색어` 보기의 `이미등록` 표시 읽기**(재노출 판정만 필요하면 이쪽이 왕복이 적다 — 저장은 누르지 않고 `취소`로 닫는다) ② 후보·승인(4-0) ③ `제외 검색어 추가` → 직접 입력 칸에 줄 단위 입력(09-25 파일 형식이 그대로 먹혔음 — 2-2 미확인 항목 확인 뒤) → 입력 내용 read-back = 승인 목록 검증 → `저장` ④ 성공/오류 문구 읽기 ⑤ 탭 목록 재읽기(등록시각으로 이번 등록분 식별) ⑥ 기록.
전제: Claude in Chrome 연결 + 사용자 크롬에 광고시스템 로그인(비밀번호 입력은 Claude가 못 한다) + 사이트 허용(0절 "safety restrictions" 해제 여부 미확인). 좌표 클릭 금지, `find()` 실패 시 대기·재시도 뒤 중단(배민 v19).
비용 [추론]: 그룹당 목록 10~20페이지 읽기 = 왕복 30~60회 추가 → 기간의 검색어 보기로 대체 시 그룹당 수 회.

**4-C. 경로가 열리지 않을 때 ① — 사용자 실행 CLI(스킬은 파일만 읽는다)**
`scripts/exclusions.py`를 사용자 PC의 **일반 셸**(VM 밖 — device_bash가 아니라 PowerShell 등, 네트워크 직접)에서 사용자가 실행: `pull`(3그룹 GET → `exclusions_pull_YYYY-MM-DD.json`을 스킬 폴더에 저장) → Claude가 그 파일을 읽어 재노출 판정·후보·승인 문구까지 만들고 `approved_YYYY-MM-DD.txt`를 사용자 폴더에 씀 → 사용자가 `push --approved …` 실행 → `verify`가 GET 재조회 결과 파일을 남김 → Claude가 읽어 기록. 사람이 명령 2~3번을 치지만 **판정·대조·기록은 전부 스킬**이고 "등록했었냐"는 질문이 사라진다. 키는 사용자 PC 로컬 파일(저장소·채팅에 안 올라옴 — 4-A보다 키 노출 면에서 낫다).

**4-D. 경로가 열리지 않을 때 ② — 최소안: 등록은 사용자, 읽기 확인·대조만 자동화**
매 갱신 회차에 사용자가 CSV 4종과 함께 **3그룹의 `기간의 검색어` 표 텍스트**(행표시 최대로 늘린 뒤 드래그 선택·복사 — `이미등록`/`+ 추가` 글자가 상태 열이 된다; `다운로드` 엑셀에는 상태 열이 없음 [실측 09-27]) 또는 제외 검색어 탭 목록 텍스트를 올린다 → 스킬이 대조·판정·후보·승인 문구·기록(`exclusions.csv`)까지 하고, 등록은 사용자가 승인 목록을 붙여넣어 수행 → 다음 회차 파일로 verified. 클릭 3~6회/회차가 사용자 몫으로 남지만 지금 없는 것(등록 여부 판정)이 생긴다. 0절이 풀리지 않는 한 **지금 당장 구현 가능한 유일한 안**.

**config 항목(안 — 이름·구조는 고를 항목 3)**
```json
"exclusion_targets": [
  {"group": "<그룹명, 사용자 확인>", "adgroup_id": "grp-a001-01-000000072697414", "url": "https://ads.naver.com/manage/ad-accounts/2580077/sa/adgroups/grp-a001-01-000000072697414"},
  {"group": "<…>", "adgroup_id": "grp-a001-01-000000072288536", "url": "https://ads.naver.com/manage/ad-accounts/2580077/sa/adgroups/grp-a001-01-000000072288536"},
  {"group": "<…>", "adgroup_id": "grp-a001-01-000000072587864", "url": "https://ads.naver.com/manage/ad-accounts/2580077/sa/adgroups/grp-a001-01-000000072587864"}
],
"exclusion_type": "EXP_SEARCH",
"never_exclude_patterns": ["운동", "산전", "산후", "임산부"],
"exclusion_registry": "audit/exclusions.csv"
```
- `exclusion_targets`: 그룹명·ID·URL을 한 항목에 — DOM은 URL, API는 ID, 기록·승인 문구는 그룹명을 쓴다. 그룹이 늘거나 OFF되면 여기만 고친다(노원키즈처럼). validate처럼 코드가 읽는 첫 소비자는 exclusions.py.
- `exclusion_type` 고정값 `EXP_SEARCH`: "일치(유사검색어)" 칸·플레이스는 대상 아님을 코드가 강제.
- `never_exclude_patterns`: [의도된 동작] 9의 사용자 결정(09-21·09-24)을 부분 일치 패턴으로 — 후보 산출에서 자동 제외하고 승인 문구에 "제외한 것 n"으로만 보인다. "필라테스"는 넣을 수 없다(6세필라테스·7세필라테스·노원키즈필라테스 등 이미 제외한 이름이 포함하므로). 경쟁사명(config `competitors`)을 여기 합칠지는 고를 항목 3.
- 새 필드는 같은 회차에 SKILL.md·config `_comment`에 문서화한다(checklist [수정 회차에 적용할 것]).

**기록 위치(안 — 고를 항목 4)**
- ① 대조 목록 표에 `등록일시·그룹·verified` 열 추가: 사람이 읽기 좋으나 이름이 이미 97+191개라 표가 비대해지고 기계 파싱이 어렵다.
- ② `audit/exclusions.csv`(기계 정본: `keyword, type, group, registered_at, source(skill/user), restrict_kwd_id, verified_at, status(pending/registered/verified/failed/deleted), note`) + 대조 목록 표에는 **회차별 요약 행만**(등록 n·verified n·실패 n) — 개정안 14(`audit/registry.md` 분리)와 결이 맞고 compute/validate가 읽을 수 있다. 원본 미보관 191개도 pull/다운로드 파일이 오면 `source=user, registered_at=UI 등록시각`으로 처음 채워진다.
- ③ ①+②(csv 정본 + 표는 요약) — 권장 후보이나 선택은 사용자.

**재노출 판정 규칙 변경(안 — 고를 항목 6)**
- 현행(대조 목록 절 머리말): 등록일 다음 날 이후 `확장` 행 재노출 → 이름·날짜·노출수 채팅 보고, 이틀 이상이면 탭 목록 확인 **요청**.
- 변경: 재노출 발견 시 스킬이 registry(4-A GET / 4-B 목록·`이미등록` / 4-C pull 파일 / 4-D 다운로드 파일)로 등록 여부를 먼저 판정하고 결과에 따라 셋 중 하나로 **묻지 않고** 보고한다 — (a) 등록돼 있음 → "**등록돼 있는데도 노출**(등록 YYYY-MM-DD hh:mm, 그룹 …)"로 07 각주·12번 1번에 사실만 적고 원인 추정은 "~일 수 있음"으로(네이버 매칭 지연·표기 차이 등) (b) 미등록(어느 그룹에도 없음, 또는 일부 그룹에만 있음 — 그룹별로 적는다) → "**등록 누락**"으로 보고하고 다음 후보 목록에 자동 포함(승인 대상) (c) registry를 못 읽은 회차 → "**미확인**"으로만 표기(질문 없이).
- 유지: 등록 당일은 판정하지 않음(CSV가 일 단위). 정확 일치만 판정(`노원역;24시` ≠ `노원역24시`). "확장" 행만.
- 이 규칙이 붙으면 대조 목록 절 머리말의 "탭 목록 확인 요청" 문장과 [의도된 동작] 9 뒤에 "등록 여부는 스킬이 registry로 판정, 사용자에게 묻지 않음" 한 줄이 들어간다(구현 회차).

**읽기 전용 모드·시험 등록(안 — 고를 항목 5)**
- 읽기 전용 모드: 검증·진단 회차 기본값. `exclusions.py --read-only`(pull·propose·verify만, push·delete 호출 자체 불가) / DOM은 "저장·추가·전체추가·삭제 클릭 금지" 절차. 이번 회차가 그 첫 예다.
- 시험 등록(구현 검증 회차, **사용자 입회**): 실제로 검색될 리 없는 시험 문자열 1개(예: `saero제외테스트0927`)를 그룹 **1개**에 등록 → 읽기 확인(id·등록시각) → 삭제 → 재확인 0 — 사용자가 화면에서 같이 본다. 3그룹 반복 여부·문자열은 사용자 지정. 시험 기록도 exclusions.csv에 `status=deleted`로 남긴다.
- `--dry-run`: 승인 문구·서명·본문까지 만들고 전송 0 — deploy.py 검증 때처럼 "정말 아무것도 안 보내는지"를 네트워크 로그로 실측한 뒤에만 신뢰.

**실패 처리(안)**
- 부분 등록(3그룹 중 일부만 성공 / 항목별 `resultStatus` 실패 / UI 오류 문구): 그룹×이름 결과표를 즉시 채팅에 — 성공분은 `registered`로 기록하고 읽기 확인으로 `verified`, 실패분은 코드·문구와 함께 `failed`로 기록 후 1회 재시도, 그래도 실패면 다음 후보로 되돌린다. **조용히 넘어가지 않는다.**
- 한도 초과(3716 / UI 문구): 등록 전 그룹별 현재 개수를 읽어 남은 용량을 승인 문구에 적고, 초과 예상이면 노출 많은 순으로 잘라 **다시 승인**받는다. 오래된 `적은검색량` 항목 정리(삭제)는 별도 승인 항목.
- 세션 만료·401·로그인 화면: 그 시점까지의 그룹·이름을 보고하고 중단. 재로그인·키 재입력은 사용자.
- 읽기 확인 불일치(등록 응답은 성공인데 목록에 없음): 결함으로 보고, `verified` 없이 다음 회차 첫 확인 항목.
- 모든 상태 전이는 `exclusions.csv`의 `status`로 남아 "어디까지 됐는지"가 파일에서 읽힌다.

**운영 조건(갱신 회차에 추가되는 것)**
| 경로 | 추가 조건 | 회차 부담 [추론] |
|---|---|---|
| 4-A API | 네트워크 허용 + API 신청·키 발급 + 매 회차 키 입력 | 도구 호출 +10 안팎 |
| 4-B DOM | 네트워크·브라우저 정책 허용 + Claude in Chrome 연결 + 광고시스템 로그인 | 도구 호출 +30~60(목록 전량) 또는 +10(기간의 검색어 보기) |
| 4-C CLI | 사용자가 PC에서 pull/push 실행 + 키 로컬 보관 | 사용자 명령 2~3회, 스킬 호출 +5 |
| 4-D 최소안 | 사용자가 다운로드 파일 3개(또는 목록 텍스트) 업로드 + 승인 목록 수동 등록 | 사용자 클릭 3~6회, 스킬 호출 +5 |

## 5. 리스크와 대응(각 한 줄)

| 리스크 | 무엇이 잘못되나 | 대응 |
|---|---|---|
| 잘못 등록 | 잠재고객 검색어(산전·산후·임산부·운동 계열, 경쟁사명 등)가 파워링크 확장 노출에서 조용히 차단됨 | `never_exclude_patterns` 자동 제외 + 승인 문구에 **전체 이름 명시** + 등록 응답 id(API)·등록시각(UI) 보관 → 되돌리기는 `DELETE ?ids=` 1회 / 목록에서 체크·삭제 — 되돌린 사실도 `status=deleted`로 기록 |
| 한도 | 3716 "최대 개수 초과", 숫자 미공개(950 추정) — 등록이 중간에 끊김 | 등록 전 그룹별 개수 읽기·남은 용량 보고, 초과 시 우선순위 재승인(4절 실패 처리) |
| UI 변경 취약성 | 탭·버튼·표 구조가 바뀌면 엉뚱한 행 클릭·오판(배민·쿠팡 이력의 셀렉터 깨짐 유형) | `find()`·ref만, 저장 전 read-back 검증, 실패 시 중단(좌표 우회 금지), API가 되면 API 우선 |
| 자동화 차단 | 지금 4경로 전부 차단(0절); 열려도 브라우저 정책 재차단·API 429 가능 | 차단 시 4-C/4-D로 강등하고 강등 사실을 기록·보고, 429는 sleep 후 1회 재시도·중단 |
| 로그인 세션·키 | 세션 만료로 중간 실패 / 키 유출 시 계정 전체 쓰기 노출 | 시작 시 세션·키 유효성 GET으로 확인, 만료 시 중단 보고; 키는 저장소 금지·채팅 입력 후 파일·회차 후 폐기 안내(4-C는 PC 로컬만) |
| `+ 전체추가` 오클릭 | 기간의 검색어 수백 개가 한 번에 제외됨(2-2 ④) | 금지 요소로 references 명시, 그 보기에서는 `취소`만 누른다 |
| 표기 변형·중복 | `노원역;24시`/`노원역24시`처럼 다른 문자열은 각각 등록해야 하고, 중복은 UI가 `이미등록`으로 거른다 | 판정·등록 모두 정확 일치, 변형은 후보로 따로 올린다(현행과 같음) |

## 사용자 확인 요청(이번 회차 — 답이 오면 이 절 아래에 추가 기록)
1. **도구 > API 사용 관리**: 서비스 신청 여부·라이선스/비밀키 발급 여부(화면 한 장 또는 한 줄).
2. UI 실물 보강: ① ~~3그룹 기간의 검색어 스크린샷~~(09-27 전부 수신 완료 — 노원산전 6장·노원역 11장·상계동 3장) ② 제외 검색어 탭 맨 아래(페이지·전체 건수) × 3그룹 ③ ~~대화상자 윗부분·직접 입력 칸~~(09-27 수신 완료 → 2-2b) ④ 스크린샷 1(탭 목록)이 어느 그룹인지 + 6장 목록이 노원산전필라테스가 맞는지.
3. 세 URL ↔ 그룹명 대응(노원역/상계동/노원산전).
4. 차단 해제 가능 여부: 조직 설정에서 `ads.naver.com`·`api.searchad.naver.com` 허용이 되는지(Team·Enterprise는 Admin settings → Capabilities에 네트워크 설정이 있다고 안내됨 — 이 계정에서 가능한지, 브라우저 "safety restrictions"까지 풀리는지는 미확인).
답이 오면 3절의 "UI 유무" 열·판정 ①②를 채우고 2-2 미확인 항목을 갱신한다. 답이 없으면 그대로 두고 다음 회차 첫 일로 넘긴다.

## 마무리 기록(이번 회차)
- 1차 커밋: `audit/last-audit.md`만(이 절을 파일 맨 위에 추가, 아래 09-26 기준선·이전 기록·운영 표 3개는 위치·내용 그대로). SKILL.md·scripts·config·data·checklist.md·references **변경 없음**. 배포 저장소 **변경 없음**.
- 전문 파일: 사용자 폴더 `saero-ad-report_제외검색어_탐색_2026-09-27.md`(이 절 전문).
- push 결과·재clone 행수·md5는 채팅 보고에. **1차 커밋 `42a860f`는 클라우드 push가 git 프록시 403(`not in this session's authorized repository set`)이라 점검표 개정안 7대로 PC(device_bash)에서 push했다**(재clone md5 일치). 이 절의 노원산전 그룹 실측(2-2b·3절 UI 표)은 **2차 커밋**, 노원역 그룹은 **3차**, 상계동·3그룹 최종 판정은 **4차 커밋**(전부 같은 파일만, 같은 방식 PC push).
- 다음 점검에서 대조할 것: 위 요청 1·3·4의 답 수령 여부 / 고를 항목 결정 → 구현 회차(코드·문서·config, 검증은 별도 세션, 시험 등록은 사용자 입회) / **미등록 확인 33개**(3절 최종 판정)의 등록 여부 — 등록되면 대조 목록 표에 원본·등록일 행 추가, 안 되면 "미등록" 유지 / 대조 목록 표 09-23 행에 "22개 미등록 확인(09-27 UI)" 주석을 다는 것은 구현 회차의 문서 작업 / 0절 차단 상태가 바뀌었는지 같은 4경로로 재실측.

## 내가 고를 항목
1. **경로**: A API / B DOM(Claude in Chrome) / C 사용자 실행 CLI / D 최소안(다운로드 파일 대조) — 그리고 A·B의 전제인 **차단 해제를 시도할지**(요청 4).
2. **승인 방식**: 승인 문구 형식(전체 이름 명시 → "등록 승인 N개") / 부분 승인(뺄 이름 답) 허용 / 무관·애매·키즈 분류를 제안으로 유지.
3. **config 항목**: `exclusion_targets`(그룹명·ID·URL — 대응은 요청 3) / `exclusion_type` 고정 `EXP_SEARCH` / `never_exclude_patterns` 초기값(운동·산전·산후·임산부) + **경쟁사명도 자동 제외할지**.
4. **기록 위치**: ① 표 열 추가 / ② `audit/exclusions.csv` 정본 + 표 요약 / ③ 둘 다(개정안 14 registry.md 분리와 연계).
5. **검증·시험 방법**: 읽기 전용 모드 기본 / 시험 등록 1개(그룹 1개 또는 3개, 문자열 지정) 사용자 입회 / `--dry-run` 실측.
6. **재노출 규칙**: 변경안(등록됨 → "등록돼 있는데도 노출" 보고, 미등록 → 후보 자동 포함, 판정 불가 → "미확인", 어느 경우도 묻지 않음) 채택 여부 + 등록 당일 제외·정확 일치 유지.
7. **남은 후보 처리**: 미등록으로 확인된 **33개**(09-23 목록 22개 + 09-27 제안 14개, 겹침 3 제외)는 이번 회차에 손대지 않았다 — 다음 갱신 회차에 현행(수동)으로 등록할지, 구현 뒤 첫 자동 회차로 넘길지. 등록하면 대조 목록 표에 원본·등록일을 남기고 다음 날부터 판정(현행 규칙).

## 구현 기록 (2026-09-27 기능 추가 회차, 탐색과 같은 세션 — 브랜치 `feat-exclusions`, main 미반영)

사용자 지시: "시간이 얼마나 걸리던 최고의 결과물을 만들 수 있는 방식으로 네가 제안해서 진행" → 위 "내가 고를 항목" 1~7을 아래 **임의 결정**으로 채워 구현했다(줄마다 번호 — 바꿀 것은 그 줄만).
**네이버 계정 쓰기 0**(등록·삭제·저장 호출 없음 — 실제 API 호출 자체가 이 환경에서 불가), 배포 저장소 변경 0, main 변경 0. 검증은 별도 세션(아래 재현 목록), 병합은 검증 뒤 사용자.
검증용 clone: `git clone -b feat-exclusions --single-branch https://github.com/LeeKwanBeom/saero-ad-report-skill <별도 폴더>`

### 변경 파일 (브랜치 = 11c0bc2 + 아래; 행수 `wc -l` · md5 앞 8자리)

| 파일 | 행수 | md5 | 무엇 |
|---|---|---|---|
| `scripts/exclusions.py` (신규) | 828 | 3350a596 | API 클라이언트(`NaverApi`: 서명·429 재시도·URLError→`NetworkBlocked`) + registry + 판정(`registration_status`·`blocked_reason`·`reexposure_judgement`·`build_proposal`) + 명령 `pull`/`import-ui`/`propose`/`push`/`verify`/`delete`/`test-roundtrip`/`report`. exit 0 성공 · 1 실패/미확인 · 2 네트워크 차단 |
| `tests/test_exclusions.py` (신규) | 326 | 4886b344 | 가짜 API(`FakeSender`) 16개 시험 — 서명 벡터·헤더·GET `type=EXP_SEARCH` 강제·금지 패턴·상태 판정·재노출 판정·제안 산출·pull(missing·UI 행 병합·그룹명 경고)·부분 실패→verify·`verified:false`·시험 순서 GET,GET,POST,GET,DELETE,GET·차단 exit 2·인증 401 exit 1(registry 불변)·dry-run 무전송·무변경·계획. 끝에 실제 registry md5 전/후 출력 |
| `audit/exclusions.csv` (신규) | 341 | 3c4c8232 | registry 초기값 340행: 3그룹 UI 전사(노원역필라테스 등록 135·미등록 24 / 노원산전필라테스 36·8 / 상계동필라테스 14·3) + 기록 행 `*`(등록 87·미등록 33). `group_id` 빈칸(첫 pull이 채움). 미등록 이름 33개 = 첫 자동 회차 후보 |
| `references/exclusion-ui.md` (신규) | 114 | e7998cd4 | 값 정의 정본 — API·환경 차단·PC 실행 절차·UI 실물·금지 요소·registry 스키마·판정 규칙·push/verify·시험·기록 |
| `config/report-config.json` | 82 (49→82) | 7142ecf2 | `exclusions` 블록 추가(`_comment`·`targets` 3·`customer_id` 4480035·`type` EXP_SEARCH·`never_exclude_patterns` 4·`never_exclude_competitors` true·`industry_terms` 2·`registry`·`api_base`·`description_prefix`). 기존 키 불변 |
| `SKILL.md` | 469 (438→469) | 7a9c5b87 | "설정값" 절 읽는 코드에 exclusions.py / **5-0단계** 신설(5단계 앞) / 8단계 기록 양식에 제외 검색어 줄 / 승인 지점 **(4) 제외 검색어 등록** / 참고 문서에 exclusion-ui.md·exclusions.py·exclusions.csv·test_exclusions.py |
| `audit/checklist.md` | 459 (444→459) | 03adcec5 | 버전 줄 **v4.5** / [의도된 동작] 9 뒤 한 줄 + **18~20** / [되돌리면 안 되는 것] **6행**(dry-run 무전송·금지 패턴 거부·verified:false=실패·확장 칸만·쓰기 전 읽기·시험 1건) / [검증 회차] **C** 재현 4개 |
| `.gitignore` | 5 (2→5) | c79498bf | `work/`·`*.keys.json`·`secrets/` — 키 파일·pull 스냅샷·제안 파일이 저장소에 올라가지 않게 |
| `audit/last-audit.md` | (커밋 뒤 보고) | | 이 절 + 대조 목록 머리말 한 항목(registry 판정·요약 행) + 09-23·09-27 제안 행 비고에 "09-27 UI 실측 미등록" 주석 |

### 임의 결정 (번호 = 사용자가 바꿀 단위)

1. **경로 = C(사용자 실행 CLI) + A의 코드**: 스크립트는 API 클라이언트 그대로이고, 실행만 사용자 PC PowerShell에서 한다. 근거 [실측]: 0절 4경로 차단 + 09-27 사용자 설정 화면 9장(Claude Code·Cowork·Chrome용 Claude 설정)에 네트워크 허용 목록이 없음. 환경이 열리면 같은 명령을 세션에서 돌리면 A가 된다(코드 변경 0).
2. **config 이름 = `exclusions` 한 블록**(설계안의 `exclusion_targets`·`exclusion_type`·`exclusion_registry` 낱개 키 대신). `targets`에 **그룹명을 적지 않았다** — 어느 ID가 어느 그룹인지 확인된 적이 없어(2-3절) 첫 `pull`이 API `name`으로 채운다. registry 그룹명(UI 전사)과 API 이름은 공백만 무시해 대조하고, 안 맞으면 `[주의]`를 찍는다.
3. **경쟁사 이름 자동 제외 = true**(`never_exclude_competitors`) — 경쟁사 검색어를 제외하면 07번 경쟁사표 데이터가 사라지므로. `never_exclude_patterns` 초기값은 설계대로 운동·산전·산후·임산부(부분 일치).
4. **`industry_terms`(필라테스·필테) 묶음 신설** — 설계에 없던 항목. 실제 9/26 합본으로 propose를 돌리자 정당한 업종 검색어가 신규 후보에 올라와서, 업종어 포함 이름은 "업종어 포함"으로 따로 보이고 사용자가 고른 것만 승인 목록에 넣게 했다(6세필라테스류 키즈 이름을 자동으로 잃지 않게 "보이기만" 한다).
5. **클릭 > 0 이름은 자동 후보 아님**(07번 표에서 사람이 본다) — 현행 수동 판단과 같다. 이전 CSV에 있었던 이름은 `--all` 없이는 후보 아님(그때 판단이 끝난 것으로 본다).
6. **기록 위치 = ②**(`audit/exclusions.csv` 정본 + 대조 목록 표는 요약 행). 개정안 14(registry.md 분리)와 결이 맞고 기계가 읽을 수 있다. 기존 표의 이름 원본 행은 그대로 둔다(역사).
7. **재등록 7개의 `registered_at` = 2026-09-26**(09-23 등록분은 UI에서 확인되지 않아 09-23 등록을 "미반영"으로 판정) — 그래서 9/26 노출(노원구어린이)은 "등록 당일(판정 안 함)". 나머지 09-23 등록 확인 3개(노원역8번출구·노원역출구·노원역배스킨라빈스)는 09-23 그대로.
8. **재노출 판정 = 변경안 채택**(고를 항목 6): registered→"등록돼 있는데도 노출"(마지막 등록일 다음 날 이후만), partial/unregistered→"…→ 후보"(자동 포함), 못 읽음→"미확인", `keep`→"노출 유지(사용자 결정)". 등록 당일 제외·정확 일치·확장 행만 유지. 등록일 이전 노출은 "등록 전 노출(정상)"으로 따로 표기(처음 구현은 이걸 "등록 당일"로 잘못 묶어 고쳤다).
9. **승인 방식**: 승인 문구는 설계 형식 그대로(전체 이름 명시 → "등록 승인 N개", 뺄 이름 답 허용). 승인된 이름은 `work/approved_<날짜>.txt`(한 줄 하나·`#` 주석) → `push --approved`. 금지 패턴·경쟁사 이름은 승인 목록에 있어도 `[거부]`(코드가 거부, 사용자에게 다시 묻지 않음).
10. **push = pull → 그룹별 없는 이름만 POST(50개 단위) → 항목별 `resultStatus` → verify(다시 읽기)** 를 한 명령으로. 확인 안 된 이름은 `failed`(성공이라고 쓰지 않음). 부분 실패는 그룹×이름으로 출력, **재시도는 자동으로 하지 않는다**(설계안의 "1회 재시도"보다 보수적 — 실패 원인이 문자 제한(3721~3723)이면 재시도가 무의미하고 한도(3716)면 재승인 대상이라). `description` = `saero-ad-report <날짜>`.
11. **429 = 5초 뒤 1회 재시도**, 401/403 = 즉시 `ApiError`(exit 1, registry 불변). 프록시 CONNECT 403·DNS·연결 실패 = `NetworkBlocked`(exit 2, "같은 명령을 PC에서") — 변환은 `NaverApi._send` 한 곳(sender를 바꿔 끼워도 같은 판정).
12. **시험 등록 = `test-roundtrip --confirm`, 그룹 1개, 문자열 사용자 지정(예 `saero제외테스트0927`)**, 없음 확인→POST→GET(없으면 `verified:false`)→DELETE→GET 없음→registry `deleted`. 이 세션에서는 돌리지 않았다(환경 차단 + 키 없음 + 입회 필요).
13. **UI 폴백 `import-ui`**: API를 못 쓰는 회차에 "기간의 검색어" 표 전사(`이미등록|이름|확장` 줄)를 registry에 반영. `+추가`는 registry에 이미 있는 이름만 미등록으로 적는다(그 외는 일반 검색어). 초기 registry 340행이 이 방식으로 만들어졌다.
14. **키 파일**: `{"api_key","secret_key","customer_id"}` JSON을 **이 세션에 연결되지 않은 PC 폴더**에 두고 `--key-file` 경로만. `*.keys.json`은 .gitignore. 사용자가 09-27 채팅에 비밀키가 보이는 화면을 올렸으므로 **첫 실사용 전 재발급**(아래 "다음에 볼 것").
15. **`registration_status`의 한계를 그대로 둠**: 미등록 증거가 없고 등록 증거가 한 그룹뿐이면 `registered`로 본다(UI 전사는 그 그룹에 노출된 이름만 보여 다른 두 그룹은 미확인) — 첫 `pull`이 3그룹 API 행으로 바로잡는다. 그래서 첫 실사용은 pull부터.
16. (수정 회차 2) **`--read-only` 모드는 만들지 않음** — 쓰기 명령 셋이 전부 `--confirm`(delete·test-roundtrip) 또는 승인 파일(push) + `--dry-run`을 가지므로 별도 모드가 필요 없다고 봤다(검증 8절 지적에 대한 답). 환경이 열리고 키가 있으면 절차(SKILL 5-0 6항)와 이 플래그들이 막는다.

### 실측 (이 세션, 브랜치 코드)

- `python3 tests/test_exclusions.py` → **Ran 16 tests · OK**, "실제 registry md5 전/후 동일: True (3c4c8232)". `python3 -m py_compile scripts/exclusions.py tests/test_exclusions.py` 통과. `-W error::ResourceWarning`에서도 OK.
- `propose /home/claude/work/combined --day 2026-09-26`(합본 09-27 갱신 회차 것): 신규 후보 **0** · 업종어 포함 **3** · 재등록 후보 **33** · 재노출 판정 **15건**(그중 "등록돼 있는데도 노출" **0**, 노원구어린이 = "등록 당일(판정 안 함)") · 후보에서 뺀 것 **5**(운동 계열·경쟁사) · 승인 문구 건수 33(3절 최종 판정의 33개와 동일). `--since 2026-09-21`: 등록 누락 33 · 등록 당일 3 · 등록 전 노출 32 · 등록돼 있는데도 노출 0.
- `push --approved <33개 후보 파일> --dry-run`: `HTTP 호출 0 · registry 변경 0`, 그룹 3개(ID 매핑 전이라 registry 그룹명 기준) 각 "등록 예정 33 · registry에 이미 등록 0"; 전후 `audit/exclusions.csv` md5 3c4c8232 동일.
- `report`: 340행, 미등록·누락 이름 33개 목록 출력. `--help`·다른 cwd에서 실행(ROOT 기준 경로) 정상.
- 하지 않은 것(환경·권한상 불가, 검증·첫 실사용 몫): 실제 `pull`(키 없음·차단) · `test-roundtrip` 실제 1건 · `push` 실제.

### 검증 회차가 재현할 것 (브랜치 clone에서, 토큰·API 키 없음)

1. `python3 tests/test_exclusions.py` → 16 OK, 실제 registry md5 전/후 동일 출력. 문법: `py_compile` 2파일, `config/report-config.json` `json.load` 통과·`exclusions` 키 10개.
2. **dry-run 무변경**: `python3 scripts/exclusions.py propose <합본> --day 2026-09-26 --out work/p.md` → `work/p_candidates.txt` 33줄 → `push --approved work/p_candidates.txt --dry-run` → 출력에 `HTTP 호출 0 · registry 변경 0`, 전후 `audit/exclusions.csv` 행수 341·md5 3c4c8232 동일, `work/` 밖 파일 변경 0(`git status`).
3. **금지 패턴 차단**: 승인 파일에 `노원역운동`·`근처산전필라테스`·경쟁사 이름 하나를 넣고 `push --dry-run` → 각각 `[거부] … 금지 패턴/경쟁사명`, 승인 건수에서 빠짐. `propose` 출력 "후보에서 뺀 것"에 운동 계열이 이유와 함께 있는지.
4. **확인 실패 경로**: `tests/test_exclusions.py`의 `test_verified_false_is_failure`(FakeSender `drop_after_post=True` — POST는 성공 응답인데 다시 읽으면 없음)가 push 쪽 `failed`와 roundtrip 쪽 `verified:false` 예외를 둘 다 확인하는지 — 코드로도 `do_verify`가 없는 이름을 `failed`로 쓰는 줄(`확인 실패: 목록에 없음`)과 `do_test_roundtrip`의 `verified:false` 줄을 인용.
5. **시험 1건**(사용자 입회, PC, 키 재발급 뒤 — 검증 세션은 명령·순서만 확인): `test-roundtrip --keyword saero제외테스트<날짜> --group <adgroup_id> --key-file <keys> --confirm` → 출력 `[test] 등록 성공 id=…` → `다시 읽어 확인: 있음(verified)` → `삭제 뒤 확인: 없음 — 원상복구` → `PASS`, registry에 `deleted` 1행. `--confirm` 없이는 SystemExit. `--dry-run`은 호출 0.
6. 재노출 판정 재현: `propose --since 2026-09-21` → 등록돼 있는데도 노출 **0** · 등록 누락 **33** · 등록 당일 **3** · 등록 전 노출 **32**(숫자는 세어서). 노원구어린이(9/26 노출)가 "등록 당일"인지(임의 결정 7).
7. 네트워크 차단 경로: 이 컨테이너에서 `pull --key-file <아무 JSON>` → `[FAIL] 네트워크 차단(프록시)…` exit 2, registry 불변(md5).
8. 문서 = 코드: SKILL.md 5-0단계 6항목 ↔ exclusion-ui.md 6~9절 ↔ `build_proposal`·`reexposure_judgement`·`cmd_push`(클릭>0 제외·첫 등장·industry_terms·거부·verify) 한 줄씩. checklist v4.5 줄·[의도된 동작] 18~20·표 6행·[검증 회차] C 존재. 옛 문구 grep: `탭 목록 확인 요청`이 현행 지시(SKILL.md·references·checklist·대조 목록 머리말)에 남아 있지 않은지(역사 행·탐색 기준선 인용은 남는 게 정상).
9. 지시 밖 변경 0: `git diff 11c0bc2 --stat`가 위 표의 파일만. `data/`·`scripts/compute.py`·`validate.py`·배포본 불변.

### 원래 제안·지시를 바꾼 곳 (B 검증이 볼 것)

- 설계안 config 키 이름·구조(낱개 키 → `exclusions` 블록, 그룹명 미기재) — 임의 결정 2. `industry_terms`·클릭>0 제외 규칙 신설 — 임의 결정 4·5. 부분 실패 "1회 재시도" → 재시도 없음(사용자 결정) — 임의 결정 10.
- 4-C 설계는 "Claude가 pull 파일을 읽어 판정"이었는데, 구현은 pull/verify가 **registry를 직접 갱신**하고 Claude는 registry·스냅샷을 읽는다(사람 명령 수는 같고 기록이 한 곳).
- 탐색 기준선 4-A의 `--read-only` 플래그는 만들지 않았다 — 쓰기 명령(push·delete·test-roundtrip)이 각각 `--dry-run`·`--confirm`을 가지므로 별도 모드가 필요 없다고 봤다(검증·진단 회차는 propose·report·`--dry-run`만 쓴다 — SKILL.md 5-0단계 6).

### 수정 기록 2 (2026-09-27, 검증 회차 판단 요청 4건 + 참고 2건 처리 — 같은 브랜치 `feat-exclusions`, main 미반영)

검증 회차(별도 세션, `saero-ad-report_검증_2026-09-27.md` 143행, 대상 a615a84): 기준값 10항목·시험 16·재현 ①~⑨ 전부 재현. 판단 요청 4건·참고 2건은 조정(이 세션)이 브랜치 코드에서 실물 확인한 뒤
사용자 지시("고쳐")로 **전부 고쳤다**. 네이버 계정 쓰기 0 · main 0 · 배포 0. 검증 2는 검증 세션에 이어서(아래 재현 목록).

| # | 검증 지적 | 분류 | 처리(절·함수명) |
|---|---|---|---|
| 판단 1 | registry 파일이 없으면 조용히 `[]`로 진행 → 이력 있는 이름이 신규 후보(실측 10개) — 문서의 "미확인" 경로가 코드에 없음 | 코드 결함(안전장치) | `load_registry(path, create_ok=False)`: 파일 없음·못 읽음·열 다름 → `RegistryUnavailable`(69~88행) → `main`이 `[FAIL] registry 없음 … 판정할 수 없어(미확인) 멈춥니다` exit 1(870행). `pull`·`import-ui`만 `create_ok=True`. 이름이 registry에 없는 경우의 판정 문구는 "미확인(등록 이력 없음)" → **"이력 없음(registry에 없는 이름)"**으로 바꿔 문서의 "미확인"과 구분. 문서: SKILL 5-0 1항·references 6절·3절·checklist 표 |
| 판단 2 | `failed` 이름이 재노출 없으면 다음 propose·report에서 사라짐(설계 "다음 후보로 되돌린다" 미구현·미기록) | 코드 결함(설계 위배) | `build_proposal` 재등록 후보 집합에 `failed` 포함(529행), `failure_note()`(452행)로 직전 실패 사유를 `rereg` 3번째 값·제안서 "**직전 실패**: …"에 표시. `cmd_report` 목록에 failed 포함 + "그중 등록·확인 실패 n개" 줄(847행~). 빼는 방법 = registry `status=keep`(문서화: references 5·7절, SKILL 5-0 1항) |
| 판단 3 | 승인 문구 "이미 등록 m"이 keep만 셈 | 경미(라벨≠값) | `n_registered`(창 안 status=registered 이름 수, 499·508행) → 문구 `이미 등록 {n_registered} · 노출 유지(사용자 결정) {len(already)}`(544행), 반환값에 `n_registered` 추가. 실측 `--day 2026-09-26` → 이미 등록 1(노원구어린이), `--since 2026-09-21` → 35(검증 보고의 32+3과 같음). references 6절 문구 갱신 |
| 판단 4 | "남은 용량 보고" 코드 없음(문서 > 코드) | 경미(문서>코드) | config `exclusions.max_per_group: 950`(UI 카운터 추정, `_comment`에 명시) 신설. `do_push`가 그룹별 `현재 N + 등록 예정 M = 합 (한도 추정 950)`을 찍고 초과 예상이면 `[주의]`만(628행~, 차단 안 함 — 3716은 항목별 failed·재승인). `dry_run_plan` 4번째 값 = 현재 registry 등록 수 → dry-run 출력 `현재 registry 등록 n → 등록 후 합/950(추정)`(712행~). references 2·7절 문구를 코드에 맞춤("남은 용량 계산 안 함") |
| 참고 1 | 스냅샷 json은 pull만 씀(문서는 pull·push·verify) | 문서≠코드 | `write_snapshot()`(320행) 분리, `do_pull(snapshot=)`·`do_push(snapshot=)`·`do_verify(snapshot=)` — `cmd_pull`·`cmd_push`(verify 단계)·`cmd_verify`가 True. 문서 = 코드 |
| 참고 2 | `delete`에 `--confirm` 없음(test-roundtrip과 비대칭) | 안전장치 | `cmd_delete`: `--dry-run`이 아니면 `--confirm` 필수(769행), 인자 추가. references 3·7절·SKILL 5-0 4항에 명시 |
| 참고 3~8 | 판정 우선순위·일치 행 제외·업종어 묶음 크기·차단 시 재저장 바이트 동일·역사 행·BrokenPipe | 결함 아님 | 변경 없음 |

검증 8절 "`--read-only` 미구현(의도의 절반)": 유지 — 쓰기 명령 3개가 이제 전부 `--confirm`(delete·test-roundtrip) 또는 승인 파일(push) + `--dry-run`을 가지므로 별도 모드는 만들지 않았다(임의 결정 16). 다른 임의 결정은 그대로.

변경 파일(수정 회차 2, 행수 `wc -l` · md5 앞 8자리): `scripts/exclusions.py` 828→**876** · 2122fffa / `tests/test_exclusions.py` 326→**424** · a8783b5d(시험 16→**20**: registry 없음 exit 1·pull은 생성·형식 다름, failed 후보 복귀·사유·keep·report, 용량 로그·경고·차단 없음, delete `--confirm`·verify 스냅샷) /
`config/report-config.json` 82→**83** · b6f1b99c(`max_per_group` 1키 + `_comment` 한 문장, 다른 키 불변) / `references/exclusion-ui.md` 114→**123** · 1cc571ac / `SKILL.md` 469→**472** · 9c618593 / `audit/checklist.md` 459→**463** · 931d9d51(v4.5 갱신 이력 1줄 + 표 3행) /
`audit/exclusions.csv` **341 · 3c4c8232 불변** / `.gitignore` 불변 / 이 파일(커밋 뒤 보고).

실측(이 세션): `python3 tests/test_exclusions.py` → **Ran 20 tests · OK**, registry md5 전/후 3c4c8232 · `py_compile` 2파일 통과 · `propose --day 2026-09-26` → 신규 0·업종어 3·재등록 33·재노출 15(등록돼 있는데도 노출 0)·뺀 것 5·**이미 등록 1 · 노출 유지 0** · `--since 2026-09-21` → 재등록 33·재노출 68·**이미 등록 35** ·
`push --dry-run`(33개) → `HTTP 호출 0 · registry 변경 0`, 그룹별 `현재 registry 등록 36/135/14 → 등록 후 69/168/47/950(추정)`, md5 불변 · `--registry <없는 경로> propose` → `[FAIL] registry 없음 … (미확인)` **exit 1**, 제안 파일 생성 0 · `report` → "미등록·누락·실패 이름 33개"(failed 0이라 실패 줄 없음).

**검증 2가 재현할 것(검증 세션에 이어서, 브랜치 최신 해시 기준, 토큰·키 없음)**
1. 기준값: 위 행수·md5·시험 20 · `git diff a615a84 --stat` = 6파일(exclusions.py·test_exclusions.py·config·references·SKILL·checklist) + last-audit.md.
2. 판단 1: `--registry <없는 경로>`로 `propose`·`push --dry-run`·`report`·`verify`·`delete --confirm`·`test-roundtrip --confirm` → 전부 `[FAIL] registry 없음 … (미확인)` exit 1, 파일 생성 0; 열이 다른 CSV도 `[FAIL] registry 형식이 다름`. 가짜 API 시험 `test_missing_registry_stops_judging_commands_but_pull_creates`에서 pull만 생성.
3. 판단 2: registry 사본에 `failed` 행(note에 사유) 추가 → `propose` 재등록 후보에 `— **직전 실패**: <사유>`로 오르고 `_candidates.txt`에 포함, `report`에 "그중 등록·확인 실패 n개" 줄; `status=keep`으로 바꾸면 사라짐(`test_failed_names_come_back_as_candidates_with_reason`).
4. 판단 3: `propose --day 2026-09-26` 승인 문구 `이미 등록 1 · 노출 유지(사용자 결정) 0`, `--since 2026-09-21` → `이미 등록 35`.
5. 판단 4: `push --dry-run` 출력의 `현재 registry 등록 n → 등록 후 합/950(추정)`; 가짜 API 시험 `test_push_logs_capacity_and_warns_over_limit`(한도 4에 3+2 → `[주의] 초과 예상`, 등록은 진행).
6. 참고 1·2: `delete … --key-file <keys>`(confirm 없음) → SystemExit `--confirm 이 필요합니다`, `--dry-run`은 exit 0 호출 0; `verify`가 `work/exclusions_pull_<날짜>.json`을 쓰는지(`test_delete_requires_confirm_and_verify_writes_snapshot`).
7. 회귀: 1차 재현 ①~⑨(구현 기록)가 그대로 — 특히 ② dry-run 무변경·③ 거부·④ verified:false·⑦ 차단 exit 2. 옛 문구 grep: "미확인(등록 이력 없음)" 0건(코드·시험), "남은 용량을 보고" 0건(references).

### 다음에 볼 것 (검증 통과 → 병합 → 첫 실사용, 순서대로)

1. **API 비밀키 재발급**(09-27 채팅에 키가 보이는 화면이 올라왔음) → PC에 `naver-api.keys.json`(저장소 밖). 2. PC에서 `pull` → 출력의 그룹명 3개·`userLock`·`useAdvoost`·`[주의]` 줄 확인, registry `group_id` 채워졌는지·`*` 행 정리·`missing` 발생 여부(있으면 그 이름들이 진짜 없는지 UI로 한 번) → 이 결과가 **2-3절 요청 3(ID↔그룹명)의 답**. 3. `test-roundtrip` 1건 입회. 4. 첫 자동 회차: `propose` → 승인 문구 → 사용자 답 → PC `push`(33개 안팎) → 대조 목록 표에 요약 행 → 다음 날부터 재노출 판정. 5. 첫 실사용 결과를 이 파일 "첫 실사용 기록"에.


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
| E2 | **기계 자리 자동 교체** — 배포본에서 행 수가 고정인 자리(KPI 4+sub 3, 01 표 5행, 03 표 31행+합계, 04 표 5행, 06 매칭표·카드 숫자, 09·10 표, 차트 data 배열 12개, labels 2개, min-width 2개, 08·09 각주 숫자, masthead·og)를 compute.py JSON으로 치환하는 `scripts/patch.py`. **행 수가 변하는 구간(07 정식표·클릭1건·클릭0·경쟁사표, 08 TOP10·컴팩트)과 문장(section-desc·note·11·12)은 사람이 쓴다** | SKILL.md 13~15 `**리포트 HTML을 새로 만들지 말 것.** … "숫자와 문구만" 교체한다` | 배포본 기계 자리: `td.num` 셀 509개(03번 224·07번 170·04번 35·01·08번 각 30)·data 배열 12·labels 8·min-width 5 vs 문장 블록 40개(note 본문 9,181자). 행 고정 자리만 세면 약 330셀 + 배열·라벨·폭 | 갱신 회차의 str_replace/sed 반복을 스크립트 1회로(추정 −10회 이상 [추론]). 원칙과의 경계: 기계 자리만 치환하면 레이아웃·CSS·순서·문장 불변이라 원칙 준수 | 치환 위치를 잘못 잡으면 표가 어긋남 → 치환 후 validate 14 PASS + compare.py 차이 0을 필수로. 07·08 가변 구간은 범위 밖 명시 |
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

# 점검 기준선
점검일: 2026-09-07 (저녁 회차, Fable) — 진단 후 사용자 선택으로 D-7·D-8·D-9 + I-6 수정, 개정안 ①~④ 반영. 검증은 별도 세션에서 받을 것
결함 3건(D-7·D-8·D-9, 전부 조치완료 — 검증 미실시) / 개선안 이월 4건(I-7~I-10) / 인용불가로 제외 0건
직전 기준선(2026-09-07 오후, 커밋 e83993f) 대비: 해결·유지 9건, 부분 유지 2건(I-3→D-7, I-4→D-9), 미해결 1건(검색어 CSV 참고 출력), 보류 2건(같은 CSV라 판정 불가), 근거없음 0건, 신규 결함 3건

점검 대상(전부 저장소에서 받은 것): `saero-ad-report-skill` @cb95494 — SKILL.md(312행) · README.md(2) ·
references/report-structure.md(291) · references/css-and-layout.md(184) · scripts/validate.py(347) ·
config/report-config.json(22) · audit/checklist.md(360, v4.1) · audit/last-audit.md(325) · .gitignore(2) /
`saero-pilates-report` @474966e index.html(1707행, 집계 2026.08.26—09.06 12일) · service-worker.js(46) —
직전 회차와 동일 커밋 / 라이브 Pages: web_fetch 수신했으나 캐시로 판정(아래) / 설치본 부트스트랩은 재업로드 언급 없어 건너뜀.
**실 CSV 4종 있음**: 필라테스_보고서(=키워드) · 검색어 · 상세지역 · 시간대별 (계정 2580077). 기간헤더 2026.08.08~09.06,
실 `일별` 2026.08.26~09.06(12일) — **직전 회차와 같은 CSV**라 CSV 실측 항목은 결과가 그대로 재현됨. 리포트 갱신에 쓰지 않음.

## 이번 회차 조치 (2026-09-07 저녁 후속, 같은 세션) — 스킬 저장소만. 배포본 변경 없음

config/report-config.json은 작업 전 백업(md5 a648e4423cdd33e944ae3c41a32d2177), 실험 후 원복, md5 대조 OK. **설정 변경 없음.**

- **D-8 조치완료** — validate.py **4곳 변경, 그중 f-string 3곳 + docstring 1곳**. f-string 3곳은 검사 이름(현재 322·331·339행)을 `f"… {CTR_HIGH:g}% 이상에만 …"`으로. 나머지 1곳(현재 131행 `check_ctr_rule` docstring)은 보간이 아니라 `클릭률 CTR_HIGH 이상에만 .ctr-high`로 **변수명을 글자로 적은 것**이다. 하드코딩된 `4%`는 validate.py에 0건이라 동작에는 문제 없음. *(2026-09-09 정정: 원래 "검사 이름 4곳을 f-string으로"라고 적혀 있었다.)*
  실측: `ctr_high_threshold` 5.0으로 바꿔 실행 → `[FAIL] 07번 클릭률 5% 이상에만 .ctr-high — … 불일치 4건` / `01번 클릭률 5% 이상에만 … 불일치 1건: 4.63%`. 라벨이 판정값과 일치. 원복 후 4%로 PASS.
- **D-9 + I-6 조치완료** — `check_chart_width`가 config `chart_min_width.date_based_sections`를 순회해 섹션마다 검사 1개(`01번 차트 min-width`, `06번 차트 min-width`). 새 함수 `check_date_labels`: `'M/D(요일)'` 항목만으로 된 `labels:[…]` 배열(01·06번 스크립트, index.html 1313·1511행)을 html 전체에서 찾아 길이 = 일수. 0건 가드 둘 다 포함. validate.py docstring 8·22–27행, SKILL.md 검산 목록·"매번 함께 바꿔야 할 텍스트" 3·4번·자동/수동 항목 문구(옛 296–298행)를 코드에 맞춤.
  **검사 개수: 12 → 14** (실행 출력 [PASS] 줄 세어 14. `date_based_sections=[1]`이면 13, `[1,6,9]`면 15 — 설정 따라 늘고 준다는 것 실측).
  요구된 실측 4종: ① 배포본 675행 960 = 12×80 → `[PASS] 06번 차트 min-width … 화면 [960] / 기대 960px` ② 675행 900 → `[FAIL] 06번 … 화면 [900] / 기대 960px` ③ 01번 263행 900 → 종전대로 `[FAIL] 01번 …` (완화 없음) ④ `date_based_sections`에서 6 제거 → 출력에 `06번 차트` 줄 없음, 13개 PASS.
  새 필드 추가 없음 — 기존에 코드 소비자가 없던 `date_based_sections`를 쓰기 시작한 것이고, validate.py docstring·SKILL.md·css-and-layout.md 174행이 이미 그 필드를 설명한다.
- **D-7 조치완료** — 항목별 판단(값 정의 자리 → config 참조 / 설명 자리 → 이름 + config 한 줄):
  · SKILL.md 41–47행 선언: "값을 다시 적지 않는다"를 "정의 자리는 키를 가리키고, 설명 자리는 이름을 두되 키를 붙인다"로 현실화 — 본문에 이름이 전혀 없을 수는 없어서.
  · 옛 156–157행 경쟁사 목록: **정의 자리(판정 기준)** → 값 삭제, `competitors` 참조. 이로써 (b) 경로 종결 — (1-1) 표 아래에 "이 문서에는 목록이 없어 갱신할 곳 없음, 예전엔 있어서 노원M 누락이 났다"고 이유 명기.
  · 옛 205–209행 제외그룹·키워드 10개: 그룹 이름 `노원필라테스(삭제)`는 **설명 자리**("삭제"가 왜 OFF인지)라 이름 유지 + `excluded_groups` 참조 한 줄. 키워드 10개 열거는 **정의 자리** → 삭제, `excluded_group_keywords` 참조. 223행 "위 목록에 없는" → "`excluded_groups`에 없는".
  · 옛 236행 타겟 지역: **정의 자리(계산 규칙)** → `target_districts` 참조(현재 5개 자치구).
  · 사용자 지시문의 "230행(타겟 지역)"은 진단 시점 236행이었다(같은 줄). 개업일(74·78·83–87행)은 설명 자리라 그대로(45–47행 규칙 적용).
  · references/report-structure.md 63행 `{날짜수×80}px. 최소 650px`·198행 `클릭률 4% 이상`·css-and-layout.md 22–23·44행 `4%`는 이번 지시 범위(SKILL.md 세 곳) 밖이라 손대지 않음 — 다음 회차 판단.
- **파괴 실험 전부 재실행(검사 조건 변경 원칙)**: 14개 검사 각 1곳씩 → 14/14 FAIL, **0건 가드 8종** FAIL(masthead·KPI·04 td·각주·**01 min-width·06 min-width**·07 name-cell·날짜형 라벨 배열 형식 변조). 완화된 검사 없음.
  *(2026-09-09 정정: 원래 "7종"에 **06번 min-width 가드**가 빠져 있었다. 가드는 `tests/mutation_test.py` 182–193행에서 고정 6종 + `date_secs` 순회 2종 = 8종이고 실행 출력도 8줄이다. 같은 파일 "점검표 갱신 이력" 절의 v4.3 기록은 처음부터 "8종"이라 한 파일 안에서 7 대 8로 갈려 있었다 — 이제 두 곳 다 8종.)*
  **교훈: `date_based_sections`에 섹션을 추가하면(D-9의 06번처럼) 그 섹션의 0건 가드도 같은 회차에 가드 목록에 넣어라.** 검사만 늘리고 가드 목록을 안 고치면 다음 회차 기록이 실제보다 적게 남는다.
  *(2026-09-09 정정: 원래 "스크립트 `mutation-test.py` 산출물로 첨부"라고 적혀 있었으나 두 가지가 틀렸다. 파일명은 하이픈이 아니라 밑줄이고 경로는 `tests/mutation_test.py`다. 그리고 이 회차 커밋 3cc21b6에는 `tests/`가 아예 없었다 — 스크립트는 다음 커밋 **dfc6a94**에서 처음 들어왔다.)*
- 배포본 index.html: 변경 없음(현재 960=12×80으로 새 검사 PASS). 다음 갱신(13일치)부터 01·06 모두 1040으로 바꿔야 PASS.

## 기록 문구 정정 (2026-09-09, 검증 회차 후속) — 이 파일만 변경

2026-09-08 수정분(D-7·D-8·D-9+I-6, 커밋 3cc21b6·dfc6a94)을 별도 세션에서 검증한 결과,
**코드·config·배포본은 전부 기록대로 동작했고 어긋난 것은 이 파일의 문구 3건뿐**이었다.
아래 3건을 위 "이번 회차 조치" 절에서 제자리 정정했다. 코드는 손대지 않았다.

| # | 위치 | 틀린 문구 | 실제 | 확인 방법 |
|---|---|---|---|---|
| 1 | "파괴 실험 전부 재실행" 줄 | `0건 가드 7종`(목록에 06번 min-width 없음) | **8종** — `tests/mutation_test.py` 182–193행 고정 6종 + `date_secs` 순회 2종, 실행 출력 8줄 | 스크립트 실행 출력 세기 |
| 2 | 같은 줄 | `스크립트 mutation-test.py 산출물로 첨부` | 경로는 `tests/mutation_test.py`(밑줄). 3cc21b6에는 `tests/` 없음 → 다음 커밋 **dfc6a94**에서 처음 들어옴 | `git show --stat 3cc21b6` |
| 3 | D-8 줄 | `검사 이름 4곳을 f-string으로` | **4곳 변경, f-string 3곳(322·331·339행) + docstring 1곳(131행, 보간 아님)** | `git show 3cc21b6 -- scripts/validate.py` |

**세 건 다 "코드는 정상, 기록 문구만 틀림" 유형이다.** 이 유형이 위험한 이유:
다음 회차는 코드가 아니라 이 기록을 기준으로 대조하므로, 문구가 틀린 채 남아 있으면
**실제로는 멀쩡한 코드를 결함으로 올리거나(가드 8종을 7종 기준으로 보면 "가드가 하나 늘었다"),
없는 파일을 찾다가 시간을 쓴다(`mutation-test.py`).** 기록 숫자·경로·범위는 코드에서
확인하고 적을 것 — checklist.md `[판정 기준]`의 "개수를 적을 때는 세어서 적어라",
"기록 문구는 방향·범위·개수를 코드에서 확인하고 적어라"가 정확히 이 항목이다.

검증 회차 실측(재현 확인, 이 파일에 기록만): 실 CSV 13일치(2026.08.26~09.07)로 돌리니
01·06 min-width가 `기대 1040px (13일)`로 FAIL — 날짜 수를 따라 늘어남 확인. masthead도
`화면 (12일) vs CSV (13일)` FAIL로 실제 작동. `date_based_sections` `[1]`→13개·`[1,6]`→14개·
`[1,6,9]`→15개 재현. config 삭제 → 검사 시작 전 exit 1, `excluded_groups` 비우기 → KPI
노출 4,912→4,918 재현. `mutation_test.py`는 원본 md5 불변(별도 `md5sum -c`로도 확인).

checklist.md는 변경 없음 — 가드 개수를 적어두지 않았고 스크립트 경로 4곳(10·84·176·180행)이
전부 `tests/mutation_test.py`로 옳게 적혀 있어 고칠 문구가 없었다.

## 직전 기준선 판정
| 항목 | 판정 | 근거(지금 원문) |
|---|---|---|
| D-3 시간대별 `일별` 없음 | 해결 유지 | SKILL.md 77–78행 `` `일별` 컬럼이 있는 3개 CSV(키워드·검색어·상세지역)의 `일별` 최솟값이 `` |
| D-4 검사 3 비교 대상 | 해결 유지 | validate.py 293행 `hourly_clicks == all_clicks,` / 실 CSV 출력 `시간대별 CSV 110 vs 전체 110 (KPI 110)` |
| D-5 검산 목록 01번 | 해결 유지 | SKILL.md 284행 `- 01번 일별 표의 클릭률 셀도 같은 규칙으로 전수 대조` |
| D-6 OFF 그룹 키워드 표시 | 해결 유지 | SKILL.md 211–212행 `키워드 보고서 CSV에는 노출이 0인 키워드는 행이 생기지 않는다. 그래서` / 실 CSV에 `노원필라테스(삭제)` 행 존재(노출 6·클릭 0) |
| I-1 2-1단계 선확인 | 해결 유지 | SKILL.md 89행 `### 2-1단계. 배포본이 이미 최신인지 먼저 확인 — 계산 전에 멈춘다`. 실 갱신 회차가 아니어서 "실제로 멈추는지"는 미실측 |
| I-2 승인 기록 3곳 | 해결 유지 | SKILL.md 169행 `**(1-1) 승인·제외 결과를 남기는 곳 — 반드시 세 곳 다**` |
| I-3 설정 단일 출처 | **부분 유지 → D-7** | config/report-config.json 존재, validate.py 57–60행이 읽음(`ctr_high_threshold` 5.0으로 바꾸면 01·07 검사 결과가 바뀜 — 실측). 그러나 SKILL.md에 값 사본이 남아 있음(D-7) |
| I-4 validate 12개 | **부분 유지 → D-9** | 검사 12개 실 CSV PASS·전부 파괴 FAIL(아래 표). 단 기준선 118행이 조치완료라 적은 `01·06번 min-width 검사` 중 06번은 코드에 없음 |
| I-5 토큰 두 종류 | 해결 유지 | SKILL.md 28행 `**토큰은 용도에 따라 두 종류다. 서로 통하지 않는다.**` + 30–33행 표 |
| 개정안 11 06번 규칙 | 해결 유지(문서) | css-and-layout.md 175행 `06번 `rankChart`도 x축이 날짜라 같은 규칙의 대상이다(12일 기준 960px).` — 문서만. 검사는 없음(D-9) |
| 라이브 1287행 문구 | 종결 유지 | web_fetch는 이번에도 `07번 표에서`를 돌려줬으나 캐시 확정(아래). 결함으로 재상정하지 않음 |
| 검색어 CSV 클릭합 참고 출력 | 미해결(이월 개선안) | validate.py 332–334행 `if sr_clicks != kpi_clicks:` → `print(f"\n참고: …")` — FAIL 아님, exit 0 |
| 노원M필라테스 자연소멸 판단 | 보류 | 같은 CSV(노원M 2회 + 변형 2회 = 4회·클릭 0). 새 주 데이터 없어 판정 불가 |
| 제외그룹 노출 지속 | 변화 없음 | 같은 CSV. `노원필라테스(삭제)` 노출 6(8/26 5·8/31 1)·클릭 0. 최근 3일 노출 [0,0,0] |

## 결함 (진단 시점 기록 — 전부 위 "이번 회차 조치"로 조치완료)
| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 실측/추론 | 왜 틀렸는지 | 수정 방향 | 작업경로 |
|---|---|---|---|---|---|---|---|---|
| D-7 | 중 | SKILL.md ↔ config/report-config.json | 42–43 ↔ 156–157 · 205–209 · 236 ↔ config 2 | SKILL.md 42–43 `**이 문서나 references, validate.py에 값을 다시 적지 않는다.** 값이 바뀌면 그 파일만 고친다.` vs 156 `이미 확인된 경쟁사 목록: 젠필라테스 · 이레필라테스 · 오운필라테스 ·` / 205 `- `노원필라테스(삭제)` — CSV 표기는 "삭제"지만` / 208–209 키워드 10개 열거 / 236 `- 타겟 지역 = 노원·도봉·강북·중랑·성북구 5개 자치구` / config 2 `SKILL.md·references·validate.py는 값을 여기서만 읽는다` | 추론(다음 경쟁사 승인 때 발생. 이번 CSV엔 새 후보 없어 조건을 못 만듦) | 문서가 스스로 세운 규칙을 같은 문서 안에서 어기고 있다. 45–46행 "예시" 면책은 개업일에 붙어 있고, 156행은 "이미 확인된 목록"이라는 판정 기준으로 읽힌다. (1-1) 표 174–178행은 승인 시 config·audit·화면 3곳만 갱신하라고 하므로 다음 승인에서 156행이 그대로 남아 config와 어긋난다 — D-1(노원M 누락)이 났던 경로 그대로 | (a) 156–157·205–209·236행을 값 없이 config 키 참조로 바꾸기(`config의 competitors 참고`) 또는 (b) 42–43행 규칙을 "코드(validate.py)만 config를 읽고 문서는 사본을 둔다, 승인 시 SKILL.md 156행도 갱신"으로 낮추고 (1-1) 표에 SKILL.md 행 추가. 선택은 사용자 | saero-ad-report-skill push |
| D-8 | 하 | scripts/validate.py | 126 · 299 · 308 · 316 | `"""클릭률 4% 이상에만 .ctr-high. …"""` / `check("07번 클릭률 4% 이상에만 .ctr-high", False,` / `"07번 클릭률 4% 이상에만 .ctr-high",` / `check_ctr_rule("01번 클릭률 4% 이상에만 .ctr-high",` | **실측** — config `ctr_high_threshold`를 5.0으로 바꿔 실행 → `[FAIL] 07번 클릭률 4% 이상에만 .ctr-high — 11행 검사, 불일치 4건: 필라테스(4.71%, 강조=있음)…` 라벨은 4%라고 말하면서 5% 기준으로 판정 | 판정값은 config에서 읽는데(58행 `CTR_HIGH = float(CFG["ctr_high_threshold"])`) 출력 문구는 하드코딩. 기준을 바꾸면 검사 이름이 거짓말을 한다. 223행 `"01번 차트 min-width = 날짜수x{}px".format(PER_DAY_PX)`처럼 이미 변수로 쓰는 곳도 있어 일관성도 깨짐 | 네 곳을 `f"… {CTR_HIGH:g}% 이상에만 …"`으로 | saero-ad-report-skill push |
| D-9 | 중 | scripts/validate.py · SKILL.md · audit/last-audit.md(직전) · config | validate 216–224 · SKILL 288 · 296–298 · 기준선 112 · 118 · config 20 | validate.py 217 `s1 = section(html, 1, 2)` (06번 미검사) / SKILL.md 288 `- 01번 차트 `min-width` = 날짜 수 × 설정값(기본 80px, 최소 650px)` / 296 `위 목록 중 "매번 함께 바꿔야 할 텍스트" 1·3·8·9번은 이제 자동 검사 대상이다.` / 297–298 `남은 수동 항목은 2(og:description) · 4(06번 x축 라벨) · 5(09번 심야 콜아웃) · 6(11번 날짜 문장) · 7(01번 인사이트 박스)뿐이다.` / 직전 기준선 112 `## 개선안 (최대 5 — 2026-09-07 저녁 전부 조치완료)` · 118 `**01·06번 min-width = 일수×80 검사(개정안 11)**` / config 20 `"date_based_sections": [1, 6]` | **실측** — 배포본 675행 `height:240px; min-width:960px;`(06번)을 900으로 바꿔 실행 → 12개 전부 PASS, exit 0. validate.py에 `date_based_sections` 참조 0건(grep), `labels`/`라벨` 참조는 180행 KPI 라벨 1건뿐 → x축 라벨도 미검사 | 세 가지가 한 덩어리다. ① 06번 min-width는 css-and-layout 175행·config 20행이 대상이라 하지만 검사도 없고 SKILL.md 264–272 수동 목록에도 없다 — 어느 목록에도 없는 갱신 항목. ② 296행 "3번 자동 검사"는 3번의 절반(x축 라벨)이 미검사라 과대 진술. ③ 직전 기준선은 06번 검사를 조치완료로 기록 → 다음 회차가 이를 기준으로 판정하게 된다(점검표 "기록 문구 정확성" 항목 해당) | validate.py `check_chart_width`가 `CFG["chart_min_width"]["date_based_sections"]`를 순회(01·06) + 01·06 차트 `labels:[…]` 개수 = 일수 검사 추가 → SKILL.md 288·296–298 문구를 코드에 맞춤 → 기준선 118행 정정. 코드를 안 고칠 거면 SKILL.md 264–272 목록에 "06번 min-width" 추가 + 296행 정정만 | saero-ad-report-skill push (배포본은 현재 960=12×80으로 맞아 수정 불필요) |

## 이번 회차 실측 요약
- validate.py 실 CSV + 배포본: **12개 검사 전부 PASS, exit 0** (세어서 12). 검색어 CSV 클릭합 110 = KPI → 참고 출력 없음.
- **파괴 실험 12/12 FAIL + 0건 가드 6종 FAIL** (스크립트 `mut/run.py`로 한 곳씩 변조):

| 조작 | 결과 |
|---|---|
| `</div>` 1개 제거 | FAIL `div 175/174` |
| 07 정식표 클릭 28→27 | FAIL `= 109 (KPI 110)` |
| 시간대별 CSV 첫 행 클릭 −1 | FAIL `109 vs 전체 110` |
| 07 4.71% 행 `.ctr-high` 제거 | FAIL `불일치 1건: 필라테스(4.71%` |
| 01 5.22% 셀 `.ctr-high` 제거 | FAIL `불일치 1건: 5.22%` |
| masthead 12일→11일 | FAIL |
| KPI 타일 4,912→4,913 | FAIL |
| 04번 91.7→91.6 (합 99.9) | FAIL |
| 01번 263행 min-width 960→900 | FAIL `화면 [900] / 기대 960px` |
| **06번 675행 min-width 960→900** | **PASS (exit 0) — D-9** |
| Section 5 주석 변조 | FAIL `누락 [5]` |
| 08번 각주 6회→5회 | FAIL |
| 상세지역 CSV 첫 행 노출 +1 | FAIL `4,919 vs 4,918` |
| 0건 유도: masthead 문구 / KPI `label` 클래스 / 04번 `td.num` / 각주 문구 / 01 min-width 제거 / 07 `name-cell` | 전부 FAIL(마크업 변경 의심 또는 합계 불일치) |

- **config가 실제로 읽히는지**: `ctr_high_threshold` 4.0→5.0으로 01·07 검사가 FAIL로 바뀜(D-8 근거). `excluded_groups` 비우기는 직전 회차 실측(4,912→4,918) 그대로.
- 제외그룹 자동감지 규칙(SKILL.md 222–223) 실 CSV 적용: 조건 해당 그룹은 `노원필라테스(삭제)`(노출 비중 0.12%·클릭 0·최근 3일 [0,0,0])만. 신규 후보 없음. 나머지 5그룹 최근 3일 노출 전부 >0.
- 경쟁사: SKILL.md 156–157·config 11–14 목록 7개 = 배포본 07번 경쟁사표 8행(퍼스트필라테스아카데미노원은 표기 변형). 검색어 CSV에서 판정 이력 밖의 새 브랜드명 패턴 없음(상위 40개 검토 — 전부 지역·일반어).
- `.ctr-high` 사용처: index.html 123(정의)·302·329(01번)·782·791·800·809·845·863·872(07번) — 다른 지표 재사용 없음.
- `.gitignore` 있음(`__pycache__/`, `*.pyc`), `git ls-files | grep pyc` 0건 → 미채택 개정안 8 종결 가능.
- 문서에 적힌 경로 전부 실존(references 2종·scripts/validate.py·config·audit 2종·배포본 manifest.json·service-worker.js·icon 2종·og-image.png·favicon.png).
- 인코딩 UTF-8 BOM, 천단위 콤마 없음 — 직전 회차와 같은 파일이라 동일.

## 라이브 Pages 확인 — web_fetch 캐시 확정
- 점검표 2) 순서대로 web_fetch. **대조군**: `github.com/…/saero-ad-report-skill/blob/main/SKILL.md`를 web_fetch하니 `234 lines (162 loc) · 12.7 KB`에 옛 본문(2단계 "각 CSV의 `일별`", 검산 목록 4개, 토큰 표 없음)이 왔다. 같은 시각 `git clone` HEAD(cb95494)는 312행이고 GitHub 웹도 당연히 그것을 보여준다 → **web_fetch가 옛 사본을 준다는 것이 이번에 저장소 파일로 직접 확정됐다.**
- 라이브 Pages도 web_fetch는 `클릭률 강조: 07번 표에서`(옛 문구). 위 대조군 결과로 캐시로 판정. masthead·KPI(4,912/110/2.24%/98,009)는 저장소와 같음.
- bash: `leekwanbeom.github.io` 403(허용 목록 외, 직전 회차와 같음). `api.github.com/…/pages/builds/latest`는 무인증 404(Pages API는 인증 필요). `raw.githubusercontent.com/…/index.html`은 200이지만 이건 저장소 사본이라 라이브 검증이 아님.
- 결론: 이 환경에서 라이브를 기계로 확인할 수단이 없다. 사용자 시크릿 창 확인이 유일. 결함 아님.

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

## 2026-09-28 갱신 회차 (진단 아님 — 리포트 배포 회차)
합본 `일별` 2026.08.26~09.27 (33일) · 배포 커밋 `e1df211`(직전 `083aaab`, 파일 sha c968d06 → 739d98d(1차 `0272498`) → 67f28d2(정정 재배포)) · 집계 기간 `2026.08.26 — 09.27 (33일)`
validate.py 검사 22개 전부 PASS(실행 출력 [PASS] 줄 세어 22 — KPI 노출 9,985 / 클릭 309 / CTR 3.09% / 광고비 351,299원, 제외 전 전체 9,991 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 083aaab = prev.html md5 88fe1bd0) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(545ced5f…, 2,101행)
`--pending` 사용: 아니오 — 채팅 질문 1건(9/27 첫 등장 제외 후보 6개 등록 승인). 07 각주·11·12번은 "채팅으로 제안했음"으로 사실만 적어 잔존 문구 0건(검사 21 PASS)
**효율: 벽시계 약 18분(clone 01:45 → 정정 재배포 push 02:03 UTC, 1차 배포까지 약 15분) · 도구 호출 약 47회(정정 재배포까지; audit 기록 포함 약 52회) · 즉석 코드 약 400행**(work/adhoc: facts.py 72 — 서술용 사실 확인 / apply.py 209 — compute.json → HTML 기계 자리 교체(09-27 apply.py를 다시 씀, compare.py 정규식을 거꾸로 적용) / narrative.py 107 — 서술 교체(대부분 문자열) / fix1.py 14 — 경쟁사 문구 정정. 리포트 숫자는 전부 compute.json — 계산 코드 0행. **apply.py가 두 회차 연속 같은 형태로 다시 쓰임 → E2(저장소에 두기) 진단 회차 판단 대상**)
- **1단계**: 업로드 4종 기간헤더 2026.09.01~09.27(이번 달 1일~어제, 27일) → `archive.py store` 4종 덮어쓰기·`combine` PASS(8월 조각 2,363/50/36,397 + 9월 조각 7,628/259/314,902 = 33일 9,991/309/351,299원). **data push 403** — 토큰이 배포 저장소용 1개만 옴(`git push --dry-run` 403·Contents GET 200으로 판별). `data:` 커밋 `c8d4441`은 로컬에만 → 스킬 저장소 토큰 요청(09-27과 같은 경우). 이 기록의 push도 같은 토큰 대기.
- 2-1단계 선확인 작동(배포본 32일 ≠ 합본 33일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.06%·최근 3일 [0,0,0] / 노원키즈 [0,0,0]은 09-17 규칙대로 04번 행 유지). 01·06 min-width 2560 → 2640, 라벨 `[33, 33]`. 05 top5 순서 변동 없음(apply.py가 라벨 순서 assert). 06 카드 큰 숫자 = 04 셀(상계동 2.56·노원산전 1.68, 검사 15 PASS). costPie title 총액 344,274 → 351,299원 손으로 교체(compare 대상 밖 — 다음 회차도 확인). KPI CTR 타일 `:g` 표기 3.09.
- **9/27(일, 연휴 뒤 첫날)**: 노출 254(플 212·파 42)·클릭 7(플 5·파 2)·CTR 2.76%·광고비 7,025원(플 6,087·CPC 1,217 / 파 938·CPC 469). 노출은 9/22(318) 이후 최다, 광고비는 9월 네 번째로 적은 날(9/26 6,077·9/19 6,443·9/8 6,921 다음). 하루 CPC 1,004원은 9/13(962) 이후 최저. **파워링크 42회 = 개업 이후 하루 최저 사흘 연속 갱신(57 → 46 → 42)이지만 클릭 2건**(노원산전 자동매칭 "노원산후필라테스" 476·노원역 자동매칭 "노원필라테스가격" 462) → 클릭 0 이틀 끊김, 노원산전 닷새 0(9/22~9/26) 끊김. 플레이스 하루 CTR 2.36%·순위 2.83(누적 3.04 → 3.03). 누적 CTR 3.10 → 3.09, 검색 지면 3.78 → 3.75%(두 회차 연속 하락). 상향 후 열하루 평균 12,603원·8.5건·CPC 1,491(전 9,658·7.2·1,344).
- **11번 판정**: 직전 8개 → 유지 6 · 뒤집힘 2(파워링크 클릭 0 이틀 → 9/27 2건 / "필라테스" 클릭 0 이틀 → 9/27 1건 — 하나로 묶어 맨 위) · 근거 소멸 0. 직전 맨 위 뒤집힘 2개(연휴 CTR·플레이스 순위)는 방향이 이어져 유지로 옮김. 신규 독립 항목 2(9/27 하루치 성과 / 중계역필라테스 2건). 이번 8개 + (참고) 2. 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어: 7개·6개 첫 판정일 0, 33개 등록 당일, 신규 후보 6개 채팅 제안) · 보류 유지 1(상계동 9/27 6회, 하루 평균 17.2). 신규·철회 0. 파워링크 "사흘 이상 클릭 0" 신규 후보 조건은 9/27 2건으로 해소.
- **07번**: 정식표 19행 280 + 클릭1건 24(신규 노원산후필라테스 14회/476원·노원필라테스가격 12회/462원 — 둘 다 파워링크 자동매칭 클릭) + 경쟁사 5 = 309. 9/27 7건 = 일치 5(중계역필라테스 2·필라테스·노원역필라테스·노원필라테스 각 1) + 확장 2. 중계역 13 → 15건(CTR 13.98 → 14.71%). 근처필라테스 87회·3.45%. 클릭 0 전체 592개·1,949회(19회차 연속 증가), ≥5 목록 66개. 행 단위 확장·클릭0 9/25 50 → 9/26 36 → 9/27 27회(23개) = 자동매칭 30회(노원산전 17·노원역 11·상계동 2) − 클릭 붙은 2행 3회. 동률은 apply.py에서 직전 순서를 2차 키로.
- **08번**: TOP 10 구성 동일, 순서 변동 — 9/27 영등포 8회로 중구·영등포(각 149)가 남양주(148)를 넘음(남양주 8 → 10위). 11위 의정부 128 vs 10위 남양주 148. 컴팩트 35개·78건(변동 없음), 클릭 0 150개·1,131회. 9/27 클릭 7건 전부 노원구(165회 = 254의 65%). 노원 47%·50%(46·48), 타겟 63%·61%(62·60)·CTR 2.98, 확인불가 478·23·28,975(8.2%, CTR 4.81), 타겟 밖 서울 1,393·54·3.88%, 서울·경기 밖 3.0% → 전국 유지.
- **09·10번**: 15시 27회 17회차 연속. 2위 9시·13시 22 동률 유지(둘 다 9/27 0), 22시 19 → 21로 14시와 동률. 심야 2,126·70·66,013원(21%·23%), 9/27 7건 중 심야 4(6시 1·7시 1·22시 2), 나머지 17시 2·21시 1. 10번 A 8,099·307·350,141 / B 140·2·1,158(9/27 다음 PC 1·다음 모바일 3 = 4회) / C 22 / D 1,724, 콘텐츠 22일 연속 0.
- **제외 검색어(5-0단계, `propose` 창 9/27)**: 재노출 판정 1건(노원역보세 — 9/27 등록 당일, 판정 안 함 = 등록돼 있는데도 노출 0 · 등록 누락 0 · 미확인 0) / 17·22·9·11개 0 유지, 9/26 재등록 7개·9/26 등록 6개 판정 첫날 0 / 33개는 등록 당일(9/28부터) / 신규 후보 6(노원역24시간·노원역감성맛집·노원역근처건물·노원역스텝·노원우동집·노원힐링장소. — 전부 확장·1회·클릭 0) → **승인 문구 채팅에 붙임, 답 오기 전 등록 0** / 업종어 포함 4(노원역50대필라테스·시니어방문필라테스·에반더필라테스상계역·필라테스노원마라탕) 보이기만 / 뺀 것 4(운동 3·경쟁사명 1) / 재등록 후보 0 / 어근 조합 4(맛집·우동·건물·24시 각 1). registry 행수 변화 없음(쓰기 0). 등록 n·verified n·실패 n = 0/0/0(승인 전).
- **경쟁사**: config 변경 없음. 9/27 젠 1(82 → 83)·와우 2(24 → 26)·이레 1(7 → 8)·퍼스트 1(1 → 2)·**퍼스트필라테스노원점 1(compute 신규변형후보 → 표기 변형으로 26행 추가, 소재구 노원구·확장)**, 클릭 0. 솔라·이루다 9/27 0(1회차째 → 보류 유지, 09-27 조건 "2회차 연속"). 신규 1회짜리 모브필라테스(일치 1) 보류(웹 검색 특정 불가). **에반더필라테스상계역(확장 1) = 09-06 종결 건(에반더필라테스상계역점)의 재등장 → 종결 유지** — 1차 배포에서 신규 후보로 잘못 적었다가 이력 표 대조 뒤 문구 4곳 정정 재배포(`e1df211`). 교훈: 1회짜리 브랜드형은 이력 표에 이름이 있는지 먼저 grep.
- **사용자에게 요청한 값(09-28 채팅)**: ① 제외 후보 6개 등록 승인("등록 승인 N개") ② 스킬 저장소 토큰(data/ 커밋 `c8d4441`·이 기록 push용).
- **09-28 채팅 후속 1 — 토큰·push**: 스킬 저장소 토큰 수령(파일로만 저장) → `git fetch`·rebase(원격 변화 없음) → `c8d4441`(9월 보관본)·`284c60a`(이 기록) push 완료, 재clone md5 5개(CSV 4 + last-audit.md) 일치.
- **09-28 채팅 후속 2 — 등록 완료(사용자 답 "등록 승인 6개 전부")**: 세션 `push --dry-run`(호출 0: 거부 0·3그룹 각 6·216 → 222/950) → 승인 목록 `work/approved_2026-09-28.txt`(6줄)를 present_files로 전달. **실행은 사장님 PC 데스크톱 앱 Code 탭(Claude Code, 저장소 새 clone)** — 첫 Claude Code 실측: 읽기 전용 `pull` exit 0(3그룹 각 216, `api.searchad.naver.com` 열림 — Cowork device_bash 403·클라우드 403과 달리 PC 일반 셸과 같은 경로) → `push` 그룹마다 5개 등록 → 자동 verify 15/15·실패 0 → registry 649 → **664행**(등록 221×3 + 시험 deleted 1), description `saero 09-28`, id `rst-a001-00-000002190005336`~`350`(연번), 커밋 `bf3089e`(사용자 화면 2장 + 세션 재pull·registry 실측). "노원힐링장소."는 Code 탭 세션이 마침표를 문장부호로 판단해 "노원힐링장소"(09-17 기등록)로 건너뜀 → 원문(마침표 포함)은 미등록 상태로 남음(아래 주의 ①). 계정 쓰기: 등록 15건, 삭제·시험 0.
  **재배포 `32d8b05`(파일 sha 67f28d2 → 1c52f70)**, validate 22개 전부 PASS · compare 95 OK / DIFF 0(직전 배포본 인자 083aaab) · overflow 0 · 재수령본 md5 일치(a3465ec0…). 숫자 변경 0 — 문구 7곳(07 각주 1 · 11번 5번 항목·판정 줄 2 · 12번 1번 제목·본문·다음 회차 판정·이월 판정 4): "채팅으로 제안했음" → "9/28 승인으로 스킬이 등록·확인 완료(신규 5 + 기등록 1), 9/29부터 판정". `--pending` 없음, 잔존 문구 0. 즉석 코드 fix2.py 14행(문구 교체). 제외 검색어 요약(8단계 양식): 후보 6 → 승인 6 → 등록 5 · verified 5 · 실패 0(기등록 1) / registry 664행.
  주의 ① **원문 규칙 어긋남**: 승인·registry·CSV 이름은 원문대로(exclusion-ui.md 7절)인데 Code 탭 세션이 "노원힐링장소."의 마침표를 뺐다. 네이버 대조가 정확 일치라면 마침표 검색은 계속 노출될 수 있음 — 1회짜리라 실익 없어 재등록 안 함. 다음 회차에 "노원힐링장소."가 확장 행에 잡히면 propose는 "이전 CSV에 있었던 이름"으로 건너뛰므로 **사람이 재상정**. Claude Code 실행 지시문에 "이름은 원문 그대로(기호·마침표 포함)"를 넣을 것. ② **결함 후보**: verify가 registry `note`를 "등록 요청 성공(확인 전)"으로 남긴 채 `status=registered`만 바꾼다(09-27 등록분도 동일, Code 탭 세션 지적) — 다음 점검 회차 결함 목록. ③ **실행 경로 갱신**: `references/exclusion-ui.md` 3절에 Claude Code 실측 한 줄 추가(이 커밋). **사용자 결정(같은 세션 후속): "Code 탭 한곳으로"** — 맨 위 탐색 기준선의 결정 블록에 기록. feat-report-fetch(구현 기준선 최종 47a9f43, 다음 = 검증) 검증·병합 뒤 새 기능 추가 회차 "Code 탭 전 단계 실행"으로 진행. 탐색·설계 프롬프트(⑥ 양식)는 채팅으로 전달.
- 다음 회차 대조: 이번 달 파일 9/1~어제로 덮어쓰기 / 33개(9/28~) 판정 첫날 / 9/28 등록 5개(9/29~) / 7개·6개·17·22·9·11개 0 유지 / "노원힐링장소."(마침표) 재노출 시 수동 재상정 / verify note 결함 후보(점검 회차) / 파워링크 노출 최저 갱신 이어지면 순위와 같이 / 노원산전 클릭 재개 뒤 방향 / 플레이스 CTR·순위 연휴 뒤 방향 / 2위 동률(9시·13시) / 솔라·이루다·모브 추가 노출(없으면 솔라·이루다 종결) / 남양주 10위 유지 여부 / costPie title 총액 / apply.py E2 판단 / 10월 1일엔 9월 확정본(09.01~09.30)을 받아 `data/2026-09` 덮어쓰기, 10월은 새 폴더.

## 2026-09-27 갱신 회차 (진단 아님 — 리포트 배포 회차) · **병합본 main 첫 실사용 회차**
합본 `일별` 2026.08.26~09.26 (32일) · 배포 커밋 `277889d`(직전 `ad48222`, 파일 sha 8c4b017 → d7715fb) · 집계 기간 `2026.08.26 — 09.26 (32일)`
validate.py 검사 22개 전부 PASS(실행 출력 [PASS] 줄 세어 22 — KPI 노출 9,731 / 클릭 302 / CTR 3.1% / 광고비 344,274원, 제외 전 전체 9,737 — 차이 6) · compare.py 차이 0(항목 95, 직전 배포본 인자 ad48222 = prev.html md5 4defb16a) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(94b436f2…, 2,083행)
`--pending` 사용: 아니오 — 채팅 질문 2건(① 32개 중 재등록 안 한 25개에서 9/26 재노출 3개 재등록 여부 ② 9/26 첫 등장 제외 후보 11개 등록 여부). 07 각주·11·12번은 "채팅으로 알렸음"으로 사실만 적어 잔존 문구 0건(검사 21 PASS)
**효율: 벽시계 약 19분(clone→배포 push) · 도구 호출 45회(배포까지; audit 기록 포함 약 50회) · 즉석 코드 약 480행**(work/adhoc: facts.py 67 — 서술용 사실 확인 / apply.py 273 — compute.json → HTML 기계 자리 교체 / narrative.py 114 — 서술 교체 / 인라인 python 약 25. E2가 없어 apply.py를 이번 회차 폴더에서 새로 씀 — **E2 초안 후보**, 저장소엔 넣지 않음)
- **새 절차 대조(2026-09-27 병합 "첫 실사용" 항목)**: 1단계 `scripts/ingest.sh` 실행 — store 4종·combine PASS(32일 · 9,737/302/344,274원)까지 통과했으나 **data push 403**(토큰이 배포 저장소용 1개만 옴 → `data:` 커밋 `f625fbc`는 로컬에만, 스킬 저장소 토큰 요청) · 4단계 `deploy.py fetch --out prev.html` + `cp` 작업본 · 5단계 `compute.py --competitors-html prev.html`(신규 변형 후보 []) · 6단계 `precheck.sh` 3인자(작업본·합본·prev.html, `--pending` 없음) 1회 FAIL → 2회 통과 · 7단계 `deploy.py push`(sha 재조회 8c4b017 그대로) → `verify` 일치. 즉석 계산은 서술용 사실(facts.py)뿐이고 리포트 숫자는 전부 compute.json.
- **6단계 1회 FAIL**: KPI 타일 클릭률을 `3.10`으로 썼더니 validate 검사 7이 `f"{ctr:g}"` = `3.1`과 문자열 비교해 FAIL → 타일을 `3.1`로. (compare.py는 float 비교라 통과했음 — 두 검사의 표기 기준이 다름, 결함 아님·기록만. 09-26까지 3.11·3.13 등 두 자리라 드러나지 않았던 경우)
- **토큰**: 처음엔 1개만 옴 → 배포 저장소 GET/PUT 성공, 스킬 저장소는 `git push` 2회·Contents API PUT 1회 전부 403(`Resource not accessible by personal access token` — 배포 저장소 전용 토큰으로 확정. API `/repos` 응답의 `permissions`는 계정 권한이라 토큰 범위 판별에 못 씀). **09-27 채팅 후속: 두 번째 토큰(스킬 저장소) 수령 → `f625fbc`(data 9월분)·`aaf739d`(이 기록) push 완료, 재clone md5 8파일·combine PASS 확인.** 앞으로 토큰 2개를 처음부터 함께 받는 것이 빠르다(09-25·09-26과 같음).
- 2-1단계 선확인 작동(배포본 31일 ≠ 합본 32일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0 / 노원키즈 9/18~ 노출 0은 09-17 규칙대로 04번 행 유지). 01·06 min-width 2480 → 2560, 라벨 `[32, 32]`. 05 top5 순서 변동 없음(검사 14 PASS). 06 카드 큰 숫자 = 04 셀(상계동 2.57·노원산전 1.66, 검사 15 PASS). costPie title 총액(338,197 → 344,274원)은 compare 대상 밖이라 손으로 교체 — 다음 회차도 확인.
- **9/26(토, 연휴 마지막 날)**: 노출 212(플 166·파 46)·클릭 4(전부 플레이스 — 노원역필라테스 2·상계동필라테스 1·운동 1, 전부 일치)·CTR 1.89%(9/19 1.78% 이후 최저)·광고비 6,077원(8/29 5,092원 이후 최저, 전부 플레이스, CPC 1,519). 파워링크 46회 = 개업 이후 최저(9/25 57회에 이어 이틀 연속 갱신)·클릭 0 이틀 연속. 플레이스 하루 CTR 2.41%, 순위 2.89(누적 3.04 그대로). 누적 CTR 3.13 → 3.10%, 검색 지면 3.83 → 3.78%(일곱 회차 3.8%대 처음 이탈). 상향 후 열흘 평균 13,254원·8.8건·CPC 1,506.
- **11번 판정**: 직전 7개 → 유지 5 · 뒤집힘 2(연휴 이틀 CTR 4%대 → 9/26 1.89% / 플레이스 순위 사흘 연속 상승 → 2.89위) · 근거 소멸 0. 이번 8개 + (참고) 2(신규 독립 항목 1: 9/26 클릭 4건 중 3건이 용인 수지·이천·대전 중구 — 노원역필라테스 2건 3,091원 = 용인 1,760 + 이천 1,331, 상계동필라테스 1,273 = 대전; 귀성·이동 중 검색 가능성으로만 서술). 검사 19~21 PASS.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(제외 검색어) · 보류 유지 1(상계동 9/26 11회, 순위 1.81). 신규·철회 0.
- **07번**: 정식표 19행 275 + 클릭1건 22 + 경쟁사 5 = 302. 상계동필라테스 6 → 7건(새로·노원구필라테스와 동률, 노출 525로 셋 중 위), 운동 5 → 6건, 노원역필라테스 61 → 63건(CPC 1,024 → 1,041). "필라테스" 이틀 연속 클릭 0(9/25 23·9/26 29회). 근처필라테스 80회·3.75%(강조 없음 유지). 클릭 0 전체 579개·1,935회(18회차 연속 증가), ≥5 목록 65개(노원스포츠 6·노원역10번출구 5 진입). 행 단위 확장·클릭0 9/24 59 → 9/25 50 → 9/26 36회(30개) = 자동매칭 36회(노원산전 15·노원역 15·상계동 6) 일치. 클릭1건 동률·클릭0 동률·08 컴팩트 동률은 직전 HTML 순서 유지(apply.py에서 직전 순서를 2차 키로).
- **08번**: TOP 10 구성·순서 동일(의정부 127 vs 영등포 141). 컴팩트 35개·78건(신규 대전광역시 중구 24·1, 용인시 수지구 18·1, 이천시 6·1 — 대전은 compare `short()` 축약 대상이 아니라 전체 이름 그대로), 클릭 0 150개·1,124회. 노원 46%·48%, 타겟 62%·60%(CTR 2.96), 확인불가 460·23·28,975원(8.4%, CTR 5.00), 타겟 밖 서울 1,372·54·3.94%, 서울·경기 밖 비용 2.7 → 3.0% → 전국 유지.
- **09·10번**: 15시 27회 16회차 연속. **2위 9시·13시 22회 동률**(9시 21 → 22) — compute `2위.시`=9, HTML "2위는 9시 22회로 13시(22회)와 동률". 심야 2,061·66·61,872원(21%·22%), 9/26 4건 = 9·10·21·22시 각 1. 10번 A 7,849·300·343,116 / B 136·2·1,158(9/26 다음-모바일 2회) / C 22 / D 1,724, 콘텐츠 21일 연속 0.
- **제외 검색어 대조(9/26 "확장" 행)**: ① 17개(9/21~, 엿새) 0 ② 22개(9/22~, 닷새) 0 ③ 9개(9/25~, 이틀) 0 ④ 11개(9/26~, 첫날) 0 ⑤ **32개 중 재등록 안 한 25개에서 3개·3회**(노원역10번출구·노원역배스킨·노원체험 각 1, 클릭 0) — 9/24 6개·11회, 9/25 7개·13회에 이어 사흘 연속 → 채팅 보고(재등록 여부는 사용자 결정) ⑥ 9/26 재등록 7개 중 노원구어린이 1회 = 등록 당일(판정 안 함) ⑦ 9/26 등록 6개 등록 당일 0 ⑧ 어근 "노원역24시간우동"·"노원역새로오픈소고기" 각 1 ⑨ 9/10·9/17 알려진 이름 0. 
- **9/26 첫 등장 16개**(전부 확장·클릭 0): 무관 10(노원역헬스장 3·노원식당맛집 2·새로클린노원 2·노원아띠·노원역24시간우동·노원역7번출구주차·노원역9번·노원역맛집출구·노원역보세·노원역새로오픈소고기 각 1) + 애매 1(노원필테강사 — 09-20 등록 "노원필라테스강사" 계열) → 제외 후보 11개 채팅 제안 / 필라테스·운동 검색 3(노원필라테스주말·필라테스1:1노원·노원역유산소운동) 그대로 / 브랜드형 2(노원솔라필라테스·이루다필라테스산전) → 아래 경쟁사 이력.
- **경쟁사**: config 변경 없음. 젠 77 → 82(9/26 일치 5회), 노원역필라테스정원 1 → 2. 클릭 0. 아트·엠코 9/26 0(2회차 연속) → 종결. 필라테스안 9/26 0(제외 확정 건). 신규 1회짜리 2건 보류(웹 검색: 노원솔라필라테스 특정 불가 / 이루다필라테스&자이로토닉 예약 앱은 있으나 지점·소재지 특정 불가).
- **사용자에게 요청한 값(09-27 채팅, 답 없이 배포)**: ① 25개 중 9/26 재노출 3개 재등록 여부 ② 9/26 첫 등장 제외 후보 11개 등록 여부 ③ 스킬 저장소 토큰(data/·audit push용) — ③은 같은 세션에서 수령·push 완료, ①②는 답 대기(등록 사실이 오면 07·12번 문구를 "등록 완료, 다음 날부터 판정"으로 고쳐 재배포).
- **09-27 채팅 후속 2 — 같은 데이터 재배포 `083aaab`(파일 sha d7715fb → c968d06), validate 22개 전부 PASS([PASS] 줄 세어 22) · compare 95 OK / DIFF 0(직전 배포본 인자 277889d = prev.html md5 94b436f2) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치(88fe1bd0…, 2,083행).** 경위: 사용자가 9/1~9/26 CSV 4종을 다시 올림 — 보관본 `data/2026-09/`와 md5 4개 전부 동일. 2-1단계 선확인 작동(배포본 집계 기간 = CSV 32일 동일)으로 계산 전에 멈추고 질문(문구만 재배포 / 내일 새 회차 / 전부 재계산) → 사용자 선택 **"그래도 전부 다시 계산·배포"**. 1단계 `ingest.sh`: store 4종(덮어쓰기, 내용 동일)·combine PASS(32일 · 9,737/302/344,274원)·"data/ 변경 없음 — push 생략". 4단계 fetch prev.html(sha d7715fb). 5단계 compute.json = 직전 회차와 동일(KPI 9,731/302/3.1%/344,274원, 신규 변형 후보 []). **숫자 변경 0 — 바뀐 것은 문구 10곳**(07 각주 2 · 11번 5번 항목·(참고)·판정 줄 3 · 12번 1번 제목·본문 2·다음 회차 판정·이월 판정 5): "3개·11개는 채팅으로 알렸음(답 대기)" → "9/27 API 조회로 32개 중 22개가 세 그룹 어디에도 미등록(재노출 = 등록 누락으로 보임) → 22 + 9/26 첫 등장 11 = 33개를 9/27 14:08 스킬로 등록·확인 완료, 9/28부터 판정"(위 4항 첫 자동 회차 결과를 리포트에 반영 — 09-27 갱신 회차 "요청한 값" ①②의 답). `--pending` 없음, 검사 21 잔존 문구 0. 11번 항목 수·판정 집계(8 + 참고 2, 7 = 5+2+0)는 그대로 두고(재배포라 직전 회차 판정을 다시 하지 않음) 판정 줄 끝에 재배포 사실 한 문장. 5-0단계 `propose`(창 9/26): 신규 후보 0 · 재등록 후보 0 · 재노출 판정 15건(등록 당일 1 = 노원구어린이 / 등록 전 노출(정상) 14 = 9/27 등록분) · 등록돼 있는데도 노출 0 · 뺀 것 5(운동 3·산전 1·경쟁사명 1) → 승인 요청 없음(건수 0, 쓰기 0). 제외 그룹 신규 후보 없음(데이터 동일).
  **효율: 벽시계 약 7분(clone 07:02 → 배포 push 07:08 UTC, 사용자 답 대기 포함) · 도구 호출 34회(배포까지, 선확인 질문 1회 포함) · 즉석 코드 약 100행**(`work/adhoc/wording.py` 40 — 문구 교체 10건, 각 문자열 1회 일치 assert / 인라인 python 약 60 — 배포본 문구 위치·md5 대조용 읽기 전용. 계산 코드 0행 — 리포트 숫자는 전부 compute.json). 토큰: 1개 수령(배포 저장소용 — GET·PUT·verify 성공). 이 기록 push는 같은 토큰으로 시도 → 결과는 채팅에 기록.
- 다음 회차 대조: 이번 달 파일 9/1~어제로 덮어쓰기 / 9/27 등록 33개는 9/28부터 판정(9/27 데이터에서는 등록 당일이라 판정 안 함 — propose가 자동 처리) / 7개(9/27~)·6개(9/27~) 판정 첫날 / 17·22·9·11개 0 유지 / 파워링크 클릭 0 사흘째면 노출·순위와 같이(12번 신규 후보) / 노원산전 클릭 재개 / 플레이스 순위·CTR 연휴 뒤 방향 / 2위 동률(9시·13시) 해소 여부 / 노원솔라·이루다 추가 노출(없으면 종결) / costPie title 총액 / KPI CTR 타일은 `:g` 표기(3.1) / apply.py를 E2 초안으로 올릴지(진단 회차 판단).

## 2026-09-26 갱신 회차 (진단 아님 — 리포트 배포 회차) · **원본 월별 보관(data/) 도입 회차**

**경위**: 첫 업로드 CSV 4종이 기간헤더 2026.08.27~09.25(최근 30일)라 개업일 8/26이 빠져 2단계에서 멈춤. 사용자 확인: 네이버가 **최근 30일까지만** 내려받게 함(09-17~09-25 회차 기간헤더도 전부 정확히 30일이었음 — 오늘 처음 8/26이 창 밖으로 밀려남). 사용자 결정으로 **원본을 스킬 저장소에 월별 보관**: 지난달은 확정본, 이번 달은 매일 1일~어제로 받아 덮어씀. 8월분(헤더 08.01~08.31, 실데이터 08.26~08.31)은 정상 수령됨 — "최근 30일" 제한은 **기간 길이** 제한으로 보이며 30일 전 날짜도 받을 수 있었음(실측).
- 스킬 저장소 커밋 `0e96147`: `data/2026-08/`·`data/2026-09/`(09.01~09.25) 4종 원본(md5 업로드본과 동일) + `scripts/archive.py`(store/combine) + SKILL.md 1·2단계·토큰 표·원본 보관 절. SKILL.md 저장 후 view로 반영 확인. 재clone 후 md5 8개 일치·combine PASS.
- archive.py 파괴 실험 4종 전부 FAIL로 멈춤: 옛 다운로드(기간 끝 이름) 거부 / 시간대별 노출 +1(조각 기간 불일치) / 8월 폴더 제거(일별 최솟값 ≠ open_date) / 검색어 헤더 09.02 시작(빈틈).
- **재현**: 합본을 9/24까지 잘라 직전 배포본(`036080a`)에 validate → 13 PASS + 시간대별만 FAIL(298 vs 290, 9/25 포함이라 예상대로). 합본 시간대별 − 직전 배포본 09번 배열 = 시간대마다 0 이상·합 194회·8건 = 9/25 하루치 → **월별 합산이 날짜 없는 시간대별까지 정확히 맞음**을 확인.
- 저장소가 공개라 원본 CSV가 공개된다는 점을 사용자에게 알림(비공개 전환 여부는 미정).

CSV 합본 `일별` 2026.08.26~09.25(31일), 계정 2580077. 배포 커밋 `4c08ab3`(직전 `036080a`, 파일 sha 96c4a77 → ef2aa5e). 집계 기간 `2026.08.26 — 09.25 (31일)`.
validate.py 14개 검사 전부 PASS(실행 출력 [PASS] 줄 세어 14 — KPI 노출 9,519 / 클릭 298 / CTR 3.13% / 광고비 338,197원, 제외 전 전체 9,525 — 차이 6). 배포 후 재수령본 md5 동일(90288880…)·14 PASS. playwright 360·390·430px scrollWidth = 뷰포트(넘침 0).
2-1단계 선확인 작동(배포본 30일 ≠ 합본 31일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0). 01·06 min-width 2400 → 2480, 라벨 `[31, 31]`.

- **토큰**: 두 개를 채팅 원문에서 바로 파일로 저장(09-23 교훈). 배포 GET·PUT은 첫 번째, data·SKILL·이 파일 push는 두 번째.
- **진행 경위**: 두 번째 응답에서 01~10번까지 반영 후 도구 한도로 멈춤 → 사용자 "계속" → 작업 파일 남아 있어 12 → 11번 순으로 쓰고 검증·배포. 채팅 질문 3건은 답 없이 배포(아래).
- **9/25(추석 당일)**: 노출 194(9/13 183회 이후 최저)·클릭 8·CTR 4.12%·12,014원 전부 플레이스(137회·8건·CPC 1,502·하루 CTR 5.84%). 파워링크 57회(**개업 이후 하루 최저**)·클릭 0 → 나흘 연속 클릭(9/21~9/24) 끊김. 플레이스 순위 2.38위(9/6 이후 두 번째, 최고 9/20 2.35), 누적 3.06 → 3.04위. 누적 CTR 3.11 → 3.13%, 검색 지면 3.83% 그대로(7,773·298).
- **11번 판정**: 직전 7개 → 유지 6 · 뒤집힘 1(파워링크 연속 클릭 → 9/25 0건) · 근거 소멸 0. 7개 + (참고) 2. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(32개 이틀 연속 재노출 → 걸어둔 조건대로 탭 목록 확인 요청) · 보류 유지 1(상계동 9/25 3회, 등록 이후 최저). 신규·철회 0.
- **정정 1건**: 06번 노원산전필라테스 카드 큰 숫자가 1.70위로 본문(1.69위)과 어긋나 있었음(직전 회차 누락) → 04번 표와 같은 1.67위로. **교훈: 06번 카드 큰 숫자는 04번 평균순위 셀과 같은 값인지 매 회차 대조.** (09-25 매체 top5 누락과 같은 유형 — validate 대상 밖)
- 04번 예산 비중 92.8 / 3.8 / 1.5 / 1.0 / 0.9(보통 반올림과 같음). CPC 격차 3.55 → 3.57배(노원역 366 고정, 플레이스 1,301 → 1,308). 05번 매체 top5 순서 변동 없음(재대조함). 06번 rankChart = 노원역필라테스 **그룹 전체(자동매칭 포함)** 가중순위여야 배포본 30개가 재현됨(직접 등록 키워드만이면 0/30) — 9/25 2.42.
- **07번**: 정식표 19행 271 + 클릭1건 22 + 경쟁사 5 = 298. 창동역필라테스 7 → 9건(마들역·상계역과 동률, 노출 적어 셋 중 마지막). **근처필라테스 3/76 = 3.95% → `.ctr-high` 해제.** 클릭 0 전체 563개·1,885회(17회차 연속 증가), ≥5 목록에 노원구어린이·노원그룹필라테스·노원키즈체험 진입(63개).
- **08번**: TOP 10 구성·순서 동일. 컴팩트 32개·75건(의정부 2 → 4건), 클릭 0 153개·1,146회. 노원 46%·49%(클릭 50 → 49), 타겟 62%·60%, 확인불가 447·23·28,975원(8.6%, CTR 5.15%), 서울·경기 밖 비용 2.7% → 전국 유지.
- **09·10번**: 15시 27회 15회차 연속, 2위 13시 22 단독. 심야 2,012·65·60,112원(21%·22%). 10번 A는 **`네이버`로 시작하는 검색 매체 전부**(네이버 검색탭 10회·1건 포함) — A 7,639·296·337,039 / B 134·2·1,158(9/25 3회) / C 22 / D 1,724.
- **제외 검색어 대조**: ① 17개(9/21~) 0 ② 22개(9/22~) 0 ③ **32개 9/25 7개·13회**(노원구어린이 3·노원역9번출구 3·노원9월행사 2·노원역추석 2·노원어린이체험·노원역6번출구·노원역테니스레슨 각 1, 클릭 0) — 이틀 연속 → 채팅으로 "제외 검색어" 탭 목록 확인 요청 ④ 9개(9/25~) 첫날 0 ⑤ 11개 등록 당일 0 ⑥ 어근 "노원역에새건물" 1 ⑦ 9/10·9/17 알려진 이름 0. 확장·클릭0 9/25 50회(34개) = 자동매칭 50회.
- **경쟁사**: config 변경 없음. "필라테스정원노원산전필라테스"(9/25 확장 1) 표기 변형으로 07번 표 25행(정원 변형 11개·누적 21). 젠 75 → 77. **필라테스안 계열 9/23~9/25 사흘 6회(누적 8)** — 웹 검색 특정 불가 → 채팅 확인 요청, 표 미등재. 아트·엠코 9/25 0(1회차).
- **사용자에게 요청한 값(09-26 채팅, 답 없이 배포)**: ① 32개 중 7개 이름이 제외 검색어 탭 목록에 있는지 ② 제외 후보 3개(노원역에새건물·노원역추석영업·6세필라테스) 등록 여부 ③ 애매 3개(노원역두·노원역월·노원역스튜디오) 판단 ④ 필라테스안 소재지.
- **09-26 채팅 후속 — 재배포 `ad48222`(파일 sha ef2aa5e → 8c4b017), 14 PASS·재수령본 md5 일치(4defb16a…).** 사용자 답 3건: ① 32개 중 재노출 7개를 파워링크 3개 그룹에 **다시 등록**(9/27부터 판정) ② 제외 후보 3개 + 애매 3개 **6개 모두 등록**(9/27부터 판정) ③ **필라테스안 = 노원 업체 아님 → 제외 확정**. 07·11·12번의 "확인 요청/판단 요청" 문구를 전부 결정 사실로 바꿈(잔존 0건 grep 확인). 11번 판정 집계(유지 6·뒤집힘 1)·7개 + (참고) 2 그대로, 수동 검사 5종 0건.
- 다음 회차 대조: 이번 달 파일은 **9/1~어제로 덮어쓰기**(store가 옛 파일 거부) / 32개 확인 결과 / 17·22·9개 0 유지 / 11개(9/26~) / 파워링크 클릭 재개(사흘 이상 0이면 노출·순위와 같이) / 추석 연휴 끝(9/26) 뒤 노출 회복 여부 / 필라테스안·아트·엠코 / 06번 카드 숫자 = 04번 셀 / 10월 1일엔 9월 확정본(09.01~09.30)을 받아 `data/2026-09` 덮어쓰기, 10월은 새 폴더.

## 2026-09-25 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.24(30일), 계정 2580077(기간헤더 2026.08.26~09.24 — 사용자가 개업일부터 지정해 받음). 배포본 index.html 갱신·배포 완료.
배포 커밋 `f5a94aa`(직전 `feed999`, 파일 sha c708134 → af6a5c0). 집계 기간 `2026.08.26 — 09.24 (30일)`.
validate.py 14개 검사 전부 PASS(실행 출력 [PASS] 줄 세어 14 — KPI 노출 9,325 / 클릭 290 / CTR 3.11% / 광고비 326,183원, 제외 전 전체 9,331 — 차이 6). 배포 후 재수령본 md5 동일(4834d7d6…)·14 PASS. playwright 360·390·430px scrollWidth = 뷰포트(넘침 0).
2-1단계 선확인 작동(배포본 29일 ≠ CSV 30일 — 하루치 신규). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.06%·최근 3일 [0,0,0]). 노원키즈필라테스 최근 3일 [0,0,0]은 09-17 규칙대로 04번 행 유지.
01·06 min-width 2320 → 2400, 라벨 `[30, 30]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 채팅 원문에서 바로 파일로 저장해 썼다(09-23 교훈). 배포본 GET·배포 PUT은 첫 번째 토큰, 이 파일 push는 두 번째 토큰.
- **진행 경위**: 첫 응답에서 계산·교체·validate까지 마치고 도구 사용 한도에 걸려 배포 직전 멈춤 → 사용자 "계속" → 작업 파일이 남아 있어 재검증(14 PASS)·sha 재조회(c708134 그대로) 후 배포. 채팅 질문 5건은 답 없이 배포(아래 "요청한 값").
- **직전 산식 재현 먼저**: 키워드·검색어·상세지역 CSV를 `일별 <= 2026.09.23.`로 잘라 배포본에 validate → 13 PASS(시간대별만 9/24 포함이라 예상대로 FAIL 290 vs 280) 확인 뒤 새 값 계산.
- **9/24(추석 연휴 첫날) 노출 217·클릭 10·CTR 4.61%·광고비 13,868원** — 노출은 9/18(209) 이후 최저, 클릭·광고비는 전날(6건·7,838원)보다 늘어남. 플레이스 138회(9/18 108회 이후 최저)·9건·13,406원·CPC 1,490원·하루 CTR 6.52%, 파워링크 79회·1건(노원역필라테스 직접 등록 462원). 누적 CTR 3.07 → 3.11%, 검색 지면 3.80 → 3.83%(7,579·290). 연휴 영향은 "하루치로 한 방향이라 말하기 어려움"으로만 서술.
- **11번 판정**: 직전 7개 → 유지 4 · 뒤집힘 3 · 근거 소멸 0. 뒤집힘 ① 9/23 저점 → 9/24 클릭·광고비 반등 ② 확장·클릭0 이틀 연속 감소·어근 사흘 0 → 9/24 53 → 59회·어근 1회·32개 목록 재노출 ③ 플레이스 순위 사흘째 3위대·순위와 클릭 반대 움직임 → 9/24 2.98위, 순위 오른 날 클릭도 5 → 9건. 7개 + (참고) 2. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건.
- **12번 이월 판정**: 직전 2개 — 상시 유지 1(1번: 32개 재노출 발견) · 보류 유지 1(상계동 9/24 9회). 신규·철회 0. 번호 변동 없음.
- **플레이스 예산**: 상향 뒤 여드레(9/17~9/24) 평균 14,306원·9.5건·CPC 1,506원 → 재상정 조건 미충족.
- **파워링크**: 나흘 연속 클릭(9/21 3·9/22 3·9/23 1·9/24 1), 누적 58건·24,316원(7.5%). 노원산전 9/24 30회·클릭 0(9/22~ 사흘 0). 상계동 9/24 9회. CPC 격차 3.56 → 3.55배(회차마다 확대·축소 반복 — 이번엔 노원역 CPC 363 → 366원 상승 비율이 플레이스 1,294 → 1,301원보다 큼). 자동매칭 39 대 직접 19(17회차).
- **04번 예산 비중 최대잔여법**: 92.6 / 3.9 / 1.6 / 1.0 / 0.9. 플레이스 92.545%가 92.6으로 표시됨(보통 반올림 92.5, 합 99.9) — 02번 section-desc도 92.6%로 맞춤. 다음 회차 이 값을 오류로 올리지 말 것.
- **직전 회차 누락 정정 — 05번 mediaChart 5위.** 9/23까지 이미 "네이버 통합검색 PC"(파워링크) 510회가 "에펨코리아 모바일" 501회를 넘었는데 배포본(feed999)은 에펨코리아를 5위로 둔 채였다. 이번에 라벨·데이터·색(ink) 교체 [3673, 2253, 985, 828, 516], 11번 하단 판정 줄에 정정 사실 명기. **교훈: 매체 top5는 매 회차 `매체이름` 합계로 순위를 다시 세어 대조할 것 — validate.py 검사 대상이 아니라 조용히 남는다.**
- **07번**: 정식표 19행(필라테스노원역 2건 승격, 일치 8·유사 3 → 일치 뱃지) 263 + 클릭1건 22 + 경쟁사 5 = 290. 9/24 10건 전부 "일치"(필라테스 4·노원역필라테스 2(플레이스 1,667·파워링크 462)·노원필라테스 2·운동 1·필라테스노원역 1). 운동 4건이 노원시니어필라테스 4건과 동률 → 노출 많은 운동(206) 위. 근처필라테스 3/75 = **4.00%로 기준선에 정확히 걸려 `.ctr-high` 유지**(validate PASS). 클릭 0 전체 551개·1,829회(16회차 연속 증가, 경쟁사 포함 정의). 컴팩트 목록 동률은 직전 순서 유지.
- **08번**: TOP 10 구성 동일, 순서만 남양주시(143)가 중구(142)를 넘음. 의정부 114 vs 10위 영등포 124. 컴팩트 32개·73건(인천 영종구 신규, 중랑 6·종로 4·양주 4), 클릭 0 153개·1,131회. 노원 46%·50%, 타겟 62%·60%(노출 63 → 62), 확인불가 432·22·27,524원(8.4%, CTR 5.09%), 타겟 밖 서울 CTR 4.00% > 타겟 3.01%, 서울·경기 밖 비용 2.4 → 2.8%(인천 영종구 1,667원) → 전국 유지.
- **09·10번**: 15시 27회 14회차 연속, 2위 13시 21회 단독. 심야 1,956·64·58,638원(21%·22%), 9/24 10건 중 심야 3(0시 1·8시 2). 10번 A 7,448·288·325,025원 / B 131·2·1,158(9/24 0회, 사용자 결정대로 추적 문장 없음) / C 22 / D 1,724. B는 `기타 매체`의 검색 3회를 포함해야 131이 재현됨(검색 파트너 5개 매체만이면 128).
- **경쟁사**: 채택·config 변경 없음. 필라테스정원 표기 변형 "노원필라테스정원내돈내산" 행 추가 → 23행(정원 변형 9개·누적 18). 9/24 경쟁사명 노출 젠 2·오운·노원오프닝·노원필라테스정원 각 1, 클릭 0. 라임 종결, 09-23 1회짜리 보류 9개 종결, 아트(노원) 재등장 보류 유지, 필라테스안노원 1(종결 건 재등장). 신규 보류: 노원엠코필라테스(1)·**노원필라테스힐링정원내돈내산(1, 정원 변형인지 불분명 — 웹 검색 특정 불가, 채팅 확인 요청)**.
- **제외 검색어 대조(09-20 사용자 지시)**: ① 9/20 등록 17개: 9/21~9/24 "확장" 재노출 **0** ② 9/21 등록 22개: 9/22~9/24 **0** ③ **9/23 등록 32개: 판정 첫날 9/24 6개·11회 재노출**(노원역6번출구 4·노원역추석 3·노원역거리·노원구어린이·노원어린이체험·노원역키즈 각 1, 전부 클릭 0) → 채팅 보고·등록 그룹/칸 질문(17·22개는 다음 날부터 0이었던 것과 다름) ④ 9/24 등록 9개: 등록 당일, 9/24 확장 0회 — 9/25부터 판정 ⑤ 어근 조합 9/24 "노원역카페새로생긴" 1회(사흘 0 뒤) ⑥ **"노원역운동" 9/24 확장 1회**(일치 2는 대상 밖) → 채팅으로 9/17 등록분 제거 여부 질문 ⑦ 9/10 알려진 이름 재노출 0. 행 단위 확장·클릭0 9/24 59회(36개) = 파워링크 자동매칭 59회(노원산전 30·노원역 25·상계동 4)와 일치.
- **사용자에게 요청한 값(09-25 채팅, 답 없이 배포)**: ① 9/23 등록 32개의 등록 그룹·칸 ② "노원역운동" 9/17 등록분 제거 여부 ③ 9/24 첫 등장 무관·키즈 7개 등록(아래 대조 목록 표 "09-25 제안" 행) ④ 애매 4개(노원스텝핑 9회·노원역어깨·노원역쾌적한·노원역금호스) 판단 ⑤ "노원필라테스힐링정원내돈내산"이 필라테스정원 변형인지.
- **09-25 채팅 후속 — 재배포 `e29a3fc`(파일 sha af6a5c0 → becadb4), 14 PASS·재수령본 md5 일치(98cf78a7…)·360/390/430px 넘침 0.** 사용자 답 5건:
  ① **32개 = 파워링크 3개 그룹 "확장 검색" 칸에 전부 등록**(17·22·9개와 같은 위치). 위치는 맞는데 9/24 6개·11회 재노출 — 원인 미상으로 기록. 다음 회차에도 잡히면 "제외 검색어" 탭 목록(입력 창 카운터 아님 — 09-17 교훈)에 그 이름이 실제로 있는지 사용자에게 확인 요청. 등록 위치는 **다시 묻지 말 것**.
  ② **"노원역운동" = 제외 검색어로 등록돼 있지 않음**(사용자 답 "아니 제외 안했어" — 제외 목록에 없다는 뜻으로 해석, 채팅에서 해석 명시). 09-17~09-24 기록의 "9/17 개별 등록한 노원역운동"은 67개 원본이 없어 **추정이었고 틀렸음** — 이 절에서 정정(원문 보존). 9/24 확장 1회는 정상 노출, "운동" 계열 제외 안 함 결정과 일치. **더 대조하지 말고 다시 묻지 말 것.**
  ③·④ **9/24 첫 등장 11개 제외 결정**(무관·키즈 7 + 애매 4) — 메모장 파일(`제외검색어_추가_0925.txt`, 한 줄에 하나, CRLF)로 전달. 등록 위치는 파워링크 3개 그룹 "확장 검색" 칸으로 안내(11개 모두 "확장" 유형). **등록일 미수령** — 대조 목록 표 "09-25" 행에 원본, 등록 확인되면 등록일을 채우고 다음 날부터 대조.
  ⑤ **"노원필라테스힐링정원내돈내산" = 필라테스정원을 찾는 검색**(사용자 확인) → 07번 표 24행(정원 변형 10개·누적 19). config 변경 없음("필라테스정원" 이미 채택).
  07·11·12번의 "확인 중/기다림" 문구를 전부 결정 사실로 바꿈. 11번 판정 집계(유지 4·뒤집힘 3)는 그대로, 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건·항목 7 + (참고) 2.
- **09-25 채팅 후속 2 — 재배포 `036080a`(파일 sha becadb4 → 96c4a77), 14 PASS·재수령본 md5 일치(8e5871f9…).** 사용자가 11개를 **2026-09-25 13:13경 파워링크 3개 그룹에 등록 완료**(채팅에 목록 원본 재첨부, 대조 목록 표 09-25 행과 일치). 07·11·12번의 "등록 예정"을 "9/25 등록 완료, 9/26부터 판정"으로.
- 다음 회차 대조: 32개 재노출("확장" 행만, 9/25 이후 잡히면 제외 검색어 탭 목록 확인 요청) / 17·22개 0 유지 / 9개(9/25~) / 11개(9/26~) / 추석 연휴(9/25·9/26) 노출·클릭("가능성"으로만) / 파워링크 연속 클릭·노원산전 클릭 재개 / 누적 CTR 3.1%대 / 매체 top5 순위 재대조 / 의정부·영등포 TOP 10 / 상계동 30회 둘째 날 / 힐링정원·엠코·아트 재등장.

## 2026-09-24 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.23(29일), 계정 2580077(기간헤더 2026.08.25~09.23). 배포본 index.html 갱신·배포 완료.
배포 커밋 `4477d98`(직전 `e9b13fb`, 파일 sha 29c84d5 → 008e3db). 집계 기간 `2026.08.26 — 09.23 (29일)`.
validate.py 14개 검사 전부 PASS(실행 출력 [PASS] 줄 세어 14 — KPI 노출 9,108 / 클릭 280 / CTR 3.07% / 광고비 312,315원, 제외 전 전체 9,114 — 차이 6). 배포 후 재수령본 md5 동일(f4900fc5…)·14 PASS. playwright 360·390·430px scrollWidth = 뷰포트(넘침 0).
2-1단계 선확인 작동(배포본 28일 ≠ CSV 29일 — 하루치 신규). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.07%·최근 3일 [0,0,0]). 노원키즈필라테스 최근 3일 [0,0,0]은 09-17 규칙대로 04번 행 유지.
01·06 min-width 2240 → 2320, 라벨 `[29, 29]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 채팅 원문에서 바로 파일로 저장해 썼다(09-23 교훈). 배포는 첫 번째 토큰 PUT 200, 이 파일 push는 두 번째 토큰.
- **직전 산식 재현 먼저**: 키워드·검색어·상세지역 CSV를 `일별 <= 2026.09.22.`로 잘라 배포본에 validate → 13 PASS(시간대별만 9/23 포함이라 예상대로 FAIL 280 vs 274) 확인 뒤 새 값 계산.
- **이번 회차 최대 건 — 9/23 노출 248·클릭 6·CTR 2.42%·광고비 7,838원, 전날 최고치(17건·22,597원) 다음 날 클릭·광고비 모두 9/19 이후 최저.** 누적 CTR 3.09 → 3.07%(3% 위 유지), 검색 지면 3.85 → 3.80%. 9/23은 추석 연휴(9/24~9/26, 웹 검색으로 확인) 전날 — "가능성"으로만 서술. 플레이스 9/23 7,096원·5건(상향 뒤 두 번째로 적은 날), 상향 뒤 이레 평균 14,435원·9.6건·CPC 1,508원 → 재상정 조건 미충족(광고비도 함께 줄어 "광고비만 느는 날" 아님).
- **11번 판정**: 직전 8개 → 유지 8 · 뒤집힘 0 · 근거 소멸 0. 직전 "뒤집힘" 세 항목(파워링크 클릭 재개·순위 3위대·누적 CTR 3% 위)은 9/23에도 유지라 뒤집힘 표시를 떼고 유지로 옮김. 셋째 항목의 9/22 최고치는 9/23 하락과 합쳐 첫 항목. 8개 + (참고) 2. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건.
- **12번 이월 판정**: 직전 3개 — 상시 유지 1 · 진행 1(파트너 9/23 9회, 이레 연속, 문의 답변 5회차 대기) · 보류 유지 1(상계동 9/23 18회). 신규·철회 0. 번호 변동 없음.
- **파워링크**: 9/23 1건 = 상계동필라테스 직접 등록 742원(그룹 9/13 이후 첫 클릭, 누적 5건·3,323원) → 04번 행 순서가 노원키즈(3,023원)와 바뀜(비용 내림차순). 파워링크 누적 57건·23,854원(7.6%). 노원산전 9/23 29회로 30회 초과 사흘에서 멈춤, 클릭 이틀 0. CPC 격차 3.55 → 3.56배(한 회차 만에 다시 확대 — 노원역 363원 고정, 플레이스 1,291 → 1,294원).
- **04번 예산 비중 최대잔여법**: 92.4 / 3.9 / 1.6 / 1.1 / 1.0. 노원역 3.955%가 3.9로 표시됨(보통 반올림이면 4.0) — 합 100.0을 맞추는 규칙대로. 다음 회차 이 값을 오류로 올리지 말 것.
- **08번 TOP 10 교체**: 영등포구 114(9/23 +9)가 의정부시 110을 넘어 10위 진입(09-23 예고대로), 의정부시는 컴팩트 목록. 컴팩트 31개·69건(송파구 3 → 4), 클릭 0 154개·1,107회. 노원 46%·50%, 타겟 63%·60%, 확인불가 421·22·27,524원(8.8%, CTR 5.23%), 서울·경기 밖 비용 2.4% → 전국 유지. 9/23 송파구 1건(1,571원)은 "노원필라테스" 클릭과 금액이 같음(사실만). 컴팩트 목록 동률(마포구·광진구 55·3)은 직전 순서 유지.
- **07번**: 정식표 18행 252 + 클릭1건 23 + 경쟁사 5 = 280. 9/23 6건 전부 "일치"(필라테스 3·노원필라테스·마들역·상계동 각 1). 마들역 9건이 상계역 9건과 동률 → 노출 많은 마들역(301)이 위로. 근처필라테스 CTR 4.05%로 `.ctr-high` 유지. 클릭 0 전체 532개·1,776회(15회차 연속 증가). 필라테스노원 일치 13·확장 13 동률 → 직전 뱃지(확장) 유지.
- **경쟁사**: 채택·config 변경 없음. **필라테스인 표기 변형 "필라테스인노원내돈내산"(9/23 확장 1) 행 추가 → 14행.** 9/23 경쟁사명 클릭 0(와우 5·필라테스인노원 2·젠 1·오운 1회). 필라테스정원 계열 9/23 0(누적 16, 채팅 확인 대기). 종결 건 재등장: 필라테스고요노원 2(고요 계열 누적 7)·노원역필라테스안 1·노원필라테스안 1(필라테스안 계열 누적 4) → 종결 유지.
- **제외 검색어 대조(09-20 사용자 지시)**: ① 9/20 등록 17개: 9/21~9/23 "확장" 재노출 **0** ② 9/21 등록 22개: 9/22·9/23 재노출 **0** ③ 어근 조합 사흘 연속 **0** ④ 노원역운동 9/23 2회 전부 **"일치"** → 대상 밖(확장 0) ⑤ 9/10·9/17 알려진 이름 재노출 0. **09-23 제안 32개는 등록 여부 미수령** — 그중 6개(노원역9번출구 2·노원역+9번출구 2·노원역2번출구 2·노원역6번출구·노원역거리·노원역추석 각 1)가 9/23 확장 9회. 등록했다면 등록 당일이라 판정 안 함. 행 단위 확장·클릭0 9/23 53회(26개, "새로필라테스" 22 대상 아님). 9/23 첫 등장 14개 중 무관 3·키즈 3 = 추가 6개(위 대조 목록 표에 "09-24 제안" 행으로 원본 보관), 애매 3개는 사용자 판단 요청.
- **09·10번**: 15시 24회 13회차 연속, 2위 9·13·14시 각 20. 심야 1,913·61·55,892원(21%·22%), 9/23 6건 중 심야 2(6시·22시). 파트너 매체 9/23 9회(노원역 7: 다음-모바일 4·네이트-PC 2·Bing-PC 1 / 새로 2: 다음-모바일), 9/6 이후 100회·누적 131·클릭 2·1,158원, 그룹 누적 노원역 66·새로 43·산전 11·상계동 6·키즈 5.
- **사용자에게 요청한 값(09-24 채팅)**: ① 09-23 추가 목록 32개 등록 여부·등록일(+이번 6개) ② 네이버 문의 답변(12번 2번, 5회차) ③ "운동" 계열 제외 여부 ④ 필라테스정원 계열 소재지 ⑤ 애매 3개(노원아기랑필라테스·노원새로필라테스경력·노원역다인원) 판단.
- **09-24 채팅 후속 — 재배포 `8b738d7`(파일 sha 008e3db → 1473547), 14 PASS·재수령본 md5 일치(b1b068dc…)·360/390/430px 넘침 0.** 사용자 답 5건:
  ① **09-23 추가 목록 32개 = 9/23 등록 완료** → 대조 시작 9/24(대조 목록 표 갱신). 등록 위치는 따로 말하지 않았고 제안 위치(파워링크 확장 칸)로 기록.
  ② **플레이스 제외 검색어 칸 가득 참.** 새 후보 6개가 파워링크에서 나왔는지 물음 → 9개 전부 "확장" = 파워링크 자동매칭(위 대조 규칙 근거)이라 파워링크 그룹에 등록하면 된다고 답함. 애매 3개(노원아기랑필라테스·노원새로필라테스경력·노원역다인원)는 **사용자 결정으로 제외** → 새 목록 9개(대조 목록 표 "09-24 제안" 행). 등록일 미수령.
  ③ **"운동" 계열 = 제외하지 않음**(사용자 답 "아니 포함 시키자" — 제외 안 하고 노출 유지로 해석, 채팅에서 해석을 명시함). 창동역·마들역·상계역·노원구·노원시니어·노원그룹운동. **다시 묻지 말 것.** 9/17에 이미 등록된 "노원역운동"과 방향이 어긋난다는 점은 채팅에서 한 줄로 알림(빼는 건 사용자 몫).
  ④ **필라테스정원 = 노원 소재 → 경쟁사 채택.** config `competitors` 9 → 10개, 07번 표에 변형 8행(노원필라테스정원 4·필라테스정원노원 4·노원정원필라테스 3·노원구정원필라테스·노원구필라테스정원·노원역필라테스정원·필라테스정원노원점·필라테스정원노원점가격 각 1, 전부 확장·클릭 0) → 22행. 07 각주·11번 (참고)·12번 각주 갱신. 클릭 0 목록(≥5)에는 해당 없음, 클릭 합계 불변.
  ⑤ **파트너 매체: 네이버 답변 안 옴, "오면 내가 말해줄게, 아예 제껴줘"** → 12번 2번 **철회**(사유 각주), 11번 해당 항목 삭제(7개 + 참고 2), 10번 section-desc·note에서 추적 문장 제거하고 한 줄만 남김(표의 수치 행은 유지). **사용자가 답변을 전하기 전까지 12번·11번에 다시 올리지 말고 채팅으로도 묻지 말 것.** 12번은 1~2번으로 재번호(2번 = 상계동), 06·11번 참조 번호 수정.
- **09-24 채팅 후속 2 — 재배포 `feed999`(파일 sha 1473547 → c708134), 14 PASS·재수령본 md5 일치(931c1738…).** 사용자가 새 목록 9개를 **파워링크 3개 그룹 "확장 검색" 칸에 등록 완료**(09-24). 12번 1번 제목·본문·판정 ②, 07번 클릭0 각주, 11번 (참고) 1을 "9/24 등록 완료, 9/25부터 판정"으로. 대조 목록 표 09-24 행 등록 확정.
- 다음 회차 대조: 17개·22개·**32개(9/24~)**·**9개(9/25~)** 재노출("확장" 행만) / (파트너 매체는 사용자 보고 전까지 추적 안 함) / 9/24~9/26 추석 연휴 기간 노출·클릭(연휴 영향 서술은 "가능성"으로만) / 파트너 매체 하루 10회 이상·문의 답변 / 상계동 30회 둘째 날·클릭 지속 / 노원산전 30회대 복귀 여부 / 누적 CTR 3% 유지 / 의정부·영등포 TOP 10 재교체 / 필라테스정원·라임·1회짜리 보류 후보 재등장.

## 2026-09-23 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.22(28일), 계정 2580077(기간헤더 2026.08.24~09.22). 배포본 index.html 갱신·배포 완료.
배포 커밋 `bd82f57`(직전 `14be19c`, 파일 sha 17151d9 → 4011ae9). 집계 기간 `2026.08.26 — 09.22 (28일)`.
validate.py 14개 검사 전부 PASS(실행 출력 [PASS] 줄 세어 14 — KPI 노출 8,860 / 클릭 274 / CTR 3.09% / 광고비 304,477원, 제외 전 전체 8,866 — 차이 6). 배포 후 재수령본 md5 동일(118172ef…)·14 PASS.
2-1단계 선확인 작동(배포본 26일 ≠ CSV 28일 — 이틀치 신규). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.07%·최근 3일 [0,0,0]). 노원키즈필라테스 최근 3일 [0,0,0]은 09-17 규칙(OFF 결정 그룹, `excluded_groups`에 넣지 않음)대로 04번 행 유지.
01·06 min-width 2080 → 2240, 라벨 `[28, 28]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 배포는 첫 번째 토큰으로 PUT 성공, 이 파일 push는 두 번째 토큰(직전 회차와 같은 방식). 배포본 읽기도 첫 번째 토큰 GET.
- **직전 산식 재현 먼저**: 키워드·검색어·상세지역 CSV를 `일별 <= 2026.09.20.`로 잘라 배포본에 validate를 돌려 13개 PASS(시간대별만 9/22 포함이라 예상대로 FAIL 274 vs 246)를 확인한 뒤 새 값을 계산했다. 계산 스크립트는 회차 작업 디렉토리에만 둠.
- **이번 회차 최대 건 — 9/22 클릭 17건·광고비 22,597원, 둘 다 개업 이후 하루 최고(종전 9/17 15건·20,773원).** 9/21·9/22 노출 318회 이틀 연속(9/9 350회 이후 최다). 누적 CTR 2.99 → 3.09%(3% 위 복귀, 9/17 3.01% 이후 두 번째), 검색 지면 3.80 → 3.85%. 플레이스 9/22 21,314원·14건(9/17 14건과 하루 최다 동률)으로 9/17 이후 두 번째 2만원대 — 상향 뒤 엿새 평균 15,658원·10.3건·CPC 1,515원, 지난 회차 완료 건의 재상정 조건(7건대·CPC 1,600원 초과) 미충족 → ✓ 행은 표에서 뺐고 01·04번에 유지 결론만 기록.
- **뒤집힘 3건(11번 맨 위)**: ① 파워링크 이틀 연속 클릭 0 → 9/21·9/22 각 3건(9/21 산전 자동 1·노원역 자동 2, 9/22 노원역 자동 2·직접 1). 누적 50 → 56·23,112원(7.6%) ② 플레이스 순위 2.35위 이틀 연속 → 9/21 3.11·9/22 3.61위(누적 3.03 → 3.05). 9/22는 닷새 중 최저 순위인데 플레이스 클릭 14건 최다 — 9/17·9/18 패턴 재현 ③ 누적 CTR 3% 아래 이틀째 → 3.09%. 판정: 직전 8개 → 유지 5 · 뒤집힘 3 · 근거 소멸 0. 8개 + (참고) 2. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건.
- **CPC 격차 3.58 → 3.55배 — 네 회차 연속 확대 뒤 첫 축소.** 노원역필라테스 이틀 5건 평균 424원(835+1,283원)이 누적 CPC 353 → 363원으로 올려 플레이스(1,263 → 1,291원)보다 상승폭이 컸음. "변화 없음" 줄에 방향 전환 명기.
- **노원산전필라테스**: 9/21 노출 47회 등록 이후 하루 최다(종전 9/20 33회)·클릭 1(닷새 연속 0 끊김), 9/22 44회·0. 사흘 연속 30회 초과. 하루 평균 15.5 → 18.3. 누적 10건. 12번 항목 아님(06번 기록).
- **파트너 매체: 9/21 13회 — 9/6 이후 하루 최다(종전 9/16 7회), 9/22 8회.** 9/6 이후 91회, 누적 122·2건·1,158원. 이틀 21회 중 14회가 플레이스 그룹(새로 다음-PC 4+3·다음-모바일 4+3), 나머지 노원역 다음-모바일 4+1·네이트PC 1·상계동 네이트PC 1. 그룹별 누적 노원역 59·새로 27 → 41·산전 11·상계동 6·키즈 5. 재설정(9/17) 뒤 엿새 연속. 문의 답변 미확인 → 12번 2번 진행 유지, 판정 조건에 "하루 10회 이상 이어지면 문의에 추가" 한 줄.
- **매체 top5 순서 변동**: 네이버 플레이스-PC 914회가 MLB파크-모바일 828회를 넘어 3위로 — 05번 mediaChart 라벨·데이터 순서 재배열(색은 전부 플레이스=민트라 그대로).
- **제외 검색어(12번 1번 상시) — 사용자 지시(09-20) 대조 결과**: ① 9/20 등록 17개: 9/21·9/22 "확장" 행 재노출 **0** ② 9/21 등록 22개: 9/22 "확장" 행 재노출 **0**(등록 당일 9/21 노원구아기랑 3·노원역오꼬 1 — 보고만) ③ 어근 조합(맛집·카페·우동) 9/20 9회 → 9/21·9/22 **0회**(등록 뒤 처음 이틀 연속 0) ④ 9/17 등록분 **"노원역운동" 9/21 확장 1회 재노출**(9/18·9/19에 이어 세 번째) → 채팅 보고·추가 목록에 다시 넣음 ⑤ 9/10 등록분 재노출 0. 행 단위 확장·클릭0 9/21 **95회(49개, 개업 이후 최다 9/9 95회와 타이 — "노원역9번출구" 22회)**·9/22 73회(43개). 키즈 계열 9/21 5·9/22 5회(새 이름 6개: 노원역아기·아기랑노원구·노원구어린이·노원구어린이체험·노원어린이체험·노원역키즈). 9/21·9/22 첫 등장 무관 검색어 + 키즈 새 이름 + "노원역배스킨라빈스"(9/21 등록분은 "베스킨" 표기라 다른 문자열) = **추가 목록 32개** 채팅 전달(아래 대조 목록 표에 "제안·미등록" 행으로 원본 보관 — 사용자 등록 확인되면 등록일을 채울 것). "운동" 계열(창동역운동 33·마들역운동 11·상계역운동 10·노원구운동 8·노원시니어운동 9·노원그룹운동 7)은 잠재고객 가능성이 있어 목록에 넣지 않고 채팅에서 사용자 판단으로 물음.
- **08번**: TOP 10 구성·순서 동일. 영등포구(105·3, 9/21 1·9/22 2) 첫 클릭으로 컴팩트 목록 진입, 노출은 10위 의정부(107)에 2회 차 — 다음 회차 교체 가능. 컴팩트 31개·69건, 클릭 0 154개·1,069회. 노원 46%·49%, 타겟 63%·60%(이틀 28건 중 타겟 15·밖 13). 확인불가 412·22·27,524원(9.0%, CTR 5.34%). 타겟 밖 서울 CTR 3.97% > 타겟 2.96%, 서울·경기 밖 비용 2.5% → 전국 유지. 광주 북구 2건(각 462원)은 07번 "노원역새로필라테스" 확장 클릭 2건과 날짜·금액이 같음(사실만 기록, 해석 안 함).
- **07번**: 정식표 18행(노원역새로필라테스 3회·2건 승격) 246 + 클릭1건 23(은행사거리필라테스 19회 첫 클릭·노원그룹필라테스추천·노원시니어헬스 신규) + 경쟁사 5 = 274. 이틀 28건 중 일치 23. 필라테스 8·노원역필라테스 5·노원필라테스 4. 상위 2개 46%. 클릭 0 전체 518개·1,733회(14회차 연속 증가). "필라테스노원"은 일치 12·확장 12 동률이라 배포본 뱃지(확장) 유지 — 동률 시 직전 뱃지 유지로 처리.
- **09번**: 15시 24회(12회차 연속), 2위 9시·13시 각 20회 동률. 심야 1,869·59·53,208원(21%·22%), 이틀 28건 중 심야 6건, 20~21시 9건.
- **경쟁사**: 채택·config 변경 없음. 젠 66 → 72·클릭 1 → 2, 와우 15 → 19·클릭 1 → 2(둘 다 9/22 1건씩 — 하루 경쟁사명 클릭 2건은 처음, 3,519원), 노원필라테스인 4 → 7, 필라테스인노원 16, 오운 14. **와우 표기 변형 2행 추가**(필라테스노원와우점 9/21 1·노원와우필라테스비추첰 9/22 1 — 후자는 비추천 후기 검색으로 보임, 표에 그대로) → 13행. 종결 4(INTOPILATES·필라테스안·노원니드·필라테스호). **종결 건 "필라테스정원" 계열 이틀 7회(누적 16, 변형 8개)** — 웹 검색(필라테스정원 노원) 특정 불가 → 표 미등재·채팅 확인 요청. 라임필라테스 2회(일치, 9/22) 보류·미언급. 노원M 9/21 확장 1(누적 6·클릭 1)·재활엠필라테스노원 9/22 1 — 표 미복귀 유지.
- **12번 이월 판정**: 직전 4개 전부 — 상시 유지 1 · 표에서 제거 1(✓ 플레이스 예산) · 진행 1(파트너) · 보류 유지 1(상계동 9/21 20·9/22 28, 30회 초과는 9/18 하루). 신규·철회 0. 항목 3개, 번호 1~3 재정렬(2번 = 파트너, 3번 = 상계동). 06·11번의 "12번 N번" 참조 전부 새 번호로.
- **사용자에게 요청한 값(09-23 채팅)**: ① 네이버 문의 답변(12번 2번, 4회차 대기) ② 추가 목록 32개 등록 여부 ③ "운동" 계열 6개 제외 여부(사용자 판단) ④ 필라테스정원 계열 소재지(재상정 여부) ⑤ 노원역운동 등록 상태(9/17 등록분인데 세 번째 재노출 — 추가 목록에 다시 넣었으니 등록되면 종결).
- **09-23 채팅 후속 — 10번 가로 넘침 수정(레이아웃만, 숫자 변경 없음).** 사용자 스크린샷: 10번 note의 17일 노출 나열 `216·242·…·318회`가 카드 밖으로 나가 페이지 전체 좌우 스크롤 발생. playwright 390px 실측 scrollWidth 418 → 수정 후 390(360·430px도 넘침 0). 수정 2곳: `body{overflow-wrap:anywhere}` 안전망 + 10번 두 나열의 `·` 뒤 `<wbr>`. 태그 짝·섹션 주석 자체 검사 통과(CSV 없어 validate.py 전체는 미실행 — 검사 대상 태그·숫자를 건드리지 않음). 상세는 css-and-layout.md 버그 기록 10. **배포 토큰 주의: 이번에 받은 토큰 하나는 스킬 저장소(saero-ad-report-skill) 권한이라 배포 PUT이 403** — `git push --dry-run`으로 두 저장소 권한을 구분했다(스킬 저장소만 push 가능). 배포 커밋은 아래 줄에.
- 배포 커밋 `e9b13fb`(파일 sha 4011ae9 → 29c84d5). 재수령본 md5 일치·390px scrollWidth 390 재확인. 토큰은 두 번째 메시지로 두 개 받아 dry-run으로 구분(첫 번째 = 배포, 두 번째 = 스킬). **첫 메시지 토큰의 401은 폐기가 아니라 Claude가 옮겨 적다 틀린 것**(`rxkT5UBY`를 `rxkr0BU`로) — 토큰은 채팅에서 파일로 바로 저장해 쓰고, 다시 타이핑하지 말 것.
- 다음 회차 대조: 17개·22개·(등록 시) 32개 재노출 → "확장" 행만, 잡히면 채팅 보고 / 어근 조합 0 유지 여부 / 노원역운동 / 파트너 매체 하루 10회 이상 지속·문의 답변 / 파워링크 클릭 지속·노원산전 30회대 노출에 클릭 따라오는지 / 플레이스 순위 3.6위대 지속 여부 / 누적 CTR 3% 유지 / 영등포구 vs 의정부 TOP 10 교체 / 상계동 30회 둘째 날 / 필라테스정원·라임 재등장 / 젠·와우 클릭 추가.

## 2026-09-21 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.20(26일), 계정 2580077(기간헤더 2026.08.22~09.20). 배포본 index.html 갱신·배포 완료.
배포 커밋 `fd7d73c`(직전 `0b81917`, 파일 sha 9be19a9 → 4b795e6). 집계 기간 `2026.08.26 — 09.20 (26일)`.
validate.py 14개 검사 전부 PASS(실행 출력 [PASS] 줄 세어 14 — KPI 노출 8,224 / 클릭 246 / CTR 2.99% / 광고비 268,170원, 제외 전 전체 8,230 — 차이 6). 배포 후 재수령본 md5 동일(03bd9d06…)·14 PASS.
2-1단계 선확인 작동(배포본 25일 ≠ CSV 26일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.07%·최근 3일 [0,0,0]). 노원키즈필라테스 최근 3일 [0,0,0]은 자동감지 조건 해당이지만 09-17 규칙(OFF 결정 그룹, `excluded_groups`에 넣지 않음)대로 04번 행 유지.
01·06 min-width 2000 → 2080, 라벨 `[26, 26]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 배포는 첫 번째 토큰으로 PUT 성공, 이 파일 push는 두 번째 토큰(직전 회차와 같은 방식). 무인증 GET은 api.github.com에서 403이 나서 읽기도 첫 번째 토큰으로 했다.
- **직전 산식 재현 먼저**: 키워드·검색어·상세지역 CSV를 `일별 <= 2026.09.19.`로 잘라 배포본에 validate를 돌려 13개 PASS(시간대별만 9/20 포함이라 예상대로 FAIL 246 vs 236)를 확인한 뒤 새 값을 계산했다. 계산 스크립트는 회차 작업 디렉토리에만 둠.
- **사용자가 "계속"만 보내 채팅 질문 5건에 답 없이 배포** — 문의 답변·노원역체험 등록 여부·추가 목록 등록·노원부티 소재지·산전산후 운영 여부는 전부 "대기"로 기록. 답이 오면 재배포.
- **이번 회차 최대 건 — 플레이스 일예산 상향(9/17) 나흘 판정 종료 → 12번 2번 ✓ 완료(상향 유지).** 9/17~9/20 하루 평균 15,041원·클릭 10.0건·CPC 1,504원 vs 상향 전 9/1~9/16 9,658원·7.2건·1,344원. 09-20에 건 조건(클릭 증가 지속 + CPC 1,600원 아래) 충족. 재상정 조건: 하루 클릭 7건대로 돌아온 채 광고비만 느는 날 사흘 이상 또는 CPC 1,600원 초과 지속. **다음 회차에 ✓ 행을 표에서 빼고, "원인 미상"이나 "예산 소진 여부"로 다시 올리지 말 것.**
- **12번 3번(지역 설정 전국)은 09-20 지시대로 표에서 제거**, 번호를 1~4로 재정렬(3번 = 파트너 매체, 4번 = 상계동). 06·10·11번의 "12번 N번" 참조를 전부 새 번호로 바꿈. 08번에 재상정 조건 대조 기록(서울·경기 밖 비용 2.3%·타겟 밖 서울 CTR 4.04% > 타겟 2.87% → 유지).
- 9/20 하루: 노출 293·클릭 10·CTR 3.41%·광고비 14,951원(전부 플레이스, CPC 1,495원). 플레이스 순위 2.35위(9/6 이후 최고, 9/19 2.43위에 이어 이틀 연속) — 누적 가중 3.06 → 3.03위. 01번 순위 그리드 강조는 9/20에.
- **파워링크 9/19·9/20 이틀 연속 클릭 0(9/2 이후 세 번째 0클릭일, 이틀 연속은 처음).** 9/20 노출 88(노원역 43·산전 33·상계동 12). 누적 50건·20,590원, 비중 8.1 → 7.7%. 노원산전 9/20 33회는 등록 이후 하루 최다(종전 9/4 30회)인데 9/16~9/20 닷새 연속 클릭 0(순위 1.80 → 1.74위). 12번 항목으로 올리지 않음(예산은 09-17 사용자 결정, 비용 증가 없음) — 각주에 "사흘 이상 이어지면 다시 봄"으로 조건만 걸어둠.
- **파트너 매체**: 9/20 2회(노원산전 Bing-PC 1·노원역 네이트검색-PC 1 — 이번엔 다음이 아니라 Bing·네이트 PC). 9/6 이후 70회, 누적 101·2건·1,158원. 그룹별 누적 노원역 53·새로 27·산전 11·키즈 5·상계동 5. 문의 답변 미확인 → 12번 3번 진행 유지.
- **제외 검색어(12번 1번 상시)**: 행 단위 확장·클릭0 9/20 59회(42개; 9/16 67 → 69 → 59 → 61 → 59). **9/20 등록 17개는 등록 당일이라 판정 안 함** — 당일 확장 노출 시니어필라테스복 1·노원역맛집내돈내산 1(보고만). **9/17 등록분 "노원역체험" 9/18에 이어 9/20 확장 1회 재노출 → 채팅 보고(등록 여부 확인 요청)**. 노원역운동·헬스·데이트 0, 우동짜장·세차·출발 0, 9/10 등록분 재노출 0. 어근 조합 9/19 5 → 9/20 9회(노원역역맛집 2 등, 전부 새 조합). 키즈 계열 12 → 7회(노원구아기랑 4·노원역아이랑 2·노원역아이와체험 1). 9/20 첫 등장 23개 중 무관 검색어 + 키즈 3개 + 노원역체험을 **추가 등록 목록 22개**로 채팅 전달(아래 대조 목록 표에 추가). 사용자 등록 확인은 미수령.
- **08번**: TOP 10 구성·순서 동일. 성동구 100회가 의정부시 100회와 동률이 됐지만 순서 유지(의정부 TOP 10, 성동구 컴팩트 목록) — 다음 회차에 성동구가 넘으면 교체. 컴팩트 26개·58건, 클릭 0 158개·1,107회. 노원 46%·49%(클릭 비중 47 → 49), 타겟 63%·61%. 확인불가 373·21·25,901원(9.7%, CTR 5.63%).
- **07번**: 정식표 17행 223 + 클릭1건 20 + 경쟁사 3 = 246. 9/20 클릭 10건 전부 "일치"(필라테스 6·9,161원 = 한 검색어 하루 최다, 종전 9/18 5건). 근처필라테스 3건·4.92% → `.ctr-high` 신규. 상계필라테스(40회) 첫 클릭으로 클릭 0 목록 → 클릭 1건 목록(50개 ↔ 20개). 클릭 0 전체 466개·1,588회(경쟁사 포함 정의 유지). 경쟁사 표는 와우 13 → 15로 필라테스인노원(15)과 동률 → 클릭 1건 있는 와우를 앞에(정렬: 노출 내림차순, 동률이면 클릭 내림차순 — 퍼스트아카데미노원 1/1도 퍼스트 1/0 앞으로).
- **11번 판정**: 직전 7개 → 유지 7 · 뒤집힘 0 · 근거 소멸 0. 신규 1(플레이스 순위 2.35위 이틀 연속). 8개 + (참고) 2. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건. "변화 없음" 줄: 2위 시간대 16시 17회 → 9시 19회(9/20 9시 3건)로 자리 바뀜 명기.
- **12번 이월 판정**: 직전 5개 전부 — 상시 유지 1 · **완료 1**(플레이스 예산) · 표에서 제거 1(지역 설정, 09-20 완료 건) · 진행 1(파트너 매체) · 보류 유지 1(상계동 9/20 12회, 9/14 이후 최저). 신규·철회 0. 항목 4개(✓ 1 포함).
- 주요 숫자 이동: CPC 격차 3.54 → 3.58배(네 회차 연속 확대 — 플레이스 1,251 → 1,263원, 노원역 353원 고정) / 플레이스 92.3%(247,580원) / 모바일 81.0% / 15시 22회 11회차 연속 / 심야 1,726·53·46,229원(21%·22%, 9/20 10건 중 3건 22·23시) / 자동매칭 34 대 16(14회차, 노출 934 대 1,577·자동 순위 2.1 → 2.0위) / 콘텐츠 1,746 11회차 연속 동일, 9/6~9/20 15일 0 / 검색 지면 누적 CTR 3.82 → 3.80%.
- 경쟁사: **신규 채택 1 — "부티필라테스"**(config `competitors` 8 → 9개, 아래 이력 표 참고). 첫 배포 시점엔 웹 검색(부티필라테스 노원) 소재지 특정 불가로 보류·채팅 확인 요청했고, 같은 회차 사장님 답으로 채택해 재배포. "노원니드필라테스"·"필라테스호"(각 1회)는 1회짜리 보류(리포트 미언급, 웹 검색 특정 불가). 유진필라테스 9/20 추가 0 → 종결. INTOPILATES 9/20 1회(누적 2) → 보류 유지. 필라테스안 9/20 0 → 보류 유지(2회차 연속 0이면 종결).
- **사용자에게 요청한 값(09-21 채팅)**: ① 네이버 문의 답변 — **아직 안 옴**(12번 3번 답변 대기 유지) ② "노원역체험" 등록 여부 — 09-21 추가 목록에 포함해 **재등록 완료**로 종결(9/17 등록분에 있었는지는 확인 안 됐고 이제 무의미) ③ 추가 목록 22개 — **09-21 등록 완료**(사용자 입력 23개, 노원역체험 중복). 대조 시작 9/22 ④ **노원부티필라테스 = "매장 근처 필라테스" → 경쟁사 채택**(위 이력 표·config·화면 3곳 같은 회차 갱신) ⑤ **산전·산후·임산부 수업 운영 중** → 노원산후·노원임산부·노원역산후·노원구산전 계열 검색어는 제외 대상 아님. 12번 1번에 명기. **다시 묻지 말 것.**
- **09-21 채팅 후속 — 재배포 `acac2d3`(파일 sha 4b795e6 → 72add0d), 14 PASS·재수령본 md5 일치(56ffa757…).** 07번 경쟁사 표 11행(부티 3·0·0원, 노원필라테스인 다음 자리)·각주, 11번 (참고) 2·판정 문단, 12번 1번(산전·산후 운영 확인)·각주 갱신. 다른 섹션 변경 없음.
- **09-21 채팅 후속 2 — 재배포 `14be19c`(파일 sha 72add0d → 17151d9), 14 PASS·재수령본 md5 일치.** 사용자가 22개(입력 23개)를 파워링크 제외 검색어로 **등록 완료**. 12번 1번 제목·본문·판정 조건 ②를 "9/22 이후 확장 행 재노출 → 채팅 보고"로, 11번 6번 항목·07번 각주도 "등록 완료(9/21)"로. 상단 "등록 제외 검색어 대조 목록" 표의 09-21 행을 등록 확정으로 고침.
- 다음 회차 대조: **9/21 이후 "확장" 행에서 9/20 등록 17개 재노출, 9/22 이후 9/21 등록 22개 재노출 → 잡히면 이름·날짜·노출수 채팅 보고(사용자 지시)** / 12번 ✓ 2번 행 제거 / 파워링크 클릭 재개(사흘 연속 0이면 노출·순위와 같이 봄)·노원산전 연속 0 / 파트너 매체 노출·문의 답변 / 누적 CTR 3% 재진입 / 플레이스 순위 2.3위대 지속 여부 / 상계동 하루 30회 둘째 날 / 성동구·의정부 100회 동률 → TOP 10 교체 여부 / 서울·경기 밖 비용 5% 선 / 노원부티·INTOPILATES·필라테스안·니드·필라테스호 재등장 / 산전·산후 답 받으면 임산부·산후 계열 검색어 제외 후보 전환.

## 2026-09-20 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.19(25일), 계정 2580077(기간헤더 2026.08.21~09.19). 배포본 index.html 갱신·배포 완료.
배포 커밋 `e20b984`(직전 `f0d3756`, 파일 sha f0be44f → 947640d). 집계 기간 `2026.08.26 — 09.19 (25일)`.
validate.py 14개 검사 전부 PASS(실행 출력 [PASS] 줄 세어 14 — KPI 노출 7,931 / 클릭 236 / CTR 2.98% / 광고비 253,219원, 제외 전 전체 7,937 — 차이 6). 배포 후 재수령본 md5 동일(eedc08b7…)·14 PASS.
2-1단계 선확인 작동(배포본 24일 ≠ CSV 25일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.08%·최근 3일 [0,0,0]). 노원키즈필라테스 최근 3일 [1,0,0]은 자동감지 조건 미해당이고 09-17 규칙대로 `excluded_groups`에 넣지 않음.
01·06 min-width 1920 → 2000, 라벨 `[25, 25]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 배포는 첫 번째 토큰으로 PUT 성공, 이 파일 push는 두 번째 토큰(직전 회차와 같은 방식).
- **직전 산식 재현 먼저**: 키워드·검색어·상세지역 CSV를 `일별 <= 2026.09.18.`로 잘라 배포본에 validate를 돌려 13개 PASS(시간대별만 9/19 포함이라 예상대로 FAIL) + KPI·01·02·04·05·06·07·08·10 값이 배포본과 같게 나오는 것을 확인한 뒤 새 값을 계산했다. 계산 스크립트는 회차 작업 디렉토리에만 둠.
- **이번 회차 최대 건 — 9/19 하루 클릭 4건(개업 당일 제외 최저, 종전 8/29 6건)·CTR 1.78%(검색 지면만 남은 9/6 이후 최저, 종전 9/16 2.68%)·광고비 6,443원(8/29 5,092원 이후 최저, 전부 플레이스).** 9/17 플레이스 일예산 2만원 상향 셋째 날 소진 없음. 같은 날 플레이스 가중순위 2.43위(9/6 이후 최고)·노출 139회(전날 108)인데 클릭 감소 → 01·04·11번에 "예산은 하루 상한, 광고비는 그날 클릭 수를 따라 움직이는 것으로 보임"으로 서술(단정 안 함). 09-19 지시대로 "원인 미상"으로 재상정하지 않음.
  12번 2번 판정: 걸어둔 닫는 조건("9/16 이전 수준 8,000~13,000원으로 돌아오면 닫음")을 하루째 충족(그 범위보다도 낮음)했으나 하루치라 **진행 유지·한 회차 더 봄**. 새 판정 조건: 9/20 이후 2만원 근처 소진일이 다시 나오면 유지(클릭 10건·CPC 1,600원 함께) / 8,000~13,000원 이하가 이어지면 9/17·9/18 이틀치 현상으로 닫음. 상향 전 일예산 값 여전히 미수령.
- **누적 CTR 3.01 → 2.98%(하루 만에 다시 3% 아래)**, 검색 지면 누적 3.89 → 3.82%(3.8%대 유지). 11번 1번을 뒤집힘으로 올림(9/17·9/18 "노출 감소·클릭 최다" → 9/19 노출 225 반등·클릭 4).
- **파워링크 9/19 클릭 0건 — 9/2 이후 두 번째 0클릭일**(노출 86: 노원역 47·상계동 24·산전 15). 누적 50건·20,590원 그대로, 비중 8.3 → 8.1%. 하루치이고 예산은 09-17 사용자 결정(현행 유지)이라 12번 항목으로 올리지 않음(12번 각주에 이유 명시).
- **파트너 매체**: 9/19 3회(노원역 2·새로 1, 전부 다음-모바일). 9/6 이후 68회, 누적 99·2건·1,158원. 그룹별 누적 노원역 52·새로 27·산전 10·키즈 5·상계동 5. 네이버 문의 접수·답변 미수령 → 12번 4번 진행 유지. 닫는 조건을 "답변 전이라도 0인 날이 이어지면 닫음"으로 명확히 함.
- **제외 검색어(12번 1번 상시)**: 행 단위 확장·클릭0 9/19 61회(41개; 9/15 33 → 9/16 67 → 9/17 69 → 9/18 59 → 9/19 61). **8/26~9/16에 이미 잡혔던 무관 검색어 노원역우동짜장(첫 9/6, 9/17~9/19 사흘 연속 1회)·노원역세차(첫 9/3)·노원역출발(첫 9/9)이 9/19 재노출** — 9/17 등록한 개별 67개·79개 목록 원본이 저장소에 없어 포함 여부 대조 불가 → 채팅으로 확인 요청. 어근 조합 9/18 10 → 9/19 5(노원역맛집내돈내산·노원역우동짜장·노원역뷰카페·노원역7번출구카페·노원카페뷰). 키즈 계열 9/19 12회(노원구아기랑 7·노원역아기랑 3·노원구아기 1·노원키즈필라테스 1). 9/10 등록분(노원역카페 35·나다운 57·수정역 7·새로오픈 18) 누적 불변 = 재노출 0 유지.
  **판정 주의(신규)**: 개별 등록한 "노원역운동"이 9/19 4회 잡혔으나 3회가 검색 유형 "일치"다. 제외 검색어는 파워링크 4그룹에만 등록돼 있어(09-10 계정 조치 기록) 플레이스 쪽 "일치" 노출은 제외 대상 밖이다. **등록 효과 판정은 "확장" 행만으로 할 것** — 누적만 보고 "등록 뒤에도 잡힌다"고 쓰면 틀린다.
- **노원키즈필라테스**: 9/18·9/19 노출 0 확정 → 09-19에 정한 대로 06번 카드 제거(04번 행 "(9/2 등록 · 9/17 OFF)"는 유지, 07번 우측 ✓ 문구는 "04번 참고"로).
- **상계동** 9/19 24회 → 하루 30회 초과는 여전히 9/18 하루뿐, 보류 유지(20일차·평균 18.8회·순위 1.73~3.11위).
- **확인불가** 9.8 → 9.5%(346·20·24,141원, CTR 5.78%), 보류 유지. 지역 설정 현재값 **7회차 미수령**.
- **08번**: 의정부시(노출 97·클릭 2, 9/19 클릭 1) TOP 10 진입, 성동구(92·7) 컴팩트 목록으로 이동. 컴팩트 26개·58건, 클릭 0 157개·1,074회. 노원 46%·47%, 타겟 63%·59% 그대로.
- **07번**: 정식표 17행(필라테스노원 9/19 클릭 1 → 2건으로 승격, 뱃지는 노출 많은 "확장") 214 + 클릭1건 19 + 경쟁사 3 = 236. 클릭 0 전체 444개·1,565회(경쟁사 포함 정의 유지). 경쟁사 표는 와우 12 → 13회로 오운(12)과 순서가 바뀜(노출 내림차순).
- **11번 판정**: 직전 8개 → 유지 6 · 뒤집힘 1 · 근거 소멸 1(파워링크 그룹 정리 — 노원키즈 종료 확정, 상계동 관찰은 "변화 없음" 줄로). 7개 + (참고) 2. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건.
- **12번 이월 판정**: 직전 5개 전부 — 상시 유지 1 · 진행 2(플레이스 예산·파트너 매체) · 보류 유지 2(확인불가·상계동). 신규·철회 0. 항목 5개.
- 주요 숫자 이동: CPC 격차 3.52 → 3.54배(세 회차 연속 확대 — 플레이스 1,243 → 1,251원, 노원역 353원 고정) / 플레이스 91.9%(232,629원) / 모바일 80.8% / 15시 22회 10회차 연속, 16시 17회 2위 / 심야 1,646·50·41,597원(21%·21%, 9/19 4건 중 2건 22·23시) / 자동매칭 34 대 직접 16(13회차) / 콘텐츠 1,746 10회차 연속 동일, 9/6~9/19 14일 0 / 매칭표 직접 905·자동 1,518.
- 경쟁사: 신규 채택 0. config `competitors` 변경 없음. 아래 이력 표에 줄 추가. 9/19 신규 브랜드형 1회짜리 "INTOPILATES"·"필라테스안노원", 재등장 "유진필라테스"(누적 2)는 웹 검색으로 소재지 특정 불가 → 보류(리포트 미언급). "노원필라테스숲"은 누적 4회 정체로 종결.
- **사용자에게 요청한 값(09-20 채팅)**: ① 9/19 전달한 개별 목록·키즈 계열 등록 여부·등록일 ② 노원역우동짜장·노원역세차·노원역출발이 67·79개 목록에 있었는지 ③ 파트너 매체 네이버 문의 접수·답변 ④ 상향 전 플레이스 일예산 ⑤ 지역 설정 현재값(7회차 — 12번 작성 기준 5 해당). 산전·산후 수업 운영 여부(노원산후필라테스 누적 9회·아기랑 계열 판단용)는 이번에도 못 물음.
- **09-20 채팅 후속 — 재배포 `a109571`(파일 sha 947640d → d2787ad), 14 PASS·재수령본 md5 일치(160d9025…).** 사용자 답 5건:
  ① **지금까지 전달한 제외 검색어 전부 등록 완료**(9/19 개별 목록·키즈 계열 포함, 등록일은 받지 않음 — 9/19 데이터는 등록 전후 혼재로 보고 효과는 9/20 이후 "확장" 행으로 판정). 9/19 무관 검색어 14개를 채팅으로 추가 전달: 9/19 첫 등장 9개(주차노원역·노원역11번출구·노원역뷰카페·노원역7번출구카페·노원카페뷰·노원역일요일영업·행사노원구·노원복싱레슨·시니어필라테스복) + 이전 목록 포함 여부 불명 5개(노원역우동짜장·노원역세차·노원역출발·노원역맛집내돈내산·노원구아기). 클릭 이력 때문에 지난 목록에서 뺐던 노원역아기랑(32회·클릭 1)·노원키즈필라테스(10회·클릭 2)와 노원필라테스강사(1회, 구인·구직 가능성)는 사용자 판단으로 물음.
  ② 우동짜장·세차·출발의 67·79개 목록 포함 여부 — **사용자도 모름** → 위 추가 목록에 넣음(중복은 광고시스템이 거름). 이 질문은 종결, 다시 묻지 말 것.
  ③ **파트너 매체 네이버 문의 접수 완료, 답변 대기** → 12번 4번 "접수 완료·답변 대기".
  ④ **상향 전 플레이스 일예산 10,000원** → 해석 변경: 9/1~9/16 16일 중 13일이 9,396~12,714원(하루 평균 9,658원·클릭 7.2건·CPC 1,344원)으로 예산 근처에서 멈춘 날이 많았던 것으로 보임. 상향 뒤 9/17~9/19 평균 15,071원·클릭 10.0건·CPC 1,507원. **12번 2번 판정 조건 교체**: 직전 조건 "8,000~13,000원으로 돌아오면 닫음"은 그 범위가 옛 예산 한도 근처라 폐기(12번 각주에 이유 명시). 새 조건 = 상향 뒤 하루 평균 클릭이 상향 전 7.2건보다 많은 상태가 이어지는지 + CPC 1,600원 아래 → 이어지면 상향 효과로 닫음 / 7건대로 돌아온 채 광고비만 늘면 예산 수준을 사용자에게 묻는 항목으로. 04번 표기 "(9/17 일예산 10,000 → 20,000원 상향)".
  ⑤ **지역 설정 = 전국** (7회차 만에 수령) → **12번 3번 ✓ 완료, 전국 유지로 정리.** 근거(상세지역 CSV, 25일): 타겟 5개 구 4,999·140·CTR 2.80%·CPC 1,101원 / 타겟 밖 서울 1,099·46·4.19%·985원 / 경기 881·25·2.84%·940원 / 확인불가 346·20·5.78%·1,207원 / 서울·경기 밖 612·5·0.82%·6,111원(2.4%). 재상정 조건: 서울·경기 밖 비용 비중 5% 초과 또는 타겟 밖 서울 CTR < 타겟 5개 구. **다음 회차에 3번은 표에서 빼고(완료), 확인불가 비중으로 승격/축소 판단을 다시 올리지 말 것.**
  11번은 2·4·5번 항목과 "변화 없음" 줄만 고쳤고 판정 집계(유지 6·뒤집힘 1·근거 소멸 1)는 그대로. 12번 이월 판정은 상시 1·진행 2·**완료 1**·보류 유지 1로 바뀜. 산전·산후 수업 운영 여부는 이번에도 못 물음.
- **09-20 채팅 후속 2 — 재배포 `ec0c9cf`(파일 sha d2787ad → 13f4616), 14 PASS·재수령본 md5 일치(162dbdc5…).** 사용자 결정: 노원역아기랑·노원키즈필라테스·노원필라테스강사 **3개도 함께 등록** → 추가 목록 14 → **17개**, 12번 1번 문구·판정 조건 ①을 17개로. 등록은 사용자가 직접 함(네이버 검색광고 커넥터는 레지스트리 검색 결과 없음 — 확인함). 클릭 이력 있는 검색어도 키즈 수업 미운영이면 제외 대상이라는 판단이 이번에 확정됨.
- **09-20 채팅 후속 3 — 재배포 `0b81917`(파일 sha 13f4616 → 9be19a9), 14 PASS·재수령본 md5 일치(01bb5b08…).** 사용자가 17개를 파워링크 제외 검색어로 **등록 완료**. 12번 1번을 "17개 추가 등록 완료(9/20)"로, 판정 조건 ①을 "9/21 이후 확장 행 재노출 → 채팅 보고"로. 목록 원본과 대조 지시는 이 파일 상단 "등록 제외 검색어 대조 목록" 절에 둠.
- 다음 회차 대조(09-20 후속 반영): 9/20 이후 플레이스 하루 클릭이 상향 전 7.2건보다 많은지·CPC 1,600원 아래인지 / **17개 등록 이름의 9/21 이후 "확장" 행 재노출 → 잡히면 채팅 보고(사용자 지시)** / 12번 3번 표에서 제거 / 누적 CTR 3% 재진입 여부 / 파워링크 클릭 재개·노원산전 연속 0 / 파트너 매체 노출·문의 답변 / 우동짜장·세차·출발 재노출(추가 등록 뒤) / 어근 조합·키즈 계열(등록일 이후 "확장" 행만) / 상계동 하루 30회 둘째 날 / 서울·경기 밖 비용 비중 5% 선(3번 재상정 조건) / 유진·INTOPILATES·필라테스안 재등장 / 의정부시 TOP 10 유지.

## 2026-09-19 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.18(24일), 계정 2580077(기간헤더 2026.08.20~09.18). 배포본 index.html 갱신·배포 완료.
배포 커밋 `2ea0fe9`(직전 `39e3f17`, 파일 sha 2f5c60f → 0107cde). 집계 기간 `2026.08.26 — 09.18 (24일)`.
validate.py 14개 검사 전부 PASS(KPI 노출 7,706 / 클릭 232 / CTR 3.01% / 광고비 246,776원, 제외 전 전체 7,712 — 차이 6). 배포 후 재수령본 md5 동일(8b87b958…)·14 PASS.
2-1단계 선확인 작동(배포본 22일 ≠ CSV 24일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.08%·최근 3일 [0,0,0]). 노원키즈필라테스는 최근 3일 [19,1,0]이라 자동감지 조건(3일 연속 0) 미해당이고, 09-17에 정한 대로 `excluded_groups`에 넣지 않음.
01·06 min-width 1760 → 1920, 라벨 `[24, 24]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 배포는 첫 번째 토큰으로 PUT 성공. 이 파일 push는 두 번째 토큰.
- **직전 산식 재현 먼저**: 새 CSV를 `일별 <= 2026.09.16.`로 잘라 KPI·01·02·03·04·05·06·07·08·10 값이 배포본과 전부 같게 나오는 것을 확인한 뒤 새 값을 계산했다(시간대별은 날짜 컬럼이 없어 재현 불가·새 값만). 계산 스크립트는 회차 작업 디렉토리에만 둠.
- **이번 회차 최대 건 — 플레이스 광고비 9/17 20,312원·9/18 18,459원(합계 20,773·18,756원)으로 종전 최고치(9/14 13,412원)를 이틀 연속 경신.** 플레이스 클릭 14·12건(종전 하루 최다 8/28 11건), 노출 178·108회로 늘지 않아 플레이스 하루 CTR 7.87%·11.11%, CPC 1,451·1,538원(9/10~9/14 1,576~1,640원보다 낮음), 순위 3.18·3.28위로 오르지 않음. **원인은 CSV로 판정 불가** — 9/17 매체 설정 재저장과 같은 날 시작됐다는 것만 확인. 12번 2번 신규 항목으로 올리고 채팅으로 "9/17에 플레이스 일예산·입찰가를 바꿨는지"를 물음. 인과를 단정하지 않았음(SKILL.md 서술 검증 규칙).
- **9/17·9/18 클릭 28건 중 27건이 검색 유형 "일치"**(플레이스). 인접 역·구 검색어에서 9건(상계역 3·창동역 3·노원구 2·중계역 1). 9/18 "필라테스" 5건·7,155원은 한 검색어 하루 최다.
- **파트너 매체**: 9/17 재설정 당일 6회(노원역 4·새로 2)·9/18 6회(노원역 2·상계동 2·산전 1·새로 1) → 09-17에 걸어둔 조건대로 **12번 4번을 네이버 검색광고 고객센터 문의로 전환**. 9/6 이후 65회, 누적 96·2건·1,158원. 그룹별 누적 노원역 50·새로 26·산전 10·키즈 5·상계동 5. 다음 회차엔 "재설정으로 해결됐을 가능성"을 다시 올리지 말 것.
- **어근 제외 검색어 부분일치 판정 — 작동하지 않는 것으로 보임**: 9/17 08:20 어근 7개 등록 뒤인 9/18에 노원인스타카페 3·노원역인스타카페 2·노원맘카페 2·노원역맛집내돈내산 1·노원역신규맛집 1·노원역우동짜장 1 = 10회. 09-17에 걸어둔 판정대로 **개별 등록으로 복귀**(12번 1번 상시). 9/17·9/18 신규 확장·클릭 0·무관 검색어 목록은 채팅으로 전달. 개별 등록 67개 중 이름을 아는 노원역헬스·노원역데이트는 9/18 0회, 노원역운동(9/17 5·9/18 1)·노원역체험(9/18 1)은 잡힘 — 67개 목록 원본이 저장소에 없어 등록 여부 대조 불가(다음 회차에 사용자에게 목록을 받아 두면 판정이 정확해진다). 9/10 38개(노원역카페·나다운·수정역·새로오픈) 재노출 0 유지.
- **노원키즈필라테스 종료**: 9/17 노출 1(OFF 당일)·9/18 0. 09-17 ✓ 항목의 판정 조건 충족 → 12번 표에서 제거(각주 기록), 06번 카드는 "종료" 정리 한 줄로 두고 **다음 회차부터 카드 제거**, 04번 표에는 "(9/2 등록 · 9/17 OFF)" 그대로. 키즈·어린이·아기 계열 검색어(노원아기랑 61·노원구아기랑 31·노원키즈 18·노원어린이체험 11 등)를 12번 1번 제외 후보로 이관.
- **상계동필라테스 9/18 노출 38회** — 등록 후 첫 30회 초과(승격 조건 "이틀"의 하루째). 보류 유지, 다음 회차 하루 더 나오면 라인 차트 승격.
- **확인불가 비중 10.8% → 9.8%** — 확인불가 비용 22,403 → 24,141원(+1,738)인데 전체 광고비가 39,529원 늘어 분모가 커진 결과. 승격 기준(10%) 아래라 12번 3번을 "보류로 내림". 지역 설정 현재값은 여섯 회차째 미수령.
- **11번 판정**: 직전 7개(+참고 2) → 유지 4(CPC 격차 확대 → 3.52배, 변화 없음 줄로 / 파워링크 / 파트너 매체 / 확장·클릭 0) · **뒤집힘 2**(검색 노출 이틀 연속 증가 → 284·209로 이틀 연속 감소, 대신 클릭 15·13 최다 / "변화 없음" 줄의 광고비 최고치 9/14 → 9/17·18) · 근거 소멸 1(노원키즈 닷새 연속 0 → OFF 종료). 신규 2(클릭 28건 검색어 구성 / 파워링크 그룹 정리). 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건, 8개 + (참고) 2.
- **12번 이월 판정**: 직전 5개 전부 — 상시 유지 1(어근 미작동 → 개별 복귀) · 보류로 내림 1(확인불가 9.8%) · 완료 확정 제거 1(노원키즈) · 진행 1(파트너 → 네이버 문의) · 보류 유지 1(상계동 38회 하루째). 신규 1(플레이스 광고비 급증 확인) · 철회 0. 항목 5개.
- 주요 숫자 이동: 누적 CTR 2.83 → 3.01%(첫 3%대) / 검색 지면 CTR 3.73 → 3.89% / 플레이스 91.7%(226,186원)·CPC 1,243원 / 파워링크 20,590원(8.3%)·CPC 412원·클릭 50(9/17 자동 1·9/18 직접 1, 노원산전 사흘 연속 0) / CPC 격차 3.42 → 3.52배 / 모바일 80.6% / 15시 22회 9회차 연속, 16시 17회 2위 / 심야 1,566·48·38,251원(20%·21%, 이틀 28건 중 7건) / 자동매칭 34 대 직접 16(12회차) / 클릭 0 검색어 419개·1,503회(11회차 연속) / 확장·클릭 0 노출 9/16 67 → 9/17 69(등록 이후 최다) → 9/18 59 / 타겟 63%·59%, 노원구 46%·47% / 콘텐츠 1,746 9회차 연속 동일, 9/6~9/18 13일 0.
- 경쟁사: 신규 채택 0. config `competitors` 변경 없음. 아래 이력 표에 9줄 추가. "노원필라테스숲" 4회(09-10 1회짜리 보류 건 + 9/17 3회)는 웹 검색으로 소재지 특정 불가 → 보류·07번 각주·11번 (참고) 언급. 9/18 "노해로필라테스"(2)·"노해로노원필라테스"(1)는 자사 주소 도로명(노해로 492) → 경쟁사 아님, 상호 검색으로 판정.
- **사용자에게 요청한 값(09-19 채팅)**: ① 9/17 플레이스 광고 일예산·입찰가 변경 여부(신규) ② 9/17 전달한 79개 후보 등록 여부(09-17부터) ③ 지역 설정 현재값(6회차) ④ 9/17·9/18 신규 무관 검색어 개별 등록 ⑤ 키즈 계열 검색어 제외 등록 ⑥ 파트너 매체 네이버 문의 접수 여부. 산전·산후 수업 운영 여부(아기랑 계열 판단용)는 이번에도 못 물음 — 다음 회차.
- **09-19 채팅 후속 — 재배포 `38a03c4`(파일 sha 0107cde → 439a880), 14 PASS·재수령본 md5 일치(6c04621b…).** 사용자 답 4건: ① **9/18 플레이스 광고 일예산 20,000원으로 상향** — 04번 새로필라테스 행에 "(9/18 일예산 20,000원으로 상향)" 표기, 01·11·12번 2번에 반영. **9/17 20,312원은 상향 전 발생이라 예산 변경으로 설명되지 않음**을 명시(상향 전 일예산 값은 미수령 — 다음 회차에 물을 것). 12번 2번 판정 조건을 "9/19 이후 2만원 근처 소진 지속 여부·클릭 10건·CPC 1,600원"으로 교체 ② **79개 후보 등록 완료** — 12번 1번 ③을 "9/19~ 재노출 0인지"로 교체 ③ 지역 설정 현재값 — 09-19에도 확인 불가(6회차 미수령 유지) ④ **파트너 매체 네이버 문의는 사용자가 넣기로 결정** — 10·11·12번 4번 문구를 "문의하기로 함(9/19 사장님 결정)"으로. 다음 회차는 문의 접수·답변 내용을 12번 4번에 기록.
- **09-19 정정 재배포 `f0d3756`(파일 sha 439a880 → f0be44f), 14 PASS·재수령본 md5 일치.** 사용자가 "9/18 상향"을 **9/17 상향**으로 정정. 9/17 20,312원·9/18 18,459원 모두 새 예산 안의 값이라 이틀치 증가는 **예산 상향으로 설명됨**으로 01·04·11·12번 문구를 고침(직전 재배포의 "9/17분은 상향 전이라 설명되지 않음" 서술은 삭제). 04번 표기 "(9/17 일예산 20,000원으로 상향)". 상향 전 일예산 값은 여전히 미수령. **다음 회차는 이 항목을 "원인 미상"으로 다시 올리지 말 것** — 남은 판정은 예산 소진 지속 여부뿐.
- 다음 회차 대조: 9/19 이후 플레이스 일 광고비가 2만원 근처(예산 소진)에서 이어지는지·그때 클릭 10건·CPC 1,600원 아래 / 상향 전 일예산 값 / 검색 노출 감소 지속 여부와 CTR / 파트너 매체 9/19 이후 노출·문의 답변 / 어근 조합 노출(개별 등록 뒤) / 79개·22개 등록 이후 재노출 / 노원역운동·체험 재노출 / 검색 노출 감소 지속 여부와 CTR / 파트너 매체 9/19 이후 노출·문의 답변 / 어근 조합 노출(개별 등록 뒤) / 노원역운동·체험 재노출 / 상계동 하루 30회 둘째 날 / 노원산전 클릭 재개 / 확인불가 10% 재초과 여부 / 노원키즈 06번 카드 제거·9/19 이후 노출 0 / 필라테스숲·토브·이나핏·유진·아이·보람상가 재등장 / 노원M 변형 / 젠필라테스 클릭.

## 2026-09-17 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.16(22일), 계정 2580077(기간헤더 2026.08.18~09.16). 배포본 index.html 갱신·배포 완료.
배포 커밋 `5240594`(직전 `069609a`, 파일 sha 5af86fb → 6e82dea). 집계 기간 `2026.08.26 — 09.16 (22일)`.
같은 회차 재배포 `04ac2df`(파일 sha 6e82dea → 249a0ff): 사용자가 스크린샷으로 매체 설정을 확인해 준 것을 10·11·12번에 반영. 14개 검사 PASS·재수령본 md5 일치.
같은 회차 재배포 `25699b2`(파일 sha 249a0ff → 4761016): **12번 5번(파워링크 예산 비중 상향) 철회** — 사용자 결정 "파워링크 예산은 그대로". 04·11·12번 반영, 12번 항목 6 → 5개. 14개 검사 PASS·재수령본 md5 일치.
같은 회차 재배포 `8ab033e`(파일 sha 4761016 → 9a4b20a): **제외 검색어 등록분 0건 확인.** 사용자가 "제외 검색어 추가" 화면을 열었더니 파워링크 그룹 확장 검색 칸이 0/950 — 9/10 등록 38개가 남아 있지 않음(사용자: "이전에 전부 등록했었는데 0건"). 그동안 "등록 이후" 기준 판단(09-11~09-17 회차의 확장·클릭0 노출 증감, 어근 재발, 노원역카페·나다운 재노출 0 = 등록 효과)은 전부 근거 없음으로 07·11·12번에 명시. 전체 기간(8/26~9/16) 확장·클릭 0·무관 검색어 **146개 + 어근 7개**(맛집·우동·타이어·사진관·건물·까페·카페) 목록을 채팅으로 전달, 사용자가 9/17 재등록 예정. 등록 칸은 "확장 검색"만(일치/유사 칸은 비움 — 그쪽 클릭 0 검색어는 전부 업종어). 14개 검사 PASS·재수령본 md5 일치.
~~**다음 회차 첫 확인**: 재등록 뒤 화면 건수가 유지되는지 … 38개 등록은 실제로는 남아 있지 않았던 것으로 판명~~ — **아래 정정으로 무효.**
**정정(같은 날, 재배포 `5a40e2a`, 파일 sha 9a4b20a → 362e2ab)**: 위 "0건" 판단은 **Claude의 오독**이었다. 사용자가 보낸 "제외 검색어 추가" 대화상자의 `확장 검색 (0/950)`은 *새로 입력 중인 항목* 수이지 등록 총량이 아니다. 이어 사용자가 보낸 "제외 검색어" 탭 목록에는 9/10 14:46 등록분(나다운필라테스·노원역주차장·노원역주차·정기주차·지도·5번출구·1번출구…)이 그대로 있고, 9/17 08:20에 어근(건물·까페·카페…)이 추가돼 있었다(목록 12페이지 × 10행 ≈ 38 + 67 + 7). 07·11·12번의 "0건" 서술을 전부 되돌리고 "9/10 38개 유지 + 어근은 미등록이었음 → 9/17 08:20 어근 7개·개별 67개 추가 등록"으로 고쳐 재배포. 14개 검사 PASS·재수령본 md5 일치.
**교훈**: 입력 대화상자의 카운터(0/950)는 등록 현황이 아니다. 등록 현황은 "제외 검색어" 탭 목록에서 본다. 다음 회차는 이 오류를 결함으로 다시 올리지 말 것(같은 세션에서 정정 완료).
- 09-17 채팅 후속: 전체 기간 기준 146개 중 첫 목록 67개를 뺀 79개(9/10 등록 38개와 겹칠 가능성 있음 — 중복은 시스템이 거를 것)를 별도 파일로 전달. 4개 그룹 전부 등록됐다고 사용자 확인(09-17). 12번 1번 판정 조건 ③을 "79개 후보 등록 여부"로 교체, 재배포(파일 sha 362e2ab → 다음 값은 배포 커밋 참조).
- ③ 어근 등록 여부 — **09-17 해소**: 미등록이었음이 확인됐고 9/17 08:20 등록 완료. 부분일치 판정은 9/18 이후 데이터로.
- ⑤ 노원키즈 광고 문구·수업 대상 — **09-17 해소**: 사용자 확인 "키즈 수업을 하지 않아". 12번 3번을 문구 수정안 철회 → **OFF 권고(결정)** 로 바꿔 재배포. 06·11번도 맞춤. **이어서 사용자가 9/17 OFF 처리 완료** → 12번 3번 ✓ 완료(항목 5개 중 완료 1·진행 4), 04번 "(9/2 등록 · 9/17 OFF)", 06번 카드 "9/17 OFF, 집행 15일", 07번 우측 카드 ✓ 문구 수정. 재배포 완료(14 PASS·md5 일치). 06번 카드는 다음 회차에 OFF 이후 노출 0 확인 후 제거.
  **다음 회차 처리 규칙(미리 정함)**: 노원키즈필라테스는 첫 그룹 "노원필라테스(삭제)"와 달리 실집행(15일 노출 334·클릭 8·3,023원)이 있으므로 `excluded_groups`에 넣어 누적에서 통째로 빼지 **않는다**. 04번 표에 남기고 "(9/2~OFF일)" 표기, 06번 카드는 OFF 뒤 첫 회차에 "종료" 한 줄로 정리 후 다음 회차부터 카드 제거. OFF 이후 날짜에 노출·클릭이 잡히면 설정 확인. 키즈 계열 검색어(노원키즈 18·노원어린이체험 11 등 09-10에 "잠재고객"으로 남겨둔 13개)는 다음 회차에 제외 검색어 후보로 전환.
validate.py 14개 검사 전부 PASS(KPI 노출 7,213 / 클릭 204 / CTR 2.83% / 광고비 207,247원, 제외 전 전체 7,219 — 차이 6). 배포 후 재수령본 md5 동일(55fe2afb…)·14 PASS.
2-1단계 선확인 작동(배포본 21일 ≠ CSV 22일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.08%·최근 3일 [0,0,0]).
01·06 min-width 1680 → 1760, 라벨 `[22, 22]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 배포는 첫 번째 토큰으로 PUT 성공(지난 회차와 같은 방식). 이 파일 push는 두 번째 토큰.
- **직전 산식 재현 먼저**: 새 CSV를 `일별 <= 2026.09.15.`로 잘라 KPI·04·06·07·08·10 값이 배포본과 전부 같게 나오는 것을 확인한 뒤 새 값을 계산했다(계산 스크립트는 회차 작업 디렉토리에만 두고 저장소에는 넣지 않음). 재현에서 걸린 정의 2가지 — 다음 회차가 같은 표를 재현하려면 필요: ① 07번 "클릭 0 검색어 전체 N개·노출 N회" 각주는 **경쟁사 검색어를 포함**한 값(350개/1,323회 재현. 경쟁사 7개·40회를 빼면 343/1,283으로 어긋남). "노출 5회 이상" 컴팩트 목록은 경쟁사를 뺀 값. ② 10번 "9/6 이후 파트너 매체 N회"는 **9/6 포함**(`>=`)이어야 46회가 재현된다(`>`면 43회).
- **01번 순위 그리드의 민트 강조는 닷새 중 가장 좋은(작은) 값에 붙인다** — 직전 커밋 b42bb0f에서 마지막 날이 아닌 9/12 3.39위에 강조가 있는 것으로 확인. 이번엔 9/15 2.85위에 유지.
- **11번 판정**: 직전 8개 → 유지 7 · 뒤집힘 1(CPC 격차 "축소" → 3.38 → 3.42배 다시 확대. 플레이스 CPC 1,193→1,201원 상승, 노원역 353→351원 하락) · 근거 소멸 0. "검색 노출 반등"은 9/16 298회(이틀 연속 증가, 9/9 이후 최다)로 이어져 유지 항목으로, "노원산전 사흘 연속 클릭"은 9/16 0건으로 끊겨 파워링크 항목에 합침. 신규 1(확장·클릭 0 노출 9/16 67회 — (참고)에서 독립 항목으로). 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건, 7개 + (참고) 2.
- **12번 이월 판정**: 직전 6개 전부 — 상시 1(확장·클릭 0 노출 33→67회로 등록 이후 최다, 어근 계열 6회로 3회차 연속 재발) · 승격 유지 1(확인불가 10.7→10.8%, 네 회차 연속 10% 초과) · 진행 2(노원키즈 닷새 연속 0이나 노출 19회로 회복 → 문구 가설 유지 / 파트너 매체 9/16 7회, 5개 그룹 전부) · **철회 1(파워링크 — 판정 구간 9/10~9/16 15건 확정으로 데이터 조건은 충족했으나 09-17 사용자 결정 "예산은 그대로". 운영 판단이므로 표에서 내림. 재상정 조건: 사용자 요청 또는 파워링크 일 클릭이 플레이스의 절반을 넘는 날이 이어질 때. 다음 회차에 신규로 다시 올리지 말 것)** · 보류 유지 1(상계동 25회, 최다 29회). 신규·철회 0.
- **사용자에게 요청한 값**: ④ 검색 파트너 매체 해제 여부 — **09-17 수령.** 사장님이 광고시스템 "매체 변경" 화면 스크린샷으로 확인: 파워링크 4그룹·플레이스 1그룹 전부 "노출 매체 유형 선택 › PC/모바일 전체 › 검색 지면 › 네이버 및 검색 포털 매체"만 체크, 파트너 매체·콘텐츠 지면(네이버·파트너) 해제. 설정은 맞는데 노출이 계속되므로 12번 4번을 걸어둔 조건대로 **네이버 문의 항목으로 전환**(문의 요지: 해제 상태에서 9/6 이후 다음·네이트·Bing 노출 53회·클릭 1건이 잡히는 이유). 다음 회차엔 "설정이 안 됐을 가능성"을 다시 올리지 말 것. ① 입찰가·일예산은 09-17 철회로 더 이상 필요 없음. 여전히 미수령: ② 지역 설정 현재값(5회차) ③ 어근 등록 여부 — **09-17 해소**: 제외 검색어 자체가 0건이라 물음이 무의미했음. 146개+어근 7개 재등록 예정, 등록일·등록 후 건수 확인 대기 ⑤ 노원키즈 광고 문구·수업 대상(2회차).
- 주요 숫자 이동: 9/16 노출 298·클릭 8·CTR 2.68%(9/5 이후 첫 누적 평균 아래)·광고비 9,905원 / 검색 지면 누적 CTR 3.79→3.73% / 플레이스 90.4%(187,415원)·CPC 1,201원 / 파워링크 19,832원(9.6%)·CPC 413원·클릭 48 / 모바일 80.8% / 15시 22회 8회차 연속 / 심야 1,446·41·28,564원(20%·20%, 9/16 8건 중 4건 심야) / 자동매칭 33 대 직접 15(11회차) / 클릭 0 검색어 370개·1,393회(10회차 연속 증가) / 확인불가 300·19·22,403원(10.8%, CTR 6.33%) / 타겟 63%·59%, 노원 46%·48%(노출 비중 47% 4회차 연속 뒤 첫 변동).
- 경쟁사: 신규 채택 0. config `competitors` 변경 없음. 아래 이력 표에 6줄 추가. 9/16 신규 1회짜리 "보니따필라테스노원상계"는 웹 검색으로 소재지 특정 불가 → 보류(리포트 미언급).
- **9/17 계정 조치 요약(사용자 직접)**: ① 파트너 매체 설정 5개 그룹 해제 확인(스크린샷) 후 **같은 날 매체 설정 재저장** — 12번 4번은 "네이버 문의 전환"에서 "9/18 이후 파트너 매체 노출·클릭 0이면 닫고, 계속되면 네이버 문의"로 바꿈(재배포) ② 08:20 제외 검색어 어근 7개+개별 67개를 4개 그룹에 등록(9/10 38개 유지 확인) ③ 노원키즈필라테스 광고그룹 OFF ④ 파워링크 예산 현행 유지 결정. 미수령은 ② 지역 설정 현재값뿐. 산전·산후 수업 운영 여부는 아기랑 계열 제외 판단용으로 다음에 물을 것.
- 다음 회차 대조: 노원키즈 9/18 이후 노출·클릭 0인지(06번 카드 제거) / 9/16 298회 증가가 이어지는지 / CTR 2.68%가 하루치인지 / CPC 격차 방향(회차마다 반전 중) / 노원산전 클릭 재개 / 노원키즈 클릭 복귀·노출 10회 미만 여부 / 파트너 매체 노출 — **9/18 이후 날짜만** 잘라 다음·네이트·Bing·기타 매체 노출·클릭이 0인지(0이면 9/17 재설정으로 해결, 12번 4번 닫음 / 계속되면 네이버 문의로 올림) / 어근 계열(맛집·까페) 노출 / 확장·클릭 0 67회가 하루치인지 / 확인불가 12% 선 / 보니따필라테스·그릿필라테스 재등장 / 제외 검색어 등록일 이후 어근 계열(맛집·우동·까페·카페 등) 노출이 0인지(어근 부분일치 판정) / 파워링크 예산 항목은 철회됐으니 다시 올리지 말 것.

## 2026-09-16 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.15(21일), 계정 2580077(기간헤더 2026.08.17~09.15). 배포본 index.html 갱신·배포 완료.
배포 커밋 `069609a`(직전 `b42bb0f`, 파일 sha 38603d3 → 5af86fb). 집계 기간 `2026.08.26 — 09.15 (21일)`.
validate.py 14개 검사 전부 PASS(KPI 노출 6,915 / 클릭 196 / CTR 2.83% / 광고비 197,342원, 제외 전 전체 6,921 — 차이 6). 배포 후 재수령본 md5 동일(df5148f0…)·14 PASS.
2-1단계 선확인 작동(배포본 20일 ≠ CSV 21일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·비중 0.09%·최근 3일 [0,0,0]).
01·06 min-width 1600 → 1680, 라벨 `[21, 21]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **토큰**: 사용자가 두 개를 줬고 `GET /repos` permissions는 둘 다 push:true로 나와 구분이 안 됐다(fine-grained PAT는 이 필드가 토큰 범위가 아니라 사용자 권한을 보여줌). 배포는 첫 번째 토큰으로 PUT 성공.
- **직전 산식 재현 먼저**: 새 CSV를 `일별 <= 2026.09.14.`로 잘라 KPI·04·07·08 값이 배포본과 전부 같게 나오는 것을 확인한 뒤 새 값을 계산했다. 07번 "확장·클릭 0 노출"은 **행 단위**(`검색 유형=='확장' & 클릭수==0` 행의 일별 합)여야 배포본 63/63/49/53/51이 재현된다 — 검색어 단위 합계로 거르면 50/53/44/46/47로 달라진다.
- **11번 판정**: 직전 8개 → 유지 6 · 뒤집힘 2(검색 노출 142~201회 구간 → 9/15 251회 / CPC 격차 "두 회차 연속 확대" → 3.41 → 3.38배 축소, 노원역 CPC 349→353원이 플레이스 1,189→1,193원보다 더 오름) · 근거 소멸 0. 신규 1(노원산전 사흘 연속 클릭). 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건, 8개 + (참고) 2.
- **12번 이월 판정**: 직전 6개 전부 — 상시 1(어근 등록 확인 대기) · 승격 유지 1(확인불가 10.4 → 10.7%) · 진행 2(노원키즈 나흘 연속 0 → 걸어둔 조건대로 **문구 수정안** 제시, 현재 문구는 CSV에 없어 대괄호 템플릿으로 / 파트너 매체: 9/6 이후 46회가 **5개 광고그룹 모두**에서 나옴 → 항목 자체 미해제 가능성) · **값 대기 1(파워링크 — 지난 회차 규칙대로 순서를 5번으로 내림)** · 보류 유지 1(상계동, 최다 29회). 신규·철회 0.
- **제외 검색어**: 행 단위 확장·클릭0 노출 9/15 33회(등록 후 최저). 어근 계열 "노원역까페"·"노원맛집새로오픈" 9/15 각 1회 재발. 9/15 "노원필라테스오픈"(확장)에 클릭 1건·715원 → "오픈"은 어근으로 막지 말라고 12번에 적음.
- **사용자에게 요청한 값(여전히 미수령)**: ① 파워링크 4그룹 입찰가·일예산 ② 지역 설정 현재값 ③ 어근 6개 등록 여부 ④ 검색 파트너 매체 해제 여부. 이번 회차에 ⑤ 노원키즈 현재 광고 문구·실제 수업 대상/형태 추가. ①②는 회차가 쌓여 12번 작성 기준 5)에 따라 채팅으로 진행 막힘 이유를 물었다.
- 경쟁사: 신규 채택 0. config `competitors` 변경 없음. 아래 이력 표에 4줄 추가(고요 종결 · 그릿 보류 · 트리니티 5회 제외 유지 · 필라테스정원 재등장).
- 다음 회차 대조: 9/16 포함 파워링크 판정 구간 확정 합계 / 9/15 노출 251회 반등 지속 여부 / CPC 격차 방향 / 노원산전 연속 클릭 / 노원키즈 클릭·노출(10회 미만 지속 시 검색량 쪽으로 판단 이동) / 파트너 매체 노출 / 어근 계열 노출 / 확인불가 12% 선 / 그릿필라테스 재등장.

## 2026-09-15 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.14(20일), 계정 2580077. 배포본 index.html 갱신·배포 완료.
배포 커밋 `1dcad3b`(직전 `a3ccb92`, 파일 sha deb8b7f → 628337e). 집계 기간 `2026.08.26 — 09.14 (20일)`.
validate.py 14개 검사 전부 PASS(KPI 노출 6,664 / 클릭 186 / CTR 2.79% / 광고비 186,053원, 제외 전 전체 6,670 — 차이 6). 배포 후 재수령본 md5 동일·14 PASS.
2-1단계 선확인 작동(배포본 19일 ≠ CSV 20일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·최근 3일 [0,0,0]).
01·06 min-width 1520 → 1600, 라벨 `[20, 20]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **신규 발견(이번 회차 최대 건) — 9/6 "해제"한 검색 지면 파트너 매체에서 노출·클릭이 계속됨.** 콘텐츠 지면 두 항목(네이버·파트너)은 9/6 이후 노출 0으로 아흐레 연속 확인되는데, **검색 지면 › 파트너 매체(다음·네이트·Bing)는 9/6 이후에도 노출 44회**가 잡히고 **9/14 다음-모바일에서 클릭 1건·698원**이 발생했다(누적 75회·2건·1,158원). 10번 표의 "9/6 조치 = 해제" 표기와 실제가 어긋난 상태다. 표기는 그대로 두고 10번 note·11번 2번 항목·12번 5번에 사실을 적었다. **설정 확인은 사용자 몫이고 다음 회차 첫 확인 항목이다.**
- **매체 그룹 분류 방법(다음 회차가 같은 표를 재현하려면 필요)**: `매체이름`만으로 10번 표 4개 행을 나누면 안 된다. `기타 매체`는 검색 3회·콘텐츠 60회로 갈리고 `다음-모바일`도 검색 47·콘텐츠 18로 갈린다. **`검색/콘텐츠 매체` 컬럼과 `매체이름`을 함께 써야** 지난 회차 값(A 4,652 / B 71 / C 22 / D 1,724)이 재현된다. 이번 값은 A 4,843 / B 75 / C 22 / D 1,724이고 콘텐츠 쪽 C·D는 9/6 이후 완전히 고정.
- **`검색/콘텐츠 매체` 컬럼의 실제 값은 `검색`·`콘텐츠`다** (`검색 매체`가 아니다). 처음 `=='검색 매체'`로 걸러 01번 지면별 노출이 전부 0/전량 콘텐츠로 나왔다 — 그대로 배포했으면 조용히 틀렸을 자리다. references 표의 컬럼명만 보고 값까지 추측하지 말 것.
- **11번 판정**: 직전 8개 → 유지 7 · 뒤집힘 1(광고비 최고치 9/13 12,503원 → 9/14 13,412원) · 근거 소멸 0. 신규 1개(검색 파트너 매체). 직전 맨 위 "파워링크 클릭 하루 최다"는 9/13 기록이 그대로여서 유지로 내림, "타겟 구 비중"·"상위 검색어 비중"은 1%p 안 변동이라 지역 항목·"변화 없음" 줄로 합침. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건, 8개 + (참고) 2.
- **12번 이월 판정**: 직전 4개 전부 판정 — 상시 유지 1(1번: 어근 등록 여부 확인으로 물음을 좁힘. 9/14 "노원역까페" 2회가 또 잡혀 어근이 등록됐는지부터 갈림) · 승격 유지 1(2번 확인불가: 10.8% → 10.4%, 기준 초과 유지) · 진행 1(3번 파워링크: 판정 구간 9/10~9/16 닷새 12건으로 기준 10건 충족) · 보류 유지 1(6번 상계동: 9/14 노출 9회, 최다 29회). **복귀 1**(4번 노원키즈: 9/12·13·14 사흘 연속 클릭 0 → 직전 회차가 걸어둔 복귀 조건 충족. 노출 17·26·22로 줄지 않고 순위는 2.02→1.99위로 좋아져 소재 쪽 가능성). **신규 1**(5번 검색 파트너 매체). 항목 6개(상한 7).
- **사용자에게 요청한 값**: ① 파워링크 4그룹 입찰가·일예산 ② 광고시스템 지역 설정 현재값 — **둘 다 세 회차 연속 미수령이고 2·3번 항목 판단이 그 값에서 멈춰 있다.** 이번 회차에 추가로 ③ 제외 검색어 어근 6개 등록 여부 ④ 검색 지면 파트너 매체 해제 여부.
- 주요 숫자 이동: 플레이스 90.1%(167,686원)·CPC 1,189원 / 파워링크 18,367원(9.9%)·CPC 408원 / CPC 격차 3.34 → 3.41배(두 회차 연속 확대, 노원역 349원 고정·플레이스만 상승) / 검색 지면 CTR 3.75% → 3.78% / 모바일 81.6% / 최다 시간대 15시 22회 6회차 연속 / 심야 노출 1,360·클릭 37·24,346원(20%·20%) / 자동매칭 32 대 직접 13(9회차) / 클릭 0 검색어 340개·1,282회(8회차 연속 증가) / 확인불가 노출 269·클릭 17·19,312원.
- **경쟁사 신규 채택 2건 (같은 회차에 세 곳 전부 갱신 — (1-1) 규칙)**: 사장님이 "노원오프닝필라테스·필라테스인 둘 다 노원 업체"라고 확인해 **"오프닝필라테스"·"필라테스인"을 채택**했다. ① config `competitors`에 두 이름 추가(6개 → 8개) ② 아래 이력 표에 채택으로 기록 ③ 화면은 07번 경쟁사 표 3행 추가(필라테스인노원 12 · 노원필라테스인 4 · 노원오프닝필라테스 4, 전부 클릭 0·0원)·각주·11번 (참고). 12번은 클릭·비용이 0이라 액션 항목으로 올리지 않고 그 이유를 각주에 적었다. "필라테스인노원"(12회)은 07번 "클릭 0·노출 5회 이상" 목록에서 빼 경쟁사 표로 옮겼다(그 목록 44개 → 43개). 클릭 합계는 변하지 않아 validate 검산 그대로 통과(정식표 165 + 클릭1건 18 + 경쟁사 3 = 186). 재배포 커밋 `b42bb0f`(파일 sha 628337e → 38603d3), 14개 검사 PASS·재수령본 md5 일치.
- 04번 표 행 순서를 비용 내림차순으로 맞춤(새로 → 노원역 → 노원산전 → 노원키즈 → 상계동). 예산 비중 90.1+4.7+2.2+1.6+1.4 = 100.0.
- 07번: 정식표 16행(클릭합 165) + 클릭1건 18 + 경쟁사 3 = 186. 클릭0·노출 5회 이상 44개 — 경쟁사명(오운 8·이레 6·스마일 5)은 아래 경쟁사 표로 빼는 관행 유지.
- 다음 회차 대조: 검색 파트너 매체 해제 여부와 노출 지속 / 어근 6개 등록 여부와 "까페" 계열 노출 / 노원키즈 클릭 복귀 / 파워링크 구간(9/16) 마감 합계 / 확인불가 비중 12% 선 / 검색 지면 CTR 3.7%대 3회차 / 노원오프닝필라테스·필라테스인 계열 판정 / 상계동 하루 30회.

## 2026-09-14 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.13(19일), 계정 2580077. 배포본 index.html 갱신·배포 완료.
배포 커밋 `a3ccb92`(직전 `9d4bf29`, 파일 sha 253fc0a → deb8b7f). 집계 기간 `2026.08.26 — 09.13 (19일)`.
validate.py 14개 검사 전부 PASS(KPI 노출 6,469 / 클릭 177 / CTR 2.74% / 광고비 172,641원, 제외 전 전체 6,475 — 차이 6). 배포 후 재수령본 md5 동일·14 PASS.
2-1단계 선확인 작동(배포본 17일 ≠ CSV 19일). 제외 그룹 신규 후보 없음(`노원필라테스(삭제)` 노출 6·클릭 0·최근 3일 [0,0,0]).
01·06 min-width 1360 → 1520, 라벨 `[19, 19]`. 스킬 문서·config 변경 없음 — 이 파일만 push.

- **11번 판정**: 직전 8개 → 유지 5 · 뒤집힘 3(파워링크 클릭 "이틀 연속 1건 최저" → 9/13 하루 7건 최다 / CPC 격차 정체 → 3.15→3.34배 / 광고비 최고치 9/9 → 9/13 12,503원) · 근거 소멸 0. 수동 검사 `필요`·`시점`·`할 것`·`검토`·`주째` 0건, 8개 + (참고) 2.
- **12번 이월 판정**: 직전 6개 전부 판정 — ✓ 2개 표에서 뺌(제외 검색어 38개: 재노출 0건 / 노원키즈: 9/12·9/13 이틀 클릭 0, 복귀 기준 "사흘"엔 미달 → 9/14도 0이면 복귀) · 상시 1(제외 검색어: 역 주변 시설 계열 3회차 연속 재발 → **어근 단위 등록으로 방식 전환**, 어근 후보 맛집·우동·타이어·사진관·건물·까페. 아기랑 계열은 대상 아님) · **승격 1**(위치 확인불가 비용 비중 9.2 → 10.8%, CTR 6.32%. 지역 설정 현재값이 CSV에 없어 사용자 입력 대기) · 진행 1(파워링크 예산: 판정 구간 9/10~9/16 나흘째 11건으로 기준 10건 조기 충족. 입찰가·일예산 현재값 대기) · 보류 1(상계동 그래프: 최다 29회). 2·3번 순서 교체(확인불가 18,614원 > 파워링크 17,669원).
- **사용자에게 요청한 값(다음 회차에 받으면 12번에 반영)**: ① 파워링크 4그룹 입찰가·일예산 ② 광고시스템 지역 설정 현재값. 09-14 회차엔 못 받음.
- **사용자 결정**: 노원M필라테스(종결 후 9/12 클릭 1건) → **경쟁사 표에 되돌리지 않고 클릭 1건 목록에 그대로**. config 변경 없음.
- 제외 검색어 38개 효과: 등록 후 재노출 0건. 확장·클릭 0 노출 9/10·9/11 63 → 9/12 49 → 9/13 53회.
- 다음 회차 대조: 파워링크 9/14~9/16 클릭(구간 마감 합계) / 노원키즈 9/14 클릭 / 검색 지면 CTR 3.75% 유지 여부 / 검색 노출 142~201회 구간 지속 여부 / 확인불가 비중 12% 선 / 어근 등록 뒤 시설 계열 노출 0인지(부분일치 판정) / 고요필라테스 재상정.

## 2026-09-12 갱신 회차 (진단 아님 — 리포트 배포 회차)

CSV 4종 실데이터 `일별` 2026.08.26~09.11(17일), 계정 2580077. 배포본 index.html 갱신·배포 완료.
validate.py 14개 검사 전부 PASS(KPI 노출 6,144 / 클릭 155 / 광고비 147,870원, 제외 전 전체 6,150 — 차이 6).
제외 그룹 신규 후보 없음(`노원필라테스(삭제)`만 조건 해당: 노출 6·클릭 0·최근 3일 [0,0,0]).
스킬 문서·config 변경 없음 — 이 파일의 경쟁사 판정 이력만 갱신.

**사용자 결정 3건 (리포트에 반영됨)**

1. **모든날필라테스 → 제외 확정**(대구 소재). 09-11 자연 소멸 종결을 되돌려 제외로 재판정, 이력 표에 기록.
   config `competitors`는 변경 없음 — 채택이 아니라 제외이므로 추가할 대상이 아니다.
2. **제외 검색어는 상시 점검 항목으로 전환.** 09-10 1차 등록(38개) 뒤에도 확장·클릭 0 노출 총량이
   줄지 않았다(9/10 36개·63회 → 9/11 38개·63회). 등록한 이름들(노원역카페·나다운필라테스·수정역필라테스)은
   멈췄으나 "노원역헬스·노원역룸·노원역옷·노원역분위기" 같은 **역 주변 시설·장소 검색 계열**이 빈자리를
   채웠다. 1회성 조치로 닫지 말고 매 회차 07번 "클릭 0·노출 5회 이상" 목록에서 신규 확장 검색어를 뽑아
   등록할 것. 12번 1번 항목에 `상시` 태그로 상주시켰다.
3. **12번 철회 2건** — "인접 지역 검색어 4개 직접 등록"(중계역·창동역·마들역·상계역필라테스, 합산
   노출 575·클릭 24·비용 28,289원 = 19.1%)과 "자동매칭 우위 → 새로필라테스 직접 등록". 5회차 연속
   미반영이라 채팅으로 물었고 **"생각이 바뀌어 안 하기로 했다"**는 답을 받았다. 데이터가 뒤집혀서가
   아니라 운영 판단이므로 다시 올리려면 새 근거가 필요하다. 파워링크 등록 키워드는 4개로 고정.
   07번 우측 카드 제목도 "신규 키워드 등록 후보" → "클릭이 발생 중인 확장·인접 검색어"로 바꿔 모순을 없앴다.

**다음 회차에 주의할 것**

- 이 파일은 **맨 위 헤더가 2026-09-07 진단 회차 기준선**이고, 현행 경쟁사 이력은 아래 `## 경쟁사 판정 이력`
  표다. 파일 중간을 건너뛰고 읽으면 하단 "이전 기록" 절의 옛 표(노원M필라테스 **채택**으로 적힌 행)를
  현행으로 착각한다 — 이번 회차에 실제로 그 착각이 났고, 사용자에게 "config와 audit이 어긋나 있다"고
  잘못 보고했다. 노원M은 **09-09에 이미 종결·config 삭제까지 끝난 건**이다. 읽을 때 `## 경쟁사 판정 이력`을
  먼저 찾을 것.
- 12번 1번(제외 검색어 상시 점검)은 완료로 닫는 항목이 아니다. 같은 계열이 3회차 연속 재발하면 개별 등록
  대신 패턴 단위 제외로 방식을 바꾸기로 되어 있다.
- "국내 - 상세 위치 확인불가" 비용 비중 7.4% → 9.2%. 10% 초과 시 지역 타겟팅 재검토로 승격(12번 3번).

## 경쟁사 판정 이력 (현행 — 09-29 갱신)
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

## 점검표 개정안 (제출 10건 중 ①~④ 채택·반영 → checklist v4.2. ⑤는 종결 기록만. 6~10은 미채택 — 다음 회차 재상정)

⑤ 종결 기록(반영 안 함): 직전 미채택 2(천단위 콤마·인코딩) — 두 회차 연속 같은 실 CSV로 콤마 없음·UTF-8 BOM 확인, 형식이 바뀐 회차에만 재확인 / 7(빈 데이터) — 헤더만·1행은 FAIL 정상 종료 실측, 기간헤더 1줄 파일은 네이버가 내지 않는 것으로 두 회차 미관측 / 8(.pyc) — `.gitignore` 있고 `git ls-files` pyc 0건.

1. **모순 수정**: `[시작 전 확인 ②]` "하나라도 없으면 저장소 clone도 하지 말고" — 이 규칙 자체가 저장소 안 checklist.md에 있어 clone 없이는 읽을 수 없다. 이번 회차도 clone 후에야 규칙을 봤다. "clone(읽기)은 하되 진단은 시작하지 말라"로.
2. **전제 수정**: 2) 라이브 Pages 수신 방법 — web_fetch 캐시가 이번에 저장소 파일(SKILL.md 234행 vs 312행)로 확정됐다. web_fetch를 "받는 방법"으로 두지 말고 "라이브는 이 환경에서 기계 확인 불가 → 사용자 시크릿 창 확인 요청, 기계 확인은 배포본 커밋과 Pages 빌드 상태를 사용자가 볼 것"으로. Pages API는 무인증 404(실측).
3. **행 번호 갱신**: "4종의 컬럼 구성이 SKILL.md 42행 표와 일치하는지" → 표는 57–62행. 파괴 실험 예시 행 번호(218·781·782·302…)는 배포본 커밋이 같아 아직 유효하지만 배포본이 바뀌면 전부 어긋난다 — 행 번호 대신 "07 정식표 첫 행 클릭" 같은 위치 서술로.
4. **1) 대상 목록에 누락**: `config/report-config.json`·`.gitignore`가 실제 ls에 있으나 점검표 목록에는 없다(validate.py 실행에 config 필수라고 판정 기준 절에는 적혀 있음).
5. **종결 제안**: 미채택 개정안 8(.pyc 커밋) — `.gitignore` 있고 추적 pyc 0건. 미채택 2·7(콤마·인코딩·빈 데이터) — 두 회차 연속 같은 실 CSV로 종결. "실 CSV 형식이 바뀐 회차에만 재확인"으로.
6. **추가**: CSV가 직전 회차와 같은 기간이면 CSV 실측은 재현 확인으로 갈음(I-9). 점검표가 "반드시 실측"만 요구해 같은 결과를 두 번 냈다.
7. **매 회차 통과 항목 축소**: 경쟁사 목록 대조(2회 연속 통과)·.ctr-high 재사용(3회)·문서 경로 실존(3회)·차트 색 배정 — validate.py로 자동화된 것(섹션 주석·min-width·각주)은 점검표에서 "validate.py PASS"로 대체하고, 나머지는 "배포본 커밋이 바뀐 회차에만".
8. **검증 회차 절 분리**: "진단 회차에는 읽지 마라"고 적혀 있지만 같은 파일이라 읽게 된다. `audit/verify.md`로 분리하거나 그대로 두되 문구를 "적용하지 마라"로.
9. **추가**: 파괴 실험 목록에 "06번 min-width"를 넣을 것 — 이번 회차에 넣어보니 PASS(D-9). 점검표는 "01·06번 모두 대상"이라 하면서 실험 예시는 01번(960→900)만 있었다.
10. **추가**: "config 값을 바꿔 검사 결과가 바뀌는지" 실험을 판정 기준에 넣을 것(이번 `ctr_high_threshold` 5.0 실험이 D-8을 찾았다). `excluded_groups` 비우기만 예시로 있었다.

## 점검표 갱신 이력 (checklist.md)
- v4.3 (2026-09-08) — 파괴 실험을 `tests/mutation_test.py`로 이관. 검사 목록을 실행 시점에 세고(고정 개수 없음), 사본에서만 변조(원본 md5 대조 출력), 0건 가드 8종·config 실험 2종 포함, 겨냥 변조가 없는 검사는 UNCOVERED로 보고. 2026-09-08 실 CSV 실행: 검사 14개 전부 FAIL 확인, UNCOVERED 0, 원본 md5 동일, exit 0. [판정 기준] 절의 2026-09-07 실측 나열은 스크립트 안내로 대체.
- v4.2 (2026-09-07 저녁) — 개정안 ①~④ 반영. ① CSV 누락 시 "clone도 하지 마라" → "clone은 하되 진단은 시작하지 마라"(점검표가 저장소 안에 있어 모순). ② 라이브 Pages 수신 방법에서 web_fetch 전제 삭제 — 캐시가 저장소 SKILL.md(234행 옛 본문 vs HEAD 312행)에도 걸리는 것이 확인돼, 기계 확인 수단 없음(bash 403·Pages API 무인증 404·raw는 저장소 사본)을 적고 사용자 시크릿 창 확인이 유일하다고 명시. 사용자 확인 전 결함 금지 규칙 유지. ③ "SKILL.md 42행 표" → 1단계 표(57~62행). ④ 대상 목록에 config/report-config.json·.gitignore 추가. 부수: 파괴 실험 개수 12→14 및 06 min-width·날짜축 라벨 예시 추가.
- v4.1 (2026-09-07) — `[검증 회차]` 절 추가. (이하 직전 회차 기록과 동일, 아래 "이전 기록" 참고)

## 갱신 회차 기록 (2026-09-11) — 배포본만 변경, 스킬 코드·config 변경 없음

새 CSV(계정 2580077, 기간헤더 2026.08.12~09.10, 실 `일별` 2026.08.26~09.10 **16일**)로 리포트 갱신·배포.
배포 커밋 `129d023`(직전 `90d8ad4`, 파일 sha 571c15b → 2f98bc7). 집계 기간 `2026.08.26 — 09.10 (16일)`.
KPI 노출 5,943 / 클릭 148 / CTR 2.49% / 광고비 137,724원. 이 파일만 push(audit).

- **2-1단계 선확인 작동**: 배포본 masthead(15일) ≠ CSV(16일) 대조 후 진행. 3회차 연속 정상.
- api.github.com 무인증 GET이 rate limit(403)으로 막혀 배포본은 `git clone` 공개 저장소로 받음(SKILL.md 4단계 대안). 배포 직전 sha는 토큰 GET으로 재조회.
- **validate.py 14개 검사 전부 PASS, exit 0.** 01·06 min-width 1200 → 1280(16일), 라벨 `[16, 16]`. 배포 후 재수령본 md5 동일(79d48d85…)·14 PASS.
- **제외 그룹**: `노원필라테스(삭제)` 노출 6·클릭 0·비중 0.10%·최근 3일 [0,0,0]. 신규 후보 없음.
- **08·09번 각주**: 5,949 − 5,943 = 6회. 클릭 148 = 148.
- **07번 정식표 집계 방식 명시**: 검색어 보고서를 `검색어`로만 묶음(검색 유형이 갈린 행은 합산, 뱃지는 노출 많은 유형). 배포본 관행(노원구필라테스 일치+확장 = 198회, 노원역근처필라테스 일치+유사 = 150회)과 같음. 클릭 0 검색어 263개·1,085회도 같은 기준.
- **12번 작성 기준 5) 첫 실적용 — 1·3번 4회차 연속 미반영 → 채팅으로 확인.** 사용자 답: 둘 다 **등록 예정**(철회 아님). 12번 해당 줄에 반영, 다음 회차에도 미등록이면 재확인.
- 12번 이월 판정: 완료 확정 제거 2(콘텐츠 해제·상계동 클릭 재발생→6번 병합) / 철회 삭제 1(노원필라테스) / **완료 1(제외 키워드 38개, 9/10 등록 — 09-10 계정 조치 기록의 완료 조건 충족)** / 진행 4 / **되돌림 1(노원키즈: 누적 7건, 기준 8건 미달 — 배포본이 걸어둔 기준을 그대로 적용)** / 보류 1. 진행 항목 6개(상한 7).
- **제외 검색어 효과 판정 보류**: 9/10 확장·클릭 0 검색어 36개·63회(노원역카페 13 등)가 등록 당일이라 시각 전후 혼재. 다음 회차는 **9/11 이후 날짜만** 잘라 63회 밑인지 확인. 나다운·수정역필라테스는 9/10 노출 0.
- **11번 작성 기준 2회차 적용**: 8개 + (참고) 2. 직전 8개 판정 유지 7·**뒤집힘 1**(검색 노출 나흘 증가 → 9/10 179회, 개업 당일 제외 최저)·근거 소멸 0. 광고비 최고치(9/9 유지)는 "변화 없음" 줄로 이동. 수동 검사: `필요`·`시점`·`할 것`·`검토`·`주째` 0건.
- 서술 정정: 04번 "4주째"·06번 "5주째"를 회차 표현으로 고침(11번 기준 5를 다른 섹션에도 적용).
- 경쟁사: 표 7행 지난주와 노출·클릭·비용 동일(9/10 경쟁사명 검색 0). 종결 2·보류 유지 3·신규 1회짜리 4건은 위 이력 표. config `competitors` 변경 없음.
- 다음 회차 대조: 9/10 노출 179회가 하루짜리인지(9/11~) / 12번 2번 판정 구간 9/10~9/16 파워링크 클릭 / 노원키즈 누적 8건 / 1·3번 등록 여부 / 제외 검색어 효과(9/11~) / 상계동 하루 30회 조건.

## 스킬 문서 변경 (2026-09-10 3차) — 11번 "작성 기준" 신설, 배포본 변경 없음

- `references/report-structure.md` 11번에 **작성 기준 6개 + 수동 검사 6항목** 추가(12번 기준과 같은 구조). 근거: 2026-09-10 배포본 11번이 15개 항목·항목당 4~6문장, 상태 항목이 매주 같은 문장으로 반복, 조치 문장("정리가 필요해 보임")이 12번과 중복, 개업 15일차에 "5주째 유지" 표현.
- `SKILL.md` 5단계에 예외 한 줄: **11번은 12번 확정 뒤 맨 마지막에 쓴다.** 두 파일이 한 규칙이다(11번 작성 기준 4 ↔ SKILL.md 5단계).
- **해결(같은 날 3차 배포 `35366e4`, 파일 sha 26ad060 → c7a80bb)**: 2차 배포(d6cd5bc)에서 12번은 노원필라테스를 철회했는데 11번 7번째·9번째 항목이 "실제로는 집행되지 않는 중 / 활성 그룹으로 옮기는 정리가 필요해 보임"이라 모순됐다 — 새 작성 기준 4) 유형. 두 문장만 "플레이스로 충분하다는 판단으로 보류 결정(12번 철회 항목 참고)"으로 고쳐 재배포, validate 14개 PASS·재수령본 일치.
- **11번 전체 재작성 — 4차 배포 `90d8ad4`(파일 sha c7a80bb → 571c15b), 같은 15일 CSV(md5 필라테스 c1bedf23…), 기준 6개 첫 적용.** 15개 항목 → **8개 + (참고) 2개**. 순서: 플레이스 89.5%/CPC 격차(114,500원) → 파워링크 33건(13,425원) → 광고비 최고치 9/9 → 콘텐츠 해제 확정 → 상위 검색어 45% → 자동매칭 24 vs 9(CPC 448 vs 297 병기) → 신규 키워드 3개 → "변화 없음" 한 줄(모바일·시간대·지역·제외 그룹). 상자 끝에 직전 회차 판정 줄(유지 15·뒤집힘 0·근거 소멸 0, 노원필라테스 서술 2곳은 보류 결정 반영). 수동 검사 6항목: 숫자 전부 CSV 재계산 일치 / 15 = 15 / `필요`·`시점`·`할 것`·`검토` 0건 / `주째` 0건 / 12번 철회와 모순 0건 / 8+2. validate 14개 PASS·재수령본 일치. og:description·1~10·12번 변경 없음.
- 다음 새 CSV 회차에 볼 것: 11번 8개 항목 각각을 새 데이터로 유지/뒤집힘/근거 소멸 판정하는 게 처음으로 실제 작동하는 회차다. "변화 없음" 줄의 4개 상태값이 ±3%p·자리 변동을 넘으면 독립 항목으로 다시 올릴 것.
- 다음 회차 대조: 11번 항목 수 ≤ 8 + (참고) ≤ 2 / 조치 문장 0건 / "주째" 0건 / 12번 철회·완료 항목과 모순 0건.

## 계정 조치 기록 (2026-09-10) — 파워링크 제외 검색어 38개 등록 (사용자 직접 수행)

- 사용자가 네이버 광고시스템에서 **파워링크 광고그룹 4개(노원역필라테스·상계동필라테스·노원키즈필라테스·노원산전필라테스) 각각의 "제외 검색어 추가 → 확장 검색" 칸**에 같은 38개를 등록함. "일치(유사검색어)" 칸은 비움(그쪽 클릭 0 검색어는 전부 업종에 맞아 제외 대상 아님). 플레이스 광고에는 넣지 않음(무관 검색어가 전부 확장 유형 = 파워링크 확장검색 유래).
- 목록 선정 근거: 2026.08.26~09.09 검색어 보고서에서 검색 유형 "확장"·클릭 0인 209개 중 업종·상권 무관만. 나다운필라테스(57)·주차/역 안내 9개·음식/카페 10개·"새로오픈" 계열 11개(상호 "새로"가 "새로 오픈한 가게" 검색에 걸림)·타 운동 레슨 3개·수정역필라테스·기타 3개. 
- 보류: 아기·어린이·시니어 계열 13개(86회·클릭 1)는 키즈필라테스 잠재 고객 가능성으로 미등록. 경쟁사 브랜드명은 경쟁사 표 정책과 별개라 미등록.
- **12번 5번 항목("제외 키워드 등록 실행")의 완료 조건 충족.** 다음 새 CSV 회차에서 ① 12번 5번을 완료(4그룹·38개·9/10)로 판정 ② 효과는 **등록 이후 날짜(9/11~)만** 잘라 클릭 0 검색어 노출이 줄었는지 확인 — 누적값(1,043회)은 등록 전 노출을 포함하므로 누적으로 비교하지 말 것 ③ 38개 중 등록 후에도 노출이 잡히는 게 있으면 제외 검색어가 부분일치가 아닐 가능성 → 확인.
- 현재 배포본(90d8ad4) 12번 5번은 "3회차째 미실행"으로 남아 있음 — 다음 배포 때 고칠 것.

## 갱신 회차 기록 (2026-09-10 2차, 12번만 재작성) — 배포본만 변경, 데이터 동일

같은 15일치 CSV(2026.08.26~09.09)로 숫자 변경 없이 **12번 다음 액션만** `references/report-structure.md` 12번 "작성 기준" 5개를 처음 적용해 다시 씀. 배포 커밋 `d6cd5bc`(직전 `4c0d83f`, 파일 sha 58f8318 → 26ad060). validate.py 14개 검사 PASS(배포 전·재수령본 모두). 1~11번·집계 기준·og:description은 손대지 않음.

- **기준 적용 결과**: 직전 12번 10개 항목 전부 판정 — 완료 3·진행 5·보류 1·**철회 1**. 각 항목에 "다음 회차 판정 조건" 한 줄 부착. 정렬을 비용 영향순으로 바꿔 인접 지역 4개(23,262원) 1번, 제외 키워드 정리(비용 0원) 2번→5번, 상계동 승격(비용 0) 맨 아래. 표 아래에 정렬 기준·판정 집계·반복 항목 각주 3줄 신설.
- **작성 기준 5번 첫 적용 — "노원필라테스" 파워링크 집행 재개 항목 철회**: 배포본에 5회차째 "미반영"으로 적혀 있어 리포트에 또 적기 전에 채팅으로 이유를 물음. 사용자 답: **플레이스로 이미 클릭이 잡히고 있어 파워링크에 비용을 더 쓰지 않으려는 의도적 보류**. 실행이 막힌 게 아니라 결정이 난 것이므로 철회 처리, 사유는 12번 해당 줄에 한 줄로 남김. **다음 회차부터 이 항목을 신규로 다시 올리지 말 것.** 재상정 조건: 검색어 "노원필라테스" 클릭당 비용(현재 1,099원)이 파워링크 직접 등록 CPC(297원)의 4배를 넘게 벌어지거나 사용자가 다시 요청할 때.
- **같은 논리가 걸리는 항목**: 12번 1번(중계역·창동역·마들역·상계역필라테스 직접 등록)도 검색 유형 "일치"로 플레이스에서 잡히는 클릭이라 성격이 같다. 다음 회차에 같은 답이면 철회로 정리할 것 — 표에 "별도 확인 필요"로 적어둠. 1·3·5번(인접 지역·자동매칭·제외 키워드)은 9/6·9/9·9/10 3회차 연속 미반영이지만 닷새 안이라 "3주"로 보지 않고 진행으로 둠. 다음 회차에도 그대로면 5번 기준 적용.
- 회차 초반 사용자가 올린 CSV는 14일치(09-09 갱신분)였고 2-1단계 대조로 배포본(15일)과 다름을 잡아 다시 받음 — 선확인이 "오래된 CSV" 경로에서도 작동한 첫 사례. 첫 토큰은 Contents 쓰기 권한이 없어 PUT 403·git push 403(SKILL.md 토큰 안내대로 권한 확인 요청 후 재발급으로 해결).

## 갱신 회차 기록 (2026-09-10) — 배포본만 변경, 스킬 코드·config 변경 없음

새 CSV(계정 2580077, 기간헤더 2026.08.11~09.09, 실 `일별` 2026.08.26~09.09 **15일**)로 리포트 갱신·배포.
배포 커밋 `4c0d83f`(직전 `ad8a522`). 집계 기간 `2026.08.26 — 09.09 (15일)`.

- **2-1단계 선확인 작동**: 배포본 masthead(14일) ≠ CSV(15일)를 먼저 대조하고 새 데이터로 판정한 뒤 계산에 들어갔다. 2회차 연속 이 경로가 정상 동작.
- **validate.py 14개 검사 전부 PASS, exit 0.** 01·06번 min-width가 `기대 1200px (15일)`로 상향 요구 → 배포본 263·695행을 1120 → 1200으로 고쳐 PASS. 날짜축 라벨 배열도 `[15, 15]`로 통과. 배포 후 재수령본(sha 58f8318)으로 다시 돌려 14개 PASS 재확인.
- **제외 그룹**: `노원필라테스(삭제)` 노출 6·클릭 0·비중 0.10%·최근 3일 [0,0,0]. 신규 후보 없음(나머지 5그룹 최근 3일 노출 전부 >0).
- **08·09번 각주**: 제외 전 전체 노출 5,770 − KPI 5,764 = 6회 차이. 클릭 141 = 141로 차이 0(제외 그룹 클릭이 계속 0이라 "클릭 N회 차이" 문구는 아직 필요 없음).
- **경쟁사 판정**: 채택·삭제 없음 — 표 7행 그대로. config `competitors` 변경 없음. 신규·기존 보류 후보는 아래 이력 표에 한 줄로 갱신.
- **서술 검증에서 뒤집힌 결론 2건**: ① 직전 회차 01번의 "플레이스 순위 사흘 연속 하락(3.60→3.71→4.02위)"이 9/9 3.54위로 반등 ② 직전 회차 06번·11번의 "상계동필라테스만 클릭이 멈춰 있다"가 9/9 클릭 1건으로 깨짐. 둘 다 SKILL.md "이전 주 결론이 뒤집히면 조용히 지우지 말고 솔직히 서술한다"에 따라 해당 섹션에 명시했다. 2회차 연속 이 유형이 나왔다 — 갱신 회차마다 직전 서술을 전수 재확인할 근거.
- **신규 키워드 카드 승격 판단**: 상계동필라테스가 10일차로 `report-structure.md` 승격 조건(10일치)을 채웠으나, 하루 노출 10~27회로 일별 순위가 1.73~2.87위로 흔들려 요약 카드로 유지했다. 판단 근거와 재검토 조건(하루 노출 30회 수준)을 12번 4번 항목에 적어 다음 회차가 같은 판단을 반복하지 않게 했다.
- 이월 개선안 I-7~I-10은 이번 회차에 손대지 않음(갱신 회차라 코드 변경 없음).

## 갱신 회차 기록 (2026-09-09) — 배포본만 변경, 스킬 코드 변경 없음

새 CSV(계정 2580077, 기간헤더 2026.08.10~09.08, 실 `일별` 2026.08.26~09.08 **14일**)로 리포트 갱신·배포.
배포 커밋 `ad8a522`(직전 `28fc744`). 집계 기간 `2026.08.26 — 09.08 (14일)`.

- **2-1단계가 실제로 작동함(직전 회차 확인 항목)**: 배포본 masthead(12일) ≠ CSV(14일)를 먼저 대조하고 새 데이터로 판정한 뒤 계산에 들어갔다. 같은 기간이었으면 여기서 멈추는 경로도 그대로 살아 있다.
- **validate.py 14개 검사 전부 PASS, exit 0.** 01·06번 min-width가 `기대 1120px (14일)`로 자동 상향 요구 → 배포본 263·675행을 960 → 1120으로 고쳐 PASS. 직전 기준선이 "다음 갱신부터 01·06 모두 바꿔야 PASS"라고 적어둔 항목이 실제 갱신에서 그대로 걸렸고, D-9 조치가 06번을 잡아낸 첫 실사례다(검사가 없었다면 06번만 960으로 남았을 것).
- 날짜축 라벨 배열 검사도 `[14, 14]`로 통과 — 01·06 두 차트 라벨을 같이 늘려야 한다는 것을 검사가 강제했다.
- **제외 그룹**: `노원필라테스(삭제)` 노출 6·클릭 0·비중 0.11%·최근 3일 [0,0,0]. 신규 후보 없음(나머지 5그룹 최근 3일 노출 전부 >0).
- **경쟁사 판정**: 노원M필라테스 종결(위 이력 표), 신규 브랜드형 후보 전부 보류. 승인·제외 결과를 config(`competitors`에서 노원M 삭제)·이 이력 표·화면 3곳에 같은 회차에 반영 — (1-1) 규칙대로.
- **08·09번 각주**: 제외 전 전체 노출 5,420 − KPI 5,414 = 6회 차이. 클릭은 131 = 131로 차이 0(제외 그룹 클릭이 계속 0이라 "클릭 N회 차이" 문구는 아직 필요 없음).
- **서술 검증에서 실제로 뒤집힌 결론 1건**: 직전 회차 11번의 "파워링크 신규 키워드 3개는 클릭이 더 붙지 않고 있음"이 이번 주 9/7·9/8 이틀 클릭 9건으로 뒤집혔다. SKILL.md "이전 주 결론이 뒤집히면 조용히 지우지 말고 솔직히 서술한다"에 따라 11번·04번에 뒤집혔다고 명시했다.
- 이월 개선안 I-7~I-10은 이번 회차에 손대지 않음(갱신 회차라 코드 변경 없음).

## 다음 점검에서 대조할 것
- (09-10 갱신 회차 추가) 다음 갱신에서 01·06번 min-width가 일수×80으로 다시 상향됐는지 / 상계동필라테스 승격 판단이 재검토됐는지(하루 노출 30회 조건) / 09-10에 종결한 1회짜리 후보 6개가 신규로 다시 잡히지 않는지 / 고요필라테스 재상정 여부.
- **검증 회차 미실시.** checklist `[검증 회차]` A(동작)·B(의도)를 별도 세션에서 받을 것. 대조 항목: validate.py `DATE_SECTIONS`·`check_date_labels`·f-string 라벨 4곳 / SKILL.md 41–47·경쟁사 절·제외그룹 절·타겟 지역 줄·검산 목록 / checklist v4.2 네 곳 / 이 절.
- 06번 min-width 파괴 실험(675행 960→900)이 FAIL인지, `date_based_sections=[1]`에서 06 검사가 사라지는지 재현.
- 직전 기준선(아래 이전 기록) 118행·112행의 "전부 조치완료"는 **당시 기록 오류**(06번 검사는 이번 회차에 처음 생김) — 원문 보존 원칙상 고치지 않고 여기 정정으로 남김.
- 검사 개수는 14. 이 숫자를 그대로 쓰지 말고 실행 출력을 세어라(설정에 따라 변한다).
- 새 CSV(다음 주) 회차에서: 2-1단계 선확인이 실제로 멈추는지 / 노원M필라테스 자연 소멸 판단 / `노원필라테스(삭제)` 클릭 발생 시 각주 "클릭 N회 차이" / masthead 형식·예산 비중 반올림 오탐 / 06번 675행 min-width가 13일×80=1040으로 갱신됐는지(검사가 없으면 여기서 처음 틀린다).
- 검색어 CSV 참고 출력(I-7) 조치 여부.
- 미채택 개정안(직전 1·2·4·5·7·8·9·10 + 이번 1~10) 재상정. 이번 회차에 종결 제안한 것: 직전 2·7·8.
- web_fetch 캐시: 다음 회차에도 SKILL.md 대조군을 한 번 받아 캐시가 풀렸는지 본다. 풀렸으면 개정안 2를 되돌릴 수 있다.

## [수정 회차에 적용할 것 — 점검표에서 옮겨 적음]
- 같은 개념을 두 파일에서 고칠 때는 기준을 대조해라. D-9는 validate.py·SKILL.md·css-and-layout.md·config·기준선 다섯 곳이 한 규칙이다.
- 검사 조건을 완화하는 수정을 했으면 기존 파괴 실험(위 표 12+6)을 전부 다시 돌려라.
- 새 설정값·새 필드를 추가했으면 같은 회차에 문서화하거나 빼라. 반대로 지금 코드 소비자가 없는 config 필드 5개(I-8)를 쓰기 시작하면 그 사실을 문서에 적어라.
- 설계를 바꿨으면 그 자리의 주석도 같이 고쳐라(validate.py 22행 docstring `9. 01번 차트 min-width`가 06번을 포함하게 되면 함께).
- 수정과 검증은 다른 세션에서 한다. 검증 문구는 checklist.md `[검증 회차]` 절.

---

# 이전 기록 (원문 보존)

# 점검 기준선
점검일: 2026-09-07 (오후 회차, Fable) — 진단 후 사용자 선택으로 D-3~D-6 수정, 개정안 3·11 반영
결함 4건(전부 조치완료) / 개선안 5건(이월) / 인용불가로 제외 0건
직전 기준선(2026-09-07 오전, 커밋 846af35) 대비: 해결 2건(D-1·D-2), 미해결 1건→실측 확정 후 조치(D-3), 근거없음 0건, 신규 3건(D-4·D-5·D-6, 조치완료)

점검 대상(전부 저장소에서 받은 것): `saero-ad-report-skill` @e83993f — SKILL.md(234행) · README.md(2) ·
references/report-structure.md(291) · references/css-and-layout.md(181) · scripts/validate.py(217) ·
audit/checklist.md(217) · audit/last-audit.md(144) / `saero-pilates-report` @474966e index.html(1707행,
집계 2026.08.26—09.06 12일) · service-worker.js(46) / 라이브 Pages(web_fetch로 수신, 아래 참고) /
설치본 부트스트랩은 재업로드 언급 없어 건너뜀.
**실 CSV 4종 있음**: 필라테스_보고서(=키워드) 197행 · 검색어 534 · 상세지역 726 · 시간대별 24.
기간헤더 2026.08.08~09.06이지만 실 `일별` 2026.08.26~09.06(12일) — 배포본과 같은 기간이라 점검에만 사용.

## 이번 회차 조치 (스킬 저장소 커밋 — 아래 "다음 점검에서 대조할 것" 참고)

- **D-3 조치완료** — SKILL.md 57행을 "`일별` 컬럼이 있는 3개 CSV(키워드·검색어·상세지역)"로 한정하고,
  시간대별은 validate.py 검사 3으로 기간 일치를 확인한다고 명시.
- **D-4 조치완료** — validate.py 검사 3 비교 대상을 KPI → 키워드 보고서 **제외 전 전체** 클릭 합계로 변경.
  출력에 `제외 전 전체 — 노출/클릭 (08·09번 각주 차이)` 줄 추가. SKILL.md 219행·validate.py docstring 11행도 맞춤.
  재실측: 제외그룹 클릭+1·시간대별 +1(일관) → PASS(`111 vs 전체 111 (KPI 110)`) / 시간대별만 ±1 → FAIL. 의도대로 동작.
- **D-5 조치완료** — SKILL.md 검산 목록에 `01번 일별 표의 클릭률 셀도 같은 규칙으로 전수 대조` 추가.
- **D-6 조치완료** — SKILL.md 152행을 "노출이 0인 키워드는 행이 생기지 않는다. OFF 그룹 키워드 10개 중 노출이 잡힌 것(예: 8/26 노원필라테스)만 보인다"로 정정.
- **개정안 11** — css-and-layout.md 버그 기록 8번에 `06번 rankChart도 x축이 날짜라 같은 규칙의 대상(12일 기준 960px)` 추가. checklist 항목도 갱신. I-4에 "min-width = 일수×80 검사(01·06번)" 추가.
- **개정안 3** — checklist 2)에 라이브 Pages 수신 방법(web_fetch 2단계) 기록.
- 수정 후 validate.py 실 CSV 실행: 5개 검사 전부 PASS, exit 0.

## 라이브 Pages 확인 (2026-09-07 오후)
- bash curl → 403 `x-deny-reason: host_not_allowed`. web_fetch로 수신 성공(방법은 checklist 2 참고).
- masthead `2026.08.26 — 09.06 (12일)`, KPI 4,912/110/2.24%/98,009 — 저장소와 일치.
- **불일치**: 집계 기준 "클릭률 강조" 문구가 라이브는 `07번 표에서`, 저장소(474966e, 09-07 00:19 UTC)는 `01·07번 표에서`.
  Pages 빌드 지연·캐시 가능성. **다음 회차 첫 확인 항목.** 계속 다르면 Pages 빌드 상태(Actions) 확인 필요.

## 실 CSV 실측 요약
- 인코딩 UTF-8 BOM(1행 기간헤더에 있어 skiprows=1로 무해). 천단위 콤마 **없음**(총비용 10,208 등 5자리가 `10208`). 4종 모두 int64 → 콤마 크래시 우려 종결.
- 컬럼: 키워드 일치 / 검색어·상세지역은 전환 컬럼 추가(주요 컬럼이라 무관) / **시간대별 `일별` 없음**(D-3 근거). 실 컬럼명 `클릭률(%)`·`평균 CPC`(공백).
- 키워드 보고서 실 파일명 `필라테스_보고서_<계정번호>.csv`.
- 배포본 KPI·01번 일별표·08번(TOP10 노출순 89 + 컴팩트 14개 21 = 110, 클릭0 161개·870회)·09번 심야(1,047·28·18,159원)·타겟 66%/61%·노원구 48%/51% 전부 실 CSV와 일치.
- 보고서 간 비용 합계 차이: 키워드 98,009 / 검색어 98,008 / 상세지역 98,010 / 시간대별 98,006 (반올림). 배포본은 키워드 기준. 결함 아님, 기록만.
- 기간 불일치: 키워드 짧음 → 검사 2·3 FAIL / 검색어 짧음 → `참고` 출력·exit 0 / 상세지역 → 미검사(I-4) / 시간대별 짧음 → 검사 3 FAIL.
- 빈 데이터: 헤더만·1행 → FAIL로 정상 종료. 기간헤더 1줄만 → EmptyDataError 크래시(네이버가 그런 파일을 내는지 미확인, 결함 아님).
- validate.py 5개 검사 + 0건 가드 2종 전부 깨뜨려 FAIL 확인(태그 218행 div / 07 781행 28→27 / 09 CSV −1 / 07 782행 4.71% 강조 제거 / 01 302행 5.22% 강조 제거 / name-cell·Section 1 주석 변조).
- 노원M필라테스: 노출 2회 + 변형 2회 = 4회, 클릭 0. 배포본 1003행과 일치.

## 직전 기준선 판정
| 항목 | 판정 | 근거(지금 원문) |
|---|---|---|
| D-1 경쟁사 목록 누락 | 해결됨 | SKILL.md 117행 `스마일필라테스 · 와우필라테스 · 퍼스트필라테스 · 노원M필라테스`. 배포본 경쟁사 표 8행과 일치(표기 변형 1건 제외) |
| D-2 .ctr-high 규칙 | **해결됨(저장소·배포·라이브 전부)** | css-and-layout.md 44행 `표 무관, 클릭률 전용` · validate.py 13행 `5. 01번 표도 같은 규칙으로 전수 대조` · index.html 1287행 `01·07번 표에서 클릭률 4% 이상인 행만`. 라이브도 동일함을 사용자가 시크릿 창으로 확인(2026-09-07). web_fetch가 옛 문구를 준 것은 도구 캐시였음 |
| D-3 "각 CSV의 일별 컬럼" | 실측 확정 → 조치완료 | 실 시간대별 CSV 컬럼 `시간대별,노출수,클릭수,클릭률(%),평균 CPC,총비용,평균노출순위,…` — `일별` 없음. SKILL.md 57행 수정 |
| I-1 배포본 최신 여부 선확인 | **조치완료(2026-09-07 저녁)** | SKILL.md 2단계~4단계 사이 변경 없음. 이번 CSV(max 09.06) = 배포본 222행 기간 — 정확히 I-1 상황 |
| I-2 승인 기록 규칙 | **조치완료(2026-09-07 저녁)** | SKILL.md 124행 `3. 승인받은 뒤에만 경쟁사 표에 추가` 이후 규칙 없음 |
| I-3 설정값 단일 출처 | **조치완료(2026-09-07 저녁)** | config 파일 없음(ls). 개업일 사본 SKILL.md 54·57·58·61·63·65·203행 |
| I-4 validate 범위 | **조치완료(2026-09-07 저녁, 검사 12개)** | validate.py 인자에 상세지역 CSV 없음 |
| I-5 토큰 두 종류 | **조치완료(2026-09-07 저녁)** | SKILL.md 25–26행 배포 토큰만 언급 |
| 배포본 1287행 문구 | 해결됨 — 저장소·라이브 모두 `01·07번 표에서` | 사용자 시크릿 창 확인(2026-09-07). 이 항목 종결, 다음 회차에 다시 다루지 않는다 |
| 06번 rankChart 960px | 종결(규칙 추가) | index.html 675행 `min-width:960px` = 12일×80. css-and-layout.md 버그 기록 8번에 06번 명시 |

## 결함 (이번 회차 발견, 전부 조치완료)
| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 실측/추론 | 왜 틀렸는지 | 수정 방향 | 작업경로 |
|---|---|---|---|---|---|---|---|---|
| D-3 | 중 | SKILL.md | 57 | `각 CSV의 `일별` 컬럼 최솟값이 `2026.08.26.`인지 확인한다.` | 실측 | 시간대별 CSV에 `일별` 없음 | 3개 CSV로 한정 — **조치완료** | saero-ad-report-skill |
| D-4 | 중(잠재) | scripts/validate.py / SKILL.md | 168–175 / 171·219 | `hourly_clicks == kpi_clicks` vs SKILL.md 171행 `08·09번…없어서 제외 불가 → 포함된 값을 쓰고` | 실측(제외그룹 클릭+1 합성 → FAIL 재현. OFF 그룹은 실 CSV 8/31에도 노출 1 발생) | 09번은 제외그룹을 포함하는데 검사는 KPI(제외 후)와 비교 → OFF 그룹 클릭 1건이면 데이터가 맞아도 배포 차단 | 제외 전 전체와 비교 — **조치완료** | saero-ad-report-skill |
| D-5 | 하 | SKILL.md | 215–220 | 검산 목록 4개(`07번 클릭률 4% 이상 행에만…`까지) | 실측 | validate.py는 5개(01번 검사) | 01번 항목 추가 — **조치완료** | saero-ad-report-skill |
| D-6 | 하 | SKILL.md | 152 | `키워드 보고서 CSV에는 OFF 그룹 내부 키워드가 보이지 않는다.` | 실측(실 CSV `새로필라테스 파워링크,노원필라테스(삭제),노원필라테스,2026.08.26.,…` 3행) | OFF 그룹 키워드가 보인다. 안 보이는 건 노출 0 때문 | 이유를 노출 0으로 정정 — **조치완료** | saero-ad-report-skill |

## I-1~I-5 조치 (2026-09-07 저녁, 실 CSV 4종으로 검증)

다섯 개 전부 반영. 실 CSV(2026.08.26–09.06)와 배포본으로 검사 12개 전수 실행,
새 검사는 각각 깨뜨려 FAIL까지 확인.

- **I-1 완료** — SKILL.md에 `### 2-1단계. 배포본이 이미 최신인지 먼저 확인`을
  2단계와 3단계 사이에 신설. masthead `집계 기간`과 CSV `일별` min/max를 대조해
  같으면 계산 전에 사용자에게 묻고 멈춘다. **이번 CSV가 정확히 그 상황이었고
  (배포본·CSV 모두 `2026.08.26 — 09.06 (12일)`), 새 절차대로면 여기서 멈춘다**는 것을
  실측으로 확인.
- **I-2 완료** — "승인이 필요한 지점"에 `(1-1) 승인·제외 결과를 남기는 곳` 표 추가.
  채택은 `config/report-config.json`의 `competitors`, 판정 전부는 audit "경쟁사 판정
  이력", 화면은 07번 각주·11번 (참고)·12번 액션 3곳. 제외·자연소멸도 이력에 남긴다.
  config·audit 갱신은 배포와 같은 회차에.
- **I-3 완료** — `config/report-config.json` 신설. 개업일·제외그룹·제외그룹 키워드·
  경쟁사 목록·타겟 지역·CTR 기준·차트 폭 규칙을 한 곳에 모음. validate.py가 이 파일을
  읽는다(하드코딩 `EXCLUDED_GROUPS`·`4.0`·`80/650` 제거). SKILL.md·css-and-layout.md는
  값을 적지 않고 이 파일을 가리킨다. 설정 파일이 없으면 스크립트가 즉시 종료한다.
  **설정의 `excluded_groups`를 비워 돌려보니 KPI가 4,912→4,918로 바뀌며 FAIL** —
  파일이 실제로 읽히는 것을 실측 확인.
- **I-4 완료** — validate.py 검사 5개 → **12개**. 상세지역 CSV를 5번째 인자로 추가.
  신규: masthead 집계 기간 · KPI 타일 4개 · 04번 예산 비중 합 100.0% ·
  01번 차트 min-width = 일수×80 · 섹션 주석 1~12 · 08·09번 각주 "N회 차이" +
  상세지역 CSV 노출 합계 대조. 전부 0건 가드 포함.
- **I-5 완료** — 배포 정보에 토큰 두 종류 표 추가(배포 = saero-pilates-report,
  스킬·기준선 push = saero-ad-report-skill). 읽기는 둘 다 토큰 불필요,
  403이면 다른 저장소 토큰인지 먼저 확인하라는 안내 포함.

### 검사 생존 확인 [실측] — 실 CSV 기준 12개 전부 PASS 후 개별 파괴

| 조작 | 결과 |
|---|---|
| masthead 12일 → 11일 | FAIL |
| KPI 타일 노출 4,912 → 4,913 | FAIL |
| 04번 예산 비중 91.7 → 91.6 (합 99.9%) | FAIL |
| 01번 차트 min-width 960 → 900 | FAIL |
| Section 5 주석 제거 | FAIL(누락 [5]) |
| 08번 각주 6회 → 5회 | FAIL |
| masthead 문구 자체 변조(0건 유도) | FAIL(마크업 변경 의심) |
| KPI 타일 마크업 변조(0건 유도) | FAIL(마크업 변경 의심) |
| config 파일 삭제 | 즉시 종료, 안내 메시지 |

부수 확인: 실 CSV로 돌린 12개 검사가 전부 PASS했다는 것은 **현재 배포본 자체가
CSV와 완전히 일치한다**는 뜻이기도 하다(KPI 타일·예산비중·각주·차트 폭 포함).


## 개선안 (최대 5 — 2026-09-07 저녁 전부 조치완료)
| # | 내용 | 이유 | 우선순위 |
|---|---|---|---|
| I-1 | (이월) 2단계 직후 배포본 masthead `집계 기간`(index.html 222행)과 CSV `일별` max 대조, 같으면 계산 전 사용자에게 먼저 묻기 | 이번 CSV가 정확히 이 상황. 3회차 연속 미변경 | 1 |
| I-2 | (이월) 승인 결과 기록 규칙 3종 + "한 저장소를 고치면 다른 쪽 대응 줄을 같은 회차에 고친다" | D-1·D-5 모두 한쪽만 고친 유형 | 2 |
| I-3 | (이월) 설정값 단일 출처 파일: 개업일 7곳, 제외그룹 2곳(SKILL.md 146·validate.py 33), 경쟁사 목록(117), 타겟지역(175), 80px/650px 3곳 | 한 곳만 고치면 어긋남 | 3 |
| I-4 | (이월·갱신) validate.py 확장: 상세지역 CSV 인자 + 08번 합 검산 · masthead 기간 vs 3개 CSV `일별` min/max · 검색어 CSV 클릭합 불일치를 참고→FAIL/명시 경고 · KPI 타일 값 vs CSV · 04번 예산비중 합 · 08·09 "N회 차이" 각주(이제 스크립트가 차이를 계산해 출력하므로 각주 대조로 확장 용이) · **01·06번 min-width = 일수×80 검사(개정안 11)** · 섹션 주석 1~12 | 검색어 CSV가 짧아도 exit 0 "배포 진행 가능" | 4 |
| I-5 | (이월) SKILL.md 25–26행 토큰 두 종류 명시 + audit 갱신 절차 | 이번 회차 스킬 저장소 토큰을 별도로 받음 | 5 |

## 경쟁사 판정 이력 (변경 없음)
| 후보 | 판정 | 근거 | 일자 |
|---|---|---|---|
| 젠·이레·오운·스마일·와우·퍼스트필라테스 | 채택(표) | 노원·도봉구 실제 업체 | ~09-05 |
| 퍼스트필라테스아카데미노원 | 채택(표기 변형, 별도 승인 불필요) | SKILL.md 126행 규칙 | 09-05 |
| 노원M필라테스 (변형 M필라테스노원·노원엠필라테스) | 채택(표) — SKILL.md 117행 반영 | 노원구 소재 확인. 09-07 CSV 4회·클릭 0 | 09-06 |
| 나다운필라테스 | 제외 | 구로 신도림/인천 검단, 확장검색 오매칭 | 09-05 확정 |
| 트리니티·웰니스·퀸즈·나인·씨앤미·벨·수현·예일필라테스 | 제외 | 한 자릿수 노출, 상권 무관 | 09-06 |
| 에반더필라테스상계역점 · RHA필라테스상계·상계동 | 종결(자연 소멸) | 2주 연속 한 자릿수·클릭 0. 다시 묻지 않음 | 09-06 |

## 점검표 개정안 (제출 11건 중 3·11 채택·반영. 나머지는 미채택 — 다음 회차에 다시 물을 것)
1. 이월 목록 갱신(D-3 종결, D-4~D-6 추가) — 미채택. **이 기준선이 정본이므로 checklist 이월 목록보다 이 파일을 우선.**
2. 천단위 콤마·인코딩 항목 종결(실 CSV 근거) — 미채택
3. 라이브 Pages 수신 방법 — **채택·반영**
4. 실 파일명 4개 패턴 명시(`필라테스_보고서_<계정>.csv` 등) — 미채택
5. 4종 기간 불일치 판정을 CSV별로 구체화 — 미채택
6. 09번 검사 가정(제외그룹 클릭 0) 명시 — D-4 조치로 사실상 해소
7. 빈 데이터 항목 축소 — 미채택
8. `scripts/__pycache__/validate.cpython-312.pyc` 커밋됨·.gitignore 없음 — 미채택
9. 매 회차 통과 항목(경쟁사 목록 대조·.ctr-high 재사용) 조건부화 — 미채택
10. 08번 TOP10 정렬 기준(노출수 내림차순) report-structure 220행에 명시 — 미채택
11. 06번 rankChart 규칙 — **채택·반영**

## 점검표 갱신 이력 (checklist.md)

- v4.1 (2026-09-07) — `[검증 회차]` 절 추가. 수정 뒤에 받을 검증 문구 두 벌(A 동작
  검증 / B 의도 검증)을 저장해 매번 새로 만들지 않게 했다. hometax 에서 A 는 0건,
  같은 저장소를 B 로 보니 6건이 나왔다(4건은 수정 과정에서 생긴 것).
- v4 (2026-09-07) — hometax-invoice-check 6차에서 겪은 것을 반영.
  ① 토큰 선요청 블록 신설(진단 후 요청하면 세션 유실 시 결과가 통째로 날아간다 —
  실제 발생). ② `[수정 회차에 적용할 것]` 절 신설 — 같은 개념을 두 파일에서 고칠 때
  기준 대조, 검사 완화 시 기존 파괴 실험 재실행, 새 설정값 문서화 의무,
  설계 변경 시 주석 동기화, dry-run 류 읽기 전용 실측, 수정·검증 세션 분리.
  ③ 판정 기준에 "개수는 세어서 적어라" · "기록 문구의 방향·범위·개수를 코드에서
  확인하라" 추가(hometax 6차 기록 오류 4건이 전부 이 유형). ④ 마무리 순서를
  push → 재수령 확인 → 채팅 보고 로 고정하고, 변경 없어 빠진 파일은 명시하도록.

- v3.3 (2026-09-07) — I-4 반영. validate.py 검사 5개→12개, 인자에 상세지역 CSV 추가.
  점검표의 검사 개수·실행 명령·실측 예시를 그에 맞게 갱신.
- v3.2 (2026-09-07) — 개정안 1 채택. 이월 항목 목록을 checklist에서 제거하고
  이 파일을 단일 정본으로 지정. 앞으로 이월 항목은 위 "개선안" 표와
  아래 "다음 점검에서 대조할 것" 절만 갱신하면 된다.
- v3.1 (2026-09-07) — web_fetch 캐시 주의 절차 추가.
- v3 (2026-09-07) — 개정안 3·11 반영.
- v2 (2026-09-07) — 점검표를 저장소 정본(audit/checklist.md)으로 이관.

## 다음 점검에서 대조할 것
- ~~라이브 Pages 1287행 문구~~ — **종결.** 사용자 시크릿 창 확인 결과 라이브도 `01·07번 표에서`였다. web_fetch가 캐시된 옛 사본을 준 것이며, Pages 빌드·저장소 모두 정상. 앞으로 web_fetch 결과가 저장소와 다르면 캐시부터 의심할 것(checklist.md 2)번 절차에 반영).
- D-3~D-6 수정이 저장소에 남아 있는지(SKILL.md 57·152·219행, validate.py 검사 3, css-and-layout.md 버그 8).
- ~~I-1~I-5~~ — **전부 조치완료(2026-09-07 저녁).** 다음 회차에는 "반영이 유지되고 있는지"만 확인하고, 새 개선안을 찾아라.
- 새 절차가 실제 갱신 회차에서 작동하는지: 2-1단계(선확인)에서 실제로 멈추는지, 승인 발생 시 config·audit·화면 3곳이 같은 회차에 갱신되는지.
- validate.py 12개 검사 중 실 갱신에서 오탐이 나는 게 있는지. 특히 masthead 형식(`YYYY.MM.DD — MM.DD (N일)`)과 예산 비중 반올림.
- 검색어 CSV 클릭 합계 불일치는 아직 참고 출력에 머물러 있다(FAIL 아님). 다음 회차 개선안 후보.
- 노원M필라테스 4회·클릭 0 — 다음도 한 자릿수면 자연 소멸 규칙 적용 판단.
- 제외그룹 `노원필라테스(삭제)` 노출 지속 여부(8/26 5회·8/31 1회). 클릭이 생기면 validate.py 출력의 "클릭 N회 차이"와 08·09번 각주가 맞는지 확인.
- 미채택 개정안 1·2·4·5·7·8·9·10 재상정.

---

# 이전 기록 (원문 보존)

## 점검 기준선 (2026-09-07 오전)
점검일: 2026-09-07
결함 3건 / 개선안 5건 / 인용불가로 제외 1건
직전 기준선(2026-09-06) 대비: 해결 3건, 미해결 2건, 근거없음 0건, 신규 3건

점검 대상(전부 저장소에서 받은 것): `saero-ad-report-skill` @3d21640 — SKILL.md(234행) · README.md ·
references/report-structure.md(291) · references/css-and-layout.md(179) · scripts/validate.py(185) ·
audit/last-audit.md / `saero-pilates-report` index.html(1707행, 집계 2026.08.26—09.06 12일) ·
service-worker.js / 라이브 Pages(저장소 index.html과 일치 확인) / 설치본 부트스트랩(45행).
실사용 CSV는 이번 회차에 없어 배포본 숫자에 맞춘 합성 CSV로 validate.py를 실측했다.

## 이번 회차 조치 (2026-09-07 후속, 커밋 846af35)

사용자가 D-1 수정과 D-2 (a)안을 선택. 스킬 저장소 push 완료, 재clone으로 반영 확인.

- **D-1 조치완료** — SKILL.md 117행 목록에 `노원M필라테스` 추가.
  근본 원인 I-2는 미조치이므로 다음 승인 때 같은 일이 재발할 수 있음.
- **D-2 (a)안 — 부분 조치.** css-and-layout.md 21–22행·44행 규칙을
  "표 무관, 클릭률 전용"으로 확장. validate.py에 01번 검사 추가.
  **미완:** 배포본 index.html 1287행 `· <b>클릭률 강조</b>: 07번 표에서 클릭률
  4% 이상인 행만 진한 민트색으로 표시` 문구는 그대로다. 배포 토큰이 없어 못 고쳤다.
  화면 설명이 실물(01번에도 적용)과 어긋난 상태 → 다음 배포 때 반드시 함께 수정할 것.
- **D-3 미조치** — 실 CSV 확보 후 판정하기로 이월.
- **예정 외 조치: validate.py 0건 가드 추가.** 아래 "다음 점검에서 대조할 것"에 있던
  "07번 파싱 0행일 때 검사 4가 PASS 나는 경로"를 이번에 닫았다. 07번·01번 모두
  파싱 결과가 0건이면 PASS가 아니라 FAIL이다. I-4에서 이 항목은 빼도 된다.

### 이번 회차 추가 실측 (합성 CSV, KPI 클릭 110)

기준 PASS를 만든 뒤 한 곳씩 깨뜨려 전부 FAIL 확인:

- 01번 302행 5.22%에서 `.ctr-high` 제거 → FAIL(불일치 1건)
- 01번 311행 3.37%에 `.ctr-high` 추가 → FAIL(불일치 1건)
- 01번 섹션 주석 변조로 셀 0건 유도 → FAIL(0건 가드 동작)
- 07번 `name-cell` 클래스 변조로 행 0건 유도 → FAIL(0건 가드 동작)

01번 표 CTR 셀 전수 대조 결과(2.69·3.37·0.84 미적용 / 5.22·4.63 적용)로,
01번도 07번과 **동일한 4% 기준**을 지키고 있음을 확인. 의미 충돌이 아니라
문서가 좁게 적힌 것이었으므로 (b)안(01번에서 제거)은 근거 없음.

---

## 직전 기준선 판정

| 항목 | 판정 | 근거(지금 원문) |
|---|---|---|
| D-1 부트스트랩 clone 주소 | 해결됨 | 설치본 SKILL.md 18행 `git clone --depth 1 https://github.com/LeeKwanBeom/saero-ad-report-skill.git saero-skill` |
| I-1 배포본 최신 여부 선확인 단계 | 미해결 | SKILL.md 51행 `### 2단계. 집계 기간 검증` → 67행 `### 3단계. 제외 그룹 확인` → 72행 `### 4단계. 현재 배포본 가져오기` 사이에 대조 단계 없음 |
| I-2 승인 결과 기록 위치 | 미해결 | SKILL.md 124행 `3. 승인받은 뒤에만 경쟁사 표에 추가` — 절차가 여기서 끝나고 기록 위치·문서 갱신 규칙 없음 (결함 D-1의 원인) |
| 이월 나다운필라테스 제외 | 해결됨 | index.html 1004행 `"나다운필라테스"(노출53·클릭0)는 우리 상권과 무관한 곳으로 확인돼 이 표에서 빼고 제외 키워드 검토 목록에 두고 있음` |
| 이월 에반더필라테스상계역점·RHA필라테스상계 | 해결됨(자연 소멸 종결) | index.html 1221행 `"에반더필라테스상계역점"·"RHA필라테스상계"는 두 주 연속 노출 한 자릿수·클릭 0이라 더 추적하지 않음` — SKILL.md 135행 규칙 적용 |

## 결함

| # | 심각도 | 파일 | 줄 | 문제 원문(그대로) | 실측/추론 | 왜 틀렸는지 | 수정 방향 | 작업경로 |
|---|---|---|---|---|---|---|---|---|
| D-1 | 중 | SKILL.md | 116–117 | `이미 확인된 경쟁사 목록: 젠필라테스 · 이레필라테스 · 오운필라테스 ·` / `스마일필라테스 · 와우필라테스 · 퍼스트필라테스` | 실측 (배포본 07번 표와 대조) | 배포본 index.html 991행 `<td class="name-cell">노원M필라테스 <span …>(이번 주 신규)</span></td>`가 승인·배포됐는데 목록에 없다. 119–124행 규칙대로면 다음 실행에서 노원M필라테스를 다시 "새 후보"로 보고하고 멈춘다. 지금 이미 틀린 상태 | 목록에 노원M필라테스 추가. 근본 해결은 I-2(승인 시 목록 갱신 규칙) | saero-ad-report-skill push |
| D-2 | 하 | references/css-and-layout.md / index.html | 42 / 1287 | `.ctr-high     클릭률 4% 이상 강조(진한민트+굵게). 07번 전용` / `· <b>클릭률 강조</b>: 07번 표에서 클릭률 4% 이상인 행만 진한 민트색으로 표시` | 실측 | 배포본 01번 표에서 이미 쓰고 있다: index.html 302행 `<td class="num ctr-high">5.22%</td>`, 329행 `<td class="num ctr-high">4.63%</td>`. 문서와 집계 기준 문구가 실물과 다르고, validate.py는 07번만 검사해 01번 강조는 대조 밖 | (a) 규칙을 "CTR 4% 이상 셀 전용(01·07번)"으로 고치고 validate.py 검사 4를 01번까지 확장, 또는 (b) 01번에서 제거. 선택은 사용자 | (a) 스킬 저장소 push + index.html 1287행 배포 / (b) index.html 배포 |
| D-3 | 하 | SKILL.md | 57 vs 42 | `각 CSV의 `일별` 컬럼 최솟값이 `2026.08.26.`인지 확인한다.` vs `| 시간대별 보고서 | 09 | 시간대별/노출수/클릭수/클릭률/평균CPC/총비용 |` | 추론 — 실 CSV가 없어 시간대별 보고서 컬럼을 실측하지 못함 | 문서 자체가 시간대별 보고서에 `일별` 컬럼이 없다고 적어놓고 "각 CSV의 일별 컬럼"을 확인하라고 한다. 4개 중 1개는 이 절차를 그대로 수행할 수 없다 | 57행을 "일별 컬럼이 있는 3개 CSV"로 한정하고, 시간대별은 validate.py 검사 3(클릭 합계 = KPI)으로 기간 일치를 확인한다고 명시 | saero-ad-report-skill push |

## 개선안 (최대 5)

| # | 내용 | 이유 | 우선순위 |
|---|---|---|---|
| I-1 | (이월) 2단계 직후 배포본 masthead `집계 기간`(index.html 222행)과 CSV 일별 max를 대조해 같으면 계산 전에 사용자에게 먼저 묻는 단계 추가 | 2026-09-06 재발 사례 그대로. 이번 회차도 절차 미변경 | 1 |
| I-2 | (이월·확장) 승인 결과 기록 규칙: ① 경쟁사 채택 시 SKILL.md 116행 목록 갱신 ② 제외 판정(나다운·트리니티·웰니스·퀸즈·나인·씨앤미·벨·수현·예일 등)은 audit "경쟁사 판정 이력"에 남김 ③ 리포트에는 07번 각주·11번 (참고)·12번 액션 3곳 관행 명문화 | D-1이 이 규칙 부재로 생김. 배포본 1003·1221·1256행 관행은 유지 중이나 문서에 없음 | 2 |
| I-3 | 설정값 단일 출처 파일(`config/report-config.json` 등) 신설: 개업일(SKILL.md 54·57·61·63·65·203행 6곳 사본), 제외 그룹(SKILL.md 146행 + validate.py 29행), 경쟁사 목록(SKILL.md 116행), 타겟 지역(SKILL.md 175행), 01번 폭 규칙 80px/650px(SKILL.md 205 · report-structure 63 · css-and-layout 170행). validate.py가 이 파일을 읽게 함 | 지금 단일 출처 파일 없음(저장소 ls 실측). 한 곳만 고치면 어긋난다 | 3 |
| I-4 | validate.py 검증 범위 확장: KPI 타일 HTML 값(230·236·248행) vs CSV 대조(현재는 07번 표를 CSV와만 비교, 타일 자체는 미검사) · masthead 기간 vs CSV 일별 min/max · 04번 예산 비중 합 100.0 · 08·09번 "N회 차이" 각주 · 01번 min-width = 일수×80 · 섹션 주석 1~12 존재 · 상세지역 CSV 인자 추가 · 07번 파싱 0행이면 명시 FAIL(현재 "0행 검사"로 PASS 가능) · D-2 선택에 따라 01번 ctr-high 검사. 현재 손대지 않는 구간: KPI 타일·01~06·08·10~12 전부(09는 CSV끼리만) | SKILL.md 203~211행 수동 체크리스트 9개 중 6개가 기계 대조 가능 | 4 |
| I-5 | SKILL.md 배포 정보(25–26행)에 토큰이 두 종류임을 명시: 배포 = `saero-pilates-report` Contents R/W, 기준선·스킬 문서 push = `saero-ad-report-skill` Contents R/W. audit 갱신 절차도 SKILL.md에 한 줄 추가 | 지금 문서는 배포 토큰만 언급(스킬 저장소 이름은 부트스트랩에만 나옴). 점검 회차에 토큰을 잘못 받으면 push에서 막힘 | 5 |

## 경쟁사 판정 이력

| 후보 | 판정 | 근거 | 일자 |
|---|---|---|---|
| 젠·이레·오운·스마일·와우·퍼스트필라테스 | 채택(표) | 노원·도봉구 실제 업체 | ~09-05 |
| 퍼스트필라테스아카데미노원 | 채택(표기 변형, 별도 승인 불필요) | SKILL.md 126행 규칙 | 09-05 |
| 노원M필라테스 (변형 M필라테스노원·노원엠필라테스) | 채택(표) — SKILL.md 117행 반영 완료(09-07) | 노원구 소재 확인, index.html 991·1221행 | 09-06 |
| 나다운필라테스 | 제외 | 구로 신도림/인천 검단, 확장검색 오매칭. 제외 키워드 검토 목록 | 09-05 확정 |
| 트리니티·웰니스·퀸즈·나인·씨앤미·벨·수현·예일필라테스 | 제외 | 한 자릿수 노출, 상권 무관(index.html 1004행) | 09-06 |
| 에반더필라테스상계역점 · RHA필라테스상계·상계동 | 종결(자연 소멸) | 2주 연속 한 자릿수·클릭 0(index.html 1221행). 다시 묻지 않음 | 09-06 |

## 점검표 개정안

1. **삭제**: "config/report-config.json 과 scripts/check_csv.py 가 어디 있는지" — 스킬 저장소·설치본 어디에도 없고(ls 실측), 어떤 문서도 참조하지 않는다(grep 0건). 존재하지 않는 파일이므로 결함이 아니다. 단일 출처 파일은 I-3로 새로 만드는 것이 맞다.
2. **전제 수정**: 점검표는 "스킬 저장소만 고치고 배포를 안 했을 것"을 걱정하는데, 이번엔 반대였다 — 배포(09-06, 12일치)는 됐고 스킬 문서가 안 따라왔다(D-1). 점검 방향을 양방향으로: "배포본에 새로 들어간 판정·행이 SKILL.md·audit에 반영됐는지"를 항목으로 추가.
3. **전제 수정**: 이월 항목 에반더·RHA는 SKILL.md 135행 자연 소멸 규칙으로 종결됐고 배포본에 명시됐다. 다음 점검표에서 이월 목록에서 빼고, "경쟁사 판정 이력" 표만 유지.
4. **추가**: 라이브 Pages와 저장소 index.html이 같은지 확인(이번엔 일치). Pages 빌드 실패·캐시로 어긋날 수 있는데 점검표에 없었다.
5. **추가**: 점검 요청에 최근 CSV 4종을 함께 올릴 것. 없으면 CSV 관련 항목(인코딩, 숫자 포맷, 컬럼명, 기간 불일치, 빈 데이터)은 합성 데이터로만 실측되고 실 데이터 조건은 [추론]으로 남는다. 이번 회차 D-3과 "인용불가 제외 1건"이 그 예.
6. **축소(매번 통과)**: 섹션 주석 1~12 존재 / .wide-table 고정 px 부재 / service-worker network-first / 12번 표 .wide-table 미부착 — 배포본 파일 구조가 바뀌지 않는 한 항상 통과한다. 섹션 주석은 I-4로 validate.py에 넣고 점검표에서 빼고, service-worker.js는 파일 해시 변경 시에만 재확인.
7. **축소**: "설치본 부트스트랩 clone 주소" — 부트스트랩은 사용자가 재업로드하지 않으면 바뀌지 않는다. 재업로드한 회차에만 확인.
8. **명시**: "validate.py 4개 검사 각각 깨뜨려 FAIL 확인" 방법을 점검표에 적어둘 것 — 배포본 숫자에 맞춘 합성 CSV(KPI 클릭 110 등)로 기준 PASS를 만든 뒤 각 검사에 대응하는 한 곳만 바꾼다. 이번 회차 결과: 태그 짝(div 제거→FAIL div 174/175) · 07클릭합(28→27→FAIL 109≠110) · 09시간대(CSV −1→FAIL 109 vs 110) · CTR(3.18% 강조 추가→FAIL / 4.71% 강조 제거→FAIL). 4개 전부 살아 있음.
9. **명시**: "데이터가 비거나 1건일 때 죽는 코드" — 컬럼 헤더만 있는 CSV·1행 CSV는 크래시 없이 FAIL로 끝남(실측). 기간 헤더 한 줄만 있는 파일은 EmptyDataError로 죽지만 그런 파일이 네이버에서 나오는지 확인 못함. 다음엔 실 CSV로 판정.
10. **주의**: "차트 색 배정(플레이스=민트/파워링크=잉크) 준수 여부" 항목은 02·10번처럼 데이터셋이 지표(노출/클릭)인 차트에는 적용할 수 없다(index.html 1380–1381·1611–1612행은 지표별 색). 규칙 문구(report-structure 41–42행 "모든 차트에서")를 "광고 유형이 데이터셋인 차트에서"로 좁히거나 점검 항목을 그렇게 읽을 것. 결함으로 올리지 않음.

## 다음 점검에서 대조할 것

- D-1·D-2·D-3 수정 여부. D-2는 사용자 선택(a/b)에 따라 확인 위치가 다름.
- I-1~I-5 반영 여부(순위 순).
- 실 CSV로 실측 못 한 것: 인코딩, 천단위 콤마(합성 `"3,727"`은 validate.py 126행 `int(...sum())`에서 ValueError로 죽음 — 실 CSV가 그 포맷인지 미확인이라 결함 아님, 인용불가 제외 1건), 시간대별 보고서 컬럼 구성(D-3 근거), 상세지역 CSV 기간이 다를 때 08번 누락 여부.
- ~~validate.py 07번 파싱이 0행일 때 검사 4가 PASS 나는 경로~~ — **2026-09-07 해결.** 0건 가드 추가로 07번·01번 모두 0건이면 FAIL. I-4에서 제외.
- **배포본 index.html 1287행 클릭률 강조 문구** — D-2 (a)안의 미완 항목. 다음 배포 때 "07번 표에서"를 "01·07번 표에서"로 고쳤는지 확인.
- 배포본 06번 rankChart min-width 960px(index.html 675행)는 문서에 규칙이 없다. 01번처럼 날짜 수에 따라 늘려야 하는지 사용자 확인 필요.
- 노원M필라테스 노출 추이(2회, 변형 포함 4회). 한 자릿수 지속이면 자연 소멸 규칙 적용 대상인지 판단.

---

## 이전 기록 (2026-09-06, 원문 보존)

점검 대상: 부트스트랩 `/mnt/skills/plugins/saero-ad-report/SKILL.md`,
저장소 `SKILL.md` · `references/` · `scripts/validate.py`
실사용 데이터: 2026.08.26–09.05 CSV 4종

### 결함

**D-1. 부트스트랩이 배포 저장소를 clone하도록 돼 있었음 — 해결됨(2026-09-06 확인)**

- 위치: 설치본 `SKILL.md` 14–17행
- 원문: `git clone --depth 1 https://github.com/LeeKwanBeom/saero-pilates-report.git saero-skill`
- 증상: `saero-pilates-report`에는 `index.html` 등 배포 산출물만 있고 `SKILL.md`가
  없다. 부트스트랩 2절 규칙대로면 여기서 작업이 멈춘다. 스킬 본체는
  `LeeKwanBeom/saero-ad-report-skill`에 있다.
- 조치: 주소를 `saero-ad-report-skill`로 고친 부트스트랩을 사용자에게 전달,
  플러그인 설정에서 교체 예정. 두 저장소가 다르다는 경고 문구도 추가.
- 확인(2026-09-06, 새 세션): 설치본 부트스트랩이 교체된 상태로 풀렸고, 거기 적힌
  주소로 clone하니 스킬 본체 저장소 `LeeKwanBeom/saero-ad-report-skill`를 받아왔다.
  → 해결됨으로 판정.

### 개선안

**I-1. 배포본이 이미 최신인지 먼저 확인하는 단계가 없음** — 2026-09-07 미해결, 위 표로 이월.

**I-2. 승인 대기 항목의 결론을 리포트에 어떻게 남길지 규칙이 없음** — 2026-09-07 미해결, 위 표로 이월.

### 근거없음 / 확인만

- `validate.py` 4개 검사 전부 통과 (태그 짝 · 07번 클릭 합계 100 · 09번 클릭 합계 100 ·
  `.ctr-high` 11행 불일치 0건). 스크립트 자체 문제 없음.
- 제외 그룹 자동 감지 규칙 정상 동작: `노원필라테스(삭제)`만 조건 해당, 신규 후보 없음.
- 04번 예산 비중 합계 100.0% 검산 통과. 단순 반올림은 100.1%가 되므로 최대잔여법으로 맞춰야 한다.

### 이월 사항 (2026-09-07에 "경쟁사 판정 이력" 표로 통합)

- `나다운필라테스` — 경쟁사 아님으로 확정. 다시 후보로 올리지 말 것.
- `에반더필라테스상계역점` · `RHA필라테스상계`·`RHA필라테스상계동` — 소재지 확인불가, 한 자릿수. 다음 주에도 한 자릿수면 자연 소멸.
