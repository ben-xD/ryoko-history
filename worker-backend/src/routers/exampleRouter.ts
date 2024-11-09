import { createRoute, OpenAPIHono, z } from "@hono/zod-openapi";
import type { AppContext } from "../AppContext";
import { ErrorSchema } from "../schema/error";

const ExamplePostRequestSchema = z.object({
  message: z.string().openapi({
    example: "123",
  }),
});

const PostRequestCompletedSchema = z.object({});

export const exampleRouter = new OpenAPIHono<AppContext>().openapi(
  createRoute({
    method: "post",
    path: "/example-post",
    request: {
      body: {
        content: {
          "application/json": {
            schema: ExamplePostRequestSchema,
          },
        },
      },
    },
    responses: {
      200: {
        content: {
          "application/json": {
            schema: PostRequestCompletedSchema,
          },
        },
        description: "Retrieve the user",
      },
      500: {
        description: "Internal server error",
        content: {
          "application/json": {
            schema: ErrorSchema,
          },
        },
      },
    },
  }),
  async (c) => {
    return c.json({}, 200);
  },
);
