import { z } from "zod";

// Usage: Limit usage of environment variables (import.meta.env) to this file. Don't use it outside, to keep it readable. Import the `env` object anywhere else.

const envSchema = z.object({
  backendHttpUrl: z.string().min(1),
  enableRouterDevtools: z.boolean(),
  //   VITE_SENTRY_DSN: z.string().min(1),
  //   VITE_POSTHOG_CLIENT_TOKEN: z.string().min(1),
});
type EnvSchema = z.infer<typeof envSchema>;

// We access the environment variables directly here instead of using `envSchema.parse(import.meta.env)` because
// vite won't replace the environment variables in the build if we do that.
export const validateEnv = () =>
  envSchema.parse({
    backendHttpUrl: import.meta.env.VITE_BACKEND_HTTP_URL,
    enableRouterDevtools: z
      .union([
        z.undefined(),
        z.boolean(),
        z.literal("true"),
        z.literal("false"),
      ])
      .transform((value) => value === true || value === "true")
      .parse(import.meta.env.VITE_ENABLE_ROUTER_DEVTOOLS),
    // VITE_SENTRY_DSN: import.meta.env.VITE_SENTRY_DSN,
    // VITE_POSTHOG_CLIENT_TOKEN: import.meta.env.VITE_POSTHOG_CLIENT_TOKEN,
  } satisfies EnvSchema);

export const env = validateEnv();
