---
name: build-test
description: Build, lint, format, and test the Flowise monorepo with the correct pnpm/turbo commands. Use when the user wants to build the project, run the linter, format code, run tests, or verify a change compiles before committing.
---

# Build & Test Flowise

Flowise is a pnpm + turbo monorepo (`packages/*`). Always run commands from the
repo root unless a step says otherwise. Requires Node `>=18.15 <19 || ^20` and
pnpm `>=9`.

## Install dependencies (run once per fresh checkout)

```bash
pnpm install
```

## Common tasks

| Goal | Command |
|------|---------|
| Build everything | `pnpm build` |
| Clean rebuild | `pnpm build-force` |
| Lint | `pnpm lint` |
| Auto-fix lint | `pnpm lint-fix` |
| Format with Prettier | `pnpm format` |
| Run server unit tests | `pnpm --filter flowise test` |
| Dev mode (all packages) | `pnpm dev` |

## Recommended pre-commit check

Before committing a change, run this sequence and make sure each step passes:

```bash
pnpm lint
pnpm build
pnpm --filter flowise test
```

## Notes

- The build is incremental via turbo; if you hit stale-cache issues use
  `pnpm build-force`.
- Tests live in `packages/server` (jest), configured by
  `packages/server/jest.config.js`. The server's import graph pulls in several
  pure-ESM packages (langchain, axios, the whole `flowise-components` package)
  that CommonJS jest cannot load; these are stubbed via `moduleNameMapper` and a
  manual mock in `packages/server/__mocks__/`. If a new test fails to load with
  "Cannot use import statement outside a module" or "Unexpected token 'export'",
  add the offending ESM package to the `moduleNameMapper` stubs in
  `jest.config.js`.
- Decorator metadata for TypeORM entities is provided by the root
  `babel.config.js`; `reflect-metadata` is loaded via jest `setupFiles`.
- Do not edit files under `dist/`, `build/`, or `node_modules/` — they are
  generated.
