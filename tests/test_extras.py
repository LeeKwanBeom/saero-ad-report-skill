#!/usr/bin/env python3
"""추가 수집(보고서 더 받기 A + B, 2026-10-12) 시험 — scripts/extras.py(보관·원장·합본·엑셀 읽기) · compute.py 판 G 값 · validate.py 검사 27 ·
compare.py 판 G 구역·_s04 첫 표 · apply.py 판 G 블록. 네이버 접속 0 · 네트워크 0 · 실제 ~/saero-fetch·data/·config 불변(끝에 md5 대조).

실행: "$PY" tests/test_extras.py   (저장소 루트, Git Bash — $PY = 저장소 밖 venv 파이썬)
완료 기준(구현 지시 표) 줄: 4·5·6·9·10·11·12·13·14·16·18·19·20·27·30·31 + 시험 후보(B 멱등 · 빈 셀). 브라우저 쪽(1·2·3·8·24·25·26·29)은 tests/test_fetch_reports.py.
"""
import datetime as dt
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, HERE)
import extras as X  # noqa: E402
import xlsxfix  # noqa: E402
from reportlib import load_config  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

D = dt.date
EXTRAS = os.path.join(ROOT, "scripts", "extras.py")
REAL = [os.path.expanduser("~/saero-fetch/extra-archive"), os.path.expanduser("~/saero-fetch/history")]


def md5f(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def tree_md5(paths):
    out = {}
    for base in paths:
        for dp, _, fns in os.walk(base):
            for fn in fns:
                out[os.path.join(dp, fn)] = md5f(os.path.join(dp, fn))
        out[base + "?exists"] = os.path.exists(base)
    return out


BEFORE = {"config": md5f(os.path.join(ROOT, "config", "report-config.json")), "real": tree_md5(REAL),
          "git": subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout}

CFG = load_config()
EX, _ = X.extras_config(CFG["report_fetch"])
H = EX["history"]
G_COLS = EX["reports"]["성별 보고서"]["columns"]
A_COLS = EX["reports"]["연령대 보고서"]["columns"]


def norm_sample():
    rows, warns = X.normalize_history(X.read_xlsx_rows(xlsxfix.write_xlsx(os.path.join(tempfile.mkdtemp(), "s.xlsx"), xlsxfix.SAMPLE)), H["columns"], H["actor_rules"])
    return rows


def a_file(path, kind, name, s, e, rows, cols=None):
    """성별·연령대 꼴 CSV(첫 줄 기간 헤더 · 2행 = config 원문). rows = [(유형, 캠페인, 'YYYY.MM.DD.', 값, 노출, 클릭, 비용)]."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = [f'"{name}({s:%Y.%m.%d.}~{e:%Y.%m.%d.}),2580077"', cols or (G_COLS if kind == "성별" else A_COLS)]
    width = len(lines[1].split(","))
    for t, camp, day, v, n, c, k in rows:
        lines.append(",".join([t, camp, day, v, str(n), str(c), "0", "0", str(k)] + ["0"] * (width - 9)))   # 2행 칸 수만큼(전환 칸 0)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\n".join(lines) + "\n")
    return path


def run(args, env=None):
    r = subprocess.run([sys.executable, EXTRAS, *args], capture_output=True, text=True, encoding="utf-8",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8", **(env or {})})
    return r.returncode, r.stdout + r.stderr


class XlsxLedger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_read_r_letters_and_actor_words(self):
        """B-8 · 기준 11·31 — 셀 빠진 SYSTEM 줄은 `r` 열 글자로(내용이 캠페인 칸으로 밀리지 않음) · 변경자 → 주체 낱말, 아이디 0 · 다른 칸의 아이디는 <ID>."""
        rows = X.read_xlsx_rows(xlsxfix.write_xlsx(os.path.join(self.tmp, "a.xlsx"), xlsxfix.SAMPLE))
        sysrow = [r for r in rows if r.get("C") == "SYSTEM"][0]
        self.assertEqual(sorted(sysrow), ["A", "B", "C", "F"])
        out, warns = X.normalize_history(rows, H["columns"], H["actor_rules"])
        self.assertEqual(warns, [])
        self.assertEqual([r[2] for r in out], ["스킬", "스킬", "시스템", "스킬", "사람", "사람", "사람", "사람"])
        s = [r for r in out if r[2] == "시스템"][0]
        self.assertEqual((s[3], s[4]), ("", ""))
        self.assertTrue(s[5].startswith("새로필라테스\n설정 값\n"))
        self.assertNotIn(xlsxfix.FAKE, json.dumps(out, ensure_ascii=False))
        self.assertNotIn(":naver", json.dumps(out, ensure_ascii=False))
        leak = [list(r) for r in xlsxfix.SAMPLE]
        leak[4][5] = leak[4][5] + f"\n메모 {xlsxfix.FAKE} 확인"                        # 아이디가 다른 칸에 섞인 줄
        out2, _ = X.normalize_history(X.read_xlsx_rows(xlsxfix.write_xlsx(os.path.join(self.tmp, "b.xlsx"), leak)), H["columns"], H["actor_rules"])
        self.assertIn("메모 <ID> 확인", out2[4][5])
        self.assertNotIn(xlsxfix.FAKE, json.dumps(out2, ensure_ascii=False))
        other = [list(r) for r in xlsxfix.SAMPLE]
        other[0][2] = "누군가"                                                        # 규칙 밖 → '기타' + [주의]
        out3, warns3 = X.normalize_history(X.read_xlsx_rows(xlsxfix.write_xlsx(os.path.join(self.tmp, "c.xlsx"), other)), H["columns"], H["actor_rules"])
        self.assertEqual(out3[0][2], "기타")
        self.assertTrue(warns3 and warns3[0].startswith("[주의]"))

    def test_header_mismatch_message_has_no_cell_text(self):
        bad = list(xlsxfix.HEADER)
        bad[2] = "작업자아이디칸"
        rows = X.read_xlsx_rows(xlsxfix.write_xlsx(os.path.join(self.tmp, "h.xlsx"), xlsxfix.SAMPLE, header=bad))
        with self.assertRaises(X.ExtrasError) as cm:
            X.normalize_history(rows, H["columns"], H["actor_rules"])
        self.assertIn("머리줄이 config history.columns 와 다름(칸 수 6 ↔ 6 · 다른 자리 1)", str(cm.exception))
        self.assertNotIn("작업자아이디칸", str(cm.exception))
        broken = [list(r) for r in xlsxfix.SAMPLE]
        broken[1][0] = "어제 오후"
        with self.assertRaisesRegex(X.ExtrasError, "변경일자 꼴"):
            X.normalize_history(X.read_xlsx_rows(xlsxfix.write_xlsx(os.path.join(self.tmp, "w.xlsx"), broken)), H["columns"], H["actor_rules"])

    def test_merge_idempotent_and_append_only(self):
        """기준 12 · 시험 후보 B 멱등 — 같은 엑셀 두 번 = 0줄(LF 칸 · 앞뒤 공백 칸 · 셀 빠진 SYSTEM 줄 · 같은 줄 두 개 포함 사본 왕복) ·
        다음 날 창(겹침) = 새 줄과 늘어난 같은 줄만 · 앞 바이트 그대로 · .bak-<시각> · 줄어든 창이어도 지우지 않음."""
        led = os.path.join(self.tmp, "hist", "ledger.csv")
        rows = norm_sample()
        n1, _ = X.merge_history(rows, D(2026, 8, 30), D(2026, 9, 28), led, "t1", log=lambda *_: None)
        self.assertEqual(n1, 8)
        b1, c1 = md5f(led), md5f(X.covered_path(led))
        self.assertEqual(X.read_ledger(led), rows)                                         # 사본 왕복 = 칸 원문 그대로
        n2, _ = X.merge_history(norm_sample(), D(2026, 8, 30), D(2026, 9, 28), led, "t2", log=lambda *_: None)
        self.assertEqual(n2, 0)
        self.assertEqual((md5f(led), md5f(X.covered_path(led))), (b1, c1))                  # 쓰기 0(같은 기록 구간도 다시 안 적음)
        self.assertEqual(glob.glob(led + ".bak-*"), [])
        with open(led, "rb") as f:
            old = f.read()
        nxt = [r for r in rows if r[0] >= "2026.08.31."] + [("2026.09.29. 09:00", "광고그룹 On/Off", "사람", "플레이스#1", "새로필라테스", "x\n변경 전\nOn/Off: ON\n변경 후\nOn/Off: OFF"),
                                                           rows[4]]                            # 같은 줄이 하나 더(같은 분 On/Off 세 번째)
        n3, _ = X.merge_history(nxt, D(2026, 8, 31), D(2026, 9, 29), led, "t3", log=lambda *_: None)
        self.assertEqual(n3, 2)
        with open(led, "rb") as f:
            self.assertTrue(f.read().startswith(old))                                      # 기존 줄 삭제·수정 0
        baks = glob.glob(led + ".bak-*")
        self.assertEqual(len(baks), 1)
        self.assertEqual(md5f(baks[0]), b1)
        self.assertEqual(len(X.read_ledger(led)), 10)
        self.assertEqual(X.read_covered(X.covered_path(led)), [(D(2026, 8, 30), D(2026, 9, 27)), (D(2026, 8, 31), D(2026, 9, 28))])
        n4, _ = X.merge_history(rows[:2], D(2026, 9, 27), D(2026, 9, 28), led, "t4", log=lambda *_: None)   # 줄어든 창 — 지우지 않는다
        self.assertEqual((n4, len(X.read_ledger(led))), (0, 10))

    def test_window_and_gap_warnings_and_repo_guard(self):
        led = os.path.join(self.tmp, "hist", "ledger.csv")
        rows = norm_sample()
        _, w = X.merge_history(rows, D(2026, 9, 20), D(2026, 9, 28), led, "t", log=lambda *_: None)
        self.assertTrue(any("화면 기간 9/20~9/28 밖 일시 1줄" in x for x in w), w)          # 9/17 줄은 창 밖 — 넣지 않음
        self.assertEqual(len(X.read_ledger(led)), 7)
        _, w = X.merge_history([], D(2026, 10, 30), D(2026, 10, 31), led, "t", log=lambda *_: None)
        self.assertTrue(any(x.startswith("[주의] 원장 구멍 9/28~10/29") for x in w), w)
        for bad in (os.path.join(ROOT, "audit", "ledger.csv"), os.path.join(ROOT, "x", "ledger.csv")):
            with self.assertRaisesRegex(X.ExtrasError, "저장소 안"):
                X.merge_history(rows, D(2026, 8, 30), D(2026, 9, 28), bad, "t", log=lambda *_: None)
            self.assertFalse(os.path.exists(bad))
        self.assertFalse(X.inside_repo(os.path.join(ROOT, "work", "extra", "a.csv")))      # work/ 는 gitignore — combine --out 자리

    def test_seed_cli_dry_run_then_real_twice(self):
        x = xlsxfix.write_xlsx(os.path.join(self.tmp, "이력 목록 20260928 0130.xlsx"), xlsxfix.SAMPLE)
        led = os.path.join(self.tmp, "seed", "ledger.csv")
        rc, out = run(["seed", x, "--start", "2026-08-30", "--end", "2026-09-28", "--dry-run"], {"SAERO_LEDGER": led})
        self.assertEqual(rc, 0, out)
        self.assertIn("[dry-run] 원장 +8줄", out)
        self.assertFalse(os.path.exists(os.path.dirname(led)))                                # dry-run 쓰기 0
        for n in (8, 0):
            rc, out = run(["seed", x, "--start", "2026-08-30", "--end", "2026-09-28"], {"SAERO_LEDGER": led})
            self.assertEqual(rc, 0, out)
            self.assertIn(f"[원장] +{n}줄", out)
            self.assertIn("환경 변수 SAERO_LEDGER 로 덮어씀", out)
        self.assertEqual(X.read_covered(X.covered_path(led)), [(D(2026, 8, 30), D(2026, 9, 27))])


class StoreCombine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arch = os.path.join(self.tmp, "arch")
        self.env = {"SAERO_EXTRA_ARCHIVE": self.arch, "SAERO_LEDGER": os.path.join(self.tmp, "hist", "ledger.csv")}

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def extra_dir(self, tag, s, e, kinds=("성별", "연령대"), hist=True, status="ok"):
        x = os.path.join(self.tmp, tag, "extra")
        os.makedirs(x)
        reps = []
        for k in kinds:
            name = f"{k} 보고서"
            fn = f"{name},2580077.csv"
            a_file(os.path.join(x, fn), k, name, s, e, [("플레이스", "플레이스#1", f"{s:%Y.%m.%d.}", "알 수 없음", 10, 1, 900)])
            reps.append({"name": name, "kind": k, "status": status, "file": fn})
        summ = {"date": (e + dt.timedelta(days=1)).isoformat(), "reports": reps, "history": None}
        if hist:
            with open(os.path.join(x, X.HISTORY_FILE), "wb") as f:
                f.write(X.history_csv_bytes(norm_sample(), D(2026, 8, 30), D(2026, 9, 28), "2580077"))
            summ["history"] = {"status": "ok", "file": X.HISTORY_FILE}
        with open(os.path.join(x, X.SUMMARY), "w", encoding="utf-8") as f:
            json.dump(summ, f, ensure_ascii=False)
        return x

    def test_store_exact_name_bak_and_refusals(self):
        """기준 5 — 보관 이름 <종류>.csv 하나 · 같은 바이트면 .bak 0 · 늘어난 파일은 옛 것 .bak · 끝이 이르면 거부 · 두 달 걸침 거부 · 2행 다르면 거부 ·
        이웃 파일(.bak·_2·접두 이름)은 건드리지 않음."""
        sp = {"kind": "성별", "columns": G_COLS}
        month = os.path.join(self.arch, "2026-09")
        os.makedirs(month)
        for nb in ("성별_2.csv", "성별연령.csv"):
            with open(os.path.join(month, nb), "w") as f:
                f.write("이웃")
        p1 = a_file(os.path.join(self.tmp, "a1.csv"), "성별", "성별 보고서", D(2026, 9, 1), D(2026, 9, 20), [("플레이스", "플레이스#1", "2026.09.01.", "남성", 5, 0, 0)])
        dest = X.store_report(p1, "성별 보고서", sp, "2580077", self.arch, log=lambda *_: None)
        self.assertEqual(dest, os.path.join(month, "성별.csv"))
        X.store_report(p1, "성별 보고서", sp, "2580077", self.arch, log=lambda *_: None)
        self.assertFalse(os.path.exists(dest + ".bak"))
        p2 = a_file(os.path.join(self.tmp, "a2.csv"), "성별", "성별 보고서", D(2026, 9, 1), D(2026, 9, 21), [("플레이스", "플레이스#1", "2026.09.21.", "남성", 6, 0, 0)])
        X.store_report(p2, "성별 보고서", sp, "2580077", self.arch, log=lambda *_: None)
        self.assertEqual(md5f(dest + ".bak"), md5f(p1))
        self.assertEqual(md5f(dest), md5f(p2))
        for label, path, frag in (("이른 끝", p1, "앞섬"),
                                  ("두 달", a_file(os.path.join(self.tmp, "a3.csv"), "성별", "성별 보고서", D(2026, 9, 30), D(2026, 10, 1), []), "두 달"),
                                  ("2행", a_file(os.path.join(self.tmp, "a4.csv"), "성별", "성별 보고서", D(2026, 9, 1), D(2026, 9, 25),
                                                 [("a", "b", "2026.09.01.", "남성", 1, 0, 0)], cols=G_COLS + ",추가열"), "2행"),
                                  ("이름", a_file(os.path.join(self.tmp, "a5.csv"), "성별", "연령대 보고서", D(2026, 9, 1), D(2026, 9, 25),
                                                  [("a", "b", "2026.09.01.", "남성", 1, 0, 0)]), "이름")):
            with self.subTest(label=label):
                with self.assertRaisesRegex(X.ExtrasError, frag):
                    X.store_report(path, "성별 보고서", sp, "2580077", self.arch, log=lambda *_: None)
                self.assertEqual(md5f(dest), md5f(p2))
        self.assertEqual(sorted(os.listdir(month)), ["성별.csv", "성별.csv.bak", "성별_2.csv", "성별연령.csv"])
        with self.assertRaisesRegex(X.ExtrasError, "저장소 안"):
            X.store_report(p2, "성별 보고서", sp, "2580077", os.path.join(ROOT, "extra-archive"), log=lambda *_: None)

    def test_store_cli_summary_driven_and_dry_run(self):
        """store 는 summary_extra.json 의 받음(ok)만 · 실패·없음은 [주의](멈춤 아님, exit 0) · --dry-run 쓰기 0(md5 전후)."""
        x = self.extra_dir("d1", D(2026, 9, 1), D(2026, 9, 27))
        with open(os.path.join(x, X.SUMMARY), encoding="utf-8") as f:
            summ = json.load(f)
        summ["reports"][1]["status"] = "fail"
        with open(os.path.join(x, X.SUMMARY), "w", encoding="utf-8") as f:
            json.dump(summ, f, ensure_ascii=False)
        rc, out = run(["store", x, "--dry-run"], self.env)
        self.assertEqual(rc, 0, out)
        self.assertIn("[dry-run] 성별 →", out)
        self.assertFalse(os.path.exists(self.arch))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "hist")))
        rc, out = run(["store", x], self.env)
        self.assertEqual(rc, 0, out)
        self.assertIn("[추가 보관] 성별", out)
        self.assertIn("[주의] 연령대: 이번 수집 fail — 보관본 그대로", out)
        self.assertIn("[원장] +8줄", out)
        self.assertEqual(os.listdir(os.path.join(self.arch, "2026-09")), ["성별.csv"])
        rc, out = run(["store", os.path.join(self.tmp, "없음")], self.env)
        self.assertEqual(rc, 0, out)
        self.assertIn("[주의] summary_extra.json 를 못 읽음", out)

    def test_combine_day_continuity(self):
        """기준 18 — 10/01~10/30 + 11/01~11/01 → 빈틈 10/31 → 머리 11/01~11/01 + [주의] · 이어지면 전체 · 겹침이면 마지막 연속 구간만 · 지난 합본은 지운다."""
        a_file(os.path.join(self.arch, "2026-10", "성별.csv"), "성별", "성별 보고서", D(2026, 10, 1), D(2026, 10, 30), [("플레이스", "플레이스#1", "2026.10.30.", "남성", 5, 1, 900)])
        a_file(os.path.join(self.arch, "2026-11", "성별.csv"), "성별", "성별 보고서", D(2026, 11, 1), D(2026, 11, 1), [("플레이스", "플레이스#1", "2026.11.01.", "여성", 7, 0, 0)])
        a_file(os.path.join(self.arch, "2026-09", "연령대.csv"), "연령대", "연령대 보고서", D(2026, 9, 1), D(2026, 9, 30), [("플레이스", "플레이스#1", "2026.09.30.", "30~34세", 3, 0, 0)])
        a_file(os.path.join(self.arch, "2026-10", "연령대.csv"), "연령대", "연령대 보고서", D(2026, 10, 1), D(2026, 10, 30), [("플레이스", "플레이스#1", "2026.10.01.", "30~34세", 4, 0, 0)])
        with open(os.path.join(self.arch, "2026-10", "성별.csv.bak"), "w", encoding="utf-8-sig") as f:   # .bak 은 읽지 않는다(정확한 이름 하나)
            f.write('"성별 보고서(2026.10.01.~2026.10.31.),2580077"\n' + G_COLS + "\n")
        out_dir = os.path.join(self.tmp, "work", "extra")
        os.makedirs(out_dir)
        with open(os.path.join(out_dir, X.HISTORY_FILE), "w") as f:
            f.write("지난 회차 사본")
        rc, out = run(["combine", "--out", out_dir], self.env)
        self.assertEqual(rc, 0, out)
        self.assertIn("[주의] 성별 빈틈 10/31~10/31 — 11/1부터만", out)
        self.assertEqual(X.read_head(os.path.join(out_dir, "성별.csv"))[0], '"성별 합본(2026.11.01.~2026.11.01.),2580077"')
        with open(os.path.join(out_dir, "성별.csv"), encoding="utf-8-sig") as f:
            self.assertEqual(f.read().splitlines()[2:], ["플레이스,플레이스#1,2026.11.01.,여성,7,0,0,0,0" + ",0" * (len(G_COLS.split(",")) - 9)])
        self.assertEqual(X.read_head(os.path.join(out_dir, "연령대.csv"))[0], '"연령대 합본(2026.09.01.~2026.10.30.),2580077"')
        self.assertFalse(os.path.exists(os.path.join(out_dir, X.HISTORY_FILE)))            # 원장 없음 → 지난 사본도 지움(옛 값 0)
        self.assertIn("[주의] 변경 이력: 원장 없음", out)
        a_file(os.path.join(self.arch, "2026-12", "성별.csv"), "성별", "성별 보고서", D(2026, 10, 31), D(2026, 11, 2), [])   # 손으로 둔 겹침 조각(11/1 이 두 번)
        rc, out = run(["combine", "--out", out_dir], self.env)
        self.assertIn("[주의] 성별 겹침 11/1~11/1 — 11/1부터만", out)
        self.assertEqual(X.read_head(os.path.join(out_dir, "성별.csv"))[0], '"성별 합본(2026.11.01.~2026.11.01.),2580077"')
        b = {p: md5f(p) for p in glob.glob(os.path.join(out_dir, "*"))}
        rc, out = run(["combine", "--out", out_dir, "--dry-run"], self.env)
        self.assertIn("[dry-run] 성별 합본", out)
        self.assertEqual({p: md5f(p) for p in glob.glob(os.path.join(out_dir, "*"))}, b)

    def test_runs_of(self):
        P = lambda a, b: (D(2026, *a), D(2026, *b))
        self.assertEqual(len(X.runs_of([P((10, 1), (10, 31)), P((11, 1), (11, 30))])), 1)
        self.assertEqual(len(X.runs_of([P((10, 1), (10, 30)), P((11, 1), (11, 1))])), 2)
        self.assertEqual(len(X.runs_of([P((10, 1), (10, 31)), P((10, 31), (11, 2))])), 2)


# ---------------------------------------------------------------- 계산·검산·대조·적용(판 G)
import compute as C  # noqa: E402
import apply as A  # noqa: E402


def ledger_rows():
    """탐색 실측 갈래를 흉내 낸 원장 줄(아이디 없음) — 스킬 등록 42줄 = 실행 17회(고유 분) · 삭제 3 · 사람 On/Off·하루예산·제외키워드 0 → 70 · SYSTEM 12."""
    rows = []
    for i in range(17):
        when = f"2026.09.{12 + i:02d}. 0{i % 3}:{10 + i:02d}"
        groups = ["상계동필라테스", "노원역필라테스", "노원산전필라테스"] if i < 8 else ["상계동필라테스", "노원역필라테스"]   # 8회 × 3 + 9회 × 2 = 42줄
        for g in groups:
            rows.append((when, "타겟팅 변경", "스킬", "새로필라테스 파워링크", g, f"{g}\n등록된 내용\n확장 검색: 가a, 가b, 가c"))
    for when in ("2026.09.27. 13:59", "2026.09.27. 14:03", "2026.09.28. 15:51"):
        rows.append((when, "타겟팅 변경", "스킬", "새로필라테스 파워링크", "상계동필라테스", "상계동필라테스\n삭제된 내용\n확장 검색: SAERO제외테스트"))
    for d in range(12, 24):
        rows.append((f"2026.09.{d:02d}. 22:20", "광고그룹 하루예산 중단" if d != 17 else "광고그룹 하루예산 재개", "시스템", "", "", "새로필라테스\n설정 값\n하루예산: 10,000원"))
    rows += [("2026.09.17. 15:30", "광고그룹 On/Off", "사람", "플레이스#1", "새로필라테스", "새로필라테스\n변경 전\nOn/Off: ON\n변경 후\nOn/Off: OFF"),
             ("2026.09.17. 15:30", "광고그룹 변경", "사람", "플레이스#1", "새로필라테스", "새로필라테스\n변경 전\n하루예산: 10,000원\n변경 후\n하루예산: 20,000원"),
             ("2026.09.17. 08:22", "타겟팅 변경", "사람", "플레이스#1", "새로필라테스", "\n변경 전\n제외키워드: \n변경 후\n제외키워드: " + ", ".join(f"k{i}" for i in range(70))),
             ("2026.09.21. 07:57", "타겟팅 변경", "사람", "새로필라테스 파워링크", "노원산전필라테스", "노원산전필라테스\n등록된 내용\n확장 검색: 노원역체험")]
    return rows


def write_extra(d, rows=None, spans=((D(2026, 9, 12), D(2026, 10, 10)),), ga=True):
    """work/extra 꼴 폴더 — 성별·연령대 합본 + 원장·기록 구간 사본."""
    os.makedirs(d, exist_ok=True)
    if ga:
        a_file(os.path.join(d, "성별.csv"), "성별", "성별 합본", D(2026, 10, 1), D(2026, 10, 9),
               [("플레이스", "플레이스#1", "2026.10.01.", "남성", 150, 6, 5400), ("파워링크", "새로필라테스 파워링크", "2026.10.01.", "남성", 30, 0, 0),
                ("플레이스", "플레이스#1", "2026.10.02.", "여성", 90, 3, 2700), ("플레이스", "플레이스#1", "2026.10.02.", "알 수 없음", 60, 1, 900)])
        a_file(os.path.join(d, "연령대.csv"), "연령대", "연령대 합본", D(2026, 10, 1), D(2026, 10, 10),
               [("플레이스", "플레이스#1", "2026.10.01.", "40~44세", 120, 5, 4500), ("플레이스", "플레이스#1", "2026.10.01.", "25~29세", 200, 4, 3600),
                ("플레이스", "플레이스#1", "2026.10.03.", "알 수 없음", 50, 0, 0), ("플레이스", "플레이스#1", "2026.10.03.", "60세~", 7, 1, 900)])
    if rows is not False:
        with open(os.path.join(d, X.HISTORY_FILE), "wb") as f:
            f.write(b"\xef\xbb\xbf" + X._rows_bytes(rows or ledger_rows(), X.LEDGER_COLS))
        with open(os.path.join(d, X.COVERED_FILE), "wb") as f:
            f.write(b"\xef\xbb\xbf" + X._rows_bytes([(s.isoformat(), e.isoformat(), "t", "t") for s, e in spans], X.COVERED_COLS))
    return d


def days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d.strftime("%Y.%m.%d."))
        d += dt.timedelta(days=1)
    return out


class ComputeG(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def cards(self, d, a=D(2026, 8, 26), b=D(2026, 10, 10), cfg=None):
        buf = io.StringIO()
        with redirect_stderr(buf):
            ga, hi = C.extra_cards(d, cfg or CFG, days(a, b))
        return ga, hi, buf.getvalue()

    def test_gender_age_min_imps_unknown(self):
        """기준 14 — min_imps 미만 '적음'(클릭률 없음) · 알 수 없음 비중 · 기간 = 합본 머리(실제) · 연령은 숫자 순 · show_unknown false 면 줄 뺌(머리 % 그대로)."""
        ga, _, _ = self.cards(write_extra(os.path.join(self.tmp, "x")))
        self.assertEqual(ga["상태"], "ok")
        sx, ag = ga["표"]
        self.assertEqual((sx["종류"], sx["기간"], sx["알수없음%"]), ("성별", "10/1~10/9", 18.2))
        self.assertEqual([(r["구분"], r["노출"], r["비중"], r["클릭"], r["CTR"], r["적음"]) for r in sx["rows"]],
                         [("남성", 180, 54.5, 6, 3.33, False), ("여성", 90, 27.3, 3, None, True), ("알 수 없음", 60, 18.2, 1, None, True)])
        self.assertEqual([r["구분"] for r in ag["rows"]], ["25~29세", "40~44세", "60세~", "알 수 없음"])
        self.assertEqual(ag["기간"], "10/1~10/10")
        cfg = json.loads(json.dumps(CFG))
        cfg["report_fetch"]["extras"]["gender_age"]["show_unknown"] = False
        ga2, _, _ = self.cards(os.path.join(self.tmp, "x"), cfg=cfg)
        self.assertEqual([r["구분"] for r in ga2["표"][0]["rows"]], ["남성", "여성"])
        self.assertEqual(ga2["표"][0]["알수없음%"], 18.2)

    def test_history_period_three_cases(self):
        """기준 19 — 표 기간 = 집계 기간 ∩ 기록 구간 마지막 연속 구간: ① B 실패 다음 날(기록 구간 끝 < 집계 끝) ② 손 다운로드 날(받은 날은 기록 구간 밖) ·
        ③ 원장 시작이 집계 시작보다 늦음 · ④ 기록 구간에 빈틈이면 마지막 구간만 · 집계 기간과 겹치지 않으면 '확인 못 함'."""
        d = os.path.join(self.tmp, "h")
        write_extra(d, spans=((D(2026, 9, 12), D(2026, 10, 9)),), ga=False)                # ① 10/10 회차 B 실패 — 10/9 까지만
        _, hi, _ = self.cards(d, b=D(2026, 10, 10))
        self.assertEqual((hi["기간"], hi["집계기간같음"]), ("9/12~10/9", False))
        write_extra(d, spans=((D(2026, 9, 12), D(2026, 10, 10)),), ga=False)                # ② 10/11 23:56 손 다운로드(화면 9/12~10/11) → 10/10 까지
        _, hi, _ = self.cards(d, b=D(2026, 10, 11))
        self.assertEqual(hi["기간"], "9/12~10/10")
        _, hi, _ = self.cards(d, b=D(2026, 10, 10))                                        # ③ 원장 9/12 시작 · 집계 8/26 시작
        self.assertEqual((hi["기간"], hi["시작"]), ("9/12~10/10", "2026.09.12."))
        write_extra(d, spans=((D(2026, 8, 1), D(2026, 9, 1)), (D(2026, 9, 20), D(2026, 10, 5)), (D(2026, 9, 25), D(2026, 10, 10))), ga=False)   # ④
        _, hi, _ = self.cards(d)
        self.assertEqual(hi["기간"], "9/20~10/10")
        write_extra(d, spans=((D(2026, 7, 1), D(2026, 7, 30)),), ga=False)
        _, hi, err = self.cards(d)
        self.assertEqual(hi["상태"], "없음")
        self.assertIn("[주의] 계정 변경 기록 확인 못 함", err)

    def test_branches_units_and_system(self):
        """기준 20·13 — 등록 n개 · 삭제 n개 · 변경(전 n → 후 m개) · 그 밖 유형만 / 스킬 = 실행 17회(고유 분) · 삭제 3 / SYSTEM 줄 0(show_system false)."""
        self.assertEqual(C.change_phrase("타겟팅 변경", "g\n등록된 내용\n확장 검색: a, b, c"), "등록 3개(확장 검색)")
        self.assertEqual(C.change_phrase("타겟팅 변경", "g\n삭제된 내용\n확장 검색: SAERO제외테스트"), "삭제 1개(확장 검색)")
        self.assertEqual(C.change_phrase("타겟팅 변경", "\n변경 전\n제외키워드: \n변경 후\n제외키워드: " + ", ".join("abcdefg")), "제외키워드 변경(전 0 → 후 7개)")
        self.assertEqual(C.change_phrase("광고그룹 On/Off", "g\n변경 전\nOn/Off: ON\n변경 후\nOn/Off: OFF"), "On/Off ON → OFF")
        self.assertEqual(C.change_phrase("광고그룹 변경", "g\n변경 전\n하루예산: 10,000원\n변경 후\n하루예산: 20,000원"), "하루예산 10,000원 → 20,000원")
        self.assertEqual(C.change_phrase("광고그룹 하루예산 중단", "g\n설정 값\n하루예산: 10,000원"), "")
        self.assertEqual(C.change_phrase("모르는 유형", "한 줄"), "")
        d = write_extra(os.path.join(self.tmp, "b"), ga=False)
        _, hi, _ = self.cards(d)
        self.assertEqual(hi["스킬"], {"등록회": 17, "삭제건": 3})
        self.assertNotIn("시스템", hi)
        self.assertEqual(hi["건수"], 3)                                                       # 9/17 15:30 두 줄 = 같은 분 → 한 줄(2026-10-12)
        self.assertEqual([(r["일시"], r["유형"], r["대상"], r["내용"]) for r in hi["rows"]],
                         [("9/21 07:57", "타겟팅 변경", "노원산전필라테스", "등록 1개(확장 검색)"),
                          ("9/17 15:30", "광고그룹 On/Off · 광고그룹 변경", "새로필라테스", "On/Off ON → OFF · 하루예산 10,000원 → 20,000원"),
                          ("9/17 08:22", "타겟팅 변경", "새로필라테스", "제외키워드 변경(전 0 → 후 70개)")])
        self.assertFalse(any(r["주체"] != "사람" for r in hi["rows"]))
        cfg = json.loads(json.dumps(CFG))
        cfg["report_fetch"]["extras"]["history"]["show_system"] = True
        _, hi2, _ = self.cards(d, cfg=cfg)
        self.assertEqual(hi2["시스템"], {"하루예산중단": 11})
        many = [(f"2026.09.{12 + i % 15:02d}. 1{i % 10}:00", "광고그룹 On/Off", "사람", "c", f"g{i}", "g\n변경 전\nOn/Off: ON\n변경 후\nOn/Off: OFF") for i in range(25)]
        _, hi3, _ = self.cards(write_extra(os.path.join(self.tmp, "m"), rows=many, ga=False))
        self.assertEqual((hi3["건수"], hi3["표시"], len(hi3["rows"])), (25, 10, 10))           # max_rows
        self.assertEqual(hi3["rows"], sorted(hi3["rows"], key=lambda r: (int(r["일시"].split("/")[1].split()[0]), r["일시"][-5:]), reverse=True))

    def test_same_minute_one_row(self):
        """2026-10-12 사용자 결정 "같은 시각 줄은 하나로 묶어줘" — 같은 분(일시 원문) 사람 줄 = 한 줄: 대상·유형·내용은 겹치지 않는 값을 원장 순서대로 ' · ' ·
        분이 다르면 따로(9/26 13:19 · 13:18) · '건수'·max_rows 는 묶은 줄 수 · validate 가 따로 다시 묶은 값과 같다(compute → apply → validate 왕복)."""
        reg = lambda when, g, n: (when, "타겟팅 변경", "사람", "새로필라테스 파워링크", g, f"{g}\n등록된 내용\n확장 검색: " + ", ".join(f"k{i}" for i in range(n)))
        rows = [reg("2026.09.26. 13:20", g, 6) for g in ("상계동필라테스", "노원역필라테스", "노원산전필라테스")]
        rows += [reg("2026.09.26. 13:19", "상계동필라테스", 7)] + [reg("2026.09.26. 13:18", g, 7) for g in ("노원역필라테스", "노원산전필라테스")]
        rows += [reg("2026.09.25. 13:13", "상계동필라테스", 11), reg("2026.09.25. 13:13", "노원역필라테스", 10)]      # 같은 분 · 내용 다름
        d = write_extra(os.path.join(self.tmp, "s"), rows=rows, ga=False)
        _, hi, _ = self.cards(d)
        self.assertEqual((hi["건수"], hi["표시"]), (4, 4))
        self.assertEqual([(r["일시"], r["유형"], r["대상"], r["내용"]) for r in hi["rows"]],
                         [("9/26 13:20", "타겟팅 변경", "상계동필라테스 · 노원역필라테스 · 노원산전필라테스", "등록 6개(확장 검색)"),
                          ("9/26 13:19", "타겟팅 변경", "상계동필라테스", "등록 7개(확장 검색)"),
                          ("9/26 13:18", "타겟팅 변경", "노원역필라테스 · 노원산전필라테스", "등록 7개(확장 검색)"),
                          ("9/25 13:13", "타겟팅 변경", "상계동필라테스 · 노원역필라테스", "등록 11개(확장 검색) · 등록 10개(확장 검색)")])
        many = [reg(f"2026.09.{12 + i // 3:02d}. 10:{i // 3:02d}", f"g{i % 3}", 1) for i in range(36)]   # 12분 × 3그룹
        _, hi2, _ = self.cards(write_extra(os.path.join(self.tmp, "s2"), rows=many, ga=False))
        self.assertEqual((hi2["건수"], hi2["표시"]), (12, 10))
        self.assertTrue(all(r["대상"] == "g0 · g1 · g2" for r in hi2["rows"]))
        # validate 가 compute 와 따로 다시 묶은 값과 같다 — apply 로 그린 블록을 check_extras 가 PASS
        R = {"변경기록": hi}
        blk = A.hi_block(R)
        html = f'<div>{blk}<!-- saero:extra gender-age --><div class="note">확인 못 함 — t</div><!-- /saero:extra gender-age --></div>'
        kw = os.path.join(self.tmp, "kw.csv")
        with open(kw, "w", encoding="utf-8") as f:
            f.write("키워드 보고서(2026.08.26.~2026.10.10.),2580077\n일별,노출수\n" + "".join(f"{x},1\n" for x in days(D(2026, 8, 26), D(2026, 10, 10))))
        import validate as V
        del V.results[:]
        with redirect_stdout(io.StringIO()):
            V.check_extras(html, d, V.read_csv(kw))
        res = [r for r in V.results if "추가 카드·표" in r[0]]
        self.assertTrue(res and res[-1][1], res)
        bad = html.replace("상계동필라테스 · 노원역필라테스 · 노원산전필라테스", "상계동필라테스", 1)          # 묶음을 푼 화면 → FAIL
        del V.results[:]
        with redirect_stdout(io.StringIO()):
            V.check_extras(bad, d, V.read_csv(kw))
        res = [r for r in V.results if "추가 카드·표" in r[0]]
        self.assertTrue(res and not res[-1][1] and "변경 기록 표" in res[-1][2], res)

    def test_no_input_is_unknown_exit0(self):
        """기준 10 — 추가 데이터 없음(첫 회 · 실패 · --extra 없음) → 상태 없음 · [주의] · compute exit 0."""
        ga, hi, err = self.cards(os.path.join(self.tmp, "없는폴더"))
        self.assertEqual((ga["상태"], hi["상태"]), ("없음", "없음"))
        self.assertIn("[주의] 성별 카드 확인 못 함", err)
        cfg = json.loads(json.dumps(CFG))
        cfg["report_fetch"]["extras"]["reports"]["성별 보고서"]["kind"] = "키워드"       # 설정 오류 → 꺼짐(두 카드 '확인 못 함')
        ga, hi, err = self.cards(os.path.join(self.tmp, "x"), cfg=cfg)
        self.assertEqual((ga["사유"], hi["사유"]), ("extras 설정 꺼짐", "extras 설정 꺼짐"))


FIX = os.path.join(HERE, "fixtures", "layout_old.html")
FIXJ = os.path.join(HERE, "fixtures", "layout_old.compute.json")


def jread(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def strip_blocks(h):
    for k in ("history", "gender-age"):
        a = h.index(f"<!-- saero:extra {k} -->")
        a = h.rindex("\n", 0, a) + 1
        b = h.index(f"<!-- /saero:extra {k} -->") + len(f"<!-- /saero:extra {k} -->") + 1
        h = h[:a] + h[b:]
    return h


class ApplyValidateCompareG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.H, cls.R = open(FIX, encoding="utf-8", newline="").read(), jread(FIXJ)
        cls.extra = write_extra(os.path.join(cls.tmp, "extra"))
        buf = io.StringIO()
        with redirect_stderr(buf):
            ga, hi = C.extra_cards(cls.extra, CFG, days(D(2026, 8, 26), D(2026, 10, 10)))
        cls.RX = dict(cls.R, 성별연령=ga, 변경기록=hi)
        cls.G0 = A.apply(cls.H, cls.R, CFG, layout=True)          # compute 에 키 없음 → '확인 못 함'
        cls.G1 = A.apply(cls.H, cls.RX, CFG, layout=True)
        import pandas as pd
        cls.kw = pd.DataFrame({"일별": days(D(2026, 8, 26), D(2026, 10, 10)), "광고그룹": "x", "노출수": 1, "클릭수": 0, "총비용": 0})

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_blocks_values_every_run_no_residue(self):
        """기준 10·15 — 값 매 회차(있음 ↔ 없음 오가도 옛 글자 0) · 다른 구역 바이트 같음 · 멱등 · 아이디 가림 글자는 이스케이프(태그 짝)."""
        self.assertIn("확인 못 함 — compute.json 에 \"성별연령\" 없음", self.G0)
        self.assertIn("9/12~10/10 기록", self.G1)
        self.assertEqual(strip_blocks(self.G0), strip_blocks(self.G1))
        self.assertEqual(A.apply(self.G1, self.R, CFG), self.G0)
        self.assertEqual(A.apply(self.G0, self.RX, CFG), self.G1)
        self.assertEqual(A.apply(self.G1, self.RX, CFG), self.G1)
        RX2 = json.loads(json.dumps(self.RX))
        RX2["변경기록"]["rows"][0]["대상"] = "<ID> & 그룹"
        o = A.apply(self.G1, RX2, CFG)
        self.assertIn("&lt;ID&gt; &amp; 그룹", o)
        self.assertEqual(o.count("<td"), o.count("</td>"))

    def test_chain_scope_and_hand_edits(self):
        """기준 15 — F → G = 사슬 바이트 · 바뀌는 곳 = meta·블록 둘(04 본 표·note 뒤 · 05 안) · 손 수정 F/G FAIL."""
        lay = CFG["report_layout"]
        cfg_f = dict(CFG, report_layout=dict(lay, layout_id="r2026-10-F"))
        F_ = A.apply(self.H, self.R, cfg_f, layout=True)
        self.assertEqual(A.apply(F_, self.R, CFG, layout=True), self.G0)
        self.assertEqual(A.chain("r2026-10-F", "r2026-10-G"), [A.convert_f_to_g])
        g = A.convert_f_to_g(F_, lay)
        self.assertEqual(strip_blocks(g).replace('content="r2026-10-G"', 'content="r2026-10-F"', 1), F_)
        s4 = g[g.index("<!-- Section 4:"):g.index("<!-- Section 5:")]
        self.assertLess(s4.index("</table>"), s4.index("<!-- saero:extra history -->"))
        self.assertIn("<!-- saero:extra gender-age -->", g[g.index("<!-- Section 5:"):g.index("<!-- Section 6:")])
        with self.assertRaisesRegex(A.ApplyError, "이미 있음"):
            A.convert_f_to_g(F_.replace("</body>", "<!-- saero:extra x --></body>", 1), lay)
        blk = g[g.rindex("\n", 0, g.index("<!-- saero:extra history -->")) + 1:g.index("<!-- /saero:extra history -->") + len("<!-- /saero:extra history -->") + 1]
        for label, bad, frag in (("블록 지움", self.G0.replace(blk, "", 1) if blk in self.G0 else None, "추가 블록 표지"),
                                 ("블록 둘", self.G0.replace(blk, blk * 2, 1) if blk in self.G0 else None, "추가 블록 표지"),
                                 ("05 로 옮김", (self.G0.replace(blk, "", 1).replace("<!-- Section 6:", blk + "<!-- Section 6:", 1)) if blk in self.G0 else None, "04 구역 안")):
            with self.subTest(label=label):
                self.assertIsNotNone(bad)
                with self.assertRaisesRegex(A.ApplyError, frag):
                    A.apply(bad, self.R, CFG, layout=True)
        no_end = F_.replace("\n  </div>\n\n  <!-- Section 5:", "\n  </div>\n<p>손</p>\n\n  <!-- Section 5:", 1)
        with self.assertRaisesRegex(A.ApplyError, "04 구역 끝"):
            A.apply(no_end, self.R, CFG, layout=True)

    def test_04_anchor_and_compare_first_table(self):
        """기준 30(B-6) — apply 의 04 tbody 앵커는 본 표 그대로 · compare _s04 는 04 첫 <table> 만(새 표가 있어도 '04 표' OK · 파싱 실패 0) · 판 G 구역 항목 OK."""
        s4 = self.G1[self.G1.index("<!-- Section 4:"):self.G1.index("<!-- Section 5:")]
        first = s4[:s4.index("</table>")]
        self.assertEqual(len(re.findall(r"<tr>", first)), len(self.R["04"]["rows"]))
        td = tempfile.mkdtemp()
        try:
            hp, jp = os.path.join(td, "index.html"), os.path.join(td, "compute.json")
            with open(hp, "w", encoding="utf-8", newline="") as f:
                f.write(self.G1)
            with open(jp, "w", encoding="utf-8") as f:
                json.dump(self.RX, f, ensure_ascii=False)
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "compare.py"), hp, jp], capture_output=True, text=True, encoding="utf-8")
            out = r.stdout
            self.assertIn("[OK]   04 표:", out)
            self.assertNotIn("파싱 실패 [04] — 마크업이 바뀌었으면 compare.py를 고칠 것: IndexError", out)   # 옛 rows(sec(4)) 는 새 표의 4칸 줄에서 r[8] IndexError
            for item in ("04 변경 기록 머리(기간)", "04 변경 기록 표", "04 변경 기록 스킬 줄", "05 성별 머리(기간·알 수 없음)", "05 성별 표", "05 연령대 머리(기간·알 수 없음)", "05 연령대 표"):
                self.assertIn(f"[OK]   {item}", out)
            self.assertNotIn("파싱 실패 [04·05 추가(판 G)]", out)
            RX2 = json.loads(json.dumps(self.RX))
            RX2["변경기록"]["스킬"]["등록회"] += 1
            RX2["성별연령"]["표"][0]["rows"][0]["노출"] += 1
            with open(jp, "w", encoding="utf-8") as f:
                json.dump(RX2, f, ensure_ascii=False)
            out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "compare.py"), hp, jp], capture_output=True, text=True, encoding="utf-8").stdout
            self.assertIn("[DIFF] 04 변경 기록 스킬 줄", out)
            self.assertIn("[DIFF] 05 성별 표", out)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def vcheck(self, html, extra):
        import validate as V
        V.results.clear()
        with redirect_stdout(io.StringIO()):
            V.check_extras(html, extra, self.kw)
        return V.results[-1]

    def test_validate_independent(self):
        """기준 27(A-5)·9·11·13 — 카드 유무 기준 = work/extra 파일 유무(첫 회·실패면 '확인 못 함' 이 PASS) · 값·기간 다르면 FAIL · 아이디 꼴·SYSTEM FAIL."""
        name, ok, det = self.vcheck(self.G1, self.extra)
        self.assertTrue(ok, det)
        self.assertIn("변경 기록 9/12~10/10 3/3줄 · 스킬 17회·삭제 3", det)      # 9/17 15:30 두 줄 = 같은 분 → 한 줄(2026-10-12)
        self.assertTrue(self.vcheck(self.G0, os.path.join(self.tmp, "없음"))[1])         # 첫 회 — 파일 없음 + '확인 못 함'
        self.assertTrue(self.vcheck(self.G0, None)[1])                                   # --extra 없음
        self.assertFalse(self.vcheck(self.G0, self.extra)[1])                            # 파일이 있는데 '확인 못 함'
        self.assertFalse(self.vcheck(self.G1, None)[1])                                  # 입력이 없는데 값이 있음(옛 값)
        for label, mut in (("노출", lambda h: h.replace('<td class="num">180</td>', '<td class="num">181</td>', 1)),
                           ("기간", lambda h: h.replace("(9/12~10/10 기록", "(9/12~10/11 기록", 1)),
                           ("스킬", lambda h: h.replace("등록 17회(실행 수)", "등록 16회(실행 수)", 1)),
                           ("줄", lambda h: h.replace("On/Off ON → OFF", "On/Off OFF → ON", 1)),
                           ("아이디", lambda h: h.replace("</body>", "<!-- x:naver --></body>", 1)),
                           ("SYSTEM", lambda h: h.replace("<!-- /saero:extra history -->", "하루예산 중단 3회<!-- /saero:extra history -->", 1))):
            with self.subTest(label=label):
                bad = mut(self.G1)
                self.assertNotEqual(bad, self.G1)
                self.assertFalse(self.vcheck(bad, self.extra)[1], label)


if __name__ == "__main__":
    ok = False
    try:
        r = unittest.main(exit=False, verbosity=2)
        ok = r.result.wasSuccessful()
    finally:
        after = {"config": md5f(os.path.join(ROOT, "config", "report-config.json")), "real": tree_md5(REAL),
                 "git": subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout}
        same = after == BEFORE
        print(f"실제 config·~/saero-fetch 추가 보관·원장 md5·저장소 git status 전/후 동일: {same}")
    sys.exit(0 if ok and same else 1)
