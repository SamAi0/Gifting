import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    rules: {
      // Allow setState in effects for context providers that synchronize external state
      'react-hooks/set-state-in-effect': 'warn',
      // Allow exporting contexts and hooks from context files
      'react-refresh/only-export-components': ['warn', { allowExportNames: ['useAuth', 'useCart', 'AuthContext', 'CartContext', 'AuthProvider', 'CartProvider'] }],
    },
  },
])
