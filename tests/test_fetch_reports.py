#!/usr/bin/env python3
"""scripts/fetch_reports.py 오프라인 검사 — 네이버 접속 0, 네트워크 0(로컬 http.server), 실제 data/·config 불변.

실행: "$PY" tests/test_fetch_reports.py   (unittest, 저장소 루트에서 Git Bash — $PY = 저장소 밖 venv 파이썬, references/code-tab.md 1절)
검사: config columns = 실 CSV 2행 / 기대 기간(평일·1일) / dry-run 브라우저 0·파일 0(가짜 playwright 패키지로 import 자체를 막음) /
     check_file·cross_check(실 data/2026-09 4파일) / --prev 재집계 WARN / click_allowed 금지 차단 /
     프로필 다운로드 기록 정리(가짜 History DB: 파일 없는 행만 삭제·파일 있는 행 유지·DB 없음/잠김 WARN) / browser_channel 그대로 /
     Playwright + 로컬 가짜 화면(tests/fixtures): --login 도달 → 4개 다운로드 성공 → 1일엔 `지난달` 프리셋 → 이름 하나 틀리면 exit 2·
     정상 폴더 없음·partial/에만 → 로그인 안 됐으면 exit 1. 브라우저(크로미움)가 없으면 브라우저 시험만 skip.
"""
import datetime as dt
import functools
import glob
import hashlib
import http.server
import io
import json
import os
import re
import shutil
import socketserver
import sqlite3
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


def real_period():
    """실제 data/2026-09 키워드.csv 첫 줄 헤더의 기간(시작, 끝) — 이번 달 파일이 갱신될 때마다 시험이 깨지지 않게
    기대 기간을 고정값이 아니라 헤더에서 읽는다(이월 ②, 2026-09-28 Code 탭 회차)."""
    head = F.read_report(os.path.join(DATA, "키워드.csv"))[0]
    g = [int(x) for x in F.HEAD_RE.search(head).groups()[:6]]
    return D(g[0], g[1], g[2]), D(g[3], g[4], g[5])


def rf_for(list_url, download_dir, profile_dir, **over):
    """실제 config 의 report_fetch + 시험 덮어쓰기. 추가 수집(extras — 2026-10-12)은 기본으로 뺀다(실제 config 의 history.url 은 광고주센터 —
    시험은 네트워크 0) — 추가 수집 시험은 extras=<가짜 화면을 가리키는 블록> 을 넘긴다(ExtrasBrowserTests)."""
    with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    base = {k: v for k, v in cfg["report_fetch"].items() if k != "extras"}
    cfg["report_fetch"] = {**base, "list_url": list_url, "download_dir": download_dir, "profile_dir": profile_dir,
                           "browser_channel": None, "timeout_sec": {"page": 8, "download": 20, "login": 20}, "settle_sec": 0.2, **over}
    return F.fetch_config(cfg)


def make_history(path, targets):
    """가짜 크롬 History DB — downloads(id, target_path)·downloads_url_chains(id, chain_index, url)·downloads_slices(download_id, …)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path)
    try:
        con.execute("CREATE TABLE downloads (id INTEGER PRIMARY KEY, guid VARCHAR NOT NULL, current_path LONGVARCHAR NOT NULL, target_path LONGVARCHAR NOT NULL)")
        con.execute("CREATE TABLE downloads_url_chains (id INTEGER NOT NULL, chain_index INTEGER NOT NULL, url LONGVARCHAR NOT NULL, PRIMARY KEY (id, chain_index))")
        con.execute("CREATE TABLE downloads_slices (download_id INTEGER NOT NULL, offset INTEGER NOT NULL, received_bytes INTEGER, finished INTEGER DEFAULT 0, PRIMARY KEY (download_id, offset))")
        for i, t in enumerate(targets, 1):
            con.execute("INSERT INTO downloads VALUES (?, ?, ?, ?)", (i, f"guid-{i}", t, t))
            con.execute("INSERT INTO downloads_url_chains VALUES (?, 0, ?)", (i, f"http://127.0.0.1/{i}.csv"))
            con.execute("INSERT INTO downloads_url_chains VALUES (?, 1, ?)", (i, f"http://127.0.0.1/{i}-r.csv"))
            con.execute("INSERT INTO downloads_slices VALUES (?, 0, 10, 1)", (i,))
        con.commit()
    finally:
        con.close()


def history_rows(path):
    con = sqlite3.connect(path)
    try:
        return ([r[0] for r in con.execute("SELECT id FROM downloads ORDER BY id")],
                sorted({r[0] for r in con.execute("SELECT id FROM downloads_url_chains")}),
                sorted({r[0] for r in con.execute("SELECT download_id FROM downloads_slices")}))
    finally:
        con.close()


class FakeChromium:
    """launch()가 넘기는 인자만 기록(브라우저 0)."""
    def __init__(self):
        self.calls = []

    def launch_persistent_context(self, profile_dir, **kw):
        self.calls.append(kw)
        return "ctx"


class FakeLocator:
    def __init__(self, text):
        self.text, self.clicked = text, False

    def inner_text(self):
        return self.text

    def click(self, timeout=None):
        self.clicked = True
        self.timeout = timeout


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
                         ["시간대별 보고서,2580077.csv", "상세지역 보고서,2580077.csv", "검색어 보고서,2580077.csv", "필라테스 보고서,2580077.csv"])

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
            self.assertEqual(r.stdout.count("보고서,2580077.csv"), 4)
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
        s, e = real_period()
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
        self.assertEqual(res["키워드"]["dates"][0], s.strftime("%Y.%m.%d."))
        # 기간이 기대와 다르면 FAIL(매월 1일 "1일~말일" 검사도 같은 자리) — 음성 단언: 기대 끝 = 헤더 끝 + 1일
        r = F.check_file(os.path.join(DATA, "키워드.csv"), "필라테스 보고서", "키워드", rf, s, e + dt.timedelta(days=1))
        self.assertFalse(r["ok"])
        self.assertIn("기간 = 기대", [c["name"] for c in r["checks"] if not c["ok"]])
        # 이름이 다르면 FAIL
        r = F.check_file(os.path.join(DATA, "키워드.csv"), "검색어 보고서", "검색어", rf, s, e)
        self.assertFalse(r["ok"])
        # 합성: 행 0 / 컬럼 다름 / 계정 다름 / 헤더 형식 — 합성 파일 헤더와 같은 고정 기간
        ss, se = D(2026, 9, 1), D(2026, 9, 26)
        tmp = tempfile.mkdtemp()
        try:
            def w(name, text):
                p = os.path.join(tmp, name)
                with open(p, "w", encoding="utf-8-sig", newline="") as f:
                    f.write(text)
                return p
            col = rf["columns"]["시간대별"]
            self.assertFalse(F.check_file(w("a.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),2580077"\n{col}\n'), "시간대별 보고서", "시간대별", rf, ss, se)["ok"])
            self.assertFalse(F.check_file(w("b.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),2580077"\n{col},추가열\n00시~01시,1,0,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, ss, se)["ok"])
            self.assertFalse(F.check_file(w("c.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),9999999"\n{col}\n00시~01시,1,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, ss, se)["ok"])
            self.assertFalse(F.check_file(w("d.csv", f'시간대별 보고서 2026-09-01~2026-09-26\n{col}\n00시~01시,1,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, ss, se)["ok"])
            good = F.check_file(w("e.csv", f'"시간대별 보고서(2026.09.01.~2026.09.26.),2580077"\n{col}\n00시~01시,1,0,0,0,0,0,0,0,0\n'), "시간대별 보고서", "시간대별", rf, ss, se)
            self.assertTrue(good["ok"], good["checks"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compare_prev_warns_on_recount(self):
        rf = F.fetch_config(download_dir="/tmp/x", profile_dir="/tmp/y")
        s, e = real_period()
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
            self.assertEqual(detail["키워드"]["common_days"], len(now[0]["by_date"]))  # 행이 있는 날짜 수(같은 파일 사본)
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
        self.assertEqual(ok.timeout, rf["timeout_sec"]["click"] * 1000)  # 클릭 대기 시간은 config timeout_sec.click
        self.assertEqual(F.click_reason(Exception("Locator.click: Timeout 30000ms exceeded.\nCall log:\n  - element is not enabled")), "Exception: 요소 비활성(disabled)")
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

    def test_clean_download_history_removes_only_missing_files(self):
        """결함 1(2회째 실행 크래시): (가) 파일 없는 기록 → 그 행·url_chains·slices 삭제 / (나) 파일 있는 기록 → 그대로(파일도 그대로).
        DB 자리는 Default/History, 없으면 프로필 바로 밑 History."""
        tmp = tempfile.mkdtemp()
        try:
            real = os.path.join(tmp, "받은 파일.csv")
            with open(real, "w", encoding="utf-8") as f:
                f.write("x")
            gone = os.path.join(tmp, "playwright-artifacts-1", "5f0c-guid")  # 이미 지워진 Playwright 임시 파일
            for prof, db in ((os.path.join(tmp, "p1"), os.path.join(tmp, "p1", "Default", "History")),
                             (os.path.join(tmp, "p2"), os.path.join(tmp, "p2", "History"))):
                make_history(db, [gone, real, ""])  # id 1 = (가), 2 = (나), 3 = 경로 빈 기록(파일 없음 → 삭제)
                lines = []
                rec = F.clean_download_history(prof, lines.append)
                self.assertEqual(rec["status"], "ok", rec)
                self.assertEqual(rec["db"], db)
                self.assertEqual((rec["deleted"], rec["chains"], rec["slices"], rec["kept"]), (2, 4, 2, 1), rec)
                self.assertEqual(history_rows(db), ([2], [2], [2]))
                self.assertTrue(os.path.exists(real))
                self.assertEqual(len(lines), 1)
                self.assertIn("파일 없는 기록 2건 삭제", lines[0])
                self.assertIn("실제 파일 있는 기록 1건 유지", lines[0])
                rec2 = F.clean_download_history(prof, lines.append)  # 두 번째는 지울 것이 없다
                self.assertEqual((rec2["status"], rec2["deleted"], rec2["kept"]), ("ok", 0, 1))
                self.assertEqual(history_rows(db), ([2], [2], [2]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_clean_download_history_no_db_or_locked_warns(self):
        """(다) 기록 DB 자체가 없음 → 무동작 WARN(파일·폴더를 만들지 않음) / DB가 잠겨 있음(브라우저가 잡고 있는 상태) → WARN, 아무것도 안 지움."""
        tmp = tempfile.mkdtemp()
        try:
            prof = os.path.join(tmp, "empty")
            os.makedirs(prof)
            lines = []
            rec = F.clean_download_history(prof, lines.append)
            self.assertEqual((rec["status"], rec["deleted"], rec["db"]), ("skip", 0, None))
            self.assertTrue(lines[0].startswith("[WARN]"), lines)
            self.assertIn("없음", lines[0])
            self.assertEqual(os.listdir(prof), [])
            missing = os.path.join(tmp, "없는 프로필")
            self.assertEqual(F.clean_download_history(missing, lines.append)["status"], "skip")
            self.assertFalse(os.path.exists(missing))
            # 잠김: 다른 연결이 쓰기 잠금을 잡고 있으면 [WARN]만, 행은 그대로
            prof2 = os.path.join(tmp, "locked")
            db = os.path.join(prof2, "Default", "History")
            make_history(db, [os.path.join(tmp, "없는 파일.csv")])
            holder = sqlite3.connect(db, isolation_level=None)
            try:
                holder.execute("BEGIN EXCLUSIVE")
                lines = []
                rec = F.clean_download_history(prof2, lines.append)
            finally:
                holder.close()
            self.assertEqual((rec["status"], rec["deleted"]), ("skip", 0), rec)
            self.assertTrue(lines[0].startswith("[WARN]"), lines)
            self.assertIn("잠김", lines[0])
            self.assertEqual(history_rows(db), ([1], [1], [1]))
            # 브라우저가 떠 있다는 표시(SingletonLock)가 있으면 DB를 열지도 않는다
            if hasattr(os, "symlink"):
                try:
                    os.symlink("host-123", os.path.join(prof2, "SingletonLock"))
                except OSError:
                    pass
                else:
                    lines = []
                    self.assertEqual(F.clean_download_history(prof2, lines.append)["status"], "skip")
                    self.assertIn("브라우저가 떠 있음", lines[0])
                    self.assertEqual(history_rows(db), ([1], [1], [1]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_launch_channel_respects_config(self):
        """② config browser_channel 그대로: null → channel 인자 없음(번들 크로미움), "chrome" → channel="chrome"(설치된 크롬)."""
        tmp = tempfile.mkdtemp()
        try:
            for value, want_channel, want_name in ((None, None, "chromium"), ("chrome", "chrome", "chrome")):
                rf = rf_for("http://127.0.0.1/x", os.path.join(tmp, "dl"), os.path.join(tmp, "prof"), browser_channel=value)
                fake = FakeChromium()
                ctx, name = F.launch(type("P", (), {"chromium": fake})(), rf, headless=True)
                self.assertEqual((ctx, name), ("ctx", want_name))
                self.assertEqual(fake.calls[0].get("channel"), want_channel)
            with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["report_fetch"]["browser_channel"], "chrome")  # 실사용 값은 설치 크롬 유지
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


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
        self.assertEqual(files, sorted(["시간대별 보고서,2580077.csv", "상세지역 보고서,2580077.csv", "검색어 보고서,2580077.csv", "필라테스 보고서,2580077.csv"]))
        self.assertTrue(os.path.exists(os.path.join(day, "summary.json")))
        self.assertTrue(os.path.isdir(os.path.join(day, "debug")))
        self.assertFalse(os.path.exists(os.path.join(dl, "partial", "2026-09-28")))
        summ = load_json(os.path.join(day, "summary.json"))
        self.assertEqual(summ["result"], "ok")
        self.assertEqual(summ["expected"], {"preset": "이번달", "start": "2026.09.01.", "end": "2026.09.27."})
        self.assertTrue(summ["cross"]["ok"])
        self.assertEqual([w for w in summ["warnings"] if "파일명" in w], [])  # 실측 이름은 WARN 대상이 아니다
        for r in summ["reports"]:
            self.assertEqual(r["status"], "ok", r)
            self.assertFalse(r["preset_clicked"])  # 저장된 `이번달`이라 프리셋 클릭 없음
            self.assertEqual(r["check"]["period"], ["2026.09.01.", "2026.09.27."])
        with open(os.path.join(day, "필라테스 보고서,2580077.csv"), "rb") as f:
            raw = f.read()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\n", raw)
        head, colline, rows, _ = F.read_report(os.path.join(day, "필라테스 보고서,2580077.csv"))
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
        p = os.path.join(tampered, "검색어 보고서,2580077.csv")
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
        self.assertNotIn("검색어 보고서,2580077.csv", files)
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
        rf = rf_for(self.srv.url("auto=1&today=2026-09-28&noperiod=" + "시간대별 보고서"), dl, prof, timeout_sec={"page": 3, "download": 10, "login": 20, "click": 3})
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), debug=True, headless=True)
        self.assertEqual(code, 2, out)
        stage = os.path.join(dl, "partial", "2026-09-28")
        files = sorted(f for f in os.listdir(stage) if f.endswith(".csv"))
        self.assertEqual(files, sorted(["상세지역 보고서,2580077.csv", "검색어 보고서,2580077.csv", "필라테스 보고서,2580077.csv"]))
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

    def test_6_query_button_disabled_when_already_queried(self):
        """왕복 2 재현: 저장된 형식으로 열면 자동 조회되고 `조회하기`가 비활성 → 건너뛰고 다운로드. 1일엔 프리셋 `확인` 뒤 활성 → 클릭."""
        dl, prof = os.path.join(self.tmp, "dl6"), os.path.join(self.tmp, "prof6")
        rf = rf_for(self.srv.url("auto=1&today=2026-09-28&query=disabled"), dl, prof, timeout_sec={"page": 8, "download": 20, "login": 20, "click": 3})
        code, out = self.run_quiet(F.cmd_login, rf, headless=True)
        self.assertEqual(code, 0, out)
        code, out = self.run_quiet(F.cmd_fetch, rf, D(2026, 9, 28), headless=True)
        self.assertEqual(code, 0, out)
        self.assertNotIn("클릭 query:", out)
        summ = load_json(os.path.join(dl, "2026-09-28", "summary.json"))
        for r in summ["reports"]:
            self.assertEqual(r["status"], "ok", r)
            self.assertFalse(r["queried"])
            self.assertTrue(any("조회하기 비활성" in st for st in r["steps"]), r["steps"])
        rf1 = rf_for(self.srv.url("auto=1&today=2026-10-01&query=disabled"), dl, prof, timeout_sec={"page": 8, "download": 20, "login": 20, "click": 3})
        code, out = self.run_quiet(F.cmd_fetch, rf1, D(2026, 10, 1), headless=True)
        self.assertEqual(code, 0, out)
        self.assertEqual(out.count("클릭 query:"), 4)
        summ1 = load_json(os.path.join(dl, "2026-10-01", "summary.json"))
        for r in summ1["reports"]:
            self.assertTrue(r["queried"], r)
            self.assertEqual(r["check"]["period"], ["2026.09.01.", "2026.09.30."])

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


# ---------------------------------------------------------------- 추가 수집(보고서 더 받기 A + B, 2026-10-12)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xlsxfix  # noqa: E402


def extras_block(srv_url_history, **over):
    """실제 config 의 extras 를 바탕으로 history.url 만 가짜 화면으로(같은 출처) — 그 밖 값(이름·종류·columns·actor_rules)은 실제 그대로."""
    with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
        ex = json.load(f)["report_fetch"]["extras"]
    ex = json.loads(json.dumps(ex))
    ex["history"]["url"] = srv_url_history
    for k, v in over.items():
        ex[k] = v
    return ex


class ExtrasConfigTests(unittest.TestCase):
    """완료 기준 7 · 8 · 16 — 설정 오류는 추가만 끔(SystemExit 0) · 클릭·goto 자리 · dry-run 쓰기 0."""

    def cfg_with(self, mutate):
        with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        mutate(cfg["report_fetch"]["extras"], cfg)
        return cfg

    def test_real_config_extras_valid(self):
        rf = F.fetch_config(download_dir="/tmp/x", profile_dir="/tmp/y")
        self.assertIsNotNone(rf["extras"])
        self.assertEqual(rf["extras_warn"], [])
        self.assertEqual({s["kind"] for s in rf["extras"]["reports"].values()}, {"성별", "연령대"})
        self.assertEqual(rf["extras"]["history"]["url"], "https://ads.naver.com/manage/ad-accounts/2580077/sa/tool/history")
        self.assertEqual(list(rf["report_names"]), ["시간대별 보고서", "상세지역 보고서", "검색어 보고서", "필라테스 보고서"])   # 4개 그대로

    def test_bad_extras_turn_off_only_extras(self):
        cases = {
            "이름이 4개와 겹침": lambda ex, c: ex["reports"].update({"검색어 보고서": dict(ex["reports"]["성별 보고서"], kind="성별2")}),
            "종류가 4개와 겹침": lambda ex, c: ex["reports"]["성별 보고서"].update(kind="키워드"),
            "종류 접두(키워드요일)": lambda ex, c: ex["reports"]["성별 보고서"].update(kind="키워드요일"),
            "종류끼리 접두": lambda ex, c: ex["reports"]["연령대 보고서"].update(kind="성별연령"),
            "이름에 금지 낱말": lambda ex, c: ex["reports"].update({"성별 삭제 보고서": ex["reports"].pop("성별 보고서")}),
            "columns 없음": lambda ex, c: ex["reports"]["성별 보고서"].pop("columns"),
            "URL 없음": lambda ex, c: ex["history"].pop("url"),
            "URL 쿼리": lambda ex, c: ex["history"].update(url=ex["history"]["url"] + "?startDate=2026-09-01"),
            "URL 다른 출처": lambda ex, c: ex["history"].update(url="https://example.com/manage/history"),
            "actor_rules 꼴": lambda ex, c: ex["history"].update(actor_rules="SYSTEM"),
            "블록이 객체 아님": lambda ex, c: c["report_fetch"].update(extras=["x"]),
        }
        for label, mut in cases.items():
            with self.subTest(label=label):
                cfg = self.cfg_with(mut)
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rf = F.fetch_config(cfg)          # SystemExit 0 — 4개 설정은 그대로 읽힌다
                self.assertIsNone(rf["extras"])
                self.assertEqual(len(rf["extras_warn"]), 1)
                self.assertTrue(rf["extras_warn"][0].startswith("[주의] extras 설정:"), rf["extras_warn"])
                self.assertIn("[주의] extras 설정:", buf.getvalue())
                self.assertEqual(len(rf["report_names"]), 4)
        cfg = self.cfg_with(lambda ex, c: c["report_fetch"].pop("extras"))   # 블록 없음 = 지금과 같음(경고 0)
        rf = F.fetch_config(cfg)
        self.assertEqual((rf["extras"], rf["extras_warn"]), (None, []))

    def test_s0_profile_snippet_survives_bad_extras(self):
        """S0 블록(code-tab.md 2절)의 `fetch_config()` 줄 — extras 가 틀려도 SystemExit 하지 않는다(rc 0, [주의] 줄)."""
        tmp = tempfile.mkdtemp()
        try:
            shutil.copytree(os.path.join(ROOT, "scripts"), os.path.join(tmp, "scripts"), ignore=shutil.ignore_patterns("__pycache__"))
            os.makedirs(os.path.join(tmp, "config"))
            cfg = self.cfg_with(lambda ex, c: ex["reports"]["성별 보고서"].update(kind="키워드"))
            with open(os.path.join(tmp, "config", "report-config.json"), "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False)
            r = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0,'scripts'); import fetch_reports as R; "
                                "sys.exit(3 if R.profile_in_use(R.fetch_config()['profile_dir']) else 0)"],
                               capture_output=True, text=True, encoding="utf-8", cwd=tmp, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("[주의] extras 설정:", r.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_clicks_and_goto_only_config(self):
        with open(os.path.join(ROOT, "scripts", "fetch_reports.py"), encoding="utf-8") as f:
            src = f.read()
        self.assertEqual(src.count(".click("), 1)                                    # 클릭 호출 1곳(변경 이력 화면도 click_allowed)
        gotos = re.findall(r"page\.goto\(([^)]*)\)", src.split('"""', 2)[2])        # 머리말 밖
        self.assertTrue(gotos)
        for arg in gotos:
            self.assertIn(arg, ('rf["list_url"]', 'h["url"]', "config history.url"), arg)
        self.assertNotIn("Shot(", src[src.index("def fetch_history"):src.index("def run_extras")])   # B 단계 스크린샷 0(B-5)

    def test_dry_run_extras_rows_and_no_writes(self):
        """완료 기준 16 — 할 일 표에 추가 줄(이름·종류·오늘 받나·저장 위치·보관 끝·원장 마지막 날·기록 구간 끝) · 브라우저 0 · 폴더 0 · 보관·원장 md5 전후 같음."""
        tmp = tempfile.mkdtemp()
        try:
            arch, led = os.path.join(tmp, "arch"), os.path.join(tmp, "hist", "ledger.csv")
            os.makedirs(os.path.join(arch, "2026-09"))
            with open(os.path.join(arch, "2026-09", "성별.csv"), "w", encoding="utf-8-sig", newline="") as f:
                f.write('"성별 보고서(2026.09.01.~2026.09.27.),2580077"\nx\n')
            import extras as X
            X.merge_history([("2026.09.20. 15:30", "광고그룹 변경", "사람", "플레이스#1", "새로필라테스", "x\n변경 전\n하루예산: 1원\n변경 후\n하루예산: 2원")],
                            D(2026, 8, 30), D(2026, 9, 28), led, "시험", log=lambda *_: None)
            before = {p: md5f(p) for p in (led, X.covered_path(led), os.path.join(arch, "2026-09", "성별.csv"))}
            listing = sorted(os.listdir(tmp))
            fake = os.path.join(tmp, "fakepw", "playwright")
            os.makedirs(fake)
            with open(os.path.join(fake, "__init__.py"), "w") as f:
                f.write("raise ImportError('dry-run must not import playwright')\n")
            env = {**os.environ, "PYTHONPATH": os.path.join(tmp, "fakepw"), "PYTHONIOENCODING": "utf-8", "SAERO_EXTRA_ARCHIVE": arch, "SAERO_LEDGER": led}
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "fetch_reports.py"), "--dry-run", "--today", "2026-09-28",
                                "--download-dir", os.path.join(tmp, "dl"), "--profile-dir", os.path.join(tmp, "prof")],
                               capture_output=True, text=True, encoding="utf-8", env=env, cwd=tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(r.stdout.count("보고서,2580077.csv"), 4)                 # 4개 줄 그대로(추가 줄은 그 글자를 안 씀)
            self.assertIn("| A1 | 성별 보고서 | 성별 | 예(매일", r.stdout)
            self.assertIn("보관 끝 2026.09.27.", r.stdout)
            self.assertIn("| A2 | 연령대 보고서 | 연령대 |", r.stdout)
            self.assertIn("보관본 없음", r.stdout)
            self.assertIn("| B | 변경 이력(", r.stdout)
            self.assertIn("원장 1줄 · 마지막 날 2026.09.20. · 기록 구간 끝 2026.09.27.", r.stdout)
            self.assertIn(os.path.join(tmp, "dl", "partial", "2026-09-28") + "-extra", r.stdout)
            self.assertEqual(sorted(os.listdir(tmp)), sorted(listing + ["fakepw"]))   # dl·prof 안 생김
            self.assertEqual({p: md5f(p) for p in before}, before)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class CtxCloseRaises:
    """launch() 가 돌려준 진짜 context 를 감싸 close() 가 (진짜로 닫은 뒤) 예외를 내게 한다 — A-3 시험."""
    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, k):
        return getattr(self._ctx, k)

    def close(self):
        self._ctx.close()
        raise RuntimeError("닫기 시험 예외")


@unittest.skipUnless(browser_available(), "playwright/크로미움 없음 — 브라우저 시험 skip")
class ExtrasBrowserTests(unittest.TestCase):
    """완료 기준 1·2·3·4·8·11·24·25·26·29·31 — 가짜 화면(목록 extra=1 · 변경 이력 history-fixture.html · 가짜 엑셀)으로 4개 + 추가 수집."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.fix = os.path.join(cls.tmp, "fix")
        shutil.copytree(FIX, cls.fix)
        xlsxfix.write_xlsx(os.path.join(cls.fix, "history-sample.xlsx"), xlsxfix.SAMPLE)
        bad = list(xlsxfix.HEADER)
        bad[2] = "변경한 사람"                                                       # 머리줄 하나 다름(셀 원문이 메시지에 실리면 안 됨)
        xlsxfix.write_xlsx(os.path.join(cls.fix, "history-badhead.xlsx"), xlsxfix.SAMPLE, header=bad)
        handler = functools.partial(QuietHandler, directory=cls.fix)
        cls.httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
        cls.port = cls.httpd.server_address[1]
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def url(self, page, query):
        return f"http://127.0.0.1:{self.port}/{page}?{query}"

    def rf(self, tag, list_q="", hist_q="", **over):
        dl, prof = os.path.join(self.tmp, "dl" + tag), os.path.join(self.tmp, "prof")
        q = "auto=1&today=2026-09-28&extra=1" + ("&" + list_q if list_q else "") + ("&" + hist_q if hist_q else "")   # 변경 이력 화면 설정도 목록 주소에(그 화면은 쿼리 없는 주소)
        ex = extras_block(f"http://127.0.0.1:{self.port}/history-fixture.html")
        to = {"page": 6, "download": 6, "login": 20, "click": 3}
        return rf_for(self.url("report-ui-fixture.html", q), dl, prof, extras=ex, timeout_sec=to, **over), dl

    def run_fetch(self, rf):
        buf = io.StringIO()
        with redirect_stdout(buf):
            if not os.path.isdir(os.path.join(self.tmp, "prof", "Default")):
                F.cmd_login(rf, headless=True)
            code = F.cmd_fetch(rf, D(2026, 9, 28), headless=True)
        return code, buf.getvalue()

    def four_ok(self, dl, code, out):
        """기존 시험(test_1)의 4개 성공 단언 그대로 — 추가 수집이 무엇을 하든 같아야."""
        self.assertEqual(code, 0, out)
        day = os.path.join(dl, "2026-09-28")
        files = sorted(f for f in os.listdir(day) if f.endswith(".csv"))
        self.assertEqual(files, sorted(["시간대별 보고서,2580077.csv", "상세지역 보고서,2580077.csv", "검색어 보고서,2580077.csv", "필라테스 보고서,2580077.csv"]))
        self.assertFalse(os.path.exists(os.path.join(dl, "partial", "2026-09-28")))   # A-2 — 4개 partial 이 되살아나지 않음(test_fetch_reports.py:442 기대값)
        summ = load_json(os.path.join(day, "summary.json"))
        self.assertEqual((summ["result"], summ["exit_code"]), ("ok", 0))
        self.assertEqual([r["status"] for r in summ["reports"]], ["ok"] * 4)
        self.assertNotIn("extras", summ)                                                # 4개 summary 꼴 그대로
        first_pass = out.index("[PASS] 4개 다운로드·검사 통과")
        self.assertIn("다음: Code 탭 1단계", out[first_pass:out.index("\n", out.index("다음: Code 탭 1단계", first_pass))])
        self.assertLess(first_pass, out.find("[추가]") if "[추가]" in out else len(out))   # 공통 안전망 — 4개 이동·summary·PASS 줄이 추가 수집보다 먼저(기준 3)
        return day

    def tail_lines_ok(self, out):
        """A-4 — 첫 `다음:` 줄 뒤 ~ 끝 `[PASS] 4개 … · 추가:` 줄 앞은 전부 `[추가]` 머리(SystemExit 의 `[FAIL]` 을 옮기지 않음) · 끝 줄 다시."""
        lines = out.splitlines()
        i = next(k for k, l in enumerate(lines) if l.startswith("다음: Code 탭 1단계"))
        j = next(k for k, l in enumerate(lines) if l.startswith("[PASS] 4개 다운로드·검사 통과") and " · 추가: " in l)
        mid = [l for l in lines[i + 1:j] if l.strip()]
        self.assertTrue(mid)
        for l in mid:
            self.assertTrue(l.startswith("[추가]"), l)
        self.assertNotIn("[FAIL]", "\n".join(lines[i + 1:]))
        self.assertTrue(lines[j + 1].startswith("다음: Code 탭 1단계") and "extras.py store" in lines[j + 1], lines[j + 1])
        return lines[j]

    def no_id(self, root):
        """기준 11 — 아이디(가짜 tester01)·`:naver` 가 받은 폴더 어디에도 없음(정리본·summary_extra·로그) · 엑셀 원본 0."""
        for dp, _, fns in os.walk(root):
            for fn in fns:
                self.assertFalse(fn.endswith(".xlsx"), os.path.join(dp, fn))
                if fn.endswith((".csv", ".json", ".txt")):
                    with open(os.path.join(dp, fn), "rb") as f:
                        b = f.read()
                    self.assertNotIn(xlsxfix.FAKE.encode(), b, fn)
                    self.assertNotIn(b":naver", b, fn)

    def test_x1_success_then_store_combine(self):
        rf, dl = self.rf("1")
        code, out = self.run_fetch(rf)
        day = self.four_ok(dl, code, out)
        final = self.tail_lines_ok(out)
        self.assertIn("· 추가: 성별 받음 · 연령대 받음 · 변경이력 받음", final)
        xdir = os.path.join(day, "extra")
        self.assertEqual(sorted(os.listdir(xdir)), sorted(["성별 보고서,2580077.csv", "연령대 보고서,2580077.csv", "변경이력.csv", "summary_extra.json"]))
        self.assertFalse(os.path.exists(os.path.join(dl, "partial", "2026-09-28-extra")))   # 다 통과하면 추가 임시 폴더도 지움
        self.assertEqual(sorted(glob.glob(os.path.join(day, "*.csv"))), sorted(os.path.join(day, f) for f in os.listdir(day) if f.endswith(".csv")))
        self.assertEqual(len(glob.glob(os.path.join(day, "*.csv"))), 4)                # 기준 4 — ingest.sh "<성공 폴더>"/*.csv 는 4개뿐(추가는 하위 폴더)
        sx = load_json(os.path.join(xdir, "summary_extra.json"))
        self.assertEqual([r["status"] for r in sx["reports"]], ["ok", "ok"])
        self.assertEqual(sx["history"]["status"], "ok")
        self.assertEqual(sx["history"]["rows"], len(xlsxfix.SAMPLE))
        self.assertEqual(sx["history"]["actors"], {"사람": 4, "스킬": 3, "시스템": 1})
        self.assertIsNone(sx["blocked"])
        self.assertEqual(sx["reports"][0]["check"]["period"], ["2026.09.01.", "2026.09.27."])
        self.no_id(dl)
        import extras as X
        first, cols, rows = X.read_table(os.path.join(xdir, "변경이력.csv"))
        self.assertEqual(first, '"변경이력(2026.08.30.~2026.09.28.),2580077"')
        self.assertEqual(cols, X.LEDGER_COLS)
        sysrow = [r for r in rows if r[2] == "시스템"][0]
        self.assertEqual((sysrow[3], sysrow[4]), ("", ""))                              # B-8 — 셀 빠진 SYSTEM 줄의 내용이 캠페인 칸으로 밀리지 않음
        self.assertTrue(sysrow[5].startswith("새로필라테스\n설정 값"))
        self.assertIn([r for r in rows if r[4] == " 새로필라테스 "][0][5].split("\n")[1], ("변경 전",))   # 앞뒤 공백 칸 그대로
        # 1x — 보관·원장(스크래치 경로) · 같은 폴더 두 번 = 원장 +0 · 저장소 작업 트리 변경 0(기준 6)
        arch, led = os.path.join(self.tmp, "x1arch"), os.path.join(self.tmp, "x1hist", "ledger.csv")
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "SAERO_EXTRA_ARCHIVE": arch, "SAERO_LEDGER": led}
        git0 = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
        for n in (1, 2):
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "extras.py"), "store", xdir], capture_output=True, text=True, encoding="utf-8", env=env)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("환경 변수 SAERO_EXTRA_ARCHIVE 로 덮어씀", r.stdout)
            self.assertIn(f"[원장] +{len(xlsxfix.SAMPLE) if n == 1 else 0}줄", r.stdout)
        self.assertTrue(os.path.exists(os.path.join(arch, "2026-09", "성별.csv")))
        self.assertEqual(sorted(os.listdir(os.path.join(arch, "2026-09"))), ["성별.csv", "연령대.csv"])   # 같은 바이트 재보관은 .bak 0
        out_dir = os.path.join(self.tmp, "x1work", "extra")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "extras.py"), "combine", "--out", out_dir], capture_output=True, text=True, encoding="utf-8", env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sorted(os.listdir(out_dir)), sorted(["성별.csv", "연령대.csv", "변경이력.csv", "변경이력_기록구간.csv"]))
        self.assertEqual(X.read_head(os.path.join(out_dir, "성별.csv"))[0], '"성별 합본(2026.09.01.~2026.09.27.),2580077"')
        self.assertEqual(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout, git0)
        self.no_id(os.path.join(self.tmp, "x1hist"))

    def test_x2_failures_isolated(self):
        """기준 2 — 링크 없음 · 2행 컬럼 다름 · 다운로드 안 됨 이 한 실행에: 4개 그대로 · exit 0 · 검사 못 넘은 파일은 partial/<날짜>-extra/ 에만."""
        rf, dl = self.rf("2", "xnolink=성별 보고서&xbad=연령대 보고서", "hnodl=1")
        code, out = self.run_fetch(rf)
        day = self.four_ok(dl, code, out)
        final = self.tail_lines_ok(out)
        self.assertIn("성별 실패(목록에 보고서 링크 '성별 보고서' 없음)", final)
        self.assertIn("연령대 실패(", final)
        self.assertIn("변경이력 실패(다운로드가 시작되지 않음", final)
        sx = load_json(os.path.join(day, "extra", "summary_extra.json"))
        self.assertEqual([r["status"] for r in sx["reports"]], ["fail", "fail"])
        self.assertIn("컬럼 원문 '다름:", sx["reports"][1]["error"])                   # 2행 = config 원문 정확 일치(kind_by_columns 안 씀)
        self.assertIn("[추가] [연령대] FAIL 2행 컬럼", out)
        self.assertEqual(sorted(os.listdir(os.path.join(day, "extra"))), sorted(["summary_extra.json", "debug"]))   # 통과 0 → 파일 0(실패 컷만)
        self.assertEqual(sorted(f for f in os.listdir(os.path.join(dl, "partial", "2026-09-28-extra")) if f.endswith(".csv")), ["연령대 보고서,2580077.csv"])

    def test_x3_forbidden_blocks_extras_only(self):
        """기준 2·8 — 추가 화면의 금지 문구 요소 → 클릭 0 · SystemExit 는 추가만 멈춤(나머지 건너뜀) · exit 0 · `[FAIL]` 줄 0."""
        rf, dl = self.rf("3", "xforbid=성별 보고서")
        code, out = self.run_fetch(rf)
        day = self.four_ok(dl, code, out)
        final = self.tail_lines_ok(out)
        self.assertIn("차단(금지 요소 클릭 시도 차단", final)
        sx = load_json(os.path.join(day, "extra", "summary_extra.json"))
        self.assertIn("금지 요소 클릭 시도 차단", sx["blocked"])
        self.assertEqual([r["status"] for r in sx["reports"]], ["skip", "skip"])   # 차단 뒤엔 클릭 0 — 연령대·변경 이력 건너뜀
        self.assertEqual(sx["history"]["status"], "skip")

    def test_x4_history_bad_header_old_period_dup(self):
        """기준 29·B-9 — 엑셀 머리줄 다름(메시지에 셀 원문 0) · 화면 기간 끝 ≠ 오늘 · `다운로드` 후보 2개 — 셋 다 B 만 실패."""
        for tag, hq, frag in (("4a", "hxlsx=history-badhead.xlsx", "엑셀 머리줄이 config history.columns 와 다름"),
                              ("4b", "hold=1", "끝이 오늘 2026.09.28. 이 아님"),
                              ("4c", "hdup=1", "후보 2개")):
            with self.subTest(tag=tag):
                rf, dl = self.rf(tag, "", hq)
                code, out = self.run_fetch(rf)
                day = self.four_ok(dl, code, out)
                final = self.tail_lines_ok(out)
                self.assertIn("성별 받음 · 연령대 받음 · 변경이력 실패(", final)
                sx = load_json(os.path.join(day, "extra", "summary_extra.json"))
                self.assertIn(frag, sx["history"]["error"])
                with open(os.path.join(day, "extra", "summary_extra.json"), encoding="utf-8") as f:
                    self.assertNotIn("변경한 사람", f.read())                       # 머리줄 셀 원문이 요약에 실리지 않음
                self.no_id(dl)

    def test_x5_browser_dies_and_close_raises(self):
        """기준 2·25(A-3) — 변경 이력 단계에서 페이지가 닫히고 예외 → 추가만 멈춤 · ctx.close() 예외는 `[주의]` 만 · exit 0 · 4개 그대로."""
        rf, dl = self.rf("5")
        real_hist, real_launch = F.fetch_history, F.launch

        def dying(page, *a, **k):
            page.close()
            raise RuntimeError("브라우저가 꺼짐(시험)")
        F.fetch_history = dying
        F.launch = lambda p, rf_, headless=False: (lambda r: (CtxCloseRaises(r[0]), r[1]))(real_launch(p, rf_, headless))
        try:
            code, out = self.run_fetch(rf)
        finally:
            F.fetch_history, F.launch = real_hist, real_launch
        day = self.four_ok(dl, code, out)
        self.assertIn("변경이력 실패(RuntimeError: 브라우저가 꺼짐(시험))", out)
        self.assertIn("[주의] 브라우저 닫기 예외(RuntimeError: 닫기 시험 예외) — 4개 결과·종료 코드는 그대로", out)
        sx = load_json(os.path.join(day, "extra", "summary_extra.json"))
        self.assertEqual([r["status"] for r in sx["reports"]], ["ok", "ok"])


if __name__ == "__main__":
    ok = False
    try:
        r = unittest.main(exit=False, verbosity=2)
        ok = r.result.wasSuccessful()
    finally:
        after = real_md5s()
        print(f"실제 data/2026-09·config md5 전/후 동일: {after == BEFORE} ({BEFORE['config'][:8]} 등)")
    sys.exit(0 if ok and after == BEFORE else 1)   # 실패하면 rc ≠ 0(수정 회차 4 X12 — 종전엔 exit=False라 늘 0)
