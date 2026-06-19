// 데이터 레이어 타입 정의.
// 추후 실제 API 응답을 이 타입에 맞춰 매핑하면 UI 코드를 바꾸지 않고 교체할 수 있다.

export type MarketIndex = {
  name: string;
  value: string;
  changePercent: number | null;
};

export type MacroIndicator = {
  name: string;
  value: string;
  direction?: "up" | "down" | "flat" | "unknown";
  note?: string;
};

export type SectorMove = {
  sector: string;
  changePercent: number;
};

export type NewsCategory =
  | "official" // 공식 뉴스
  | "analyst" // 애널리스트 리포트
  | "overseas" // 해외 주요 뉴스 한글 요약
  | "chatter" // 월스트리트 채터
  | "rumor"; // 미확인 루머

export type NewsItem = {
  category: NewsCategory;
  title: string;
  summaryKo: string;
  relatedTickers: string[];
  impact: "positive" | "negative" | "neutral" | "mixed";
  confidence: "high" | "medium" | "low";
  source?: string;
  publishedAt?: string;
};

export type StockItem = {
  ticker: string;
  nameKo: string;
  nameEn?: string;
  sector: string;
  market: "US" | "KR" | "PRIVATE" | "ETF" | "MACRO";
  currency: "USD" | "KRW";
  closePrice: number | null;
  afterHoursPrice?: number | null;
  changePercent?: number | null;
  targetLow?: number | null;
  targetAverage?: number | null;
  targetHigh?: number | null;
  keyNews: string;
  dataTime?: string;
  riskNote?: string;
};

// 미국 시가총액 Top 10
export type MarketCapItem = {
  rank: number;
  ticker: string;
  nameKo: string;
  marketCap: string; // 예: "$5.10T"
  changePercent: number | null;
};

// 세계 증시 주요 일정 (월별 → 주별)
export type CalendarEvent = {
  dateLabel: string; // 예: "7/28~29 (화~수)"
  title: string;
  category: "FOMC" | "지표" | "실적" | "정책" | "기타";
  region: "US" | "KR" | "GLOBAL";
  importance: "high" | "medium" | "low";
};

export type CalendarWeek = {
  week: string; // 예: "6월 4주"
  events: CalendarEvent[];
};

export type CalendarMonth = {
  month: string; // 예: "2026년 6월"
  weeks: CalendarWeek[];
};

export type EconomicCalendar = {
  note?: string;
  months: CalendarMonth[];
};

export type FinalAnalysis = {
  marketDiagnosis: string;
  sectorRotationAnalysis: string;
  koreanMarketStrategy: string;
  usPortfolioStrategy: string;
  topOpportunities: string[];
  topRisks: string[];
  actionPlan: string[];
};

export type BriefingData = {
  title: string;
  generatedAt: string;
  oneLineConclusion: string;
  economicCalendar?: EconomicCalendar;
  usMarketCap?: { asOf: string; items: MarketCapItem[] };
  marketIndexes: MarketIndex[];
  macroIndicators: MacroIndicator[];
  sectorRotation: {
    strong: SectorMove[];
    weak: SectorMove[];
  };
  news: NewsItem[];
  stocks: StockItem[];
  finalAnalysis: FinalAnalysis;
};
