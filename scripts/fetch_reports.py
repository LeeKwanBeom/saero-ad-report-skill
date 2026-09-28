#!/usr/bin/env python3
"""네이버 광고주센터 다차원 보고서 4개 자동 다운로드 + 검사 — 1단계 "CSV 받기"의 수동 부분(PC 전용, Playwright).

흐름(설계안 C, 2026-09-28 탐색 기준선 6-6): 목록 URL → 보고서 링크를 이름으로 클릭 → 기간 텍스트 읽기 → 기대 범위와
다르면 프리셋(`이번달`/`지난달`) 클릭 → `확인` → 다시 읽어 기대와 같은지 확인 → `조회하기` → `다운로드`(download 이벤트)
→ 저장 → `돌아가기`. 4개 반복 → 파일마다 검사 → 4개 교차 검사 → summary.json.

모드(전부 저장소 루트에서, PC PowerShell):
    python scripts\\fetch_reports.py --dry-run            브라우저 0. 할 일 표(보고서 4개·기대 기간·저장 경로)만 출력, 파일·폴더 변경 0.
    python scripts\\fetch_reports.py --login              전용 크롬 프로필로 창을 띄우고 사용자가 직접 로그인('로그인 상태 유지')할
                                                         때까지 기다린 뒤 목록 URL 도달을 확인하고 닫는다. 폼 입력 0.
    python scripts\\fetch_reports.py [--prev <폴더>] [--debug]   기본 실행: 4개 다운로드 + 검사.
        --prev   직전 4개 폴더(또는 저장소 data/YYYY-MM)와 겹치는 날짜의 일별 노출·클릭·비용을 비교, 다르면 WARN(막지 않음).
        --debug  단계마다 스크린샷을 저장 폴더 debug/ 에 남긴다.
        --today YYYY-MM-DD   기대 기간 계산 기준일(시험용. 기본 = KST 오늘).
        --download-dir / --profile-dir   config 값 대신 쓸 경로.

결과: 성공이면 <download_dir>/<YYYY-MM-DD>/ 에 원본 이름 그대로 4개 + summary.json (exit 0).
      4개 중 하나라도 실패면 받은 파일은 <download_dir>/partial/<YYYY-MM-DD>/ 에만 두고 정상 폴더에는 남기지 않는다 (exit 2).
      로그인 필요·사용법·환경 오류·금지 클릭 시도 차단은 exit 1.
      store 이후(archive.py store → combine → …)는 현재 흐름 그대로 — 사용자가 4개를 세션에 올린다.

규칙(값 정의는 config `report_fetch`, 문서 = `references/report-fetch.md`):
  - 로케이터는 role·text 기준만. 좌표 클릭·키 입력·드래그 0.
  - 클릭은 `click_allowed()` 한 곳에서만 하고, config `allowed_actions` 밖 동작이나 `forbidden_actions` 문구가 든 요소는
    절대 클릭하지 않는다(그 자리에서 멈춘다).
  - 자격 증명·키는 코드·config·로그·summary 어디에도 없다. 로그인은 사용자가 창에서 직접.
  - 헤드리스 안 씀(사용자가 보는 창). 브라우저는 config `browser_channel` 그대로(null = 번들 크로미움, "chrome" = 설치된 크롬 —
    실행이 안 되면 번들 크로미움).
  - 브라우저를 띄우기 전에 프로필 다운로드 기록 중 파일이 없는 행만 지운다(`clean_download_history` — 2회째 실행 크래시, 수정 회차 2).
  - 검사(첫 줄·컬럼·행·노출합)가 전부 통과하기 전에는 store 하지 않는다(부분 실패도 store 금지).
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import sys
import time

try:
    from reportlib import ROOT, load_config
except ImportError as _e:  # 사용자 PC에는 pandas가 없을 수 있다(reportlib이 pandas를 import) — exclusions.py와 같은 폴백
    if getattr(_e, "name", None) not in ("pandas", "reportlib"):
        raise
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_config():
        """reportlib.load_config와 같은 동작(pandas 없는 PC용 사본) — config/report-config.json, 없으면 즉시 종료."""
        cfg = os.path.join(ROOT, "config", "report-config.json")
        try:
            with open(cfg, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise SystemExit(f"설정 파일이 없습니다: {cfg}\n스킬 저장소를 통째로 받았는지 확인하세요.")

try:  # Windows 콘솔 한글
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

KST = dt.timezone(dt.timedelta(hours=9))
HEAD_RE = re.compile(r"\((\d{4})\.(\d{2})\.(\d{2})\.~(\d{4})\.(\d{2})\.(\d{2})\.\)\s*\"?,\s*(\d+)")  # archive.py 51행과 같은 식
DATE_RE = re.compile(r"(\d{4})\.(\d{2})\.(\d{2})\.?")  # 읽기용 — 끝 점은 있어도 없어도(왕복 1: 실물 표기 미확정)
RANGE_RE = re.compile(r"\d{4}\.\d{2}\.\d{2}\.?\s*(?:→|~|-|–|—|>)?\s*\d{4}\.\d{2}\.\d{2}\.?")  # 화살표가 아이콘이면 구분자 없이 붙는다
DATED = ("키워드", "검색어", "상세지역")  # `일별` 컬럼이 있는 종류(시간대별은 없다)
ACTIONS = ("open_report", "open_period", "preset", "confirm", "query", "download", "back")  # 코드가 아는 동작 전부
DEFAULT_TIMEOUTS = {"page": 40, "download": 90, "login": 600, "click": 15}  # click = 클릭 가능(보임·활성·정지)해질 때까지 기다리는 초


# ---------------------------------------------------------------- config·계획
def fetch_config(cfg=None, download_dir=None, profile_dir=None):
    """config `report_fetch` 블록 + CLI 덮어쓰기. 경로는 `~` 확장(Windows는 C:\\Users\\<사용자>)."""
    cfg = cfg if cfg is not None else load_config()
    if "report_fetch" not in cfg:
        raise SystemExit("config/report-config.json에 report_fetch 블록이 없습니다 — 저장소를 최신으로 받았는지 확인")
    rf = dict(cfg["report_fetch"])
    for key in ("list_url", "account_no", "report_names", "columns", "period_rule", "download_dir", "profile_dir",
                "allowed_actions", "forbidden_actions"):
        if key not in rf:
            raise SystemExit(f"config report_fetch.{key} 가 없습니다")
    rf["download_dir"] = os.path.abspath(os.path.expanduser(download_dir or rf["download_dir"]))
    rf["profile_dir"] = os.path.abspath(os.path.expanduser(profile_dir or rf["profile_dir"]))
    rf["account_no"] = str(rf["account_no"])
    rf["timeout_sec"] = {**DEFAULT_TIMEOUTS, **(rf.get("timeout_sec") or {})}
    unknown = [a for a in rf["allowed_actions"] if a not in ACTIONS]
    if unknown:
        raise SystemExit(f"config allowed_actions에 코드가 모르는 동작이 있습니다: {unknown} (아는 동작: {list(ACTIONS)})")
    for name, kind in rf["report_names"].items():
        if kind not in rf["columns"]:
            raise SystemExit(f"config report_names[{name!r}]={kind!r} 의 컬럼 원문이 columns에 없습니다")
    return rf


def today_kst():
    return dt.datetime.now(KST).date()


def expected_period(today, rule):
    """평일 = `이번달`(이번 달 1일~어제), 매월 1일 = `지난달`(지난달 1일~말일). 라벨은 config period_rule."""
    if today.day == 1:
        end = today - dt.timedelta(days=1)
        return rule["day1"], end.replace(day=1), end
    return rule["other"], today.replace(day=1), today - dt.timedelta(days=1)


def short_name(report_name):
    """'시간대별 보고서' → '시간대별'."""
    return report_name[:-len(" 보고서")] if report_name.endswith(" 보고서") else report_name


def expected_filenames(report_name, account_no):
    """네이버가 주는 다운로드 파일명 후보 — 스크립트 실측(왕복 3, 2026-09-28) `<이름>,<계정>.csv`(예 `시간대별 보고서,2580077.csv`)가 첫째,
    손으로 받을 때 보이던 `<보고서명>_보고서_<계정>.csv`(탐색 기준선 ③)가 둘째. 둘 다 정상, 그 밖이면 WARN(내용 검사가 통과하면 그대로 쓴다)."""
    return [f"{report_name},{account_no}.csv", f"{short_name(report_name)}_보고서_{account_no}.csv"]


def fmt(d):
    return d.strftime("%Y.%m.%d.")


def make_plan(rf, today):
    preset, s, e = expected_period(today, rf["period_rule"])
    day_dir = os.path.join(rf["download_dir"], today.isoformat())
    items = []
    for name, kind in rf["report_names"].items():
        names = expected_filenames(name, rf["account_no"])
        items.append({"name": name, "kind": kind, "expected_file": names[0], "expected_files": names, "save_dir": day_dir})
    return {"today": today.isoformat(), "preset": preset, "start": fmt(s), "end": fmt(e),
            "start_date": s, "end_date": e, "day_dir": day_dir,
            "stage_dir": os.path.join(rf["download_dir"], "partial", today.isoformat()), "items": items}


def cmd_dry_run(rf, today):
    """브라우저 0·파일 변경 0 — 할 일 표만."""
    plan = make_plan(rf, today)
    print(f"[dry-run] 브라우저를 열지 않음 · 파일·폴더 변경 0 · 기준일 {plan['today']} (KST)")
    print(f"기대 기간: 프리셋 `{plan['preset']}` = {plan['start']}~{plan['end']} · 계정 {rf['account_no']}")
    print(f"목록 URL: {rf['list_url']}")
    print(f"프로필: {rf['profile_dir']}")
    print(f"저장 폴더: {plan['day_dir']}  (실패 시 {plan['stage_dir']})")
    print("| # | 보고서 | 종류 | 기대 기간 | 저장 파일 |")
    print("|---|---|---|---|---|")
    for i, it in enumerate(plan["items"], 1):
        print(f"| {i} | {it['name']} | {it['kind']} | {plan['start']}~{plan['end']} | {os.path.join(it['save_dir'], it['expected_file'])} |")
    print(f"허용 동작: {', '.join(rf['allowed_actions'].keys())} / 금지 문구 {len(rf['forbidden_actions'])}개 / 자격 증명 입력 0")
    return 0


# ---------------------------------------------------------------- 파일 검사(브라우저 무관)
def read_report(path):
    """네이버 UI CSV: 첫 줄 기간 헤더, 2행 컬럼, 이후 행. utf-8-sig. 반환 (첫 줄, 컬럼 줄 원문, 행 목록(list[list]), crlf 여부)."""
    with open(path, "rb") as f:
        raw = f.read()
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    if len(lines) < 2:
        return (lines[0] if lines else ""), "", [], crlf
    rows = list(csv.reader(lines[2:]))
    rows = [r for r in rows if any(c.strip() for c in r)]
    return lines[0], lines[1], rows, crlf


def kind_by_columns(cols):
    """archive.py kind_of와 같은 규칙(컬럼으로 종류 판별)."""
    s = set(cols)
    if {"광고그룹", "키워드"} <= s:
        return "키워드"
    for k in ("검색어", "상세지역", "시간대별"):
        if k in s:
            return k
    return None


def sums_of(cols, rows):
    """노출·클릭·비용 합계와 (일별 컬럼이 있으면) 날짜별 합계."""
    idx = {c: i for i, c in enumerate(cols)}
    tot = {"노출수": 0, "클릭수": 0, "총비용": 0}
    by_date = {}
    for r in rows:
        vals = {}
        for k in tot:
            try:
                vals[k] = int(float(r[idx[k]])) if idx.get(k) is not None and idx[k] < len(r) and r[idx[k]] != "" else 0
            except ValueError:
                vals[k] = 0
            tot[k] += vals[k]
        if "일별" in idx and idx["일별"] < len(r):
            d = by_date.setdefault(r[idx["일별"]], {"노출수": 0, "클릭수": 0, "총비용": 0})
            for k in vals:
                d[k] += vals[k]
    return tot, by_date


def check_file(path, name, kind, rf, exp_start, exp_end):
    """파일 하나의 검사 — 첫 줄(HEAD_RE·이름·기간=기대·계정) / 2행 컬럼 = config 원문 / 행 0 아님. 반환 dict(ok, checks, …)."""
    out = {"file": path, "name": name, "kind": kind, "checks": [], "ok": True}

    def add(cname, ok, msg):
        out["checks"].append({"name": cname, "ok": bool(ok), "msg": msg})
        if not ok:
            out["ok"] = False

    try:
        head, colline, rows, crlf = read_report(path)
    except (OSError, UnicodeDecodeError) as e:
        add("읽기", False, f"파일을 utf-8로 읽을 수 없음: {e}")
        return out
    out["head"] = head
    out["crlf"] = crlf
    m = HEAD_RE.search(head)
    if not m:
        add("첫 줄 형식", False, f"기간 헤더를 읽을 수 없음(archive.py HEAD_RE) — {head!r}")
        return out
    g = [int(x) for x in m.groups()[:6]]
    s, e, acct = dt.date(*g[:3]), dt.date(*g[3:]), m.group(7)
    out["period"] = [fmt(s), fmt(e)]
    out["account"] = acct
    add("첫 줄 형식", True, head)
    add("첫 줄 이름", head.lstrip('"').startswith(name + "("), f"헤더 이름 ↔ 보고서 {name}")
    add("기간 = 기대", (s, e) == (exp_start, exp_end), f"헤더 {fmt(s)}~{fmt(e)} ↔ 기대 {fmt(exp_start)}~{fmt(exp_end)}")
    add("계정", acct == rf["account_no"], f"헤더 계정 {acct} ↔ config {rf['account_no']}")
    want = rf["columns"][kind]
    add("2행 컬럼", colline == want, f"컬럼 원문 {'일치' if colline == want else '다름: ' + colline!r}")
    cols = colline.split(",")
    add("종류(컬럼)", kind_by_columns(cols) == kind, f"컬럼으로 판별한 종류 {kind_by_columns(cols)} ↔ {kind}")
    add("행 수", len(rows) > 0, f"데이터 {len(rows)}행")
    out["rows"] = len(rows)
    tot, by_date = sums_of(cols, rows)
    out["sums"] = tot
    if kind in DATED and rows:
        dates = sorted(by_date)
        out["dates"] = [dates[0], dates[-1], len(dates)]
        out["by_date"] = by_date
        lo, hi = fmt(s), fmt(e)
        add("일별 ⊂ 헤더", dates[0] >= lo and dates[-1] <= hi, f"일별 {dates[0]}~{dates[-1]}({len(dates)}일) ↔ 헤더 {lo}~{hi}")
    return out


def cross_check(results):
    """4개 뒤: 시간대별·상세지역·키워드 노출합 동일(combine 정합과 같은 식). 검색어는 콘텐츠 지면 미포함이라 비교하지 않는다."""
    by_kind = {r["kind"]: r for r in results if r.get("ok") and r.get("sums")}
    need = ("키워드", "시간대별", "상세지역")
    if not all(k in by_kind for k in need):
        return {"ok": False, "msg": "3종(키워드·시간대별·상세지역)이 다 있어야 노출합을 대조할 수 있음", "values": {}}
    vals = {k: by_kind[k]["sums"]["노출수"] for k in need}
    ok = len(set(vals.values())) == 1
    return {"ok": ok, "values": vals,
            "msg": ("노출합 일치 " if ok else "노출합 불일치(기간이 다르게 받아졌을 수 있음) ") + " · ".join(f"{k} {v:,}" for k, v in vals.items())}


def load_prev(prev_dir):
    """--prev 폴더의 CSV(원본 이름이든 data/의 키워드.csv 이름이든)를 종류별 날짜 합계로."""
    out = {}
    if not os.path.isdir(prev_dir):
        return None
    for fn in sorted(os.listdir(prev_dir)):
        if not fn.lower().endswith(".csv"):
            continue
        p = os.path.join(prev_dir, fn)
        try:
            head, colline, rows, _ = read_report(p)
        except (OSError, UnicodeDecodeError):
            continue
        cols = colline.split(",")
        k = kind_by_columns(cols)
        if not k or k not in DATED:
            continue
        tot, by_date = sums_of(cols, rows)
        out[k] = {"file": fn, "by_date": by_date, "sums": tot}
    return out


def compare_prev(results, prev):
    """재집계 감지: 겹치는 날짜의 일별 노출·클릭·비용이 다르면 WARN(막지 않음)."""
    warns, detail = [], {}
    for r in results:
        k = r.get("kind")
        if k not in DATED or not r.get("by_date") or k not in prev:
            continue
        common = sorted(set(r["by_date"]) & set(prev[k]["by_date"]))
        diffs = []
        for d in common:
            a, b = r["by_date"][d], prev[k]["by_date"][d]
            if any(a[x] != b[x] for x in ("노출수", "클릭수", "총비용")):
                diffs.append({"date": d, "now": a, "prev": b})
        detail[k] = {"prev_file": prev[k]["file"], "common_days": len(common), "diff_days": len(diffs), "diffs": diffs}
        if diffs:
            warns.append(f"[WARN] {k}: 직전({prev[k]['file']})과 겹치는 {len(common)}일 중 {len(diffs)}일의 일별 합계가 다름(재집계 가능성) — "
                         + "; ".join(f"{x['date']} 노출 {x['prev']['노출수']}→{x['now']['노출수']} 클릭 {x['prev']['클릭수']}→{x['now']['클릭수']} "
                                     f"비용 {x['prev']['총비용']}→{x['now']['총비용']}" for x in diffs[:5])
                         + (" …" if len(diffs) > 5 else ""))
        elif not common:
            warns.append(f"[알림] {k}: 직전 파일과 겹치는 날짜가 없어 재집계 비교를 못 함")
    return warns, detail


# ---------------------------------------------------------------- 브라우저(여기서만 Playwright)
def _playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        from playwright.sync_api import TimeoutError as PWTimeout  # noqa: F401
    except ImportError:
        raise SystemExit("playwright가 없습니다 — PC에서 `pip install playwright` 뒤 `python -m playwright install chromium` "
                         "(references/report-fetch.md 1절)")
    return sync_playwright, PWTimeout


def history_db(profile_dir):
    """프로필의 다운로드 기록 DB — `Default/History`, 없으면 profile_dir 바로 밑 `History`. 둘 다 없으면 None."""
    for p in (os.path.join(profile_dir, "Default", "History"), os.path.join(profile_dir, "History")):
        if os.path.isfile(p):
            return p
    return None


def profile_in_use(profile_dir):
    """이 프로필을 쓰는 브라우저가 떠 있는지 — POSIX는 `SingletonLock` 링크, Windows는 크롬이 잡고 있는 `lockfile`(열리지 않음)."""
    if os.path.lexists(os.path.join(profile_dir, "SingletonLock")):
        return True
    lock = os.path.join(profile_dir, "lockfile")
    if os.name == "nt" and os.path.exists(lock):
        try:
            with open(lock, "a"):
                pass
        except OSError:
            return True
    return False


def clean_download_history(profile_dir, log=print):
    """launch() 전 프로필 정리(수정 회차 2, 결함 1): 같은 프로필 2회째 실행부터 다운로드 시작 순간 크롬이 0xC0000005로 죽는다 —
    프로필 다운로드 기록에 이미 지워진 Playwright 임시 파일 경로가 남아 있으면 난다(검증 보고 2026-09-28). 기록 DB(`history_db`)의
    `downloads`에서 **target_path 파일이 없는 행**과 그에 딸린 `downloads_url_chains`(있으면 `downloads_slices`) 행만 지운다.
    실제 파일이 있는 기록은 건드리지 않는다. DB가 없거나·브라우저가 떠 있거나·잠김·오류면 [WARN]만 찍고 계속(아무것도 안 지움).
    반환 dict(status ok/skip, deleted, chains, slices, kept, db, msg)."""
    rec = {"status": "skip", "deleted": 0, "chains": 0, "slices": 0, "kept": 0, "db": None}
    db = history_db(profile_dir)
    if db is None:
        rec["msg"] = f"[WARN] 프로필 정리: 다운로드 기록 DB(Default/History·History)가 없음 — 무동작 ({profile_dir})"
    elif profile_in_use(profile_dir):
        rec["msg"] = f"[WARN] 프로필 정리: 이 프로필을 쓰는 브라우저가 떠 있음 — 정리하지 않고 계속 ({profile_dir})"
    else:
        rec["db"] = db
        try:
            con = sqlite3.connect(db, timeout=1, isolation_level=None)
            try:
                con.execute("BEGIN IMMEDIATE")  # 쓰기 잠금 — 브라우저가 DB를 잡고 있으면 여기서 'database is locked'
                tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
                gone = []
                if "downloads" in tables:
                    for i, target in con.execute("SELECT id, target_path FROM downloads").fetchall():
                        if target and os.path.exists(target):
                            rec["kept"] += 1
                        else:
                            gone.append((i,))
                if gone:
                    if "downloads_url_chains" in tables:
                        rec["chains"] = con.executemany("DELETE FROM downloads_url_chains WHERE id = ?", gone).rowcount
                    if "downloads_slices" in tables:
                        rec["slices"] = con.executemany("DELETE FROM downloads_slices WHERE download_id = ?", gone).rowcount
                    rec["deleted"] = con.executemany("DELETE FROM downloads WHERE id = ?", gone).rowcount
                con.execute("COMMIT")
            finally:
                con.close()  # COMMIT 전에 오류가 나면 닫으면서 되돌린다
            rec["status"] = "ok"
            rec["msg"] = (f"[profile] 다운로드 기록 정리: 파일 없는 기록 {rec['deleted']}건 삭제(url_chains {rec['chains']}건"
                          + (f"·slices {rec['slices']}건" if rec["slices"] else "") + f") · 실제 파일 있는 기록 {rec['kept']}건 유지")
        except sqlite3.Error as e:
            rec["msg"] = f"[WARN] 프로필 정리: 기록 DB 잠김·오류 — 정리하지 않고 계속 ({type(e).__name__}: {e})"
    log(rec["msg"])
    return rec


def launch(p, rf, headless=False):
    """전용 프로필(persistent context). config `browser_channel` 그대로 — null이면 번들 크로미움, "chrome"이면 설치된 크롬
    (실행 실패 시 번들 크로미움). 반환 (context, 브라우저 이름). 프로필 정리(`clean_download_history`)는 호출하는 쪽이 이 앞에서 한다."""
    os.makedirs(rf["profile_dir"], exist_ok=True)
    kwargs = dict(headless=headless, accept_downloads=True)
    if headless:
        kwargs["viewport"] = {"width": 1400, "height": 900}
    else:
        kwargs["no_viewport"] = True  # 실제 창 크기 그대로
        kwargs["args"] = ["--start-maximized"]
    channel = rf.get("browser_channel")  # 수정 회차 2: 전에는 null도 "chrome"으로 바꿔 시험까지 설치 크롬으로 돌았다
    if not channel:
        return p.chromium.launch_persistent_context(rf["profile_dir"], **kwargs), "chromium"
    try:
        return p.chromium.launch_persistent_context(rf["profile_dir"], channel=channel, **kwargs), channel
    except Exception as e:  # 설치된 크롬 없음 등
        print(f"[알림] channel={channel} 실행 실패({type(e).__name__}: {str(e).splitlines()[0][:120]}) → 번들 크로미움으로 재시도")
        return p.chromium.launch_persistent_context(rf["profile_dir"], **kwargs), "chromium"


def current_url(page):
    """브라우저에 물어본 현재 URL. (`page.url`은 sync API에서 다른 호출이 있어야 갱신되므로 폴링에는 쓰지 않는다 — 09-28 시험 실측)"""
    try:
        return page.evaluate("location.href")
    except Exception:
        return page.url


def at_list(page, rf):
    """목록 URL에 있는지(쿼리·해시·끝 슬래시 무시)."""
    cur = current_url(page).split("#")[0].split("?")[0].rstrip("/")
    want = rf["list_url"].split("#")[0].split("?")[0].rstrip("/")
    return cur == want


def wait_until(pred, timeout, step=0.5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if pred():
                return True
        except Exception:
            pass
        time.sleep(step)
    return False


def name_ok(text, label):
    """요소 문구가 라벨과 같은지 — 앞뒤의 기호·공백(`← 돌아가기`·`다운로드 ∨`)만 허용, 다른 글자가 붙으면 다른 요소로 본다.
    (파이썬 정규식으로 판정한다 — Playwright에 regex를 넘기면 JS `\\W`가 한글을 비단어로 취급해 `보고서 형식 저장 ∨`가 `저장`에 걸린다.)"""
    t = " ".join((text or "").split())
    return t == label or re.fullmatch(r"[\W_]*" + re.escape(label) + r"[\W_]*", t) is not None


def locate(page, label, roles=("button", "link"), text_fallback=True):
    """role·text 기준 로케이터 — 보이는 첫 요소. label이 문자열이면 문구 일치(name_ok), 정규식이면 그 패턴. 좌표 없음.
    text_fallback=False면 역할(button·link…)로만 찾는다(제목 h2 같은 글자만 있는 요소를 링크로 오인하지 않게 — 왕복 2 시험)."""
    cands = [page.get_by_role(r, name=label) for r in roles]
    if text_fallback:
        cands.append(page.get_by_text(label))
    for c in cands:
        try:
            n = c.count()
        except Exception:
            continue
        for i in range(min(n, 60)):
            el = c.nth(i)
            try:
                if not el.is_visible():
                    continue
                if isinstance(label, str) and not name_ok(el.inner_text(), label):
                    continue
                return el
            except Exception:
                continue
    return None


def click_reason(ex):
    """Playwright 클릭 예외의 원인을 한 줄로(호출 로그에서 골라냄) — 왕복 2: 첫 줄만 보면 'Timeout'뿐이라 원인을 알 수 없었다."""
    msg = str(ex)
    for marker, why in (("not enabled", "요소 비활성(disabled)"), ("intercepts pointer events", "다른 요소가 가림"),
                        ("not visible", "보이지 않음"), ("not stable", "움직이는 중"), ("detached", "요소가 사라짐")):
        if marker in msg:
            return f"{type(ex).__name__}: {why}"
    return f"{type(ex).__name__}: {msg.splitlines()[0][:160]}"


def click_allowed(action, locator, rf, log=None, timeout=None):
    """**유일한 클릭 자리.** allowed_actions 밖 동작·forbidden_actions 문구가 든 요소는 클릭하지 않고 SystemExit(1).
    timeout(초)은 요소가 클릭 가능해질 때까지 기다리는 시간(없으면 config timeout_sec.click)."""
    if action not in rf["allowed_actions"]:
        raise SystemExit(f"[FAIL] 허용 목록 밖 동작 {action!r} — 클릭하지 않음(config report_fetch.allowed_actions: "
                         f"{list(rf['allowed_actions'])})")
    parts = []
    for getter in (lambda: locator.inner_text(), lambda: locator.get_attribute("aria-label"), lambda: locator.get_attribute("title"),
                   lambda: locator.input_value()):
        try:
            v = getter()
            if v:
                parts.append(str(v).strip())
        except Exception:
            pass
    text = " | ".join(parts)
    for bad in rf["forbidden_actions"]:
        if bad and bad in text:
            raise SystemExit(f"[FAIL] 금지 요소 클릭 시도 차단: 동작 {action} → 요소 문구 {text!r} (forbidden_actions {bad!r}) — "
                             "화면이 바뀐 것 같으니 --debug 스크린샷을 첨부해 주세요")
    if log:
        log(f"클릭 {action}: {text!r}"[:160])
    locator.click(timeout=(timeout if timeout is not None else rf["timeout_sec"]["click"]) * 1000)


def read_period(page):
    """보고서 화면의 기간 → (시작, 끝, 읽은 방법). 못 읽으면 (None, None, 이유). 읽기만 한다(클릭·입력 0).
    ① 기간 텍스트 `YYYY.MM.DD. → YYYY.MM.DD.`(가장 짧은 보이는 요소) ② 날짜 값을 가진 보이는 input 두 개(RangePicker형) ③ 본문 한 줄에 날짜 2개."""
    try:
        cands = page.get_by_text(RANGE_RE)
        best = None
        for i in range(min(cands.count(), 30)):
            el = cands.nth(i)
            try:
                if not el.is_visible():
                    continue
                t = " ".join(el.inner_text().split())
            except Exception:
                continue
            if len(DATE_RE.findall(t)) >= 2 and (best is None or len(t) < len(best)):
                best = t
        if best:
            ds = DATE_RE.findall(best)
            return _d(ds[0]), _d(ds[1]), "range-text"
    except Exception:
        pass
    try:  # ② 값이 날짜인 input(읽기 전용 표시칸·팝업 입력칸) — 한 번의 evaluate로 전부 읽는다
        vals = page.evaluate(
            "() => Array.from(document.querySelectorAll('input')).filter(e => e.offsetWidth || e.offsetHeight || e.getClientRects().length)"
            ".map(e => e.value || '')")
        ds = [DATE_RE.search(v).groups() for v in vals if DATE_RE.search(v or "")]
        if len(ds) >= 2:
            return _d(ds[0]), _d(ds[1]), "inputs"
    except Exception:
        pass
    try:  # ③ 본문에서 날짜 2개가 한 줄에 있는 첫 줄(집계 완료 시간 띠는 날짜 1개라 걸리지 않는다)
        for line in page.inner_text("body").splitlines():
            ds = DATE_RE.findall(line)
            if len(ds) >= 2:
                return _d(ds[0]), _d(ds[1]), "body-line"
    except Exception:
        pass
    return None, None, "기간 텍스트를 찾지 못함"


def period_target(page, rf):
    """기간 팝업을 여는 요소 — config period_opener가 있으면 그 이름, 없으면 기간 텍스트, 그것도 없으면 날짜 값을 가진 첫 textbox."""
    opener = rf.get("period_opener")
    if opener:
        return locate(page, opener)
    el = locate(page, RANGE_RE, roles=())
    if el is not None:
        return el
    try:
        boxes = page.get_by_role("textbox")
        for i in range(min(boxes.count(), 80)):
            b = boxes.nth(i)
            if b.is_visible() and DATE_RE.search(b.input_value() or ""):
                return b
    except Exception:
        pass
    return None


def dump_inventory(page, path):
    """실패·디버그용 읽기 전용 목록: 날짜가 든 요소·input·button·link의 태그/역할/이름/클래스/문구를 파일로(다음 왕복에서 로케이터 확정용).
    자격 증명·쿠키는 담기지 않는다(화면 문구만)."""
    js = r"""() => {
      const vis = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
      const info = e => ({tag: e.tagName.toLowerCase(), role: e.getAttribute('role') || '', id: e.id || '', cls: (e.className && e.className.baseVal !== undefined ? '' : (e.className || '')).toString().slice(0, 120),
                          aria: e.getAttribute('aria-label') || '', text: (e.innerText || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120),
                          value: e.value === undefined ? '' : String(e.value).slice(0, 60), placeholder: e.placeholder || '', type: e.type || '', visible: vis(e)});
      const out = {url: location.href, title: document.title, dates: [], inputs: [], clickables: []};
      const re = /\d{4}\.\d{2}\.\d{2}/;
      for (const e of document.querySelectorAll('body *')) {
        if (e.children.length === 0 && re.test(e.textContent || '') && vis(e)) out.dates.push(info(e));
        if (out.dates.length > 60) break;
      }
      for (const e of document.querySelectorAll('input, textarea, select')) { out.inputs.push(info(e)); if (out.inputs.length > 200) break; }
      for (const e of document.querySelectorAll('button, a, [role=button], [role=link], [role=menuitem], [role=option], li')) {
        if (vis(e)) out.clickables.push(info(e)); if (out.clickables.length > 300) break; }
      return out;
    }"""
    try:
        data = page.evaluate(js)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        return path
    except Exception:
        return None


def _d(g):
    return dt.date(int(g[0]), int(g[1]), int(g[2]))


def _enabled(locator):
    """버튼이 활성인지(disabled·aria-disabled 아님). 못 읽으면 활성으로 본다."""
    try:
        if not locator.is_enabled():
            return False
        if (locator.get_attribute("aria-disabled") or "").lower() == "true":
            return False
        return True
    except Exception:
        return True


class Shot:
    """--debug 스크린샷(단계마다) + 실패 시 1장은 항상."""

    def __init__(self, page, folder, enabled):
        self.page, self.folder, self.enabled, self.n = page, folder, enabled, 0

    def take(self, tag, force=False):
        if not (self.enabled or force):
            return None
        os.makedirs(self.folder, exist_ok=True)
        self.n += 1
        path = os.path.join(self.folder, f"{self.n:02d}_{tag}.png")
        try:
            self.page.screenshot(path=path, full_page=False)
        except Exception:
            return None
        try:  # 접근성 트리(역할·이름) — 다음 왕복에서 로케이터를 확정하는 근거. 화면 문구만 담긴다
            with open(path[:-4] + ".aria.txt", "w", encoding="utf-8") as f:
                f.write(self.page.locator("body").aria_snapshot())
        except Exception:
            pass
        dump_inventory(self.page, path[:-4] + ".inventory.json")
        return path


def fetch_one(page, item, plan, rf, stage, shot, log):
    """보고서 하나: 열기 → 기간 확인/프리셋 → 확인 → 조회하기 → 다운로드 → 저장 → 돌아가기. 반환 dict(status, file, …)."""
    T = rf["timeout_sec"]
    name, kind = item["name"], item["kind"]
    rec = {"name": name, "kind": kind, "status": "fail", "file": None, "steps": []}

    def step(s):
        rec["steps"].append(s)
        log(f"  [{kind}] {s}")

    if not wait_until(lambda: (locate(page, name, roles=("link", "button")) is not None), T["page"]):
        rec["error"] = f"목록에 보고서 링크 {name!r} 없음"
        shot.take(f"{kind}_no_link", force=True)
        return rec
    link = locate(page, name, roles=("link", "button"), text_fallback=False) or locate(page, name, roles=("link", "button"))
    click_allowed("open_report", link, rf, log)
    if not wait_until(lambda: locate(page, rf["allowed_actions"]["back"]) is not None, T["page"]):
        rec["error"] = "보고서 화면(돌아가기 버튼)이 뜨지 않음"
        shot.take(f"{kind}_no_report_page", force=True)
        return rec
    shot.take(f"{kind}_opened")
    step("보고서 열림")

    wait_until(lambda: read_period(page)[0] is not None, T["page"])  # 기간 표시는 보고서 정의가 로드된 뒤에 그려질 수 있다(왕복 1)
    s, e, how = read_period(page)
    rec["period_read"] = {"start": fmt(s) if s else None, "end": fmt(e) if e else None, "how": how}
    if s is None:
        rec["error"] = f"기간을 읽지 못함({how})"
        shot.take(f"{kind}_no_period", force=True)
        return rec
    step(f"기간 읽음 {fmt(s)}~{fmt(e)} ({how})")
    want = (plan["start_date"], plan["end_date"])
    rec["preset_clicked"] = False
    if (s, e) != want:
        step(f"기대 {plan['start']}~{plan['end']}와 다름 → 프리셋 `{plan['preset']}`")
        opener = rf.get("period_opener")  # null이면 기간 텍스트(없으면 날짜 값 textbox)를 클릭, 문자열이면 그 이름의 요소(예: 달력 아이콘)
        period_el = period_target(page, rf)
        if period_el is None:
            rec["error"] = "기간 표시 요소(팝업 열기)를 찾지 못함" + (f" — period_opener {opener!r}" if opener else "")
            shot.take(f"{kind}_no_period_el", force=True)
            return rec
        click_allowed("open_period", period_el, rf, log)
        if not wait_until(lambda: locate(page, plan["preset"]) is not None, T["page"]):
            rec["error"] = f"기간 팝업에 프리셋 `{plan['preset']}` 이 없음"
            shot.take(f"{kind}_no_preset", force=True)
            return rec
        shot.take(f"{kind}_period_popup")
        click_allowed("preset", locate(page, plan["preset"]), rf, log)
        confirm = locate(page, rf["allowed_actions"]["confirm"])
        if confirm is None:
            rec["error"] = "기간 팝업의 `확인` 버튼을 찾지 못함"
            shot.take(f"{kind}_no_confirm", force=True)
            return rec
        click_allowed("confirm", confirm, rf, log)
        rec["preset_clicked"] = True
        if not wait_until(lambda: read_period(page)[:2] == want, T["page"]):
            s2, e2, how2 = read_period(page)
            rec["error"] = (f"프리셋 뒤 기간이 기대와 다름: {fmt(s2) if s2 else '?'}~{fmt(e2) if e2 else '?'} ({how2}) "
                            f"↔ 기대 {plan['start']}~{plan['end']}")
            shot.take(f"{kind}_period_mismatch", force=True)
            return rec
        step(f"기간 확인 {plan['start']}~{plan['end']}")
    else:
        step("기간 = 기대(저장된 프리셋)")

    query = locate(page, rf["allowed_actions"]["query"])
    if query is None:
        rec["error"] = "`조회하기` 버튼을 찾지 못함"
        shot.take(f"{kind}_no_query", force=True)
        return rec
    # 저장된 형식으로 열면 결과가 자동 조회되고 `조회하기`는 비활성(회색)이다(왕복 2: 4개 모두 클릭 대기 30초 초과). 활성일 때만 누른다.
    rec["queried"] = False
    if _enabled(query):
        try:
            click_allowed("query", query, rf, log)
            rec["queried"] = True
            step("조회하기")
        except SystemExit:
            raise
        except Exception as ex:
            if not _enabled(query):
                step(f"조회하기 비활성 → 건너뜀({click_reason(ex)})")
            else:
                rec["error"] = f"`조회하기` 클릭 실패: {click_reason(ex)}"
                rec["error_detail"] = str(ex)[:800]
                shot.take(f"{kind}_query_click_failed", force=True)
                return rec
    else:
        step("조회하기 비활성(저장된 형식으로 이미 조회됨) → 건너뜀")
    try:
        page.wait_for_load_state("networkidle", timeout=T["page"] * 1000)
    except Exception:
        pass
    time.sleep(rf.get("settle_sec", 1.5))
    shot.take(f"{kind}_queried")

    dl_btn = locate(page, rf["allowed_actions"]["download"])
    if dl_btn is None:
        rec["error"] = "`다운로드` 버튼을 찾지 못함"
        shot.take(f"{kind}_no_download", force=True)
        return rec
    try:
        with page.expect_download(timeout=T["download"] * 1000) as dl_info:
            click_allowed("download", dl_btn, rf, log)
            menu = rf.get("download_menu_item")
            if menu:  # 다운로드가 메뉴(예: CSV)로 갈리면 config로 지정 — 같은 동작 키 `download`
                wait_until(lambda: locate(page, menu) is not None, 5)
                mi = locate(page, menu)
                if mi is not None:
                    click_allowed("download", mi, rf, log)
        download = dl_info.value
    except Exception as ex:
        rec["error"] = f"다운로드가 시작되지 않음({click_reason(ex)})"
        rec["error_detail"] = str(ex)[:800]
        shot.take(f"{kind}_download_timeout", force=True)
        return rec
    fname = download.suggested_filename or item["expected_file"]
    dest = os.path.join(stage, fname)
    download.save_as(dest)
    rec["file"] = dest
    rec["suggested_filename"] = download.suggested_filename
    step(f"다운로드 저장 {fname}")
    if fname not in item["expected_files"]:
        rec.setdefault("warn", []).append(f"파일명 {fname!r} ≠ 기대 {item['expected_files']}")

    back_to_list(page, rf, log)
    shot.take(f"{kind}_back")
    rec["status"] = "downloaded"
    return rec


def on_list(page, rf):
    """목록 화면인지 — 목록 URL이고 보고서 이름이 링크·버튼 역할로 2개 이상 보일 때(보고서 화면의 제목 글자는 세지 않는다)."""
    if not at_list(page, rf):
        return False
    seen = sum(locate(page, n, roles=("link", "button"), text_fallback=False) is not None for n in rf["report_names"])
    return seen >= min(2, len(rf["report_names"]))


def back_to_list(page, rf, log=None):
    """보고서 화면에서 목록으로 — `돌아가기`가 보이면 클릭, 아니면 목록 URL로 이동. 성공·실패 어느 경우에도 다음 보고서 전에 호출한다(왕복 1 결함: 실패 뒤 목록 복귀가 없어 나머지 3개가 '링크 없음')."""
    T = rf["timeout_sec"]
    if on_list(page, rf):
        return True
    back = locate(page, rf["allowed_actions"]["back"])
    if back is not None:
        try:
            click_allowed("back", back, rf, log)
        except SystemExit:
            raise
        except Exception:
            pass
    ok = wait_until(lambda: on_list(page, rf), T["page"] / 2)
    if not ok:
        try:
            page.goto(rf["list_url"])
        except Exception:
            pass
        ok = wait_until(lambda: on_list(page, rf), T["page"])
    return ok


def cmd_login(rf, headless=False):
    """전용 프로필로 창을 띄우고 사용자가 직접 로그인할 때까지 기다린 뒤 목록 URL 도달을 확인. 폼 입력 0."""
    sync_playwright, _ = _playwright()
    T = rf["timeout_sec"]
    clean_download_history(rf["profile_dir"])
    with sync_playwright() as p:
        ctx, browser = launch(p, rf, headless)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        print(f"[login] {browser} · 프로필 {rf['profile_dir']}")
        print(f"[login] 창에서 직접 로그인하세요('로그인 상태 유지' 체크). 이 스크립트는 아무것도 입력하지 않습니다. "
              f"목록 화면({rf['list_url']})이 뜨면 자동으로 닫힙니다(최대 {T['login'] // 60}분).")
        page.goto(rf["list_url"])
        ok = wait_until(lambda: at_list(page, rf), T["login"], step=2)
        if not ok:
            print("[FAIL] 시간 안에 목록 화면에 도달하지 못함 — 다시 --login")
            ctx.close()
            return 1
        names = list(rf["report_names"])
        seen = wait_until(lambda: all(locate(page, n, roles=("link", "button")) is not None for n in names), T["page"])
        print(f"[OK] 목록 URL 도달 · 보고서 이름 {sum(locate(page, n, roles=('link', 'button')) is not None for n in names)}/{len(names)}개 보임"
              + ("" if seen else " (전부 보이지는 않음 — 이름을 config report_names와 대조)"))
        ctx.close()  # persistent context를 닫아야 로그인 상태가 프로필에 저장된다
    return 0


def cmd_fetch(rf, today, prev_dir=None, debug=False, headless=False):
    """기본 실행: 4개 다운로드 → 검사 → 성공이면 day_dir로 이동, 아니면 partial/에만."""
    sync_playwright, _ = _playwright()
    plan = make_plan(rf, today)
    stage, day_dir = plan["stage_dir"], plan["day_dir"]
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    os.makedirs(stage, exist_ok=True)
    started = dt.datetime.now(KST).isoformat(timespec="seconds")
    log_lines = []

    def log(s):
        log_lines.append(s)
        print(s)

    log(f"[fetch] 기준일 {plan['today']} · 기대 `{plan['preset']}` {plan['start']}~{plan['end']} · 계정 {rf['account_no']}")
    log(f"[fetch] 임시 저장 {stage}")
    records = []
    try:
        from importlib.metadata import version as _v
        pw_version = _v("playwright")
    except Exception:
        pw_version = "?"
    cleanup = clean_download_history(rf["profile_dir"], log)
    with sync_playwright() as p:
        ctx, browser = launch(p, rf, headless)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        shot = Shot(page, os.path.join(stage, "debug"), debug)
        page.goto(rf["list_url"])
        T = rf["timeout_sec"]
        if not wait_until(lambda: at_list(page, rf), T["page"], step=1):
            shot.take("not_logged_in", force=True)
            ctx.close()
            print(f"[FAIL] 목록 URL에 도달하지 못함(현재 {current_url(page)[:100]}) — 로그인 세션이 끝난 것 같습니다. "
                  f"`python scripts\\fetch_reports.py --login` 을 다시 실행하세요")
            return 1
        shot.take("list")
        for item in plan["items"]:
            try:
                rec = fetch_one(page, item, plan, rf, stage, shot, log)
            except SystemExit:
                raise
            except Exception as ex:  # 한 보고서의 예외는 그 보고서 실패로만
                rec = {"name": item["name"], "kind": item["kind"], "status": "fail",
                       "error": click_reason(ex), "error_detail": str(ex)[:800], "file": None}
                shot.take(f"{item['kind']}_exception", force=True)
                try:
                    page.goto(rf["list_url"])
                except Exception:
                    pass
            records.append(rec)
            log(f"  → {item['kind']}: {rec['status']}" + (f" ({rec.get('error')})" if rec.get("error") else ""))
            if rec["status"] != "downloaded":  # 실패한 보고서 뒤에도 목록으로 돌아가 다음 보고서를 시도한다
                back_to_list(page, rf, log)
        ctx.close()

    # ---- 검사
    for rec in records:
        if rec.get("file"):
            chk = check_file(rec["file"], rec["name"], rec["kind"], rf, plan["start_date"], plan["end_date"])
            rec["check"] = chk
            rec["status"] = "ok" if chk["ok"] else "fail"
            if not chk["ok"]:
                rec["error"] = "; ".join(c["msg"] for c in chk["checks"] if not c["ok"])
            for c in chk["checks"]:
                log(f"  [{rec['kind']}] {'PASS' if c['ok'] else 'FAIL'} {c['name']}: {c['msg']}"[:220])
    checks = [r["check"] for r in records if r.get("check")]
    cross = cross_check(checks)
    log(f"  [4개] {'PASS' if cross['ok'] else 'FAIL'} {cross['msg']}")
    warnings = []
    prev_detail = None
    if prev_dir:
        prev = load_prev(prev_dir)
        if prev is None:
            warnings.append(f"[알림] --prev 폴더가 없음: {prev_dir}")
        else:
            w, prev_detail = compare_prev(checks, prev)
            warnings += w
    for r in records:
        for w in r.get("warn", []):
            warnings.append(f"[WARN] {r['kind']}: {w}")
    for w in warnings:
        log(w)

    n_ok = sum(1 for r in records if r["status"] == "ok")
    all_ok = n_ok == len(records) and cross["ok"]
    result = "ok" if all_ok else "partial"
    summary = {"date": plan["today"], "started": started, "finished": dt.datetime.now(KST).isoformat(timespec="seconds"),
               "expected": {"preset": plan["preset"], "start": plan["start"], "end": plan["end"]},
               "account_no": rf["account_no"], "list_url": rf["list_url"], "browser": browser, "playwright": pw_version,
               "steps": [cleanup["msg"]], "profile_cleanup": cleanup,
               "reports": [{k: v for k, v in r.items() if k not in ("check",)} | {"check": _slim(r.get("check"))} for r in records],
               "cross": cross, "prev_compare": prev_detail, "warnings": warnings, "result": result,
               "exit_code": 0 if all_ok else 2, "log": log_lines}
    for r in summary["reports"]:
        if r.get("file"):
            r["file"] = os.path.basename(r["file"])

    if all_ok:
        os.makedirs(day_dir, exist_ok=True)
        for r in records:
            shutil.move(r["file"], os.path.join(day_dir, os.path.basename(r["file"])))
        dbg = os.path.join(stage, "debug")
        if os.path.isdir(dbg):
            dst = os.path.join(day_dir, "debug")
            shutil.rmtree(dst, ignore_errors=True)
            shutil.move(dbg, dst)
        summary["folder"] = day_dir
        with open(os.path.join(day_dir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=1, default=str)
        shutil.rmtree(stage, ignore_errors=True)
        print(f"[PASS] 4개 다운로드·검사 통과 → {day_dir}")
        _table(records)
        print("다음: 이 4개를 세션에 올리면 1단계(archive.py store → combine)가 이어진다. 검사 통과 전·부분 실패에는 store 하지 않는다.")
        return 0
    summary["folder"] = stage
    with open(os.path.join(stage, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1, default=str)
    print(f"[FAIL] 4개 중 성공 {n_ok} · 실패 {len(records) - n_ok}" + ("" if cross["ok"] or n_ok < 3 else " · 노출합 불일치")
          + f" → 받은 파일은 {stage} 에만 있음(정상 폴더 {day_dir} 에는 이번 실행 파일 없음). store 금지")
    _table(records)
    return 2


def _slim(chk):
    """summary.json용 — 날짜별 표는 빼고 파일은 이름만."""
    if not chk:
        return None
    out = {k: v for k, v in chk.items() if k != "by_date"}
    if out.get("file"):
        out["file"] = os.path.basename(out["file"])
    return out


def _table(records):
    print("| 보고서 | 종류 | 결과 | 파일 | 행 | 노출·클릭·비용 | 비고 |")
    print("|---|---|---|---|---|---|---|")
    for r in records:
        chk = r.get("check") or {}
        sums = chk.get("sums") or {}
        s = " · ".join(f"{sums.get(k, '-'):,}" if isinstance(sums.get(k), int) else "-" for k in ("노출수", "클릭수", "총비용")) if sums else "-"
        print(f"| {r['name']} | {r['kind']} | {'성공' if r['status'] == 'ok' else '실패'} | {os.path.basename(r['file']) if r.get('file') else '-'} "
              f"| {chk.get('rows', '-')} | {s} | {(r.get('error') or '')[:120]} |")


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="네이버 광고주센터 다차원 보고서 4개 자동 다운로드(PC 전용, Playwright)")
    ap.add_argument("--dry-run", action="store_true", help="브라우저 0 — 할 일 표만")
    ap.add_argument("--login", action="store_true", help="전용 프로필로 창을 띄우고 사용자가 직접 로그인할 때까지 기다림(폼 입력 0)")
    ap.add_argument("--debug", action="store_true", help="단계마다 스크린샷을 저장 폴더 debug/에")
    ap.add_argument("--prev", metavar="폴더", help="직전 4개 폴더 또는 저장소 data/YYYY-MM — 겹치는 날짜 일별 합계 비교(WARN)")
    ap.add_argument("--today", metavar="YYYY-MM-DD", help="기대 기간 계산 기준일(시험용, 기본 KST 오늘)")
    ap.add_argument("--download-dir", help="config report_fetch.download_dir 대신")
    ap.add_argument("--profile-dir", help="config report_fetch.profile_dir 대신")
    a = ap.parse_args(argv)
    rf = fetch_config(download_dir=a.download_dir, profile_dir=a.profile_dir)
    today = dt.date.fromisoformat(a.today) if a.today else today_kst()
    if a.dry_run:
        return cmd_dry_run(rf, today)
    if a.login:
        return cmd_login(rf)
    return cmd_fetch(rf, today, prev_dir=a.prev, debug=a.debug)


if __name__ == "__main__":
    sys.exit(main())
