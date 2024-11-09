// Warning: use `import type`, rather than `import` to avoid accidentally importing backend packages that are transitively imported. This would cause the application to fail to start.
import { env } from "../env";

import createClient from "openapi-fetch";
import type {paths} from '../codegen/client';

export const client = createClient<paths>({ baseUrl: env.backendHttpUrl });
