import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          forest: "#1F694B",
          emerald: "#2E8B67",
          charcoal: "#1C231F",
          offwhite: "#F7F5EE",
          white: "#FFFFFF",
          gold: "#D6A434",
          sage: "#E7F0EA",
          gray: "#6B756F",
          amber: "#B7791F",
          red: "#B84A4A",
          surface: "rgba(255, 255, 255, 0.88)",
          subtle: "rgba(28, 35, 31, 0.04)",
          border: "rgba(28, 35, 31, 0.08)",
        },
      },
      borderRadius: {
        'bento-sm': '12px',
        'bento-md': '18px',
        'bento-lg': '24px',
        'bento-xl': '28px',
      },
      boxShadow: {
        'bento': '0 8px 30px rgba(28, 35, 31, 0.06)',
        'bento-hover': '0 14px 40px rgba(28, 35, 31, 0.10)',
        'bento-active': '0 4px 15px rgba(28, 35, 31, 0.08)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
export default config;
