import { build, defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

// F039 T003, DECISION F039 D8 — a page opened from `file://` can load no chunk: the story
// player is built a second time, once the cockpit's own build closes, as ONE script and ONE
// style sheet under fixed names, so the export can inline both into a page that needs no
// server and no module loader.
export const STORY_PLAYER_OUT_DIR = "dist/story";

function storyPlayerBuild(): Plugin {
  return {
    name: "remedy-story-player",
    apply: "build",
    async closeBundle() {
      await build({
        configFile: false,
        root: ".",
        base: "./",
        logLevel: "warn",
        plugins: [react()],
        build: {
          outDir: STORY_PLAYER_OUT_DIR,
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
