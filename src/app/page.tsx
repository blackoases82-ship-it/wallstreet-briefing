import { mockBriefing } from "@/data/mockBriefing";
import Header from "@/components/Header";
import EconomicCalendar from "@/components/EconomicCalendar";
import OneLineConclusion from "@/components/OneLineConclusion";
import MarketIndexGrid from "@/components/MarketIndexGrid";
import MacroPills from "@/components/MacroPills";
import SectorRotationCard from "@/components/SectorRotationCard";
import UsMarketCapTop10 from "@/components/UsMarketCapTop10";
import KoreanMarketFocus from "@/components/KoreanMarketFocus";
import NewsSection from "@/components/NewsSection";
import SectorStockSection from "@/components/SectorStockSection";
import UsMarketNews from "@/components/UsMarketNews";
import FinalAnalysis from "@/components/FinalAnalysis";
import ActionPlan from "@/components/ActionPlan";

export default function Home() {
  const data = mockBriefing;
  const usTickers = data.stocks
    .filter((s) => s.market === "US")
    .map((s) => s.ticker);

  return (
    <main className="min-h-screen bg-bg">
      <div className="mx-auto max-w-app px-4 py-4 space-y-5">
        <Header title={data.title} generatedAt={data.generatedAt} />

        {/* 세계 증시 주요 일정 — 최상단 */}
        <EconomicCalendar calendar={data.economicCalendar} />

        <OneLineConclusion text={data.oneLineConclusion} />

        <MarketIndexGrid indexes={data.marketIndexes} />

        <MacroPills indicators={data.macroIndicators} />

        <SectorRotationCard
          strong={data.sectorRotation.strong}
          weak={data.sectorRotation.weak}
        />

        {/* 미국 시가총액 Top 10 — 국내장 위 */}
        <UsMarketCapTop10 data={data.usMarketCap} />

        {/* 한국장 개장 전 추천 */}
        <KoreanMarketFocus stocks={data.stocks} />

        <NewsSection news={data.news} />

        <SectorStockSection stocks={data.stocks} />

        {/* 미국 시장 주요 뉴스 상세 — 하단 */}
        <UsMarketNews news={data.news} usTickers={usTickers} />

        <FinalAnalysis analysis={data.finalAnalysis} />

        <ActionPlan items={data.finalAnalysis.actionPlan} />

        <footer className="pt-2 pb-8 text-center">
          <p className="text-[11px] text-sub leading-relaxed">
            데이터는 매일 6:30 / 13:00 / 20:00 (KST) 자동 갱신됩니다. 투자 자문이
            아닌 <b>브리핑/분석 보조 도구</b>이며, 실제 투자 판단에는 검증된 데이터
            확인이 필요합니다.
          </p>
        </footer>
      </div>
    </main>
  );
}
