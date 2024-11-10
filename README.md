# ryoko

AI video summary of your travels in any language

## TODOs (how to use this template)

- Install NodeJS and pnpm
- Use degit to clone the repo: run `pnpx degit --mode=git git@github.com:ben-xD/ts-react-hono-cloudflare-worker-drizzle-postgres-supabase-template.git new-project-name`
- Find and replace ryoko with your app name
- Update description in readme
- Update project section in readme
- Delete template TODOs section in readme
- Follow Setup section in this file and then for individual projects
- Design interactions / mvp features (first ideas, then sketching, then figma)
- Implement frontend and backend features when necessary. Do modelling of backend/db

## URLs:

- Frontend: https://ryoko.pages.dev/
- Backend/API: https://ryoko.benz.workers.dev
- Backend OpenAPI: https://ryoko.benz.workers.dev/docs
- Modern OpenAPI (Scalar): https://ryoko.benz.workers.dev/scalar
- Note: The API pages don't work over some VPNs (because the servers that host the openapi and scalar static assets block some VPNs - can be worked around)

## Technology selection

- Frontend: Typescript, React, Vite, Shadcn/ui, lucide icons, Cloudflare Pages
- Backend: Typescript, hono.js, Drizzle, Cloudflare Workers
- Database and storage: Postgres, Supabase, Cloudflare Hyperdrive, Cloudflare R2
- APIs: LLMs

## Setup

- Install dependencies: `pnpm install`
- Create supabase account and project
- Create cloudflare account
  - [Paid cloudflare accounts only] Create a [hyperdrive configuration](https://developers.cloudflare.com/hyperdrive/examples/supabase/)
- Install podman desktop, launch it and make sure compose, kubectl and podman is installed
- Start containers (e.g. database): `podman compose up -d`

## Project history

Created as part of [ElevenLabs consumer AI hackathon in London](https://partiful.com/e/azjS3QhW3YQZVr2NdPbN?).

Created by Miki Suzuki, Jim Plimmer and Ben Butterworth

## Deployment process
- Make sure DB is up to date (migrated)
- Deploy backend
- Build frontend
- Deploy frontend

## TODOs

- Try to integrate Conversational API in frontend. We can then just send the user transcript and assistant transcript (from the API response) as part of our "create video summary" API
- Call OpenAPI to generate transcript for voice
- Call ElevenLabs to generate voice from transcript
- Generate translations of voice over (for use case: grandmother in Japan)
- Create nice output (end to end). Find a great example to demo.
- Create video recording of demo
- Create slides (Problem, tech)
