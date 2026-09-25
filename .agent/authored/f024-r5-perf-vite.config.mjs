import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scratchDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  root: scratchDir,
  base: "/",
  plugins: [react()],
  build: {
    outDir: path.join(scratchDir, "dist"),
    emptyOutDir: true,
    sourcemap: false,
    rollupOptions: {
      input: path.join(scratchDir, "index.html"),
    },
  },
  server: {
    host: "127.0.0.1",
    fs: {
      // Harness imports ForceBrainGraph.tsx, brainPerfFixture.ts etc. straight
      // from the repo root's apps/ui/src, outside this scratch root.
      allow: [scratchDir, path.resolve(scratchDir, "../../apps/ui")],
    },
  },
});
