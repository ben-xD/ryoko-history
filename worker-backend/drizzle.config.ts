import { config } from "dotenv";
import type { Config } from "drizzle-kit";

config({ path: ".dev.vars" });

const url = process.env.DATABASE_URL;

if (url === undefined) {
  throw new Error("DATABASE_URL not found in env");
}

// Migrations are ran from Node/command line rather than cloudflare workers

// Warning: using `./src/db/schema/index` or `/src/db/schema/` doesn't work
export default {
  schema: "./src/db/schema/index.ts",
  out: "./migrations",
  dialect: "postgresql",
  // breakpoints: true,
  dbCredentials: {
    url,
  },
} satisfies Config;
