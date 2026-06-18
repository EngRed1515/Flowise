import { useState } from 'react'
import api from '../api/client.js'
import { PageHeader, Card, ErrorBox, Badge, Json, Empty } from '../components/ui.jsx'

const NUMERIC = new Set(['employment', 'turnover_qar', 'total_assets_qar', 'sales', 'production_costs'])
const BOOL = new Set(['is_nonprofit', 'is_financial', 'has_premises', 'has_employees', 'has_autonomy'])

const emptyEdge = () => ({
  owner_id: '',
  owner_name: '',
  owner_is_government: false,
  owner_is_resident: true,
  owner_country: '',
  ownership_pct: '',
  voting_pct: '',
  control_indicator: '',
  is_ultimate: false,
})

const DIMENSIONS = [
  ['sector_code', 'Sector'],
  ['public_private', 'Public / Private'],
  ['control_flag', 'Control'],
  ['market_status', 'Market status'],
  ['size_class', 'Size class'],
  ['fdi_flag', 'FDI flag'],
  ['special_entity_flag', 'Special entity'],
]

export default function Simulate() {
  const [form, setForm] = useState({
    legal_name_en: 'Sandbox Enterprise',
    legal_form_code: '',
    residence: '',
    isic_class: '',
    employment: '',
    turnover_qar: '',
    total_assets_qar: '',
    sales: '',
    production_costs: '',
    is_nonprofit: false,
    is_financial: false,
    has_premises: true,
    has_employees: true,
    has_autonomy: true,
    jurisdiction: '',
  })
  const [edges, setEdges] = useState([])
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  function set(k, v) {
    setForm((f) => ({ ...f, [k]: v }))
  }
  function setEdge(i, k, v) {
    setEdges((arr) => arr.map((e, idx) => (idx === i ? { ...e, [k]: v } : e)))
  }

  function buildEnterprise() {
    const out = {}
    Object.entries(form).forEach(([k, v]) => {
      if (BOOL.has(k)) out[k] = !!v
      else if (v === '' || v == null) {
        /* skip */
      } else if (NUMERIC.has(k)) {
        const n = Number(v)
        if (!Number.isNaN(n)) out[k] = n
      } else out[k] = v
    })
    return out
  }

  function buildEdges() {
    return edges.map((e) => ({
      owner_id: e.owner_id || null,
      owner_name: e.owner_name || null,
      owner_is_government: !!e.owner_is_government,
      owner_is_resident: !!e.owner_is_resident,
      owner_country: e.owner_country || null,
      ownership_pct: e.ownership_pct === '' ? null : Number(e.ownership_pct),
      voting_pct: e.voting_pct === '' ? null : Number(e.voting_pct),
      control_indicator: e.control_indicator || null,
      is_ultimate: !!e.is_ultimate,
    }))
  }

  async function run(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    setResult(null)
    try {
      const payload = { ...buildEnterprise(), ownership: buildEdges() }
      const r = await api.simulate(payload)
      setResult(r)
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  const res = result?.result || {}
  const conf =
    result?.confidence == null
      ? null
      : (Number(result.confidence) <= 1 ? result.confidence * 100 : result.confidence).toFixed(1)

  return (
    <div>
      <PageHeader
        title="Simulation Sandbox"
        subtitle="Test hypothetical classifications without persisting any data"
      />
      <div className="sandbox-banner">SANDBOX — Results are never persisted to the register.</div>

      <form onSubmit={run}>
        <Card title="Hypothetical Enterprise">
          <div className="form-grid">
            <label className="field">
              <span>Legal name (EN)</span>
              <input value={form.legal_name_en} onChange={(e) => set('legal_name_en', e.target.value)} />
            </label>
            <label className="field">
              <span>Legal form code</span>
              <input value={form.legal_form_code} onChange={(e) => set('legal_form_code', e.target.value)} />
            </label>
            <label className="field">
              <span>Residence</span>
              <input value={form.residence} onChange={(e) => set('residence', e.target.value)} />
            </label>
            <label className="field">
              <span>ISIC class</span>
              <input value={form.isic_class} onChange={(e) => set('isic_class', e.target.value)} />
            </label>
            <label className="field">
              <span>Employment</span>
              <input type="number" value={form.employment} onChange={(e) => set('employment', e.target.value)} />
            </label>
            <label className="field">
              <span>Turnover (QAR)</span>
              <input type="number" value={form.turnover_qar} onChange={(e) => set('turnover_qar', e.target.value)} />
            </label>
            <label className="field">
              <span>Total assets (QAR)</span>
              <input type="number" value={form.total_assets_qar} onChange={(e) => set('total_assets_qar', e.target.value)} />
            </label>
            <label className="field">
              <span>Jurisdiction</span>
              <input value={form.jurisdiction} onChange={(e) => set('jurisdiction', e.target.value)} />
            </label>
          </div>
          <div className="checkbox-row">
            {[...BOOL].map((b) => (
              <label key={b} className="checkbox">
                <input type="checkbox" checked={!!form[b]} onChange={(e) => set(b, e.target.checked)} />
                <span>{b.replace(/_/g, ' ')}</span>
              </label>
            ))}
          </div>
        </Card>

        <Card
          title={`Ownership Edges (${edges.length})`}
          actions={
            <button type="button" className="btn btn-sm" onClick={() => setEdges([...edges, emptyEdge()])}>
              + Add Edge
            </button>
          }
        >
          {edges.length === 0 ? (
            <Empty label="No ownership edges. Add edges to test control / FDI logic." />
          ) : (
            edges.map((edge, i) => (
              <div className="edge-row" key={i}>
                <input placeholder="owner_id" value={edge.owner_id} onChange={(e) => setEdge(i, 'owner_id', e.target.value)} />
                <input placeholder="owner name" value={edge.owner_name} onChange={(e) => setEdge(i, 'owner_name', e.target.value)} />
                <input placeholder="country" value={edge.owner_country} onChange={(e) => setEdge(i, 'owner_country', e.target.value)} />
                <input type="number" placeholder="own %" value={edge.ownership_pct} onChange={(e) => setEdge(i, 'ownership_pct', e.target.value)} />
                <input type="number" placeholder="vote %" value={edge.voting_pct} onChange={(e) => setEdge(i, 'voting_pct', e.target.value)} />
                <label className="checkbox tight">
                  <input type="checkbox" checked={edge.owner_is_government} onChange={(e) => setEdge(i, 'owner_is_government', e.target.checked)} />
                  <span>Gov</span>
                </label>
                <label className="checkbox tight">
                  <input type="checkbox" checked={edge.owner_is_resident} onChange={(e) => setEdge(i, 'owner_is_resident', e.target.checked)} />
                  <span>Res</span>
                </label>
                <label className="checkbox tight">
                  <input type="checkbox" checked={edge.is_ultimate} onChange={(e) => setEdge(i, 'is_ultimate', e.target.checked)} />
                  <span>Ult</span>
                </label>
                <button type="button" className="btn btn-sm btn-ghost" onClick={() => setEdges(edges.filter((_, idx) => idx !== i))}>
                  ✕
                </button>
              </div>
            ))
          )}
        </Card>

        <ErrorBox error={error} />
        <button className="btn btn-primary" disabled={busy}>
          {busy ? 'Simulating…' : 'Run Simulation'}
        </button>
      </form>

      {result && (
        <>
          <Card title="Simulation Result" className="result-card">
            <div className="dim-grid">
              {DIMENSIONS.map(([k, label]) => (
                <div className="dim-card" key={k}>
                  <div className="dim-label">{label}</div>
                  <div className="dim-value">{String(res[k] ?? '—')}</div>
                </div>
              ))}
            </div>
            <div className="conf-row">
              <span>Confidence</span>
              <div className="gauge-track small">
                <div className="gauge-fill gauge-good" style={{ width: `${conf || 0}%` }} />
              </div>
              <strong>{conf != null ? `${conf}%` : '—'}</strong>
              <Badge tone="warn">SANDBOX</Badge>
            </div>
          </Card>
          {result.facts && (
            <Card title="Derived Facts">
              <Json value={result.facts} />
            </Card>
          )}
          {result.trace && (
            <Card title="Trace">
              <Json value={result.trace} />
            </Card>
          )}
        </>
      )}
    </div>
  )
}
