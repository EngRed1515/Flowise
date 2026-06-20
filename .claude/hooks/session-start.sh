#!/bin/bash
set -euo pipefail

# Only run in Claude Code on the web (remote) sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# The `faiss-node` native dependency needs system BLAS/LAPACK to compile.
# Install them best-effort; never let this step fail the session start.
if command -v apt-get >/dev/null 2>&1; then
  apt-get install -y libopenblas-dev liblapack-dev >/dev/null 2>&1 || true
fi

# Enable pnpm via corepack if it isn't already on PATH.
if ! command -v pnpm >/dev/null 2>&1; then
  corepack enable >/dev/null 2>&1 || true
fi

# Install workspace dependencies. A plain `install` (not a frozen/ci install)
# lets the cached container state be reused across sessions and is idempotent.
# If a native build (e.g. faiss-node without BLAS) fails, fall back to an
# install that skips build scripts so lint/test deps are still available.
pnpm install || pnpm install --ignore-scripts
