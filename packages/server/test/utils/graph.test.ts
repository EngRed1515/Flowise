import { constructGraphs, getStartingNodes, getEndingNodes, getAllConnectedNodes } from '../../src/utils'
import { IReactFlowNode, IReactFlowEdge } from '../../src/Interface'
import { InternalFlowiseError } from '../../src/errors/internalFlowiseError'

const makeNode = (id: string, category: string, outputs: Record<string, any> = {}): IReactFlowNode => {
    return {
        id,
        position: { x: 0, y: 0 },
        type: 'customNode',
        data: {
            id,
            label: id,
            name: id.split('_')[0],
            type: id.split('_')[0],
            category,
            outputs,
            inputs: {},
            inputParams: []
        }
    } as unknown as IReactFlowNode
}

const makeEdge = (source: string, target: string): IReactFlowEdge => {
    return {
        source,
        target,
        sourceHandle: `${source}-output`,
        targetHandle: `${target}-input`,
        type: 'buttonedge',
        id: `${source}-${target}`
    } as IReactFlowEdge
}

/**
 * Simple LLM chain flow:
 *   chatOpenAI_0 ──┐
 *                  ├──> llmChain_0
 *   promptTemplate_0 ──┘
 */
const nodes = [makeNode('chatOpenAI_0', 'Chat Models'), makeNode('promptTemplate_0', 'Prompts'), makeNode('llmChain_0', 'Chains')]
const edges = [makeEdge('chatOpenAI_0', 'llmChain_0'), makeEdge('promptTemplate_0', 'llmChain_0')]

describe('constructGraphs', () => {
    it('should construct a directed graph and node dependencies', () => {
        const { graph, nodeDependencies } = constructGraphs(nodes, edges)
        expect(graph).toEqual({
            chatOpenAI_0: ['llmChain_0'],
            promptTemplate_0: ['llmChain_0'],
            llmChain_0: []
        })
        expect(nodeDependencies).toEqual({
            chatOpenAI_0: 0,
            promptTemplate_0: 0,
            llmChain_0: 2
        })
    })

    it('should construct a non-directed graph with edges in both directions', () => {
        const { graph } = constructGraphs(nodes, edges, { isNonDirected: true })
        expect(graph['llmChain_0']).toEqual(expect.arrayContaining(['chatOpenAI_0', 'promptTemplate_0']))
        expect(graph['chatOpenAI_0']).toEqual(['llmChain_0'])
        expect(graph['promptTemplate_0']).toEqual(['llmChain_0'])
    })

    it('should construct a reversed graph', () => {
        const { graph } = constructGraphs(nodes, edges, { isReversed: true })
        expect(graph['llmChain_0']).toEqual(expect.arrayContaining(['chatOpenAI_0', 'promptTemplate_0']))
        expect(graph['chatOpenAI_0']).toEqual([])
        expect(graph['promptTemplate_0']).toEqual([])
    })

    it('should handle a flow with no edges', () => {
        const { graph, nodeDependencies } = constructGraphs([makeNode('toolAgent_0', 'Agents')], [])
        expect(graph).toEqual({ toolAgent_0: [] })
        expect(nodeDependencies).toEqual({ toolAgent_0: 0 })
    })
})

describe('getStartingNodes', () => {
    it('should find starting nodes and depth queue from the reversed graph', () => {
        const { graph } = constructGraphs(nodes, edges, { isReversed: true })
        const { startingNodeIds, depthQueue } = getStartingNodes(graph, 'llmChain_0')
        expect(startingNodeIds.sort()).toEqual(['chatOpenAI_0', 'promptTemplate_0'])
        expect(depthQueue).toEqual({
            chatOpenAI_0: 0,
            promptTemplate_0: 0,
            llmChain_0: 1
        })
    })

    it('should handle a multi-level chain', () => {
        // promptTemplate_0 -> llmChain_0 -> promptTemplate_1 -> llmChain_1
        const chainNodes = [
            makeNode('promptTemplate_0', 'Prompts'),
            makeNode('llmChain_0', 'Chains'),
            makeNode('promptTemplate_1', 'Prompts'),
            makeNode('llmChain_1', 'Chains')
        ]
        const chainEdges = [
            makeEdge('promptTemplate_0', 'llmChain_0'),
            makeEdge('llmChain_0', 'promptTemplate_1'),
            makeEdge('promptTemplate_1', 'llmChain_1')
        ]
        const { graph } = constructGraphs(chainNodes, chainEdges, { isReversed: true })
        const { startingNodeIds, depthQueue } = getStartingNodes(graph, 'llmChain_1')
        expect(startingNodeIds).toEqual(['promptTemplate_0'])
        expect(depthQueue['promptTemplate_0']).toBe(0)
        expect(depthQueue['llmChain_1']).toBe(3)
    })
})

describe('getAllConnectedNodes', () => {
    it('should return all nodes reachable from the starting node in a non-directed graph', () => {
        const { graph } = constructGraphs(nodes, edges, { isNonDirected: true })
        const connected = getAllConnectedNodes(graph, 'chatOpenAI_0')
        expect(connected.sort()).toEqual(['chatOpenAI_0', 'llmChain_0', 'promptTemplate_0'])
    })

    it('should not include disconnected nodes', () => {
        const allNodes = [...nodes, makeNode('calculator_0', 'Tools')]
        const { graph } = constructGraphs(allNodes, edges, { isNonDirected: true })
        const connected = getAllConnectedNodes(graph, 'chatOpenAI_0')
        expect(connected).not.toContain('calculator_0')
    })
})

describe('getEndingNodes', () => {
    it('should return the ending node of a valid flow', () => {
        const { graph, nodeDependencies } = constructGraphs(nodes, edges)
        const endingNodes = getEndingNodes(nodeDependencies, graph, nodes)
        expect(endingNodes.map((node) => node.id)).toEqual(['llmChain_0'])
    })

    it('should return a single node flow as its own ending node', () => {
        const singleNode = [makeNode('conversationChain_0', 'Chains')]
        const { graph, nodeDependencies } = constructGraphs(singleNode, [])
        const endingNodes = getEndingNodes(nodeDependencies, graph, singleNode)
        expect(endingNodes.map((node) => node.id)).toEqual(['conversationChain_0'])
    })

    it('should accept an explicit EndingNode output even outside ending categories', () => {
        const flowNodes = [makeNode('chatOpenAI_0', 'Chat Models'), makeNode('seqEnd_0', 'Sequential Agents', { output: 'EndingNode' })]
        const flowEdges = [makeEdge('chatOpenAI_0', 'seqEnd_0')]
        const { graph, nodeDependencies } = constructGraphs(flowNodes, flowEdges)
        const endingNodes = getEndingNodes(nodeDependencies, graph, flowNodes)
        expect(endingNodes.map((node) => node.id)).toEqual(['seqEnd_0'])
    })

    it('should throw when the ending node category is not allowed', () => {
        const flowNodes = [makeNode('chatOpenAI_0', 'Chat Models'), makeNode('promptTemplate_0', 'Prompts')]
        const flowEdges = [makeEdge('chatOpenAI_0', 'promptTemplate_0')]
        const { graph, nodeDependencies } = constructGraphs(flowNodes, flowEdges)
        expect(() => getEndingNodes(nodeDependencies, graph, flowNodes)).toThrow(InternalFlowiseError)
        expect(() => getEndingNodes(nodeDependencies, graph, flowNodes)).toThrow('Ending node must be either a Chain or Agent or Engine')
    })

    it('should throw when there is no ending node', () => {
        const flowNodes = [makeNode('llmChain_0', 'Chains'), makeNode('llmChain_1', 'Chains')]
        // cycle: llmChain_0 -> llmChain_1 -> llmChain_0
        const flowEdges = [makeEdge('llmChain_0', 'llmChain_1'), makeEdge('llmChain_1', 'llmChain_0')]
        const { graph, nodeDependencies } = constructGraphs(flowNodes, flowEdges)
        expect(() => getEndingNodes(nodeDependencies, graph, flowNodes)).toThrow('Ending nodes not found')
    })
})
