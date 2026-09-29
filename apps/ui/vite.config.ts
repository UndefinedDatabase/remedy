import path from "node:path";
import { build, defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

// F039 T003, DECISION F039 D9 — the player lands in this subdirectory of whatever `outDir`
// the cockpit's own build resolved, `dist/story` by default.
export const STORY_PLAYER_SUBDIR = "story";

function storyPlayerBuild(): Plugin {
  let outDir = "dist";
  return {
    name: "remedy-story-player",
    apply: "build",
    configResolved(config) {
      outDir = path.resolve(config.root, config.build.outDir);
    },
    async closeBundle() {
      await build({
        configFile: false,
        root: ".",
        base: "./",
        logLevel: "warn",
        plugins: [react()],
        build: {
          outDir: path.join(outDir, STORY_PLAYER_SUBDIR),
          emptyOutDir: true,
          sourcemap: false,
          copyPublicDir: false,
          cssCodeSplit: false,
          modulePreload: false,
          rollupOptions: {
            input: "src/storyPlayerMain.tsx",
            output: {
              entryFileNames: "story-player.js",
              assetFileNames: "story-player[extname]",
              inlineDynamicImports: true,
            },
          },
        },
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), storyPlayerBuild()],
  root: ".",
  base: "/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: false,
    rollupOptions: {
      input: "index.html",
    },
  },
  server: {
    host: "127.0.0.1",
  },
});
