import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // 다크 모드 팔레트
        bg: "#0B0F19",
        card: "#151B28",
        cardHi: "#1C2434",
        ink: "#E6E9EF",
        sub: "#93A0B4",
        line: "#252D3D",
        up: "#F05252", // 한국 기준 상승 = 빨강 (다크용으로 밝게)
        down: "#5C8DF6", // 하락 = 파랑
        marginBadge: "#3A1F22", // 안전마진 배지 배경(다크)
        newsPos: "#0F2A22",
        newsWarn: "#2C2410",
        newsRisk: "#33181B",
      },
      maxWidth: {
        app: "820px",
      },
      boxShadow: {
        card: "0 1px 2px rgba(0,0,0,0.4), 0 1px 3px rgba(0,0,0,0.3)",
      },
    },
  },
  plugins: [],
};

export default config;
