import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

// F044 T003's frame-pipeline trace stage builds this harness fresh into a scratch `outDir`
// (never the shared `apps/ui/dist`, DECISION F039 D9); it is never part of the shipped app's
// own build, whose `rollupOptions.input` in `apps/ui/vite.config.ts` names only the root
// `index.html` one directory up. This harness is only ever built, never served by `vite dev`,
// so it declares no `server.fs.allow` of its own.
const harnessDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  root: harnessDir,
  base: "/",
  plugins: [react()],
  build: {
    sourcemap: false,
    rollupOptions: {
      input: path.join(harnessDir, "index.html"),
    },
  },
});
