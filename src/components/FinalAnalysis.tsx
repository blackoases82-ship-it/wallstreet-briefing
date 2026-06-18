import type { FinalAnalysis as FinalAnalysisType } from "@/types/briefing";

type Props = {
  analysis: FinalAnalysisType;
};

function Block({ title, body }: { title: string; body: string }) {
  return (
    <div>
      <p className="text-sm font-bold mb-1">{title}</p>
      <p className="text-sm text-gray-700 leading-relaxed">{body}</p>
    </div>
  );
}

function ListBlock({
  title,
  items,
  tone,
}: {
  title: string;
  items: string[];
  tone: "up" | "down";
}) {
  const dot = tone === "up" ? "text-up" : "text-down";
  return (
    <div>
      <p className="text-sm font-bold mb-1">{title}</p>
      <ul className="space-y-1">
        {items.map((it, i) => (
          <li key={i} className="text-sm text-gray-700 leading-relaxed flex gap-2">
            <span className={`${dot} font-bold`}>{i + 1}.</span>
            <span>{it}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function FinalAnalysis({ analysis }: Props) {
  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">전문 분석</h2>
      <div className="bg-white rounded-2xl shadow-card px-5 py-4 space-y-4">
        <Block title="시장 진단" body={analysis.marketDiagnosis} />
        <Block title="섹터 순환 분석" body={analysis.sectorRotationAnalysis} />
        <Block title="한국장 전략" body={analysis.koreanMarketStrategy} />
        <Block title="미국 포트폴리오 전략" body={analysis.usPortfolioStrategy} />
        <ListBlock
          title="오늘의 Top 3 기회"
          items={analysis.topOpportunities}
          tone="up"
        />
        <ListBlock
          title="오늘의 Top 3 리스크"
          items={analysis.topRisks}
          tone="down"
        />
      </div>
    </section>
  );
}
