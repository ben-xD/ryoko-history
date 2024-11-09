import type { Config } from "tailwindcss";
import containerQueries from "@tailwindcss/container-queries";
import * as tailwindCssAnimate from "tailwindcss-animate";

export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: ["class", "class"],
  theme: {
    fontFamily: {
      sans: ["Roboto Mono", "sans-serif"],
    },
    extend: {
      animation: {
        jackInTheBox: "jackInTheBox 0.5s ease-in-out 1",
      },
      colors: {
        primary: {
          "50": "var(--primary-50)",
          "100": "var(--primary-100)",
          "200": "var(--primary-200)",
          "300": "var(--primary-300)",
          "400": "var(--primary-400)",
          "500": "var(--primary-500)",
          "600": "var(--primary-600)",
          "700": "var(--primary-700)",
          "800": "var(--primary-800)",
          "900": "var(--primary-900)",
          "950": "var(--primary-950)",
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          "50": "var(--secondary-50)",
          "100": "var(--secondary-100)",
          "200": "var(--secondary-200)",
          "300": "var(--secondary-300)",
          "400": "var(--secondary-400)",
          "500": "var(--secondary-500)",
          "600": "var(--secondary-600)",
          "700": "var(--secondary-700)",
          "800": "var(--secondary-800)",
          "900": "var(--secondary-900)",
          "950": "var(--secondary-950)",
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        bg: {
          "50": "var(--bg-50)",
          "100": "var(--bg-100)",
          "200": "var(--bg-200)",
          "300": "var(--bg-300)",
          "400": "var(--bg-400)",
          "500": "var(--bg-500)",
          "600": "var(--bg-600)",
          "700": "var(--bg-700)",
          "800": "var(--bg-800)",
          "900": "var(--bg-900)",
          "950": "var(--bg-950)",
        },
        primaryDark: "colors.white",
        danger: "colors.red",
        dangerSecondary: "colors.amber",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        chart: {
          "1": "hsl(var(--chart-1))",
          "2": "hsl(var(--chart-2))",
          "3": "hsl(var(--chart-3))",
          "4": "hsl(var(--chart-4))",
          "5": "hsl(var(--chart-5))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [
    // https://github.com/tailwindlabs/tailwindcss-container-queries
    containerQueries,
    tailwindCssAnimate,
  ],
} satisfies Config;
