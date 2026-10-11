#!/usr/bin/env python3
"""scripts/deploy.py 오프라인 검사 — 가짜 GitHub API + 가짜 git 자격 증명 도우미(네트워크 0, 이 PC 실제 자격 증명 0).

실행: "$PY" tests/test_deploy.py   (unittest, 저장소 루트에서 Git Bash. git이 필요 — 없으면 skip)
격리: deploy.py를 자식 파이썬으로 돌린다. 자식 환경은 호출 환경의 `GIT_*` 변수를 전부 지우고(GIT_DIR 등으로 실제 저장소·도우미에
      닿지 않게) GIT_CONFIG_NOSYSTEM=1 · GIT_CONFIG_GLOBAL=<임시 설정 — 가짜 도우미만> · GIT_CEILING_DIRECTORIES=<임시 폴더의 부모>라
      `git credential fill`이 이 PC의 자격 증명 관리자(GCM)에 닿지 않는다. urllib.request.urlopen은 가짜로 바꿔 끼워
      요청(메서드·URL·Authorization)을 임시 파일에 적고 시나리오 응답을 돌려준다(api.github.com 요청 0).
검사(2026-09-28 수정 회차 2 N4):
  1 가짜 자격 증명 값이 stdout·stderr에 0건 — 값은 Authorization 헤더에만 간다(헤더에 실제로 실렸는지도 확인해 빈 시험이 아님을 보인다)
  2 dry-run이면 PUT 0(--file 있음·없음) · 3 --base 불일치 → [FAIL] exit 1·PUT 0, 일치 → PUT 1, 실제 push에 --base 없음 → exit 2·요청 0
  4 permissions.push 거짓 → [FAIL] exit 1, 권한 조회 401 → [FAIL] exit 1 · 5 도우미 없음 → [FAIL] 자격 증명을 얻지 못함(출처: git)
  6 token_of: 없는 파일 → None(Traceback 없음) · UTF-16LE·BE(BOM) · UTF-8 BOM · 깨진 바이트
  (수정 회차 3) 7 permissions 필드 없음 → [FAIL] · 못 읽는 --base·--file 없는 --base → exit 2 · PUT 409·403 문구(오류 문구가 헤더 값을
  되돌려 줘도 `***`) · precheck 도장 없음·불일치 → 실제 push [FAIL]·PUT 0, dry-run은 [주의]
  (2026-09-29 후속) 8 push 성공 줄 = 커밋 전체 sha + `verify --ref` 다음 명령 · ref 없는 GET이 옛 본문(캐시)이면 verify 불일치에
  "캐시일 수 있다 … 재PUT 금지" 문구, `--ref`는 `?ref=` 조회로 새 본문 → 일치(PUT 0) · 커밋 본문 자체가 다르면 캐시 문구 없이 불일치 ·
  없는 커밋 404 · `--ref` 인자 오류(verify 밖·16진 7~40자 아님)는 GET 전에 exit 2
  (2026-10-06 회차 2, 막음 M4) 9 레이아웃 판 게이트 4건 — --file·--base 의 `<meta name="report-layout">` 다름(한쪽 없음·값 다름) → 실제 push
  [FAIL] exit 1·요청 0 · `--layout-change` → PUT 1 · 같음 → 게이트 문구 없이 PUT 1 · dry-run → [주의]·PUT 0. 기존 PREV·WORK 는 둘 다 meta 가 없어 "같음"
  (2026-10-11 배포 뒤 공개 사이트 확인 — 안 B) 10 live·redeploy·public·verify 다음 live — 가짜 urlopen 이 github.io(바이트 본문·Date·Age·Content-Encoding)·
  githubstatus·Actions·Deployments·git 끝점을 흉내 내고 time.time·time.sleep 은 가짜 시계(한 시험 몇 초 안). 요청 로그에 시각·Accept-Encoding·
  POST/PATCH 본문. 가짜 자격 증명 도우미는 불릴 때마다 helper_calls 에 한 줄(credential() 호출 수). 완료 기준 표(last-audit 탐색 기준선 4절 + 구현
  지시 18~28) 줄 번호를 각 시험 docstring 에 적는다.
"""
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글 — 다른 시험·스크립트와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
GIT = shutil.which("git")
FAKE = "ghp_FAKE0928deployTESTvalue"           # 가짜 자격 증명 값 — 출력에 이것(또는 가운데 조각)이 나오면 실패
FRAG = "0928deployTEST"
PREV = b"<html><!-- prev --></html>\n"         # 4단계 fetch로 받은 직전 배포본(가짜)
WORK = b"<html><!-- work --></html>\n"         # 작업본
OTHER = b"<html><!-- other deploy --></html>\n"
LAY_B = b'<html><head><meta name="report-layout" content="r2026-10-B"></head><!-- work B --></html>\n'      # 레이아웃 판 작업본(가짜)
LAY_B_PREV = b'<html><head><meta name="report-layout" content="r2026-10-B"></head><!-- prev B --></html>\n'  # 같은 판 직전 배포본
LAY_X_PREV = b'<html><head><meta name="report-layout" content="r2026-10-X"></head><!-- prev X --></html>\n'  # 다른 판 직전 배포본
T = 1791680000                                  # 가짜 시계 시작(2026-10-11 09:53:20 KST)
COMMIT = "c0ffee" + "1" * 34                     # 이번 push 커밋(40자)
NEWC = "beef00" + "2" * 34                       # redeploy 가 만든 빈 커밋
OTHERC = "0dd000" + "3" * 34                     # 다른 배포 커밋
TREE = "7eee00" + "4" * 34                       # HEAD tree
WF = "pages build and deployment"
sys.path.insert(0, SCRIPTS)
from reportlib import load_config as _load_config  # noqa: E402
SITE = _load_config()["deploy_site_url"]          # 공개 주소(config — 시험도 하드코딩하지 않는다)


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def run_obj(status="in_progress", conclusion=None, created=T - 10, updated=None, num=160, sha=COMMIT, msg="리포트 갱신: 시험", rid=111):
    """Actions 실행 객체(api_probe.out 꼴 — head_commit 메시지·시각 포함)."""
    return {"id": rid, "run_number": num, "name": WF, "head_sha": sha, "status": status, "conclusion": conclusion,
            "created_at": iso(created), "updated_at": iso(updated if updated is not None else created + 5),
            "head_commit": {"message": msg, "timestamp": iso(created - 2)}}


def runs(*rs):
    return [200, {"total_count": len(rs), "workflow_runs": list(rs)}]

RUNNER = r'''
import base64, email.utils, gzip, hashlib, io, json, os, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.environ["T_SCRIPTS"])
scen = json.load(open(os.environ["T_SCEN"], encoding="utf-8"))
CLOCK = [float(scen["t_start"])]          # 가짜 시계 — deploy.py 는 time.time()·time.sleep() 만 쓴다
time.time = lambda: CLOCK[0]
time.sleep = lambda s: CLOCK.__setitem__(0, CLOCK[0] + max(0.0, float(s)))
STATE = {"patched": False, "unauth": 0}

class Resp:
    def __init__(self, status, body, headers=None):
        self.status = status
        self._b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.headers = headers or {}
    def read(self):
        return self._b
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False

def timeline(key):
    """scen[key] = [[until, 값], …] — 지금 가짜 시각 < until 인 첫 값(until null = 끝까지)."""
    for until, val in scen.get(key) or []:
        if until is None or CLOCK[0] < until:
            return val
    return None

def fake_urlopen(req, timeout=None):
    m, url, auth = req.get_method(), req.full_url, req.get_header("Authorization")
    rec = {"method": m, "url": url, "auth": auth, "enc": req.get_header("Accept-encoding"), "t": CLOCK[0]}
    if m == "PUT":  # 실제로 보낸 본문의 md5(도장과 같은 바이트인지)
        rec["body_md5"] = hashlib.md5(base64.b64decode(json.loads(req.data)["content"])).hexdigest()
    elif m in ("POST", "PATCH"):
        rec["body"] = json.loads(req.data)
    with open(os.environ["T_LOG"], "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    path, _, query = url.partition("?")
    hdrs = {}
    if url.startswith(scen["site"]):  # 공개 주소 — 바이트 본문 · Date · Age(= 지금 − CDN 확인 시각) · gzip 요청이면 Content-Encoding gzip
        ent = timeline("public") or {"status": 404}
        if ent.get("raise"):
            raise urllib.error.URLError("fake down")
        hdrs = {"Date": email.utils.formatdate(CLOCK[0], usegmt=True), "Cache-Control": "max-age=600"}
        if ent["status"] >= 400:
            raise urllib.error.HTTPError(url, ent["status"], "err", hdrs, io.BytesIO(b"<html>error</html>"))
        body = base64.b64decode(scen["bodies"][ent["body"]])
        if "checked" in ent:
            hdrs["Age"] = str(int(CLOCK[0] - ent["checked"]))
        if "gzip" in (rec["enc"] or ""):
            body, hdrs["Content-Encoding"] = gzip.compress(body), "gzip"
        return Resp(200, body, hdrs)
    if url == scen["status_url"]:
        status, body = scen.get("gh_status") or [200, {"components": [{"name": "Pages", "status": "operational"}, {"name": "Actions", "status": "operational"}]}]
        if status >= 400:
            raise urllib.error.HTTPError(url, status, "err", {}, io.BytesIO(b"{}"))
        return Resp(status, body)
    if url.startswith("https://api.github.com/") and not auth and m == "GET" and not path.endswith("/contents/index.html"):
        STATE["unauth"] += 1
        lim = scen.get("unauth_limit")
        if lim is not None and STATE["unauth"] > lim:  # 이 PC 공유 무인증 60/h 가 다 찬 경우 흉내
            raise urllib.error.HTTPError(url, 403, "rate limit", {"X-RateLimit-Reset": str(int(CLOCK[0]) + 1200)},
                                         io.BytesIO(json.dumps({"message": "API rate limit exceeded"}).encode()))
    if m == "GET" and path.endswith("/contents/index.html"):
        if scen.get("edit_on_get"):  # GET을 기다리는 사이 작업본이 바뀌는 경우 흉내(편집기 저장·다른 세션)
            with open(scen["edit_on_get"], "wb") as f:
                f.write(b"<html>edited AFTER precheck</html>\n")
        if query.startswith("ref="):  # 커밋 고정 조회 — 그 커밋의 본문(없는 커밋이면 404)
            ref = scen.get("refs", {}).get(query[len("ref="):])
            status, body = (200, {"sha": "sha1ref", "content": ref}) if ref else (404, {"message": "No commit found for the ref"})
        else:  # ref 없는 조회 — PUT 직후 캐시가 옛 본문을 돌려주는 경우는 content_b64에 옛 본문을 둔다(2026-09-29 실측)
            status, body = 200, {"sha": "sha0prev", "content": scen["content_b64"]}
    elif m == "GET" and url.endswith("/repos/" + scen["repo"]):
        status, body = scen["repo_auth"] if auth else [200, {"name": "x"}]
    elif m == "PUT":
        if scen.get("put_raise"):  # PUT 도중 끊김(응답 못 받음) 흉내 — 서버가 받았는지 모른다
            raise TimeoutError("timed out")
        status, body = scen.get("put") or [200, {"commit": {"sha": "c0ffee1234"}, "content": {"sha": "f11e5ha000"}}]
        if isinstance(body.get("message"), str):  # 서버·프록시가 요청 헤더를 되돌려 주는 경우 흉내
            body = dict(body, message=body["message"].replace("{AUTH}", auth or ""))
    elif m == "GET" and path.endswith("/actions/runs") and "head_sha=" in query:
        status, body = timeline("runs_head") or [200, {"total_count": 0, "workflow_runs": []}]
    elif m == "GET" and path.endswith("/actions/runs"):
        status, body = scen.get("runs_all") or [200, {"workflow_runs": []}]
    elif m == "GET" and path.rsplit("/", 1)[-1].isdigit() and path.rsplit("/", 2)[-2] == "runs":   # 실행 하나(cap 다시 읽기)
        status, body = timeline("run_by_id") or [404, {"message": "Not Found"}]
    elif m == "GET" and path.endswith("/jobs"):
        status, body = (scen.get("jobs_all") if "filter=all" in query else scen.get("jobs")) or [200, {"total_count": 0, "jobs": []}]
    elif m == "GET" and path.endswith("/statuses"):
        status, body = scen.get("statuses") or [200, []]
    elif m == "GET" and path.endswith("/deployments"):
        status, body = scen.get("deployments") or [200, []]
    elif m == "GET" and path.endswith("/git/ref/heads/main"):
        status, body = (scen.get("ref_after_patch") if STATE["patched"] and scen.get("ref_after_patch")
                        else timeline("ref") or [200, {"ref": "refs/heads/main", "object": {"sha": scen.get("head"), "type": "commit"}}])
    elif m == "GET" and "/git/commits/" in path:
        c = (scen.get("commits") or {}).get(path.rsplit("/", 1)[-1])
        status, body = (200, c) if c else (404, {"message": "Not Found"})
    elif m == "POST" and path.endswith("/git/commits"):
        if scen.get("post_raise"):
            raise TimeoutError("timed out")
        status, body = scen.get("post_commit") or [404, {"message": "no post scenario"}]
    elif m == "PATCH" and path.endswith("/git/refs/heads/main"):
        if scen.get("patch_raise"):
            STATE["patched"] = True
            raise TimeoutError("timed out")
        status, body = scen.get("patch_ref") or [404, {"message": "no patch scenario"}]
        STATE["patched"] = status < 400
    else:
        status, body = 404, {"message": "no route"}
    if status >= 400:
        raise urllib.error.HTTPError(url, status, "err", {}, io.BytesIO(json.dumps(body).encode()))
    return Resp(status, body)

urllib.request.urlopen = fake_urlopen
import deploy
sys.argv = ["deploy.py"] + json.loads(os.environ["T_ARGV"])
sys.exit(deploy.main())
'''


@unittest.skipUnless(GIT, "git 없음")
class DeployTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()
        p = lambda n: os.path.join(self.td, n)
        self.runner, self.log, self.scen = p("runner.py"), p("requests.jsonl"), p("scen.json")
        with open(self.runner, "w", encoding="utf-8") as f:
            f.write(RUNNER)
        helper = p("fakehelper.sh")
        self.helper_calls = p("helper_calls")                                # credential() 가 도우미를 부른 수(한 번에 한 줄)
        with open(helper, "w", encoding="utf-8", newline="\n") as f:
            f.write(f'#!/bin/sh\n[ "$1" = get ] || exit 0\necho x >> \'{self.helper_calls.replace(os.sep, "/")}\'\n'
                    f'echo username=fakeuser\necho password={FAKE}\n')
        self.cfg_helper, self.cfg_none = p("gitconfig-helper"), p("gitconfig-none")
        with open(self.cfg_helper, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"[credential]\n\thelper = \"!sh '{helper.replace(os.sep, '/')}'\"\n")
        with open(self.cfg_none, "w", encoding="utf-8", newline="\n") as f:
            f.write("[core]\n\tautocrlf = false\n")
        for name, data in (("prev.html", PREV), ("work.html", WORK), ("other.html", OTHER)):
            with open(p(name), "wb") as f:
                f.write(data)
        self.prev, self.work, self.other = p("prev.html"), p("work.html"), p("other.html")
        self.stamp = p("precheck_ok.md5")                                    # precheck.sh가 전부 통과하면 쓰는 도장(작업본·직전 배포본 md5·모드)
        self.write_stamp()

    def write_stamp(self, work=WORK, prev=PREV, mode="full"):
        with open(self.stamp, "w", encoding="utf-8") as f:
            f.write(f"{hashlib.md5(work).hexdigest()}  work.html\n{hashlib.md5(prev).hexdigest()}  prev.html\nmode {mode}\n")

    def tearDown(self):
        shutil.rmtree(self.td)

    def run_deploy(self, argv, repo_auth=(200, {"permissions": {"admin": True, "push": True, "pull": True}}),
                   deployed=PREV, helper=True, put=None, edit_on_get=None, put_raise=False, refs=None, extra=None, env_extra=None):
        sys.path.insert(0, SCRIPTS)
        from reportlib import load_config
        cfg = load_config()
        scen = {"content_b64": base64.b64encode(deployed).decode(), "repo": cfg["deploy_repo"],
                "repo_auth": list(repo_auth), "put": list(put) if put else None, "edit_on_get": edit_on_get, "put_raise": put_raise,
                "refs": {k: base64.b64encode(v).decode() for k, v in (refs or {}).items()},
                "t_start": T, "site": cfg["deploy_site_url"], "status_url": cfg["live_check"]["status_url"],
                "bodies": {k: base64.b64encode(v).decode() for k, v in (("work", WORK), ("prev", PREV), ("other", OTHER))}}
        scen.update(extra or {})
        with open(self.scen, "w", encoding="utf-8") as f:
            json.dump(scen, f, ensure_ascii=False)
        if os.path.exists(self.log):
            os.remove(self.log)
        if os.path.exists(self.helper_calls):
            os.remove(self.helper_calls)
        env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "PYTHONUTF8", "SAERO_"))}   # 호출 환경의 GIT_DIR 등 전부 제거
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=self.cfg_helper if helper else self.cfg_none,
                   GIT_CEILING_DIRECTORIES=os.path.dirname(self.td),
                   T_SCRIPTS=SCRIPTS, T_SCEN=self.scen, T_LOG=self.log, T_ARGV=json.dumps(argv))
        env.update(env_extra or {})
        r = subprocess.run([sys.executable, self.runner], cwd=self.td, env=env, capture_output=True)
        out, err = r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
        for stream in (out, err):
            self.assertNotIn(FAKE, stream)                  # 자격 증명 값 출력 0(stdout·stderr)
            self.assertNotIn(FRAG, stream)
        reqs = []
        if os.path.exists(self.log):
            with open(self.log, encoding="utf-8") as f:
                reqs = [json.loads(line) for line in f]
        return r.returncode, out, err, reqs

    def methods(self, reqs):
        return [(q["method"], q["url"].rsplit("/", 1)[-1], bool(q["auth"])) for q in reqs]

    def test_dry_run_without_file_checks_permission_and_never_puts(self):
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run"])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("자격 증명 확인됨(출처: git)", out)
        self.assertIn("배포 저장소 쓰기 권한(permissions.push): 참", out)
        self.assertIn("[dry-run] PUT을 보내지 않음", out)
        self.assertEqual(self.methods(reqs), [("GET", "index.html", False), ("GET", "saero-pilates-report", True)])  # 무인증 조회 → 인증 권한 조회
        self.assertEqual(reqs[1]["auth"], f"token {FAKE}")          # 값은 헤더로만 간다(이 시험이 빈 시험이 아니라는 확인)
        self.assertNotIn("PUT", [q["method"] for q in reqs])

    def test_dry_run_with_file_and_base(self):
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m", "--dry-run"])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("배포본 = --base(4단계 fetch)", out)
        self.assertIn("precheck 도장 = 작업본 md5", out)
        self.assertIn("permissions.push): 참", out)
        self.assertNotIn("PUT", [q["method"] for q in reqs])

    def test_permission_false_or_lookup_error_fails(self):
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run"], repo_auth=(200, {"permissions": {"push": False, "pull": True}}))
        self.assertEqual(rc, 1, out + err)
        self.assertIn("permissions.push): 거짓", out)
        self.assertIn("[FAIL] 이 자격 증명은 배포 저장소", out)
        self.assertNotIn("PUT", [q["method"] for q in reqs])
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--dry-run"],
                                             repo_auth=(401, {"message": "Bad credentials"}))
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 배포 저장소 권한 조회 실패", out)
        self.assertNotIn("[dry-run] PUT을 보내지 않음", out)

    def test_base_mismatch_stops_before_put(self):
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"], deployed=OTHER)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 배포본이 4단계 fetch 뒤 바뀜", out)
        self.assertEqual(self.methods(reqs), [("GET", "index.html", False)])   # PUT 0 · 자격 증명 요청 0
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m", "--dry-run"], deployed=OTHER)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 배포본이 4단계 fetch 뒤 바뀜", out)

    def test_real_push_requires_base_and_puts_once_when_base_matches(self):
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--message", "m"])
        self.assertEqual(rc, 2, out + err)
        self.assertIn("[FAIL] 실제 push에는 --base", out)
        self.assertEqual(reqs, [])                                            # 요청 0
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("저장소 반영 커밋 c0ffee1234 · 파일 sha", out)              # 커밋 전체 sha(verify --ref에 그대로)
        self.assertNotIn("배포 완료", out)                                     # 2026-10-11 — "배포 완료"는 live exit 0 의 기록 머리에서만(완료 기준 1·22)
        self.assertIn(f"다음(읽기): deploy.py verify --file {self.work} --ref c0ffee1234", out)
        puts = [q for q in reqs if q["method"] == "PUT"]
        self.assertEqual(len(puts), 1)
        self.assertEqual(puts[0]["auth"], f"token {FAKE}")

    def test_verify_ref_reads_commit_not_stale_cache(self):
        """2026-09-29 후속 1: PUT 직후 ref 없는 contents GET이 옛 본문(캐시)을 돌려줘 verify가 거짓 불일치 —
        ref 없이 불일치면 "캐시일 수 있다" 문구·재PUT 금지, --ref <커밋>이면 ?ref= 조회로 새 본문 → 일치. PUT 0."""
        refs = {"c0ffee1234": WORK}                                              # PUT이 만든 커밋 = 작업본
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work], deployed=PREV, refs=refs)   # 캐시가 옛 본문
        self.assertEqual(rc, 1, out + err)
        self.assertIn("→ 불일치", out)
        self.assertIn("[FAIL] 불일치 — PUT 직후라면 캐시일 수 있다: ls-remote HEAD와 --ref로 다시 verify(읽기). 재PUT 금지", out)
        self.assertEqual([(q["method"], q["url"].endswith("/contents/index.html")) for q in reqs], [("GET", True)])
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", "c0ffee1234"], deployed=PREV, refs=refs)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("재수령본 (ref c0ffee1234 기준) sha", out)
        self.assertIn("→ 일치", out)
        self.assertEqual([q["url"].rsplit("/", 1)[-1] for q in reqs if "/contents/" in q["url"]], ["index.html?ref=c0ffee1234"])   # ref 조회 1회뿐
        self.assertEqual([q["url"].split("/repos/", 1)[-1].split("/", 2)[-1] for q in reqs if "/contents/" not in q["url"]],
                         ["git/ref/heads/main"])                                          # 2026-10-11 B-7: 일치 뒤 다음 live 커밋을 고르는 HEAD 읽기(무인증)
        self.assertEqual([q for q in reqs if q["method"] != "GET" or q["auth"]], [])                   # PUT 0 · 자격 증명 0
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", "C0FFEE1"], refs={"c0ffee1": WORK})
        self.assertEqual(rc, 0, out + err)                                        # 짧은 sha·대문자(소문자로 조회)
        self.assertTrue(reqs[0]["url"].endswith("?ref=c0ffee1"))
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", "c0ffee1234"], refs={"c0ffee1234": OTHER})
        self.assertEqual(rc, 1, out + err)                                        # 커밋 본문 자체가 다름 — 캐시 문구가 아니다
        self.assertIn("[FAIL] 불일치 — ref c0ffee1234의 본문이 로컬과 다름(커밋 고정 조회라 캐시 아님)", out)
        self.assertNotIn("캐시일 수 있다", out)
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", "deadbee"], refs=refs)
        self.assertEqual(rc, 1, out + err)                                        # 없는 커밋
        self.assertIn("[FAIL] ref deadbee의 index.html을 찾지 못함", out)

    def test_ref_argument_errors_before_network(self):
        """--ref는 verify에만·16진 7~40자만 — 아니면 GET 전에 exit 2(요청 0). URL에 &·# 같은 값이 들어가지 않는다."""
        for argv, want in ((["verify", "--file", self.work, "--ref", "main"], "[FAIL] --ref는 커밋 sha"),
                           (["verify", "--file", self.work, "--ref", "c0ffee1&x=1"], "[FAIL] --ref는 커밋 sha"),
                           (["verify", "--file", self.work, "--ref", "abc12"], "[FAIL] --ref는 커밋 sha"),
                           (["push", "--file", self.work, "--base", self.prev, "--message", "m", "--ref", "c0ffee1234"], "[FAIL] --ref는 verify에만"),
                           (["fetch", "--out", os.path.join(self.td, "x.html"), "--ref", "c0ffee1234"], "[FAIL] --ref는 verify에만")):
            rc, out, err, reqs = self.run_deploy(argv)
            self.assertEqual(rc, 2, (argv, out + err))
            self.assertIn(want, out)
            self.assertEqual(reqs, [], argv)

    def test_permission_field_missing_fails(self):
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run"], repo_auth=(200, {"name": "x"}))   # 응답에 permissions 없음
        self.assertEqual(rc, 1, out + err)
        self.assertIn("permissions.push): 거짓", out)
        self.assertIn("[FAIL] 이 자격 증명은 배포 저장소", out)

    def test_base_argument_errors_exit_2_without_requests(self):
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", os.path.join(self.td, "없음.html"), "--message", "m"])
        self.assertEqual(rc, 2, out + err)
        self.assertIn("[FAIL] --base 파일을 읽을 수 없음", out)
        self.assertEqual(reqs, [])
        rc, out, err, reqs = self.run_deploy(["push", "--base", self.prev, "--dry-run"])        # --file 없이 --base만
        self.assertEqual(rc, 2, out + err)
        self.assertIn("[FAIL] --base는 --file과 함께만", out)
        self.assertEqual(reqs, [])

    def test_put_409_and_403_messages_mask_echoed_credential(self):
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"],
                                             put=(409, {"message": "sha mismatch; you sent {AUTH}"}))
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치) — PUT 안 됨, 4단계부터 다시 할지는 사용자가 정한다", out)   # 수정 기록 3 W8 문구 그대로(X13)
        self.assertIn("you sent token ***", out)                              # 되돌아온 헤더 값은 가려진다(run_deploy가 값 0건도 단언)
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"],
                                             put=(403, {"message": "Resource not accessible by integration {AUTH}"}))
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] PUT 403 — 쓰기 권한 없음", out)
        self.assertIn("***", out)

    def test_precheck_stamp_required_for_real_push(self):
        """W11: 작업본 옆 도장(precheck_ok.md5) = --file md5일 때만 PUT. 없음·불일치 → [FAIL] exit 1(요청 0 — 네트워크 전에 본다), dry-run은 [주의]."""
        os.remove(self.stamp)
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] precheck 통과본이 아님 — PUT 안 함(도장 없음", out)
        self.assertEqual(reqs, [])
        with open(self.stamp, "w", encoding="utf-8") as f:
            f.write(f"{hashlib.md5(OTHER).hexdigest()}  work.html\n{hashlib.md5(PREV).hexdigest()}  prev.html\nmode full\n")   # 다른 파일의 도장
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] precheck 통과본이 아님", out)
        self.assertIn("precheck 뒤 바뀌었거나 다른 파일", out)
        self.assertEqual(reqs, [])
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m", "--dry-run"])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("[주의] precheck 통과본이 아님", out)
        self.assertNotIn("PUT", [q["method"] for q in reqs])
        with open(self.stamp, "wb") as f:                                       # UTF-8이 아닌 도장(손으로 쓴·다른 인코딩) — Traceback 대신 사유
            f.write(b"\xb5\xb5\xc0\xe5 cp949\n")
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] precheck 통과본이 아님 — PUT 안 함(도장을 읽을 수 없음(UnicodeDecodeError)", out)
        self.assertNotIn("Traceback", err)
        self.assertEqual(reqs, [])

    def test_file_read_once_put_body_equals_stamped_bytes(self):
        """리뷰 반영(W11): --file은 한 번만 읽는다 — 도장 대조 뒤 GET을 기다리는 사이 작업본이 바뀌어도 PUT 본문은 도장과 같은 바이트."""
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"], edit_on_get=self.work)
        self.assertEqual(rc, 0, out + err)
        puts = [q for q in reqs if q["method"] == "PUT"]
        self.assertEqual([q["body_md5"] for q in puts], [hashlib.md5(WORK).hexdigest()])   # 바뀐 파일이 아니라 도장 찍힌 바이트

    def test_stamp_binds_prev_and_mode(self):
        """X2: 도장의 직전 배포본 md5 ≠ --base면(409 뒤 prev만 다시 받음) 실제 push FAIL·요청 0, dry-run [주의] ·
        옛 형식(1줄) 도장 FAIL · pending 도장은 막지 않고 [주의]."""
        other_prev = os.path.join(self.td, "other.html")                      # 4단계를 다시 받아 prev가 OTHER가 된 상황
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", other_prev, "--message", "m"], deployed=OTHER)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] precheck 통과본이 아님 — PUT 안 함(도장의 직전 배포본 md5", out)
        self.assertIn("4단계를 다시 받았으면 5·6단계부터", out)
        self.assertEqual(reqs, [])
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", other_prev, "--message", "m", "--dry-run"], deployed=OTHER)
        self.assertIn("[주의] precheck 통과본이 아님(도장의 직전 배포본 md5", out)
        with open(self.stamp, "w", encoding="utf-8") as f:
            f.write(f"{hashlib.md5(WORK).hexdigest()}  work.html\n")         # 옛 형식(수정 회차 3) — 직전 배포본·모드 줄 없음
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("도장 형식이 옛 판", out)
        self.assertEqual(reqs, [])
        self.write_stamp(mode="pending")                                        # 답 대기 배포용 통과본 — 막지 않는다
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("[주의] --pending 통과본(답 대기 배포용)", out)
        self.assertEqual([q["method"] for q in reqs].count("PUT"), 1)

    def test_put_result_unknown_and_already_applied(self):
        """X8: PUT 도중 끊김·5xx → "결과 모름 — 재PUT 금지, verify 먼저" exit 1 · 지금 배포본 = 작업본이면 "앞 PUT이 이미 반영됨" exit 0·PUT 0."""
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"], put_raise=True)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] PUT 결과 모름(요청 실패(TimeoutError)) — 반영됐을 수 있다. 재PUT 금지, 먼저 deploy.py verify --file", out)
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"],
                                             put=(502, {"message": "Bad Gateway"}))
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] PUT 결과 모름(", out)
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"], deployed=WORK)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨(verify로 확인). PUT 안 함", out)   # 지시 문구 그대로(md5는 끝에)
        self.assertEqual(self.methods(reqs), [("GET", "index.html", False)])       # PUT 0 · 자격 증명 요청 0

    def test_argument_errors_before_network_and_token_shape(self):
        """X9: --file·--out 없음은 GET 전에 exit 2 · --token-file ''은 git 자격 증명으로 넘어가지 않고 FAIL · 토큰은 [A-Za-z0-9_]만."""
        for argv, want in ((["fetch"], "[FAIL] fetch에는 --out이 필요"), (["verify"], "[FAIL] verify에는 --file이 필요"),
                           (["push", "--base", self.prev, "--message", "m"], "[FAIL] push에는 --file이 필요"),
                           (["push", "--message", "m"], "[FAIL] push에는 --file이 필요")):
            rc, out, err, reqs = self.run_deploy(argv)
            self.assertEqual(rc, 2, (argv, out + err))
            self.assertIn(want, out)
            self.assertEqual(reqs, [], argv)                                   # GET 0
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run", "--token-file", ""])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 자격 증명을 얻지 못함(출처: token-file)", out)
        self.assertEqual([q for q in reqs if q["auth"]], [])                   # git 도우미 값(FAKE)으로 넘어가지 않음
        sys.path.insert(0, SCRIPTS)
        import deploy
        for bad in ("ab-c", "ab.c", "a/b", "tok+1"):
            self.assertIsNone(deploy.usable(bad), bad)
        self.assertEqual(deploy.usable("github_pat_AB12_cd"), "github_pat_AB12_cd")

    def test_no_credential_helper_fails_cleanly(self):
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run"], helper=False)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 자격 증명을 얻지 못함(출처: git)", out)
        self.assertEqual([q for q in reqs if q["auth"]], [])
        self.assertNotIn("Traceback", err)

    def layout_files(self, prev):
        """레이아웃 판 작업본(LAY_B) + 주어진 직전 배포본 파일과 그 둘의 도장. (작업본 경로, 직전 배포본 경로)"""
        w, b = os.path.join(self.td, "lay_work.html"), os.path.join(self.td, "lay_prev.html")
        for path, data in ((w, LAY_B), (b, prev)):
            with open(path, "wb") as f:
                f.write(data)
        self.write_stamp(work=LAY_B, prev=prev)
        return w, b

    def test_layout_gate_meta_differs_fails_before_network(self):
        for label, prev in (("직전 배포본 meta 없음(옛 판)", PREV), ("meta 값이 다름", LAY_X_PREV)):
            with self.subTest(label):
                w, b = self.layout_files(prev)
                rc, out, err, reqs = self.run_deploy(["push", "--file", w, "--base", b, "--message", "m"], deployed=prev)
                self.assertEqual(rc, 1, out + err)
                self.assertIn("[FAIL] 레이아웃 판이 바뀜 — PUT 안 함", out)
                self.assertIn("--layout-change", out)
                self.assertEqual(reqs, [])                                    # 네트워크 전 — GET·PUT 0

    def test_layout_gate_layout_change_puts_once(self):
        w, b = self.layout_files(PREV)
        rc, out, err, reqs = self.run_deploy(["push", "--file", w, "--base", b, "--message", "m", "--layout-change"], deployed=PREV)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("레이아웃 판 바뀜", out)
        self.assertIn("저장소 반영 커밋 c0ffee1234", out)
        self.assertNotIn("배포 완료", out)
        puts = [q for q in reqs if q["method"] == "PUT"]
        self.assertEqual(len(puts), 1)
        self.assertEqual(puts[0]["body_md5"], hashlib.md5(LAY_B).hexdigest())

    def test_layout_gate_same_meta_passes_silently(self):
        w, b = self.layout_files(LAY_B_PREV)
        rc, out, err, reqs = self.run_deploy(["push", "--file", w, "--base", b, "--message", "m"], deployed=LAY_B_PREV)
        self.assertEqual(rc, 0, out + err)
        self.assertNotIn("레이아웃 판", out)                                   # 데이터 회차 — 게이트 문구 0
        self.assertEqual(len([q for q in reqs if q["method"] == "PUT"]), 1)
        self.write_stamp()                                                     # 기존 PREV·WORK — 둘 다 meta 없음 = 같음
        rc, out, err, reqs = self.run_deploy(["push", "--file", self.work, "--base", self.prev, "--message", "m"])
        self.assertEqual(rc, 0, out + err)
        self.assertNotIn("레이아웃 판", out)

    def test_layout_gate_dry_run_warns_and_never_puts(self):
        w, b = self.layout_files(PREV)
        rc, out, err, reqs = self.run_deploy(["push", "--file", w, "--base", b, "--message", "m", "--dry-run"], deployed=PREV)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("[주의] 레이아웃 판이 바뀜", out)
        self.assertIn("실제 push 에는 --layout-change", out)
        self.assertIn("[dry-run] PUT을 보내지 않음", out)
        self.assertNotIn("PUT", [q["method"] for q in reqs])

    def test_token_file_encodings_and_missing(self):
        sys.path.insert(0, SCRIPTS)
        import deploy
        p = lambda n: os.path.join(self.td, n)
        cases = {"le.txt": b"\xff\xfe" + "tokLE123\r\n".encode("utf-16-le"),          # Windows PowerShell 5.1 `'…' > 파일`
                 "be.txt": b"\xfe\xff" + "tokBE123".encode("utf-16-be"),
                 "bom8.txt": b"\xef\xbb\xbftokU8\n", "bad.txt": b"\xc3\x28tok\n"}
        for n, b in cases.items():
            with open(p(n), "wb") as f:
                f.write(b)
        self.assertEqual(deploy.token_of(p("le.txt")), "tokLE123")
        self.assertEqual(deploy.token_of(p("be.txt")), "tokBE123")
        self.assertEqual(deploy.token_of(p("bom8.txt")), "tokU8")
        self.assertIsNone(deploy.token_of(p("bad.txt")))
        self.assertIsNone(deploy.token_of(p("없는파일.txt")))
        rc, out, err, _ = self.run_deploy(["push", "--dry-run", "--token-file", p("없는파일.txt")])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 자격 증명을 얻지 못함(출처: token-file)", out)
        self.assertNotIn("Traceback", err)
        with open(p("fake16.txt"), "wb") as f:
            f.write(b"\xff\xfe" + FAKE.encode("utf-16-le"))
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run", "--token-file", p("fake16.txt")])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("자격 증명 확인됨(출처: token-file)", out)
        self.assertEqual(reqs[-1]["auth"], f"token {FAKE}")

    # ---------------------------------------------------------------- 2026-10-11 배포 뒤 공개 사이트 확인(live · redeploy · public — 안 B)
    def live(self, extra, more=(), helper=True, env_extra=None, commit=COMMIT):
        return self.run_deploy(["live", "--file", self.work, "--prev", self.prev, "--commit", commit] + list(more),
                               extra=extra, helper=helper, env_extra=env_extra)

    def redeploy(self, extra, more=(), helper=True, repo_auth=(200, {"permissions": {"push": True}}), commit=COMMIT):
        return self.run_deploy(["redeploy", "--file", self.work, "--prev", self.prev, "--commit", commit] + list(more),
                               extra=extra, helper=helper, repo_auth=repo_auth)

    def api_gets(self, reqs, auth=False):
        return [q for q in reqs if q["method"] == "GET" and q["url"].startswith("https://api.github.com/") and bool(q["auth"]) == auth]

    def polls(self, reqs):
        return [q for q in self.api_gets(reqs) if "head_sha=" in q["url"]]

    def site_reqs(self, reqs):
        return [q for q in reqs if q["url"].startswith(SITE)]

    def helper_count(self):
        if not os.path.exists(self.helper_calls):
            return 0
        with open(self.helper_calls, encoding="utf-8") as f:
            return len(f.read().split())

    def live_ok(self):
        p = os.path.join(self.td, "live_ok")
        if not os.path.exists(p):
            return None
        with open(p, encoding="utf-8") as f:
            return f.read()

    def test_live_normal_publishes_after_success_only(self):
        """완료 기준 3·4·7·21: 첫 폴(시작) in_progress → 다음 폴 = max(t0 + 40, 앞 폴 + 60) success → 그 뒤에만 공개 GET(gzip · 쿼리 없음 ·
        Authorization 0) → md5 = 작업본 → live_ok(커밋 · 공개 md5) · `기록 머리: 배포 완료` exit 0. 무인증 2 · 쓰기 0 · 자격 증명 호출 0."""
        extra = {"runs_head": [[T + 50, runs(run_obj())], [None, runs(run_obj("completed", "success", updated=T + 45))]],
                 "public": [[None, {"status": 200, "body": "work", "checked": T + 55}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 0, out + err)
        self.assertIn(f"기록 머리: 배포 완료 `{COMMIT[:7]}`", out)
        self.assertEqual(out.count("배포 완료"), 1)                                     # 기록 머리 줄 하나에서만
        self.assertRegex(out, r"기록 줄: 저장소 반영\(커밋\) c0ffee1 \d\d:\d\d · 공개 사이트 반영 \d\d:\d\d\(커밋 뒤 \d+초 · Pages #160\)")
        self.assertEqual([q["t"] - T for q in self.polls(reqs)], [0, 60])
        self.assertEqual(len(self.api_gets(reqs)), 2)                                   # 정상 무인증 ≤ 2
        self.assertEqual(self.api_gets(reqs, auth=True), [])
        site = self.site_reqs(reqs)
        self.assertTrue(site and all(q["t"] >= T + 60 and q["auth"] is None and q["enc"] == "gzip" and q["url"] == SITE for q in site), site)
        self.assertEqual([q for q in reqs if q["method"] != "GET"], [])
        self.assertEqual(self.live_ok(), f"commit {COMMIT}\npublic_md5 {hashlib.md5(WORK).hexdigest()}\nat {iso(T + 60)}\n")
        self.assertEqual(self.helper_count(), 0)

    def test_live_already_success_one_poll_and_override_path(self):
        """R1 꼴: 첫 폴에 이미 success → 공개 GET 1 → exit 0. 리허설·시험 전용 SAERO_LIVE_OK 덮어쓰기 — 첫 줄에 그 경로, 작업본 옆엔 쓰지 않는다."""
        extra = {"runs_head": [[None, runs(run_obj("completed", "success", created=T - 300, updated=T - 260))]],
                 "public": [[None, {"status": 200, "body": "work", "checked": T - 100}]]}
        alt = os.path.join(self.td, "scratch_live_ok")
        rc, out, err, reqs = self.live(extra, env_extra={"SAERO_LIVE_OK": alt})
        self.assertEqual(rc, 0, out + err)
        self.assertEqual(out.splitlines()[0], f"live_ok 자리: {alt}(덮어쓰기 SAERO_LIVE_OK — 리허설·시험 전용, 운영 회차 금지)")
        self.assertEqual((len(self.polls(reqs)), len(self.api_gets(reqs)), len(self.site_reqs(reqs))), (1, 1, 1))
        self.assertTrue(os.path.exists(alt))
        self.assertIsNone(self.live_ok())

    def test_live_argument_errors_before_network(self):
        """완료 기준 2·3: --commit 40자만 · md5(--file·--prev) = 도장 1·2행 · 둘이 다름 — 아니면 네트워크 전 exit 2(요청 0) · 시작 때 옛 live_ok 를 지운다."""
        okp = os.path.join(self.td, "live_ok")
        for argv, want in ((["live", "--file", self.work, "--prev", self.prev, "--commit", COMMIT[:7]], "[FAIL] --commit 은 커밋 sha 40자만"),
                           (["live", "--file", self.work, "--commit", COMMIT], "에는 --file work/index.html --prev work/prev.html --commit"),
                           (["live", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--confirm"], "[FAIL] live 는 읽기만"),
                           (["live", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--seen", "abc"], "[FAIL] --seen 은 md5 32자"),
                           (["live", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--since", "어제"], "[FAIL] --since 는 ISO 시각"),
                           (["redeploy", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--since", iso(T)], "[FAIL] --since·--seen 은 live 에만"),
                           (["redeploy", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--confirm", "--dry-run"], "기본 dry-run"),
                           (["push", "--file", self.work, "--base", self.prev, "--message", "m", "--commit", COMMIT], "[FAIL] --commit는 live·redeploy 에만"),
                           (["verify", "--file", self.work, "--confirm"], "[FAIL] --confirm 은 redeploy 에만"),
                           (["redeploy", "--file", self.prev, "--prev", self.work, "--commit", COMMIT], "precheck 도장 1·2행이 아님"),
                           (["live", "--file", self.prev, "--prev", self.work, "--commit", COMMIT], "precheck 도장 1·2행이 아님")):       # 인자 뒤바뀜(마지막)
            with open(okp, "w", encoding="utf-8") as f:
                f.write("commit x\n")
            rc, out, err, reqs = self.run_deploy(argv)
            self.assertEqual(rc, 2, (argv, out + err))
            self.assertIn(want, out, argv)
            self.assertEqual(reqs, [], argv)
        self.assertFalse(os.path.exists(okp))                                           # 마지막 live 꼴(뒤바뀜)은 도장 검사 전에 옛 live_ok 를 지움
        same = os.path.join(self.td, "same.html")                                        # --prev = 작업본과 같은 바이트(도장도 그렇게)
        with open(same, "wb") as f:
            f.write(WORK)
        self.write_stamp(work=WORK, prev=WORK)
        rc, out, err, reqs = self.run_deploy(["live", "--file", self.work, "--prev", same, "--commit", COMMIT])
        self.assertEqual((rc, reqs), (2, []), out)
        self.assertIn("[FAIL] --file md5 = --prev md5", out)
        os.remove(self.stamp)
        rc, out, err, reqs = self.run_deploy(["live", "--file", self.work, "--prev", self.prev, "--commit", COMMIT])
        self.assertEqual((rc, reqs), (2, []), out)
        self.assertIn("도장 없음", out)

    def test_live_stuck_run_reports_and_asks_redeploy_question(self):
        """완료 기준 5·7·8·21(#158 꼴 — api_probe.out 값): queued 그대로 → 폴 ≤ 5(60초 이상 간격) → cap 에 공개 GET 1회 → 상태 읽기 ≤ 6 →
        [멈춤] 실행 번호·status·잡·배포 상태·멈춘 분·그 밖 미완료 실행·GitHub 상태 + 결정 4 문구 · --confirm 없는 redeploy 줄 · 기록 머리 exit 1."""
        q = run_obj("queued", created=T - 10, num=158, rid=38093661514)
        extra = {"runs_head": [[None, runs(q)]],
                 "jobs": [200, {"total_count": 0, "jobs": []}],
                 "jobs_all": [200, {"total_count": 3, "jobs": [
                     {"name": "build", "status": "completed", "conclusion": "success", "run_attempt": 1},
                     {"name": "report-build-status", "status": "completed", "conclusion": "success", "run_attempt": 1},
                     {"name": "deploy", "status": "completed", "conclusion": "cancelled", "run_attempt": 1}]}],
                 "deployments": [200, [{"id": 6988093133, "sha": COMMIT}]],
                 "statuses": [200, [{"state": "waiting", "created_at": iso(T - 9)}]],
                 "runs_all": runs(q, run_obj("queued", num=157, sha=OTHERC, rid=222)),
                 "public": [[None, {"status": 200, "body": "prev", "checked": T - 100}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[멈춤] Pages 실행 #158 · status queued · 잡 0개(최근 시도) — 이전 시도 build completed success(시도 1) · "
                      "report-build-status completed success(시도 1) · deploy completed cancelled(시도 1)", out)
        self.assertRegex(out, r"배포 상태 waiting\(\d\d:\d\d 부터 \d+분\)")
        self.assertIn("그 밖 미완료 실행 #157(0dd0003 queued) · GitHub 상태 Pages operational · Actions operational", out)
        self.assertIn("재배포 질문(사용자에게 이 문구 그대로): 멈춘 실행 #158 — Actions 화면에서 'Cancel workflow' 가 보이면 먼저 눌러 보세요(사람). "
                      "그다음 '재배포' 라고 답하면 1번만 새 배포를 일으킵니다.", out)
        self.assertIn(f"deploy.py redeploy --file {self.work} --prev {self.prev} --commit {COMMIT}", out)
        self.assertNotIn("--confirm", out)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(GitHub 쪽 대기)", out)
        self.assertIn("· 재배포 0/1", out)
        self.assertNotIn("배포 완료", out)
        self.assertIsNone(self.live_ok())
        polls = self.polls(reqs)
        self.assertLessEqual(len(polls), 5)
        self.assertTrue(all(b["t"] - a["t"] >= 60 for a, b in zip(polls, polls[1:])))
        self.assertLessEqual(len(self.api_gets(reqs)) - len(polls), 6)
        site = self.site_reqs(reqs)
        self.assertEqual(len(site), 1)
        self.assertGreaterEqual(site[0]["t"], T - 10 + 300)                             # cap 뒤에만 · 그 앞 공개 GET 0
        self.assertLess(site[0]["t"], min(q["t"] for q in self.api_gets(reqs) if "/jobs" in q["url"]) + 1)   # 공개 GET → 상태 읽기 순
        self.assertEqual([q for q in reqs if q["method"] != "GET"], [])

    def test_live_unreadable_state_still_gives_redeploy_question(self):
        """완료 기준 5·7: 무인증 한도(403)·자격 증명 없음 → 'GitHub 상태 못 읽음(<사유>)' · 그래도 재배포 안내 그대로 · 무인증 ≤ 폴 5 + 상태 6."""
        extra = {"unauth_limit": 0, "public": [[None, {"status": 200, "body": "prev", "checked": T - 100}]]}
        rc, out, err, reqs = self.live(extra, helper=False)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[멈춤] GitHub 상태 못 읽음(무인증 403 — 리셋 ", out)
        self.assertIn("자격 증명 못 얻음(출처: git)", out)
        self.assertIn("재배포 질문(사용자에게 이 문구 그대로): 멈춘 실행 없음(Pages 실행이 안 생김) — Actions 화면에서 'Cancel workflow'", out)
        self.assertIn("deploy.py redeploy --file", out)
        self.assertLessEqual(len(self.polls(reqs)), 5)
        self.assertLessEqual(len(self.api_gets(reqs)), 5 + 6)
        self.assertEqual(self.helper_count(), 0)                                         # 도우미 없음 — 불렸어도 값 0(설정에 도우미 없음)

    def test_live_unauth_limit_uses_credential_once(self):
        """완료 기준 7·3: 무인증 403 → 자격 증명 1회(credential() 한 번) → 그 뒤는 인증 · github.io 요청엔 Authorization 0."""
        extra = {"unauth_limit": 0, "runs_head": [[None, runs(run_obj("completed", "success", created=T - 300, updated=T - 260))]],
                 "public": [[None, {"status": 200, "body": "work", "checked": T - 100}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("무인증 API 제한(403) → 자격 증명으로 다시 읽음(출처: git)", out)
        self.assertEqual(self.helper_count(), 1)
        self.assertEqual(len(self.api_gets(reqs, auth=True)), 1)
        self.assertTrue(all(q["auth"] is None for q in self.site_reqs(reqs)))

    def test_live_no_run_and_redeploy_commit_waits(self):
        """완료 기준 5·10: 이 커밋 실행이 시작 뒤 60초가 지나도 없음 → [멈춤] Pages 실행 없음 exit 1(재배포 질문) · --commit 이 재배포 커밋
        (메시지 redeploy_message 접두)이면 재배포 질문 대신 `GitHub 쪽 대기 — 기다림(재배포 1/1)`(실행이 있어도 없어도)."""
        cm = {"sha": COMMIT, "tree": {"sha": TREE}, "message": "리포트 갱신: 시험", "parents": [{"sha": OTHERC}], "committer": {"date": iso(T - 20)}}
        extra = {"commits": {COMMIT: cm}, "public": [[None, {"status": 200, "body": "prev", "checked": T - 100}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[멈춤] Pages 실행 없음 — live 시작 뒤 60초가 지나도 'pages build and deployment' 실행이 안 생김", out)
        self.assertIn("재배포 질문(사용자에게 이 문구 그대로): 멈춘 실행 없음(Pages 실행이 안 생김)", out)
        self.assertEqual([q["t"] - T for q in self.polls(reqs)], [0, 60])
        self.assertEqual([q["t"] - T for q in self.site_reqs(reqs)], [60])               # [멈춤] 전 공개 GET 1회(완료 기준 20 — 실행이 없어도)
        self.assertRegex(out, r"기록 줄: 저장소 반영\(커밋\) c0ffee1 \d\d:\d\d · 공개 미반영 — GitHub 쪽 대기\(Pages 실행 없음\) · 재배포 0/1")
        extra["commits"] = {COMMIT: dict(cm, message="Pages 재배포 — 504ea88 실행 #158 queued")}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("GitHub 쪽 대기 — 기다림(재배포 1/1)", out)
        self.assertNotIn("재배포 질문(", out)
        self.assertNotIn("deploy.py redeploy", out)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(GitHub 쪽 대기 — 기다림)", out)
        rc, out, err, reqs = self.live(dict(extra, public=[[None, {"status": 200, "body": "work", "checked": T}]], head=OTHERC))
        self.assertEqual(rc, 0, out + err)                                               # 실행이 없거나 사라져도 공개가 작업본이면 exit 0(R2 기대)
        self.assertIn("(다른 실행이 올림 — HEAD 0dd0003)", out)
        q = run_obj("queued", created=T - 10, num=161, msg="Pages 재배포 — 504ea88 실행 #158 queued")   # 재배포 커밋의 실행이 멈춤
        rc, out, err, reqs = self.live({"runs_head": [[None, runs(q)]], "public": [[None, {"status": 200, "body": "prev", "checked": T}]]})
        self.assertEqual(rc, 1, out + err)
        self.assertIn("GitHub 쪽 대기 — 기다림(재배포 1/1)", out)
        self.assertNotIn("deploy.py redeploy", out)
        self.assertNotIn("배포 완료", out)

    def test_live_since_ignores_older_run(self):
        """완료 기준 25(C-6): --since 가 있으면 created_at ≥ since − 5초인 실행만 — 옛 실행을 잡아 5분을 건너뛰지 않는다 · t0 = max(created, since)."""
        old_run = run_obj("completed", "success", created=T - 600, updated=T - 560, num=158, rid=1)
        new_run = run_obj("completed", "success", created=T + 20, updated=T + 55, num=161, rid=2)
        extra = {"runs_head": [[T + 30, runs(old_run)], [None, runs(new_run, old_run)]],
                 "public": [[None, {"status": 200, "body": "work", "checked": T + 58}]]}
        rc, out, err, reqs = self.live(extra, more=["--since", iso(T - 2)])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("[폴 1]", out)
        self.assertIn("이 커밋 Pages 실행 아직 없음", out)
        self.assertIn("Pages #161)", out)
        self.assertEqual([q["t"] - T for q in self.polls(reqs)], [0, 60])
        rc, out, err, reqs = self.live({"runs_head": [[None, runs(old_run)]]}, more=["--since", iso(T - 2)])
        self.assertEqual(rc, 1, out + err)                                               # since 뒤 60초가 지나도 새 실행 없음
        self.assertIn("[멈춤] Pages 실행 없음 — --since 뒤 60초", out)

    def test_live_cdn_wait_then_published_and_exit3(self):
        """완료 기준 6·19: 실행 success · 공개 = 직전 배포본 · CDN 확인(Date − Age) < 실행 완료 → CDN 대기(interval_s) → 풀리면 exit 0 /
        상한 max(t0 + 660, 완료 + 630)까지 옛 판이면 exit 3 `공개 미반영(CDN 캐시)`(재배포 권하지 않음) / 상한이 한 번 실행 570초 밖이면 exit 3 '같은 명령 한 번 더'."""
        done = run_obj("completed", "success", created=T - 400, updated=T - 300)
        extra = {"runs_head": [[None, runs(done)]],
                 "public": [[T + 100, {"status": 200, "body": "prev", "checked": T - 350}], [None, {"status": 200, "body": "work", "checked": T + 100}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("CDN 대기", out)
        site = self.site_reqs(reqs)
        self.assertTrue(len(site) > 2 and all(b["t"] - a["t"] == 15 for a, b in zip(site, site[1:])), [q["t"] - T for q in site])
        extra["public"] = [[None, {"status": 200, "body": "prev", "checked": T - 350}]]
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 3, out + err)
        self.assertIn("CDN 상한", out)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(CDN 캐시)", out)
        for word in ("재배포 질문", "deploy.py redeploy", "배포 완료"):
            self.assertNotIn(word, out)
        self.assertLessEqual(self.site_reqs(reqs)[-1]["t"], T + 330)                     # max(T-400+660, T-300+630)
        self.assertIsNone(self.live_ok())
        extra["runs_head"] = [[None, runs(run_obj("completed", "success", created=T - 10, updated=T - 2))]]   # 상한 T+650 > 시작 + 570
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 3, out + err)
        self.assertIn("한 번 실행 상한 570초", out)
        self.assertIn("같은 live 명령 한 번 더", out)
        self.assertIn("공개 미반영(CDN 캐시)", out)
        self.assertLessEqual(max(q["t"] for q in reqs) - T, 570)

    def test_live_old_page_after_completion(self):
        """완료 기준 18(A-6·A-7)·27: md5 = 작업본이면 Date − Age 와 무관하게 exit 0 · 완료 뒤 확인된 옛 판은 두 번 더 본 뒤 [멈춤](프록시 캐시일 수 있음) ·
        '작업본도 prev 도 아님' [FAIL] 은 완료 뒤 확인 객체에만(완료 전이면 CDN 대기) · --seen md5 는 옛 판으로 인정."""
        extra = {"runs_head": [[None, runs(run_obj("completed", "success", created=T - 60, updated=T - 20))]],
                 "public": [[None, {"status": 200, "body": "prev", "checked": T - 10}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("GitHub 프록시 캐시일 수 있음", out)
        self.assertEqual(len(self.site_reqs(reqs)), 3)
        self.assertIn("재배포 질문", out)
        extra["public"] = [[None, {"status": 200, "body": "other", "checked": T - 10}]]
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("가 작업본도 직전 배포본도 아님(실행 완료 뒤 확인된 객체 · 3번 같음) — 다른 배포가 겹쳤을 수 있다. 재배포 묻지 않음", out)
        self.assertNotIn("재배포 질문(", out)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(확인 못 함)", out)
        rc, out, err, reqs = self.live(extra, more=["--seen", hashlib.md5(OTHER).hexdigest()])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("GitHub 프록시 캐시일 수 있음", out)
        self.assertNotIn("[FAIL]", out)
        extra["runs_head"] = [[None, runs(run_obj("completed", "success", created=T - 400, updated=T - 300))]]
        extra["public"] = [[None, {"status": 200, "body": "other", "checked": T - 350}]]
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 3, out + err)                                               # 완료 전 확인 객체 — CDN 대기
        self.assertNotIn("[FAIL]", out)
        extra["public"] = [[None, {"status": 200, "body": "work", "checked": T - 350}]]
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 0, out + err)

    def test_live_cap_public_already_work(self):
        """완료 기준 20(A-9·C-7 — R2 꼴): 이 커밋 실행이 멈춰도 cap 의 공개 GET 1회가 작업본이면 exit 0 '다른 실행이 올림 — HEAD <sha7>' + live_ok."""
        q = run_obj("queued", created=T - 400, num=158)                                  # t0 + cap 이 이미 지남
        extra = {"runs_head": [[None, runs(q)]], "head": OTHERC, "public": [[None, {"status": 200, "body": "work", "checked": T - 50}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 0, out + err)
        self.assertRegex(out, r"공개 사이트 반영 \d\d:\d\d\(다른 실행이 올림 — HEAD 0dd0003\)")
        self.assertIn("기록 머리: 배포 완료 `c0ffee1`", out)
        self.assertEqual((len(self.polls(reqs)), len(self.site_reqs(reqs)), len(self.api_gets(reqs))), (1, 1, 2))
        self.assertIsNotNone(self.live_ok())

    def test_live_site_errors_never_use_credentials(self):
        """완료 기준 3·28(C-10): 공개 GET 은 한 함수 — 403·429·5xx 에도 credential() 호출 0 · Authorization 0 · 잇달아 3번 실패면 '확인 못 함' exit 1."""
        for st in (403, 429, 500):
            extra = {"runs_head": [[None, runs(run_obj("completed", "success", created=T - 300, updated=T - 260))]],
                     "public": [[None, {"status": st}]]}
            rc, out, err, reqs = self.live(extra)
            self.assertEqual(rc, 1, out + err)
            self.assertIn(f"[FAIL] 공개 사이트 확인 못 함(HTTP {st})", out)
            self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(확인 못 함)", out)
            self.assertEqual(len(self.site_reqs(reqs)), 3)
            self.assertEqual(self.helper_count(), 0, st)
            self.assertTrue(all(q["auth"] is None for q in self.site_reqs(reqs)))
            self.assertNotIn("배포 완료", out)

    def rd_scen(self, **kw):
        sc = {"head": COMMIT,
              "commits": {COMMIT: {"sha": COMMIT, "tree": {"sha": TREE}, "message": "리포트 갱신: 2026.08.26 — 10.10 (46일)", "parents": [{"sha": OTHERC}]},
                          OTHERC: {"sha": OTHERC, "tree": {"sha": TREE}, "message": "리포트 갱신: 다른 회차", "parents": [{"sha": COMMIT}]}},
              "runs_head": [[None, runs(run_obj("queued", created=T - 900, updated=T - 600, num=158))]],
              "public": [[None, {"status": 200, "body": "prev", "checked": T - 700}]],
              "post_commit": [201, {"sha": NEWC, "tree": {"sha": TREE}, "parents": [{"sha": COMMIT}]}],
              "patch_ref": [200, {"ref": "refs/heads/main", "object": {"sha": NEWC, "type": "commit"}}]}
        sc.update(kw)
        return sc

    def writes(self, reqs):
        return [q for q in reqs if q["method"] != "GET"]

    def test_redeploy_default_dry_run_reads_all_writes_nothing(self):
        """완료 기준 8·9: 기본 dry-run(쓰기 0) — 도장 → (e) 자격 증명·권한 → (b) 공개 → (a) 인증 GET HEAD = --commit → (d) → (c) → 쓰기 요약
        (POST tree = HEAD tree · parents = [HEAD] · PATCH force:false). 어떤 출력에도 --confirm 없음."""
        rc, out, err, reqs = self.redeploy(self.rd_scen())
        self.assertEqual(rc, 0, out + err)
        self.assertIn("redeploy dry-run(기본 — 쓰기 0)", out)
        marks = ["(e) 자격 증명 확인됨(출처: git)", "permissions.push): 참", "(b) 공개 md5", "(a) 배포 저장소 HEAD c0ffee1 = --commit(인증 GET)",
                 "(d) HEAD c0ffee1 메시지 '리포트 갱신", "(c) Pages 실행 #158 queued", "쓰기 요약:", "[dry-run] 쓰기 0"]
        pos = [out.index(m) for m in marks]
        self.assertEqual(pos, sorted(pos))
        self.assertIn(f"쓰기 요약: POST /git/commits {{message: 'Pages 재배포 — c0ffee1 실행 #158 queued', tree: {TREE[:7]}, parents: [c0ffee1]}} → "
                      "PATCH /git/refs/heads/main {sha: <새 커밋>, force: false}", out)
        self.assertEqual(self.writes(reqs), [])
        self.assertNotIn("--confirm", out)
        self.assertNotIn("배포 완료", out)
        self.assertEqual(self.helper_count(), 1)
        self.assertTrue(all(q["auth"] for q in reqs if q["url"].startswith("https://api.github.com/")))   # (a)·(d)·(c) 인증 읽기
        self.assertTrue(all(q["auth"] is None for q in self.site_reqs(reqs)))

    def test_redeploy_dry_run_goes_on_after_stop(self):
        """완료 기준 8·10(R3 꼴): 공개 = 작업본 · HEAD 메시지가 재배포 접두 → (b) 이미 반영됨 → (a) → (d) 이미 재배포함 → (c) → 쓰기 요약 →
        끝 줄 '실제였다면 (b)에서 멈춤 — 쓰기 0', exit = 첫 멈춤(0) · HEAD ≠ --commit 이면 첫 멈춤 (a) exit 1 · 자격 증명 없으면 (e)."""
        sc = self.rd_scen(public=[[None, {"status": 200, "body": "work", "checked": T - 700}]])
        sc["commits"][COMMIT]["message"] = "Pages 재배포 — #158 대기열 멈춤"
        rc, out, err, reqs = self.redeploy(sc)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("(b) 공개 사이트 = 작업본(md5", out)
        self.assertIn("이미 반영됨 · 쓰기 0", out)
        self.assertIn("(a) 배포 저장소 HEAD c0ffee1 = --commit", out)
        self.assertIn("[FAIL] 이미 재배포함 — 두 번째 없음 · 쓰기 0", out)
        self.assertIn("(c) Pages 실행 #158", out)
        self.assertIn("쓰기 요약:", out)
        self.assertEqual(out.rstrip().splitlines()[-1], "[dry-run] 실제였다면 (b)에서 멈춤 — 쓰기 0")
        self.assertEqual(self.writes(reqs), [])
        rc, out, err, reqs = self.redeploy(self.rd_scen(head=OTHERC))
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] (a) 배포 저장소 HEAD 0dd0003 ≠ --commit c0ffee1 — 다른 배포가 겹쳤거나 이미 재배포함 · 쓰기 0", out)
        self.assertEqual(out.rstrip().splitlines()[-1], "[dry-run] 실제였다면 (a)에서 멈춤 — 쓰기 0")
        rc, out, err, reqs = self.redeploy(self.rd_scen(), helper=False)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] (e) 자격 증명을 얻지 못함(출처: git)", out)
        self.assertIn("(a)·(d)·(c) 자격 증명 없음 — 인증 읽기 못 함", out)
        self.assertEqual(out.rstrip().splitlines()[-1], "[dry-run] 실제였다면 (e)에서 멈춤 — 쓰기 0")
        self.assertEqual([q["url"] for q in reqs], [SITE])                                # 공개 GET 1 뿐 — API 0
        self.assertEqual(self.writes(reqs), [])

    def test_redeploy_confirm_one_post_one_patch(self):
        """완료 기준 11·12·28: 실제(--confirm) = POST 1(tree = HEAD tree · parents = [HEAD]) + PATCH 1(force:false) · '재배포 요청 보냄'(배포 완료 0) ·
        다음(읽기) live --commit <새 HEAD> --since <쓰기 시각>."""
        rc, out, err, reqs = self.redeploy(self.rd_scen(), more=["--confirm"])
        self.assertEqual(rc, 0, out + err)
        posts = [q for q in reqs if q["method"] == "POST"]
        patches = [q for q in reqs if q["method"] == "PATCH"]
        self.assertEqual((len(posts), len(patches)), (1, 1))
        self.assertEqual(posts[0]["body"], {"message": "Pages 재배포 — c0ffee1 실행 #158 queued", "tree": TREE, "parents": [COMMIT]})
        self.assertEqual(patches[0]["body"], {"sha": NEWC, "force": False})
        self.assertEqual(posts[0]["auth"], f"token {FAKE}")
        self.assertIn(f"재배포 요청 보냄 빈 커밋 {NEWC[:7]}", out)
        self.assertIn(f"다음(읽기): deploy.py live --file {self.work} --prev {self.prev} --commit {NEWC} --since {iso(T)}", out)
        self.assertNotIn("배포 완료", out)
        self.assertNotIn("--confirm", out)
        self.assertEqual([q for q in reqs if q["method"] == "PUT"], [])

    def test_redeploy_confirm_stops_write_nothing(self):
        """완료 기준 9·10·11: 실제여도 (e) 자격 증명·권한 / (b) 공개 못 읽음 / (a) HEAD ≠ --commit·못 읽음·꼴 다름 / (d) 이미 재배포함 / (c) 2분 안 움직임·
        못 읽음 이면 첫 멈춤에서 끝 — 쓰기 0 · 기록 머리 'GitHub 쪽 대기 — 기다림'."""
        rd = self.rd_scen()
        rd["commits"][COMMIT]["message"] = "Pages 재배포 — 504ea88 실행 #158 queued"
        cases = [(rd, {}, "[FAIL] 이미 재배포함 — 두 번째 없음 · 쓰기 0", "1/1"),
                 (self.rd_scen(head=OTHERC), {}, "[FAIL] (a) 배포 저장소 HEAD 0dd0003 ≠ --commit c0ffee1", "0/1"),
                 (self.rd_scen(runs_head=[[None, runs(run_obj("in_progress", created=T - 100, updated=T - 30, num=158))]]), {}, "30초 전에 움직임(2분 안) — 쓰기 0", "0/1"),
                 (self.rd_scen(ref=[[None, [500, {"message": "x"}]]]), {}, "[FAIL] (a) 배포 저장소 HEAD 를 읽지 못함", "0/1"),
                 (self.rd_scen(ref=[[None, [200, {"object": {"sha": "zz"}}]]]), {}, "[FAIL] (a) 배포 저장소 HEAD 를 읽지 못함(꼴 다름)", "0/1"),
                 (self.rd_scen(commits={}), {}, "[FAIL] (a) 커밋 c0ffee1 을 읽지 못함", "0/1"),
                 (self.rd_scen(public=[[None, {"status": 503}]]), {}, "[FAIL] (b) 공개 사이트를 읽지 못함(HTTP 503)", "0/1"),
                 (self.rd_scen(runs_head=[[None, [502, {"message": "bad"}]]]), {}, "[FAIL] (c) Pages 실행을 읽지 못함", "0/1"),
                 (self.rd_scen(), {"helper": False}, "[FAIL] (e) 자격 증명을 얻지 못함(출처: git)", "0/1"),
                 (self.rd_scen(), {"repo_auth": (200, {"permissions": {"push": False}})}, "[FAIL] (e) 배포 저장소 쓰기 권한 확인 안 됨", "0/1")]
        for sc, kw, want, count in cases:
            rc, out, err, reqs = self.redeploy(sc, more=["--confirm"], **kw)
            self.assertEqual(rc, 1, (want, out + err))
            self.assertIn(want, out)
            self.assertEqual(self.writes(reqs), [], want)
            self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(GitHub 쪽 대기 — 기다림)", out)
            self.assertIn(f"재배포 {count}", out)
        rc, out, err, reqs = self.redeploy(self.rd_scen(public=[[None, {"status": 200, "body": "work"}]]), more=["--confirm"])
        self.assertEqual(rc, 0, out + err)                                               # (b) 이미 반영됨 — 쓰기 0, live 로
        self.assertEqual(self.writes(reqs), [])
        self.assertIn(f"다음(읽기): deploy.py live --file {self.work} --prev {self.prev} --commit {COMMIT}", out)

    def test_redeploy_result_unknown_never_retries(self):
        """완료 기준 11·24(B-6): POST 결과 모름 → PATCH 0 · ref 그대로 · 1/1 · PATCH 결과 모름 → 재시도 0, 60초 뒤 인증 GET 으로 HEAD =
        새 커밋(반영) / = --commit(안 됨 1/1) / 그 밖(겹침) · PATCH 422 = 쓰기 끝 · POST 응답 꼴 다름 → PATCH 0."""
        rc, out, err, reqs = self.redeploy(self.rd_scen(post_raise=True), more=["--confirm"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("재배포 커밋 만들기(POST) 결과 모름(요청 실패(TimeoutError)) — PATCH 안 보냄 · ref 그대로 · 재시도 0 · 재배포 1/1 로 셈", out)
        self.assertEqual(([q["method"] for q in self.writes(reqs)]), ["POST"])
        for after, rc_want, want in ((NEWC, 0, "PATCH 결과 모름 뒤 다시 읽음: HEAD = 새 커밋"), (COMMIT, 1, "[FAIL] 재배포 안 됨 — 다시 읽은 HEAD = c0ffee1"),
                                     (OTHERC, 1, "[FAIL] 다시 읽은 HEAD 0dd0003 — 다른 배포가 겹침")):
            rc, out, err, reqs = self.redeploy(self.rd_scen(patch_raise=True, ref_after_patch=[200, {"object": {"sha": after}}]), more=["--confirm"])
            self.assertEqual(rc, rc_want, out + err)
            self.assertIn(want, out)
            self.assertEqual([q["method"] for q in self.writes(reqs)], ["POST", "PATCH"])
            patch_t = self.writes(reqs)[1]["t"]
            reread = [q for q in reqs if q["method"] == "GET" and q["url"].endswith("/git/ref/heads/main") and q["t"] > patch_t]
            self.assertEqual(len(reread), 1)
            self.assertGreaterEqual(reread[0]["t"] - patch_t, 60)
            self.assertTrue(reread[0]["auth"])
        rc, out, err, reqs = self.redeploy(self.rd_scen(patch_ref=[422, {"message": "Update is not a fast forward"}]), more=["--confirm"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] ref 이동 거부(PATCH 422", out)
        self.assertEqual([q["method"] for q in self.writes(reqs)], ["POST", "PATCH"])
        rc, out, err, reqs = self.redeploy(self.rd_scen(post_commit=[201, {"sha": NEWC, "tree": {"sha": OTHERC}, "parents": [{"sha": COMMIT}]}]),
                                           more=["--confirm"])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 만든 커밋 꼴이 다름", out)
        self.assertEqual([q["method"] for q in self.writes(reqs)], ["POST"])

    def test_public_uncompressed_one_get_no_api(self):
        """완료 기준 15·28: public = 무압축 GET 1(Accept-Encoding 없음) · API 0 · 자격 증명 0 · 같음 exit 0 / 다름 [주의] exit 1(--seen 값) · '배포 완료' 0."""
        extra = {"public": [[None, {"status": 200, "body": "prev", "checked": T - 30}]]}
        rc, out, err, reqs = self.run_deploy(["public", "--file", self.prev], extra=extra)
        self.assertEqual(rc, 0, out + err)
        self.assertIn(f"공개 md5 {hashlib.md5(PREV).hexdigest()} = {self.prev} md5 → 같음", out)
        self.assertEqual([(q["url"], q["enc"], q["auth"]) for q in reqs], [(SITE, None, None)])
        self.assertIn("CDN 확인", out)
        rc, out, err, reqs = self.run_deploy(["public", "--file", self.work], extra=extra)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[주의] 공개 사이트가 저장소 HEAD 와 다름 — 옛 실행이 덮었을 수 있다", out)
        self.assertIn(f"--seen {hashlib.md5(PREV).hexdigest()}", out)
        self.assertNotIn("배포 완료", out)
        rc, out, err, reqs = self.run_deploy(["public", "--file", self.prev], extra={"public": [[None, {"status": 403}]]})
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[주의] 공개 사이트를 읽지 못함(HTTP 403)", out)
        self.assertEqual(self.helper_count(), 0)
        rc, out, err, reqs = self.run_deploy(["public"])
        self.assertEqual((rc, reqs), (2, []), out)

    def test_verify_ref_match_prints_next_live_commit(self):
        """완료 기준 25(B-7): verify --ref 일치 뒤 deploy.py 가 HEAD·부모를 읽어 다음 live 의 --commit 을 고른다 — HEAD = push 커밋이면 그것 ·
        HEAD 메시지가 재배포 접두이고 부모 = push 커밋이면 HEAD · 아니면 push 커밋. 짧은 ref 는 HEAD 로 40자."""
        refs = {COMMIT: WORK}
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", COMMIT], refs=refs, extra={"head": COMMIT})
        self.assertEqual(rc, 0, out + err)
        self.assertRegex(out, r"다음\(읽기\): deploy\.py live --file .+ --prev .*prev\.html --commit " + COMMIT)
        rdc = {"sha": NEWC, "tree": {"sha": TREE}, "message": "Pages 재배포 — c0ffee1 실행 #158 queued", "parents": [{"sha": COMMIT}]}
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", COMMIT], refs=refs, extra={"head": NEWC, "commits": {NEWC: rdc}})
        self.assertEqual(rc, 0, out + err)
        self.assertIn(f"--commit {NEWC}", out)
        oth = dict(rdc, sha=OTHERC, message="리포트 갱신: 다른 회차")
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", COMMIT], refs=refs, extra={"head": OTHERC, "commits": {OTHERC: oth}})
        self.assertIn(f"--commit {COMMIT}", out)
        rc, out, err, reqs = self.run_deploy(["verify", "--file", self.work, "--ref", COMMIT[:7]], refs={COMMIT[:7]: WORK}, extra={"head": COMMIT})
        self.assertIn(f"--commit {COMMIT}", out)
        self.assertEqual(self.helper_count(), 0)
        self.assertEqual(self.writes(reqs), [])

    def test_live_values_only_in_config(self):
        """완료 기준 13: 공개 주소·GitHub 상태 주소는 config 에만(deploy.py 하드코딩 0) · live·redeploy 함수 숫자 토큰에 live_check 값 없음."""
        import inspect
        import io
        import tokenize
        with open(os.path.join(SCRIPTS, "deploy.py"), encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("github.io", src)
        self.assertNotIn("githubstatus", src)
        sys.path.insert(0, SCRIPTS)
        import deploy
        lc = deploy.LC
        vals = {lc["interval_s"], lc["cap_s"], lc["cdn_max_age_s"], lc["cdn_extra_s"], lc["cdn_floor_s"], lc["run_max_s"], *lc["api_poll_s"]}
        for fn in (deploy.cmd_live, deploy.cmd_redeploy, deploy.cmd_public, deploy.stop_report, deploy.public_get, deploy.pick_run, deploy.Gh,
                   deploy.main_site, deploy.live_commit_after_verify):
            nums = {int(t.string) for t in tokenize.generate_tokens(io.StringIO(inspect.getsource(fn)).readline)
                    if t.type == tokenize.NUMBER and t.string.isdigit()}
            self.assertEqual(sorted(nums & vals), [], fn.__name__)

    def test_live_cap_rereads_run_before_stopping(self):
        """F3(자체 검토): 폴 한도 뒤 cap 에서 마지막 폴이 interval_s 넘게 지났으면 실행 하나를 다른 주소로 1회 다시(상태 한도 안) —
        그 사이 success 면 [멈춤] 대신 공개 GET 경로로 exit 0. 다시 읽기 실패·여전히 미완료면 기존 [멈춤](상태 읽기 합 ≤ 6)."""
        extra = {"runs_head": [[None, runs(run_obj())]],
                 "run_by_id": [[None, [200, {"id": 111, "status": "completed", "conclusion": "success", "updated_at": iso(T + 250)}]]],
                 "public": [[None, {"status": 200, "body": "work", "checked": T + 260}]]}
        rc, out, err, reqs = self.live(extra)
        self.assertEqual(rc, 0, out + err)
        self.assertIn("[cap]", out)
        self.assertIn("completed success(다시 읽음)", out)
        self.assertNotIn("[멈춤]", out)
        self.assertRegex(out, r"공개 사이트 반영 \d\d:\d\d\(커밋 뒤 \d+초 · Pages #160\)")
        self.assertEqual(len(self.polls(reqs)), 5)
        self.assertEqual(len(self.api_gets(reqs)) - 5, 1)

    def test_live_ok_write_failure_never_says_deployed(self):
        """완료 기준 1(자체 검토 F1): live_ok 를 못 쓰면 exit 1 — 출력 어디에도 '배포 완료' 부분 문자열 0 · 기록 머리 '공개 미반영(확인 못 함)'."""
        extra = {"runs_head": [[None, runs(run_obj("completed", "success", created=T - 300, updated=T - 260))]],
                 "public": [[None, {"status": 200, "body": "work", "checked": T - 100}]]}
        bad = os.path.join(self.td, "없는폴더", "live_ok")
        rc, out, err, reqs = self.live(extra, env_extra={"SAERO_LIVE_OK": bad})
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] live_ok 를 쓰지 못함", out)
        self.assertNotIn("배포 완료", out + err)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(확인 못 함)", out)

    def test_live_after_redeploy_never_asks_again(self):
        """완료 기준 10·12: --since(redeploy 가 찍은 값)가 있는 live 는 재배포 뒤 — 멈춰도 질문 대신 'GitHub 쪽 대기 — 기다림(재배포 1/1)' ·
        CDN exit 3 도 머리에 '기다림'·줄에 '재배포 1/1'."""
        q = run_obj("queued", created=T + 1, num=161)
        rc, out, err, reqs = self.live({"runs_head": [[None, runs(q)]], "public": [[None, {"status": 200, "body": "prev", "checked": T}]]},
                                       more=["--since", iso(T - 2)])
        self.assertEqual(rc, 1, out + err)
        self.assertIn("GitHub 쪽 대기 — 기다림(재배포 1/1)", out)
        self.assertNotIn("재배포 질문(", out)
        self.assertNotIn("deploy.py redeploy", out)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(GitHub 쪽 대기 — 기다림)", out)
        done = run_obj("completed", "success", created=T - 400, updated=T - 300)
        rc, out, err, reqs = self.live({"runs_head": [[None, runs(done)]], "public": [[None, {"status": 200, "body": "prev", "checked": T - 350}]]},
                                       more=["--since", iso(T - 405)])
        self.assertEqual(rc, 3, out + err)
        self.assertIn("기록 머리: 저장소 반영 `c0ffee1` · 공개 미반영(CDN 캐시 — 기다림)", out)
        self.assertIn("· 재배포 1/1", out)
        self.assertNotIn("배포 완료", out)

    def test_abbreviated_flags_rejected(self):
        """자체 검토 F4: 줄인 플래그(--con)가 --confirm 으로 먹히지 않는다 — argparse 오류 exit 2 · 요청 0."""
        for argv in (["redeploy", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--con"],
                     ["redeploy", "--file", self.work, "--prev", self.prev, "--commit", COMMIT, "--conf"]):
            rc, out, err, reqs = self.redeploy(self.rd_scen(), more=argv[7:])
            self.assertEqual((rc, reqs), (2, []), out + err)


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1)
    sys.exit(0 if r.result.wasSuccessful() else 1)
