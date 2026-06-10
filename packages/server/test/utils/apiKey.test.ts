import { generateAPIKey, generateSecretHash, compareKeys } from '../../src/utils/apiKey'

describe('generateAPIKey', () => {
    it('should generate a base64url-encoded key', () => {
        const apiKey = generateAPIKey()
        expect(apiKey).toMatch(/^[A-Za-z0-9_-]+$/)
        expect(Buffer.from(apiKey, 'base64url')).toHaveLength(32)
    })

    it('should generate a different key on each call', () => {
        expect(generateAPIKey()).not.toBe(generateAPIKey())
    })
})

describe('generateSecretHash', () => {
    it('should produce a hash in the format <hash>.<salt>', () => {
        const secretHash = generateSecretHash(generateAPIKey())
        const [hash, salt] = secretHash.split('.')
        expect(hash).toMatch(/^[a-f0-9]{128}$/)
        expect(salt).toMatch(/^[a-f0-9]{16}$/)
    })

    it('should produce different hashes for the same key thanks to the random salt', () => {
        const apiKey = generateAPIKey()
        expect(generateSecretHash(apiKey)).not.toBe(generateSecretHash(apiKey))
    })
})

describe('compareKeys', () => {
    it('should accept the key the hash was generated from', () => {
        const apiKey = generateAPIKey()
        const secretHash = generateSecretHash(apiKey)
        expect(compareKeys(secretHash, apiKey)).toBe(true)
    })

    it('should reject a different key', () => {
        const secretHash = generateSecretHash(generateAPIKey())
        expect(compareKeys(secretHash, generateAPIKey())).toBe(false)
    })
})
