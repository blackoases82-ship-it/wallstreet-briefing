// 투자 브리핑 핵심 계산 로직.
// 모든 함수는 입력이 부족하면 null 을 반환하고, UI 에서 "-" 또는 "계산 제외" 로 표시한다.

// 고변동 성장주: 안전마진이 높아도 등급에 주의 문구를 붙인다.
export const HIGH_VOLATILITY_TICKERS = [
  "PLTR",
  "ASTS",
  "RKLB",
  "IONQ",
  "RGTI",
  "BE",
  "FLNC",
];

// 컨센서스 부족으로 계산에서 제외할 종목 (비상장 등)
export const NO_CONSENSUS_TICKERS = ["SPACEX", "SPACE-X", "SPACEX-PROXY"];

/**
 * 상승여력 = (평균 목표가 - 현재가) / 현재가 * 100
 */
export function calculateUpside(
  currentPrice: number | null,
  targetAverage: number | null
): number | null {
  if (
    currentPrice == null ||
    targetAverage == null ||
    currentPrice === 0 ||
    targetAverage === 0
  ) {
    return null;
  }
  return ((targetAverage - currentPrice) / currentPrice) * 100;
}

/**
 * 컨센서스 안전마진 = (평균 목표가 - 현재가) / 평균 목표가 * 100
 */
export function calculateSafetyMargin(
  currentPrice: number | null,
  targetAverage: number | null
): number | null {
  if (
    currentPrice == null ||
    targetAverage == null ||
    currentPrice === 0 ||
    targetAverage === 0
  ) {
    return null;
  }
  return ((targetAverage - currentPrice) / targetAverage) * 100;
}

/**
 * 안전마진별 매수가
 *   20% → 평균 목표가 * 0.80
 *   25% → 평균 목표가 * 0.75
 *   30% → 평균 목표가 * 0.70
 */
export function calculateBuyPrice(
  targetAverage: number | null,
  margin: 20 | 25 | 30
): number | null {
  if (targetAverage == null || targetAverage === 0) return null;
  const factor = margin === 20 ? 0.8 : margin === 25 ? 0.75 : 0.7;
  return targetAverage * factor;
}

/**
 * 추천 등급.
 * 안전마진 기준 + 고변동 종목 보정.
 */
export function getRecommendationLabel(
  safetyMargin: number | null,
  ticker?: string
): string {
  if (safetyMargin == null) return "계산 제외";

  const t = (ticker ?? "").toUpperCase();
  const isHighVol = HIGH_VOLATILITY_TICKERS.includes(t);

  let base: string;
  if (safetyMargin >= 30) base = "매수검토";
  else if (safetyMargin >= 25) base = "분할매수";
  else if (safetyMargin >= 15) base = "관찰";
  else if (safetyMargin >= 5) base = "보유";
  else base = "추격금지"; // 5% 미만 및 음수

  if (isHighVol) {
    if (safetyMargin >= 25) return "공격형 분할매수 · 초고위험 변동성";
    if (safetyMargin >= 5) return `${base} · 고변동 주의`;
    return "추격금지 · 고변동";
  }

  return base;
}

/**
 * 추천 등급의 색상 톤(UI 배지용). 한국 기준: 긍정=빨강 계열, 부정=회색.
 */
export function getRecommendationTone(
  label: string
): "buy" | "split" | "watch" | "hold" | "avoid" | "none" {
  if (label.includes("계산 제외")) return "none";
  if (label.includes("매수검토")) return "buy";
  if (label.includes("분할매수")) return "split";
  if (label.includes("관찰")) return "watch";
  if (label.includes("추격금지")) return "avoid";
  if (label.includes("보유")) return "hold";
  return "none";
}
