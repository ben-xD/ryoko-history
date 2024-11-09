import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";
import { config } from "dotenv";

config({ path: ".dev.vars" });
const DATABASE_URL = process.env.DATABASE_URL;
// TODO use zod to parse all env vars, not manually throwing
if (DATABASE_URL === undefined) {
  throw new Error("DATABASE_URL environment variable is not set.");
}

// See https://developers.cloudflare.com/workers/testing/vitest-integration/configuration/
// vitest workers uses miniflare internally.
export default defineWorkersConfig({
  test: {
    // setupFiles: ["./setupTests/setupTests.ts"],
    poolOptions: {
      workers: {
        wrangler: { configPath: "./wrangler.toml" },
        // See https://github.com/cloudflare/workers-sdk/tree/main/packages/miniflare#interface-workeroptions for more params
        miniflare: {
          bindings: {
            DATABASE_URL,
          },
        },
      },
    },
    // Not well documented, and not user friendly (It doesn't work out of the box/existing-tsconfig and needs more config)
    // typecheck: {}
  },
});
