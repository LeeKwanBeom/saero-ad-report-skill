#!/usr/bin/env python3
"""scripts/fetch_reports.py 오프라인 검사 — 네이버 접속 0, 네트워크 0(로컬 http.server), 실제 data/·config 불변.

실행: python3 tests/test_fetch_reports.py   (unittest, 저장소 루트에서)
검사: config columns = 실 CSV 2행 / 기대 기간(평일·1일) / dry-run 브라우저 0·파일 0(가짜 playwright 패키지로 import 자체를 막음) /
     check_file·cross_check(실 data/2026-09 4파일) / --prev 재집계 WARN / click_allowed 금지 차단 /
     Playwright + 로컬 가짜 화면(tests/fixtures): --login 도달 → 4개 다운로드 성공 → 1일엔 `지난달` 프리셋 → 이름 하나 틀리면 exit 2·
     정상 폴더 없음·partial/에만 → 로그인 안 됐으면 exit 1. 브라우저(크로미움)가 없으면 브라우저 시험만 skip.
"""
import datetime as dt
import functools
import hashlib
import http.server
import io
import json
import os
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import fetch_reports as F  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures")
DATA = os.path.join(ROOT, "data", "2026-09")
D = dt.date


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def md5f(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def real_md5s():
    out = {}
    for fn in ("키워드.csv", "검색어.csv", "상세지역.csv", "시간대별.csv"):
        out[fn] = md5f(os.path.join(DATA, fn))
    out["config"] = md5f(os.path.join(ROOT, "config", "report-config.json"))
    return out


BEFORE = real_md5s()


def rf_for(list_url, download_dir, profile_dir, **over):
    with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["report_fetch"] = {**cfg["report_fetch"], "list_url": list_url, "download_dir": download_dir, "profile_dir": profile_dir,
                           "browser_channel": None, "timeout_sec": {"page": 8, "download": 20, "login": 20}, "settle_sec": 0.2, **over}
    return F.fetch_config(cfg)


class FakeLocator:
    def __init__(self, text):
        self.text, self.clicked = text, False

    def inner_text(self):
        return self.text

    def click(self):
        self.clicked = True


class PureTests(unittest.TestCase):
    def test_config_columns_match_real_csv(self):
        rf = F.fetch_config()
        for fn, kind in (("키워드.csv", "키워드"), ("검색어.csv", "검색어"), ("상세지역.csv", "상세지역"), ("시간대별.csv", "시간대별")):
            head, colline, rows, crlf = F.read_report(os.path.join(DATA, fn))
            self.assertEqual(colline, rf["columns"][kind], fn)
            self.assertEqual(F.kind_by_columns(colline.split(",")), kind)
            self.assertFalse(crlf, fn)
        self.assertEqual(rf["account_no"], "2580077")
        self.assertEqual(list(rf["report_names"].values()), ["시간대별", "상세지역", "검색어", "키워드"])

    def test_expected_period(self):
        rule = {"other": "이번달", "day1": "지난달"}
        self.assertEqual(F.expected_period(D(2026, 9, 28), rule), ("이번달", D(2026, 9, 1), D(2026, 9, 27)))
        self.assertEqual(F.expected_period(D(2026, 10, 1), rule), ("지난달", D(2026, 9, 1), D(2026, 9, 30)))
        self.assertEqual(F.expected_period(D(2026, 9, 1), rule), ("지난달", D(2026, 8, 1), D(2026, 8, 31)))
        self.assertEqual(F.expected_period(D(2026, 3, 1), rule), ("지난달", D(2026, 2, 1), D(2026, 2, 28)))
        self.assertEqual(F.expected_period(D(2026, 9, 2), rule), ("이번달", D(2026, 9, 1), D(2026, 9, 1)))
        self.assertEqual(F.short_name("필라테스 보고서"), "필라테스")
        plan = F.make_plan(F.fetch_config(download_dir="/tmp/x", profile_dir="/tmp/y"), D(2026, 9, 28))
        self.assertEqual([i["expected_file"] for i in plan["items"]],
                         ["시간대별_보고서_2580077.csv", "상세지역_보고서_2580077.csv", "검색어_보고서_2580077.csv", "필라테스_보고서_2580077.csv"])

    def test_dry_run_no_browser_no_files(self):
        """가짜 playwright 패키지를 앞에 두어 import되면 실패하게 하고, 저장·프로필 폴더가 생기지 않는지."""
        tmp = tempfile.mkdtemp()
        try:
            fake = os.path.join(tmp, "fakepw", "playwright")
            os.makedirs(fake)
            with open(os.path.join(fake, "__init__.py"), "w") as f:
                f.write("raise ImportError('dry-run must not import playwright')\n")
            env = {**os.environ, "PYTHONPATH": os.path.join(tmp, "fakepw"), "PYTHONIOENCODING": "utf-8"}
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "fetch_reports.py"), "--dry-run", "--today", "2026-09-28",
                                "--download-dir", os.path.join(tmp, "dl"), "--profile-dir", os.path.join(tmp, "prof")],
                               capture_output=True, text=True, encoding="utf-8", env=env, cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("브라우저를 열지 않음", r.stdout)
            self.assertEqual(r.stdout.count("_보고서_2580077.csv"), 4)
            self.assertIn("2026.09.01.~2026.09.27.", r.stdout)
            self.assertFalse(os.path.exists(os.path.join(tmp, "dl")))
            self.assertFalse(os.path.exists(os.path.join(tmp, "prof")))
            r2 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "fetch_reports.py"), "--dry-run", "--today", "2026-10-01",
                                 "--download-dir", os.path.join(tmp, "dl"), "--profile-dir", os.path.join(tmp, "prof")],
                                capture_output=True, text=True, encoding="utf-8", env=env)
            self.assertIn("`지난달` = 2026.09.01.~2026.09.30.", r2.stdout)
            # 브라우저가 필요한 모드는 같은 환경에서 exit 1로 멈춰야 한다(설치 안내)
            r3 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "fetch_reports.py"), "--login",
                                 "--download-dir", os.path.join(tmp, "dl"), "--profile-dir", os.path.join(tmp, "prof")],
                                capture_output=True, text=True, encoding="utf-8", env=env)
            self.assertEqual(r3.returncode, 1)
            self.assertIn("playwright가 없습니다", r3.stdout + r3.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_file_and_cross_on_real_data(self):
        rf = F.fetch_config(download_dir="/tmp/x", profile_dir="/tmp/y")
        s, e = D(2026, 9, 1), D(2026, 9, 26)
        res = {}
        for fn, name, kind in (("키워드.csv", "필라테스 보고서", "키워드"), ("검색어.csv", "검색어 보고서", "검색어"),
                               ("상세지역.csv", "상세지역 보고서", "상세지역"), ("시간대별.csv", "시간대별 보고서", "시간대별")):
            r = F.check_file(os.path.join(DATA, fn), name, kind, rf, s, e)
            self.assertTrue(r["ok"], (fn, [c for c in r["checks"] if not c["ok"]]))
            self.assertEqual(r["account"], "2580077")
            res[kind] = r
        cross = F.cross_check(list(res.values()))
        self.assertTrue(cross["ok"], cross)
        self.assertEqual(len(set(cross["values"].values())), 1)
        self.assertEqual(res["키워드"]["dates"][0], "2026.09.01.")
        # 기간이 기대와 다르면 FAIL(매월 1일 "1일~말일" 검사도 같은 자리)
        r = F.check_file(os.path.join(DATA, "키워드.csv"), "필라테스 보고서", "키워드", rf, s, D(2026, 9, 27))
        self.assertFalse(r["ok"])
        self.assertIn("기간 = 기대", [c["name"] for c in r["checks"] if not c["ok"]])
        # 이름이 다르면 FAIL
        r = F.check_file(os.path.join(DATA, "키워드.csv"), "검색어 보고서", "검색어", rf, s, e)
        self.assertFalse(r["ok"])
        # 합성: 행 0 / 컬럼 다름 / 계정 다름 / 헤더 형식
        tmp = tempfile.mkdtemp()
        try:
            def w(name, text):
                p = os.path.join(tmp, name)
                with open(p, "w", encoding="utf-8-sig", newline="") as f:
                    f.write(text)
                return p
            col = rf["columns"]["시간대별"]
            self.assertFalse(F.check_file(w("a.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),2580077"\n{col}\n'), "시간대별 보고서", "시간대별", rf, s, e)["ok"])
            self.assertFalse(F.check_file(w("b.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),2580077"\n{col},추가열\n00시~01시,1,0,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, s, e)["ok"])
            self.assertFalse(F.check_file(w("c.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),9999999"\n{col}\n00시~01시,1,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, s, e)["ok"])
            self.assertFalse(F.check_file(w("d.csv", f'시간대별 보고서 2026-09-01~2026-09-26\n{col}\n00시~01시,1,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, s, e)["ok"])
            good = F.check_file(w("e.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),2580077"\n{col}\n00시~01시,1,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, s, e)
            self.assertTrue(good["ok"], good["checks"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compare_prev_warns_on_recount(self):
        rf = F.fetch_config(download_dir="/tmp/x", profile_dir="/tmp/y")
        s, e = D(2026, 9, 1), D(2026, 9, 26)
        now = [F.check_file(os.path.join(DATA, fn), name, kind, rf, s, e) for fn, name, kind in
               (("키워드.csv", "필라테스 보고서", "키워드"), ("검색어.csv", "검색어 보고서", "검색어"), ("상세지역.csv", "상세지역 보고서", "상세지역"))]
        tmp = tempfile.mkdtemp()
        try:
            for fn in ("키워드.csv", "검색어.csv", "상세지역.csv", "시간대별.csv"):
                shutil.copy(os.path.join(DATA, fn), os.path.join(tmp, fn))
            prev = F.load_prev(tmp)
            self.assertEqual(set(prev), {"키워드", "검색어", "상세지역"})
            warns, detail = F.compare_prev(now, prev)
            self.assertEqual(warns, [])
            self.assertEqual(detail["키워드"]["common_days"], 26)
            # 9/10 노출 하나를 바꾸면 WARN
            p = os.path.join(tmp, "키워드.csv")
            with open(p, encoding="utf-8-sig") as f:
                lines = f.read().split("\n")
            for i, ln in enumerate(lines):
                if ",2026.09.10.," in ln:
                    parts = ln.split(",")
                    parts[7] = str(int(parts[7]) + 1)
                    lines[i] = ",".join(parts)
                    break
            with open(p, "w", encoding="utf-8-sig", newline="") as f:
                f.write("\n".join(lines))
            warns, detail = F.compare_prev(now, F.load_prev(tmp))
            self.assertEqual(len(warns), 1)
            self.assertIn("[WARN] 키워드", warns[0])
            self.assertIn("2026.09.10.", warns[0])
            self.assertEqual(detail["키워드"]["diff_days"], 1)
            self.assertIsNone(F.load_prev(os.path.join(tmp, "없음")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_click_allowed_guard(self):
        rf = F.fetch_config(download_dir="/tmp/x", profile_dir="/tmp/y")
        for text in ("보고서 형식 저장 ∨", "+ 새 보고서 ∨", "삭제", "로그인", "×"):
            loc = FakeLocator(text)
            with self.assertRaises(SystemExit) as cm:
                F.click_allowed("download", loc, rf)
            self.assertIn("금지 요소", str(cm.exception))
            self.assertFalse(loc.clicked, text)
        loc = FakeLocator("저장")
        with self.assertRaises(SystemExit) as cm:
            F.click_allowed("save_format", loc, rf)
        self.assertIn("허용 목록 밖", str(cm.exception))
        self.assertFalse(loc.clicked)
        ok = FakeLocator("다운로드")
        F.click_allowed("download", ok, rf)
        self.assertTrue(ok.clicked)
        # config에 코드가 모르는 동작을 넣으면 시작부터 거부
        with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["report_fetch"] = {**cfg["report_fetch"], "allowed_actions": {**cfg["report_fetch"]["allowed_actions"], "save_format": "보고서 형식 저장"}}
        with self.assertRaises(SystemExit):
            F.fetch_config(cfg)
        # 소스에서 클릭 호출 자리가 하나뿐인지·좌표/입력 API가 없는지
        with open(os.path.join(ROOT, "scripts", "fetch_reports.py"), encoding="utf-8") as f:
            src = f.read()
        self.assertEqual(src.count(".click("), 1)
        for bad in ("mouse.", ".fill(", ".type(", ".press(", "drag_to", "password", "비밀번호"):
            self.assertNotIn(bad, src, bad)


# ---------------------------------------------------------------- 브라우저(가짜 화면) 시험
def browser_available():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            b.close()
        return True
    except Exception:
        return False


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class FixtureServer:
    def __enter__(self):
        handler = functools.partial(QuietHandler, directory=FIX)
        self.httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
        self.port = self.httpd.server_address[1]
        self.t = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.t.start()
        return self

    def url(self, query=""):
        return f"http://127.0.0.1:{self.port}/report-ui-fixture.html" + (("?" + query) if query else "")

    def __exit__(self, *a):
        self.httpd.shutdown()
        self.httpd.server_close()


@unittest.skipUnless(browser_available(), "playwright/크로미움 없음 — 브라우저 시험 skip")
class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.srv = FixtureServer().__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.srv.__exit__(None, None, None)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_quiet(self, fn, *a, **k):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = fn(*a, **k)
        return code, buf.getvalue()

    def test_1_login_then_fetch_success_then_day1_then_prev(self):
        dl, prof = os.path.join(self.tmp, "dl"), os.path.join(self.tmp, "prof")
        rf = rf_for(self.srv.url("auto=1&today=2026-09-28"), dl, prof)
        code, out = self.run_quiet(F.cmd_login, rf, headless=True)
        self.assertEqual(code, 0, out)
        self.assertIn("목록 URL 도달", out)
        self.assertIn("4/4개", out)
        # 본 실행(로그인 상태 유지 — 프로필 재사용)
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), debug=True, headless=True)
        self.assertEqual(code, 0, out)
        day = os.path.join(dl, "2026-09-28")
        files = sorted(f for f in os.listdir(day) if f.endswith(".csv"))
        self.assertEqual(files, sorted(["시간대별_보고서_2580077.csv", "상세지역_보고서_2580077.csv", "검색어_보고서_2580077.csv", "필라테스_보고서_2580077.csv"]))
        self.assertTrue(os.path.exists(os.path.join(day, "summary.json")))
        self.assertTrue(os.path.isdir(os.path.join(day, "debug")))
        self.assertFalse(os.path.exists(os.path.join(dl, "partial", "2026-09-28")))
        summ = load_json(os.path.join(day, "summary.json"))
        self.assertEqual(summ["result"], "ok")
        self.assertEqual(summ["expected"], {"preset": "이번달", "start": "2026.09.01.", "end": "2026.09.27."})
        self.assertTrue(summ["cross"]["ok"])
        for r in summ["reports"]:
            self.assertEqual(r["status"], "ok", r)
            self.assertFalse(r["preset_clicked"])  # 저장된 `이번달`이라 프리셋 클릭 없음
            self.assertEqual(r["check"]["period"], ["2026.09.01.", "2026.09.27."])
        with open(os.path.join(day, "필라테스_보고서_2580077.csv"), "rb") as f:
            raw = f.read()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\n", raw)
        head, colline, rows, _ = F.read_report(os.path.join(day, "필라테스_보고서_2580077.csv"))
        self.assertEqual(head, '"필라테스 보고서(2026.09.01.~2026.09.27.),2580077"')
        self.assertEqual(colline, rf["columns"]["키워드"])
        self.assertEqual(len(rows), 27 * 2)
        for f in os.listdir(day):  # 금지 요소가 클릭됐다면 화면이 FORBIDDEN_CLICKED로 바뀌어 다운로드가 안 된다
            self.assertNotIn("FORBIDDEN", f)

        # 매월 1일: 기대 = 지난달(9/1~9/30) — 화면은 `이번달`로 뜨므로 프리셋 클릭 경로
        rf1 = rf_for(self.srv.url("auto=1&today=2026-10-01"), dl, prof)
        code, out = self.run_quiet(F.cmd_fetch, rf1, D(2026, 10, 1), headless=True)
        self.assertEqual(code, 0, out)
        summ1 = load_json(os.path.join(dl, "2026-10-01", "summary.json"))
        self.assertEqual(summ1["expected"]["preset"], "지난달")
        for r in summ1["reports"]:
            self.assertTrue(r["preset_clicked"], r)
            self.assertEqual(r["check"]["period"], ["2026.09.01.", "2026.09.30."])
        self.assertTrue(summ1["cross"]["ok"])
        self.assertIn("프리셋 `지난달`", out)

        # --prev: 9/28 폴더(9/1~9/27)와 10/1 결과(9/1~9/30)의 겹치는 27일 — 같은 생성 규칙이라 WARN 0; 바꾼 사본은 WARN
        code, out = self.run_quiet(F.cmd_fetch, rf1, D(2026, 10, 1), prev_dir=day, headless=True)
        self.assertEqual(code, 0, out)
        summ2 = load_json(os.path.join(dl, "2026-10-01", "summary.json"))
        self.assertEqual([w for w in summ2["warnings"] if w.startswith("[WARN]")], [])
        self.assertEqual(summ2["prev_compare"]["키워드"]["common_days"], 27)
        tampered = os.path.join(self.tmp, "prev_tampered")
        shutil.copytree(day, tampered, ignore=shutil.ignore_patterns("debug", "summary.json"))
        p = os.path.join(tampered, "검색어_보고서_2580077.csv")
        with open(p, encoding="utf-8-sig") as f:
            txt = f.read().replace(",2026.09.10.,", ",2026.09.10.,9", 1)
        with open(p, "w", encoding="utf-8-sig", newline="") as f:
            f.write(txt)
        code, out = self.run_quiet(F.cmd_fetch, rf1, D(2026, 10, 1), prev_dir=tampered, headless=True)
        self.assertEqual(code, 0, out)  # WARN은 막지 않는다
        summ3 = load_json(os.path.join(dl, "2026-10-01", "summary.json"))
        w = [x for x in summ3["warnings"] if x.startswith("[WARN] 검색어")]
        self.assertEqual(len(w), 1, summ3["warnings"])
        self.assertIn("2026.09.10.", w[0])

    def test_2_partial_failure_wrong_name_exit2(self):
        dl, prof = os.path.join(self.tmp, "dl2"), os.path.join(self.tmp, "prof2")
        names = {"시간대별 보고서": "시간대별", "상세지역 보고서": "상세지역", "검색어 보고서X": "검색어", "필라테스 보고서": "키워드"}
        rf = rf_for(self.srv.url("auto=1&today=2026-09-28"), dl, prof, report_names=names, timeout_sec={"page": 3, "download": 10, "login": 20})
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), headless=True)
        self.assertEqual(code, 2, out)
        self.assertFalse(os.path.exists(os.path.join(dl, "2026-09-28")))  # 정상 폴더 없음
        stage = os.path.join(dl, "partial", "2026-09-28")
        files = sorted(f for f in os.listdir(stage) if f.endswith(".csv"))
        self.assertEqual(len(files), 3)
        self.assertNotIn("검색어_보고서_2580077.csv", files)
        summ = load_json(os.path.join(stage, "summary.json"))
        self.assertEqual(summ["result"], "partial")
        self.assertEqual(summ["exit_code"], 2)
        st = {r["name"]: r["status"] for r in summ["reports"]}
        self.assertEqual(st["검색어 보고서X"], "fail")
        self.assertEqual(sum(1 for v in st.values() if v == "ok"), 3)
        self.assertIn("성공 3 · 실패 1", out)
        self.assertIn("store 금지", out)
        self.assertTrue(any(f.endswith("_no_link.png") for f in os.listdir(os.path.join(stage, "debug"))))

    def test_4_inputs_ui_with_delay_and_day1_preset(self):
        """RangePicker형(기간이 input 2개 + 아이콘)이고 표시가 늦게 그려져도 읽고, 1일엔 textbox를 눌러 프리셋을 고른다."""
        dl, prof = os.path.join(self.tmp, "dl4"), os.path.join(self.tmp, "prof4")
        rf = rf_for(self.srv.url("auto=1&today=2026-09-28&ui=inputs&delay=900"), dl, prof)
        code, out = self.run_quiet(F.cmd_login, rf, headless=True)
        self.assertEqual(code, 0, out)
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), headless=True)
        self.assertEqual(code, 0, out)
        summ = load_json(os.path.join(dl, "2026-09-28", "summary.json"))
        for r in summ["reports"]:
            self.assertEqual(r["status"], "ok", r)
            self.assertEqual(r["period_read"]["how"], "inputs", r["period_read"])
            self.assertFalse(r["preset_clicked"])
        rf1 = rf_for(self.srv.url("auto=1&today=2026-10-01&ui=inputs&delay=900"), dl, prof)
        code, out = self.run_quiet(F.cmd_fetch, rf1, D(2026, 10, 1), headless=True)
        self.assertEqual(code, 0, out)
        summ1 = load_json(os.path.join(dl, "2026-10-01", "summary.json"))
        for r in summ1["reports"]:
            self.assertTrue(r["preset_clicked"], r)
            self.assertEqual(r["check"]["period"], ["2026.09.01.", "2026.09.30."])
        self.assertIn("클릭 open_period:", out)

    def test_5_period_missing_on_one_report_others_still_downloaded(self):
        """왕복 1 재현: 첫 보고서 화면에서 기간을 못 읽어 실패해도 목록으로 돌아가 나머지 3개를 받는다(exit 2, partial 3개)."""
        dl, prof = os.path.join(self.tmp, "dl5"), os.path.join(self.tmp, "prof5")
        rf = rf_for(self.srv.url("auto=1&today=2026-09-28&noperiod=" + "시간대별 보고서"), dl, prof, timeout_sec={"page": 3, "download": 10, "login": 20})
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), debug=True, headless=True)
        self.assertEqual(code, 2, out)
        stage = os.path.join(dl, "partial", "2026-09-28")
        files = sorted(f for f in os.listdir(stage) if f.endswith(".csv"))
        self.assertEqual(files, sorted(["상세지역_보고서_2580077.csv", "검색어_보고서_2580077.csv", "필라테스_보고서_2580077.csv"]))
        summ = load_json(os.path.join(stage, "summary.json"))
        st = {r["kind"]: r for r in summ["reports"]}
        self.assertEqual(st["시간대별"]["status"], "fail")
        self.assertIn("기간을 읽지 못함", st["시간대별"]["error"])
        for k in ("상세지역", "검색어", "키워드"):
            self.assertEqual(st[k]["status"], "ok", st[k])
        self.assertFalse(os.path.exists(os.path.join(dl, "2026-09-28")))
        dbg = os.listdir(os.path.join(stage, "debug"))
        self.assertTrue(any(f.endswith("_no_period.png") for f in dbg), dbg)
        self.assertTrue(any(f.endswith("_no_period.aria.txt") for f in dbg), dbg)
        self.assertTrue(any(f.endswith("_no_period.inventory.json") for f in dbg), dbg)
        inv = load_json(os.path.join(stage, "debug", [f for f in dbg if f.endswith("_no_period.inventory.json")][0]))
        self.assertIn("clickables", inv)
        self.assertTrue(any("돌아가기" in c["text"] for c in inv["clickables"]))
        with open(os.path.join(stage, "debug", [f for f in dbg if f.endswith("_no_period.aria.txt")][0]), encoding="utf-8") as f:
            self.assertIn("돌아가기", f.read())

    def test_3_not_logged_in_exit1(self):
        dl, prof = os.path.join(self.tmp, "dl3"), os.path.join(self.tmp, "prof3")
        rf = rf_for(self.srv.url("today=2026-09-28"), dl, prof, timeout_sec={"page": 3, "download": 10, "login": 4})
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), headless=True)
        self.assertEqual(code, 1, out)
        self.assertIn("--login", out)
        self.assertFalse(os.path.exists(os.path.join(dl, "2026-09-28")))
        self.assertEqual([f for f in os.listdir(os.path.join(dl, "partial", "2026-09-28")) if f.endswith(".csv")], [])
        code, out = self.run_quiet(F.cmd_login, rf, headless=True)  # 사용자가 로그인하지 않으면 --login도 시간 안에 실패
        self.assertEqual(code, 1, out)


if __name__ == "__main__":
    try:
        unittest.main(exit=False, verbosity=2)
    finally:
        after = real_md5s()
        print(f"실제 data/2026-09·config md5 전/후 동일: {after == BEFORE} ({BEFORE['config'][:8]} 등)")
