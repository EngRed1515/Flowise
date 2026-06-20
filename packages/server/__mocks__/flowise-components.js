/**
 * Manual mock for the `flowise-components` workspace package.
 *
 * Jest automatically uses manual mocks placed in a root-level `__mocks__`
 * directory for node_modules packages, so every test that (transitively)
 * imports `flowise-components` gets this stub instead of the real package.
 *
 * The real package `export *`s the entire component library, which drags in a
 * large graph of integration SDKs — several of them pure ESM (langchain,
 * axios, ...) that CommonJS jest cannot load. The unit tests only need the
 * named exports to exist, not to do anything, so every export resolves to a
 * no-op proxy (callable, constructable, and property-accessible).
 *
 * If a test needs real behaviour from a specific export, mock that export
 * explicitly in the test instead of relying on this stub.
 */
module.exports = require('../jest/esmStub.js')
