#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
나만의 월스트리트 - 일일 데이터 자동 생성기 (GitHub Actions용)

- yfinance로 관심종목/지수/거시/섹터ETF/시총을 받아 src/data/briefing.json 의
'숫자' 부분을 갱신한다.
- 뉴스(news) / 최종분석(finalAnalysis) / 경제캘린더(economicCalendar) / 제목(title) /
oneLineConclusion 은 기존 파일 값을 그대로 보존한다(LLM 없이 자동 생성 불가하므로).
=> 나중에 ANTHROPIC_API_KEY 를 붙이면 이 부분도 자동화 가능(확장 지점 표시).
- 값을 못 받은 항목은 기존 JSON 값을 유지(앱이 빈칸/깨짐 없이 항상 동작).

실행: python scripts/generate_briefing.py
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

import yfinance as yf

KST = timezone(timedelta(hours=9))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "src", "data", "briefing.json")

# ---------------------------------------------------------------------------
# 관심종목 메타데이터 (티커 → 표시정보). 시세/목표가는 yfinance로 채운다.
# riskNote 가 있으면 고변동 라벨로 사용.
# ---------------------------------------------------------------------------
STOCKS = [
