#!/usr/bin/env python3
"""제외 검색어(파워링크 "확장 검색" 칸) 자동화 — 네이버 검색광고 API 클라이언트 + 등록 상태 registry.

흐름(SKILL.md 5-0단계): 후보 제시(propose) → 사용자 승인 → 쓰기 전 읽기(pull) → 등록(push) → 다시 읽어 확인(verify)
→ 기록(registry = config `exclusions.registry`, 기본 audit/exclusions.csv). "이미 등록했었냐"는 사용자에게 묻지 않고
registry(API·UI 실물)로 판정한다. 등록·삭제는 승인 뒤에만, 읽기는 언제나.

사용법(전부 저장소 루트에서):
    python3 scripts/exclusions.py pull   --key-file <keys.json>            # 3그룹 목록 읽기 → registry 갱신(읽기 전용)
    python3 scripts/exclusions.py import-ui <전사파일> --group <그룹명> [--date YYYY-MM-DD]
                                                                            # API를 못 쓸 때: "기간의 검색어" 화면 전사로 registry 갱신
    python3 scripts/exclusions.py propose <합본폴더> [--day YYYY-MM-DD] [--out <md>]   # 후보·재노출 판정·승인 문구(쓰기 0)
    python3 scripts/exclusions.py push   --approved <파일> --key-file <keys.json> [--dry-run] [--reason "..."]
                                                                            # 승인 목록을 3그룹에 등록. --dry-run은 HTTP 호출 0·파일 변경 0
    python3 scripts/exclusions.py verify --key-file <keys.json> [--approved <파일>]  # 다시 읽어 verified_at 기록, 없으면 실패
    python3 scripts/exclusions.py delete --group <adgroup_id> --ids <id,id> --key-file <keys.json> --confirm [--dry-run]
    python3 scripts/exclusions.py test-roundtrip --keyword <시험문자열> --group <adgroup_id> --key-file <keys.json> --confirm [--dry-run]
                                                                            # 시험 1건: 없음 확인 → 등록 → 확인 → 삭제 → 없음 확인(사용자 입회)
    python3 scripts/exclusions.py report                                    # registry 요약

keys.json: {"api_key": "<엑세스라이선스>", "secret_key": "<비밀키>", "customer_id": 4480035}
  — 저장소·채팅에 두지 않는다. 이 세션에 연결되지 않은 PC 폴더에 두고 경로만 넘긴다. customer_id를 생략하면 config 값.
네트워크가 막힌 환경(프록시 403)에서는 pull/push/verify가 그 사실을 출력하고 exit 2 — 같은 명령을 PC에서 실행한다.
registry 파일이 없거나 못 읽으면 propose/push/verify/delete/test-roundtrip/report는 "[FAIL] registry 없음 … (미확인)" exit 1로 멈춘다
(빈 registry로 판정하면 이력 있는 이름이 신규 후보로 올라오므로). 새로 만드는 명령은 pull·import-ui만.
값의 정의(문서 = 코드): SKILL.md 5-0단계, references/exclusion-ui.md.
"""
import argparse
import base64
import csv
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    from reportlib import ROOT, load_config
except ImportError as _e:  # 사용자 PC(파이썬만 있는 환경)에는 pandas가 없을 수 있다 — reportlib이 맨 위에서 pandas를 import하므로 여기서만 대신 정의(첫 실사용 2026-09-27)
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

CFG = load_config()
EX = CFG["exclusions"]
REG_COLS = ["keyword", "group_id", "group_name", "type", "status", "source", "registered_at",
            "restrict_kwd_id", "verified_at", "note"]
# status: registered(등록 확인) · unregistered(미등록 확인) · pending(등록 요청 성공, 재확인 전) · failed(등록 실패/확인 실패)
#         missing(등록 기록이 있는데 API 목록에 없음) · deleted(삭제) · keep(사용자 결정으로 노출 유지 — 후보에서 제외)
STAR = "*"  # 그룹별 미확인(기록에서 온 행)


def today():
    return dt.date.today().isoformat()


def registry_path(override=None):
    p = override or EX["registry"]
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


# ---------------------------------------------------------------- registry
class RegistryUnavailable(Exception):
    """registry 파일이 없거나 열 수 없다 — 판정 불가(미확인). propose/push/verify/delete/test/report는 여기서 멈춘다."""


def load_registry(path, create_ok=False):
    """registry 읽기. 파일이 없으면 create_ok(pull·import-ui)일 때만 빈 목록, 아니면 RegistryUnavailable."""
    if not os.path.exists(path):
        if create_ok:
            return []
        raise RegistryUnavailable(f"registry 없음: {path} — 등록 상태를 판정할 수 없어(미확인) 멈춥니다. "
                                  "저장소를 통째로 받았는지·--registry 경로가 맞는지 확인. 새로 만드는 명령은 pull·import-ui만")
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames or []
            rows = [dict(r) for r in reader]
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        raise RegistryUnavailable(f"registry를 읽을 수 없음: {path} — {e}")
    if "keyword" not in header or "status" not in header:
        raise RegistryUnavailable(f"registry 형식이 다름: {path} — 열 {header} (필요: {REG_COLS})")
    for r in rows:
        for c in REG_COLS:
            r.setdefault(c, "")
    return rows


def save_registry(path, rows):
    rows.sort(key=lambda r: (r["group_name"] != STAR, r["group_name"], r["keyword"], r["status"]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REG_COLS)
        w.writeheader()
        w.writerows([{c: r.get(c, "") for c in REG_COLS} for r in rows])


def find_row(rows, keyword, group_id=None, group_name=None):
    for r in rows:
        if r["keyword"] != keyword:
            continue
        if group_id and r["group_id"] == group_id:
            return r
        if group_name and norm_name(r["group_name"]) == norm_name(group_name) and (not group_id or not r["group_id"]):
            return r
    return None


def upsert(rows, keyword, group_id, group_name, **fields):
    r = find_row(rows, keyword, group_id=group_id) or find_row(rows, keyword, group_name=group_name)
    if r is None:
        r = {c: "" for c in REG_COLS}
        r.update(keyword=keyword, type=EX["type"])
        rows.append(r)
    if group_id:
        r["group_id"] = group_id
    if group_name:
        r["group_name"] = group_name
    for k, v in fields.items():
        if v is not None:
            r[k] = v
    return r


def targets():
    return list(EX["targets"])


def target_ids():
    return [t["adgroup_id"] for t in targets()]


def group_label(rows, gid):
    for r in rows:
        if r["group_id"] == gid and r["group_name"] and r["group_name"] != STAR:
            return r["group_name"]
    return gid


def norm_name(s):
    """그룹명 대조용 정규화 — 공백만 무시(UI 전사 'A B' ↔ API 'AB'). 그 외 차이는 다른 그룹으로 본다."""
    return re.sub(r"\s+", "", s or "")


def registration_status(rows, keyword):
    """키워드 하나의 등록 상태를 registry로 판정.
    반환: ("registered" | "partial" | "unregistered" | "keep" | "unknown", 등록 그룹 set, 미등록 그룹 set)
    - registered: 3그룹 API 행이 모두 registered, 또는 (미등록 증거 0 이고 등록 증거(API/UI/기록) 1개 이상)
    - partial: 등록 증거와 미등록 증거가 같이 있음(일부 그룹 누락)
    - unregistered: 미등록 증거만 있음
    - keep: 사용자 결정으로 노출 유지
    - unknown: registry에 없음(한 번도 등록·제안된 적 없음)"""
    mine = [r for r in rows if r["keyword"] == keyword]
    if not mine:
        return "unknown", set(), set()
    if any(r["status"] == "keep" for r in mine):
        return "keep", set(), set()
    reg = set(); unreg = set()
    for r in mine:
        g = r["group_name"] if r["group_name"] and r["group_name"] != STAR else (r["group_id"] or STAR)  # 표시는 그룹명(검증 2 참고 ①), 이름 없는 API 행만 ID
        if r["status"] in ("registered", "pending"):
            reg.add(g)
        elif r["status"] in ("unregistered", "missing", "failed"):
            unreg.add(g)
    if unreg and reg:
        return "partial", reg, unreg
    if unreg:
        return "unregistered", reg, unreg
    if reg:
        return "registered", reg, unreg
    return "unknown", reg, unreg  # deleted만 있는 경우 등


# ---------------------------------------------------------------- 금지 패턴
def blocked_reason(keyword):
    """never_exclude_patterns(부분 일치)·competitors 이름 포함이면 이유 문자열, 아니면 None."""
    for p in EX.get("never_exclude_patterns", []):
        if p and p in keyword:
            return f"금지 패턴 '{p}'"
    if EX.get("never_exclude_competitors"):
        for c in CFG.get("competitors", []):
            if c and c in keyword:
                return f"경쟁사명 '{c}'"
    return None


# ---------------------------------------------------------------- API
class ApiError(Exception):
    pass


class NetworkBlocked(ApiError):
    pass


def _default_sender(method, url, headers, data):
    req = urllib.request.Request(url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"message": raw[:500]}
        return e.code, body
    # URLError(프록시 차단·DNS·연결 실패)는 NaverApi._send 가 NetworkBlocked/ApiError 로 바꾼다 — sender 를 바꿔 끼워도 같은 판정


class NaverApi:
    """서명: X-Signature = base64(HMAC-SHA256(secret, "{timestamp}.{METHOD}.{uri}")), uri는 쿼리 제외 경로.
    (naver/searchad-apidoc python-sample/signaturehelper.py·ad_management_sample.py 그대로)"""

    def __init__(self, api_key, secret_key, customer_id, base=None, sender=None, log=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.customer_id = str(customer_id)
        self.base = (base or EX["api_base"]).rstrip("/")
        self.sender = sender or _default_sender
        self.calls = []  # (method, uri) — 테스트·dry-run 검증용
        self.log = log
        self.last_description = None  # 마지막 POST에 실제로 쓴 description(3721 폴백 확인용)

    def sign(self, ts, method, uri):
        msg = f"{ts}.{method}.{uri}".encode("utf-8")
        return base64.b64encode(hmac.new(self.secret_key.encode("utf-8"), msg, hashlib.sha256).digest()).decode()

    def _send(self, method, url, headers, data):
        """sender 호출 한 곳. 연결 자체가 안 되는 URLError(프록시 CONNECT 403·DNS·연결 거부)를
        NetworkBlocked(403/Tunnel/Forbidden) 또는 ApiError 로 바꾼다 — 어떤 sender 를 끼워도 판정이 같다."""
        try:
            return self.sender(method, url, headers, data)
        except urllib.error.HTTPError as e:  # sender 가 HTTPError 를 그대로 올린 경우(기본 sender 는 직접 처리)
            raw = e.read().decode("utf-8", "replace") if hasattr(e, "read") else ""
            try:
                body = json.loads(raw)
            except Exception:
                body = {"message": raw[:500]}
            return e.code, body
        except urllib.error.URLError as e:
            msg = str(e.reason)
            if "403" in msg or "Tunnel" in msg or "Forbidden" in msg:
                raise NetworkBlocked(f"네트워크 차단(프록시): {msg} — 같은 명령을 PC에서 실행하세요")
            raise ApiError(f"네트워크 오류: {msg}")

    def request(self, method, uri, params=None, body=None):
        ts = str(round(time.time() * 1000))
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Timestamp": ts, "X-API-KEY": self.api_key,
                   "X-Customer": self.customer_id, "X-Signature": self.sign(ts, method, uri)}
        url = self.base + uri + ("?" + urllib.parse.urlencode(params) if params else "")
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        self.calls.append((method, uri))
        status, resp = self._send(method, url, headers, data)
        if status == 429:  # 키워드 도구 429 가이드(2020-12-18 공지): 쉬었다 1회 재시도
            time.sleep(5)
            ts = str(round(time.time() * 1000))
            headers.update({"X-Timestamp": ts, "X-Signature": self.sign(ts, method, uri)})
            self.calls.append((method, uri))
            status, resp = self._send(method, url, headers, data)
        if status in (401, 403):
            raise ApiError(f"{method} {uri} → {status} 인증/권한 오류: {json.dumps(resp, ensure_ascii=False)[:300]}")
        return status, resp

    # --- 광고그룹·제외 검색어
    def adgroup(self, gid):
        st, r = self.request("GET", f"/ncc/adgroups/{gid}")
        if st != 200:
            raise ApiError(f"GET adgroup {gid} → {st}: {json.dumps(r, ensure_ascii=False)[:300]}")
        return r

    def restricted(self, gid):
        st, r = self.request("GET", f"/ncc/adgroups/{gid}/restricted-keywords", params={"type": EX["type"]})
        if st != 200:
            raise ApiError(f"GET restricted-keywords {gid} → {st}: {json.dumps(r, ensure_ascii=False)[:300]}")
        return r or []

    def add_restricted(self, gid, keywords, description):
        """POST. description 은 식별용(선택) — 한도가 문서에 없고 3721(설명 최대 길이 초과, 첫 실사용 2026-09-27: 29자에서 발생)이 오면
        짧은 것 → 없음 순으로 물러선다(이름 등록이 목적이지 설명이 목적이 아니다). 실제로 쓴 값은 self.last_description."""
        tried = []
        chain = []
        for d in (description or "", short_description(description), ""):
            if d not in chain:
                chain.append(d)
        for desc in chain:
            body = [dict({"keyword": k, "type": EX["type"]}, **({"description": desc} if desc else {})) for k in keywords]
            st, r = self.request("POST", f"/ncc/adgroups/{gid}/restricted-keywords", body=body)
            if st in (200, 201):
                self.last_description = desc
                return r or []
            code = str((r or {}).get("code")) if isinstance(r, dict) else ""
            tried.append((desc, st, code))
            if st == 400 and code == "3721" and desc != "":
                continue  # 설명이 길다 — 더 짧게
            raise ApiError(f"POST restricted-keywords {gid} → {st}: {json.dumps(r, ensure_ascii=False)[:500]}")
        raise ApiError(f"POST restricted-keywords {gid}: description 시도 전부 실패 {tried}")

    def delete_restricted(self, gid, ids):
        st, r = self.request("DELETE", f"/ncc/adgroups/{gid}/restricted-keywords", params={"ids": ",".join(ids)})
        if st not in (200, 204):
            raise ApiError(f"DELETE restricted-keywords {gid} → {st}: {json.dumps(r, ensure_ascii=False)[:300]}")
        return True


def short_description(description):
    """3721 폴백용 짧은 설명 — 첫 낱말(prefix)만. 예 'saero 09-27' → 'saero'."""
    return (description or "").split(" ")[0][:10]


def default_description(kind=""):
    """등록 설명 기본값 — 짧게: '<prefix> [kind ]MM-DD' (예 'saero 09-27', 'saero test 09-27'). 첫 실사용에서 29자짜리가 3721로 거부됐다."""
    prefix = EX.get("description_prefix", "saero")
    return f"{prefix} {kind + ' ' if kind else ''}{today()[5:]}"


def load_keys(path):
    with open(path, encoding="utf-8") as f:
        k = json.load(f)
    for need in ("api_key", "secret_key"):
        if not k.get(need):
            raise SystemExit(f"키 파일에 {need}가 없습니다: {path}")
    return k["api_key"], k["secret_key"], k.get("customer_id") or EX["customer_id"]


def api_from_args(a):
    if not a.key_file:
        raise SystemExit("--key-file <keys.json> 이 필요합니다(저장소·채팅에 두지 말 것)")
    key, secret, cid = load_keys(a.key_file)
    return NaverApi(key, secret, cid)


KST = dt.timezone(dt.timedelta(hours=9))


def regtm_to_date(s):
    """API regTm(UTC, 예 2026-09-16T23:40:12.000Z) → **KST 날짜**. 검색어 CSV의 '일별'이 KST라 등록 당일 판정은 KST로 해야 맞다
    (첫 실사용 2026-09-27: UTC 날짜로 두면 09-17 오전 등록분이 09-16으로 잡혀 09-17 노출이 "등록돼 있는데도 노출"이 된다)."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?", str(s or ""))
    if not m:
        return ""
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if m.group(4) is None:
        return f"{y:04d}-{mo:02d}-{d:02d}"
    t = dt.datetime(y, mo, d, int(m.group(4)), int(m.group(5)), int(m.group(6) or 0), tzinfo=dt.timezone.utc)
    return t.astimezone(KST).date().isoformat()


# ---------------------------------------------------------------- pull (읽기)
def write_snapshot(out):
    """pull 결과를 work/exclusions_pull_<날짜>.json 에 — Claude가 읽는 파일. 그룹별 이름 목록 + 이름별 {id, regTm(원문 UTC), 등록일(KST)}. 반환 경로."""
    snap = os.path.join(ROOT, "work", f"exclusions_pull_{today()}.json")
    os.makedirs(os.path.dirname(snap), exist_ok=True)
    data = {}
    for g, v in out.items():
        items = {k: {"id": it.get("nccAdgroupRestrictKwdId", ""), "regTm": it.get("regTm", ""), "registered_at": regtm_to_date(it.get("regTm"))}
                 for k, it in v["keywords"].items()}
        data[g] = {"name": v["name"], "count": len(items), "keywords": sorted(items), "items": items}
    with open(snap, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return snap


def do_pull(api, rows, log=print, gids=None, mark_missing=True, snapshot=False):
    """3그룹 GET → registry 갱신. 반환: {gid: {"name":…, "keywords": {kw: item}, "adgroup": {...}}}. snapshot=True면 work/ 스냅샷도 쓴다."""
    out = {}
    stamp = today()
    for gid in (gids or target_ids()):
        ag = api.adgroup(gid)
        name = ag.get("name", gid)
        items = api.restricted(gid)
        kws = {}
        for it in items:
            kw = it.get("keyword", "")
            if not kw or it.get("type", EX["type"]) != EX["type"]:
                continue
            kws[kw] = it
            upsert(rows, kw, gid, name, status="registered", source="api",
                   registered_at=regtm_to_date(it.get("regTm")) or None, restrict_kwd_id=it.get("nccAdgroupRestrictKwdId", ""),
                   verified_at=stamp)
        # 이 그룹에 등록됐다고 적혀 있는데 API 목록에 없는 행 → missing
        for r in rows:
            same_group = (r["group_id"] == gid) or (not r["group_id"] and norm_name(r["group_name"]) == norm_name(name))
            if same_group and not r["group_id"]:
                r["group_id"] = gid  # UI 전사 행에 그룹 ID를 채운다(이름 정규화 일치)
            if mark_missing and same_group and r["status"] in ("registered", "pending") and r["keyword"] not in kws:
                r["status"] = "missing"
                r["note"] = (r["note"] + " | " if r["note"] else "") + f"{stamp} API 목록에 없음"
        advoost = ag.get("useAdvoost")
        out[gid] = {"name": name, "keywords": kws, "adgroup": ag}
        log(f"[pull] {name}({gid}): 확장 검색 제외 {len(kws)}개 · userLock={ag.get('userLock')} · useExpSearch={ag.get('useExpSearch')}"
            + (f" · useAdvoost={advoost}(ON이면 등록 거부됨: 오류 3754/4422)" if advoost is not None else ""))
        if ag.get("userLock") or name in CFG.get("excluded_groups", []):
            log(f"[pull] [주의] {name}: userLock={ag.get('userLock')} 또는 config excluded_groups에 있음 — OFF·제외 그룹이면 config targets에서 빼야 한다")
    # registry의 UI 그룹명 중 API 그룹명과 하나도 안 맞는 것 → 경고(등록 상태가 영원히 어긋난다)
    api_names = {norm_name(v["name"]) for v in out.values()}
    stray = sorted({r["group_name"] for r in rows if r["group_name"] and r["group_name"] != STAR and not r["group_id"]
                    and norm_name(r["group_name"]) not in api_names})
    if stray and (gids is None or set(gids) >= set(target_ids())):
        log(f"[pull] [주의] registry 그룹명 {', '.join(stray)} 은(는) API 그룹명 {', '.join(v['name'] for v in out.values())} 과 맞지 않음 — registry 그룹명을 API 이름으로 고치거나 targets를 확인")
    # 기록 행(*, 그룹 미확인): 3그룹을 다 읽었으면 API가 정본 — 그룹별 행으로 풀고 * 행은 지운다(첫 실사용 2026-09-27: 읽은 뒤에는 "그룹 미확인"이 남을 이유가 없다)
    #   · 3그룹 모두 등록 → API 행이 이미 있으니 그냥 제거
    #   · 없는 그룹이 있음 → 그 그룹에 명시 행: * 행이 registered/pending이면 missing(기록엔 등록인데 실물에 없음), keep은 keep, 그 외(unregistered 등)는 unregistered
    if set(out) >= set(target_ids()):
        for r in [r for r in rows if r["group_name"] == STAR]:
            lacking = [g for g in target_ids() if r["keyword"] not in out[g]["keywords"]]
            new_status = "missing" if r["status"] in ("registered", "pending") else ("keep" if r["status"] == "keep" else "unregistered")
            for g in lacking:
                if find_row(rows, r["keyword"], group_id=g) is None:  # 그 그룹 행이 이미 있으면(UI 전사 등) 그대로 둔다
                    upsert(rows, r["keyword"], g, out[g]["name"], status=new_status, source="api", verified_at=stamp,
                           registered_at=r["registered_at"] or None,
                           note=(f"{stamp} API 확인: 이 그룹에 없음" + (f" | 기록: {r['note']}" if r["note"] else ""))[:300])
        rows[:] = [r for r in rows if r["group_name"] != STAR]
    if snapshot:
        log(f"[pull] 스냅샷 {write_snapshot(out)}")
    return out


def cmd_pull(a):
    api = api_from_args(a)
    path = registry_path(a.registry)
    rows = load_registry(path, create_ok=True)  # pull은 registry를 새로 만들 수 있는 명령
    try:
        do_pull(api, rows, snapshot=True)
    except NetworkBlocked as e:
        print(f"[FAIL] {e}")
        return 2
    except ApiError as e:  # 인증·권한·응답 오류 — registry는 건드리지 않는다
        print(f"[FAIL] {e}")
        return 1
    save_registry(path, rows)
    print(f"[pull] registry 갱신 {path} ({len(rows)}행)")
    return 0


# ---------------------------------------------------------------- import-ui (읽기 폴백)
UI_LINE = re.compile(r"^(?:(\d+)\|)?(이미등록|\+?추가)\|([^|]+)\|([^|]*)\|?(.*)$")


def parse_ui_lines(text):
    """"페이지|상태|검색어|검색유형|노출|클릭|비용" 또는 "상태|검색어|검색유형" 형식. 반환 [(status, keyword, type)]"""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = UI_LINE.match(line)
        if not m:
            continue
        st = "이미등록" if m.group(2) == "이미등록" else "+추가"
        out.append((st, m.group(3).strip(), (m.group(4) or "확장").strip()))
    return out


def do_import_ui(rows, parsed, group_name, date):
    n_reg = n_unreg = 0
    for st, kw, ty in parsed:
        if ty != "확장":
            continue
        if st == "이미등록":
            upsert(rows, kw, None, group_name, status="registered", source="ui", verified_at=date)
            n_reg += 1
        elif any(r["keyword"] == kw for r in rows):  # 기록·제안에 있던 이름만 미등록으로 기록(그 외 +추가는 일반 검색어)
            upsert(rows, kw, None, group_name, status="unregistered", source="ui", verified_at=date)
            n_unreg += 1
    return n_reg, n_unreg


def cmd_import_ui(a):
    path = registry_path(a.registry)
    rows = load_registry(path, create_ok=True)  # import-ui도 registry를 새로 만들 수 있다(첫 UI 전사)
    with open(a.file, encoding="utf-8") as f:
        parsed = parse_ui_lines(f.read())
    n_reg, n_unreg = do_import_ui(rows, parsed, a.group, a.date or today())
    save_registry(path, rows)
    print(f"[import-ui] {a.group}: 이미등록 {n_reg} · 미등록(기록 이름) {n_unreg} → {path} ({len(rows)}행)")
    return 0


# ---------------------------------------------------------------- propose (쓰기 0)
def load_search_terms(combined_dir):
    import pandas as pd
    sr = pd.read_csv(os.path.join(combined_dir, "검색어.csv"), skiprows=1)
    sr["d"] = sr["일별"].astype(str).str.rstrip(".").map(lambda s: dt.date(*[int(x) for x in s.split(".")]))
    return sr


def failure_note(rows, keyword):
    """직전 등록·확인 실패 사유(failed 행 note) — 재등록 후보 옆에 보여 사용자가 keep(제외)할지 정하게."""
    notes = sorted({r["note"] for r in rows if r["keyword"] == keyword and r["status"] == "failed" and r["note"]})
    return " / ".join(notes)[:200]


def fmt_groups(gs):
    return ", ".join("기록(그룹 미확인)" if g == STAR else g for g in sorted(gs)) or "-"


def reexposure_judgement(rows, keyword, exposure_days):
    """(판정 문자열, 근거) — 등록일 다음 날 이후 확장 노출이 있는 이름에 대해."""
    status, reg, unreg = registration_status(rows, keyword)
    if status == "registered":
        dates = [r["registered_at"] for r in rows if r["keyword"] == keyword and r["registered_at"]]
        rd = max(dates) if dates else ""  # 재등록이 있으면 마지막 등록일 기준
        if not rd:
            return "등록됨(등록일 미상)", ""
        after = [d for d in exposure_days if d.isoformat() > rd]
        same = [d for d in exposure_days if d.isoformat() == rd]
        if after:
            return "등록돼 있는데도 노출", f"등록 {rd} · 노출일 {', '.join(x.isoformat() for x in after)}"
        if same:
            return "등록 당일(판정 안 함)", f"등록 {rd}"
        return "등록 전 노출(정상)", f"등록 {rd}"
    if status == "partial":
        return "일부 그룹 미등록 → 후보", f"등록 {fmt_groups(reg)} / 미등록 {fmt_groups(unreg)}"
    if status == "unregistered":
        return "등록 누락 → 후보", f"미등록 {fmt_groups(unreg)}"
    if status == "keep":
        return "노출 유지(사용자 결정)", ""
    return "이력 없음(registry에 없는 이름)", ""


def build_proposal(rows, sr, day=None, since=None, first_seen_only=True):
    """반환 dict: window, new(신규 후보), rereg(재등록 후보), blocked, already, reexposed, approval_text, candidates(list)"""
    last = sr["d"].max()
    if since:
        lo, hi = dt.date.fromisoformat(since), last
    else:
        hi = dt.date.fromisoformat(day) if day else last
        lo = hi
    win = sr[(sr["d"] >= lo) & (sr["d"] <= hi)]
    ext = win[win["검색 유형"] == "확장"]
    first_seen = sr.groupby("검색어")["d"].min()
    agg = ext.groupby("검색어").agg(imp=("노출수", "sum"), clk=("클릭수", "sum"), days=("d", lambda s: sorted(set(s))))
    new, industry, blocked, already, reexposed, rereg_names = [], [], [], [], [], set()
    n_registered = 0  # 창 안에 나왔지만 이미 등록돼 있어 후보가 아닌 이름 수(승인 문구 "이미 등록 m")
    for kw, r in agg.iterrows():
        status, reg, unreg = registration_status(rows, kw)
        judge, why = reexposure_judgement(rows, kw, r["days"])
        if status in ("registered", "partial", "unregistered"):
            reexposed.append((kw, int(r["imp"]), judge, why))
            if status in ("partial", "unregistered"):
                rereg_names.add(kw)
            else:
                n_registered += 1
            continue
        if status == "keep":
            already.append((kw, int(r["imp"]), "노출 유지(사용자 결정)"))
            continue
        if int(r["clk"]) > 0:
            continue  # 클릭이 있는 검색어는 자동 후보로 올리지 않는다(사람이 07번 표에서 판단)
        why_b = blocked_reason(kw)
        if why_b:
            blocked.append((kw, int(r["imp"]), why_b))
            continue
        fs = first_seen.get(kw)
        if first_seen_only and fs is not None and fs < lo:
            continue  # 이전에도 나왔던 이름은 그때 판단이 끝난 것으로 본다(--all로 포함)
        entry = (kw, int(r["imp"]), fs.isoformat() if fs is not None else "")
        if any(t and t in kw for t in EX.get("industry_terms", [])):
            industry.append(entry)  # 업종어 포함 — 기본 후보 아님, 사용자가 고르면 승인 목록에 넣는다
        else:
            new.append(entry)
    # 재등록 후보: registry에 미등록·누락·등록 실패로 적힌 이름 전부(이번 창에 안 나온 것 포함) — 실패한 이름도 조용히 사라지지 않는다
    rereg = []
    for kw in sorted({r["keyword"] for r in rows if r["status"] in ("unregistered", "missing", "partial", "failed")} | rereg_names):
        status, reg, unreg = registration_status(rows, kw)
        if status in ("unregistered", "partial"):
            if blocked_reason(kw):
                blocked.append((kw, 0, blocked_reason(kw) + "(등록 기록 있음 — 사용자 확인)"))
                continue
            rereg.append((kw, sorted(unreg), failure_note(rows, kw)))
    new.sort(key=lambda x: (-x[1], x[0]))
    industry.sort(key=lambda x: (-x[1], x[0]))
    cands = [k for k, _, _ in new] + [k for k, _, _ in rereg if k not in {n[0] for n in new}]
    names = [group_label(rows, t["adgroup_id"]) for t in targets()]
    if all(n == t["adgroup_id"] for n, t in zip(names, targets())):  # 첫 pull 전: registry의 그룹명(UI 전사)으로 표기
        names = sorted({r["group_name"] for r in rows if r["group_name"] != STAR}) or names
    text = ("제외 검색어 등록 승인 요청 — 대상: 파워링크 3그룹(" + ", ".join(names) + ') "확장 검색" 칸 / '
            f"건수: {len(cands)} / 목록: " + " · ".join(cands) +
            f" / 제외한 것: 금지 패턴·경쟁사 {len(blocked)} · 이미 등록 {n_registered} · 노출 유지(사용자 결정) {len(already)}\n"
            '답: "등록 승인 N개" (뺄 이름이 있으면 적어 주세요 — 그만큼 뺀 뒤 다시 확인합니다). 답이 오기 전에는 아무것도 등록하지 않습니다.')
    return dict(window=(lo, hi), new=new, industry=industry, rereg=rereg, blocked=blocked, already=already,
                reexposed=reexposed, candidates=cands, approval_text=text, n_registered=n_registered)


def render_proposal(p):
    lo, hi = p["window"]
    L = [f"# 제외 검색어 제안 — 검색어 CSV `확장` 행, 창 {lo}~{hi} (생성 {today()})", ""]
    L.append(f"## 신규 후보 {len(p['new'])}개 (창 안 첫 등장 · 클릭 0 · 금지 패턴·경쟁사·등록 이력 없음) — 무관/애매/키즈 분류는 채팅에서")
    L += [f"- {k} — 노출 {imp} · 첫 등장 {fs}" for k, imp, fs in p["new"]] or ["- (없음)"]
    L.append(f"\n## 업종어 포함 {len(p['industry'])}개 (config industry_terms — 기본 후보 아님, 뺄 이름은 사용자가 고른다)")
    L += [f"- {k} — 노출 {imp} · 첫 등장 {fs}" for k, imp, fs in p["industry"]] or ["- (없음)"]
    L.append(f"\n## 재등록 후보 {len(p['rereg'])}개 (registry에 미등록·일부 그룹 누락·등록 실패로 기록된 이름)")
    L += [f"- {k} — 미등록 {fmt_groups(g)}" + (f" — **직전 실패**: {why} (반복 실패면 registry status=keep으로 제외)" if why else "")
          for k, g, why in p["rereg"]] or ["- (없음)"]
    L.append(f"\n## 재노출 판정 {len(p['reexposed'])}건 (등록 이력이 있는 이름의 창 안 확장 노출)")
    L += [f"- {k} — 노출 {imp} — **{j}** {w}" for k, imp, j, w in p["reexposed"]] or ["- (없음)"]
    L.append(f"\n## 후보에서 뺀 것 {len(p['blocked'])}개 (config never_exclude_patterns·competitors)")
    L += [f"- {k} — 노출 {imp} — {w}" for k, imp, w in p["blocked"]] or ["- (없음)"]
    if p["already"]:
        L.append(f"\n## 노출 유지(사용자 결정) {len(p['already'])}개")
        L += [f"- {k} — 노출 {imp}" for k, imp, _ in p["already"]]
    L.append("\n## 승인 문구(그대로 채팅에)\n")
    L.append(p["approval_text"])
    return "\n".join(L) + "\n"


def cmd_propose(a):
    rows = load_registry(registry_path(a.registry))
    sr = load_search_terms(a.combined)
    p = build_proposal(rows, sr, day=a.day, since=a.since, first_seen_only=not a.all)
    md = render_proposal(p)
    out = a.out or os.path.join(ROOT, "work", f"exclusions_proposal_{p['window'][1].isoformat()}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    cand = os.path.splitext(out)[0] + "_candidates.txt"
    with open(cand, "w", encoding="utf-8") as f:
        f.write("\n".join(p["candidates"]) + ("\n" if p["candidates"] else ""))
    print(md)
    print(f"[propose] 제안 {out} · 후보 목록 {cand}(승인된 이름만 남겨 push --approved에 넘긴다)")
    return 0


# ---------------------------------------------------------------- push / verify / delete / test
def read_approved(path):
    seen, out = set(), []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            k = line.strip()
            if not k or k.startswith("#") or k in seen:
                continue
            seen.add(k)
            out.append(k)
    return out


def split_blocked(names):
    ok, refused = [], []
    for k in names:
        why = blocked_reason(k)
        (refused if why else ok).append((k, why) if why else k)
    return ok, refused


def item_ok(item):
    rs = item.get("resultStatus") or {}
    code = rs.get("code")
    return bool(item.get("nccAdgroupRestrictKwdId")) and (code in (None, 0, "0"))


def do_push(api, rows, names, description, log=print, chunk=50, snapshot=False):
    """쓰기 전 읽기(pull) → 그룹별로 아직 없는 이름만 POST → 응답 항목별 성공/실패 → registry(pending/failed).
    반환 {gid: {"added": [...], "skipped": [...], "failed": [(kw, msg)]}}"""
    stamp = today()
    current = do_pull(api, rows, log=log, mark_missing=False, snapshot=snapshot)
    result = {}
    for gid in target_ids():
        name = current[gid]["name"]
        have = current[gid]["keywords"]
        todo = [k for k in names if k not in have]
        skipped = [k for k in names if k in have]
        added, failed = [], []
        cap = int(EX.get("max_per_group") or 0)
        log(f"[push] {name}: 현재 {len(have)} + 등록 예정 {len(todo)} = {len(have) + len(todo)}"
            + (f" (한도 추정 {cap}{' — [주의] 초과 예상: 3716 오류 항목은 failed로 남고 우선순위를 다시 승인받는다' if len(have) + len(todo) > cap else ''})" if cap else ""))
        for i in range(0, len(todo), chunk):
            part = todo[i:i + chunk]
            try:
                resp = api.add_restricted(gid, part, description)
                if api.last_description != description:
                    log(f"[push] {name}: description '{description}'는 3721(길이 초과)라 '{api.last_description or '(없음)'}'으로 등록")
            except ApiError as e:
                for k in part:
                    failed.append((k, str(e)[:200]))
                    upsert(rows, k, gid, name, status="failed", source="skill", note=f"{stamp} 등록 실패: {str(e)[:120]}")
                continue
            by_kw = {it.get("keyword"): it for it in (resp or [])}
            for k in part:
                it = by_kw.get(k)
                if it is not None and item_ok(it):
                    added.append(k)
                    upsert(rows, k, gid, name, status="pending", source="skill", registered_at=regtm_to_date(it.get("regTm")) or stamp,
                           restrict_kwd_id=it.get("nccAdgroupRestrictKwdId", ""), note=f"{stamp} 등록 요청 성공(확인 전)")
                else:
                    msg = json.dumps((it or {}).get("resultStatus") or {"message": "응답에 없음"}, ensure_ascii=False)[:160]
                    failed.append((k, msg))
                    upsert(rows, k, gid, name, status="failed", source="skill", note=f"{stamp} 등록 실패: {msg}")
        for k in skipped:
            upsert(rows, k, gid, name, status="registered", source="api", verified_at=stamp)
        result[gid] = {"name": name, "added": added, "skipped": skipped, "failed": failed}
        log(f"[push] {name}: 요청 {len(todo)} · 성공 {len(added)} · 이미 있음 {len(skipped)} · 실패 {len(failed)}")
        for k, m in failed:
            log(f"       [FAIL] {k}: {m}")
    return result


def do_verify(api, rows, names, log=print, snapshot=False):
    """다시 읽어 names가 3그룹 모두에 있는지. 있으면 registered+verified_at, 없으면 failed. 반환 {gid: missing[]}"""
    stamp = today()
    current = do_pull(api, rows, log=log, mark_missing=False, snapshot=snapshot)
    missing = {}
    for gid in target_ids():
        name = current[gid]["name"]
        have = current[gid]["keywords"]
        miss = [k for k in names if k not in have]
        for k in names:
            if k in have:
                it = have[k]
                upsert(rows, k, gid, name, status="registered", source="api", verified_at=stamp,
                       registered_at=regtm_to_date(it.get("regTm")) or None, restrict_kwd_id=it.get("nccAdgroupRestrictKwdId", ""))
            else:
                upsert(rows, k, gid, name, status="failed", source="skill", note=f"{stamp} 확인 실패: 목록에 없음")
        missing[gid] = miss
        log(f"[verify] {name}: 확인 {len(names) - len(miss)}/{len(names)}" + (f" · 없음: {', '.join(miss)}" if miss else ""))
    return missing


def dry_run_plan(rows, names):
    """registry만으로 그룹별 계획 [(라벨, 등록 예정, 건너뜀, 현재 registry 등록 수)]. 첫 pull 전(그룹 ID↔이름 매핑 없음)에는 registry의 그룹명 기준."""
    plan = []
    mapped = {gid: group_label(rows, gid) for gid in target_ids()}
    if all(name == gid for gid, name in mapped.items()):
        groups = [(g, f"{g}(ID 매핑 전 — pull 뒤 확정)") for g in sorted({r["group_name"] for r in rows if r["group_name"] != STAR})]
        groups = groups or [(None, "(registry 비어 있음 — 3그룹 전부 등록 예정)")]
        for g, label in groups:
            have = {r["keyword"] for r in rows if r["status"] == "registered" and g is not None and r["group_name"] == g}
            plan.append((label, [k for k in names if k not in have], [k for k in names if k in have], len(have)))
        return plan
    for gid, name in mapped.items():
        have = {r["keyword"] for r in rows if r["status"] == "registered"
                and (r["group_id"] == gid or (not r["group_id"] and r["group_name"] == name))}
        plan.append((f"{name}({gid})", [k for k in names if k not in have], [k for k in names if k in have], len(have)))
    return plan


def cmd_push(a):
    names = read_approved(a.approved)
    ok, refused = split_blocked(names)
    for k, why in refused:
        print(f"[거부] {k}: {why} — 승인 목록에 있어도 등록하지 않는다(config never_exclude)")
    if not ok:
        print("[push] 등록할 이름이 없습니다")
        return 1
    description = default_description()
    path = registry_path(a.registry)
    rows = load_registry(path)
    if a.dry_run:  # 할 일 목록만 — HTTP 호출 0 · registry 변경 0. 실제 push는 registry가 아니라 API를 다시 읽어(pull) 정한다
        print(f"[dry-run] HTTP 호출 0 · registry 변경 0. 승인 {len(ok)}개 · description='{description}' · 아래는 registry 기준 계획")
        cap = int(EX.get("max_per_group") or 0)
        for label, todo, skip, have_n in dry_run_plan(rows, ok):
            print(f"[dry-run] {label}: 등록 예정 {len(todo)} · registry에 이미 등록 {len(skip)} · 현재 registry 등록 {have_n}"
                  + (f" → 등록 후 {have_n + len(todo)}/{cap}(추정)" if cap else ""))
            if todo:
                print("           등록: " + " · ".join(todo))
            if skip:
                print("           건너뜀: " + " · ".join(skip))
        return 0
    api = api_from_args(a)
    try:
        res = do_push(api, rows, ok, a.reason or description)
        save_registry(path, rows)
        miss = do_verify(api, rows, ok, snapshot=True)  # 등록 뒤 다시 읽은 목록이 그날의 스냅샷
    except NetworkBlocked as e:
        save_registry(path, rows)
        print(f"[FAIL] {e}")
        return 2
    except ApiError as e:
        save_registry(path, rows)
        print(f"[FAIL] {e} — registry에는 이 시점까지의 상태만 기록. 남은 것은 verify로 확인 뒤 재시도는 사용자 결정")
        return 1
    save_registry(path, rows)
    nfail = sum(len(v["failed"]) for v in res.values()) + sum(len(m) for m in miss.values())
    print(f"[push] 완료: 그룹 {len(res)} · 실패/미확인 {nfail} · registry {path}"
          + (" — 실패 항목은 registry status=failed, 재시도는 사용자 결정" if nfail else " — 전부 다시 읽어 확인(verified)"))
    return 1 if nfail else 0


def cmd_verify(a):
    api = api_from_args(a)
    path = registry_path(a.registry)
    rows = load_registry(path)
    names = read_approved(a.approved) if a.approved else sorted({r["keyword"] for r in rows if r["status"] == "pending"})
    if not names:
        print("[verify] 확인할 이름이 없습니다(pending 0)")
        return 0
    try:
        miss = do_verify(api, rows, names, snapshot=True)
    except NetworkBlocked as e:
        print(f"[FAIL] {e}")
        return 2
    except ApiError as e:
        print(f"[FAIL] {e}")
        return 1
    save_registry(path, rows)
    n = sum(len(m) for m in miss.values())
    print(f"[verify] {'전부 확인' if n == 0 else f'{n}건 없음 → failed로 기록'}")
    return 1 if n else 0


def cmd_delete(a):
    ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    if a.dry_run:
        print(f"[dry-run] DELETE {a.group} ids={ids} — 호출 0")
        return 0
    if not a.confirm:
        raise SystemExit("--confirm 이 필요합니다(삭제도 승인 대상 — 사용자가 화면을 보는 자리에서만 실행)")
    api = api_from_args(a)
    path = registry_path(a.registry)
    rows = load_registry(path)
    try:
        api.delete_restricted(a.group, ids)
    except NetworkBlocked as e:
        print(f"[FAIL] {e}")
        return 2
    except ApiError as e:
        print(f"[FAIL] {e}")
        return 1
    for r in rows:
        if r["group_id"] == a.group and r["restrict_kwd_id"] in ids:
            r["status"] = "deleted"
            r["note"] = (r["note"] + " | " if r["note"] else "") + f"{today()} 삭제"
    save_registry(path, rows)
    print(f"[delete] {a.group}: {len(ids)}개 삭제 요청 → registry deleted")
    return 0


def do_test_roundtrip(api, rows, keyword, gid, log=print):
    """시험 1건: 없음 확인 → 등록 → 확인(verified) → 삭제 → 없음 확인. 실패하면 그 단계에서 예외."""
    stamp = today()
    name = api.adgroup(gid).get("name", gid)
    before = {it.get("keyword") for it in api.restricted(gid)}
    if keyword in before:
        raise ApiError(f"시험 키워드 '{keyword}'가 이미 {name}에 있음 — 다른 문자열로")
    want = default_description("test")
    resp = api.add_restricted(gid, [keyword], want)
    if api.last_description != want:
        log(f"[test] description '{want}'는 3721(길이 초과)라 '{api.last_description or '(없음)'}'으로 등록")
    it = next((x for x in (resp or []) if x.get("keyword") == keyword), None)
    if it is None or not item_ok(it):
        raise ApiError(f"등록 실패: {json.dumps(resp, ensure_ascii=False)[:300]}")
    rid = it.get("nccAdgroupRestrictKwdId")
    log(f"[test] 등록 성공 id={rid}")
    after = {x.get("keyword"): x for x in api.restricted(gid)}
    if keyword not in after:
        raise ApiError("등록 응답은 성공인데 다시 읽은 목록에 없음(verified:false)")
    log(f"[test] 다시 읽어 확인: 있음(verified)")
    api.delete_restricted(gid, [rid])
    final = {x.get("keyword") for x in api.restricted(gid)}
    if keyword in final:
        raise ApiError("삭제 뒤에도 목록에 남아 있음")
    log(f"[test] 삭제 뒤 확인: 없음 — 원상복구")
    upsert(rows, keyword, gid, name, status="deleted", source="skill", registered_at=stamp, restrict_kwd_id=rid, verified_at=stamp,
           note=f"{stamp} 시험 등록→확인→삭제")
    return rid


def cmd_test_roundtrip(a):
    if not a.confirm:
        raise SystemExit("--confirm 이 필요합니다(사용자가 화면을 보는 자리에서만 실행)")
    if a.dry_run:
        print(f"[dry-run] 시험 순서: {a.group}에서 '{a.keyword}' 없음 확인 → 등록 → 확인 → 삭제 → 없음 확인 (호출 0)")
        return 0
    api = api_from_args(a)
    path = registry_path(a.registry)
    rows = load_registry(path)
    try:
        do_test_roundtrip(api, rows, a.keyword, a.group)
    except NetworkBlocked as e:
        print(f"[FAIL] {e}")
        return 2
    except ApiError as e:
        save_registry(path, rows)
        print(f"[FAIL] {e}")
        return 1
    save_registry(path, rows)
    print("[test] PASS — registry에 deleted 행으로 기록")
    return 0


def cmd_report(a):
    rows = load_registry(registry_path(a.registry))
    from collections import Counter
    c = Counter((r["group_name"], r["status"]) for r in rows)
    print(f"registry {registry_path(a.registry)} · {len(rows)}행")
    for (g, s), n in sorted(c.items()):
        print(f"  {g:<12} {s:<12} {n}")
    un = sorted({r['keyword'] for r in rows if r['status'] in ('unregistered', 'partial', 'missing', 'failed')})
    print(f"  미등록·누락·실패 이름 {len(un)}개: " + " · ".join(un))
    fl = sorted({r['keyword'] for r in rows if r['status'] == 'failed'})
    if fl:
        print(f"  그중 등록·확인 실패 {len(fl)}개(다음 propose 재등록 후보에 사유와 함께 오름): " + " · ".join(fl))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", help="registry csv 경로(기본 config exclusions.registry)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("pull"); s.add_argument("--key-file"); s.set_defaults(fn=cmd_pull)
    s = sub.add_parser("import-ui"); s.add_argument("file"); s.add_argument("--group", required=True); s.add_argument("--date"); s.set_defaults(fn=cmd_import_ui)
    s = sub.add_parser("propose"); s.add_argument("combined"); s.add_argument("--day"); s.add_argument("--since"); s.add_argument("--all", action="store_true"); s.add_argument("--out"); s.set_defaults(fn=cmd_propose)
    s = sub.add_parser("push"); s.add_argument("--approved", required=True); s.add_argument("--key-file"); s.add_argument("--dry-run", action="store_true"); s.add_argument("--reason"); s.set_defaults(fn=cmd_push)
    s = sub.add_parser("verify"); s.add_argument("--key-file"); s.add_argument("--approved"); s.set_defaults(fn=cmd_verify)
    s = sub.add_parser("delete"); s.add_argument("--group", required=True); s.add_argument("--ids", required=True); s.add_argument("--key-file"); s.add_argument("--confirm", action="store_true"); s.add_argument("--dry-run", action="store_true"); s.set_defaults(fn=cmd_delete)
    s = sub.add_parser("test-roundtrip"); s.add_argument("--keyword", required=True); s.add_argument("--group", required=True); s.add_argument("--key-file"); s.add_argument("--confirm", action="store_true"); s.add_argument("--dry-run", action="store_true"); s.set_defaults(fn=cmd_test_roundtrip)
    s = sub.add_parser("report"); s.set_defaults(fn=cmd_report)
    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except RegistryUnavailable as e:  # 판정 불가(미확인) — 아무것도 제안·등록하지 않고 멈춘다
        print(f"[FAIL] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
