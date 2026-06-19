import type { NewsItem } from "@/types/briefing";

type Props = {
  news: NewsItem[];
  usTickers: string[];
};

const CAT_LABEL: Record<string, string> = {
  official: "공식",
  analyst: "애널리스트",
  overseas: "해외매체",
  chatter: "월가 채터",
  rumor: "미확인",
};

function impactChip(impact: NewsItem["impact"]) {
  switch (impact) {
    case "positive":
      return { t: "긍정", c: "bg-up/15 text-up" };
    case "negative":
      return { t: "부정", c: "bg-down/15 text-down" };
    case "mixed":
      return { t: "혼조", c: "bg-amber-500/15 text-amber-300" };
    default:
      return { t: "중립", c: "bg-white/10 text-sub" };
  }
}

export default function UsMarketNews({ news, usTickers }: Props) {
  const set = new Set(usTickers.map((t) => t.toUpperCase()));
  // 미국 관련 뉴스만: 미국 티커가 엮였거나, 해외매체/애널리스트 카테고리
  const usNews = news.filter(
    (n) =>
      n.relatedTickers.some((t) => set.has(t.toUpperCase())) ||
      n.category === "overseas"
  );
  if (usNews.length === 0) return null;

  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">
        🇺🇸 미국 시장 주요 뉴스 (상세)
      </h2>
      <div className="bg-card rounded-2xl shadow-card border border-line divide-y divide-line">
        {usNews.map((n, i) => {
          const chip = impactChip(n.impact);
          return (
            <article key={i} className="px-4 py-3.5">
              <div className="flex items-center gap-2 flex-wrap mb-1">
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-white/10 text-sub">
                  {CAT_LABEL[n.category] ?? n.category}
                </span>
                <span
                  className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${chip.c}`}
                >
                  {chip.t}
                </span>
                {n.source && (
                  <span className="text-[11px] text-sub">{n.source}</span>
                )}
                {n.publishedAt && (
                  <span className="text-[11px] text-sub">· {n.publishedAt}</span>
                )}
              </div>
              <h3 className="font-bold text-[15px] leading-snug text-ink">
                {n.title}
              </h3>
              <p className="mt-1.5 text-sm text-gray-300 leading-relaxed">
                {n.summaryKo}
              </p>
              {n.relatedTickers.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {n.relatedTickers.map((t) => (
                    <span
                      key={t}
                      className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-white/5 border border-line text-sub"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              )}
            </article>
          );
        })}
      </div>
      <p className="text-[11px] text-sub mt-1 px-1">
        ※ 미확인 채터·루머는 단독 매수 근거로 쓰지 마세요. 투자 자문이 아닙니다.
      </p>
    </section>
  );
}
