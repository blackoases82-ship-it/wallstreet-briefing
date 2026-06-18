import type { NewsItem, NewsCategory } from "@/types/briefing";

type Props = {
  news: NewsItem[];
};

const CATEGORY_LABEL: Record<NewsCategory, string> = {
  official: "공식 뉴스",
  analyst: "애널리스트",
  overseas: "해외 주요 뉴스",
  chatter: "월가 채터",
  rumor: "미확인 월가 채터",
};

// 카테고리별 배경/테두리 톤
function cardTone(cat: NewsCategory): string {
  switch (cat) {
    case "official":
      return "bg-newsPos border-emerald-200";
    case "analyst":
      return "bg-white border-gray-200";
    case "overseas":
      return "bg-white border-gray-200";
    case "chatter":
      return "bg-newsWarn border-amber-200";
    case "rumor":
      return "bg-newsRisk border-red-300";
  }
}

function badgeTone(cat: NewsCategory): string {
  switch (cat) {
    case "official":
      return "bg-emerald-600 text-white";
    case "analyst":
      return "bg-gray-800 text-white";
    case "overseas":
      return "bg-blue-600 text-white";
    case "chatter":
      return "bg-amber-500 text-white";
    case "rumor":
      return "bg-red-600 text-white";
  }
}

function impactLabel(impact: NewsItem["impact"]): { text: string; cls: string } {
  switch (impact) {
    case "positive":
      return { text: "영향: 긍정", cls: "text-up" };
    case "negative":
      return { text: "영향: 부정", cls: "text-down" };
    case "mixed":
      return { text: "영향: 혼조", cls: "text-amber-600" };
    default:
      return { text: "영향: 중립", cls: "text-sub" };
  }
}

function confidenceLabel(c: NewsItem["confidence"]): string {
  return c === "high" ? "높음" : c === "medium" ? "중간" : "낮음";
}

export default function NewsSection({ news }: Props) {
  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">해외 주요 뉴스</h2>
      <div className="space-y-3">
        {news.map((n, i) => {
          const impact = impactLabel(n.impact);
          return (
            <article
              key={i}
              className={`rounded-2xl shadow-card border px-4 py-3 ${cardTone(
                n.category
              )}`}
            >
              <div className="flex items-center gap-2 flex-wrap">
                <span
                  className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${badgeTone(
                    n.category
                  )}`}
                >
                  [{CATEGORY_LABEL[n.category]}]
                </span>
                {n.source && (
                  <span className="text-[11px] text-sub">{n.source}</span>
                )}
                {n.publishedAt && (
                  <span className="text-[11px] text-sub">· {n.publishedAt}</span>
                )}
              </div>

              <h3 className="mt-2 font-bold text-[15px] leading-snug">
                {n.title}
              </h3>
              <p className="mt-1 text-sm text-gray-700 leading-relaxed">
                {n.summaryKo}
              </p>

              {n.relatedTickers.length > 0 && (
                <p className="mt-2 text-xs text-sub">
                  관련 종목: {n.relatedTickers.join(", ")}
                </p>
              )}

              <div className="mt-1 flex items-center gap-3 text-xs">
                <span className={`font-semibold ${impact.cls}`}>
                  {impact.text}
                </span>
                {n.category === "rumor" && (
                  <span className="text-sub">
                    신뢰도: {confidenceLabel(n.confidence)}
                  </span>
                )}
              </div>

              {n.category === "rumor" && (
                <p className="mt-2 text-xs font-semibold text-red-700 bg-white/70 rounded-lg px-2 py-1">
                  ⚠️ 주의: 공식 확인 전 단독 매수 근거로 사용 금지
                </p>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
