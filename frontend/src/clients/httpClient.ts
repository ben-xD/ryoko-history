// Warning: use `import type`, rather than `import` to avoid accidentally importing backend packages that are transitively imported. This would cause the application to fail to start.
import { env } from "../env";
import { hcWithType } from "@repo/backend/httpClient";

export const client = hcWithType(env.backendHttpUrl);

// Less efficient example, but works without needing to build the backend (more type inference at runtime)
// import {hc} from 'hono/client';
// import type {AppType} from '@repo/backend';
// export const client = hc<AppType>(env.backendHttpUrl);
