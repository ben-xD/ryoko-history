# backend

## Setup

- See root README for general setup instructions
- Create a cloudflare worker project: `pnpm run deploy`, or get a `wrangler.toml` from someone who has set this project up (if they're your friend), or create one yourself with `cp example.wrangler.toml wrangler.toml` (inside this folder)
- Wait for the DNS records to get set up (it takes a few minutes), before trying to visit your new project URL
- Read package.json scripts section to see commands

## Changing secrets

- Use `pnpx wrangler secret`, e.g. `pnpx wrangler secret put`

## Testing

- We pin vitest to 2.0.5 because "Currently, the @cloudflare/vitest-pool-workers package only works with Vitest 2.0.5.". Check back on https://developers.cloudflare.com/workers/testing/vitest-integration/get-started/write-your-first-test/ to see if we can upgrade vitest.

## Need more code?

- Need a Python backend? Use FastAPI and OpenAPI client generation for the frontend, similar to https://github.com/ben-xD/melange
- Need maps? Use deck.gl or Cesium, and see how Geojsons.com does it
- Need CI? See how Geojsons.com configures it

## Notes

- **OpenAPI integration**: I previously used trpc-openapi, which was quicker to define API routes, more similar to how FastAPI, a python framework. With Hono's OpenAPI integration (and Fastify), there's more openapi config you need to specify. It takes more time to write APIs, but it does mean you are in full control and underrstanding of the API, it is defined to OpenAPI standards, and instead it being implicit in the function definitions, and not compatible with non-tRPC clients.
- `turbo.jsonc` is the file you should edit since you won't get any IDE warnings about comments being in a JSON file. It is just a symlink to `turbo.json`, which Turbo will read. Turbo also doesn't care about comments. 
- Cloudflare workers / wrangler / miniflare: It's annoying that sometimes the server will fail to start, and I get no errors anywhere.
- The boiler plate code here was based on my older projects:
  - Zuko https://github.com/ben-xD/zuko
  - A template https://github.com/ben-xD/hono-rpc-openapi-cloudflare-drizzle-turbo
  - TalkDash https://talkdash.orth.uk/