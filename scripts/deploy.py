#!/usr/bin/env python3
"""배포본 index.html 받기·올리기(4·7단계)와 배포 뒤 공개 사이트 반영 확인(7단계 뒤) — 계산 로직 없음.

사용법(Code 탭 — references/code-tab.md):
    $PY scripts/deploy.py fetch  --out <index.html> [--token-file <파일>]
        GET contents API(무인증 먼저) → 파일 저장, sha 출력.
    $PY scripts/deploy.py push   --file <index.html> --base <4단계 fetch 파일> --message "<커밋 메시지>" [--dry-run] [--token-file <파일>]
        sha를 **다시 조회**한 뒤 PUT. 그 조회 본문 md5 ≠ --base md5면 "[FAIL] 배포본이 4단계 fetch 뒤 바뀜" exit 1(PUT 0).
        실제 push는 --base 필수(없으면 exit 2, --file 없이 --base만 줘도 exit 2) · 작업본 옆 precheck 도장(precheck_ok.md5 — precheck.sh가
        전부 통과했을 때 쓴 작업본 md5) = --file md5일 때만 PUT(아니면 "[FAIL] precheck 통과본이 아님" exit 1, dry-run은 [주의]).
        도장 = 작업본 md5 · 직전 배포본 md5(= --base여야) · 모드(pending이면 [주의]만). PUT 결과 모름(요청 예외·5xx) = 재PUT 금지·verify 먼저,
        PUT 409 = 배포본이 GET 뒤 바뀜(sha 불일치) · 403 = 쓰기 권한 없음 · 404 = 저장소·경로 없음(권한 부족도 404) — 넷 다 [FAIL] exit 1.
        GET 본문이 --base와 다른데 작업본과 같으면 "앞 PUT이 이미 반영됨" exit 0(PUT 안 함). 인자 오류(--file·--out 없음)는 GET 전에 exit 2.
        레이아웃 판 게이트(2026-10-06 회차 2, 막음 M4): --file 과 --base 의 `<meta name="report-layout" content="…">` 가 다르면(한쪽 없음 포함)
        실제 push 는 `--layout-change` 없이 "[FAIL] 레이아웃 판이 바뀜 — PUT 안 함" exit 1(네트워크 전 — GET·PUT 0), dry-run 은 [주의]만.
        같으면 아무것도 찍지 않는다(데이터 회차엔 안 걸림). `--layout-change` 는 첫 적용 회차에 사용자가 작업본 화면을 보고 "배포"라고 했을 때만 붙인다.
        --dry-run 은 sha 조회·base 대조·자격 증명 확인·쓰기 권한 확인
        (인증 GET /repos/{deploy_repo}의 permissions.push — 계정 역할 기준, 토큰 범위는 PUT이 최종 확인. 참/거짓만 찍고 거짓이면 [FAIL])·본문 준비까지만 하고 PUT을 보내지 않는다
        (아무 파일도 쓰지 않는다 — 2026-09-26 실측). "자격 증명 확인됨(출처: token-file|git)"만 찍는다.
        --dry-run 은 --file 없이도 된다(S0 사전 점검 — sha·자격 증명·쓰기 권한만 확인).
        성공 줄은 `저장소 반영 커밋 <40자> …`(2026-10-11 — "배포 완료"는 live exit 0 의 `기록 머리:` 줄에서만 나온다).
    $PY scripts/deploy.py verify --file <index.html> [--ref <커밋 sha>] [--token-file <파일>]
        배포 후 재수령본 md5 = 로컬 md5 인지. 다르면 exit 1 — 다시 PUT하지 않는다(재PUT은 사용자 결정).
        --ref = push 성공 줄이 찍은 커밋 sha(16진 7~40자, 아니면 GET 전에 exit 2) — 있으면 `?ref=`로 그 커밋의 본문을 받는다.
        ref 없는 contents GET은 PUT 직후 약 1분 옛 본문을 돌려줄 수 있다(2026-09-29 실측 2회 — 요청의 no-cache로도 안 막힘).
        그래서 7단계는 push → verify --ref <push가 찍은 커밋>. ref 없이 불일치면 캐시일 수 있다는 문구(ls-remote HEAD와 --ref로 다시 verify — 읽기, 재PUT 금지).
        --ref 일치면 배포 저장소 HEAD(·HEAD 커밋)를 읽어 다음 live 의 --commit 을 고른다(2026-10-11 B-7): HEAD 메시지가 재배포 접두이고 부모 = --ref 면 HEAD,
        아니면 --ref → `다음(읽기): deploy.py live … --commit <40자>`(무인증 GET 1~2 — 403·429 면 자격 증명 1회).
    $PY scripts/deploy.py live --file work/index.html --prev work/prev.html --commit <40자> [--since <ISO>] [--seen <공개 md5>] [--token-file <파일>]
        (읽기만 — 2026-10-11 안 B) 공개 사이트가 작업본을 내보내는지 확인. 네트워크 전: --commit 40자 · md5(--file) = 작업본 옆 도장 1행 ·
        md5(--prev) = 2행 · 둘이 다름(아니면 exit 2) · 옛 live_ok 를 지움. 이 커밋의 Pages 실행(config live_check.pages_workflow)을 무인증 API 로 폴
        (첫 폴 = 시작, 다음 = max(t0 + api_poll_s[i], 앞 폴 + 60초), 첫 폴 포함 api_poll_max 번) → success 뒤에만 공개 GET(gzip 풀어 · 쿼리 없음 ·
        Authorization 0 — 403·429·5xx 에도) → md5 = 작업본이면 작업본 옆 live_ok(커밋 sha · 공개 md5)를 쓰고 `기록 머리: 배포 완료 `<sha7>`` exit 0.
        t0 + cap_s 안에 success 아님 → 공개 GET 1회(= 작업본이면 exit 0 "다른 실행이 올림") → 상태 읽기(api_status_max 안) → [멈춤] exit 1 +
        재배포 질문(사용자 결정 4 문구 · --commit 이 재배포 커밋이면 "GitHub 쪽 대기 — 기다림(재배포 1/1)"). 실행이 --since(없으면 시작) 뒤 60초가 지나도
        없으면 [멈춤] Pages 실행 없음 exit 1. CDN(실행 success · 옛 판 · 그 객체를 CDN 이 완료 전에 확인)은 max(t0 + cdn_floor_s, 완료 + cdn_max_age_s + cdn_extra_s)
        까지 기다려 exit 3(재배포 권하지 않음) · 한 번 실행은 run_max_s 안(넘으면 exit 3 — 같은 명령 한 번 더). exit 1·3 에도 `기록 머리:` 한 줄.
        live_ok 자리는 작업본 옆 — 환경 변수 SAERO_LIVE_OK(리허설·시험 전용 — 운영 회차 금지)가 있으면 그 경로(첫 줄에 찍는다).
    $PY scripts/deploy.py redeploy --file work/index.html --prev work/prev.html --commit <40자> [--confirm] [--token-file <파일>]
        (빈 커밋 — Git Data API · 사용자 답 '재배포' 원문 뒤에만 실제) 기본 dry-run(쓰기 0) — 실제는 같은 명령에 --confirm. 순서: 도장 →
        (e) 자격 증명·권한 → (b) 공개 GET(이미 작업본 → 쓰기 0 exit 0) → (a) 인증 GET HEAD = --commit → (d) HEAD 메시지가 재배포 접두면
        "[FAIL] 이미 재배포함 — 두 번째 없음 · 쓰기 0" → (c) 이 커밋 실행이 2분 안 움직였으면 쓰기 0 → 쓰기 POST /git/commits {tree: HEAD tree,
        parents: [HEAD]} 1 + PATCH /git/refs/heads/main {force: false} 1. 결과 모름 = 재시도 0(PATCH 면 60초 뒤 인증 GET 으로 판정 · 재배포 1/1 로 셈).
        dry-run 은 멈춤 판정이 나와도 남은 읽기와 쓰기 요약을 끝까지 찍고 끝 줄 "실제였다면 <첫 멈춤>에서 멈춤 — 쓰기 0"(exit = 첫 멈춤 기준).
    $PY scripts/deploy.py public --file <파일>
        (진단·4단계 뒤 대조 — 읽기) 공개 주소 무압축 GET 1(사용자 gzip 객체를 심지 않음 · API 0) → md5 같음 exit 0 / 다름 [주의] exit 1 / 못 읽음 exit 1.

자격 증명(2026-09-28 Code 탭 회차):
  - GET(fetch·verify·push 전 sha)은 무인증으로 먼저 보내고, 403·429(무인증 rate limit)일 때만 자격 증명으로 1회 다시 보낸다.
  - PUT은 --token-file이 있으면 그 파일, 없으면 이 PC의 git 자격 증명(`git credential fill`, github.com)을 subprocess로 얻는다
    (credential.interactive=false · GIT_TERMINAL_PROMPT=0 · GCM_INTERACTIVE=never · askpass 변수 제거 — 창·프롬프트를 띄우지 않는다). 못 얻으면 [FAIL] exit 1.
  - 자격 증명 값은 변수에만 둔다 — 출력·파일·로그·예외 문구 어디에도 남기지 않는다(한 줄 토큰 형식이 아니면 쓰지 않고,
    요청 예외는 종류만 — 네트워크 연결 오류만 소켓 사유 문구, 헤더 값 없음. 서버·프록시가 되돌려 준 오류 문구 속 자격 증명 값은 `***`로 바꾼다). --token-file은 바이트로 읽어 UTF-16(BOM FF FE·FE FF)과
    UTF-8(BOM 허용)을 가리고, 없거나 못 읽으면 "[FAIL] 자격 증명을 얻지 못함(출처: token-file)"(Traceback 없음).
    `push --dry-run`은 값을 얻은 뒤 인증 GET(읽기)으로 배포 저장소 permissions.push까지 본다(2026-09-28 수정 회차 2 N1 — 계정 역할 기준이라
    fine-grained 토큰의 저장소·권한 범위는 PUT이 최종 확인한다). 저장소는 config deploy_repo.
  - 공개 주소(config deploy_site_url)·GitHub 상태(config live_check.status_url) GET 은 한 함수씩 — 어떤 응답에도 자격 증명을 얻지도 싣지도 않는다(2026-10-11 C-10).
  - 시각은 전부 time.time() 하나에서(시험은 가짜 시계) · 공개 주소·GitHub 상태도 urllib.request.urlopen 으로 보낸다(시험의 가짜를 지나치지 않게).
"""
import argparse
import base64
import calendar
import email.utils
import gzip
import hashlib
import http.client
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

from reportlib import load_config

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — fetch_reports.py·exclusions.py와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

CFG = load_config()
STAMP = "precheck_ok.md5"  # precheck.sh가 전부 통과했을 때 작업본 옆에 쓰는 도장(작업본 md5 · 직전 배포본 md5 · 모드 full|pending)
REPO_API = f"https://api.github.com/repos/{CFG['deploy_repo']}"
API = f"{REPO_API}/contents/index.html"


def usable(tok):
    """헤더에 넣을 수 있는 GitHub 토큰 모양인지(`[A-Za-z0-9_]+` — ghp_·gho_·github_pat_ 모두). 아니면 None — 값은 어디에도 찍지 않는다
    (개행이 든 값을 헤더에 넣으면 http.client가 값 전체를 예외 문구에 담고, 기호가 섞이면 *** 가림이 덜 된다)."""
    return tok if tok and re.fullmatch(r"[A-Za-z0-9_]+", tok) else None


def token_of(path):
    """--token-file 값. 바이트로 읽어 BOM FF FE·FE FF면 UTF-16(Windows PowerShell 5.1의 `'…' > 파일` 기본), 아니면 utf-8-sig
    (메모장·`Out-File -Encoding utf8`의 BOM은 벗긴다). 없거나 못 열거나 못 읽으면 None — 호출한 쪽이 [FAIL](값·Traceback 출력 0)."""
    try:
        with open(os.path.expanduser(path), "rb") as f:
            raw = f.read()
        text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig")
    except (OSError, UnicodeError):
        return None
    return usable(text.strip())


def git_credential():
    """이 PC git 자격 증명(github.com)의 비밀 값. 못 얻으면 None. 값은 돌려주기만 한다(출력·기록 0).
    창·프롬프트를 띄우지 않는다: credential.interactive=false · GCM_INTERACTIVE=never · GIT_TERMINAL_PROMPT=0 · askpass 변수 제거."""
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_ASKPASS", "SSH_ASKPASS")}
    env.update({"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"})
    try:
        r = subprocess.run(["git", "-c", "credential.interactive=false", "credential", "fill"],
                           input="protocol=https\nhost=github.com\n\n",
                           capture_output=True, text=True, encoding="utf-8", env=env, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        if line.startswith("password="):
            return usable(line[len("password="):].strip())
    return None


HINT = {"git": "이 PC git 자격 증명(github.com 로그인)을 사용자가 확인",
        "token-file": "토큰 파일이 한 줄 토큰(영문·숫자·밑줄만)인지 사용자가 확인"}


def credential(token_file):
    """(값, 출처). 출처 = "token-file" | "git". 값이 None이면 못 얻은 것."""
    if token_file is not None:  # --token-file ''(빈 문자열)도 token-file — git 자격 증명으로 몰래 넘어가지 않는다
        return token_of(token_file), "token-file"
    return git_credential(), "git"


def api_full(token, method="GET", body=None, url=API):
    """GitHub API 요청 하나 → (status, JSON 본문, 소문자 키 응답 헤더). 요청 예외는 status 0."""
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None)
    if token:
        req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    if method == "GET":
        req.add_header("Cache-Control", "no-cache")  # 무인증 응답은 공용 캐시(max-age 60). 이것으로도 PUT 직후 옛 본문이 왔다(2026-09-29 2회) — verify는 --ref
    if body:
        req.add_header("Content-Type", "application/json")

    def mask(text):  # 서버·프록시가 요청 헤더를 되돌려 줘도 쓰는 자격 증명 값이 출력에 새지 않게(자른 뒤가 아니라 자르기 전에)
        return text.replace(token, "***") if token else text

    def heads(obj):
        h = getattr(obj, "headers", None) or {}
        try:
            return {str(k).lower(): str(v) for k, v in h.items()}
        except AttributeError:
            return {}

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode()), heads(r)
    except urllib.error.HTTPError as e:
        return e.code, {"message": mask(e.read().decode(errors="replace"))[:300]}, heads(e)
    except urllib.error.URLError as e:
        return 0, {"message": mask(f"네트워크 오류: {e.reason}")}, {}
    except (ValueError, OSError, http.client.HTTPException) as e:  # 예외 문구에 헤더 값이 들어갈 수 있어 종류만 찍는다
        return 0, {"message": f"요청 실패({type(e).__name__})"}, {}


def api(token, method="GET", body=None, url=API):
    status, res, _ = api_full(token, method, body, url)
    return status, res


def get(token_file, url=API):
    """무인증 GET → 403·429면 자격 증명으로 1회. (status, res, 인증 출처 또는 None). url = API 또는 API?ref=<커밋>(verify --ref)."""
    status, res = api(None, url=url)
    if status in (403, 429):
        tok, src = credential(token_file)
        if not tok:
            return status, res, None
        status, res = api(tok, url=url)
        return status, res, src
    return status, res, None


def md5(data):
    return hashlib.md5(data).hexdigest()


def precheck_stamp(path, data, base=None):
    """작업본 옆 도장(precheck_ok.md5 — 1줄 `<작업본 md5>  <이름>` · 2줄 `<직전 배포본 md5>  <이름>` · 3줄 `mode full|pending`)을 본다
    → (통과, 사유, pending). data = main이 한 번만 읽은 --file 바이트(PUT 본문과 같은 바이트), base = --base 바이트(있으면).
    통과 = 작업본 md5 같음 + 형식(직전 배포본·모드 줄) + 직전 배포본 md5 = --base md5(4단계를 다시 받았으면 precheck도 다시).
    pending = --pending으로 통과한 도장(막지 않고 호출한 쪽이 [주의]). 도장은 precheck.sh가 전부 통과했을 때만 쓴다."""
    sp = os.path.join(os.path.dirname(os.path.abspath(path)), STAMP)
    cur = md5(data)
    try:
        with open(sp, encoding="utf-8") as f:
            rows = [ln.split() for ln in f.read().splitlines() if ln.strip()]
    except FileNotFoundError:
        return False, f"도장 없음: {sp}", False
    except (OSError, UnicodeError) as e:  # 손으로 쓴·다른 인코딩 도장 — Traceback 대신 사유(실제 push는 [FAIL], dry-run은 [주의])
        return False, f"도장을 읽을 수 없음({type(e).__name__}): {sp}", False
    want = rows[0][0] if rows else ""
    prev = rows[1][0] if len(rows) > 1 else None
    mode = rows[2][-1] if len(rows) > 2 else None
    pending = mode == "pending"
    if want != cur:
        return False, f"도장 md5 {want[:8]} ≠ 작업본 md5 {cur[:8]} — precheck 뒤 바뀌었거나 다른 파일", pending
    if prev is None or mode not in ("full", "pending"):
        return False, "도장 형식이 옛 판(직전 배포본·모드 줄 없음) — precheck.sh를 다시", pending
    if base is not None and prev != md5(base):
        return False, f"도장의 직전 배포본 md5 {prev[:8]} ≠ --base md5 {md5(base)[:8]} — 4단계를 다시 받았으면 5·6단계부터", pending
    return True, f"precheck 도장 = 작업본 md5 {cur[:8]}… · 직전 배포본 {prev[:8]}… 확인", pending


LAYOUT_META = re.compile(rb'<meta name="report-layout" content="([^"]*)">')


def layout_of(data):
    """배포본 바이트의 레이아웃 판 meta 값(없으면 None — 옛 판)."""
    m = LAYOUT_META.search(data)
    return m.group(1).decode("utf-8", "replace") if m else None


def push_permission_ok(tok):
    """인증 GET /repos/{deploy_repo}(읽기)로 permissions.push를 본다 — 참/거짓만 찍는다(값·응답 본문 출력 0). 참이면 True."""
    status, res = api(tok, url=REPO_API)
    if status != 200:
        print(f"[FAIL] 배포 저장소 권한 조회 실패(인증 GET /repos/{CFG['deploy_repo']} → {status}: {res.get('message', '')[:120]}) — 자격 증명이 유효한지 사용자가 확인")
        return False
    perm = (res.get("permissions") or {}).get("push")
    print(f"배포 저장소 쓰기 권한(permissions.push): {'참' if perm is True else '거짓'}")
    if perm is not True:
        print(f"[FAIL] 이 자격 증명은 배포 저장소({CFG['deploy_repo']})에 쓰기 권한이 없음 — PUT이 거부된다. 사용자가 계정·권한 확인")
        return False
    return True


# ---------------------------------------------------------------- 배포 뒤 공개 사이트 확인(live · redeploy · public — 2026-10-11 안 B)
SITE = CFG["deploy_site_url"]
LC = CFG["live_check"]
REDEPLOY_PREFIX = LC["redeploy_message"].split("{", 1)[0]   # 이 접두로 시작하는 커밋 = 이미 재배포함(07f4a96 손 커밋 포함 — 의도)
LIVE_OK = "live_ok"            # live exit 0 이 작업본 옆에 쓰는 기록(커밋 sha · 공개 md5) — leads.py guard 가 회차 머리 "배포 완료"와 대조
LIVE_OK_ENV = "SAERO_LIVE_OK"  # 리허설·시험 전용 live_ok 경로 덮어쓰기(운영 회차 금지 — guard 는 이 경로를 읽지 않는다)
API_CACHE_S = 60               # 무인증 API 응답 s-maxage(2026-10-11 실측) — 같은 URL 폴 간격의 하한
RUN_WAIT_S = 60                # 실행이 생기기를 기다리는 상한(--since·시작 뒤)
SINCE_SLACK_S = 5              # --since 앞 이 초 안에 생긴 실행까지 이 재배포의 실행으로 본다(시계 차)
MOVING_S = 120                 # redeploy (c): 이 초 안에 updated 된 미완료 실행 = 움직이는 중
AFTER_LOOKS = 2                # 실행 완료 뒤 확인된 옛 판을 몇 번 더 보고 멈출지(A-7)
PUBLIC_FAIL_MAX = 3            # 공개 GET 이 잇달아 이만큼 실패하면 확인 못 함
SHA40 = re.compile(r"[0-9a-f]{40}")
MD5_HEX = re.compile(r"[0-9a-f]{32}")
ISO_RE = re.compile(r"(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(?:\.\d+)?(Z|[+-]\d\d:?\d\d)?$")
HEAD_FORM = re.compile(r"배포 완료 `([0-9a-fA-F]{7,40})`")   # 회차 머리 꼴 줄(`## ` 로 시작)의 sha — K3 guard


def dig(obj, *keys):
    """중첩 dict 에서 값 — 없거나 꼴이 다르면 None."""
    for k in keys:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(k)
    return obj


def sha_at(obj, *keys):
    """중첩 dict 의 커밋 sha(16진 40자) — 아니면 ""."""
    v = dig(obj, *keys)
    return v if isinstance(v, str) and SHA40.fullmatch(v) else ""


def now():
    """모든 시각·경과·HH:MM 의 단일 출처(datetime.now·time.monotonic 0 — 시험은 time.time·time.sleep 을 가짜 시계로 바꾼다)."""
    return time.time()


def kst(t, sec=False):
    return time.strftime("%H:%M:%S" if sec else "%H:%M", time.gmtime(t + 9 * 3600))


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def iso_epoch(s):
    """GitHub ISO 시각(Z·±HH:MM) → epoch 초. 꼴이 다르면 None."""
    m = ISO_RE.match(s) if isinstance(s, str) else None
    if not m:
        return None
    y, mo, d, h, mi, se, tz = m.groups()
    t = calendar.timegm((int(y), int(mo), int(d), int(h), int(mi), int(se), 0, 0, 0))
    if tz and tz != "Z":
        off = int(tz[1:3]) * 3600 + int(tz[-2:]) * 60
        t -= off if tz[0] == "+" else -off
    return t


def http_epoch(s):
    """HTTP Date 헤더 → epoch 초(없거나 꼴이 다르면 None)."""
    try:
        p = email.utils.parsedate_tz(s) if s else None
        return email.utils.mktime_tz(p) if p else None
    except (TypeError, ValueError, OverflowError):
        return None


def public_get(gz=True):
    """공개 주소 GET 한 함수(live·redeploy (b)·public) — 쿼리 없음 · Authorization 0 · 어떤 응답(403·429·5xx)에도 credential() 호출 0.
    gz=True 면 Accept-Encoding: gzip(사용자 브라우저와 같은 CDN 객체) 받아 풀고, False 면 헤더 없이(무압축 객체 — 사용자 객체를 심지 않음).
    → (status, 본문 바이트 또는 None, 소문자 키 헤더, 사유)."""
    req = urllib.request.Request(SITE)
    if gz:
        req.add_header("Accept-Encoding", "gzip")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, raw = r.status, r.read()
            hdr = {str(k).lower(): str(v) for k, v in (getattr(r, "headers", None) or {}).items()}
    except urllib.error.HTTPError as e:
        return e.code, None, {str(k).lower(): str(v) for k, v in (getattr(e, "headers", None) or {}).items()}, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return 0, None, {}, f"네트워크 오류: {e.reason}"
    except (ValueError, OSError, http.client.HTTPException) as e:
        return 0, None, {}, f"요청 실패({type(e).__name__})"
    if hdr.get("content-encoding", "").lower() == "gzip":
        try:
            raw = gzip.decompress(raw)
        except (OSError, EOFError, ValueError) as e:
            return status, None, hdr, f"gzip 풀기 실패({type(e).__name__})"
    if status != 200:
        return status, None, hdr, f"HTTP {status}"
    return status, raw, hdr, ""


def plain_json(url):
    """GitHub 상태(status_url — GitHub API 한도 밖) GET 한 함수 — 자격 증명 0. → (JSON 또는 None, 사유)."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=60) as r:
            return json.loads(r.read().decode()), ""
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"네트워크 오류: {e.reason}"
    except (ValueError, OSError, http.client.HTTPException) as e:
        return None, f"요청 실패({type(e).__name__})"


class Gh:
    """live·redeploy·verify 의 GitHub API 읽기 — 무인증 먼저, 403·429 면 자격 증명을 1회 얻어 그 뒤는 인증으로(IP 60/h 를 안 씀).
    무인증·인증 수를 센다(값은 변수에만 — 출력 0)."""

    def __init__(self, token_file, tok=None, src=None):
        self.token_file, self.tok, self.src = token_file, tok, src
        self.tried = tok is not None
        self.unauth = self.auth = 0
        self.note = ""        # 무인증 제한 사유(리셋 시각)

    def get(self, url):
        if self.tok is None:
            self.unauth += 1
            st, res, hdr = api_full(None, url=url)
            if st not in (403, 429):
                return st, res
            reset = hdr.get("x-ratelimit-reset", "")
            self.note = f"무인증 {st}" + (f" — 리셋 {kst(int(reset))}" if reset.isdigit() else "")
            if self.tried:
                return st, res
            self.tried = True
            self.tok, self.src = credential(self.token_file)
            if not self.tok:
                self.note += f" · 자격 증명 못 얻음(출처: {self.src})"
                return st, res
            print(f"무인증 API 제한({st}) → 자격 증명으로 다시 읽음(출처: {self.src})")
        self.auth += 1
        st, res, _ = api_full(self.tok, url=url)
        return st, res

    def why(self, st, res):
        msg = (res or {}).get("message", "") if isinstance(res, dict) else ""
        return self.note if st in (403, 429) and self.note else f"GET {st}{': ' + msg[:120] if msg else ''}"


def pick_run(res, commit, since=None):
    """runs 응답에서 이 커밋의 Pages 실행(name = pages_workflow) 중 created_at 이 가장 늦은 것. --since 가 있으면 created_at ≥ since − 5초만(C-6).
    응답 꼴이 다르면 ValueError."""
    runs = res.get("workflow_runs") if isinstance(res, dict) else None
    if not isinstance(runs, list):
        raise ValueError("workflow_runs 없음")
    got = []
    for r in runs:
        if not isinstance(r, dict) or r.get("name") != LC["pages_workflow"] or r.get("head_sha") != commit:
            continue
        c = iso_epoch(r.get("created_at"))
        if c is None or (since is not None and c < since - SINCE_SLACK_S):
            continue
        got.append((c, r))
    return max(got, key=lambda x: x[0])[1] if got else None


def run_word(run):
    s = run.get("status") or "?"
    return f"{s} {run.get('conclusion')}" if s == "completed" else s


def commit_info(run):
    """실행 객체의 head_commit → (메시지, 커밋 시각 epoch). 없으면 ("", None)."""
    hc = (run or {}).get("head_commit") or {}
    return hc.get("message") or "", iso_epoch(hc.get("timestamp"))


def head_line(c7, kind=None):
    """`기록 머리:` 한 줄 — exit 0(kind None)만 "배포 완료", 그 밖은 저장소 반영 · 공개 미반영(GitHub 쪽 대기 | CDN 캐시 | 확인 못 함)."""
    if kind is None:
        return f"기록 머리: 배포 완료 `{c7}`"
    return f"기록 머리: 저장소 반영 `{c7}` · 공개 미반영({kind})"


def redeploy_question(num):
    """사용자 결정 4 문구 그대로(실행이 없으면 '#n' 자리만 '없음(Pages 실행이 안 생김)')."""
    what = f"멈춘 실행 #{num}" if num is not None else "멈춘 실행 없음(Pages 실행이 안 생김)"
    return (f"{what} — Actions 화면에서 'Cancel workflow' 가 보이면 먼저 눌러 보세요(사람). "
            "그다음 '재배포' 라고 답하면 1번만 새 배포를 일으킵니다.")


def stop_report(gh, commit, run, budget, t):
    """[멈춤] 보고 꼴의 몸통(실행 번호·status·잡·배포 상태·멈춘 분·그 밖 미완료 실행·GitHub 상태). GitHub API 읽기는 budget 번 안
    (budget = 정수, 또는 live 가 다른 상태 읽기와 같이 쓰는 [남은 수] 목록) — 리허설은 이 함수를 스크래치 한 줄로 부른다. → 부분 문자열 목록."""
    parts = []
    left = budget if isinstance(budget, list) else [budget]

    def read(url):
        if left[0] <= 0:
            return None, "한도 — 생략"
        left[0] -= 1
        st, res = gh.get(url)
        return (res, "") if st == 200 and isinstance(res, (dict, list)) else (None, gh.why(st, res))

    def field(res, key):
        return res.get(key) if isinstance(res, dict) else None

    if run:
        parts.append(f"Pages 실행 #{run.get('run_number')} · status {run_word(run)}")
        res, why = read(f"{REPO_API}/actions/runs/{run.get('id')}/jobs")
        jobs = field(res, "jobs")
        if isinstance(jobs, list) and jobs:
            parts.append("잡 " + " · ".join(f"{j.get('name')} {run_word(j)}" for j in jobs if isinstance(j, dict)))
        elif isinstance(jobs, list):
            res2, why2 = read(f"{REPO_API}/actions/runs/{run.get('id')}/jobs?filter=all")
            jobs2 = field(res2, "jobs")
            prev = " · ".join(f"{j.get('name')} {run_word(j)}(시도 {j.get('run_attempt')})" for j in jobs2 if isinstance(j, dict)) \
                if isinstance(jobs2, list) else f"못 읽음({why2})"
            parts.append(f"잡 0개(최근 시도) — 이전 시도 {prev or '없음'}")
        else:
            parts.append(f"잡 못 읽음({why})")
    else:
        parts.append(f"이 커밋({commit[:7]}) 실행 0개")
    res, why = read(f"{REPO_API}/deployments?sha={commit}&environment=github-pages&per_page=3")
    deps = res if isinstance(res, list) else None
    if res is None and why:
        parts.append(f"배포 상태 못 읽음({why})")
    elif not deps:
        parts.append("배포(github-pages) 없음")
    else:
        dep = deps[0]
        res2, why2 = read(f"{REPO_API}/deployments/{dep.get('id')}/statuses?per_page=3")
        sts = res2 if isinstance(res2, list) else None
        if sts:
            s0 = sts[0]
            c = iso_epoch(s0.get("created_at"))
            parts.append(f"배포 상태 {s0.get('state')}" + (f"({kst(c)} 부터 {int((t - c) // 60)}분)" if c else ""))
        else:
            parts.append(f"배포 상태 못 읽음({why2})" if why2 else "배포 상태 없음")
    res, why = read(f"{REPO_API}/actions/runs?per_page=10")
    runs = field(res, "workflow_runs")
    if isinstance(runs, list):
        others = [r for r in runs if isinstance(r, dict) and r.get("name") == LC["pages_workflow"]
                  and r.get("status") != "completed" and r.get("head_sha") != commit]
        parts.append("그 밖 미완료 실행 " + (" · ".join(f"#{r.get('run_number')}({str(r.get('head_sha'))[:7]} {r.get('status')})" for r in others) or "없음"))
    else:
        parts.append(f"그 밖 미완료 실행 못 읽음({why})")
    js, why = plain_json(LC["status_url"])
    comps = (js or {}).get("components") if isinstance(js, dict) else None
    if isinstance(comps, list):
        want = [c for c in comps if isinstance(c, dict) and c.get("name") in ("Pages", "Actions")]
        parts.append("GitHub 상태 " + (" · ".join(f"{c.get('name')} {c.get('status')}" for c in want) or "Pages·Actions 항목 없음"))
    else:
        parts.append(f"GitHub 상태 못 읽음({why or '꼴 다름'})")
    return parts


def live_ok_path(file):
    return os.environ.get(LIVE_OK_ENV) or os.path.join(os.path.dirname(os.path.abspath(file)), LIVE_OK)


def read_live_ok(path):
    """live_ok → ({commit, public_md5}, "") 또는 (None, 사유)."""
    try:
        with open(path, encoding="utf-8") as f:
            kv = dict(ln.split(None, 1) for ln in f.read().splitlines() if len(ln.split(None, 1)) == 2)
    except FileNotFoundError:
        return None, "없음"
    except (OSError, UnicodeError, ValueError) as e:
        return None, f"못 읽음({type(e).__name__})"
    c, m = kv.get("commit", "").strip(), kv.get("public_md5", "").strip()
    if not SHA40.fullmatch(c) or not MD5_HEX.fullmatch(m):
        return None, "꼴 다름"
    return {"commit": c, "public_md5": m}, ""


def record_head_hits(added, removed, repo):
    """leads.py guard 가 부른다(K3). staged 추가 줄 중 회차 머리 꼴 줄(.md 파일 · `## ` 로 시작 · "배포 완료 `<16진 7~40자>`" 를 품은 줄 — 날짜 자리·회차 낱말·
    sha 뒤 괄호 무관)의 sha 마다 <repo>/work/live_ok(live exit 0 이 쓴 커밋 sha · 공개 md5)의 커밋이 그 sha 로 시작하고 공개 md5 = <repo>/work/index.html md5
    일 때만 통과. 같은 staged 에서 지운 줄과 글자가 같은 줄(옮김 — 옛 절 보관 등)은 새 주장이 아니라 뺀다. 덮어쓰기 경로(SAERO_LIVE_OK)는 읽지 않는다.
    → (걸린 것 목록, 대조한 줄 수)."""
    moved = set(removed)
    lines = [(p, ln) for p, ln in added
             if p.lower().endswith(".md") and ln.startswith("## ") and HEAD_FORM.search(ln) and ln not in moved]
    if not lines:
        return [], 0
    ok, why = read_live_ok(os.path.join(repo, "work", LIVE_OK))
    wmd5 = None
    try:
        with open(os.path.join(repo, "work", "index.html"), "rb") as f:
            wmd5 = md5(f.read())
    except OSError:
        pass
    hits = []
    for p, ln in lines:
        for sha in HEAD_FORM.findall(ln):
            s = sha.lower()
            if ok is None:
                hits.append(f"회차 머리 배포 완료 {s[:7]} ≠ work/live_ok({why}) — {p}")
            elif not ok["commit"].startswith(s):
                hits.append(f"회차 머리 배포 완료 {s[:7]} ≠ work/live_ok 커밋 {ok['commit'][:7]} — {p}")
            elif wmd5 != ok["public_md5"]:
                hits.append(f"회차 머리 배포 완료 {s[:7]} ≠ work/live_ok — live_ok 공개 md5 {ok['public_md5'][:8]} ≠ work/index.html "
                            f"{(wmd5 or '없음')[:8]}(다른 회차의 live_ok) — {p}")
    return hits, len(lines)


def check_pair(a):
    """live·redeploy 네트워크 전 검사(K2) — (작업본 바이트, 직전 배포본 바이트) 또는 exit 코드(int)."""
    try:
        with open(a.file, "rb") as f:
            local = f.read()
        with open(a.prev, "rb") as f:
            prev = f.read()
    except OSError as e:
        print(f"[FAIL] --file·--prev 를 읽을 수 없음({type(e).__name__}) — 네트워크 전")
        return 2
    ok, why, pending = precheck_stamp(a.file, local, prev)
    if not ok:
        print(f"[FAIL] --file·--prev 가 precheck 도장 1·2행이 아님({why}) — 네트워크 전. 인자를 바꿔 넣었거나 다시 받은 본문이면 precheck.sh 부터")
        return 2
    if md5(local) == md5(prev):
        print(f"[FAIL] --file md5 = --prev md5({md5(local)[:8]}) — 공개 반영을 가를 수 없음, 네트워크 전")
        return 2
    print(why + (" · [주의] --pending 통과본" if pending else ""))
    return local, prev


def cmd_live(a, local, prev):
    t_start = now()
    c7, wmd5, pmd5 = a.commit[:7], md5(local), md5(prev)
    old = {pmd5} | ({a.seen} if a.seen else set())
    since = iso_epoch(a.since) if a.since else None
    gh = Gh(a.token_file)
    pub = [0]
    lp = live_ok_path(a.file)
    print(f"live 시작 {kst(t_start, True)} · 커밋 {c7} · 작업본 md5 {wmd5[:8]} · 직전 배포본 {pmd5[:8]}"
          + (f" · 본 적 있는 공개 md5 {a.seen[:8]}" if a.seen else "") + (f" · --since {kst(since, True)}" if since else ""))

    def tally():
        el = int(now() - t_start)
        print(f"무인증 API {gh.unauth}회 · 인증 {gh.auth}회 · 공개 GET {pub[0]}회 · 걸린 시간 {el}초")

    meta = {}   # 실행이 없을 때 git/commits 로 읽은 커밋 시각

    def commit_time(run):
        _, ct = commit_info(run)
        return ct or meta.get("time") or iso_epoch((run or {}).get("created_at"))

    def after_redeploy(run):
        """재배포 뒤의 live 인가 — --since(redeploy 가 찍어 넘긴 값)가 있거나 실행 head_commit 메시지가 재배포 접두."""
        return bool(a.since) or commit_info(run)[0].startswith(REDEPLOY_PREFIX)

    def line_head(run, kind, tail):
        ct = commit_time(run)
        if after_redeploy(run):  # 재배포 뒤 live 가 exit 0 이 아니면 'GitHub 쪽 대기 — 기다림' 머리·줄(완료 기준 12) · 두 번째 없음
            kind = kind if "기다림" in kind else f"{kind} — 기다림"
            tail = tail.replace("재배포 0/1", "재배포 1/1")
        tally()
        print(head_line(c7, kind))
        print(f"기록 줄: 저장소 반영(커밋) {c7} {kst(ct) if ct else '시각 모름'} · {tail}")

    def published(run, t, other_head=None):
        try:
            with open(lp, "w", encoding="utf-8", newline="\n") as f:
                f.write(f"commit {a.commit}\npublic_md5 {wmd5}\nat {iso(t)}\n")
        except OSError as e:
            print(f"[FAIL] live_ok 를 쓰지 못함({type(e).__name__}): {lp} — 공개 = 작업본이지만 기록 머리는 아래 '저장소 반영 …' 줄 그대로(guard 가 live_ok 없이는 막는다)")
            line_head(run, "확인 못 함", f"공개 = 작업본 {kst(t)}(live_ok 못 씀) · 재배포 0/1")
            return 1
        print(f"live_ok 씀: {lp}")
        ct = commit_time(run)
        after = f"커밋 뒤 {int(t - ct)}초 · " if ct else ""
        what = (f"다른 실행이 올림 — HEAD {other_head}" if other_head
                else f"{after}Pages #{run.get('run_number')}" if run else f"{after}Pages 실행 상태 못 읽음")
        tally()
        print(head_line(c7))
        print(f"기록 줄: 저장소 반영(커밋) {c7} {kst(ct) if ct else '시각 모름'} · 공개 사이트 반영 {kst(t)}({what})")
        return 0

    def is_redeploy(run):
        """--commit 이 재배포 커밋(메시지가 redeploy_message 접두)인가 — 실행 객체 head_commit 에서, 없으면 git/commits 1회(상태 한도 안). 못 읽으면 None."""
        if a.since:  # --since 는 redeploy 가 찍은 다음 live 에만 — 그 live 는 재배포 뒤(두 번째 질문 0)
            return True
        msg, _ = commit_info(run)
        if not msg:
            if left[0] <= 0:
                return None
            left[0] -= 1
            st, res = gh.get(f"{REPO_API}/git/commits/{a.commit}")
            if not (st == 200 and isinstance(res, dict) and isinstance(res.get("message"), str)):
                return None
            msg = res["message"]
            meta["time"] = iso_epoch(dig(res, "committer", "date"))
        return msg.startswith(REDEPLOY_PREFIX)

    def stopped(run, parts, headline=None):
        num = (run or {}).get("run_number")
        print("[멈춤] " + (headline + " · " if headline else "") + " · ".join(parts))
        rd = is_redeploy(run)
        if rd:
            print(f"GitHub 쪽 대기 — 기다림(재배포 1/1) — 커밋 {c7} 이 재배포 커밋(메시지 '{REDEPLOY_PREFIX}…')이라 두 번째 재배포는 없다 · 사용자에게 재배포를 묻지 않는다")
            line_head(run, "GitHub 쪽 대기 — 기다림",
                      f"공개 미반영 — GitHub 쪽 대기 — 기다림({f'Pages #{num} {run_word(run)}' if run else 'Pages 실행 없음'}) · 재배포 1/1")
            return 1
        if rd is None:
            print("[주의] 이 커밋이 재배포 커밋인지 못 읽음 — redeploy (d) 가 인증으로 다시 본다")
        print(f"재배포 질문(사용자에게 이 문구 그대로): {redeploy_question(num)}")
        print(f"답이 '재배포' 원문일 때만 — 다음(읽기 · dry-run): deploy.py redeploy --file {a.file} --prev {a.prev} --commit {a.commit}")
        line_head(run, "GitHub 쪽 대기", f"공개 미반영 — GitHub 쪽 대기({f'Pages #{num} {run_word(run)}' if run else 'Pages 실행 없음'}) · 재배포 0/1")
        return 1

    def guard_time(wait, kind):
        """한 번 실행 run_max_s 를 넘기게 되면 exit 3(같은 명령 한 번 더 — 읽기)."""
        if now() + wait > t_start + LC["run_max_s"]:
            print(f"한 번 실행 상한 {LC['run_max_s']}초 — 여기서 끝냄. 다음(읽기): 같은 live 명령 한 번 더(재배포는 묻지 않는다)")
            line_head(run_box[0], kind, f"공개 미반영 — {kind}(한 번 실행 상한 — live 다시) · 재배포 0/1")
            return True
        return False

    run_box = [None]
    left = [LC["api_status_max"]]   # 상태 읽기 한도 — stop_report · 재배포 커밋 판별 · cap 의 실행 다시 읽기·HEAD 읽기가 같이 쓴다
    polls, t0, any_ok, last_why, t_last, no_run = 0, None, False, "", None, None
    # ---- 1) 실행 폴 — 첫 폴 = 시작 · 다음 = max(t0 + api_poll_s[i], 앞 폴 + 60초)(지난 자리는 건너뜀) · 첫 폴 포함 api_poll_max 번
    while True:
        tp = t_last = now()
        polls += 1
        st, res = gh.get(f"{REPO_API}/actions/runs?head_sha={a.commit}&per_page=10")
        got, ok_read = None, False
        if st == 200:
            try:
                got, ok_read = pick_run(res, a.commit, since), True
            except ValueError:
                last_why = "꼴 다름"
        else:
            last_why = gh.why(st, res)
        any_ok = any_ok or ok_read
        if got:
            run_box[0] = got
        run = run_box[0]
        if run:
            created = iso_epoch(run["created_at"])
            t0 = max(created, since) if since else created
            print(f"[폴 {polls}] {kst(tp, True)} Pages 실행 #{run.get('run_number')} {run_word(run)}(생성 {kst(created, True)})"
                  + ("" if ok_read else f" — 이번 읽기 실패({last_why}), 앞 값"))
        else:
            t0 = since if since else t_start
            print(f"[폴 {polls}] {kst(tp, True)} " + ("이 커밋 Pages 실행 아직 없음" if ok_read else f"실행 못 읽음({last_why})"))
        if run and run.get("status") == "completed":
            if run.get("conclusion") != "success":
                print(f"Pages 실행 #{run.get('run_number')} 이 success 없이 끝남({run.get('conclusion')}) — 기다리지 않고 멈춤 판정으로")
            break
        if not run and ok_read and tp >= t0 + RUN_WAIT_S:
            no_run = (f"Pages 실행 없음 — {'--since' if since else 'live 시작'} 뒤 {RUN_WAIT_S}초가 지나도 "
                      f"'{LC['pages_workflow']}' 실행이 안 생김")
            break
        t_cap = t0 + LC["cap_s"]
        if tp >= t_cap:
            break
        later = [s for s in LC["api_poll_s"] if t0 + s > tp]
        if polls >= LC["api_poll_max"] or not later:  # 폴 한도 — cap 까지 기다렸다가 멈춤 판정(폴 없이)
            wait = max(0, t_cap - now())
            if guard_time(wait, "확인 못 함"):
                return 3
            time.sleep(wait)
            break
        wait = max(0, max(t0 + later[0], tp + API_CACHE_S) - now())
        if guard_time(wait, "확인 못 함"):
            return 3
        time.sleep(wait)
    run = run_box[0]
    if (run and run.get("status") != "completed" and left[0] > 0 and t_last is not None
            and now() - t_last >= LC["interval_s"]):  # cap: 마지막 폴 뒤 바뀌었을 수 있다 — 실행 하나를 다른 주소로 1회(상태 한도 안 · 같은 주소는 60초 캐시)
        left[0] -= 1
        st, res = gh.get(f"{REPO_API}/actions/runs/{run.get('id')}")
        if st == 200 and isinstance(res, dict) and isinstance(res.get("status"), str):
            run = dict(run, **{k: res.get(k) for k in ("status", "conclusion", "updated_at") if k in res})
            run_box[0] = run
            print(f"[cap] {kst(now(), True)} Pages 실행 #{run.get('run_number')} {run_word(run)}(다시 읽음)")
        else:
            print(f"[cap] 실행 다시 읽기 실패({gh.why(st, res)}) — 마지막 폴 값으로")
    # ---- 2) 실행 success 가 아님(멈춤·실행 없음·못 읽음) — 공개 GET 1회(작업본이면 exit 0) → 상태 읽기 → [멈춤]
    if not (run and run.get("status") == "completed" and run.get("conclusion") == "success"):
        st, body, hdr, why = public_get(True)
        pub[0] += 1
        t = now()
        if body is not None and md5(body) == wmd5:
            left[0] -= 1
            st2, res2 = gh.get(f"{REPO_API}/git/ref/heads/main")
            h = sha_at(res2, "object", "sha") if st2 == 200 else ""
            print(f"[공개 {pub[0]}] {kst(t, True)} md5 {wmd5[:8]} = 작업본 — 이 커밋 실행 success 는 못 봤지만 공개는 작업본")
            other = None if h == a.commit else (h[:7] if SHA40.fullmatch(h) else "못 읽음")
            return published(run, t, other_head=other)
        print(f"[공개 {pub[0]}] {kst(t, True)} " + (f"md5 {md5(body)[:8]} ≠ 작업본 {wmd5[:8]}" if body is not None else f"못 읽음({why})"))
        parts = stop_report(gh, a.commit, run, left, now())
        if run is None:
            head = no_run or (f"Pages 실행 없음 — '{LC['pages_workflow']}' 실행이 안 생김" if any_ok
                              else f"GitHub 상태 못 읽음({gh.note or last_why})")
            return stopped(None, parts, head)
        return stopped(run, parts)
    # ---- 3) 실행 success — 공개 GET(gzip) interval_s 간격
    t_done = iso_epoch(run.get("updated_at")) or now()
    deadline = max(t0 + LC["cdn_floor_s"], t_done + LC["cdn_max_age_s"] + LC["cdn_extra_s"])
    print(f"Pages 실행 #{run.get('run_number')} success(완료 {kst(t_done, True)}) — 공개 GET 시작(CDN 상한 {kst(deadline, True)})")
    after_old, fails, state = 0, 0, "after"
    while True:
        st, body, hdr, why = public_get(True)
        pub[0] += 1
        t = now()
        if body is None:
            fails += 1
            print(f"[공개 {pub[0]}] {kst(t, True)} 못 읽음({why})")
            if fails >= PUBLIC_FAIL_MAX:
                print(f"[FAIL] 공개 사이트 확인 못 함({why}) — {PUBLIC_FAIL_MAX}번 잇달아 실패")
                line_head(run, "확인 못 함", f"공개 미반영 — 확인 못 함(공개 GET {why}) · 재배포 0/1")
                return 1
        else:
            fails = 0
            m = md5(body)
            if m == wmd5:
                print(f"[공개 {pub[0]}] {kst(t, True)} md5 {m[:8]} = 작업본")
                return published(run, t)
            d, age = http_epoch(hdr.get("date")), hdr.get("age", "")
            checked = d - int(age) if d is not None and age.strip().isdigit() else d
            which = "직전 배포본" if m == pmd5 else ("본 적 있는 공개 판" if m in old else "작업본도 직전 배포본도 아님")
            if checked is not None and checked < t_done:
                state = "cdn"
                print(f"[공개 {pub[0]}] {kst(t, True)} md5 {m[:8]} = {which}(옛 판 — CDN 이 {kst(checked, True)} 에 확인한 객체, 실행 완료 전 → CDN 대기, 늦어도 {kst(deadline, True)})")
            else:
                state = "after"
                after_old += 1
                at = kst(checked, True) if checked is not None else "모름"
                print(f"[공개 {pub[0]}] {kst(t, True)} md5 {m[:8]} = {which}(CDN 확인 {at} — 실행 완료 뒤 · {after_old}/{AFTER_LOOKS + 1})")
                if after_old > AFTER_LOOKS:
                    if m in old:
                        parts = [f"Pages #{run.get('run_number')} success(완료 {kst(t_done, True)})인데 공개 본문이 옛 판(md5 {m[:8]} = {which} · "
                                 f"CDN 확인 {at} = 완료 뒤 · {AFTER_LOOKS + 1}번 같음) — GitHub 프록시 캐시일 수 있음"]
                        return stopped(run, parts)
                    print(f"[FAIL] 공개 본문 md5 {m[:8]} 가 작업본도 직전 배포본도 아님(실행 완료 뒤 확인된 객체 · {AFTER_LOOKS + 1}번 같음) — "
                          "다른 배포가 겹쳤을 수 있다. 재배포 묻지 않음 — 배포 저장소 HEAD(ls-remote)와 함께 보고")
                    line_head(run, "확인 못 함", f"공개 미반영 — 확인 못 함(공개 md5 {m[:8]} — 작업본·직전 배포본 아님) · 재배포 0/1")
                    return 1
        if state == "cdn" and now() + LC["interval_s"] > deadline:
            print(f"CDN 상한 {kst(deadline, True)} 까지 옛 판 — 재배포는 묻지 않는다. 다음(읽기): 잠시 뒤 같은 live 명령 한 번 더")
            line_head(run, "CDN 캐시", f"공개 미반영 — CDN 캐시(Pages #{run.get('run_number')} 성공 {kst(t_done)}) · 재배포 0/1")
            return 3
        if guard_time(LC["interval_s"], "CDN 캐시" if state == "cdn" else "확인 못 함"):
            return 3
        time.sleep(LC["interval_s"])


def cmd_redeploy(a, local, prev):
    real = bool(a.confirm)
    c7, wmd5 = a.commit[:7], md5(local)
    stops = []      # (표지, exit 코드, 재배포 셈)
    print(f"redeploy {'실제 — 쓰기 1번(사용자 답 재배포 뒤)' if real else 'dry-run(기본 — 쓰기 0)'} · 커밋 {c7} · 작업본 md5 {wmd5[:8]}")

    def stop(label, code, line, count="0/1"):
        print(line)
        stops.append((label, code, count))
        return real

    def end_real():
        label, code, count = stops[0]
        if code == 0:
            print(f"다음(읽기): deploy.py live --file {a.file} --prev {a.prev} --commit {a.commit}")
            return 0
        print(head_line(c7, "GitHub 쪽 대기 — 기다림"))
        print(f"기록 줄: 저장소 반영(커밋) {c7} · 공개 미반영 — GitHub 쪽 대기 — 기다림(redeploy {label} 에서 끝남) · 재배포 {count}")
        return code

    tok, src = credential(a.token_file)
    if not tok:
        if stop("(e)", 1, f"[FAIL] (e) 자격 증명을 얻지 못함(출처: {src}) — {HINT[src]} · 쓰기 0"):
            return end_real()
    else:
        print(f"(e) 자격 증명 확인됨(출처: {src})")
        if not push_permission_ok(tok) and stop("(e)", 1, "[FAIL] (e) 배포 저장소 쓰기 권한 확인 안 됨 — 쓰기 0"):
            return end_real()
    st, body, hdr, why = public_get(True)
    if body is None:
        if stop("(b)", 1, f"[FAIL] (b) 공개 사이트를 읽지 못함({why}) — 쓰기 0"):
            return end_real()
    elif md5(body) == wmd5:
        if stop("(b)", 0, f"(b) 공개 사이트 = 작업본(md5 {wmd5[:8]}) — 이미 반영됨 · 쓰기 0"):
            return end_real()
    else:
        print(f"(b) 공개 md5 {md5(body)[:8]} ≠ 작업본 {wmd5[:8]} — 미반영")
    head, tree, run = None, None, None
    if not tok:
        print("(a)·(d)·(c) 자격 증명 없음 — 인증 읽기 못 함")
    else:
        gh = Gh(a.token_file, tok, src)
        st, res = gh.get(f"{REPO_API}/git/ref/heads/main")
        h = sha_at(res, "object", "sha") if st == 200 else ""
        if not SHA40.fullmatch(h):
            if stop("(a)", 1, f"[FAIL] (a) 배포 저장소 HEAD 를 읽지 못함({gh.why(st, res) if st != 200 else '꼴 다름'}) — 쓰기 0"):
                return end_real()
        else:
            head = h
            if h != a.commit:
                if stop("(a)", 1, f"[FAIL] (a) 배포 저장소 HEAD {h[:7]} ≠ --commit {c7} — 다른 배포가 겹쳤거나 이미 재배포함 · 쓰기 0"):
                    return end_real()
            else:
                print(f"(a) 배포 저장소 HEAD {h[:7]} = --commit(인증 GET)")
        target = head or a.commit
        st, res = gh.get(f"{REPO_API}/git/commits/{target}")
        tsha = sha_at(res, "tree", "sha") if st == 200 else ""
        msg = res.get("message") if st == 200 and isinstance(res, dict) else None
        if not SHA40.fullmatch(tsha) or not isinstance(msg, str):
            if stop("(a)", 1, f"[FAIL] (a) 커밋 {target[:7]} 을 읽지 못함({gh.why(st, res) if st != 200 else '꼴 다름'}) — 쓰기 0"):
                return end_real()
        else:
            tree = tsha
            first = msg.splitlines()[0] if msg else ""
            if msg.startswith(REDEPLOY_PREFIX):
                if stop("(d)", 1, f"[FAIL] 이미 재배포함 — 두 번째 없음 · 쓰기 0 (HEAD {target[:7]} 메시지 '{first}')", count="1/1"):
                    return end_real()
            else:
                print(f"(d) HEAD {target[:7]} 메시지 '{first}' — 재배포 커밋 아님")
        st, res = gh.get(f"{REPO_API}/actions/runs?head_sha={a.commit}&per_page=10")
        try:
            run = pick_run(res, a.commit) if st == 200 else None
            ok_read = st == 200
        except ValueError:
            ok_read = False
        if not ok_read:
            if stop("(c)", 1, f"[FAIL] (c) Pages 실행을 읽지 못함({gh.why(st, res) if st != 200 else '꼴 다름'}) — 쓰기 0"):
                return end_real()
        elif run is None:
            print(f"(c) 이 커밋 Pages 실행 없음")
        else:
            up = iso_epoch(run.get("updated_at"))
            ago = int(now() - up) if up else None
            if run.get("status") != "completed" and ago is not None and ago < MOVING_S:
                if stop("(c)", 1, f"[주의] (c) Pages 실행 #{run.get('run_number')} {run_word(run)} — {ago}초 전에 움직임(2분 안) — 쓰기 0, live 다시"):
                    return end_real()
            else:
                print(f"(c) Pages 실행 #{run.get('run_number')} {run_word(run)}(마지막 움직임 {kst(up, True) if up else '모름'}) — 2분 안 움직임 없음")
    num = (run or {}).get("run_number", "?")
    status = run_word(run) if run else "실행 없음"
    message = LC["redeploy_message"].format(commit7=c7, run=num, status=status)
    parent = head or a.commit
    print(f"쓰기 요약: POST /git/commits {{message: '{message}', tree: {(tree or '<못 읽음>')[:7]}, parents: [{parent[:7]}]}} → "
          "PATCH /git/refs/heads/main {sha: <새 커밋>, force: false} — ref 이동 1번 · 본문 변화 0(tree = HEAD tree)")
    if not real:
        if stops:
            print(f"[dry-run] 실제였다면 {stops[0][0]}에서 멈춤 — 쓰기 0")
            return stops[0][1]
        print("[dry-run] 쓰기 0 — 실제 쓰기는 사용자 답 '재배포' 원문 뒤 같은 명령 1번(SKILL.md 7단계)")
        return 0
    # ---- 실제 쓰기(사용자 답 '재배포' 뒤 1번 — 결과 모름이면 재시도 0)
    t_write = now()
    st, res, _ = api_full(tok, "POST", {"message": message, "tree": tree, "parents": [head]}, url=f"{REPO_API}/git/commits")
    detail = (res or {}).get("message", "")[:200] if isinstance(res, dict) else ""
    if st == 0 or st >= 500:
        print(f"[FAIL] 재배포 커밋 만들기(POST) 결과 모름({detail}) — PATCH 안 보냄 · ref 그대로 · 재시도 0 · 재배포 1/1 로 셈(다시는 사용자)")
        stops.append(("POST", 1, "1/1(결과 모름)"))
        return end_real()
    new = sha_at(res, "sha")
    if st not in (200, 201):
        print(f"[FAIL] POST /git/commits {st}: {detail} — 쓰기 끝(ref 그대로) · 재시도 0")
        stops.append(("POST", 1, "0/1(쓰기 거부)"))
        return end_real()
    parents = [sha_at(p, "sha") for p in (dig(res, "parents") or []) if isinstance(p, dict)]
    if not new or sha_at(res, "tree", "sha") != tree or parents != [head]:
        print("[FAIL] 만든 커밋 꼴이 다름(sha·tree·parents) — PATCH 안 보냄 · ref 그대로 · 재시도 0")
        stops.append(("POST", 1, "0/1(ref 그대로)"))
        return end_real()
    st, res, _ = api_full(tok, "PATCH", {"sha": new, "force": False}, url=f"{REPO_API}/git/refs/heads/main")
    detail = (res or {}).get("message", "")[:200] if isinstance(res, dict) else ""
    nxt = f"다음(읽기): deploy.py live --file {a.file} --prev {a.prev} --commit {new} --since {iso(t_write)}"
    if st == 200 and sha_at(res, "object", "sha") == new:
        print(f"재배포 요청 보냄 빈 커밋 {new[:7]} {kst(t_write, True)}(부모 {head[:7]} · tree 같음 · force:false)")
        print(nxt)
        return 0
    if 400 <= st < 500:
        print(f"[FAIL] ref 이동 거부(PATCH {st}: {detail}) — 쓰기 끝(ref 그대로 — 떠 있는 커밋 객체는 tree 가 같아 무해) · 재시도 0")
        stops.append(("PATCH", 1, "0/1(ref 그대로)"))
        return end_real()
    print(f"[주의] ref 이동(PATCH) 결과 모름({detail or st}) — 재시도 0 · {RUN_WAIT_S}초 뒤 인증 GET 으로 HEAD 를 다시 읽는다")
    time.sleep(RUN_WAIT_S)
    st, res, _ = api_full(tok, url=f"{REPO_API}/git/ref/heads/main")
    h = sha_at(res, "object", "sha") if st == 200 else ""
    if h == new:
        print(f"재배포 요청 보냄 빈 커밋 {new[:7]} {kst(t_write, True)} — PATCH 결과 모름 뒤 다시 읽음: HEAD = 새 커밋")
        print(nxt)
        return 0
    if h == a.commit:
        print(f"[FAIL] 재배포 안 됨 — 다시 읽은 HEAD = {c7}(그대로) · 재배포 1/1 로 셈(다시는 사용자) · 재시도 0")
        stops.append(("PATCH", 1, "1/1(결과 모름 — 안 됨)"))
    elif SHA40.fullmatch(h):
        print(f"[FAIL] 다시 읽은 HEAD {h[:7]} — 다른 배포가 겹침 · 재시도 0")
        stops.append(("PATCH", 1, "1/1(결과 모름 — 겹침)"))
    else:
        print(f"[FAIL] 다시 읽기도 실패(GET {st}) — 결과 모름 그대로 · 재배포 1/1 로 셈 · 재시도 0")
        stops.append(("PATCH", 1, "1/1(결과 모름)"))
    return end_real()


def cmd_public(a):
    try:
        with open(a.file, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"[FAIL] --file을 읽을 수 없음({type(e).__name__}): {a.file} — GET 안 함")
        return 2
    st, body, hdr, why = public_get(False)
    print(f"공개 GET(무압축 — 사용자 gzip 객체를 심지 않음 · API 0) {SITE} → {st or '실패'}")
    if body is None:
        print(f"[주의] 공개 사이트를 읽지 못함({why}) — 확인 못 함(멈추지 않는다)")
        return 1
    d, age = http_epoch(hdr.get("date")), hdr.get("age", "")
    checked = d - int(age) if d is not None and age.strip().isdigit() else None
    print("헤더: " + " · ".join(f"{k} {hdr[k]}" for k in ("last-modified", "etag", "age", "x-cache", "content-length") if k in hdr)
          + (f" · CDN 확인 {kst(checked, True)}(Date − Age)" if checked is not None else ""))
    m, f = md5(body), md5(data)
    if m == f:
        print(f"공개 md5 {m} = {a.file} md5 → 같음")
        return 0
    print(f"공개 md5 {m} ≠ {a.file} md5 {f[:8]} → 다름")
    print(f"[주의] 공개 사이트가 저장소 HEAD 와 다름 — 옛 실행이 덮었을 수 있다(멈추지 않는다 · 이번 회차 live 에 --seen {m})")
    return 1


def live_commit_after_verify(token_file, ref):
    """verify --ref 일치 뒤 다음 live 의 --commit(B-7): HEAD = ref 면 HEAD · HEAD 메시지가 재배포 접두이고 부모 = ref 면 HEAD · 아니면 ref.
    → (40자 또는 None, 사유)."""
    full = ref if SHA40.fullmatch(ref) else None
    st, res, _ = get(token_file, f"{REPO_API}/git/ref/heads/main")
    h = sha_at(res, "object", "sha") if st == 200 else ""
    if not SHA40.fullmatch(h):
        return full, f"배포 저장소 HEAD 를 못 읽음(GET {st}) — 재배포가 있었으면 그 빈 커밋으로"
    if h.startswith(ref):
        return h, "HEAD = push 커밋"
    st, res, _ = get(token_file, f"{REPO_API}/git/commits/{h}")
    parents = [sha_at(p, "sha") for p in (dig(res, "parents") or []) if isinstance(p, dict)] if st == 200 else []
    msg = res.get("message", "") if st == 200 and isinstance(res, dict) else ""
    if isinstance(msg, str) and msg.startswith(REDEPLOY_PREFIX) and len(parents) == 1 and parents[0].startswith(ref):
        return h, f"HEAD {h[:7]} = 재배포 빈 커밋(부모 = push 커밋)"
    return full, f"HEAD {h[:7]} ≠ push 커밋 · 재배포 커밋 아님 — push 커밋으로"


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)  # 줄인 플래그(--con 등)가 --confirm 으로 먹히지 않게(2026-10-11)
    ap.add_argument("cmd", choices=["fetch", "push", "verify", "live", "redeploy", "public"])
    ap.add_argument("--token-file", help="선택. 없으면 GET은 무인증, PUT은 이 PC git 자격 증명")
    ap.add_argument("--out")
    ap.add_argument("--file")
    ap.add_argument("--message")
    ap.add_argument("--base", help="push: 4단계 fetch가 저장한 직전 배포본(work/prev.html) — PUT 직전 배포본이 이것과 같아야 한다. 실제 push는 필수")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--layout-change", action="store_true",
                    help="push: --file·--base 의 레이아웃 판(meta report-layout)이 다를 때 PUT 을 허락 — 첫 적용 회차에 사용자가 작업본 화면을 보고 '배포'라고 했을 때만")
    ap.add_argument("--ref", help="verify: push 성공 줄이 찍은 커밋 sha — 그 커밋의 본문을 ?ref=로 받는다(ref 없는 GET은 PUT 직후 캐시로 옛 본문일 수 있다)")
    ap.add_argument("--prev", help="live·redeploy: 4단계 fetch 파일(work/prev.html — 도장 2행)")
    ap.add_argument("--commit", help="live·redeploy: 배포 저장소 커밋 40자(verify 일치 줄의 다음 live 명령 값)")
    ap.add_argument("--since", help="live: redeploy 가 찍은 쓰기 시각(ISO) — 그 앞 5초보다 먼저 생긴 실행은 안 고른다")
    ap.add_argument("--seen", help="live: 4단계 public 이 본 공개 md5(32자) — 옛 판으로 인정")
    ap.add_argument("--confirm", action="store_true", help="redeploy: 실제 쓰기 — 사용자 답 '재배포' 원문 뒤 1번만")
    a = ap.parse_args()
    base = None
    # 인자 오류는 네트워크 전에(GET 0)
    if a.ref is not None and a.cmd != "verify":
        print("[FAIL] --ref는 verify에만 — push는 늘 최신 sha를 다시 조회한다. GET 안 함")
        return 2
    if a.ref is not None and not re.fullmatch(r"[0-9a-fA-F]{7,40}", a.ref):
        print("[FAIL] --ref는 커밋 sha(16진 7~40자 — push 성공 줄 `저장소 반영 커밋 …`의 값)만 — GET 안 함")
        return 2
    if a.ref:
        a.ref = a.ref.lower()
    if a.cmd in ("live", "redeploy", "public"):
        return main_site(a)
    for k in ("prev", "commit", "since", "seen"):
        if getattr(a, k) is not None:
            print(f"[FAIL] --{k}는 live·redeploy 에만 — GET 안 함")
            return 2
    if a.confirm:
        print("[FAIL] --confirm 은 redeploy 에만 — GET 안 함")
        return 2
    if a.cmd == "fetch" and not a.out:
        print("[FAIL] fetch에는 --out이 필요 — GET 안 함")
        return 2
    if a.cmd == "verify" and not a.file:
        print("[FAIL] verify에는 --file이 필요 — GET 안 함")
        return 2
    if a.cmd == "push" and not a.file and not a.dry_run:
        print("[FAIL] push에는 --file이 필요(--file 없는 push는 --dry-run — S0 사전 점검만) — GET 안 함")
        return 2
    if a.base and not a.file:
        print("[FAIL] --base는 --file과 함께만 — --file 없는 push --dry-run(S0)에는 --base를 주지 않는다. PUT 안 함")
        return 2
    if a.cmd == "push" and a.file and not a.dry_run and not a.base:
        print("[FAIL] 실제 push에는 --base work/prev.html(4단계 fetch 파일)이 필요 — 그 뒤 배포본이 바뀌었으면 덮어쓰지 않게. PUT 안 함")
        return 2
    if a.cmd == "push" and a.base:
        try:
            with open(a.base, "rb") as f:
                base = f.read()
        except OSError as e:
            print(f"[FAIL] --base 파일을 읽을 수 없음({type(e).__name__}): {a.base} — PUT 안 함")
            return 2
    local = None
    if a.cmd in ("push", "verify") and a.file:  # --file은 여기서 한 번만 읽는다 — 도장 대조·PUT 본문·verify가 같은 바이트(사이에 파일이 바뀌어도)
        try:
            with open(a.file, "rb") as f:
                local = f.read()
        except OSError as e:
            print(f"[FAIL] --file을 읽을 수 없음({type(e).__name__}): {a.file} — PUT 안 함")
            return 2
    if a.cmd == "push" and a.file:  # precheck 통과본만 PUT — 네트워크 전에 본다
        ok, why, pending = precheck_stamp(a.file, local, base)
        if not ok and not a.dry_run:
            print(f"[FAIL] precheck 통과본이 아님 — PUT 안 함({why}). scripts/precheck.sh를 이 작업본·이 --base로 다시 통과시킨다")
            return 1
        print(why if ok else f"[주의] precheck 통과본이 아님({why}) — 실제 push는 여기서 멈춘다")
        if pending:
            print("[주의] --pending 통과본(답 대기 배포용) — 답을 반영한 재배포라면 --pending 없이 precheck를 다시")
    if a.cmd == "push" and a.file and base is not None:  # 레이아웃 판 게이트(막음 M4) — 네트워크 전에 본다(GET·PUT 0)
        lf, lb = layout_of(local), layout_of(base)
        if lf != lb:
            what = f"직전 배포본(--base) {lb or 'meta 없음(옛 판)'} → 작업본(--file) {lf or 'meta 없음(옛 판)'}"
            if a.layout_change:
                print(f"레이아웃 판 바뀜 — {what} · --layout-change(사용자가 작업본 화면을 보고 '배포')로 진행")
            elif not a.dry_run:
                print(f"[FAIL] 레이아웃 판이 바뀜 — PUT 안 함({what}). 첫 적용 회차면 사용자가 작업본 화면을 본 뒤 '배포'라고 했을 때만 "
                      "--layout-change 를 붙인다. 데이터 회차에서 났으면(병합 뒤 첫 적용 전) 여기서 멈추고 사용자에게 묻는다")
                return 1
            else:
                print(f"[주의] 레이아웃 판이 바뀜 — 실제 push 에는 --layout-change(사용자가 작업본 화면을 본 뒤) · {what}")
    status, res, how = get(a.token_file, f"{API}?ref={a.ref}" if a.ref else API)
    if status != 200:
        print(f"GET {status}{f' (ref {a.ref})' if a.ref else ''}: {res.get('message', '')}")
        if a.ref and status == 404:
            print(f"[FAIL] ref {a.ref}의 index.html을 찾지 못함 — push 성공 줄의 커밋 sha를 그대로 넣었는지 확인(재PUT 금지)")
            return 1
        print("무인증 GET이 막히고(403·429) 자격 증명으로도 안 되면 `git clone -c core.autocrlf=false https://github.com/LeeKwanBeom/saero-pilates-report`로 받는다(SKILL.md 4단계).")
        return 1
    if how:
        print(f"GET 무인증 제한 → 자격 증명으로 다시 받음(출처: {how})")
    sha, content = res["sha"], base64.b64decode(res["content"])
    if a.cmd == "fetch":
        with open(a.out, "wb") as f:
            f.write(content)
        print(f"저장 {a.out} ({len(content.splitlines())}행, md5 {md5(content)[:8]}…) sha {sha}")
        return 0
    if not a.file:
        if a.cmd == "push" and a.dry_run:  # S0 사전 점검: 본문 없이 sha·자격 증명·쓰기 권한만 확인(references/code-tab.md 2절)
            tok, src = credential(a.token_file)
            print(f"최신 sha {sha} · 본문 없음(--file 없이 dry-run — 자격 증명·쓰기 권한만 확인)")
            if not tok:
                print(f"[FAIL] 자격 증명을 얻지 못함(출처: {src}) — {HINT[src]}")
                return 1
            print(f"자격 증명 확인됨(출처: {src})")
            if not push_permission_ok(tok):
                return 1
            print("[dry-run] PUT을 보내지 않음. 파일 변경 없음.")
            return 0
        print(f"{a.cmd}에는 --file 이 필요합니다")
        return 2
    if a.cmd == "verify":
        same = md5(local) == md5(content)
        at = f"(ref {a.ref} 기준) " if a.ref else ""
        print(f"재수령본 {at}sha {sha} · md5 {md5(content)[:8]}… vs 로컬 {md5(local)[:8]}… → {'일치' if same else '불일치'}")
        if not same and a.ref:  # 커밋에 고정된 본문 — 캐시로 설명되지 않는다
            print(f"[FAIL] 불일치 — ref {a.ref}의 본문이 로컬과 다름(커밋 고정 조회라 캐시 아님). 다시 PUT하지 않는다. "
                  "위 sha·md5를 보고하고 재PUT은 사용자가 정한다(SKILL.md 7단계)")
        elif not same:
            print("[FAIL] 불일치 — PUT 직후라면 캐시일 수 있다: ls-remote HEAD와 --ref로 다시 verify(읽기). 재PUT 금지 "
                  "(위 sha·md5를 보고 — 재PUT은 사용자가 정한다, SKILL.md 7단계)")
            print(f"  확인(읽기): git ls-remote https://github.com/{CFG['deploy_repo']} HEAD → "
                  f"deploy.py verify --file {a.file} --ref <push 성공 줄의 커밋 — 없으면 ls-remote HEAD 값>")
        if same and a.ref:  # 다음 live 의 --commit 은 deploy.py 가 고른다(B-7 — 세션은 손으로 API 를 읽지 않는다)
            commit, why = live_commit_after_verify(a.token_file, a.ref)
            d = os.path.dirname(a.file)
            prev_path = (d.replace(os.sep, "/") + "/" if d else "") + "prev.html"
            print(f"live 커밋: {why}")
            print(f"다음(읽기): deploy.py live --file {a.file} --prev {prev_path} --commit {commit or '<push 성공 줄의 40자 커밋>'}")
        return 0 if same else 1
    if base is not None:  # PUT에 쓸 sha를 준 바로 그 GET 본문이 4단계 fetch 파일과 같아야 한다(그 사이 다른 배포가 있었으면 덮어쓰지 않는다)
        if md5(content) != md5(base) and md5(content) == md5(local):  # 결과 모름이던 앞 PUT이 실제로 반영된 경우 — 다시 PUT하지 않는다
            print(f"지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨(verify로 확인). PUT 안 함 (md5 {md5(local)[:8]}…)")
            return 0
        if md5(content) != md5(base):
            print(f"[FAIL] 배포본이 4단계 fetch 뒤 바뀜 — 지금 배포본 sha {sha} · md5 {md5(content)[:8]}… ≠ --base {a.base} md5 {md5(base)[:8]}…. "
                  "PUT 안 함 — 새 배포본으로 4단계부터 다시 할지는 사용자가 정한다")
            return 1
        print(f"배포본 = --base(4단계 fetch) md5 {md5(base)[:8]}… 확인")
    else:
        print("[dry-run] --base 없음 — 실제 push에는 --base work/prev.html이 필요")
    body = {"message": a.message or "리포트 갱신", "content": base64.b64encode(local).decode(), "sha": sha}
    print(f"최신 sha {sha}, 본문 {len(local):,}바이트 ({len(local.splitlines())}행, md5 {md5(local)[:8]}…)")
    tok, src = credential(a.token_file)
    if not tok:
        print(f"[FAIL] 자격 증명을 얻지 못함(출처: {src}) — {HINT[src]}. PUT 안 함")
        return 1
    print(f"자격 증명 확인됨(출처: {src})")
    if a.dry_run:
        if not push_permission_ok(tok):
            return 1
        print("[dry-run] PUT을 보내지 않음. 파일 변경 없음.")
        return 0
    status, res = api(tok, "PUT", body)
    msg = res.get("message", "")[:200]
    if status == 0 or status >= 500:  # 요청 예외(타임아웃·연결 끊김)·서버 오류 — 서버가 PUT을 받았는지 모른다
        print(f"[FAIL] PUT 결과 모름({msg}) — 반영됐을 수 있다. 재PUT 금지, 먼저 deploy.py verify --file {a.file}")
        return 1
    if status == 409:
        print(f"[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치) — PUT 안 됨, 4단계부터 다시 할지는 사용자가 정한다(PUT 409: {msg})")
        return 1
    if status == 403:
        print(f"[FAIL] PUT 403 — 쓰기 권한 없음(자격 증명 출처 {src} · 배포 저장소 {CFG['deploy_repo']}): {msg}. PUT 안 됨 — 계정·토큰 권한은 사용자가 확인")
        return 1
    if status == 404:
        print(f"[FAIL] PUT 404 — 저장소·경로를 찾지 못함(config deploy_repo {CFG['deploy_repo']} · 권한이 없어도 404로 온다): {msg}. PUT 안 됨")
        return 1
    if status not in (200, 201):
        print(f"[FAIL] PUT {status}: {msg} — PUT 안 됨(자격 증명 출처 {src}, 배포 저장소 {CFG['deploy_repo']}). 재시도는 사용자가 정한다")
        return 1
    commit = res["commit"]["sha"]  # 전체 sha — verify --ref에 그대로(ref 없는 GET은 PUT 직후 캐시로 옛 본문일 수 있다)
    print(f"저장소 반영 커밋 {commit} · 파일 sha {res['content']['sha'][:7]} · 공개 사이트 반영은 verify 뒤 live 로 확인(보통 1~2분)")
    print(f"다음(읽기): deploy.py verify --file {a.file} --ref {commit}")
    return 0


def main_site(a):
    """live · redeploy · public — 인자 검사(네트워크 전) 뒤 각 명령."""
    if a.cmd == "public":
        if not a.file:
            print("[FAIL] public 에는 --file 이 필요 — GET 안 함")
            return 2
        for k in ("prev", "commit", "since", "seen", "base", "message"):
            if getattr(a, k) is not None:
                print(f"[FAIL] public 에는 --{k} 를 주지 않는다 — GET 안 함")
                return 2
        if a.confirm or a.dry_run:
            print("[FAIL] public 은 읽기만 — --confirm·--dry-run 없음. GET 안 함")
            return 2
        return cmd_public(a)
    if not (a.file and a.prev and a.commit):
        print(f"[FAIL] {a.cmd} 에는 --file work/index.html --prev work/prev.html --commit <40자> 가 필요 — 네트워크 전")
        return 2
    if not re.fullmatch(r"[0-9a-fA-F]{40}", a.commit):
        print(f"[FAIL] --commit 은 커밋 sha 40자만(verify 일치 줄이 찍은 다음 live 명령 값 — 짧은 sha 는 Actions 필터가 0건을 줄 수 있다) — 네트워크 전")
        return 2
    a.commit = a.commit.lower()
    if a.base is not None or a.message is not None or a.layout_change:
        print(f"[FAIL] {a.cmd} 에는 --base·--message·--layout-change 를 주지 않는다 — 네트워크 전")
        return 2
    if a.cmd == "redeploy":
        if a.since is not None or a.seen is not None:
            print("[FAIL] --since·--seen 은 live 에만 — 네트워크 전")
            return 2
        if a.confirm and a.dry_run:
            print("[FAIL] redeploy 는 기본 dry-run — --dry-run 과 실제 쓰기를 함께 주지 않는다. 네트워크 전")
            return 2
    else:
        if a.confirm or a.dry_run:
            print("[FAIL] live 는 읽기만 — --confirm·--dry-run 없음. 네트워크 전")
            return 2
        if a.since is not None and iso_epoch(a.since) is None:
            print("[FAIL] --since 는 ISO 시각(YYYY-MM-DDTHH:MM:SSZ — redeploy 가 찍은 값)만 — 네트워크 전")
            return 2
        if a.seen is not None:
            if not MD5_HEX.fullmatch(a.seen.lower()):
                print("[FAIL] --seen 은 md5 32자(4단계 public 이 찍은 공개 md5)만 — 네트워크 전")
                return 2
            a.seen = a.seen.lower()
        lp = live_ok_path(a.file)  # 시작 때 옛 live_ok 를 지운다 — 이번 live 가 exit 0 일 때만 다시 생긴다
        print(f"live_ok 자리: {lp}" + (f"(덮어쓰기 {LIVE_OK_ENV} — 리허설·시험 전용, 운영 회차 금지)" if os.environ.get(LIVE_OK_ENV) else ""))
        try:
            os.remove(lp)
            print("옛 live_ok 지움")
        except FileNotFoundError:
            pass
        except OSError as e:
            print(f"[FAIL] 옛 live_ok 를 지우지 못함({type(e).__name__}): {lp} — 네트워크 전")
            return 2
    pair = check_pair(a)
    if isinstance(pair, int):
        return pair
    local, prev = pair
    return cmd_live(a, local, prev) if a.cmd == "live" else cmd_redeploy(a, local, prev)


if __name__ == "__main__":
    sys.exit(main())
