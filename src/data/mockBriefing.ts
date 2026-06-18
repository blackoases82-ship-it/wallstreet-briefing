import type { BriefingData } from "@/types/briefing";
import briefingJson from "./briefing.json";

// 데이터는 briefing.json 에서 읽습니다.
// 매일 아침 6:30 예약 작업이 이 JSON 을 실데이터로 덮어쓰고 git push → Vercel 자동 재배포.
// 따라서 UI/컴포넌트 코드는 건드릴 필요 없이 데이터만 교체됩니다.
export const mockBriefing = briefingJson as BriefingData;
