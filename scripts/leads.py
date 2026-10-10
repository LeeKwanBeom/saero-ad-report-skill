#!/usr/bin/env python3
"""주간 성과 장부(설계안 A — 매출 작업, 2026-10-10) — 광고비 → 문의 → 등록을 사장님 숫자로 잰다. 네트워크 0(네이버·GitHub 호출 없음).

사용법("$PY" = 저장소 밖 venv 파이썬 — references/code-tab.md 1절):
    "$PY" scripts/leads.py path                                   # 쓰는 장부 경로(--ledger > 환경 변수 SAERO_LEADS > config leads.path)
    "$PY" scripts/leads.py status [--combined work/combined] [--numbers]   # 읽기만 — 지난주 입력 여부·(5) 물을지·판정 낱말
    "$PY" scripts/leads.py add --inquiry N --trial N --signup N --naver N [--revenue N] [--place-visit N] [--call N] [--direction N] [--save N] [--dry-run]
    "$PY" scripts/leads.py add … --replace --week YYYY-MM-DD [--dry-run]  # 정정(사용자 "정정" 답이 있을 때만) — 옛 파일은 .bak-<시각>
    "$PY" scripts/leads.py skip [--dry-run]                       # 사용자 "건너뜀" 답 — 숫자 칸 없는 줄(판정에서는 미입력(구멍))
    "$PY" scripts/leads.py guard --staged [--message-file F]      # 스킬 저장소 커밋 전 — staged 추가 줄·커밋 메시지에 장부 숫자가 있으면 [FAIL]
    "$PY" scripts/leads.py row --compute work/compute.json        # 12번 장부 행(서술 표지 안쪽) 고정 꼴 — 서술 스크립트가 import 해 써도 된다
  공통: [--ledger <장부 경로>] (시험·리허설은 스크래치 — 운영 기본은 config leads.path)

- 장부 = CSV 한 파일(저장소 밖). 칸: week(월요일 ISO) · status(ok|skip) · inquiry·trial·signup·naver(필수 숫자) · revenue·place_visit·call·direction·save(선택 숫자) ·
  entered_at(KST ISO). **숫자 칸만 — 글자 칸 0**(이름·전화·메모 없음). 머리줄이 다르거나 줄 꼴이 다르면 "꼴 다름" — 쓰지 않는다.
- **줄 추가만**: add·skip 은 끝에 한 줄을 붙이고(처음이면 'x' 모드로 머리줄과 함께 새 파일) 다시 읽어 앞 줄 바이트가 그대로인지·새 줄이 끝에 있는지 본다.
  같은 주 줄이 이미 있으면 `[FAIL] 같은 주` 쓰기 0. 정정(--replace --week)은 그 주 줄이 있을 때만 — 옛 파일을 `<장부>.bak-<YYYYmmdd-HHMMSS>`('x' 모드 —
  덮어쓰기 없음)로 복사한 뒤 임시 파일 → 바꿔 끼우기 → 다시 읽기.
- 주는 세션이 고르지 않는다(A-F8): add·skip 의 대상 = status 와 같은 '지난주'(합본 키워드 `일별` 마지막 날 = 집계 끝 기준 다 찬 월~일). --week 는 --replace 와 함께만,
  월요일이고 그 주 일요일 ≤ 집계 끝이어야 한다.
- 입력 검사(쓰기 전 — 하나라도 걸리면 [FAIL] 쓰기 0): 10진 숫자만(음수·소수·글자 FAIL) · config leads.max_per_week 초과 · 체험 > 문의 · 등록 > 문의 + 체험 · 네이버 경유 > 등록.
- 판정(compute.py 성과장부와 같은 함수 verdict): config leads 주석 — 판정 전(N/8주) · 미입력(구멍) · 비교 불가 · 좋아짐/나빠짐(포아송 2σ 밖) · 구별 안 됨 · 확인 못 함.
- 공개 범위(publish = verdict): status 의 기본 출력·row·compute.json 에는 판정 낱말만. 건수는 `status --numbers`(채팅)·`add` 출력(채팅)에만 —
  last-audit·커밋 메시지·리포트에 옮기지 않는다. guard 가 그 마지막 관문(라벨+숫자 · 장부 머리줄 · 최근 매출 값).
종료 코드: 0 = 통과(status·row 는 늘 0 — 장부 없음·꼴 다름은 [주의]) · 1 = [FAIL](쓰기 0) · 2 = 인자.
"""
import argparse
import csv
import datetime as dt
import io
import math
import os
import re
import shutil
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — 다른 스크립트와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlib import ROOT, load_config, parse_days, read_csv  # noqa: E402

KST = dt.timezone(dt.timedelta(hours=9))
WD = "월화수목금토일"
FIELDS = ["inquiry", "trial", "signup", "naver", "revenue", "place_visit", "call", "direction", "save"]
HEADER = ["week", "status"] + FIELDS + ["entered_at"]
HEADER_LINE = ",".join(HEADER)


class LedgerError(ValueError):
    """장부 꼴이 다름(머리줄·줄 꼴·같은 주 두 줄) — 판정 '확인 못 함', 쓰기 0."""


# ---------------------------------------------------------------- 설정·경로·주
def lcfg(cfg=None):
    c = (cfg or load_config())["leads"]
    if c.get("week_start") != "월" or c.get("verdict_rule") != "poisson2":
        raise SystemExit("[FAIL] config leads.week_start 는 \"월\", verdict_rule 은 \"poisson2\" 만 — 다른 규칙은 설계 회차 몫")
    return c


def ledger_path(arg=None, cfg=None):
    """--ledger > 환경 변수 SAERO_LEADS > config leads.path(~ 풀기)."""
    p = arg or os.environ.get("SAERO_LEADS") or lcfg(cfg)["path"]
    return os.path.abspath(os.path.expanduser(p))


def md(d):
    return f"{d.month}/{d.day}"


def mdw(d):
    return f"{d.month}/{d.day}({WD[d.weekday()]})"


def week_label(monday):
    return f"{mdw(monday)}~{mdw(monday + dt.timedelta(days=6))}"


def last_full_week(end):
    """집계 끝(date) 기준 다 찬 월~일 주의 월요일 — 일요일 ≤ 집계 끝인 가장 최근 주."""
    sunday = end - dt.timedelta(days=(end.weekday() + 1) % 7)
    return sunday - dt.timedelta(days=6)


def combined_end(combined):
    """합본 키워드 `일별` 마지막 날(date)."""
    _, dmax, _ = parse_days(read_csv(os.path.join(combined, "키워드.csv")))
    return dmax.date()


def now_kst():
    return dt.datetime.now(KST).replace(microsecond=0)


# ---------------------------------------------------------------- 장부 읽기
def parse_ledger(text):
    """CSV 글 → [{week: date, status, 칸: int|None, entered_at}] (주 오름차순). 꼴이 다르면 LedgerError."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines or lines[0].rstrip("\r") != HEADER_LINE:
        raise LedgerError(f"머리줄이 다름(기대 `{HEADER_LINE}`)")
    rows, seen = [], set()
    for i, line in enumerate(lines[1:], start=2):
        cells = next(csv.reader([line.rstrip("\r")]))
        if len(cells) != len(HEADER):
            raise LedgerError(f"{i}번째 줄 칸 수 {len(cells)} ≠ {len(HEADER)}")
        r = dict(zip(HEADER, cells))
        try:
            w = dt.date.fromisoformat(r["week"])
        except ValueError:
            raise LedgerError(f"{i}번째 줄 week 가 날짜가 아님")
        if w.weekday() != 0:
            raise LedgerError(f"{i}번째 줄 week {w} 가 월요일이 아님")
        if w in seen:
            raise LedgerError(f"{i}번째 줄 같은 주 {w} 두 줄")
        seen.add(w)
        st = r["status"]
        out = {"week": w, "status": st, "entered_at": r["entered_at"]}
        for k in FIELDS:
            v = r[k]
            if v == "":
                out[k] = None
            elif re.fullmatch(r"\d+", v):
                out[k] = int(v)
            else:
                raise LedgerError(f"{i}번째 줄 {k} 칸이 숫자가 아님")
        if st == "ok":
            if any(out[k] is None for k in ("inquiry", "trial", "signup", "naver")):
                raise LedgerError(f"{i}번째 줄 ok 인데 필수 칸이 빔")
        elif st == "skip":
            if any(out[k] is not None for k in FIELDS):
                raise LedgerError(f"{i}번째 줄 skip 인데 숫자 칸이 있음")
        else:
            raise LedgerError(f"{i}번째 줄 status {st!r}(ok|skip 만)")
        try:
            dt.datetime.fromisoformat(r["entered_at"])
        except ValueError:
            raise LedgerError(f"{i}번째 줄 entered_at 이 시각이 아님")
        rows.append(out)
    return sorted(rows, key=lambda x: x["week"])


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def load_ledger(path):
    """(rows, 상태) — 상태 'ok' | '장부 없음' | '꼴 다름: …'. 없음·꼴 다름이면 rows = None."""
    if not os.path.exists(path):
        return None, "장부 없음"
    try:
        return parse_ledger(read_bytes(path).decode("utf-8")), "ok"
    except (LedgerError, UnicodeDecodeError, csv.Error, OSError) as e:
        return None, f"꼴 다름: {e}"


# ---------------------------------------------------------------- 판정(compute.py 성과장부와 같은 함수)
def verdict(rows, end, cfg=None):
    """집계 끝(date) 기준 공개 판정 낱말 하나 + 입력 주 수. rows = None 이면 '확인 못 함'."""
    c = lcfg(cfg)
    vw, W, MIN = c["verdict_words"], int(c["window_weeks"]), int(c["min_weeks"])
    if rows is None:
        return vw["unknown"], 0
    last = last_full_week(end)
    rows = [r for r in rows if r["week"] <= last]
    n = len(rows)
    if n < MIN:
        return f"{vw['before']}({n}/{MIN}주)", n
    by = {r["week"]: r for r in rows}
    weeks = [last - dt.timedelta(weeks=i) for i in range(2 * W)]  # 최근 → 과거
    if any(w not in by or by[w]["status"] != "ok" for w in weeks):
        return vw["hole"], n
    recent = sum(by[w]["signup"] for w in weeks[:W])
    prev = sum(by[w]["signup"] for w in weeks[W:])
    if prev == 0:
        return vw["nocompare"], n
    if abs(recent - prev) > 2 * math.sqrt(recent + prev):
        return (vw["up"] if recent > prev else vw["down"]), n
    return vw["same"], n


def verdict_words_all(cfg=None):
    """공개될 수 있는 판정 낱말 전부(시험·validate 의 꼴 대조용) — '판정 전' 은 '(N/8주)' 를 붙인 꼴."""
    c = lcfg(cfg)
    vw = c["verdict_words"]
    return [vw[k] for k in ("hole", "nocompare", "up", "down", "same", "unknown")], vw["before"], int(c["min_weeks"])


# ---------------------------------------------------------------- 공개 범위 가드(라벨+숫자)
def label_regex(labels):
    """장부 라벨 바로 뒤 숫자 — 제외 검색어 문구('등록 N개' · '등록 N · verified' · 'N행')·날짜(M/D · ISO)는 빼고 센다."""
    alt = "|".join(re.escape(x) for x in sorted(labels, key=len, reverse=True))
    return re.compile(rf"(?P<arrow>→\s*)?(?P<lab>{alt})\s*[:=]?\s*(?:약\s*)?(?P<num>\d[\d,]*(?:\.\d+)?)(?![\d,])(?!\s*개)(?!\s*행)(?!\s*·\s*verified)(?![-/]\d)(?P<person>\s*명)?")


def label_hits(text, labels, skip_context=None):
    """[(라벨, 숫자)] — 공개 글에 장부 라벨+숫자가 있으면. 줄 단위로 본다. '등록' 은 제외 검색어 기록과 낱말이 겹쳐 사람 단위 'N명'이 아니면
    ① '→ 등록 N'(8단계 '후보 n → 승인 n → 등록 n' 꼴) ② 제외 검색어 맥락 낱말(config leads.label_skip_context — 제외 검색어·registry·verified·미등록·propose)이 있는 줄
    에서는 세지 않는다. 다른 라벨(문의·체험·상담·매출·네이버 경유 …)은 어느 줄이든 센다."""
    if skip_context is None:
        skip_context = load_config()["leads"].get("label_skip_context", [])
    rx, out = label_regex(labels), []
    for line in text.split("\n"):
        ctx = any(w in line for w in skip_context)
        for m in rx.finditer(line):
            if m["lab"] == "등록" and not m["person"] and (m["arrow"] or ctx):
                continue
            out.append((m["lab"], m["num"]))
    return out


def value_forms(n):
    """매출 같은 큰 값이 글에 실리는 꼴 — 1200000 · 1,200,000 · 120만."""
    forms = {str(n), f"{n:,}"}
    if n % 10000 == 0:
        forms.add(f"{n // 10000:,}만")
        forms.add(f"{n // 10000}만")
    return forms


# ---------------------------------------------------------------- 입력 검사·줄 만들기
def check_values(vals, c):
    """vals = {칸: 문자열|None} → ({칸: int|None}, [FAIL 사유]). 숫자 아님·음수·상한·모순."""
    out, bad = {}, []
    lab = c["field_labels"]
    for k in FIELDS:
        v = vals.get(k)
        if v is None:
            out[k] = None
            continue
        if not re.fullmatch(r"\d+", str(v)):
            bad.append(f"{lab[k]} 칸 {v!r} — 10진 숫자만(음수·소수·글자 안 됨)")
            out[k] = None
            continue
        out[k] = int(v)
        cap = int(c["max_per_week"][k])
        if out[k] > cap:
            bad.append(f"{lab[k]} {out[k]:,} > 상한 {cap:,}(config leads.max_per_week — 오타 막기)")
    for k in c["fields"]["required"]:
        if out.get(k) is None and not any(k in b for b in bad):
            bad.append(f"{lab[k]} 칸이 없음(필수)")
    i, t, s, nv = (out.get(k) for k in ("inquiry", "trial", "signup", "naver"))
    if None not in (i, t, s, nv):
        if t > i:
            bad.append(f"모순: {lab['trial']} > {lab['inquiry']}")
        if s > i + t:
            bad.append(f"모순: {lab['signup']} > {lab['inquiry']} + {lab['trial']}")
        if nv > s:
            bad.append(f"모순: {lab['naver']} > {lab['signup']}")
    return out, bad


def row_line(week, status, nums, at):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerow(
        [week.isoformat(), status] + ["" if nums.get(k) is None else str(nums[k]) for k in FIELDS] + [at.isoformat()])
    return buf.getvalue()


def shown_nums(nums, c):
    lab = c["field_labels"]
    return " · ".join(f"{lab[k]} {nums[k]:,}" for k in FIELDS if nums.get(k) is not None)


# ---------------------------------------------------------------- 쓰기(줄 추가 · 정정)
def append_row(path, line):
    """끝에 한 줄. 처음이면 'x' 모드로 머리줄과 함께. 쓰기 전·뒤 바이트를 대조해 앞 줄이 그대로인지 본다."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "x", encoding="utf-8", newline="") as f:
            f.write(HEADER_LINE + "\n" + line)
        before = b""
    else:
        before = read_bytes(path)
        if before and not before.endswith(b"\n"):
            raise LedgerError("마지막 줄이 줄바꿈으로 끝나지 않음 — 손으로 고친 파일, 쓰지 않음")
        with open(path, "a", encoding="utf-8", newline="") as f:
            f.write(line)
    after = read_bytes(path)
    want_tail = line.encode("utf-8")
    if before and (not after.startswith(before) or after[len(before):] != want_tail):
        raise LedgerError("다시 읽은 장부가 기대와 다름(앞 줄이 바뀌었거나 새 줄이 끝이 아님) — 손대지 말고 사용자에게 보고")
    if not before and after != (HEADER_LINE + "\n").encode("utf-8") + want_tail:
        raise LedgerError("새로 만든 장부를 다시 읽은 바이트가 기대와 다름")
    parse_ledger(after.decode("utf-8"))


def replace_row(path, week, line, now):
    """그 주 줄 하나만 바꾼 새 파일 — 옛 파일은 .bak-<시각>('x' — 덮어쓰기 없음), 임시 파일 → os.replace → 다시 읽기."""
    old = read_bytes(path)
    text = old.decode("utf-8")
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(week.isoformat() + ",")]
    if len(idx) != 1:
        raise LedgerError(f"정정할 주 {week} 줄이 {len(idx)}개(1개여야)")
    lines[idx[0]] = line.rstrip("\n")
    new = "\n".join(lines).encode("utf-8")
    bak = f"{path}.bak-{now:%Y%m%d-%H%M%S}"
    with open(bak, "xb") as f:
        f.write(old)
    if read_bytes(bak) != old:
        raise LedgerError(f"백업 {bak} 를 다시 읽은 바이트가 옛 장부와 다름 — 바꾸지 않음")
    tmp = f"{path}.tmp-{now:%Y%m%d-%H%M%S}"
    with open(tmp, "xb") as f:
        f.write(new)
    os.replace(tmp, path)
    if read_bytes(path) != new:
        raise LedgerError("바꾼 장부를 다시 읽은 바이트가 기대와 다름 — 백업 " + bak)
    parse_ledger(new.decode("utf-8"))
    return bak


# ---------------------------------------------------------------- 12번 행(서술 표지 안쪽 — 고정 꼴)
def row_html(R):
    """compute.json(R)의 성과장부 → 12번 장부 행 안쪽 HTML. 'M/D까지' = 합본 마지막 날(masthead 끝) · 판정 낱말만(숫자 0)."""
    g = R["성과장부"]
    return ('<span class="tag tag-mint">매주</span> '
            f"<b>성과 장부(광고비 → 문의 → 등록) — {g['기준']} 장부 기준 판정 = {g['판정']}</b>"
            f" — 사장님 주간 숫자로 최근 {g['창주']}주 등록 합을 직전 {g['창주']}주와 비교(숫자는 공개하지 않음)"
            f'<div class="note" style="margin-top:4px;">다음 회차 판정: 새 주 장부 입력 뒤 같은 규칙 — 장부 {g["최소주"]}주부터, '
            "차이가 2×√(두 합의 합)을 넘을 때만 좋아짐·나빠짐</div>")


# ---------------------------------------------------------------- 명령
def cmd_path(a):
    print(ledger_path(a.ledger))
    return 0


def week_of_run(a):
    end = combined_end(a.combined)
    return end, last_full_week(end)


def cmd_status(a):
    c = lcfg()
    path = ledger_path(a.ledger)
    end, wk = week_of_run(a)
    rows, st = load_ledger(path)
    word, n = verdict(rows, end)
    print(f"[장부] {path} · 집계 끝 {mdw(end)} · 지난주 {week_label(wk)}")
    if rows is None:
        print(f"[주의] {st} — 판정 '{word}'" + (" (첫 입력 전이면 정상)" if st == "장부 없음" else " — 장부를 손으로 고치지 말고 사용자에게 보고"))
    have = None if rows is None else next((r for r in rows if r["week"] == wk), None)
    ask = have is None and not st.startswith("꼴 다름")  # 꼴 다름이면 물어도 쓸 수 없다 — 보고만
    if have is not None:
        print(f"[장부] 지난주 줄 있음({'입력' if have['status'] == 'ok' else '건너뜀'}) → (5) 묻지 않음")
    elif st.startswith("꼴 다름"):
        print("[장부] 꼴 다름 → (5) 묻지 않음(쓰기 불가 — 사용자에게 보고)")
    else:
        print("[장부] 지난주 줄 없음 → (5) 묻기")
        print("(5) 질문: " + c["question"].format(week=week_label(wk))
              + ' — 이번 주 건너뜀이면 "건너뜀"(답이 없으면 이번 회차는 미입력으로 진행, 다음 회차에 다시 묻는다)')
    print(f"[장부] 판정(공개 낱말): {word} · 입력 주 {n}")
    if a.numbers and rows:
        print("[장부 숫자 — 채팅에만, last-audit·커밋·리포트에 옮기지 않는다]")
        for r in rows[-int(c["min_weeks"]):]:
            print(f"  {week_label(r['week'])}: " + ("건너뜀" if r["status"] == "skip" else shown_nums(r, c)))
    print(f"STATUS ask5={'yes' if ask else 'no'} week={wk.isoformat()} verdict={word}")
    return 0


def collect(a):
    return {k: getattr(a, k) for k in FIELDS}


def cmd_add(a, skip=False):
    c = lcfg()
    path = ledger_path(a.ledger)
    end, wk = week_of_run(a)
    if a.week and not a.replace:
        print("[FAIL] --week 는 --replace(정정)와 함께만 — 새 줄의 주는 status 가 정한 지난주(세션이 고르지 않는다)")
        return 2
    if a.replace:
        if not a.week:
            print("[FAIL] --replace 에는 --week YYYY-MM-DD(정정할 주의 월요일)")
            return 2
        try:
            wk = dt.date.fromisoformat(a.week)
        except ValueError:
            print(f"[FAIL] --week {a.week!r} — YYYY-MM-DD 만")
            return 2
        if wk.weekday() != 0:
            print(f"[FAIL] --week {wk} 가 월요일이 아님({WD[wk.weekday()]}요일)")
            return 1
        if wk + dt.timedelta(days=6) > end:
            print(f"[FAIL] --week {wk} 주의 일요일 {wk + dt.timedelta(days=6)} > 집계 끝 {end} — 다 찬 주만 정정")
            return 1
    nums = {k: None for k in FIELDS}
    if not skip:
        nums, bad = check_values(collect(a), c)
        if bad:
            for b in bad:
                print(f"[FAIL] {b}")
            print("[FAIL] 입력 검사 — 쓰기 0")
            return 1
    elif any(v is not None for v in collect(a).values()):
        print("[FAIL] skip 에는 숫자 칸을 주지 않는다")
        return 2
    rows, st = load_ledger(path)
    if rows is None and st != "장부 없음":
        print(f"[FAIL] 장부 {st} — 쓰기 0(손으로 고치지 말고 사용자에게 보고)")
        return 1
    have = [] if rows is None else [r for r in rows if r["week"] == wk]
    if a.replace and not have:
        print(f"[FAIL] 정정할 주 {week_label(wk)} 줄이 장부에 없음 — 새 줄은 --replace 없이")
        return 1
    if not a.replace and have:
        print(f"[FAIL] 같은 주 {week_label(wk)} 줄이 이미 있음({'입력' if have[0]['status'] == 'ok' else '건너뜀'}) — 쓰기 0. 고치려면 사용자 \"정정\" 답 뒤 --replace --week {wk}")
        return 1
    at = now_kst()
    line = row_line(wk, "skip" if skip else "ok", nums, at)
    what = "건너뜀" if skip else shown_nums(nums, c)
    print(f"[장부] {path} · 주 {week_label(wk)} · {what}")
    if a.dry_run:
        print(f"[dry-run] {'정정' if a.replace else '추가'}할 줄 1개 — 파일 쓰기 0")
        return 0
    try:
        if a.replace:
            bak = replace_row(path, wk, line, at)
            print(f"[정정] {week_label(wk)} 줄을 바꿈 · 옛 장부 {bak}")
        else:
            n0 = 0 if rows is None else len(rows)
            append_row(path, line)
            print(f"[추가] 장부 {n0} → {n0 + 1}줄")
    except (LedgerError, OSError) as e:
        print(f"[FAIL] 장부 쓰기: {e}")
        return 1
    word, n = verdict(load_ledger(path)[0], end)
    print(f"[장부] 판정(공개 낱말): {word} · 입력 주 {n}")
    return 0


def git_out(args, cwd):
    r = subprocess.run(["git", "-c", "core.quotepath=false"] + args, cwd=cwd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace").strip()[:300])
    return r.stdout.decode("utf-8", "replace")


GUARD_SCOPE = re.compile(r"^(audit/|config/|references/|local/|[^/]+\.md$)")
LEDGER_ROW = re.compile(r"^\d{4}-\d{2}-\d{2},(ok|skip),[\d,]*,\d{4}-\d{2}-\d{2}T")  # 장부 데이터 줄 꼴(어느 파일이든 — 장부를 통째로 옮긴 것)


def staged_added(cwd):
    """[(경로, 추가 줄)] — git diff --cached 의 '+' 줄(머리 '+++' 빼고)."""
    out, cur = [], None
    for line in git_out(["diff", "--cached", "-U0", "--no-color", "--no-ext-diff"], cwd).split("\n"):
        if line.startswith("+++ "):
            cur = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("+") and cur is not None:
            out.append((cur, line[1:]))
    return out


def cmd_guard(a):
    c = lcfg()
    if not a.staged:
        print("[FAIL] guard 는 --staged 로(커밋 직전 — git add 경로 지정 뒤)")
        return 2
    cwd = a.repo or os.getcwd()
    try:
        added = staged_added(cwd)
    except (RuntimeError, OSError) as e:
        print(f"[FAIL] git diff --cached 를 못 읽음: {e}")
        return 2
    msg = ""
    if a.message_file:
        with open(a.message_file, encoding="utf-8") as f:
            msg = f.read()
    path = ledger_path(a.ledger)
    rows, st = load_ledger(path)
    values = set()
    if rows:
        last_ok = [r for r in rows if r["status"] == "ok"]
        if last_ok and last_ok[-1].get("revenue") and last_ok[-1]["revenue"] >= int(c["guard_value_min"]):
            values = value_forms(last_ok[-1]["revenue"])
    hits = []
    files = sorted({p for p, _ in added})
    for p, line in added:
        if line.rstrip("\r") == HEADER_LINE or LEDGER_ROW.match(line):
            hits.append(f"{p}: 장부 머리줄·데이터 줄 꼴 — 장부 파일이 staged 에 있음")
        if not GUARD_SCOPE.match(p) or p.lower().endswith(".csv"):
            continue
        for lab, num in label_hits(line, c["public_labels"]):
            hits.append(f"{p}: 장부 라벨+숫자 '{lab} {num}'")
        for v in values:
            if re.search(rf"(?<![\d,]){re.escape(v)}(?![\d,])", line):
                hits.append(f"{p}: 장부 최근 매출 값과 같은 숫자")
    for lab, num in label_hits(msg, c["public_labels"]):
        hits.append(f"커밋 메시지: 장부 라벨+숫자 '{lab} {num}'")
    for v in values:
        if re.search(rf"(?<![\d,]){re.escape(v)}(?![\d,])", msg):
            hits.append("커밋 메시지: 장부 최근 매출 값과 같은 숫자")
    print(f"[guard] staged 파일 {len(files)}개 · 추가 줄 {len(added)} · 커밋 메시지 {'있음' if a.message_file else '없음(--message-file)'} · "
          f"장부 {('값 대조 ' + str(len(values)) + '꼴') if values else st}")
    if hits:
        for h in hits[:30]:
            print(f"[FAIL] {h}")
        print(f"[FAIL] 공개 저장소에 장부 숫자 {len(hits)}곳 — 커밋하지 말고 그 줄을 '(5) 장부 입력됨(로컬)' / '미입력' 꼴로 고쳐 다시 guard")
        return 1
    print("[PASS] guard — staged 추가 줄·커밋 메시지에 장부 숫자 0")
    return 0


def cmd_row(a):
    import json
    with open(a.compute, encoding="utf-8") as f:
        R = json.load(f)
    if "성과장부" not in R:
        print("[FAIL] compute.json 에 \"성과장부\" 없음 — 5단계 compute 를 --leads 와 함께")
        return 1
    print(row_html(R))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="주간 성과 장부(설계안 A) — 네트워크 0")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, combined=True):
        p.add_argument("--ledger", help="장부 경로(기본: 환경 변수 SAERO_LEADS > config leads.path)")
        if combined:
            p.add_argument("--combined", default="work/combined", help="합본 폴더(집계 끝 = 키워드 일별 마지막 날)")

    common(sub.add_parser("path"), combined=False)
    p = sub.add_parser("status")
    common(p)
    p.add_argument("--numbers", action="store_true", help="최근 min_weeks 주 숫자(채팅에만)")
    for name in ("add", "skip"):
        p = sub.add_parser(name)
        common(p)
        for k in FIELDS:
            p.add_argument("--" + k.replace("_", "-"), dest=k)
        p.add_argument("--replace", action="store_true", help="정정 — 사용자 \"정정\" 답이 있을 때만(옛 파일 .bak-<시각>)")
        p.add_argument("--week", help="--replace 와 함께만: 정정할 주의 월요일 YYYY-MM-DD")
        p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("guard")
    common(p, combined=False)
    p.add_argument("--staged", action="store_true")
    p.add_argument("--message-file", help="커밋 메시지 파일(git commit -F 와 같은 파일)")
    p.add_argument("--repo", help="저장소 폴더(기본 지금 폴더)")
    p = sub.add_parser("row")
    p.add_argument("--compute", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "path":
        return cmd_path(a)
    if a.cmd == "status":
        return cmd_status(a)
    if a.cmd == "add":
        return cmd_add(a)
    if a.cmd == "skip":
        return cmd_add(a, skip=True)
    if a.cmd == "guard":
        return cmd_guard(a)
    return cmd_row(a)


if __name__ == "__main__":
    sys.exit(main())
