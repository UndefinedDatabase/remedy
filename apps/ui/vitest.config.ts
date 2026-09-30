import { defineConfig } from "vitest/config";

// amend0930-test-load: the same worker cap as tests/conftest.py. REMEDY_TEST_MAX_WORKERS unset
// or not a number means 6, and 0 means no limit.
const asked = Number.parseInt(process.env.REMEDY_TEST_MAX_WORKERS ?? "", 10);
const workerCap = Number.isNaN(asked) || asked < 0 ? 6 : asked;

export default defineConfig({
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
    ...(workerCap > 0 ? { maxWorkers: workerCap, minWorkers: 1 } : {}),
  },
});
