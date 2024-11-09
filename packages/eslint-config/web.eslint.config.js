import globals from "globals";
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import eslintReactRecommended from "eslint-plugin-react/configs/recommended.js";
import eslintReactJsxRuntime from "eslint-plugin-react/configs/jsx-runtime.js";
import eslintPluginReactHooks from "eslint-plugin-react-hooks";
import eslintPluginPrettier from "eslint-plugin-prettier";
import tseslintParser from "@typescript-eslint/parser";
import eslintTanstackQuery from "@tanstack/eslint-plugin-query";
import eslintTailwind from "eslint-plugin-tailwindcss";
import { fixupPluginRules } from "@eslint/compat";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strict,
  ...tseslint.configs.stylistic,
  ...eslintTailwind.configs["flat/recommended"],
  ...eslintTanstackQuery.configs["flat/recommended"],
  eslintReactRecommended,
  eslintReactJsxRuntime,
  // This needs to in a separate object to be a "global ignore". See https://github.com/eslint/eslint/discussions/17429
  { ignores: ["dist", "*.gen.ts", "vite.config.ts.timestamp-*.mjs", ".wrangler"] },
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2020,
      },
      parser: tseslintParser,
      // These are merged in with the parserOptions from the project specific eslint.config.js
      parserOptions: {
        // Handy to debug which tsconfig.json files are being used:
        //   debugLevel: true,
        ecmaVersion: "latest",
        sourceType: "module",
        // No point setting these because they'll be wrong for specific projects:
        // project: [],
        // tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      prettier: eslintPluginPrettier,
      "react-hooks": fixupPluginRules(eslintPluginReactHooks),
    },
    settings: {
      react: {
        version: "detect",
      },
      // See https://www.npmjs.com/package/eslint-plugin-tailwindcss for more options
      tailwindcss: {
        cssFiles: [
          "**/*.css",
          // eslint-plugin-tailwindcss doesn't detect the style.css file from the design system without this:
          "./node_modules/@repo/design-system/dist/style.css"
        ]
      }
    },
    rules: {
      ...eslintPluginReactHooks.configs.recommended.rules,

      // Disable prop-types rule since we use TS. This does disable runtime prop checks
      // We do this to prevent errors in some shadcn/ui components e.g. `error  'className' is missing in props validation`
      // Code taken from https://github.com/shadcn-ui/ui/issues/120#issuecomment-1828081539
      "react/prop-types": "off",

      // Prevent if (!value) causing bugs when value==0 is treated like value is not set.
      // See https://stackoverflow.com/a/64995330/7365866 and https://stackoverflow.com/a/78267055/7365866
      "@typescript-eslint/strict-boolean-expressions": "error",

      // Annoying error after creating a new component from templates
      "@typescript-eslint/no-empty-object-type": "off",

      eqeqeq: ["error", "always"],

      // Inspired from https://www.themosaad.com/blog/two-years-of-tailwind-css
      // Enforce typesafety for Tailwind CSS classnames
      // https://github.com/francoismassart/eslint-plugin-tailwindcss/blob/master/docs/rules/no-custom-classname.md
      "tailwindcss/no-custom-classname": "error",

      // Avoid contradicting Tailwind CSS classnames
      // https://github.com/francoismassart/eslint-plugin-tailwindcss/blob/master/docs/rules/no-contradicting-classname.md
      "tailwindcss/no-contradicting-classname": "error",

      // Disable this lint rule because it crashes eslint when linting an enum:
      // TypeError: Cannot read properties of undefined (reading 'members')
      "@typescript-eslint/no-duplicate-enum-values": "off",

      // Prevent @typescript-eslint/no-misused-promises errors in code like `<MenuItem onClick={copyToClipboard}>Copy</MenuItem>`
      // where copyToClipboard is an async function.
      // as per https://github.com/orgs/react-hook-form/discussions/8622#discussioncomment-4060570
      "@typescript-eslint/no-misused-promises": [
        2,
        {
          checksVoidReturn: {
            attributes: false,
          },
        },
      ],
    },
  },
);