import { generateEncryptKey, encryptCredentialData, decryptCredentialData, redactCredentialWithPasswordType } from '../../src/utils'
import { IComponentCredentials } from '../../src/Interface'

const REDACTED_VALUE = '_FLOWISE_BLANK_07167752-1a71-43b1-bf8f-4f32252165db'

const componentCredentials: IComponentCredentials = {
    openAIApi: {
        label: 'OpenAI API',
        name: 'openAIApi',
        version: 1,
        inputs: [
            {
                label: 'OpenAI Api Key',
                name: 'openAIApiKey',
                type: 'password'
            },
            {
                label: 'Organization',
                name: 'organization',
                type: 'string'
            }
        ]
    }
} as unknown as IComponentCredentials

describe('credential encryption', () => {
    const ORIGINAL_ENV = process.env

    beforeAll(() => {
        process.env = { ...ORIGINAL_ENV, FLOWISE_SECRETKEY_OVERWRITE: 'test-encryption-key' }
    })

    afterAll(() => {
        process.env = ORIGINAL_ENV
    })

    it('should encrypt and decrypt credential data back to the original object', async () => {
        const plainData = { openAIApiKey: 'sk-secret-value', organization: 'org-123' }
        const encrypted = await encryptCredentialData(plainData)

        expect(typeof encrypted).toBe('string')
        expect(encrypted).not.toContain('sk-secret-value')

        const decrypted = await decryptCredentialData(encrypted)
        expect(decrypted).toEqual(plainData)
    })

    it('should redact password-type fields when decrypting for the client', async () => {
        const plainData = { openAIApiKey: 'sk-secret-value', organization: 'org-123' }
        const encrypted = await encryptCredentialData(plainData)

        const decrypted = await decryptCredentialData(encrypted, 'openAIApi', componentCredentials)
        expect(decrypted.openAIApiKey).toBe(REDACTED_VALUE)
        expect(decrypted.organization).toBe('org-123')
    })
})

describe('generateEncryptKey', () => {
    it('should generate a base64-encoded 24-byte key', () => {
        const key = generateEncryptKey()
        expect(Buffer.from(key, 'base64')).toHaveLength(24)
    })

    it('should generate a different key on each call', () => {
        expect(generateEncryptKey()).not.toBe(generateEncryptKey())
    })
})

describe('redactCredentialWithPasswordType', () => {
    it('should replace only password-type fields with the redacted placeholder', () => {
        const decrypted = { openAIApiKey: 'sk-secret-value', organization: 'org-123' }
        const redacted = redactCredentialWithPasswordType('openAIApi', decrypted, componentCredentials)

        expect(redacted.openAIApiKey).toBe(REDACTED_VALUE)
        expect(redacted.organization).toBe('org-123')
    })

    it('should not mutate the original credential object', () => {
        const decrypted = { openAIApiKey: 'sk-secret-value' }
        redactCredentialWithPasswordType('openAIApi', decrypted, componentCredentials)
        expect(decrypted.openAIApiKey).toBe('sk-secret-value')
    })
})
