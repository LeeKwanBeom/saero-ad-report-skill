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
"""
import base64
import hashlib
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
import base64, hashlib, io, json, os, sys, urllib.error, urllib.request
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
    rec = {"method": m, "url": url, "auth": auth}
    if m == "PUT":  # 실제로 보낸 본문의 md5(도장과 같은 바이트인지)
        rec["body_md5"] = hashlib.md5(base64.b64decode(json.loads(req.data)["content"])).hexdigest()
    with open(os.environ["T_LOG"], "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    if m == "GET" and url.endswith("/contents/index.html"):
        if scen.get("edit_on_get"):  # GET을 기다리는 사이 작업본이 바뀌는 경우 흉내(편집기 저장·다른 세션)
            with open(scen["edit_on_get"], "wb") as f:
                f.write(b"<html>edited AFTER precheck</html>\n")
        status, body = 200, {"sha": "sha0prev", "content": scen["content_b64"]}
    elif m == "GET" and url.endswith("/repos/" + scen["repo"]):
        status, body = scen["repo_auth"] if auth else [200, {"name": "x"}]
    elif m == "PUT":
        if scen.get("put_raise"):  # PUT 도중 끊김(응답 못 받음) 흉내 — 서버가 받았는지 모른다
            raise TimeoutError("timed out")
        status, body = scen.get("put") or [200, {"commit": {"sha": "c0ffee1234"}, "content": {"sha": "f11e5ha000"}}]
        if isinstance(body.get("message"), str):  # 서버·프록시가 요청 헤더를 되돌려 주는 경우 흉내
            body = dict(body, message=body["message"].replace("{AUTH}", auth or ""))
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
        self.stamp = p("precheck_ok.md5")                                    # precheck.sh가 전부 통과하면 쓰는 도장(작업본·직전 배포본 md5·모드)
        self.write_stamp()

    def write_stamp(self, work=WORK, prev=PREV, mode="full"):
        with open(self.stamp, "w", encoding="utf-8") as f:
            f.write(f"{hashlib.md5(work).hexdigest()}  work.html\n{hashlib.md5(prev).hexdigest()}  prev.html\nmode {mode}\n")

    def tearDown(self):
        shutil.rmtree(self.td)

    def run_deploy(self, argv, repo_auth=(200, {"permissions": {"admin": True, "push": True, "pull": True}}),
                   deployed=PREV, helper=True, put=None, edit_on_get=None, put_raise=False):
        sys.path.insert(0, SCRIPTS)
        from reportlib import load_config
        with open(self.scen, "w", encoding="utf-8") as f:
            json.dump({"content_b64": base64.b64encode(deployed).decode(), "repo": load_config()["deploy_repo"],
                       "repo_auth": list(repo_auth), "put": list(put) if put else None, "edit_on_get": edit_on_get, "put_raise": put_raise}, f)
        if os.path.exists(self.log):
            os.remove(self.log)
        env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "PYTHONUTF8"))}   # 호출 환경의 GIT_DIR 등 전부 제거
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=self.cfg_helper if helper else self.cfg_none,
                   GIT_CEILING_DIRECTORIES=os.path.dirname(self.td),
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
        self.assertIn("배포 완료 커밋 c0ffee1", out)
        puts = [q for q in reqs if q["method"] == "PUT"]
        self.assertEqual(len(puts), 1)
        self.assertEqual(puts[0]["auth"], f"token {FAKE}")

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
