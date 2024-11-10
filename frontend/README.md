# frontend

## Setup

- See root README for general setup instructions
- build the frontend and it's dependencies: run `turbo build`
- Create a cloudflare pages project: `pnpm run deploy`, or get a `wrangler.toml` from someone who has set this project up (if they're your friend), or create one yourself with `cp example.wrangler.toml wrangler.toml` (inside this folder)
- Wait for the DNS records to get set up (it takes a few minutes), before trying to visit your new project URL
- Read package.json scripts section to see commands

## Usage
- Run `pnpm generate-client` if any backend code has changed
- Start dev server: `pnpm dev`