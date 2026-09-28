#!/usr/bin/env python3
"""scripts/ingest.sh 오프라인 검사 — 임시 저장소 + 로컬 bare origin(네트워크 0, 실제 data/·원격 저장소 불변).

실행: $PY tests/test_ingest.py   (unittest, 저장소 루트에서. bash·git이 필요 — 없으면 skip)
검사(2026-09-28 Code 탭 회차 K10 + 수정 회차 2 N4):
  1 정상: data/2026-09가 없는 임시 저장소에 9월 4개(data/ 밖 사본, 실제 수집 파일명 `<이름> 보고서,2580077.csv` — 쉼표·공백)
    → store·combine·커밋·push → origin/main == HEAD, 원격 main의 data/2026-09 4개 = 입력 바이트
  2 main 아닌 브랜치 → [FAIL] exit 1, 커밋 0·data/ 변경 0(store 전에 멈춤)
  3 push가 거부되면 [FAIL] push 실패 exit 1, 커밋만 된 상태에서 같은 입력으로 다시 → 시작 검사에서 [FAIL](HEAD ≠ origin/main) — 숨지 않음
  4 data/ 밖에 스테이징된 변경은 'data:' 커밋에 섞이지 않는다
  5 CRLF 입력 CSV → 원격 blob 바이트 = 입력(.gitattributes `*.csv -text`가 없으면 autocrlf=true가 LF로 바꿔 실패)
  6·7 시작 검사(N3): 원격이 앞서 있음 / stat만 깨끗한 CRLF 작업 파일(i/lf w/crlf) → store 전 [FAIL] exit 1, 쓰기 0
  8 시작 검사(수정 회차 3 W2): data/가 HEAD와 다름 — 스테이징된 CRLF(줄바꿈 검사는 못 잡음)·미스테이징 둘 다 [FAIL], 추적 안 된 파일도 [FAIL]
  git·ingest·precheck 자식 env는 GIT_* 제거 + 시스템·전역 설정 끔(clean_env — 호출 환경의 GIT_DIR 등으로 실제 저장소에 닿지 않게)
  1은 "origin/main = HEAD"를 두 번(시작 검사·push 뒤) 단언
  precheck: compute만 실패하는 PY 래퍼 → rc ≠ 0·"전부 통과" 없음·옛 도장 지움(통과 래퍼 대조군은 rc 0·도장 = 작업본 md5)
임시 저장소는 core.autocrlf=true(이 PC와 같게 — .gitattributes가 막는지 보려면 변환이 켜져 있어야 한다).
입력은 늘 data/ 밖 사본이다(archive.py store는 같은 경로면 원본을 지운 뒤 복사하다 잃는다 — 그 조건을 쓰지 않는다).
"""
import atexit
import hashlib
import os
import shutil
import stat
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
DATA = os.path.join(ROOT, "data")
FILES = {"키워드.csv": "필라테스 보고서,2580077.csv", "검색어.csv": "검색어 보고서,2580077.csv",
         "상세지역.csv": "상세지역 보고서,2580077.csv", "시간대별.csv": "시간대별 보고서,2580077.csv"}
_fd, EMPTY_GITCONFIG = tempfile.mkstemp(suffix=".gitconfig")   # 실행마다 새 빈 파일(공용 이름이면 남은 내용이 전역 설정이 된다 — 리뷰 반영)
os.close(_fd)
atexit.register(lambda: os.path.exists(EMPTY_GITCONFIG) and os.remove(EMPTY_GITCONFIG))


def clean_env(**extra):
    """호출 환경의 GIT_* 변수(GIT_DIR 등)를 지우고 시스템·전역 git 설정을 끈다 — 임시 저장소 밖 실제 저장소·설정에 닿지 않게(test_deploy W10과 같은 방식).
    autocrlf는 임시 저장소 설정으로 켠다(setUp)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "PYTHONUTF8"))}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=EMPTY_GITCONFIG, GIT_CEILING_DIRECTORIES=os.path.dirname(tempfile.gettempdir()), **extra)
    return env


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
    r = subprocess.run([GIT, "-c", "core.quotepath=false", *args], cwd=cwd, capture_output=True, env=clean_env(),
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
        git(self.repo, "config", "core.autocrlf", "true")                # 이 PC와 같게(시스템 설정에 기대지 않는다)
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
        env = clean_env(PY=sys.executable)                               # ingest.sh가 스스로 PYTHONUTF8=1을 건다
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
        self.assertEqual(out.count("origin/main = HEAD"), 2, out)           # 시작 검사 + push 뒤 끝 확인
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
        head_after = self.head()
        rc2, out2 = self.ingest()                                     # 같은 입력 → 시작 검사(N3)가 store 전에 멈춘다
        self.assertEqual(rc2, 1, out2)
        self.assertIn("≠ origin/main", out2)
        self.assertIn("시작 전 — store 전에 멈춤", out2)
        self.assertNotIn("== store", out2)
        self.assertEqual(self.head(), head_after)
        self.assertEqual(git(self.bare, "rev-parse", "main"), origin_before)

    def test_5_crlf_input_bytes_preserved(self):
        """수집 CSV가 CRLF여도 원격 blob은 입력 바이트 그대로(.gitattributes `*.csv -text`). 이 PC(autocrlf=true)에서 속성이 없으면 LF로 바뀐다."""
        crlf = {}
        for p in self.inputs:
            with open(p, "rb") as f:
                b = f.read().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            with open(p, "wb") as f:
                f.write(b)
            crlf[p] = b
        rc, out = self.ingest()
        self.assertEqual(rc, 0, out)
        for kind, p in zip(FILES, self.inputs):
            got = git(self.bare, "show", f"main:data/2026-09/{kind}", raw=True)
            self.assertIn(b"\r\n", got, kind)
            self.assertEqual(md5b(got), md5b(crlf[p]), kind)

    def test_6_start_check_origin_ahead_stops_before_store(self):
        other = os.path.join(self.td, "other")
        git(self.td, "clone", "-q", self.bare, other)
        with open(os.path.join(other, "note.txt"), "w", encoding="utf-8") as f:
            f.write("원격이 앞선다\n")
        git(other, "add", "note.txt")
        git(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "ahead")
        git(other, "push", "-q", "origin", "HEAD:main")
        before = self.head()
        rc, out = self.ingest()
        self.assertEqual(rc, 1, out)
        self.assertIn("≠ origin/main", out)
        self.assertIn("시작 전 — store 전에 멈춤", out)
        self.assertNotIn("== store", out)
        self.assertEqual(self.head(), before)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "data", "2026-09")))

    def test_7_start_check_eol_mismatch_stops_before_store(self):
        """병합 직후 main 작업 폴더 흉내: .gitattributes 없던 때 autocrlf=true로 풀린 CSV(CRLF)가 blob이 같아 다시 안 풀려
        `git status`·`git diff HEAD`는 깨끗한데 i/lf w/crlf — 줄바꿈 검사만 잡는다(검증 1 10항 재현 방식)."""
        rel, sp = "data/2026-08/키워드.csv", "data/2026-08/공백 이름.csv"   # 공백 경로 — awk `$NF`면 "이름.csv"로 잘린다
        c = ("-c", "user.name=t", "-c", "user.email=t@t")
        shutil.copy(os.path.join(self.repo, *rel.split("/")), os.path.join(self.repo, *sp.split("/")))
        git(self.repo, "add", sp)
        git(self.repo, *c, "commit", "-q", "-m", "공백 경로")
        git(self.repo, "push", "-q", "origin", "HEAD:main")                   # 시작 검사(HEAD = origin/main)는 통과하게
        git(self.repo, "rm", "-q", ".gitattributes")
        git(self.repo, *c, "commit", "-q", "-m", "속성 없던 때")
        for r in (rel, sp):
            os.remove(os.path.join(self.repo, *r.split("/")))
            git(self.repo, "checkout", "--", r)                               # autocrlf=true·속성 없음 → CRLF로 풀림
        time.sleep(1.2)
        git(self.repo, "status", "--porcelain")                               # 색인 stat 갱신(racy 아님)
        git(self.repo, "reset", "-q", "--keep", "HEAD~1")                     # .gitattributes 있는 커밋으로 — CSV blob이 같아 다시 안 풀림
        with open(os.path.join(self.repo, *rel.split("/")), "rb") as f:
            self.assertIn(b"\r\n", f.read())
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")         # 상태·diff는 깨끗(이 경우를 diff 검사는 못 잡는다)
        before = self.head()
        rc, out = self.ingest()
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] data/ CSV 줄바꿈이 커밋과 다름", out)
        self.assertIn(f"  {rel}", out)                                        # 경로 전체(탭 기준 — 공백 경로도 안 잘림)
        self.assertIn(f"  {sp}", out)
        self.assertNotIn("data/가 HEAD와 다름", out)
        self.assertNotIn("== store", out)
        self.assertEqual(self.head(), before)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "data", "2026-09")))
        self.assertEqual(git(self.repo, "diff", "--cached", "--name-only"), "")   # 스테이징 0

    def test_8_start_check_data_differs_from_head_staged_or_not(self):
        """W2: 스테이징된 CRLF(i/crlf w/crlf라 줄바꿈 검사는 통과)·미스테이징 변경 둘 다 `git diff --quiet HEAD -- data`가 store 전에 멈춘다."""
        rel = "data/2026-08/키워드.csv"
        p = os.path.join(self.repo, *rel.split("/"))
        with open(p, "rb") as f:
            orig = f.read()
        for staged in (True, False):
            with open(p, "wb") as f:
                f.write(orig.replace(b"\n", b"\r\n"))
            if staged:
                git(self.repo, "add", rel)
                self.assertIn("i/crlf", git(self.repo, "ls-files", "--eol", "--", rel))
            before = self.head()
            rc, out = self.ingest()
            self.assertEqual(rc, 1, out)
            self.assertIn("[FAIL] data/가 HEAD와 다름(스테이징·미스테이징)", out)
            self.assertNotIn("== store", out)
            self.assertEqual(self.head(), before)
            self.assertFalse(os.path.exists(os.path.join(self.repo, "data", "2026-09")))
            git(self.repo, "restore", "--source=HEAD", "--staged", "--worktree", "--", "data")   # code-tab.md 4절 복구 명령
            self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        newf = os.path.join(self.repo, "data", "2026-10", "시간대별.csv")          # 스테이징된 새 파일(ingest 커밋 실패로 남는 `A`) — 복구 명령이 지운다
        os.makedirs(os.path.dirname(newf))
        shutil.copy(p, newf)
        git(self.repo, "add", "data/2026-10/시간대별.csv")
        rc, out = self.ingest()
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] data/가 HEAD와 다름", out)
        self.assertIn("git restore --source=HEAD --staged --worktree -- data", out)
        git(self.repo, "restore", "--source=HEAD", "--staged", "--worktree", "--", "data")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        self.assertFalse(os.path.exists(newf))
        extra = os.path.join(self.repo, "data", "2026-10", "키워드.csv")          # 추적 안 된 파일(store 부분 적용 흉내) — diff는 못 본다(리뷰 반영)
        os.makedirs(os.path.dirname(extra), exist_ok=True)
        shutil.copy(p, extra)
        self.assertEqual(subprocess.run([GIT, "diff", "--quiet", "HEAD", "--", "data"], cwd=self.repo, env=clean_env()).returncode, 0)
        before = self.head()
        rc, out = self.ingest()
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] data/에 추적 안 된 파일이 있음", out)
        self.assertIn("  data/2026-10/키워드.csv", out)
        self.assertNotIn("== store", out)
        self.assertEqual(self.head(), before)


PYWRAP = r"""#!/bin/sh
case "$1" in
  *compute.py) if [ "$T_COMPUTE" = fail ]; then echo "compute 실패(시험 래퍼)" >&2; exit 1; fi
               if [ -n "$T_EDIT" ]; then printf 'x' >> "$T_EDIT"; fi; echo "compute 통과(시험 래퍼)"; exit 0 ;;
  *validate.py|*compare.py|*overflow_check.py) printf '%s\n' "가짜 1" "가짜 2" "${1##*/} 통과(시험 래퍼)"; exit 0 ;;
esac
exec "{py}" "$@"
"""


@unittest.skipUnless(BASH, "bash 없음")
class PrecheckTests(unittest.TestCase):
    """precheck.sh 흐름(검증 1 결론 6): validate가 통과하고 compute만 실패하면 거기서 멈춘다(옛 판은 '전부 통과' rc 0)."""

    def setUp(self):
        self.td = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.td, "work"))
        os.makedirs(os.path.join(self.td, "combined"))
        for name, text in (("work/index.html", "<html>work</html>\n"), ("prev.html", "<html>prev</html>\n")):
            with open(os.path.join(self.td, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        self.wrap = os.path.join(self.td, "pywrap.sh")
        with open(self.wrap, "w", encoding="utf-8", newline="\n") as f:
            f.write(PYWRAP.replace("{py}", sys.executable.replace(os.sep, "/")))

    def tearDown(self):
        shutil.rmtree(self.td, onerror=_rm_ro)

    def precheck(self, compute, *extra, prev="prev.html", edit=None, html="work/index.html"):
        u = lambda n: os.path.join(self.td, n).replace(os.sep, "/")
        env = clean_env(PY=u("pywrap.sh"), T_COMPUTE=compute, T_EDIT=u(edit) if edit else "")
        r = subprocess.run([BASH, os.path.join(ROOT, "scripts", "precheck.sh").replace(os.sep, "/"),
                            u(html), u("combined"), u(prev), *extra],
                           cwd=self.td, env=env, capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr

    def md5_of(self, rel):
        with open(os.path.join(self.td, *rel.split("/")), "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def test_compute_failure_stops_before_compare(self):
        stamp = os.path.join(self.td, "work", "precheck_ok.md5")
        rc, out = self.precheck("ok")                                 # 대조군: 래퍼가 통과면 끝까지 간다(빈 시험이 아님) + 도장(W11)
        self.assertEqual(rc, 0, out)
        self.assertIn("compare.py 통과(시험 래퍼)", out)
        self.assertIn("== 6단계 전부 통과", out)
        with open(stamp, encoding="utf-8") as f:                        # X2: 작업본 md5 · 직전 배포본 md5 · 모드
            self.assertEqual(f.read(), f"{self.md5_of('work/index.html')}  index.html\n{self.md5_of('prev.html')}  prev.html\nmode full\n")
        rc, out = self.precheck("fail")
        self.assertNotEqual(rc, 0, out)
        self.assertIn("== compute", out)
        self.assertIn("compute 실패(시험 래퍼)", out)
        self.assertNotIn("compare.py 통과", out)
        self.assertNotIn("== overflow", out)
        self.assertNotIn("전부 통과", out)
        self.assertFalse(os.path.exists(stamp))                        # 실패한 실행은 옛 도장도 지운다

    def test_stamp_pending_mode_edit_during_run_and_missing_file(self):
        """X2·X11: --pending 통과면 도장 모드 pending · precheck 도중 작업본이 바뀌면 [FAIL]·도장 없음 ·
        파일 없음(직전 배포본·작업본 둘 다)은 md5 가드 전에 exit 2 — 그때도 옛 도장은 지운다."""
        stamp = os.path.join(self.td, "work", "precheck_ok.md5")
        rc, out = self.precheck("ok", "--pending")
        self.assertEqual(rc, 0, out)
        with open(stamp, encoding="utf-8") as f:
            self.assertTrue(f.read().endswith("mode pending\n"))
        rc, out = self.precheck("ok", edit="work/index.html")          # compute 도중 작업본이 바뀜(편집기 저장 등)
        self.assertEqual(rc, 1, out)
        self.assertIn("[FAIL] 작업본이 precheck 도중 바뀜", out)
        self.assertNotIn("전부 통과", out)
        self.assertFalse(os.path.exists(stamp))
        for kw in ({"prev": "없는.html"}, {"html": "work/없는.html"}):
            rc, out = self.precheck("ok", "--pending")                    # 통과(도장 생김) 뒤에
            self.assertEqual(rc, 0, out)
            self.assertTrue(os.path.exists(stamp))
            rc, out = self.precheck("ok", **kw)                           # 파일 없음 — 옛 도장(mode pending)이 남지 않는다
            self.assertEqual(rc, 2, out)
            self.assertIn("[FAIL] 파일 없음:", out)
            self.assertIn("없는.html", out)
            self.assertNotIn("== validate", out)
            self.assertFalse(os.path.exists(stamp), kw)


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1)
    same = BEFORE == real_md5s()
    print(f"실제 data/ md5 전/후 동일: {same} ({len(BEFORE)}파일)")
    sys.exit(0 if r.result.wasSuccessful() and same else 1)
