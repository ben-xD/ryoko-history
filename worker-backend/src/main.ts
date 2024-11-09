import { swaggerUI } from "@hono/swagger-ui";
import { OpenAPIHono } from "@hono/zod-openapi";
import { apiReference as scalarUI } from "@scalar/hono-api-reference";
import type { AppContext } from "./AppContext";
import { cors } from "hono/cors";
import { exampleRouter } from "./routers/exampleRouter";
import { connectToDb } from "./db/db";

// See https://hono.dev/docs/concepts/stacks and https://hono.dev/docs/guides/rpc for more information
// For streaming LLM responses over SSE, we can use https://hono.dev/docs/helpers/streaming#streamsse
// For middlewares, see https://hono.dev/docs/guides/middleware

const ryoko = "ryoko";
const appVersion = "0.0.1";
const openapiPath = "/openapi.json";
const app = new OpenAPIHono<AppContext>()
  .doc31(openapiPath, {
    openapi: "3.1.0",
    info: {
      version: appVersion,
      title: ryoko,
    },
  })
  .use("/api/*", cors())
  .use(async (c, next) => {
    // https://hono.dev/docs/api/context#set-get
    c.set("db", connectToDb(c.env.DATABASE_URL, c.env.LOG_DATABASE));
    await next();
  })
  // More middlewares:
  // .use(async (c, next) => {
  //   await next();
  // })
  .route("/api/example", exampleRouter)
  // TODO Register more routers here.
  .get("/", (c) => {
    return c.text("OK");
  })
  // .get('/urls', (c) => {
  //   // Just to debug environment variables.
  //   const oakUrl = c.env.OAK_NATIONAL_ACADEMY_HTTP_URL;
  //   return c.text(oakUrl);
  // })
  .get("/docs", swaggerUI({ url: openapiPath }))
  .get(
    "/scalar",
    scalarUI({
      spec: {
        url: openapiPath,
      },
    }),
  );

export default app;

export type AppType = typeof app;
