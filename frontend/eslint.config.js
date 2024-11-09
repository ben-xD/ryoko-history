import sharedEslintConfig from "@repo/eslint-config/web.eslint.config.js";
import tseslint from "typescript-eslint";

export default tseslint.config(...sharedEslintConfig, {
  languageOptions: {
    parserOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      project: [
        "./tsconfig.json",
        "./tsconfig.react.json",
        "./tsconfig.config.json",
      ],
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
