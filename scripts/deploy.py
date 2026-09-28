#!/usr/bin/env python3
"""배포본 index.html 받기·올리기(4·7단계) — 계산 로직 없음.

사용법(Code 탭 — references/code-tab.md):
    $PY scripts/deploy.py fetch  --out <index.html> [--token-file <파일>]
        GET contents API(무인증 먼저) → 파일 저장, sha 출력.
    $PY scripts/deploy.py push   --file <index.html> --base <4단계 fetch 파일> --message "<커밋 메시지>" [--dry-run] [--token-file <파일>]
        sha를 **다시 조회**한 뒤 PUT. 그 조회 본문 md5 ≠ --base md5면 "[FAIL] 배포본이 4단계 fetch 뒤 바뀜" exit 1(PUT 0).
        실제 push는 --base 필수(없으면 exit 2). --dry-run 은 sha 조회·base 대조·자격 증명 확인·쓰기 권한 확인
        (인증 GET /repos/{deploy_repo}의 permissions.push — 참/거짓만 찍고 거짓이면 [FAIL])·본문 준비까지만 하고 PUT을 보내지 않는다
        (아무 파일도 쓰지 않는다 — 2026-09-26 실측). "자격 증명 확인됨(출처: token-file|git)"만 찍는다.
        --dry-run 은 --file 없이도 된다(S0 사전 점검 — sha·자격 증명·쓰기 권한만 확인).
    $PY scripts/deploy.py verify --file <index.html> [--token-file <파일>]
        배포 후 재수령본 md5 = 로컬 md5 인지. 다르면 exit 1 — 다시 PUT하지 않는다(재PUT은 사용자 결정).

자격 증명(2026-09-28 Code 탭 회차):
  - GET(fetch·verify·push 전 sha)은 무인증으로 먼저 보내고, 403·429(무인증 rate limit)일 때만 자격 증명으로 1회 다시 보낸다.
  - PUT은 --token-file이 있으면 그 파일, 없으면 이 PC의 git 자격 증명(`git credential fill`, github.com)을 subprocess로 얻는다
    (credential.interactive=false · GIT_TERMINAL_PROMPT=0 · GCM_INTERACTIVE=never · askpass 변수 제거 — 창·프롬프트를 띄우지 않는다). 못 얻으면 [FAIL] exit 1.
  - 자격 증명 값은 변수에만 둔다 — 출력·파일·로그·예외 문구 어디에도 남기지 않는다(한 줄 토큰 형식이 아니면 쓰지 않고,
    요청 예외는 종류만 — 네트워크 연결 오류만 소켓 사유 문구, 헤더 값 없음). --token-file은 바이트로 읽어 UTF-16(BOM FF FE·FE FF)과
    UTF-8(BOM 허용)을 가리고, 없거나 못 읽으면 "[FAIL] 자격 증명을 얻지 못함(출처: token-file)"(Traceback 없음).
    `push --dry-run`은 값을 얻은 뒤 인증 GET(읽기)으로 배포 저장소 permissions.push까지 본다(2026-09-28 수정 회차 2 N1). 저장소는 config deploy_repo.
"""
import argparse
import base64
import hashlib
import http.client
import json
import os
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
REPO_API = f"https://api.github.com/repos/{CFG['deploy_repo']}"
API = f"{REPO_API}/contents/index.html"


def usable(tok):
    """헤더에 넣을 수 있는 한 줄 토큰인지(공백·개행·비 ASCII 없음). 아니면 None — 값은 어디에도 찍지 않는다
    (개행이 든 값을 헤더에 넣으면 http.client가 값 전체를 예외 문구에 담는다)."""
    return tok if tok and tok.isascii() and not any(c.isspace() for c in tok) else None


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
        "token-file": "토큰 파일이 한 줄 토큰(공백·개행 없음)인지 사용자가 확인"}


def credential(token_file):
    """(값, 출처). 출처 = "token-file" | "git". 값이 None이면 못 얻은 것."""
    if token_file:
        return token_of(token_file), "token-file"
    return git_credential(), "git"


def api(token, method="GET", body=None, url=API):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None)
    if token:
        req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    if method == "GET":
        req.add_header("Cache-Control", "no-cache")  # 무인증 응답은 공용 캐시(max-age 60) — PUT 직후 verify가 옛 본문을 받지 않게
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"message": e.read().decode(errors="replace")[:300]}
    except urllib.error.URLError as e:
        return 0, {"message": f"네트워크 오류: {e.reason}"}
    except (ValueError, OSError, http.client.HTTPException) as e:  # 예외 문구에 헤더 값이 들어갈 수 있어 종류만 찍는다
        return 0, {"message": f"요청 실패({type(e).__name__})"}


def get(token_file):
    """무인증 GET → 403·429면 자격 증명으로 1회. (status, res, 인증 출처 또는 None)."""
    status, res = api(None)
    if status in (403, 429):
        tok, src = credential(token_file)
        if not tok:
            return status, res, None
        status, res = api(tok)
        return status, res, src
    return status, res, None


def md5(data):
    return hashlib.md5(data).hexdigest()


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
    a = ap.parse_args()
    base = None
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
    status, res, how = get(a.token_file)
    if status != 200:
        print(f"GET {status}: {res.get('message', '')}")
        print("무인증 GET이 막히고(403·429) 자격 증명으로도 안 되면 `git clone https://github.com/LeeKwanBeom/saero-pilates-report`로 받는다(SKILL.md 4단계).")
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
    with open(a.file, "rb") as f:
        local = f.read()
    if a.cmd == "verify":
        same = md5(local) == md5(content)
        print(f"재수령본 sha {sha} · md5 {md5(content)[:8]}… vs 로컬 {md5(local)[:8]}… → {'일치' if same else '불일치'}")
        if not same:
            print("[FAIL] 불일치 — 다시 PUT하지 않는다. 위 sha·md5를 보고하고 재PUT은 사용자가 정한다(SKILL.md 7단계)")
        return 0 if same else 1
    if base is not None:  # PUT에 쓸 sha를 준 바로 그 GET 본문이 4단계 fetch 파일과 같아야 한다(그 사이 다른 배포가 있었으면 덮어쓰지 않는다)
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
    if status not in (200, 201):
        print(f"PUT {status}: {res.get('message', '')} — 자격 증명 출처({src})가 배포 저장소({CFG['deploy_repo']}) 쓰기 권한이 있는지 확인")
        return 1
    print(f"배포 완료 커밋 {res['commit']['sha'][:7]} · 파일 sha {res['content']['sha'][:7]} · 반영까지 1~2분")
    return 0


if __name__ == "__main__":
    sys.exit(main())
