import { defineConfig } from "vite";

export default defineConfig({
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
});
