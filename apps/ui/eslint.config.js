import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  {
    files: ["src/**/*.{ts,tsx}"],
    // R-0622: without the TypeScript parser every file stopped at its first type
    // annotation, so no rule below ever evaluated.
    languageOptions: { parser: tseslint.parser },
    // Registered so a `@typescript-eslint/...` disable comment names a rule that exists.
    plugins: { "react-hooks": reactHooks, "@typescript-eslint": tseslint.plugin },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "no-unused-vars": "off",
      // typescript-eslint's own guidance: `tsc` resolves names, including the DOM
      // globals and type names this rule cannot see, and `npm run typecheck` is gated.
      "no-undef": "off",
      // The one typescript-eslint rule this source already opts out of by region
      // (`src/api/remedyApi.ts`), so the opt-out means what it says.
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
  {
    ignores: ["dist/**", "node_modules/**", "legacy/**"],
  },
];
