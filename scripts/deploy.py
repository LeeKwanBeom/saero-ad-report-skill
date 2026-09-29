#!/usr/bin/env python3
"""배포본 index.html 받기·올리기(4·7단계) — 계산 로직 없음.

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
        --dry-run 은 sha 조회·base 대조·자격 증명 확인·쓰기 권한 확인
        (인증 GET /repos/{deploy_repo}의 permissions.push — 계정 역할 기준, 토큰 범위는 PUT이 최종 확인. 참/거짓만 찍고 거짓이면 [FAIL])·본문 준비까지만 하고 PUT을 보내지 않는다
        (아무 파일도 쓰지 않는다 — 2026-09-26 실측). "자격 증명 확인됨(출처: token-file|git)"만 찍는다.
        --dry-run 은 --file 없이도 된다(S0 사전 점검 — sha·자격 증명·쓰기 권한만 확인).
    $PY scripts/deploy.py verify --file <index.html> [--ref <커밋 sha>] [--token-file <파일>]
        배포 후 재수령본 md5 = 로컬 md5 인지. 다르면 exit 1 — 다시 PUT하지 않는다(재PUT은 사용자 결정).
        --ref = push 성공 줄이 찍은 커밋 sha(16진 7~40자, 아니면 GET 전에 exit 2) — 있으면 `?ref=`로 그 커밋의 본문을 받는다.
        ref 없는 contents GET은 PUT 직후 약 1분 옛 본문을 돌려줄 수 있다(2026-09-29 실측 2회 — 요청의 no-cache로도 안 막힘).
        그래서 7단계는 push → verify --ref <push가 찍은 커밋>. ref 없이 불일치면 캐시일 수 있다는 문구(ls-remote HEAD와 --ref로 다시 verify — 읽기, 재PUT 금지).

자격 증명(2026-09-28 Code 탭 회차):
  - GET(fetch·verify·push 전 sha)은 무인증으로 먼저 보내고, 403·429(무인증 rate limit)일 때만 자격 증명으로 1회 다시 보낸다.
  - PUT은 --token-file이 있으면 그 파일, 없으면 이 PC의 git 자격 증명(`git credential fill`, github.com)을 subprocess로 얻는다
    (credential.interactive=false · GIT_TERMINAL_PROMPT=0 · GCM_INTERACTIVE=never · askpass 변수 제거 — 창·프롬프트를 띄우지 않는다). 못 얻으면 [FAIL] exit 1.
  - 자격 증명 값은 변수에만 둔다 — 출력·파일·로그·예외 문구 어디에도 남기지 않는다(한 줄 토큰 형식이 아니면 쓰지 않고,
    요청 예외는 종류만 — 네트워크 연결 오류만 소켓 사유 문구, 헤더 값 없음. 서버·프록시가 되돌려 준 오류 문구 속 자격 증명 값은 `***`로 바꾼다). --token-file은 바이트로 읽어 UTF-16(BOM FF FE·FE FF)과
    UTF-8(BOM 허용)을 가리고, 없거나 못 읽으면 "[FAIL] 자격 증명을 얻지 못함(출처: token-file)"(Traceback 없음).
    `push --dry-run`은 값을 얻은 뒤 인증 GET(읽기)으로 배포 저장소 permissions.push까지 본다(2026-09-28 수정 회차 2 N1 — 계정 역할 기준이라
    fine-grained 토큰의 저장소·권한 범위는 PUT이 최종 확인한다). 저장소는 config deploy_repo.
"""
import argparse
import base64
import hashlib
import http.client
import json
import os
import re
import subprocess
import sys
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


def api(token, method="GET", body=None, url=API):
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

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"message": mask(e.read().decode(errors="replace"))[:300]}
    except urllib.error.URLError as e:
        return 0, {"message": mask(f"네트워크 오류: {e.reason}")}
    except (ValueError, OSError, http.client.HTTPException) as e:  # 예외 문구에 헤더 값이 들어갈 수 있어 종류만 찍는다
        return 0, {"message": f"요청 실패({type(e).__name__})"}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "push", "verify"])
    ap.add_argument("--token-file", help="선택. 없으면 GET은 무인증, PUT은 이 PC git 자격 증명")
    ap.add_argument("--out")
    ap.add_argument("--file")
    ap.add_argument("--message")
    ap.add_argument("--base", help="push: 4단계 fetch가 저장한 직전 배포본(work/prev.html) — PUT 직전 배포본이 이것과 같아야 한다. 실제 push는 필수")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ref", help="verify: push 성공 줄이 찍은 커밋 sha — 그 커밋의 본문을 ?ref=로 받는다(ref 없는 GET은 PUT 직후 캐시로 옛 본문일 수 있다)")
    a = ap.parse_args()
    base = None
    # 인자 오류는 네트워크 전에(GET 0)
    if a.ref is not None and a.cmd != "verify":
        print("[FAIL] --ref는 verify에만 — push는 늘 최신 sha를 다시 조회한다. GET 안 함")
        return 2
    if a.ref is not None and not re.fullmatch(r"[0-9a-fA-F]{7,40}", a.ref):
        print("[FAIL] --ref는 커밋 sha(16진 7~40자 — push 성공 줄 `배포 완료 커밋 …`의 값)만 — GET 안 함")
        return 2
    if a.ref:
        a.ref = a.ref.lower()
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
    print(f"배포 완료 커밋 {commit} · 파일 sha {res['content']['sha'][:7]} · 반영까지 1~2분")
    print(f"다음(읽기): deploy.py verify --file {a.file} --ref {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
