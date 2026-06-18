// 표시 포맷 유틸. 값이 없으면 "-" 로 표시한다.

export function formatPrice(
  value: number | null | undefined,
  currency: "USD" | "KRW"
): string {
  if (value == null) return "-";
  if (currency === "USD") {
    return `$${value.toLocaleString("en-US", {
      minimumFractionDigits: value < 100 ? 2 : 0,
      maximumFractionDigits: 2,
    })}`;
  }
  // KRW
  return `${Math.round(value).toLocaleString("ko-KR")}원`;
}

export function formatPercent(value: number | null | undefined): string {
  if (value == null) return "-";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}%`;
}

// 한국 기준: 상승 빨강, 하락 파랑.
export function changeColorClass(value: number | null | undefined): string {
  if (value == null) return "text-sub";
  if (value > 0) return "text-up";
  if (value < 0) return "text-down";
  return "text-ink";
}

// 시간외 가격 표시: 값이 없으면 "확인중"
export function formatAfterHours(
  value: number | null | undefined,
  currency: "USD" | "KRW"
): string {
  if (value == null) return "확인중";
  return formatPrice(value, currency);
}
