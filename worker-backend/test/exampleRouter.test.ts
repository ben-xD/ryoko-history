import {
  env,
  createExecutionContext,
  waitOnExecutionContext,
  SELF,
} from "cloudflare:test";
import { type IncomingRequestCfProperties } from "@cloudflare/workers-types";
import { describe, it, expect } from "vitest";
import app from "../src/main";

// For now, you'll need to do something like this to get a correctly-typed
// `Request` to pass to `worker.fetch()`.
const IncomingRequest = Request<unknown, IncomingRequestCfProperties>;

describe("exampleRouter", () => {
  it("responds with OK (unit style)", async () => {
    const request = new IncomingRequest("http://example.com");
    // Create an empty context to pass to `worker.fetch()`
    const ctx = createExecutionContext();
    const response = await app.fetch(request, env, ctx);
    // Wait for all `Promise`s passed to `ctx.waitUntil()` to settle before running test assertions
    await waitOnExecutionContext(ctx);
    expect(await response.text()).toBe("OK");
  });

  it("responds with Hello World! (integration style)", async () => {
    const response = await SELF.fetch("https://example.com");
    expect(await response.text()).toMatchInlineSnapshot(`"OK"`);
  });
});
