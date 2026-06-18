import { useState, useMemo } from 'react'
import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import {
  PageHeader,
  Card,
  Loading,
  ErrorBox,
  Empty,
  Badge,
  Json,
} from '../components/ui.jsx'

function RuleTester({ rule }) {
  const [text, setText] = useState('{\n  \n}')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  async function run() {
    setBusy(true)
    setError(null)
    setResult(null)
    let facts
    try {
      facts = JSON.parse(text)
    } catch {
      setError(new Error('Facts must be valid JSON.'))
      setBusy(false)
      return
    }
    try {
      const r = await api.testRule(rule.rule_id, facts)
      setResult(r)
    } catch (e) {
      setError(e)
    } finally {
      setBusy(false)
    }
  }

  function prefill() {
    const inputs = rule.inputs_required || []
    const obj = {}
    ;(Array.isArray(inputs) ? inputs : []).forEach((k) => (obj[k] = ''))
    setText(JSON.stringify(obj, null, 2))
  }

  return (
    <div className="rule-tester">
      <h4>Rule Tester</h4>
      <p className="muted small">
        Paste a facts JSON object and run it against <span className="mono">{rule.rule_id}</span>.
      </p>
      <div className="tester-actions">
        <button className="btn btn-sm btn-ghost" type="button" onClick={prefill}>
          Prefill from inputs_required
        </button>
      </div>
      <textarea
        className="json-input"
        rows={8}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button className="btn btn-primary btn-sm" onClick={run} disabled={busy}>
        {busy ? 'Testing…' : 'Run Test'}
      </button>
      <ErrorBox error={error} />
      {result && (
        <div className="tester-result">
          <div className="tester-verdict">
            <Badge tone={result.matched ? 'good' : 'neutral'}>
              {result.matched ? 'MATCHED' : 'NO MATCH'}
            </Badge>
            {result.output != null && (
              <span>
                Output: <strong>{String(result.output)}</strong>
              </span>
            )}
          </div>
          {result.rationale && <p className="rationale">{result.rationale}</p>}
          {result.standard_ref && <div className="standard-ref">Standard: {result.standard_ref}</div>}
        </div>
      )}
    </div>
  )
}

function RuleDetail({ rule }) {
  return (
    <div className="rule-detail">
      <div className="rule-detail-head">
        <h3>{rule.name}</h3>
        <div className="badge-row">
          <Badge tone="accent">{rule.test_code}</Badge>
          {rule.domain && <Badge>{rule.domain}</Badge>}
          {rule.approval_status && <Badge tone="warn">{rule.approval_status}</Badge>}
          {rule.is_active ? <Badge tone="good">Active</Badge> : <Badge tone="bad">Inactive</Badge>}
          {rule.version && <Badge>v{rule.version}</Badge>}
        </div>
      </div>
      {rule.description && <p>{rule.description}</p>}
      <div className="kv-grid">
        <div className="kv">
          <span className="kv-label">Rule ID</span>
          <span className="kv-value mono">{rule.rule_id}</span>
        </div>
        <div className="kv">
          <span className="kv-label">Output</span>
          <span className="kv-value">{String(rule.output ?? '—')}</span>
        </div>
        <div className="kv">
          <span className="kv-label">Priority</span>
          <span className="kv-value">{rule.priority ?? '—'}</span>
        </div>
        <div className="kv">
          <span className="kv-label">Confidence</span>
          <span className="kv-value">{rule.confidence ?? '—'}</span>
        </div>
        <div className="kv">
          <span className="kv-label">Standard ref</span>
          <span className="kv-value">{rule.standard_ref || '—'}</span>
        </div>
      </div>
      {rule.rationale && (
        <>
          <h4 className="section-h">Rationale</h4>
          <p className="rationale">{rule.rationale}</p>
        </>
      )}
      {rule.inputs_required && (
        <>
          <h4 className="section-h">Inputs Required</h4>
          <Json value={rule.inputs_required} />
        </>
      )}
      <h4 className="section-h">Logic</h4>
      <Json value={rule.logic} />
      <RuleTester rule={rule} />
    </div>
  )
}

export default function Rules() {
  const [q, setQ] = useState('')
  const [selected, setSelected] = useState(null)
  const { data, error, loading, reload } = useAsync(() => api.rules(), [])

  const rules = Array.isArray(data) ? data : data?.items || []

  const grouped = useMemo(() => {
    const filtered = rules.filter((r) => {
      if (!q) return true
      const hay = `${r.rule_id} ${r.name} ${r.description} ${r.test_code} ${r.domain}`.toLowerCase()
      return hay.includes(q.toLowerCase())
    })
    const g = {}
    filtered.forEach((r) => {
      const key = r.test_code || 'OTHER'
      ;(g[key] = g[key] || []).push(r)
    })
    return g
  }, [rules, q])

  return (
    <div>
      <PageHeader
        title="Rules Repository"
        subtitle="Classification rule library grouped by test, with an interactive tester"
      />
      {loading ? (
        <Loading />
      ) : error ? (
        <ErrorBox error={error} onRetry={reload} />
      ) : (
        <div className="split-layout">
          <div className="split-list">
            <Card title="Rules">
              <input
                className="search-input"
                placeholder="Search rules…"
                value={q}
                onChange={(e) => setQ(e.target.value)}
              />
              {Object.keys(grouped).length === 0 ? (
                <Empty />
              ) : (
                Object.entries(grouped).map(([test, list]) => (
                  <div key={test} className="rule-group">
                    <div className="rule-group-head">{test}</div>
                    {list.map((r) => (
                      <button
                        key={r.rule_id}
                        className={'rule-item' + (selected?.rule_id === r.rule_id ? ' active' : '')}
                        onClick={() => setSelected(r)}
                      >
                        <span className="rule-item-name">{r.name}</span>
                        <span className="rule-item-id mono">{r.rule_id}</span>
                      </button>
                    ))}
                  </div>
                ))
              )}
            </Card>
          </div>
          <div className="split-detail">
            <Card>
              {selected ? (
                <RuleDetail rule={selected} />
              ) : (
                <Empty label="Select a rule to view its logic and test it." />
              )}
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
