import { getVariableValue, resolveVariables, replaceInputsWithConfig, isSameOverrideConfig } from '../../src/utils'
import { IReactFlowNode, INodeData, IMessage } from '../../src/Interface'

const makeExecutedNode = (id: string, instance: any): IReactFlowNode => {
    return {
        id,
        position: { x: 0, y: 0 },
        type: 'customNode',
        data: {
            id,
            label: id,
            name: id.split('_')[0],
            type: id.split('_')[0],
            category: 'Chains',
            instance,
            inputs: {},
            inputParams: []
        }
    } as unknown as IReactFlowNode
}

const chatHistory: IMessage[] = [
    { message: 'What is Flowise?', type: 'userMessage' },
    { message: 'Flowise is a low-code LLM apps builder.', type: 'apiMessage' }
]

describe('getVariableValue', () => {
    it('should return the value untouched when it has no variables', () => {
        const result = getVariableValue('plain value', [], 'question', [])
        expect(result).toBe('plain value')
    })

    it('should resolve {{question}} when variables are accepted', () => {
        const result = getVariableValue('User asked: {{question}}', [], 'What is AI?', [], true)
        expect(result).toBe('User asked: What is AI?')
    })

    it('should escape special characters when resolving {{question}}', () => {
        const result = getVariableValue('{{question}}', [], 'line one\nline two', [], true)
        expect(result).toBe('line oneFLOWISE_NEWLINEline two')
    })

    it('should resolve {{chat_history}} when variables are accepted', () => {
        const result = getVariableValue('{{chat_history}}', [], 'question', chatHistory, true)
        expect(result).toBe('Human: What is Flowise?FLOWISE_NEWLINEAssistant: Flowise is a low-code LLM apps builder.')
    })

    it('should resolve a node output reference to the node instance', () => {
        const executedNodes = [makeExecutedNode('llmChain_0', 'chain output value')]
        const result = getVariableValue('{{llmChain_0.data.instance}}', executedNodes, 'question', [])
        expect(result).toBe('chain output value')
    })

    it('should replace multiple variables in the same string', () => {
        const executedNodes = [makeExecutedNode('llmChain_0', 'first'), makeExecutedNode('llmChain_1', 'second')]
        const result = getVariableValue(
            '{{llmChain_0.data.instance}} and {{llmChain_1.data.instance}}',
            executedNodes,
            'question',
            [],
            true
        )
        expect(result).toBe('first and second')
    })
})

describe('resolveVariables', () => {
    it('should resolve variables inside node inputs', () => {
        const executedNodes = [makeExecutedNode('llmChain_0', 'resolved value')]
        const nodeData = {
            id: 'llmChain_1',
            label: 'LLM Chain',
            name: 'llmChain',
            type: 'llmChain',
            category: 'Chains',
            inputs: { prompt: '{{llmChain_0.data.instance}}' },
            inputParams: []
        } as unknown as INodeData

        const resolved = resolveVariables(nodeData, executedNodes, 'question', [])
        expect(resolved.inputs?.prompt).toBe('resolved value')
    })

    it('should not mutate the original node data', () => {
        const executedNodes = [makeExecutedNode('llmChain_0', 'resolved value')]
        const nodeData = {
            id: 'llmChain_1',
            label: 'LLM Chain',
            name: 'llmChain',
            type: 'llmChain',
            category: 'Chains',
            inputs: { prompt: '{{llmChain_0.data.instance}}' },
            inputParams: []
        } as unknown as INodeData

        resolveVariables(nodeData, executedNodes, 'question', [])
        expect(nodeData.inputs?.prompt).toBe('{{llmChain_0.data.instance}}')
    })

    it('should resolve each element of array inputs', () => {
        const executedNodes = [makeExecutedNode('tool_0', 'tool instance')]
        const nodeData = {
            id: 'agent_0',
            label: 'Agent',
            name: 'agent',
            type: 'agent',
            category: 'Agents',
            inputs: { tools: ['{{tool_0.data.instance}}'] },
            inputParams: []
        } as unknown as INodeData

        const resolved = resolveVariables(nodeData, executedNodes, 'question', [])
        expect(resolved.inputs?.tools).toEqual(['tool instance'])
    })
})

describe('replaceInputsWithConfig', () => {
    const makeNodeData = (inputs: Record<string, any>): INodeData => {
        return {
            id: 'llmChain_0',
            label: 'LLM Chain',
            name: 'llmChain',
            type: 'llmChain',
            category: 'Chains',
            inputs,
            inputParams: []
        } as unknown as INodeData
    }

    it('should override an existing input value', () => {
        const result = replaceInputsWithConfig(makeNodeData({ temperature: 0.5 }), { temperature: 0.9 })
        expect(result.inputs?.temperature).toBe(0.9)
    })

    it('should apply a node-scoped override only to the matching node id', () => {
        const result = replaceInputsWithConfig(makeNodeData({ systemMessage: 'default' }), {
            systemMessage: { llmChain_0: 'overridden' }
        })
        expect(result.inputs?.systemMessage).toBe('overridden')
    })

    it('should skip a node-scoped override targeting a sibling node of the same type', () => {
        const result = replaceInputsWithConfig(makeNodeData({ systemMessage: 'default' }), {
            systemMessage: { llmChain_1: 'other node' }
        })
        expect(result.inputs?.systemMessage).toBe('default')
    })

    it('should merge object overrides into JSON string inputs', () => {
        const result = replaceInputsWithConfig(makeNodeData({ promptValues: '{"existing":"value"}' }), {
            promptValues: { added: 'newValue' }
        })
        expect(result.inputs?.promptValues).toEqual({ existing: 'value', added: 'newValue' })
    })

    it('should convert boolean-like strings to booleans', () => {
        const result = replaceInputsWithConfig(makeNodeData({ returnSourceDocuments: false }), { returnSourceDocuments: 'true' })
        expect(result.inputs?.returnSourceDocuments).toBe(true)
    })
})

describe('isSameOverrideConfig', () => {
    it('should return true for internal calls without existing override config', () => {
        expect(isSameOverrideConfig(true)).toBe(true)
    })

    it('should return false for internal calls with existing override config', () => {
        expect(isSameOverrideConfig(true, { sessionId: 'abc' })).toBe(false)
    })

    it('should return true when both override configs are equal', () => {
        expect(isSameOverrideConfig(false, { temperature: 1 }, { temperature: 1 })).toBe(true)
    })

    it('should return false when override configs differ', () => {
        expect(isSameOverrideConfig(false, { temperature: 1 }, { temperature: 2 })).toBe(false)
    })

    it('should return true when neither config is provided', () => {
        expect(isSameOverrideConfig(false)).toBe(true)
    })

    it('should return false when only one config is provided', () => {
        expect(isSameOverrideConfig(false, { temperature: 1 }, undefined)).toBe(false)
    })
})
