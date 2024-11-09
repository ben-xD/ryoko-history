import eslint from "@eslint/js";
import tseslintParser from "@typescript-eslint/parser";
import eslintPluginPrettier from "eslint-plugin-prettier";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strict,
  ...tseslint.configs.stylistic,
  // This needs to in a separate object to be a "global ignore". See https://github.com/eslint/eslint/discussions/17429
  { ignores: ["dist", "*.gen.ts", "vite.config.ts.timestamp-*.mjs", ".wrangler"] },
  {
    languageOptions: {
      globals: {
        ...globals.node,
      },
      parser: tseslintParser,
      // These are merged in with the parserOptions from the project specific eslint.config.js
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        // No point setting these because they'll be wrong for specific projects:
        // project: [],
        // tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      prettier: eslintPluginPrettier,
    },
    settings: {},
    rules: {
      // Prevent if (!value) causing bugs when value==0 is treated like value is not set.
      // See https://stackoverflow.com/a/64995330/7365866 and https://stackoverflow.com/a/78267055/7365866
      "@typescript-eslint/strict-boolean-expressions": "error",

      eqeqeq: ["error", "always"],

      // Disable this lint rule because it crashes eslint when linting an enum:
      // TypeError: Cannot read properties of undefined (reading 'members')
      "@typescript-eslint/no-duplicate-enum-values": "off",
    },
  },
);