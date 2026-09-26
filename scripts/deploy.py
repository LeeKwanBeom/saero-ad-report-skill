#!/usr/bin/env python3
"""배포본 index.html 받기·올리기(4·7단계) — 계산 로직 없음.

사용법:
    python3 scripts/deploy.py fetch  --token-file <파일> --out <index.html>
        GET contents API → 파일 저장, sha 출력. 토큰이 없거나 403이면 `git clone`으로 받으라고 안내(진단·검증 회차).
    python3 scripts/deploy.py push   --token-file <파일> --file <index.html> --message "<커밋 메시지>" [--dry-run]
        sha를 **다시 조회**한 뒤 PUT. --dry-run 은 sha 조회와 본문 준비까지만 하고 PUT을 보내지 않는다
        (아무 파일도 쓰지 않는다 — 2026-09-26 실측).
    python3 scripts/deploy.py verify --token-file <파일> --file <index.html>
        배포 후 재수령본 md5 = 로컬 md5 인지.
토큰은 파일에서만 읽는다(채팅에서 옮겨 적지 말 것 — 09-23 교훈). 저장소는 config deploy_repo.
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

from reportlib import load_config

CFG = load_config()
API = f"https://api.github.com/repos/{CFG['deploy_repo']}/contents/index.html"


def token_of(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def api(token, method="GET", body=None):
    req = urllib.request.Request(API, method=method, data=json.dumps(body).encode() if body else None)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"message": e.read().decode()[:300]}


def md5(data):
    return hashlib.md5(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "push", "verify"])
    ap.add_argument("--token-file", required=True)
    ap.add_argument("--out")
    ap.add_argument("--file")
    ap.add_argument("--message")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    token = token_of(a.token_file)
    status, res = api(token)
    if status != 200:
        print(f"GET {status}: {res.get('message', '')}")
        print("토큰이 없거나 403이면 `git clone https://github.com/LeeKwanBeom/saero-pilates-report`로 받는다(SKILL.md 4단계).")
        return 1
    sha, content = res["sha"], base64.b64decode(res["content"])
    if a.cmd == "fetch":
        with open(a.out, "wb") as f:
            f.write(content)
        print(f"저장 {a.out} ({len(content.splitlines())}행, md5 {md5(content)[:8]}…) sha {sha}")
        return 0
    with open(a.file, "rb") as f:
        local = f.read()
    if a.cmd == "verify":
        same = md5(local) == md5(content)
        print(f"재수령본 md5 {md5(content)[:8]}… vs 로컬 {md5(local)[:8]}… → {'일치' if same else '불일치'}")
        return 0 if same else 1
    body = {"message": a.message or "리포트 갱신", "content": base64.b64encode(local).decode(), "sha": sha}
    print(f"최신 sha {sha}, 본문 {len(local):,}바이트 ({len(local.splitlines())}행, md5 {md5(local)[:8]}…)")
    if a.dry_run:
        print("[dry-run] PUT을 보내지 않음. 파일 변경 없음.")
        return 0
    status, res = api(token, "PUT", body)
    if status not in (200, 201):
        print(f"PUT {status}: {res.get('message', '')} — 다른 저장소 토큰은 아닌지 확인(SKILL.md 토큰 표)")
        return 1
    print(f"배포 완료 커밋 {res['commit']['sha'][:7]} · 파일 sha {res['content']['sha'][:7]} · 반영까지 1~2분")
    return 0


if __name__ == "__main__":
    sys.exit(main())
