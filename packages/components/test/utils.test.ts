import { z } from 'zod'
import {
    getInputVariables,
    handleEscapeCharacters,
    handleErrorMessage,
    serializeQueryParams,
    convertSchemaToZod,
    flattenObject,
    convertChatHistoryToText,
    serializeChatHistory,
    convertMultiOptionsToStringArray,
    getCredentialParam
} from '../src/utils'
import { ICommonObject, IMessage, INodeData } from '../src/Interface'

describe('getInputVariables', () => {
    it('should extract single-brace variables from a prompt template', () => {
        expect(getInputVariables('Tell me a {adjective} joke about {topic}')).toEqual(['adjective', 'topic'])
    })

    it('should return an empty array when there are no variables', () => {
        expect(getInputVariables('No variables here')).toEqual([])
    })

    it('should skip escaped curly brackets', () => {
        expect(getInputVariables('Escaped \\{notavariable\\} but {realvariable}')).toEqual(['realvariable'])
    })

    it('should return an empty array for non-string input', () => {
        expect(getInputVariables(undefined as unknown as string)).toEqual([])
    })

    it('should ignore an unclosed bracket', () => {
        expect(getInputVariables('An {unclosed variable never ends')).toEqual([])
    })
})

describe('handleEscapeCharacters', () => {
    it('should encode special characters in a string', () => {
        expect(handleEscapeCharacters('line one\nline two\tend', false)).toBe('line oneFLOWISE_NEWLINEline twoFLOWISE_TABend')
    })

    it('should decode special characters back', () => {
        expect(handleEscapeCharacters('line oneFLOWISE_NEWLINEline twoFLOWISE_TABend', true)).toBe('line one\nline two\tend')
    })

    it('should round-trip a string with quotes and backslashes', () => {
        const original = 'He said "hello" \\ goodbye\r\n'
        const encoded = handleEscapeCharacters(original, false)
        expect(handleEscapeCharacters(encoded, true)).toBe(original)
    })

    it('should encode strings nested inside objects', () => {
        const input = { outer: { inner: 'a\nb' }, plain: 1 }
        const result = handleEscapeCharacters(input, false)
        expect(result.outer.inner).toBe('aFLOWISE_NEWLINEb')
        expect(result.plain).toBe(1)
    })

    it('should return non-string non-object input untouched', () => {
        expect(handleEscapeCharacters(42, false)).toBe(42)
    })
})

describe('handleErrorMessage', () => {
    it('should use the error message', () => {
        expect(handleErrorMessage(new Error('something failed'))).toBe('something failed. ')
    })

    it('should append the response data error string', () => {
        const error = { message: 'Request failed', response: { data: { error: 'invalid key' } } }
        expect(handleErrorMessage(error)).toBe('Request failed. invalid key. ')
    })

    it('should stringify object response errors', () => {
        const error = { response: { data: { error: { code: 401 } } } }
        expect(handleErrorMessage(error)).toBe('{"code":401}. ')
    })

    it('should fall back to a generic message', () => {
        expect(handleErrorMessage({})).toBe('Unexpected Error.')
    })
})

describe('serializeQueryParams', () => {
    it('should serialize simple key-value pairs', () => {
        expect(serializeQueryParams({ q: 'flowise', page: 2 })).toBe('q=flowise&page=2')
    })

    it('should skip null and undefined values', () => {
        expect(serializeQueryParams({ a: 1, b: null, c: undefined })).toBe('a=1')
    })

    it('should serialize arrays with indexes by default', () => {
        expect(serializeQueryParams({ tag: ['x', 'y'] })).toBe('tag[0]=x&tag[1]=y')
    })

    it('should serialize arrays without indexes when skipIndex is set', () => {
        expect(serializeQueryParams({ tag: ['x', 'y'] }, true)).toBe('tag=x&tag=y')
    })

    it('should encode spaces as plus signs', () => {
        expect(serializeQueryParams({ q: 'hello world' })).toBe('q=hello+world')
    })
})

describe('convertSchemaToZod', () => {
    it('should convert a JSON string schema to zod types', () => {
        const schema = JSON.stringify([
            { property: 'title', type: 'string', description: 'Title of the item', required: true },
            { property: 'count', type: 'number', description: 'How many', required: false },
            { property: 'active', type: 'boolean', description: 'Is active', required: false }
        ])
        const zodObj = convertSchemaToZod(schema)
        expect(zodObj.title).toBeInstanceOf(z.ZodString)
        expect(zodObj.count).toBeInstanceOf(z.ZodNumber)
        expect(zodObj.active).toBeInstanceOf(z.ZodBoolean)
    })

    it('should accept an already parsed schema object', () => {
        const zodObj = convertSchemaToZod([{ property: 'name', type: 'string', description: 'Name', required: true }])
        expect(zodObj.name).toBeInstanceOf(z.ZodString)
    })

    it('should throw on invalid JSON', () => {
        expect(() => convertSchemaToZod('not valid json')).toThrow()
    })
})

describe('flattenObject', () => {
    it('should flatten nested objects using dot notation', () => {
        expect(flattenObject({ a: { b: { c: 1 } }, d: 2 })).toEqual({ 'a.b.c': 1, d: 2 })
    })

    it('should return an empty object for empty input', () => {
        expect(flattenObject({})).toEqual({})
    })

    it('should keep top-level scalar values', () => {
        expect(flattenObject({ key: 'value' })).toEqual({ key: 'value' })
    })
})

describe('convertChatHistoryToText', () => {
    it('should prefix messages by their role', () => {
        const history: IMessage[] = [
            { message: 'Hi there', type: 'userMessage' },
            { message: 'Hello, how can I help?', type: 'apiMessage' }
        ]
        expect(convertChatHistoryToText(history)).toBe('Human: Hi there\nAssistant: Hello, how can I help?')
    })

    it('should return an empty string for empty history', () => {
        expect(convertChatHistoryToText()).toBe('')
    })
})

describe('serializeChatHistory', () => {
    it('should join array history with newlines', () => {
        expect(serializeChatHistory(['one', 'two'])).toBe('one\ntwo')
    })

    it('should return string history as-is', () => {
        expect(serializeChatHistory('already a string')).toBe('already a string')
    })
})

describe('convertMultiOptionsToStringArray', () => {
    it('should parse a JSON array string', () => {
        expect(convertMultiOptionsToStringArray('["a","b"]')).toEqual(['a', 'b'])
    })

    it('should return an empty array for invalid JSON', () => {
        expect(convertMultiOptionsToStringArray('not json')).toEqual([])
    })
})

describe('getCredentialParam', () => {
    const credentialData: ICommonObject = { apiKey: 'from-credential' }

    it('should prefer the node input value over the credential value', () => {
        const nodeData = { inputs: { apiKey: 'from-node' } } as unknown as INodeData
        expect(getCredentialParam('apiKey', credentialData, nodeData)).toBe('from-node')
    })

    it('should fall back to the credential value', () => {
        const nodeData = { inputs: {} } as unknown as INodeData
        expect(getCredentialParam('apiKey', credentialData, nodeData)).toBe('from-credential')
    })

    it('should return undefined when the param exists nowhere', () => {
        const nodeData = { inputs: {} } as unknown as INodeData
        expect(getCredentialParam('missing', credentialData, nodeData)).toBeUndefined()
    })
})
