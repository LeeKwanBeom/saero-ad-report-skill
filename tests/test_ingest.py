#!/usr/bin/env python3
"""scripts/ingest.sh 오프라인 검사 — 임시 저장소 + 로컬 bare origin(네트워크 0, 실제 data/·원격 저장소 불변).

실행: $PY tests/test_ingest.py   (unittest, 저장소 루트에서. bash·git이 필요 — 없으면 skip)
검사(2026-09-28 Code 탭 회차 K10):
  1 정상: data/2026-09가 없는 임시 저장소에 9월 4개(data/ 밖 사본, 실제 수집 파일명 `<이름> 보고서,2580077.csv` — 쉼표·공백)
    → store·combine·커밋·push → origin/main == HEAD, 원격 main의 data/2026-09 4개 = 입력 바이트
  2 main 아닌 브랜치 → [FAIL] exit 1, 커밋 0·data/ 변경 0(store 전에 멈춤)
  3 push가 거부되면 [FAIL] push 실패 exit 1, 커밋만 된 상태에서 같은 입력으로 다시 → "data/ 변경 없음" 분기에서도 [FAIL](HEAD ≠ origin/main) — 숨지 않음
  4 data/ 밖에 스테이징된 변경은 'data:' 커밋에 섞이지 않는다
입력은 늘 data/ 밖 사본이다(archive.py store는 같은 경로면 원본을 지운 뒤 복사하다 잃는다 — 그 조건을 쓰지 않는다).
"""
import hashlib
import os
import shutil
import stat
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
DATA = os.path.join(ROOT, "data")
FILES = {"키워드.csv": "필라테스 보고서,2580077.csv", "검색어.csv": "검색어 보고서,2580077.csv",
         "상세지역.csv": "상세지역 보고서,2580077.csv", "시간대별.csv": "시간대별 보고서,2580077.csv"}
BASH = shutil.which("bash") or next((p for p in (r"C:\Program Files\Git\bin\bash.exe",) if os.path.exists(p)), None)
GIT = shutil.which("git")
COPY = ("scripts/ingest.sh", "scripts/archive.py", "scripts/reportlib.py", "config/report-config.json", ".gitattributes", ".gitignore")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def md5f(path):
    with open(path, "rb") as f:
        return md5b(f.read())


def real_md5s():
    return {os.path.relpath(os.path.join(dp, fn), DATA): md5f(os.path.join(dp, fn))
            for dp, _, fns in os.walk(DATA) for fn in fns}


BEFORE = real_md5s()


def _rm_ro(func, path, _exc):  # Windows: git 객체 파일은 읽기 전용
    os.chmod(path, stat.S_IWRITE)
    func(path)


def git(cwd, *args, check=True, raw=False):
    r = subprocess.run([GIT, "-c", "core.quotepath=false", *args], cwd=cwd, capture_output=True,
                       **({} if raw else {"text": True, "encoding": "utf-8"}))
    if check and r.returncode != 0:
        raise AssertionError(f"git {args} → {r.returncode}: {r.stderr}")
    return r.stdout if raw else r.stdout.strip()


@unittest.skipUnless(BASH and GIT, "bash·git 없음")
class IngestTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()
        self.repo = os.path.join(self.td, "repo")
        for rel in COPY:
            dst = os.path.join(self.repo, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(ROOT, rel), dst)
        shutil.copytree(os.path.join(DATA, "2026-08"), os.path.join(self.repo, "data", "2026-08"))
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", "-A")
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "seed")
        self.bare = os.path.join(self.td, "origin.git")
        git(self.td, "clone", "-q", "--bare", self.repo, self.bare)
        git(self.repo, "remote", "add", "origin", self.bare)
        git(self.repo, "fetch", "-q", "origin")
        self.inp = os.path.join(self.td, "in 폴더")                     # 공백·한글 폴더 + 쉼표 파일명(실제 수집 이름)
        os.makedirs(self.inp)
        self.inputs = []
        for src, name in FILES.items():
            p = os.path.join(self.inp, name)
            shutil.copy(os.path.join(DATA, "2026-09", src), p)
            self.inputs.append(p)

    def tearDown(self):
        shutil.rmtree(self.td, onerror=_rm_ro)

    def ingest(self):
        env = {k: v for k, v in os.environ.items() if k != "PYTHONUTF8"}  # ingest.sh가 스스로 PYTHONUTF8=1을 건다
        env["PY"] = sys.executable
        script = os.path.join(self.repo, "scripts", "ingest.sh").replace("\\", "/")
        r = subprocess.run([BASH, script, *[p.replace("\\", "/") for p in self.inputs]], cwd=self.repo, env=env,
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr

    def head(self, ref="HEAD"):
        return git(self.repo, "rev-parse", ref)

    def test_1_normal_push_and_origin_equals_head(self):
        rc, out = self.ingest()
        self.assertEqual(rc, 0, out)
        self.assertIn("[PASS] 합본 검사 통과", out)
        self.assertIn("origin/main = HEAD", out)
        self.assertEqual(self.head(), git(self.bare, "rev-parse", "main"))
        names = git(self.bare, "ls-tree", "-r", "--name-only", "main").splitlines()
        for kind in FILES:
            self.assertIn(f"data/2026-09/{kind}", names)
            got = git(self.bare, "show", f"main:data/2026-09/{kind}", raw=True)
            self.assertEqual(md5b(got), md5f(os.path.join(DATA, "2026-09", kind)), kind)  # 바이트 그대로(-text)
        self.assertTrue(git(self.repo, "log", "-1", "--format=%s").startswith("data: 보관본 갱신"))
        # 같은 입력으로 다시: 변경 없음 + origin/main == HEAD → 통과
        rc2, out2 = self.ingest()
        self.assertEqual(rc2, 0, out2)
        self.assertIn("data/ 변경 없음", out2)

    def test_4_only_data_is_committed(self):
        """data/ 밖에 스테이징된 변경이 있어도 'data:' 커밋에는 data/만 들어간다(다른 스테이징은 그대로 남는다)."""
        with open(os.path.join(self.repo, "config", "report-config.json"), "a", encoding="utf-8") as f:
            f.write(" ")                                              # data/ 밖 변경(JSON은 그대로 유효)
        git(self.repo, "add", "config/report-config.json")
        rc, out = self.ingest()
        self.assertEqual(rc, 0, out)
        changed = git(self.repo, "show", "--name-only", "--format=", "HEAD").splitlines()
        self.assertTrue(changed and all(p.startswith("data/") for p in changed), changed)
        self.assertIn("config/report-config.json", git(self.repo, "diff", "--cached", "--name-only"))

    def test_2_not_main_branch_fails_before_writing(self):
        git(self.repo, "checkout", "-q", "-b", "feat-x")
        before = self.head()
        rc, out = self.ingest()
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] 현재 브랜치가 main이 아님(feat-x)", out)
        self.assertNotIn("== store", out)
        self.assertEqual(self.head(), before)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "data", "2026-09")))
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_3_unpushed_commit_is_not_hidden_by_no_change(self):
        hook = os.path.join(self.bare, "hooks", "pre-receive")
        with open(hook, "w", newline="\n") as f:
            f.write("#!/bin/sh\necho 'rejected by test hook' >&2\nexit 1\n")
        os.chmod(hook, 0o755)
        origin_before = git(self.bare, "rev-parse", "main")
        rc, out = self.ingest()                                       # 커밋은 되고 push는 거부
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] push 실패", out)
        self.assertNotEqual(self.head(), origin_before)
        self.assertEqual(git(self.bare, "rev-parse", "main"), origin_before)
        rc2, out2 = self.ingest()                                     # 같은 입력 → 변경 없음 분기
        self.assertEqual(rc2, 1, out2)
        self.assertIn("data/ 변경 없음", out2)
        self.assertIn("≠ origin/main", out2)
        self.assertEqual(git(self.bare, "rev-parse", "main"), origin_before)


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1)
    same = BEFORE == real_md5s()
    print(f"실제 data/ md5 전/후 동일: {same} ({len(BEFORE)}파일)")
    sys.exit(0 if r.result.wasSuccessful() and same else 1)
