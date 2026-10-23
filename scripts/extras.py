#!/usr/bin/env python3
"""추가 수집(보고서 더 받기 A + B, 2026-10-12) — 기존 4개 흐름 옆 줄기: 저장소 밖 보관·변경 이력 원장·합본 + 변경 이력 엑셀 읽기.

기존 4개(fetch 4개 → ingest.sh → data/ → archive.py combine 4종 → compute)의 파일·종료 코드는 그대로다. 이 스크립트는 data/·저장소 작업 트리·git 에
닿지 않는다(쓰는 곳 = config `report_fetch.extras.archive_dir`·`history.ledger` — 저장소 **밖**, 그리고 `combine --out` 의 work/(gitignore)).
표준 라이브러리만(pandas 0 — fetch_reports.py 가 pandas 없는 PC 에서도 import 한다).

하위 명령(작업 폴더 = 저장소 루트, Code 탭 Git Bash — $PY = 저장소 밖 venv 파이썬, references/code-tab.md 1절):
    "$PY" scripts/extras.py store "<성공 폴더>/extra" [--dry-run]
        fetch 가 쓴 summary_extra.json 의 받음(ok) 항목만: A(성별·연령대) CSV → <archive>/YYYY-MM/<종류>.csv(정확한 이름 하나 — 접두 glob·--chunk 0 ·
        두 달 걸침 거부 · 끝이 보관본보다 이르면 거부 · 임시 파일 → 이름 바꾸기 · 옛 파일 .bak) / B 변경이력.csv → 원장 병합(추가만 — 아래).
    "$PY" scripts/extras.py combine --out work/extra [--dry-run]
        A 종류마다 보관 조각을 **일 단위 연속**으로 이어 <out>/<종류>.csv(첫 줄 `"<종류> 합본(시작~끝),<계정>"`) — 빈틈·겹침이면 마지막 연속 구간만 +
        `[주의] <종류> 빈틈 <M/D~M/D> — <시작>부터만`. B 는 원장·기록 구간 사본 <out>/변경이력.csv · <out>/변경이력_기록구간.csv. 시작에 <out> 의 이 이름들만 지운다.
    "$PY" scripts/extras.py seed <변경 이력 xlsx> --start YYYY-MM-DD --end YYYY-MM-DD [--dry-run]
        처음 한 번(사용자 결정 6): 손으로 받은 엑셀(화면 기간 start~end, end = 받은 날)을 원장에 같은 병합으로 넣는다 — 기록 구간 = [start, end − 1].
    경로 덮어쓰기(시험·리허설 전용 — 운영 회차 금지, 명령 첫 줄에 쓰는 경로가 찍힌다): --archive <폴더> · --ledger <파일> 또는 환경 변수
    SAERO_EXTRA_ARCHIVE · SAERO_LEDGER. 저장소 안 경로(work/ 밖)는 쓰지 않는다(`[주의]`).
    종료 코드: store·combine 0 = 끝(문제는 `[주의]` 줄 — 멈춤 아님, 4개 흐름과 무관) · seed 1 = 시드 안 함(`[주의] 시드 안 함: …` — 처음 한 번 손으로 돌리는 명령) ·
    2 = 사용법. 쓰기 실패도 `[주의]`(원장·보관본은 임시 파일 → 이름 바꾸기라 반쪽 0).

원장(B): `<ledger>`(utf-8-sig) 칸 = 일시 · 유형 · 주체 · 캠페인 · 그룹 · 내용 — **변경자 원문(아이디)은 읽는 즉시 주체 낱말(사람/스킬/시스템/기타)로 바꾸고 버린다**.
  추가만 하는 병합: (일시·유형·주체·캠페인·그룹·내용) 같은 줄의 개수를 세어 새 파일 쪽이 많을 때만 그 차이만큼 끝에 더한다(같은 엑셀 두 번 = 0줄) ·
  기존 바이트 그대로(앞 바이트 대조) · 쓰기 전 `.bak-<시각>` · 임시 파일 → 이름 바꾸기. 칸 값은 원문 그대로(앞뒤 공백 그대로 · 줄바꿈만 `\\n` 하나로).
  기록 구간 `<ledger 폴더>/covered.csv`(추가만): 성공한 다운로드마다 [화면 기간 시작, 화면 끝(= 받은 날) − 1] — 원장이 그날까지 다 받았다는 날들.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — 다른 스크립트와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KST = dt.timezone(dt.timedelta(hours=9))
HEAD_RE = re.compile(r"\((\d{4})\.(\d{2})\.(\d{2})\.~(\d{4})\.(\d{2})\.(\d{2})\.\)\s*\"?,\s*(\d+)")  # archive.py·fetch_reports.py 와 같은 식
WHEN_RE = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})\. (\d{2}):(\d{2})$")                           # 변경 이력 `변경일자`(분 단위 — 10/11 실측)
LEDGER_COLS = ["일시", "유형", "주체", "캠페인", "그룹", "내용"]
COVERED_COLS = ["시작", "끝", "출처", "기록 시각"]
HISTORY_FILE = "변경이력.csv"            # fetch 가 <성공 폴더>/extra/ 에 쓰는 아이디 없는 정리본 · combine 의 원장 사본 이름
COVERED_FILE = "변경이력_기록구간.csv"    # combine 의 기록 구간 사본 이름
SUMMARY = "summary_extra.json"
BAD_NAME = re.compile(r'[\\/:*?"<>|]|^\.|^$')


class ExtrasError(ValueError):
    """추가 수집 설정·파일 꼴 문제 — 추가 줄기만 멈춘다(4개 흐름 무관)."""


def load_config():
    """config/report-config.json(pandas 없는 읽기 — fetch_reports.py 폴백과 같은 파일)."""
    with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
        return json.load(f)


def fmt(d):
    return d.strftime("%Y.%m.%d.")


def md(d):
    return f"{d.month}/{d.day}"


def to_date(s):
    """'2026.10.01.' / '2026-10-01' → date."""
    m = re.match(r"^(\d{4})[.-](\d{2})[.-](\d{2})\.?$", s.strip())
    if not m:
        raise ValueError(f"날짜 꼴이 아님: {s!r}")
    return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def now_kst():
    return dt.datetime.now(KST)


# ---------------------------------------------------------------- config(설정 오류는 추가만 끈다 — SystemExit 0)
def _origin(url):
    m = re.match(r"^(https?://[^/?#]+)", url or "")
    return m.group(1).lower() if m else None


def extras_config(rf):
    """config `report_fetch.extras` 검사 → (정리한 dict | None, 경고 줄 목록). 블록이 없으면 (None, []) — 지금과 같음.
    어긋나면(이름·종류가 4개와 겹침 · 종류끼리 접두 · 이름에 금지 낱말 · columns 없음 · URL 없음/다른 출처/쿼리 · 꼴 다름) (None, ['[주의] extras 설정: …'])
    — 추가 수집만 끄고 4개는 그대로(SystemExit 하지 않는다 — S0 의 fetch_config() 포함)."""
    raw = rf.get("extras")
    if raw is None:
        return None, []
    try:
        return _extras_config(rf, raw), []
    except Exception as e:  # noqa: BLE001 — 어떤 꼴 오류든 추가만 끈다
        return None, [f"[주의] extras 설정: {e} — 추가 수집 끔(4개는 그대로)"]


def _extras_config(rf, raw):
    if not isinstance(raw, dict):
        raise ExtrasError("report_fetch.extras 가 객체가 아님")
    four_names = set(rf["report_names"])
    four_kinds = set(rf["columns"]) | set(rf["report_names"].values())
    forbidden = [b for b in rf.get("forbidden_actions", []) if b]
    sub = raw.get("subdir", "extra")
    if not isinstance(sub, str) or BAD_NAME.search(sub) or sub in (".", ".."):
        raise ExtrasError(f"subdir {sub!r} — 하위 폴더 이름 하나여야")
    arch = raw.get("archive_dir")
    if not isinstance(arch, str) or not arch.strip():
        raise ExtrasError("archive_dir 없음")
    out = {"subdir": sub, "archive_dir": arch, "reports": {}, "history": None, "gender_age": None}
    kinds = []
    reports = raw.get("reports") or {}
    if not isinstance(reports, dict):
        raise ExtrasError("reports 가 객체가 아님")
    for name, spec in reports.items():
        if not isinstance(name, str) or not name.strip():
            raise ExtrasError(f"보고서 이름 {name!r}")
        if name in four_names:
            raise ExtrasError(f"보고서 이름 {name!r} 이 기존 4개(report_names)와 겹침")
        bad = [b for b in forbidden if b in name]
        if bad:
            raise ExtrasError(f"보고서 이름 {name!r} 에 금지 낱말 {bad[0]!r}(forbidden_actions) — 그 링크는 클릭하지 않는다")
        if not isinstance(spec, dict):
            raise ExtrasError(f"reports[{name!r}] 가 객체가 아님")
        kind, cols, dim = spec.get("kind"), spec.get("columns"), spec.get("dim")
        if not isinstance(kind, str) or BAD_NAME.search(kind):
            raise ExtrasError(f"reports[{name!r}].kind {kind!r} — 파일 이름으로 쓸 수 있는 낱말이어야")
        if not isinstance(cols, str) or not cols.strip():
            raise ExtrasError(f"reports[{name!r}].columns 없음(다운로드 CSV 2행 원문)")
        if not isinstance(dim, str) or dim not in cols.split(","):
            raise ExtrasError(f"reports[{name!r}].dim {dim!r} 이 columns 칸에 없음")
        if spec.get("every", "daily") != "daily":
            raise ExtrasError(f"reports[{name!r}].every {spec.get('every')!r} — 지금은 daily 만")
        dated = spec.get("dated", True)
        if not isinstance(dated, bool) or (dated and "일별" not in cols.split(",")):
            raise ExtrasError(f"reports[{name!r}].dated {dated!r} — true 면 columns 에 `일별` 칸이 있어야")
        for c in ("노출수", "클릭수", "총비용"):
            if c not in cols.split(","):
                raise ExtrasError(f"reports[{name!r}].columns 에 `{c}` 칸 없음")
        kinds.append(kind)
        out["reports"][name] = {"kind": kind, "columns": cols, "dim": dim, "dated": dated, "every": "daily"}
    h = raw.get("history")
    if h is not None:
        if not isinstance(h, dict):
            raise ExtrasError("history 가 객체가 아님")
        url, kind, cols = h.get("url"), h.get("kind", "변경이력"), h.get("columns")
        if not isinstance(url, str) or not url.strip():
            raise ExtrasError("history.url 없음(변경 이력 관리 주소 — 사용자가 알려 준 경로)")
        if "?" in url or "#" in url:
            raise ExtrasError("history.url 에 쿼리·해시가 있음 — 기간이 붙으면 매일 같은 기간이 뜬다(쿼리 뗀 경로만)")
        if _origin(url) is None or _origin(url) != _origin(rf["list_url"]):
            raise ExtrasError(f"history.url 출처 {_origin(url)!r} ≠ list_url 출처 {_origin(rf['list_url'])!r}")
        if not isinstance(kind, str) or BAD_NAME.search(kind):
            raise ExtrasError(f"history.kind {kind!r}")
        if not isinstance(cols, str) or not cols.strip():
            raise ExtrasError("history.columns 없음(엑셀 머리줄 원문)")
        need = ("변경일자", "변경 유형", "변경자", "캠페인", "광고그룹", "변경 내용")
        miss = [c for c in need if c not in cols.split(",")]
        if miss:
            raise ExtrasError(f"history.columns 에 {miss} 없음")
        rules = h.get("actor_rules")
        if not isinstance(rules, list) or not rules or not all(isinstance(r, list) and len(r) == 2 and all(isinstance(x, str) and x for x in r) for r in rules):
            raise ExtrasError("history.actor_rules — [[끝 글자, 주체 낱말], …] 이어야")
        ledger = h.get("ledger")
        if not isinstance(ledger, str) or not ledger.strip():
            raise ExtrasError("history.ledger 없음")
        show = h.get("show", ["사람"])
        if not isinstance(show, list) or not all(isinstance(x, str) for x in show):
            raise ExtrasError("history.show — 주체 낱말 목록이어야")
        ss, mr = h.get("show_system", False), h.get("max_rows", 10)
        if not isinstance(ss, bool) or isinstance(mr, bool) or not isinstance(mr, int) or mr < 1:
            raise ExtrasError(f"history.show_system {ss!r} · max_rows {mr!r}")
        if h.get("every", "daily") != "daily":
            raise ExtrasError(f"history.every {h.get('every')!r} — 지금은 daily 만")
        kinds.append(kind)
        out["history"] = {"kind": kind, "url": url, "columns": cols, "actor_rules": [list(r) for r in rules], "ledger": ledger,
                          "show": list(show), "show_system": ss, "max_rows": mr, "every": "daily"}
    ga = raw.get("gender_age")
    if out["reports"]:
        if not isinstance(ga, dict):
            raise ExtrasError("gender_age 없음(min_imps · show_unknown · unknown)")
        mi, su, unk = ga.get("min_imps"), ga.get("show_unknown"), ga.get("unknown", "알 수 없음")
        if isinstance(mi, bool) or not isinstance(mi, int) or mi < 0 or not isinstance(su, bool) or not isinstance(unk, str) or not unk:
            raise ExtrasError(f"gender_age min_imps {mi!r} · show_unknown {su!r} · unknown {unk!r}")
        hk = ga.get("hide_unknown_kinds", [])   # 판 J(2026-10-23 결정 8) — show_unknown 이어도 알 수 없음 줄을 빼는 종류(연령대)
        if not isinstance(hk, list) or not all(isinstance(k, str) and k in kinds for k in hk):
            raise ExtrasError(f"gender_age hide_unknown_kinds {hk!r} — reports 종류(kind) 목록이어야")
        out["gender_age"] = {"min_imps": mi, "show_unknown": su, "unknown": unk, "hide_unknown_kinds": list(hk)}
    if len(set(kinds)) != len(kinds):
        raise ExtrasError(f"종류 이름이 겹침: {kinds}")
    for k in kinds:
        if k in four_kinds:
            raise ExtrasError(f"종류 {k!r} 가 기존 4종과 겹침")
        for o in list(four_kinds) + kinds:
            if o != k and (o.startswith(k) or k.startswith(o)):
                raise ExtrasError(f"종류 {k!r} 와 {o!r} 가 접두 관계 — 보관 이름 glob 이 섞일 수 있다")
    if not out["reports"] and out["history"] is None:
        raise ExtrasError("reports·history 둘 다 비었음")
    return out


def archive_dir(ex, override=None):
    return os.path.abspath(os.path.expanduser(override or os.environ.get("SAERO_EXTRA_ARCHIVE") or ex["archive_dir"]))


def ledger_path(ex, override=None):
    return os.path.abspath(os.path.expanduser(override or os.environ.get("SAERO_LEDGER") or ex["history"]["ledger"]))


def covered_path(ledger):
    return os.path.join(os.path.dirname(ledger), "covered.csv")


def path_note(arg, env):
    """첫 줄에 찍을 덮어쓰기 표시(운영 회차에 바뀐 경로를 눈으로 잡는다)."""
    if arg:
        return "(인자로 덮어씀 — 시험·리허설 전용)"
    if os.environ.get(env):
        return f"(환경 변수 {env} 로 덮어씀 — 시험·리허설 전용)"
    return "(config)"


def inside_repo(path):
    """저장소 작업 트리 안(work/ 밖)이면 True — 보관·원장은 저장소 밖이어야(다음 날 S0 `git status --porcelain` · ingest 시작 검사)."""
    p = os.path.normcase(os.path.abspath(path))
    r = os.path.normcase(ROOT)
    w = os.path.normcase(os.path.join(ROOT, "work"))
    return (p == r or p.startswith(r + os.sep)) and not (p == w or p.startswith(w + os.sep))


# ---------------------------------------------------------------- 파일 읽기(공용 — 값 계산 아님)
def read_head(path):
    """CSV 첫 줄 → (원문, 시작 date, 끝 date, 계정). 못 읽으면 ExtrasError."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        line = f.readline().rstrip("\r\n")
    m = HEAD_RE.search(line)
    if not m:
        raise ExtrasError(f"첫 줄 기간 헤더를 읽을 수 없음 — {os.path.basename(path)}")
    g = [int(x) for x in m.groups()[:6]]
    return line, dt.date(*g[:3]), dt.date(*g[3:]), m.group(7)


def read_lines(path):
    """utf-8-sig 텍스트 → 줄 목록(줄 끝 \\n·\\r\\n 떼고). 따옴표 안 줄바꿈이 없는 UI CSV 용."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        return f.read().splitlines()


def read_table(path):
    """머리 한 줄(기간) + 머리줄 + 줄 — 따옴표 안 줄바꿈까지 csv 모듈로. 반환 (첫 줄, 머리줄 list, 줄 list[list])."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        text = f.read()
    first, _, rest = text.partition("\n")
    rows = list(csv.reader(io.StringIO(rest)))
    if not rows:
        return first.rstrip("\r"), [], []
    return first.rstrip("\r"), rows[0], [r for r in rows[1:] if r]


def read_ledger(path):
    """원장 → [(일시, 유형, 주체, 캠페인, 그룹, 내용)]. 없으면 None. 머리줄이 다르면 ExtrasError."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows or rows[0] != LEDGER_COLS:
        raise ExtrasError(f"원장 머리줄이 {LEDGER_COLS} 가 아님 — {path}")
    out = []
    for r in rows[1:]:
        if len(r) != len(LEDGER_COLS):
            raise ExtrasError(f"원장 칸 수 {len(r)} ≠ {len(LEDGER_COLS)} — {path}")
        out.append(tuple(r))
    return out


def read_covered(path):
    """기록 구간 → [(시작 date, 끝 date)] (적힌 순서). 없으면 []."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows or rows[0] != COVERED_COLS:
        raise ExtrasError(f"기록 구간 머리줄이 {COVERED_COLS} 가 아님 — {path}")
    return [(to_date(r[0]), to_date(r[1])) for r in rows[1:] if r]


# ---------------------------------------------------------------- 변경 이력 엑셀(xlsx — 표준 라이브러리 zipfile + xml)
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_PNS = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _text(el):
    """공유 문자열·인라인 문자열 <si>/<is> 의 글자 — 바로 아래 <t> 와 서식 조각 <r><t> 만(<rPh> 읽는 법 표기는 뺀다)."""
    parts = []
    for ch in el:
        if ch.tag == _NS + "t":
            parts.append(ch.text or "")
        elif ch.tag == _NS + "r":
            for t in ch.findall(_NS + "t"):
                parts.append(t.text or "")
    return "".join(parts)


def _clean(s):
    """칸 글자 — 줄바꿈만 \\n 하나로(엑셀 `_x000D_`·CRLF·CR). 앞뒤 공백은 그대로(원장 키 = 칸 원문)."""
    s = s.replace("_x000D_", "")
    return s.replace("\r\n", "\n").replace("\r", "\n")


def read_xlsx_rows(path):
    """첫 시트 → [{열 글자: 값}] 줄 목록(문서 순서). **빈 셀이 아예 빠진 줄(SYSTEM 줄 — 셀 4개)도 셀 `r` 속성의 열 글자로 놓는다**(B-8).
    공유 문자열(t="s")·인라인(inlineStr)·수식 글자(str)·숫자. openpyxl 없음(venv 실측) — zipfile + xml.etree 만."""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        ss = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(_NS + "si"):
                ss.append(_clean(_text(si)))
        sheet = "xl/worksheets/sheet1.xml"
        try:  # 첫 시트의 실제 파일(workbook.xml → rels)
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            rid = wb.find(_NS + "sheets")[0].get(_RNS + "id")
            rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
            for r in rels.findall(_PNS + "Relationship"):
                if r.get("Id") == rid:
                    t = r.get("Target").lstrip("/")
                    sheet = t if t.startswith("xl/") else "xl/" + t
        except Exception:  # noqa: BLE001 — 꼴이 달라도 sheet1 로
            pass
        root = ET.fromstring(z.read(sheet))
    rows = []
    data = root.find(_NS + "sheetData")
    for r in (data.findall(_NS + "row") if data is not None else []):
        cells = {}
        for c in r.findall(_NS + "c"):
            ref = c.get("r") or ""
            m = re.match(r"([A-Z]+)\d*$", ref)
            if not m:
                raise ExtrasError(f"셀 위치(r 속성)를 읽을 수 없음 — 행 {r.get('r')}")
            t, v = c.get("t"), c.find(_NS + "v")
            if t == "s":
                val = ss[int(v.text)] if v is not None and v.text is not None else ""
            elif t == "inlineStr":
                isv = c.find(_NS + "is")
                val = _clean(_text(isv)) if isv is not None else ""
            else:
                val = _clean(v.text or "") if v is not None else ""
            cells[m.group(1)] = val
        rows.append(cells)
    return rows


def _col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def actor_word(raw, rules):
    """변경자 원문 → 주체 낱말(config actor_rules — 앞 규칙부터 끝 글자 맞춤). 안 맞으면 '기타'. 원문은 돌려주지 않는다."""
    for suffix, word in rules:
        if raw.endswith(suffix):
            return word
    return "기타"


def normalize_history(rows, columns, rules):
    """엑셀 줄(read_xlsx_rows) → (원장 줄 [(일시, 유형, 주체, 캠페인, 그룹, 내용)], 경고 목록). 머리줄 ≠ config columns 이면 ExtrasError
    (**셀 원문을 메시지에 넣지 않는다** — 칸 수·다른 자리 수만). 변경자 칸은 주체 낱말로 바꾸고 버린다 · 다른 칸에 아이디 꼴이 있으면 `<ID>` 로 가린다."""
    want = columns.split(",")
    if not rows:
        raise ExtrasError("엑셀에 줄이 없음(머리줄 없음)")
    head = rows[0]
    letters = sorted(head, key=_col_index)
    got = [head[k] for k in letters]
    if got != want:
        diff = sum(1 for a, b in zip(got, want) if a != b) + abs(len(got) - len(want))
        raise ExtrasError(f"엑셀 머리줄이 config history.columns 와 다름(칸 수 {len(got)} ↔ {len(want)} · 다른 자리 {diff}) — 화면·파일 꼴이 바뀐 것 같다")
    pos = {name: letters[i] for i, name in enumerate(want)}
    out, warns, bad_when, other = [], [], 0, 0
    for cells in rows[1:]:
        if not any(v.strip() for v in cells.values()):
            continue
        when = cells.get(pos["변경일자"], "")
        if not WHEN_RE.match(when):
            bad_when += 1
            continue
        raw = cells.get(pos["변경자"], "")
        who = actor_word(raw, rules)
        if who == "기타":
            other += 1
        rec = [when, cells.get(pos["변경 유형"], ""), who, cells.get(pos["캠페인"], ""), cells.get(pos["광고그룹"], ""), cells.get(pos["변경 내용"], "")]
        ident = raw.split(":")[0].strip()
        if len(ident) >= 3 and ident.upper() != "SYSTEM":   # 아이디가 다른 칸에 섞여 있으면 가린다(원장·리포트에 아이디 0)
            rec = [rec[0], rec[1], rec[2]] + [x.replace(ident, "<ID>") for x in rec[3:]]
        out.append(tuple(rec))
    if bad_when:
        raise ExtrasError(f"변경일자 꼴(YYYY.MM.DD. HH:MM)이 아닌 줄 {bad_when}개 — 파일 꼴이 바뀐 것 같다")
    if other:
        warns.append(f"[주의] 변경자 규칙(actor_rules)에 안 맞는 줄 {other}개 — 주체 '기타'로 적음")
    return out, warns


def history_csv_bytes(rows, start, end, account):
    """fetch 가 쓰는 아이디 없는 정리본(<성공 폴더>/extra/변경이력.csv) — 첫 줄 기간 헤더(화면 기간) + 원장 머리줄 + 줄."""
    buf = io.StringIO()
    buf.write(f"\"변경이력({fmt(start)}~{fmt(end)}),{account}\"\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(LEDGER_COLS)
    w.writerows(rows)
    return ("﻿" + buf.getvalue()).encode("utf-8")


def _rows_bytes(rows, header=None):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    if header:
        w.writerow(header)
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


# ---------------------------------------------------------------- 쓰기(임시 파일 → 이름 바꾸기 · 추가만)
def _replace_bytes(path, data):
    """같은 폴더 임시 파일 → os.replace → 다시 읽어 대조."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=folder)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    with open(path, "rb") as f:
        if f.read() != data:
            raise ExtrasError(f"다시 읽은 바이트가 기대와 다름 — {path}")


def _append_only(path, header, rows, stamp):
    """추가만: 옛 바이트 + 새 줄. 옛 파일이 있으면 `.bak-<시각>`('x' — 덮어쓰기 없음) 먼저. 새 파일 = 앞 바이트가 옛 바이트와 같아야."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            old = f.read()
        if old and not old.endswith(b"\n"):
            raise ExtrasError(f"마지막 줄이 줄바꿈으로 끝나지 않음 — 손으로 고친 파일로 보임, 쓰지 않음: {path}")
        bak, n = f"{path}.bak-{stamp}", 1
        while os.path.exists(bak):   # 같은 초에 두 번 쓰면 이름 뒤에 번호(덮어쓰기 없음)
            n += 1
            bak = f"{path}.bak-{stamp}-{n}"
        with open(bak, "xb") as f:
            f.write(old)
        new = old + _rows_bytes(rows)
    else:
        old, bak = b"", None
        new = b"\xef\xbb\xbf" + _rows_bytes(rows, header)
    _replace_bytes(path, new)
    with open(path, "rb") as f:
        if not f.read().startswith(old):
            raise ExtrasError(f"앞 바이트가 바뀜 — {path}")
    return bak


def merge_plan(old_rows, new_rows):
    """추가만 하는 병합 — 같은 줄(6칸 원문)의 개수를 세어 새 쪽이 많은 만큼만(새 파일 순서). 반환 (더할 줄, 이미 있던 줄 수)."""
    have = Counter(old_rows or [])
    seen, add = Counter(), []
    for r in new_rows:
        seen[r] += 1
        if seen[r] > have[r]:
            add.append(r)
    return add, len(new_rows) - len(add)


def merge_history(rows, start, end, ledger, source, dry_run=False, log=print):
    """원장 병합 + 기록 구간 [start, end − 1] 추가. rows = 아이디 없는 원장 줄. 반환 (더한 줄 수, 경고 목록)."""
    warns = []
    if inside_repo(ledger):
        raise ExtrasError(f"원장 경로가 저장소 안(work/ 밖) — 쓰지 않음: {ledger}")
    inwin = [r for r in rows if start <= to_date(r[0][:11]) <= end]
    if len(inwin) != len(rows):
        warns.append(f"[주의] 화면 기간 {md(start)}~{md(end)} 밖 일시 {len(rows) - len(inwin)}줄 — 원장에 넣지 않음")
    old = read_ledger(ledger)
    cov = covered_path(ledger)
    spans = read_covered(cov)
    add, dup = merge_plan(old, inwin)
    if spans:
        last = max(e for _, e in spans)
        if start > last + dt.timedelta(days=1):
            warns.append(f"[주의] 원장 구멍 {md(last + dt.timedelta(days=1))}~{md(start - dt.timedelta(days=1))} — 30일 넘게 받지 못한 날(화면 기간을 바꿔 손으로 받을지는 사용자)")
    cov_end = end - dt.timedelta(days=1)
    stamp = now_kst().strftime("%Y%m%d-%H%M%S")
    if dry_run:
        log(f"[dry-run] 원장 +{len(add)}줄(같은 줄 {dup} 건너뜀) · 기록 구간 +{md(start)}~{md(cov_end)} — 쓰기 0 ({ledger})")
        return len(add), warns
    if add or old is None:
        _append_only(ledger, LEDGER_COLS, add, stamp)
    if cov_end >= start and (start, cov_end) not in spans:   # 같은 구간이 이미 있으면 다시 적지 않는다(추가만 · 같은 날 재실행)
        _append_only(cov, COVERED_COLS, [(start.isoformat(), cov_end.isoformat(), source, now_kst().isoformat(timespec="seconds"))], stamp)
    log(f"[원장] +{len(add)}줄(같은 줄 {dup} 건너뜀 · 원장 {len(old or []) + len(add)}줄) · 기록 구간 +{md(start)}~{md(cov_end)} ({ledger})")
    return len(add), warns


# ---------------------------------------------------------------- store(A 보관 + B 원장)
def store_report(path, name, spec, account, archive, dry_run=False, log=print):
    """A 파일 하나 → <archive>/YYYY-MM/<종류>.csv. 거부는 ExtrasError(그 종류만)."""
    if inside_repo(archive):
        raise ExtrasError(f"보관 경로가 저장소 안(work/ 밖) — 쓰지 않음: {archive}")
    head, s, e, acct = read_head(path)
    if not head.lstrip('"').startswith(name + "("):
        raise ExtrasError(f"첫 줄 이름 ≠ {name!r}")
    if acct != account:
        raise ExtrasError(f"첫 줄 계정 {acct} ≠ config {account}")
    if (s.year, s.month) != (e.year, e.month):
        raise ExtrasError(f"기간 {fmt(s)}~{fmt(e)} 가 두 달에 걸침")
    lines = read_lines(path)
    if len(lines) < 3 or lines[1] != spec["columns"]:
        raise ExtrasError("2행 컬럼 ≠ config columns(또는 데이터 행 없음)")
    kind = spec["kind"]
    dest = os.path.join(archive, f"{s.year:04d}-{s.month:02d}", f"{kind}.csv")
    if os.path.exists(dest):
        _, os_, oe, _ = read_head(dest)
        if e < oe:
            raise ExtrasError(f"기간 끝 {fmt(e)} 가 보관본 끝 {fmt(oe)} 보다 앞섬 — 옛 다운로드로 보임(보관본 그대로)")
    with open(path, "rb") as f:
        data = f.read()
    if dry_run:
        log(f"[dry-run] {kind} → {dest} ({fmt(s)}~{fmt(e)}) — 쓰기 0")
        return dest
    if os.path.exists(dest):
        with open(dest, "rb") as f:
            old = f.read()
        if old != data:
            _replace_bytes(dest + ".bak", old)
    _replace_bytes(dest, data)
    log(f"[추가 보관] {kind} → {dest} ({fmt(s)}~{fmt(e)})")
    return dest


def cmd_store(a, ex, cfg):
    folder = os.path.abspath(a.folder)
    arch = archive_dir(ex, a.archive)
    print(f"[extras store] {folder} · 보관 {arch} {path_note(a.archive, 'SAERO_EXTRA_ARCHIVE')}"
          + (f" · 원장 {ledger_path(ex, a.ledger)} {path_note(a.ledger, 'SAERO_LEDGER')}" if ex["history"] else "")
          + (" · dry-run(쓰기 0)" if a.dry_run else ""))
    sp = os.path.join(folder, SUMMARY)
    try:
        with open(sp, encoding="utf-8") as f:
            summ = json.load(f)
    except (OSError, ValueError) as e:
        print(f"[주의] {SUMMARY} 를 못 읽음({type(e).__name__}) — 추가 보관 없음(4개와 무관): {sp}")
        return 0
    account = str(cfg["report_fetch"]["account_no"])
    n_ok = 0
    by_name = {r.get("name"): r for r in summ.get("reports", [])}
    for name, spec in ex["reports"].items():
        r = by_name.get(name)
        if not r or r.get("status") != "ok" or not r.get("file"):
            print(f"[주의] {spec['kind']}: 이번 수집 {'없음' if not r else r.get('status')} — 보관본 그대로(카드는 보관본 기간으로)")
            continue
        try:
            store_report(os.path.join(folder, r["file"]), name, spec, account, arch, a.dry_run)
            n_ok += 1
        except (ExtrasError, OSError, ValueError) as e:
            print(f"[주의] {spec['kind']} 보관 거부: {e}")
    h = summ.get("history")
    if ex["history"]:
        if not h or h.get("status") != "ok":
            print(f"[주의] 변경 이력: 이번 수집 {'없음' if not h else h.get('status')} — 원장·기록 구간 그대로")
        else:
            try:
                head, s, e, acct = read_head(os.path.join(folder, HISTORY_FILE))
                if acct != account:
                    raise ExtrasError(f"첫 줄 계정 {acct} ≠ config {account}")
                first, cols, rows = read_table(os.path.join(folder, HISTORY_FILE))
                if cols != LEDGER_COLS:
                    raise ExtrasError("정리본 머리줄이 원장 칸과 다름")
                _, warns = merge_history([tuple(r) for r in rows], s, e, ledger_path(ex, a.ledger), f"fetch {summ.get('date', '?')}", a.dry_run)
                for w in warns:
                    print(w)
                n_ok += 1
            except (ExtrasError, OSError, ValueError) as e:
                print(f"[주의] 변경 이력 원장 병합 안 함: {e}")
    print(f"[extras store] 끝 — 처리 {n_ok}건 (다음: extras.py combine --out work/extra)")
    return 0


# ---------------------------------------------------------------- combine(일 단위 연속 — 마지막 연속 구간만)
def runs_of(pieces):
    """[(시작, 끝, …)] 시작순 → 연속 구간 목록 [[조각…]] — 앞 끝 + 1일 = 다음 시작일 때만 잇는다(archive.py:133 과 같은 식). 빈틈·겹침이면 새 구간."""
    runs = []
    for p in sorted(pieces, key=lambda x: (x[0], x[1])):
        if runs and p[0] == runs[-1][-1][1] + dt.timedelta(days=1):
            runs[-1].append(p)
        else:
            runs.append([p])
    return runs


def cmd_combine(a, ex, cfg):
    """combine 본체(_combine)를 감싼다 — 디스크·권한 오류도 `[주의]`(exit 0 — 4개와 무관, 지난 합본 이름은 먼저 지워져 카드는 '확인 못 함')."""
    try:
        return _combine(a, ex, cfg)
    except (OSError, ExtrasError, ValueError) as err:
        print(f"[주의] 추가 합본을 끝내지 못함({type(err).__name__}: {str(err)[:160]}) — 남은 종류는 '확인 못 함'")
        return 0


def _combine(a, ex, cfg):
    out = os.path.abspath(a.out)
    if inside_repo(out):
        raise ExtrasError(f"--out 이 저장소 안(work/ 밖) — 쓰지 않음: {out}")
    arch = archive_dir(ex, a.archive)
    account = str(cfg["report_fetch"]["account_no"])
    print(f"[extras combine] 보관 {arch} {path_note(a.archive, 'SAERO_EXTRA_ARCHIVE')} → {out}" + (" · dry-run(쓰기 0)" if a.dry_run else ""))
    names = [spec["kind"] + ".csv" for spec in ex["reports"].values()] + ([HISTORY_FILE, COVERED_FILE] if ex["history"] else [])
    if not a.dry_run:
        os.makedirs(out, exist_ok=True)
        for n in names:  # 지난 합본이 남아 카드가 옛 값으로 나가는 길 0 — 이 이름들만 지운다
            p = os.path.join(out, n)
            if os.path.exists(p):
                os.remove(p)
    for name, spec in ex["reports"].items():
        kind = spec["kind"]
        pieces = []
        if os.path.isdir(arch):
            for month in sorted(os.listdir(arch)):
                p = os.path.join(arch, month, f"{kind}.csv")   # 정확한 이름 하나(접두 glob 0 — .bak 은 안 읽는다)
                if not os.path.isfile(p):
                    continue
                try:
                    head, s, e, acct = read_head(p)
                    lines = read_lines(p)
                    if acct != account or lines[1] != spec["columns"] or not head.lstrip('"').startswith(name + "("):
                        raise ExtrasError("계정·2행 컬럼·이름이 config 와 다름")
                    pieces.append((s, e, p, lines))
                except (ExtrasError, OSError, IndexError) as err:
                    print(f"[주의] {kind} 보관 조각 {month} 건너뜀: {err}")
        if not pieces:
            print(f"[주의] {kind}: 보관본 없음 — 카드 '확인 못 함'(첫 회·수집 실패)")
            continue
        runs = runs_of(pieces)
        last = runs[-1]
        s0, e0 = last[0][0], last[-1][1]
        if len(runs) > 1:
            prev_end = runs[-2][-1][1]
            if prev_end >= s0:
                gap = f"겹침 {md(s0)}~{md(min(prev_end, e0))}"
            else:
                gap = f"빈틈 {md(prev_end + dt.timedelta(days=1))}~{md(s0 - dt.timedelta(days=1))}"
            print(f"[주의] {kind} {gap} — {md(s0)}부터만")
        body = [f"\"{kind} 합본({fmt(s0)}~{fmt(e0)}),{account}\"", spec["columns"]]
        for s, e, p, lines in last:
            body += [ln for ln in lines[2:] if ln.strip()]
        if a.dry_run:
            print(f"[dry-run] {kind} 합본 {fmt(s0)}~{fmt(e0)} · 조각 {len(last)} · 행 {len(body) - 2} — 쓰기 0")
            continue
        _replace_bytes(os.path.join(out, f"{kind}.csv"), ("﻿" + "\n".join(body) + "\n").encode("utf-8"))
        print(f"[추가 합본] {kind} {fmt(s0)}~{fmt(e0)} · 조각 {len(last)} · 행 {len(body) - 2} → {os.path.join(out, kind + '.csv')}")
    if ex["history"]:
        led = ledger_path(ex, a.ledger)
        try:
            rows = read_ledger(led)
            spans = read_covered(covered_path(led))
        except (ExtrasError, OSError, ValueError) as err:
            print(f"[주의] 변경 이력 원장을 못 읽음 — 표 '확인 못 함': {err}")
            rows, spans = None, []
        if rows is None or not spans:
            print(f"[주의] 변경 이력: 원장{'' if rows is not None else ' 없음'}{' · 기록 구간 없음' if not spans else ''} — 표 '확인 못 함' ({led})")
        elif a.dry_run:
            print(f"[dry-run] 변경 이력 원장 {len(rows)}줄 · 기록 구간 {len(spans)}건(끝 {md(max(e for _, e in spans))}) — 쓰기 0")
        else:  # 원장·기록 구간 바이트 그대로 사본(5단계와 precheck 가 같은 입력을 읽는다)
            for src, dst in ((led, HISTORY_FILE), (covered_path(led), COVERED_FILE)):
                with open(src, "rb") as f:
                    _replace_bytes(os.path.join(out, dst), f.read())
            print(f"[추가 합본] 변경 이력 원장 {len(rows)}줄 · 기록 구간 {len(spans)}건(끝 {md(max(e for _, e in spans))}) → {os.path.join(out, HISTORY_FILE)}")
    print("[extras combine] 끝")
    return 0


def cmd_seed(a, ex, cfg):
    led = ledger_path(ex, a.ledger)
    print(f"[extras seed] {a.xlsx} → 원장 {led} {path_note(a.ledger, 'SAERO_LEDGER')}" + (" · dry-run(쓰기 0)" if a.dry_run else ""))
    try:
        s, e = to_date(a.start), to_date(a.end)
        if s > e:
            raise ExtrasError(f"--start {a.start} > --end {a.end}")
        rows, warns = normalize_history(read_xlsx_rows(a.xlsx), ex["history"]["columns"], ex["history"]["actor_rules"])
        for w in warns:
            print(w)
        _, warns = merge_history(rows, s, e, led, f"seed {os.path.basename(a.xlsx)}", a.dry_run)
        for w in warns:
            print(w)
    except (ExtrasError, OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as err:
        print(f"[주의] 시드 안 함: {err}")
        return 1
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="추가 수집 보관·원장·합본(저장소 밖) — 보고서 더 받기 A + B")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("store", "combine", "seed"):
        p = sub.add_parser(name)
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--archive", help="보관 폴더(시험·리허설 전용 — 운영 금지)")
        p.add_argument("--ledger", help="원장 파일(시험·리허설 전용 — 운영 금지)")
        if name == "store":
            p.add_argument("folder", help="<성공 폴더>/extra")
        elif name == "combine":
            p.add_argument("--out", required=True, help="work/extra")
        else:
            p.add_argument("xlsx")
            p.add_argument("--start", required=True, help="화면 기간 시작 YYYY-MM-DD")
            p.add_argument("--end", required=True, help="화면 기간 끝(= 받은 날) YYYY-MM-DD")
    a = ap.parse_args(argv)
    cfg = load_config()
    rf = cfg.get("report_fetch") or {}
    ex, warns = extras_config(rf) if rf else (None, ["[주의] config report_fetch 없음"])
    for w in warns:
        print(w)
    if ex is None:
        print("[주의] extras 설정 없음·꺼짐 — 할 일 없음(4개 흐름은 그대로)")
        return 0
    if a.cmd == "seed" and not ex["history"]:
        print("[주의] history 설정 없음 — 시드 안 함")
        return 1
    return {"store": cmd_store, "combine": cmd_combine, "seed": cmd_seed}[a.cmd](a, ex, cfg)


if __name__ == "__main__":
    sys.exit(main())
