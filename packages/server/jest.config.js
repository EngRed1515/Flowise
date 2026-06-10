module.exports = {
    testEnvironment: 'node',
    testMatch: ['<rootDir>/test/**/*.test.ts'],
    moduleNameMapper: {
        // Resolve the workspace package from source so tests run without a prior build
        '^flowise-components$': '<rootDir>/../components/src/index.ts'
    },
    // Allow the mapped flowise-components sources (outside <rootDir>) to be transformed
    roots: ['<rootDir>', '<rootDir>/../components/src']
}
