// Warning: use `import type`, rather than `import` to avoid accidentally importing backend packages that are transitively imported. This would cause the application to fail to start.
import { env } from "../env";

import createClient from "openapi-fetch";
import type {paths} from '../codegen/client';

export const client = createClient<paths>({ baseUrl: env.backendHttpUrl });


//Examples
// const reply = await client.POST("/uploadfiles/", {
//     body: {files: []}
// })


// // 
// const mutation = useMutation({
//     mutationFn: async (files: File[]) => {
//         const reply = await client.POST("/uploadfiles/", {
//             body: {files}
//         })
//         return reply;
//     }
// })

// if (mutation.isLoading) {
//     return <div>Loading...</div>
// }
// if (mutation.data) {
//     return <div>Success!</div>
// }