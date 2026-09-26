#!/usr/bin/env python3
"""validate.py · compute.py · compare.py가 함께 쓰는 공통 헬퍼 — **읽기·필터·일수·섹션 자르기까지만.**

값 계산(KPI 합·순위·비중·정렬)은 여기 두지 않는다. validate.py는 compute.py와 독립된
검산이어야 하므로 값 계산 함수를 공유하면 같은 오류를 두 번 통과시킨다(2026-09-26 수정 회차 규칙).
"""
import json
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_PATH = os.path.join(ROOT, "config", "report-config.json")


def load_config():
    """config/report-config.json. 없으면 즉시 종료(validate.py 종전 동작 유지)."""
    try:
        with open(CFG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"설정 파일이 없습니다: {CFG_PATH}\n스킬 저장소를 통째로 받았는지 확인하세요.")


def read_csv(path):
    """네이버 보고서·합본 모두 첫 줄이 기간 헤더."""
    return pd.read_csv(path, skiprows=1)


def exclude_groups(kw, cfg):
    """키워드 보고서에서 config excluded_groups를 뺀 프레임(KPI·01~07·10번 기준)."""
    return kw[~kw["광고그룹"].isin(cfg["excluded_groups"])]


def day_list(kw):
    """`일별` 값을 정렬한 문자열 목록 ('2026.08.26.' 형태)."""
    return sorted(kw["일별"].astype(str).unique())


def parse_days(kw):
    """키워드 보고서 `일별`에서 (min, max, 일수) — Timestamp."""
    d = pd.to_datetime(kw["일별"].astype(str).str.rstrip("."), format="%Y.%m.%d")
    return d.min(), d.max(), (d.max() - d.min()).days + 1


def section(html, num, next_num=None):
    """<!-- Section N: --> 부터 다음 섹션 주석(없으면 <script>)까지. 12번은 <script> 앞에서 끊는다."""
    start = html.find(f"<!-- Section {num}:")
    if start == -1:
        return ""
    end = html.find(f"<!-- Section {next_num if next_num else num + 1}:")
    if end == -1:
        end = html.find("<script>", start)
    return html[start:end if end != -1 else len(html)]


def read_html(path):
    with open(path, encoding="utf-8") as f:
        return f.read()
