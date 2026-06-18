# 나만의 월스트리트

개인 투자 모닝 브리핑 PWA. 매일 아침 아이폰/아이패드에서 1~3분 안에 시장 흐름과
관심 종목 상태를 파악하는 "개인 월스트리트 뉴스룸".

## 실행 방법

```bash
npm install
npm run dev
```

브라우저에서 http://localhost:3000 접속.
아이폰 Safari에서 **공유 → 홈 화면에 추가**로 앱처럼 설치할 수 있습니다 (PWA).

> 📱 아이폰에서 열려면(localhost는 맥에서만 열림), 그리고 매일 6:30 자동 갱신 +
> 메일 받기 설정은 **[DEPLOY.md](./DEPLOY.md)** 를 보세요.

## 주요 기능

- 오늘 한 줄 결론
- 시장 현황 (다우/S&P500/나스닥/러셀2000)
- 거시 지표 (원/달러, 금, 은, VIX, 美10년물, 공포·탐욕)
- 섹터 순환 (강세 ▲ / 약세 ▼)
- 국내장 개장 전 관심/추천 섹션
- 섹터별 관심종목 테이블 (가로 스크롤, 종목명 고정)
- 종가/현재가와 안전마진을 **붙여서** 표시
- 목표가 저/평균/고 + 상승여력 + 추천 등급
- 해외 뉴스 한글 요약 (공식/애널리스트/해외/채터/미확인 루머 구분)
- 미확인 월가 채터 경고 라벨
- 마지막 전문 분석 + 오늘 액션 플랜

## 계산 공식

```text
상승여력        = (평균 목표가 - 현재가) / 현재가 * 100
컨센서스 안전마진 = (평균 목표가 - 현재가) / 평균 목표가 * 100
20% 매수가       = 평균 목표가 * 0.80
25% 매수가       = 평균 목표가 * 0.75
30% 매수가       = 평균 목표가 * 0.70
```

평균 목표가가 없거나 0이면 안전마진/상승여력은 "계산 제외" (사유: 컨센서스 부족).

## 추천 등급 기준

| 안전마진 | 등급 |
|---|---|
| 30% 이상 | 매수검토 |
| 25~30% | 분할매수 |
| 15~25% | 관찰 |
| 5~15% | 보유 |
| 5% 미만 / 음수 | 추격금지 |

고변동 성장주(PLTR, ASTS, RKLB, IONQ, RGTI, BE, FLNC)는 안전마진이 높아도
"고변동 주의 / 초고위험 변동성" 문구가 등급에 붙습니다.

## 기술 스택

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- PWA (manifest.json)
- Mock Data 기반 1차 MVP

## 데이터 교체 가이드 (추후 API 연결)

데이터 구조와 계산 로직이 UI와 분리되어 있습니다.

- 타입: `src/types/briefing.ts`
- 계산: `src/lib/calculations.ts`, 포맷: `src/lib/formatters.ts`
- 샘플 데이터: `src/data/mockBriefing.ts`

앱은 `src/data/briefing.json` 을 읽습니다(`mockBriefing.ts` 가 이 JSON 을 로드).
매일 아침 예약 작업이 이 JSON 을 실데이터로 덮어쓰므로, 컴포넌트 코드는 건드릴
필요가 없습니다. 실제 API 응답을 `BriefingData` 형태로 매핑해 JSON 에 쓰면 끝입니다.

## 폴더 구조

```text
src/
  app/          page.tsx, layout.tsx, globals.css
  components/   11개 카드/섹션 컴포넌트
  data/         mockBriefing.ts
  lib/          calculations.ts, formatters.ts
  types/        briefing.ts
public/
  manifest.json
  icons/        icon-192.png, icon-512.png
```

## 주의

현재 버전은 **샘플 데이터 기반 MVP**입니다. 실제 시세·목표가가 아니며,
투자 자문이 아닌 브리핑/분석 보조 도구입니다.
실제 투자 판단에는 검증된 데이터 소스가 필요합니다.

## 추후 추가 예정

실제 미국/한국 주가 API, 애널리스트 컨센서스, 뉴스 API + AI 한글 요약,
매일 오전 6:30 자동 생성, PDF 출력, 푸시 알림, 관심종목 편집, 종목 상세 페이지.
