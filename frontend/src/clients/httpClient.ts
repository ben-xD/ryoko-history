// Warning: use `import type`, rather than `import` to avoid accidentally importing backend packages that are transitively imported. This would cause the application to fail to start.
import { env } from "../env";

import createClient from "openapi-fetch";
import type {components, paths} from '../codegen/client';


export type Schema = components["schemas"];
export const client = createClient<paths>({ baseUrl: env.backendHttpUrl });


export type CreateTravelSummaryMetadata = Schema["CreateTravelSummaryMetadata"]

//Examples
// const reply = await client.POST("/uploadfiles/", {
//     body: {files: []}
// })

// Get presigned URL for elevenlabs:
// const reply = await client.POST("/conversation/signed-url/")


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