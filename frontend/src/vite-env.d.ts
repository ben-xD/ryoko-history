/// <reference types="vite/client" />

// https://www.npmjs.com/package/vite-plugin-svgr
/// <reference types="vite-plugin-svgr/client" />

// See https://vite.dev/guide/env-and-mode#intellisense-for-typescript
interface ImportMetaEnv {
  readonly VITE_BACKEND_HTTP_URL: string;
  readonly ENABLED_ROUTER_DEVTOOLS: string;
  // more env variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
