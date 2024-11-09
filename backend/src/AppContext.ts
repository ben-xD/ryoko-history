import type { Database } from "./db/db";
import { Ai } from "@cloudflare/workers-types";

export interface AppContext {
  // So you can set c.set("db") amd c.get("db") with typesafety
  Variables: {
    db: Database;
  };
  // For Cloudflare bindings (e.g. KV, Durable objects, R2, etc.)
  Bindings: {
    AI: Ai;
    // "Connection string to postgres database, starting with `postgres://`. Can be local or remote."
    DATABASE_URL: string;
    LOG_DATABASE: boolean;
    // LOG_HONO_REQUEST: boolean,
  };
}
