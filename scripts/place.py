#!/usr/bin/env python3
"""플레이스 화면·소재 손보기 체크리스트(설계안 C — 매출 작업, 2026-10-10) — 사장님이 스마트플레이스에서 바꾼 것을 적고, 효과는 compute.py 플레이스전후가 잰다.
네트워크 0(네이버 호출 없음 — 소재 출처 "스마트플레이스"는 [추론], 리포트에 소재 효과 문장을 쓰지 않는다).

사용법("$PY" = 저장소 밖 venv 파이썬):
    "$PY" scripts/place.py path                                    # 쓰는 체크리스트 경로(--checklist > 환경 변수 SAERO_PLACE > config place_checklist.path)
    "$PY" scripts/place.py status [--combined work/combined]       # 읽기만 — 첫 회 9항목 질문 · 12번 ✗ 항목 · (7) 물을 항목 · 채팅 질문 신호
    "$PY" scripts/place.py set P1=done P2=todo P5=no P6=later:2026-11-01 … [--dry-run]   # 상태(✓ ✗ 안 함 미룸) — 첫 set 은 P1~P9 전부
    "$PY" scripts/place.py done P3 --date 2026-10-12 [--dry-run]   # (7) 답 — 바꾼 날(ISO, 오늘 이하) · 효과 판정 시작
    "$PY" scripts/place.py row --compute work/compute.json         # 12번 플레이스 행들(서술 표지 안쪽) 고정 꼴 — 서술 스크립트가 import 해 써도 된다
  공통: [--checklist <경로>] (시험·리허설은 스크래치 — 운영 기본은 저장소 audit/place-checklist.csv, 첫 실사용이 만든다)

- 체크리스트 = CSV 한 파일, **줄 추가만**(덮어쓰기 0 · 글자 칸 0). 칸: recorded(쓴 날 KST) · id(config items 의 P1~P9) · state(done ✓ · todo ✗ · no 안 함 · later 미룸) ·
  state_date(done = 바꾼 날 — 비면 "처음부터 됨"(판정 안 함) · no·later = 결정한 날) · revisit(later = 다시 볼 날) · in12_since(12번 ✗ 행에 오른 날 — todo 만).
  id 마다 마지막 줄이 지금 상태. 쓸 때마다 12번 ✗ 행(todo 중 config 순서 위 items_in_12 개)을 다시 정해, 상태나 in12_since 가 바뀐 id 의 줄을 덧붙인다.
- 쓰기 전 검사(하나라도 걸리면 [FAIL] 쓰기 0): id 가 config 에 없음 · 상태 낱말 밖 · 날짜가 ISO 아님·미래(바꾼 날)·과거(다시 볼 날) · 첫 set 에 빠진 id ·
  지금과 같은 상태(같은 줄) · 바꾼 날이 지금 기록보다 앞 · 머리줄·줄 꼴 다름. 쓴 뒤 다시 읽어 앞 줄 바이트가 그대로인지 본다.
종료 코드: 0 = 통과(status·row 는 체크리스트 없음·꼴 다름이어도 0 — [주의]) · 1 = [FAIL](쓰기 0) · 2 = 인자.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
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
STATES = ("done", "todo", "no", "later")
HEADER = ["recorded", "id", "state", "state_date", "revisit", "in12_since"]
HEADER_LINE = ",".join(HEADER)


class ChecklistError(ValueError):
    """체크리스트 꼴이 다름·요청이 규칙 밖 — 쓰기 0."""


def pcfg(cfg=None):
    return (cfg or load_config())["place_checklist"]


def checklist_path(arg=None, cfg=None):
    """--checklist > 환경 변수 SAERO_PLACE > config place_checklist.path(상대 경로면 저장소 루트 기준)."""
    p = arg or os.environ.get("SAERO_PLACE") or pcfg(cfg)["path"]
    p = os.path.expanduser(p)
    return os.path.abspath(p if os.path.isabs(p) else os.path.join(ROOT, p))


def md(d):
    return f"{d.month}/{d.day}"


def today_kst():
    return dt.datetime.now(KST).date()


def iso(s, what):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        raise ChecklistError(f"{what} {s!r} — YYYY-MM-DD 만")


# ---------------------------------------------------------------- 읽기
def parse_checklist(text, cfg=None):
    """CSV 글 → 줄 목록(파일 순서) [{recorded, id, state, state_date, revisit, in12_since}] (날짜는 date|None)."""
    ids = [it["id"] for it in pcfg(cfg)["items"]]
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines or lines[0].rstrip("\r") != HEADER_LINE:
        raise ChecklistError(f"머리줄이 다름(기대 `{HEADER_LINE}`)")
    rows = []
    for i, line in enumerate(lines[1:], start=2):
        cells = next(csv.reader([line.rstrip("\r")]))
        if len(cells) != len(HEADER):
            raise ChecklistError(f"{i}번째 줄 칸 수 {len(cells)} ≠ {len(HEADER)}")
        r = dict(zip(HEADER, cells))
        if r["id"] not in ids:
            raise ChecklistError(f"{i}번째 줄 id {r['id']!r} 가 config items 에 없음")
        if r["state"] not in STATES:
            raise ChecklistError(f"{i}번째 줄 state {r['state']!r}")
        out = {"id": r["id"], "state": r["state"]}
        for k in ("recorded", "state_date", "revisit", "in12_since"):
            out[k] = iso(r[k], f"{i}번째 줄 {k}") if r[k] else None
        if out["recorded"] is None:
            raise ChecklistError(f"{i}번째 줄 recorded 가 빔")
        st = out["state"]
        if st in ("no", "later") and out["state_date"] is None:
            raise ChecklistError(f"{i}번째 줄 {st} 인데 state_date(결정한 날)가 빔")
        if (st == "later") != (out["revisit"] is not None):
            raise ChecklistError(f"{i}번째 줄 revisit 은 later 에만")
        if st == "todo" and out["state_date"] is not None:
            raise ChecklistError(f"{i}번째 줄 todo 인데 state_date 가 있음")
        if st != "todo" and out["in12_since"] is not None:
            raise ChecklistError(f"{i}번째 줄 in12_since 는 todo 에만")
        rows.append(out)
    return rows


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def load_checklist(path, cfg=None):
    """(rows, 상태) — 상태 'ok' | '체크리스트 없음' | '꼴 다름: …'. 없음·꼴 다름이면 rows = None."""
    if not os.path.exists(path):
        return None, "체크리스트 없음"
    try:
        return parse_checklist(read_bytes(path).decode("utf-8"), cfg), "ok"
    except (ChecklistError, UnicodeDecodeError, csv.Error, OSError) as e:
        return None, f"꼴 다름: {e}"


def current(rows):
    """{id: 마지막 줄}."""
    cur = {}
    for r in rows:
        cur[r["id"]] = r
    return cur


def done_events(rows):
    """바꾼 날이 있는 done 줄 전부 [(id, date)] — 같은 (id, 날) 은 하나(겹침 판정용 — 지난 바꿈도 센다)."""
    seen = []
    for r in rows:
        if r["state"] == "done" and r["state_date"] and (r["id"], r["state_date"]) not in seen:
            seen.append((r["id"], r["state_date"]))
    return seen


def in12_ids(cur, cfg=None):
    """12번 ✗ 행 — todo 이면서 in12_since 가 있는 id, config 순서, items_in_12 개까지."""
    c = pcfg(cfg)
    return [it["id"] for it in c["items"] if it["id"] in cur and cur[it["id"]]["state"] == "todo"
            and cur[it["id"]]["in12_since"]][: int(c["items_in_12"])]


def wanted_in12(states, cfg=None):
    """상태만으로 정한 12번 ✗ 행(쓸 때 다시 정하는 규칙) — todo 중 config 순서 위 items_in_12 개."""
    c = pcfg(cfg)
    return [it["id"] for it in c["items"] if states.get(it["id"], {}).get("state") == "todo"][: int(c["items_in_12"])]


# ---------------------------------------------------------------- 쓰기
def plan_rows(rows, requests, today, cfg=None, first=False):
    """requests = [(id, state, state_date|None, revisit|None)] → 덧붙일 줄 목록. 규칙 밖이면 ChecklistError."""
    full = cfg or load_config()
    c = pcfg(full)
    ids = [it["id"] for it in c["items"]]
    open_date = dt.date.fromisoformat(full["open_date"].rstrip(".").replace(".", "-"))
    cur = current(rows or [])
    if first:
        missing = [i for i in ids if i not in {r[0] for r in requests}]
        if missing:
            raise ChecklistError(f"첫 set 은 {ids[0]}~{ids[-1]} 전부 — 빠진 id {missing}")
    seen = set()
    new_state = {i: dict(cur[i]) for i in cur}
    changed = []
    for rid, st, sd, rv in requests:
        if rid not in ids:
            raise ChecklistError(f"id {rid!r} 가 config place_checklist.items 에 없음")
        if rid in seen:
            raise ChecklistError(f"id {rid} 를 두 번 줌")
        seen.add(rid)
        if st not in STATES:
            raise ChecklistError(f"{rid} 상태 {st!r} — done·todo·no·later 만")
        if st == "done" and sd is not None:
            if sd > today:
                raise ChecklistError(f"{rid} 바꾼 날 {sd} 가 오늘({today}) 뒤 — 미래 날짜 안 됨")
            if sd < open_date:
                raise ChecklistError(f"{rid} 바꾼 날 {sd} 가 개업일({open_date}) 앞")
        if st == "later" and (rv is None or rv <= today):
            raise ChecklistError(f"{rid} 미룸의 다시 볼 날 {rv} 는 오늘({today}) 뒤여야")
        if st in ("no", "later"):
            sd = today
        old = cur.get(rid)
        if old is not None and old["state"] == st:
            same = f"{rid} 지금과 같은 상태({c['state_words'][st]}) — 같은 줄, 쓰기 0"
            if st in ("todo", "no") or (st == "later" and rv == old["revisit"]):
                raise ChecklistError(same)
            if st == "done":
                if sd is None:
                    raise ChecklistError(same if old["state_date"] is None else
                                         f"{rid} 는 이미 {old['state_date']} 바꿈 기록이 있음 — 다시 바꿨으면 그 날짜로(done {rid} --date)")
                if old["state_date"] is not None and sd <= old["state_date"]:
                    raise ChecklistError(f"{rid} 바꾼 날 {sd} 가 지금 기록({old['state_date']})보다 앞이거나 같음")
        new_state[rid] = {"id": rid, "state": st, "state_date": sd if st != "todo" else None, "revisit": rv if st == "later" else None,
                          "in12_since": None}
        changed.append(rid)
    before12 = set(in12_ids(cur, cfg)) if cur else set()
    after12 = wanted_in12(new_state, cfg)
    out = []
    for it in c["items"]:
        i = it["id"]
        if i not in new_state:
            continue
        s = new_state[i]
        since = None
        if i in after12:
            since = cur[i]["in12_since"] if (i in before12 and i not in changed) else today
        if i in changed or (i in after12) != (i in before12):
            out.append({"recorded": today, "id": i, "state": s["state"], "state_date": s["state_date"], "revisit": s["revisit"], "in12_since": since})
    return out


def line_of(r):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerow([("" if r[k] is None else (r[k].isoformat() if isinstance(r[k], dt.date) else r[k])) for k in HEADER])
    return buf.getvalue()


def append_rows(path, new_rows, cfg=None):
    """줄 추가만 — 처음이면 'x' 모드로 머리줄과 함께. 다시 읽어 앞 바이트가 그대로·새 줄이 끝인지 본다."""
    text = "".join(line_of(r) for r in new_rows)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "x", encoding="utf-8", newline="") as f:
            f.write(HEADER_LINE + "\n" + text)
        before = b""
    else:
        before = read_bytes(path)
        if before and not before.endswith(b"\n"):
            raise ChecklistError("마지막 줄이 줄바꿈으로 끝나지 않음 — 손으로 고친 파일, 쓰지 않음")
        with open(path, "a", encoding="utf-8", newline="") as f:
            f.write(text)
    after = read_bytes(path)
    want = text.encode("utf-8")
    if before and (not after.startswith(before) or after[len(before):] != want):
        raise ChecklistError("다시 읽은 체크리스트가 기대와 다름(앞 줄이 바뀌었거나 새 줄이 끝이 아님)")
    if not before and after != (HEADER_LINE + "\n").encode("utf-8") + want:
        raise ChecklistError("새로 만든 체크리스트를 다시 읽은 바이트가 기대와 다름")
    parse_checklist(after.decode("utf-8"), cfg)


# ---------------------------------------------------------------- 12번 행(서술 표지 안쪽 — 고정 꼴)
def band_text(P):
    b = P["띠"]
    return f"클릭 {b['clicks'][0]:+d}~{b['clicks'][1]:+d}% · CTR {b['ctr'][0]:+d}~{b['ctr'][1]:+d}%"


def rows_html(R):
    """compute.json(R)의 플레이스전후["12번"] → 12번 플레이스 행 안쪽 HTML 목록(순서 그대로). 'M/D까지' = 합본 마지막 날."""
    P = R["플레이스전후"]
    W = P["창일수"]
    out = []
    for it in P["12번"]:
        if it["종류"] == "상태":
            out.append('<span class="tag tag-mint">화면 손보기</span> '
                       f"<b>플레이스 {it['id']} {it['문구']} — {P['기준']} 상태 = {it['값']}</b>"
                       " — 사장님 손(스마트플레이스) · 입찰가·예산 그대로 · 한 번에 하나씩"
                       f'<div class="note" style="margin-top:4px;">다음 회차 판정: 바꾸면 채팅으로 번호·날짜 → 다음 날부터 {W}일 플레이스 검색 지면 '
                       f"하루 클릭·CTR 을 바꾸기 전 {W}일과 비교, 둘 다 띠({band_text(P)}) 위면 좋아짐·둘 다 아래면 나빠짐·그 밖 구별 안 됨</div>")
            continue
        detail = ""
        if "변화%" in it:
            a, b, ch = it["전"], it["후"], it["변화%"]
            detail = (f"(하루 클릭 {a['하루클릭']} → {b['하루클릭']}건 {ch['하루클릭']:+.0f}% · "
                      f"CTR {a['CTR']} → {b['CTR']}% {ch['CTR']:+.0f}%)")
        nxt = (f"{it['끝날']}까지 {W}일이 차면 바꾸기 전 {W}일과 비교" if it["값"].startswith(P["낱말"]["measuring"])
               else f"판정 그대로 — {P['남김일']}일 뒤 12번에서 빼고 이월 판정 줄에 한 번")
        out.append('<span class="tag tag-ink">✓</span> '
                   f"<b>플레이스 {it['id']} {it['문구']} — {it['바꾼날']} 바꿈 · {P['기준']} 판정 = {it['값']}</b>{detail}"
                   f" — 장부 판정 = {P['장부판정']}"
                   f'<div class="note" style="margin-top:4px;">다음 회차 판정: {nxt}</div>')
    return out


# ---------------------------------------------------------------- 명령
def cmd_path(a):
    print(checklist_path(a.checklist))
    return 0


def word_of(c, r):
    w = c["state_words"][r["state"]]
    if r["state"] == "done":
        return w + (f"({md(r['state_date'])} 바꿈)" if r["state_date"] else "(처음부터)")
    if r["state"] == "no":
        return f"{w}({md(r['state_date'])} 결정)"
    if r["state"] == "later":
        return f"{w}({md(r['revisit'])} 다시 봄)"
    return w + (f"(12번 {md(r['in12_since'])}부터)" if r["in12_since"] else "")


def cmd_status(a):
    c = pcfg()
    path = checklist_path(a.checklist)
    try:
        _, dmax, _ = parse_days(read_csv(os.path.join(a.combined, "키워드.csv")))
        end = dmax.date()
    except (OSError, ValueError, KeyError) as e:
        print(f"[FAIL] 합본을 못 읽음({type(e).__name__}): {a.combined}")
        return 1
    rows, st = load_checklist(path)
    print(f"[체크리스트] {path} · 집계 끝 {md(end)}({WD[end.weekday()]})")
    if rows is None:
        if st == "체크리스트 없음":
            print("[체크리스트] 없음 → 첫 회 9항목 질문은 ⓐ 와 별도 메시지(답이 없으면 이번 회차는 12번 플레이스 행 0 · 다음 회차에 다시 묻는다):")
            for it in c["items"]:
                print(f"  {it['id']} {it['문구']} — {it['확인 방법']}")
            print('  답 예: "P1 ✓ P2 ✗ P3 ✗ P4 ✓ P5 안 함 P6 미룸 11/1 P7 ✗ P8 ✓ P9 ✓" → place.py set P1=done P2=todo … P6=later:YYYY-MM-DD --dry-run → 같은 명령에서 --dry-run 빼고')
            print("STATUS first=yes ask7=none chat=none")
        else:
            print(f"[주의] 체크리스트 {st} — 쓰지 않음(손으로 고치지 말고 사용자에게 보고) · 12번 플레이스 행은 compute 가 '확인 못 함'")
            print("STATUS first=no ask7=none chat=broken")
        return 0
    cur = current(rows)
    ids12 = in12_ids(cur)
    for it in c["items"]:
        r = cur.get(it["id"])
        print(f"  {it['id']} {it['문구']}: {word_of(c, r) if r else '(줄 없음)'}")
    chat = []
    for i in ids12:
        since = cur[i]["in12_since"]
        if (end - since).days >= int(c["chat_after_days"]):
            chat.append(f"{i} 12번 {md(since)}부터 {(end - since).days}일 그대로")
    for i, r in cur.items():
        if r["state"] == "later" and r["revisit"] <= end:
            chat.append(f"{i} 미룸 다시 볼 날({md(r['revisit'])}) 지남")
    names = {it["id"]: it["문구"] for it in c["items"]}
    if ids12:
        print("(7) 질문((5) 를 묻는 회차에만 같은 묶음에): 지난주 플레이스에서 바꾼 것 — " + " · ".join(f"{i} {names[i]}" for i in ids12)
              + ' (번호·바꾼 날짜, 없으면 "없음" — 답이 없으면 바꾼 것 없음으로 진행)')
    if chat:
        print("[체크리스트] 채팅 질문 신호(리포트에 또 적기 전에 사용자에게 먼저): " + " / ".join(chat))
    print(f"STATUS first=no ask7={','.join(ids12) or 'none'} chat={len(chat)}")
    return 0


SET_RE = re.compile(r"^(P\d+)=(done|todo|no|later)(?::(\d{4}-\d{2}-\d{2}))?$")


def run_write(a, requests, first_allowed):
    path = checklist_path(a.checklist)
    rows, st = load_checklist(path)
    if rows is None and st != "체크리스트 없음":
        print(f"[FAIL] 체크리스트 {st} — 쓰기 0")
        return 1
    today = dt.date.fromisoformat(a.today) if a.today else today_kst()
    first = rows is None
    if first and not first_allowed:
        print("[FAIL] 체크리스트가 아직 없음 — 첫 회는 set 으로 P1~P9 전부")
        return 1
    try:
        new = plan_rows(rows, requests, today, first=first)
    except ChecklistError as e:
        print(f"[FAIL] {e}")
        return 1
    c = pcfg()
    for r in new:
        print(f"  + {r['id']} {word_of(c, r)}")
    print(f"[체크리스트] {path} · 덧붙일 줄 {len(new)}개" + (" (새 파일)" if first else ""))
    if a.dry_run:
        print("[dry-run] 파일 쓰기 0")
        return 0
    try:
        append_rows(path, new)
    except (ChecklistError, OSError) as e:
        print(f"[FAIL] 체크리스트 쓰기: {e}")
        return 1
    print(f"[추가] {0 if first else len(rows)} → {(0 if first else len(rows)) + len(new)}줄 · 12번 ✗ 행 {in12_ids(current(load_checklist(path)[0]))}")
    return 0


def cmd_set(a):
    reqs = []
    for s in a.items:
        m = SET_RE.match(s)
        if not m:
            print(f"[FAIL] {s!r} — P<n>=done|todo|no|later[:YYYY-MM-DD](done 은 바꾼 날, later 는 다시 볼 날)")
            return 2
        rid, st, d = m.groups()
        try:
            dd = dt.date.fromisoformat(d) if d else None
        except ValueError:
            print(f"[FAIL] {s!r} 날짜가 달력에 없음")
            return 2
        if st in ("todo", "no") and dd is not None:
            print(f"[FAIL] {s!r} — {st} 에는 날짜를 붙이지 않는다(no 의 결정한 날 = 오늘)")
            return 2
        reqs.append((rid, st, dd if st == "done" else None, dd if st == "later" else None))
    return run_write(a, reqs, first_allowed=True)


def cmd_done(a):
    try:
        d = dt.date.fromisoformat(a.date)
    except ValueError:
        print(f"[FAIL] --date {a.date!r} — YYYY-MM-DD 만")
        return 2
    return run_write(a, [(a.id, "done", d, None)], first_allowed=False)


def cmd_row(a):
    with open(a.compute, encoding="utf-8") as f:
        R = json.load(f)
    if "플레이스전후" not in R:
        print("[FAIL] compute.json 에 \"플레이스전후\" 없음 — 5단계 compute 를 --place 와 함께")
        return 1
    for i, h in enumerate(rows_html(R), 1):
        print(f"-- 플레이스 행 {i}\n{h}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="플레이스 화면·소재 손보기 체크리스트(설계안 C) — 네트워크 0")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("path")
    p.add_argument("--checklist")
    p = sub.add_parser("status")
    p.add_argument("--checklist")
    p.add_argument("--combined", default="work/combined")
    p = sub.add_parser("set")
    p.add_argument("items", nargs="+", help="P<n>=done|todo|no|later[:YYYY-MM-DD]")
    p.add_argument("--checklist")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--today", help=argparse.SUPPRESS)  # 시험용(KST 오늘 대신)
    p = sub.add_parser("done")
    p.add_argument("id")
    p.add_argument("--date", required=True, help="바꾼 날 YYYY-MM-DD(오늘 이하)")
    p.add_argument("--checklist")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--today", help=argparse.SUPPRESS)
    p = sub.add_parser("row")
    p.add_argument("--compute", required=True)
    a = ap.parse_args(argv)
    return {"path": cmd_path, "status": cmd_status, "set": cmd_set, "done": cmd_done, "row": cmd_row}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
