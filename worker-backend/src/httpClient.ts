// For the frontend
import { hc } from "hono/client";
import type { AppType } from "./main";

// Using https://github.com/m-shaka/hono-rpc-perf-tips-example/blob/main/apps/client/src/index.ts
// assign the client to a variable to calculate the type when compiling
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const client = hc<AppType>("");
export type Client = typeof client;

export const hcWithType = (...args: Parameters<typeof hc>): Client =>
  hc<AppType>(...args);
