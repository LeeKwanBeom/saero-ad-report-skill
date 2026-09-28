#!/usr/bin/env python3
"""scripts/deploy.py 오프라인 검사 — 가짜 GitHub API + 가짜 git 자격 증명 도우미(네트워크 0, 이 PC 실제 자격 증명 0).

실행: "$PY" tests/test_deploy.py   (unittest, 저장소 루트에서 Git Bash. git이 필요 — 없으면 skip)
격리: deploy.py를 자식 파이썬으로 돌린다. 자식 환경은 GIT_CONFIG_NOSYSTEM=1 · GIT_CONFIG_GLOBAL=<임시 설정 — 가짜 도우미만>이라
      `git credential fill`이 이 PC의 자격 증명 관리자(GCM)에 닿지 않는다. urllib.request.urlopen은 가짜로 바꿔 끼워
      요청(메서드·URL·Authorization)을 임시 파일에 적고 시나리오 응답을 돌려준다(api.github.com 요청 0).
검사(2026-09-28 수정 회차 2 N4):
  1 가짜 자격 증명 값이 stdout·stderr에 0건 — 값은 Authorization 헤더에만 간다(헤더에 실제로 실렸는지도 확인해 빈 시험이 아님을 보인다)
  2 dry-run이면 PUT 0(--file 있음·없음) · 3 --base 불일치 → [FAIL] exit 1·PUT 0, 일치 → PUT 1, 실제 push에 --base 없음 → exit 2·요청 0
  4 permissions.push 거짓 → [FAIL] exit 1, 권한 조회 401 → [FAIL] exit 1 · 5 도우미 없음 → [FAIL] 자격 증명을 얻지 못함(출처: git)
  6 token_of: 없는 파일 → None(Traceback 없음) · UTF-16LE·BE(BOM) · UTF-8 BOM · 깨진 바이트
"""
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
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

RUNNER = r'''
import io, json, os, sys, urllib.error, urllib.request
sys.path.insert(0, os.environ["T_SCRIPTS"])
scen = json.load(open(os.environ["T_SCEN"], encoding="utf-8"))

class Resp:
    def __init__(self, status, body):
        self.status, self._b = status, json.dumps(body).encode()
    def read(self):
        return self._b
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False

def fake_urlopen(req, timeout=None):
    m, url, auth = req.get_method(), req.full_url, req.get_header("Authorization")
    with open(os.environ["T_LOG"], "a", encoding="utf-8") as f:
        f.write(json.dumps({"method": m, "url": url, "auth": auth}) + "\n")
    if m == "GET" and url.endswith("/contents/index.html"):
        status, body = 200, {"sha": "sha0prev", "content": scen["content_b64"]}
    elif m == "GET" and url.endswith("/repos/" + scen["repo"]):
        status, body = scen["repo_auth"] if auth else [200, {"name": "x"}]
    elif m == "PUT":
        status, body = 200, {"commit": {"sha": "c0ffee1234"}, "content": {"sha": "f11e5ha000"}}
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
        with open(helper, "w", encoding="utf-8", newline="\n") as f:
            f.write(f'#!/bin/sh\n[ "$1" = get ] || exit 0\necho username=fakeuser\necho password={FAKE}\n')
        self.cfg_helper, self.cfg_none = p("gitconfig-helper"), p("gitconfig-none")
        with open(self.cfg_helper, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"[credential]\n\thelper = \"!sh '{helper.replace(os.sep, '/')}'\"\n")
        with open(self.cfg_none, "w", encoding="utf-8", newline="\n") as f:
            f.write("[core]\n\tautocrlf = false\n")
        for name, data in (("prev.html", PREV), ("work.html", WORK), ("other.html", OTHER)):
            with open(p(name), "wb") as f:
                f.write(data)
        self.prev, self.work, self.other = p("prev.html"), p("work.html"), p("other.html")

    def tearDown(self):
        shutil.rmtree(self.td)

    def run_deploy(self, argv, repo_auth=(200, {"permissions": {"admin": True, "push": True, "pull": True}}),
                   deployed=PREV, helper=True):
        sys.path.insert(0, SCRIPTS)
        from reportlib import load_config
        with open(self.scen, "w", encoding="utf-8") as f:
            json.dump({"content_b64": base64.b64encode(deployed).decode(), "repo": load_config()["deploy_repo"],
                       "repo_auth": list(repo_auth)}, f)
        if os.path.exists(self.log):
            os.remove(self.log)
        env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_CONFIG", "PYTHONUTF8"))}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=self.cfg_helper if helper else self.cfg_none,
                   T_SCRIPTS=SCRIPTS, T_SCEN=self.scen, T_LOG=self.log, T_ARGV=json.dumps(argv))
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
        self.assertIn("배포 완료 커밋 c0ffee1", out)
        puts = [q for q in reqs if q["method"] == "PUT"]
        self.assertEqual(len(puts), 1)
        self.assertEqual(puts[0]["auth"], f"token {FAKE}")

    def test_no_credential_helper_fails_cleanly(self):
        rc, out, err, reqs = self.run_deploy(["push", "--dry-run"], helper=False)
        self.assertEqual(rc, 1, out + err)
        self.assertIn("[FAIL] 자격 증명을 얻지 못함(출처: git)", out)
        self.assertEqual([q for q in reqs if q["auth"]], [])
        self.assertNotIn("Traceback", err)

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


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1)
    sys.exit(0 if r.result.wasSuccessful() else 1)
