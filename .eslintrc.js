module.exports = {
    extends: [
      'eslint:recommended',
      'plugin:@typescript-eslint/eslint-recommended',
      'plugin:@typescript-eslint/recommended',
      'plugin:prettier/recommended',
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      project: 'tsconfig.json',
      sourceType: 'module'
    },
    plugins: ['@typescript-eslint'],
    rules: {
      '@typescript-eslint/ban-ts-ignore': 'off', //stackoverflow.com/questions/59729654/how-ignore-typescript-errors-with-ts-ignore
      '@typescript-eslint/camelcase': 'off',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/naming-convention': [ // https://stackoverflow.com/questions/62915344/eslint-erro-when-adding-rule-typescript-eslint-interface-name-prefix
        "error",
          {
          "selector": "interface",
          "format": ["PascalCase"],
          "custom": {
            "regex": "^I[A-Z]",
            "match": true
          }
        }
      ],
      '@typescript-eslint/ban-ts-comment': [
        'error',
        {'ts-ignore': false},
      ],
      '@typescript-eslint/no-unused-vars': ['warn', { args: 'none' }],
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-namespace': 'off',
      '@typescript-eslint/no-this-alias': [
        'error',
        {
          allowedNames: ['self'], // Allow `const self = this`
        },
      ],
      '@typescript-eslint/no-use-before-define': 'off',
      '@typescript-eslint/quotes': [
        'error',
        'single',
        { avoidEscape: true, allowTemplateLiterals: false }
      ],
      curly: ['error', 'all'],
      eqeqeq: 'error',
      'prefer-arrow-callback': 'error'
    }
  };
