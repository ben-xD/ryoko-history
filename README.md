# ryoko

AI video summary of your travels in any language

## Project history

Created as part of [ElevenLabs consumer AI hackathon in London](https://partiful.com/e/azjS3QhW3YQZVr2NdPbN?).

Created by Miki Suzuki, Jim Plimmer and Ben Butterworth

Submitted on https://consumer-ai-hackathon-london.devpost.com/

## URLs:

- Frontend: https://ryoko.pages.dev/

## Technology selection

- Frontend: Typescript, React, Vite
- Backend: Python, FastAPI, ffmpeg
- Storage: Cloudflare R2
- APIs: ElevenLabs, Luma labs, OpenAI

## Setup

- Install dependencies: `pnpm install`
- Create supabase account and project
- Create cloudflare account
  - [Paid cloudflare accounts only] Create a [hyperdrive configuration](https://developers.cloudflare.com/hyperdrive/examples/supabase/)
- Install podman desktop, launch it and make sure compose, kubectl and podman is installed
- Start containers (e.g. database): `podman compose up -d`

## Deployment process
- Make sure DB is up to date (migrated)
- Deploy backend
- Build frontend
- Deploy frontend

## TODOs

- Call ElevenLabs to generate voice from transcript
- Create nice output (end to end). Find a great example to demo.
- Create video recording of demo
- Create slides (Problem, tech)

- Low priority
  - read exifmetadata from images in backend
