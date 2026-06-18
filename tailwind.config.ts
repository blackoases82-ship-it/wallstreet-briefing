import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#F6F7F9",
        card: "#FFFFFF",
        ink: "#111827",
        sub: "#6B7280",
        up: "#DC2626",
        down: "#2563EB",
        marginBadge: "#FEE2E2",
        newsPos: "#ECFDF5",
        newsWarn: "#FEF3C7",
        newsRisk: "#FEE2E2",
      },
      maxWidth: {
        app: "820px",
      },
      boxShadow: {
        card: "0 1px 3px rgba(17, 24, 39, 0.08), 0 1px 2px rgba(17, 24, 39, 0.04)",
      },
    },
  },
  plugins: [],
};

export default config;
