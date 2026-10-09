#!/usr/bin/env python3
"""광고비 잔액(비즈머니) 읽기 — 5단계 첫 명령(레이아웃 판 r2026-10-F 광고비 잔액 카드, 2026-10-09).

사용법: "$PY" scripts/balance.py --key-file ~/naver-api.keys.json [--out work/balance.json]

- 네이버 검색광고 API `GET /billing/bizmoney` 를 **한 번** 읽는다(읽기 전용 — POST·DELETE 0). 서명·인증·오류 판정은 scripts/exclusions.py 의
  NaverApi.request · load_keys 를 그대로 쓴다(429 는 거기서 5초 쉬고 1회 재시도).
- 결과를 --out(기본 work/balance.json)에 쓴다 — 다음 명령 `compute.py … --balance work/balance.json` 이 카드 값("잔액")을 만들고 apply 가 카드에 쓴다.
  · 성공: {"status": "ok", "read_at": "<읽은 시각 KST ISO>", "bizmoney": <원 단위 버림>, "bizmoney_raw": <응답 값 그대로>, "budgetLock": …, "refundLock": …}
  · 실패: {"status": "fail", "read_at": "<시도 시각 KST ISO>", "reason": "<범주 한 줄>"} — 카드는 "확인 못 함"(옛 값을 새 시각으로 보이지 않는다).
    실패 = 키 파일 문제 · 네트워크·프록시 · 401·403 · 429(재시도 뒤) · 5xx·그 밖 200 아님 · 요청 결과 모름 · 응답 꼴 다름(dict 아님 · bizmoney 없음 ·
    숫자 아님(bool 포함) · NaN/무한 · 음수 · customerId 가 요청한 고객 번호와 다름).
- **시작하자마자 옛 --out 파일을 지운다** — 이번 실행이 끝까지 가야 다시 생긴다(쓰기에 실패해도 지난 회차 성공 기록이 남지 않는다 — precheck 도장과 같은 원칙).
- 키 값은 출력·json 어디에도 쓰지 않는다: json 의 reason 은 정해진 범주 글뿐(서버 문구 없음), 화면의 세부는 NaverApi._mask 로 가린 뒤 300자.
- 종료 코드: 0 = 기록을 씀(성공·실패 모두 — 조회 실패로 회차를 멈추지 않는다, 사용자 결정 2026-10-09) · 1 = 기록 파일을 못 씀(파일 없음 → compute --balance 가 FAIL) ·
  2 = 인자(argparse).
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

import exclusions as X

URI = "/billing/bizmoney"
WD = "월화수목금토일"


def now_kst():
    return dt.datetime.now(X.KST).replace(microsecond=0)


def shown(t):
    """'10/9(금) 14:34' — 카드 보조 줄과 같은 꼴(분 아래 버림)."""
    return f"{t.month}/{t.day}({WD[t.weekday()]}) {t:%H:%M}"


class Shape(Exception):
    """응답 꼴이 다름 — 숫자를 만들지 않는다."""


def parse(resp, customer_id):
    """응답 dict → (버림 원, 원래 값, budgetLock, refundLock). 꼴이 다르면 Shape."""
    if not isinstance(resp, dict):
        raise Shape(f"dict 아님({type(resp).__name__})")
    if "bizmoney" not in resp:
        raise Shape("bizmoney 칸 없음")
    v = resp["bizmoney"]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise Shape(f"bizmoney 가 숫자 아님({type(v).__name__})")
    if not math.isfinite(v) or v < 0:
        raise Shape(f"bizmoney 값 {v!r}")
    cid = resp.get("customerId")
    if cid is not None and str(cid) != str(customer_id):
        raise Shape("customerId 가 요청한 고객 번호와 다름")
    return int(math.floor(v)), v, resp.get("budgetLock"), resp.get("refundLock")


def read(api):
    """GET 1회 → 기록 dict. 실패도 기록(status fail)으로 돌려준다 — (기록, 화면 세부)."""
    try:
        st, resp = api.request("GET", URI)
    except X.NetworkBlocked as e:
        return {"status": "fail", "read_at": now_kst().isoformat(), "reason": "네트워크 차단(프록시)"}, api._mask(str(e))
    except X.ApiError as e:
        msg = api._mask(str(e))
        if "인증/권한 오류" in msg:
            why = "인증·권한 오류(401/403)"
        elif "요청 결과 모름" in msg:
            why = "요청 결과 모름(응답 도중 끊김·본문 못 읽음)"
        else:
            why = "네트워크 오류"
        return {"status": "fail", "read_at": now_kst().isoformat(), "reason": why}, msg
    except Exception as e:  # 예상 못 한 오류도 "확인 못 함"으로(회차는 계속) — 종류만 보이고 문구는 가린다
        return {"status": "fail", "read_at": now_kst().isoformat(), "reason": f"알 수 없는 오류({type(e).__name__})"}, api._mask(str(e))
    t = now_kst()
    if st != 200:
        why = "429 요청 한도(재시도 1회 뒤)" if st == 429 else (f"서버 오류({st})" if isinstance(st, int) and st >= 500 else f"응답 코드 {st}")
        return {"status": "fail", "read_at": t.isoformat(), "reason": why}, api._mask(json.dumps(resp, ensure_ascii=False))
    try:
        won, raw, bl, rl = parse(resp, api.customer_id)
    except Shape as e:
        return {"status": "fail", "read_at": t.isoformat(), "reason": "응답 꼴 다름"}, api._mask(str(e))
    return {"status": "ok", "read_at": t.isoformat(), "bizmoney": won, "bizmoney_raw": raw, "budgetLock": bl, "refundLock": rl}, ""


def write(path, rec):
    """임시 파일에 쓴 뒤 바꿔 넣는다(반쯤 쓴 파일이 남지 않게)."""
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
    os.replace(tmp, path)


def main(argv=None, sender=None):
    ap = argparse.ArgumentParser(description="광고비 잔액(비즈머니) GET 1회 → work/balance.json(5단계 — 판 F 잔액 카드)")
    ap.add_argument("--key-file", required=True, help="네이버 API 키 파일 경로(값은 열어 출력하지 않는다)")
    ap.add_argument("--out", default="work/balance.json")
    a = ap.parse_args(argv)
    try:
        os.remove(a.out)                      # 옛 기록부터 지운다 — 이번 실행이 끝까지 가야 다시 생긴다
    except FileNotFoundError:
        pass
    except OSError as e:
        print(f"[FAIL] 옛 잔액 기록을 지우지 못함({type(e).__name__}): {a.out} — 손으로 지운 뒤 다시")
        return 1
    api, detail = None, ""
    try:
        key, secret, cid = X.load_keys(a.key_file)
        api = X.NaverApi(key, secret, cid, sender=sender)
    except (SystemExit, OSError, ValueError, AttributeError, TypeError) as e:   # 키 파일 없음·JSON 아님·객체 아님·칸 없음·형식 — load_keys 문구에 값은 없다
        rec = {"status": "fail", "read_at": now_kst().isoformat(), "reason": "키 파일 문제"}
        detail = f"{type(e).__name__}" + (f": {e}" if isinstance(e, SystemExit) else "")
    if api is not None:
        rec, detail = read(api)
    try:
        write(a.out, rec)
    except OSError as e:
        print(f"[FAIL] 잔액 기록을 쓰지 못함({type(e).__name__}): {a.out} — 기록 없음(compute --balance 가 멈춘다)")
        return 1
    calls = len(api.calls) if api is not None else 0
    t = dt.datetime.fromisoformat(rec["read_at"])
    if rec["status"] == "ok":
        print(f"[잔액] {rec['bizmoney']:,}원 · {shown(t)} 기준(KST) · GET {URI} {calls}회 → {a.out}")
    else:
        print(f"[주의] 잔액 확인 못 함({rec['reason']}) — 카드에 \"확인 못 함\"으로 배포(회차는 계속) · {shown(t)} 시도 · GET {URI} {calls}회 → {a.out}"
              + (f"\n  세부: {detail[:300]}" if detail else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
