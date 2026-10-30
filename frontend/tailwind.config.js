/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#080B10",
        surface: "#0D131F",
        "surface-raised": "#131C2E",
        "surface-border": "#1E2A42",
        primary: {
          DEFAULT: "#00E5FF",
          glow: "#00B4D8",
          dark: "#0077B6",
        },
        electric: "#3B82F6",
        neon: "#00F5D4",
        danger: "#EF4444",
        warning: "#F59E0B",
        success: "#10B981",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      animation: {
        "pulse-subtle": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow-flow": "glow 4s ease-in-out infinite alternate",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 15px rgba(0, 229, 255, 0.2)" },
          "100%": { boxShadow: "0 0 30px rgba(0, 229, 255, 0.5)" },
        },
      },
    },
  },
  plugins: [],
};

