import sharedEslintConfig from "@repo/eslint-config/node.eslint.config.js";
import tseslint from "typescript-eslint";

export default tseslint.config(...sharedEslintConfig, {
  languageOptions: {
    parserOptions: {
      tsconfigRootDir: import.meta.dirname,
      project: [
        "./tsconfig.json",
        "./tsconfig.config.json",
        "./tsconfig.fe-client.json",
        "./tsconfig.worker.json",
        "./tsconfig.tests.json",
      ],
    },
  },
});
