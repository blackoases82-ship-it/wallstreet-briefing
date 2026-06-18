import { mockBriefing } from "@/data/mockBriefing";
import Header from "@/components/Header";
import OneLineConclusion from "@/components/OneLineConclusion";
import MarketIndexGrid from "@/components/MarketIndexGrid";
import MacroPills from "@/components/MacroPills";
import SectorRotationCard from "@/components/SectorRotationCard";
import KoreanMarketFocus from "@/components/KoreanMarketFocus";
import NewsSection from "@/components/NewsSection";
import SectorStockSection from "@/components/SectorStockSection";
import FinalAnalysis from "@/components/FinalAnalysis";
import ActionPlan from "@/components/ActionPlan";

export default function Home() {
  const data = mockBriefing;

  return (
    <main className="min-h-screen bg-bg">
      <div className="mx-auto max-w-app px-4 py-4 space-y-5">
        <Header title={data.title} generatedAt={data.generatedAt} />

        <OneLineConclusion text={data.oneLineConclusion} />

        <MarketIndexGrid indexes={data.marketIndexes} />

        <MacroPills indicators={data.macroIndicators} />

        <SectorRotationCard
          strong={data.sectorRotation.strong}
          weak={data.sectorRotation.weak}
        />

        {/* 한국장 개장 전 추천 — 상단 강조 */}
        <KoreanMarketFocus stocks={data.stocks} />

        <NewsSection news={data.news} />

        <SectorStockSection stocks={data.stocks} />

        <FinalAnalysis analysis={data.finalAnalysis} />

        <ActionPlan items={data.finalAnalysis.actionPlan} />

        <footer className="pt-2 pb-8 text-center">
          <p className="text-[11px] text-sub leading-relaxed">
            본 화면은 <b>샘플(Mock) 데이터</b> 기반 MVP입니다. 실제 시세·목표가가
            아니며, 투자 자문이 아닌 <b>브리핑/분석 보조 도구</b>입니다.
            <br />
            실제 투자 판단에는 검증된 데이터 소스가 필요합니다.
          </p>
        </footer>
      </div>
    </main>
  );
}
