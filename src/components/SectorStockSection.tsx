import type { StockItem } from "@/types/briefing";
import StockRow from "./StockRow";

type Props = {
  stocks: StockItem[];
};

// 섹터별로 묶어서 표시. 가로 스크롤 허용, 종목명은 sticky 로 항상 노출.
export default function SectorStockSection({ stocks }: Props) {
  // 섹터별 그룹화 (입력 순서 유지)
  const groups = new Map<string, StockItem[]>();
  for (const s of stocks) {
    const key = s.sector;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(s);
  }

  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">
        섹터별 관심종목
      </h2>
      <p className="text-[11px] text-sub mb-2 px-1">
        ← 좌우로 밀어서 목표가·상승여력·등급까지 확인
      </p>

      <div className="space-y-4">
        {Array.from(groups.entries()).map(([sector, items]) => (
          <div
            key={sector}
            className="bg-card rounded-2xl shadow-card overflow-hidden border border-line"
          >
            <div className="px-4 pt-3 pb-1">
              <h3 className="font-bold text-sm">{sector}</h3>
            </div>
            <div className="scroll-x no-scrollbar">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="text-[11px] text-sub border-b border-line">
                    <th className="sticky left-0 bg-card px-3 py-2 font-medium">
                      종목
                    </th>
                    <th className="px-3 py-2 font-medium whitespace-nowrap">
                      종가/시간외
                    </th>
                    <th className="px-3 py-2 font-medium whitespace-nowrap">
                      안전마진
                    </th>
                    <th className="px-3 py-2 font-medium whitespace-nowrap">
                      목표가 저/평/고
                    </th>
                    <th className="px-3 py-2 font-medium whitespace-nowrap">
                      상승여력
                    </th>
                    <th className="px-3 py-2 font-medium">등급</th>
                    <th className="px-3 py-2 font-medium">핵심 뉴스</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((s) => (
                    <StockRow key={s.ticker} stock={s} />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
