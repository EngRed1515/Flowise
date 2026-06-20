/**
 * Generic stand-in for ESM-only packages (e.g. `langchain`, `@langchain/*`)
 * that are imported through the dependency graph but are NOT exercised by the
 * unit tests. Jest runs in CommonJS and cannot `require()` these pure-ESM
 * packages, so they are mapped here via `moduleNameMapper`.
 *
 * Every named/default export resolves to the same value, which is:
 *   - callable      → returns undefined
 *   - constructable → returns an empty object (so `extends` works)
 *   - any property  → returns the stub again (recursively)
 *
 * If a test ever needs real behaviour from one of these packages, mock that
 * specific export explicitly instead of relying on this stub.
 */
function Stub() {}

const proxy = new Proxy(Stub, {
    get(_target, prop) {
        if (prop === '__esModule') return true
        if (prop === 'default') return proxy
        return proxy
    },
    apply() {
        return undefined
    },
    construct() {
        return {}
    }
})

module.exports = proxy
