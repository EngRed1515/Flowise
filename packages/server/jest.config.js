/** @type {import('jest').Config} */
module.exports = {
    setupFiles: [
        // Register the openai SDK's Node fetch shim before anything imports it,
        // otherwise its runtime detection throws under jest ("fetch is not
        // defined").
        'openai/shims/node',
        // Load the reflect-metadata polyfill before any TypeORM entity is
        // imported so column types are available when the decorators run.
        'reflect-metadata'
    ],
    // The `flowise-components` workspace package is pulled in through the import
    // graph and drags in several pure-ESM dependencies (langchain, axios, ...).
    // CommonJS jest cannot `require()` ESM, and these packages are not exercised
    // by the unit tests, so they are stubbed out here. See esmStub.js.
    moduleNameMapper: {
        '^langchain(/.*)?$': '<rootDir>/jest/esmStub.js',
        '^@langchain/.*$': '<rootDir>/jest/esmStub.js',
        '^langchainhub$': '<rootDir>/jest/esmStub.js',
        '^langsmith(/.*)?$': '<rootDir>/jest/esmStub.js',
        '^axios$': '<rootDir>/jest/esmStub.js'
    }
}
