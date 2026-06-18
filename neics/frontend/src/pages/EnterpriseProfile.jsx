import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import { useAuth, hasRole } from '../auth.jsx'
import {
  PageHeader,
  Card,
  Loading,
  ErrorBox,
  Empty,
  Badge,
  Gauge,
  Json,
} from '../components/ui.jsx'

const TABS = [
  'Master Data',
  'Ownership',
  'Classification',
  'Explainability',
  'History',
  'Quality',
  'Audit',
]

function Field({ label, value }) {
  return (
    <div className="kv">
      <span className="kv-label">{label}</span>
      <span className="kv-value">{value === 0 ? '0' : value || '—'}</span>
    </div>
  )
}

// ---------- Master Data ----------
function MasterData({ e }) {
  if (!e) return <Empty />
  return (
    <div className="kv-grid">
      <Field label="Enterprise ID" value={e.enterprise_id} />
      <Field label="Legal name (EN)" value={e.legal_name_en} />
      <Field label="Legal name (AR)" value={e.legal_name_ar} />
      <Field label="LEI" value={e.lei} />
      <Field label="Legal form" value={e.legal_form_code} />
      <Field label="Residence" value={e.residence} />
      <Field label="ISIC class" value={e.isic_class} />
      <Field label="Sector" value={e.sector_code} />
      <Field label="Public / Private" value={e.public_private} />
      <Field label="Control flag" value={e.control_flag} />
      <Field label="Market status" value={e.market_status} />
      <Field label="Size class" value={e.size_class} />
      <Field label="FDI flag" value={String(e.fdi_flag ?? '')} />
      <Field label="Special entity" value={String(e.special_entity_flag ?? '')} />
      <Field label="Group ID" value={e.group_id} />
      <Field label="Employment" value={e.employment} />
      <Field label="Turnover (QAR)" value={e.turnover_qar} />
      <Field label="Jurisdiction" value={e.jurisdiction} />
      <Field label="Is financial" value={String(e.is_financial ?? '')} />
      <Field label="Quality flag" value={e.quality_flag} />
      <Field label="Quality score" value={e.quality_score} />
      <Field label="Classification version" value={e.classification_version} />
      <Field label="Classification date" value={e.classification_date} />
      <Field label="Birth date" value={e.birth_date} />
    </div>
  )
}

// ---------- Ownership ----------
function OwnershipTree({ chain }) {
  if (!chain || !chain.length) return null
  return (
    <ul className="own-tree">
      {chain.map((node, i) => (
        <li key={i} className="own-node">
          <div className="own-box">
            <div className="own-name">{node.owner_name || node.name || node.owner_id || `Level ${i + 1}`}</div>
            <div className="own-meta">
              {node.ownership_pct != null && <span>{node.ownership_pct}% owned</span>}
              {node.owner_country && <span>· {node.owner_country}</span>}
              {node.owner_is_government && <Badge tone="warn">Government</Badge>}
            </div>
          </div>
        </li>
      ))}
    </ul>
  )
}

function Ownership({ id, ownership }) {
  const [form, setForm] = useState({
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
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const [ok, setOk] = useState(false)

  const o = ownership || {}
  const facts = o.facts || {}
  const uci = o.uci || {}
  const edges = o.edges || []

  async function addOwner(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    setOk(false)
    try {
      const payload = {
        owner_id: form.owner_id,
        owner_name: form.owner_name,
        owner_is_government: !!form.owner_is_government,
        owner_is_resident: !!form.owner_is_resident,
        owner_country: form.owner_country || null,
        ownership_pct: form.ownership_pct === '' ? null : Number(form.ownership_pct),
        voting_pct: form.voting_pct === '' ? null : Number(form.voting_pct),
        control_indicator: form.control_indicator || null,
        is_ultimate: !!form.is_ultimate,
      }
      await api.addOwnership(id, payload)
      setOk(true)
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <div className="grid-2">
        <Card title="Ownership Facts" className="flush">
          <div className="kv-grid">
            <Field label="Government ownership %" value={facts.government_ownership_pct} />
            <Field label="Foreign ownership %" value={facts.foreign_ownership_pct} />
            <Field label="Government control" value={String(facts.government_control ?? '')} />
            <Field
              label="Representative control"
              value={String(facts.representative_control_flag ?? '')}
            />
          </div>
        </Card>
        <Card title="Ultimate Controlling Institutional Unit (UCI)" className="flush">
          {uci && (uci.uci_id || uci.uci_name) ? (
            <div className="kv-grid">
              <Field label="UCI ID" value={uci.uci_id} />
              <Field label="UCI name" value={uci.uci_name} />
              <Field label="Is government" value={String(uci.is_government ?? '')} />
              <Field label="Is resident" value={String(uci.is_resident ?? '')} />
              <Field label="Country" value={uci.country} />
            </div>
          ) : (
            <Empty label="No UCI resolved." />
          )}
        </Card>
      </div>

      {o.chain && o.chain.length > 0 && (
        <Card title="Ownership Chain">
          <OwnershipTree chain={o.chain} />
        </Card>
      )}

      <Card title="Ownership Edges">
        {edges.length ? (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Owner</th>
                  <th>Country</th>
                  <th>Gov</th>
                  <th>Resident</th>
                  <th>Ownership %</th>
                  <th>Voting %</th>
                  <th>Control</th>
                  <th>Ultimate</th>
                </tr>
              </thead>
              <tbody>
                {edges.map((g, i) => (
                  <tr key={i}>
                    <td>
                      {g.owner_name || g.owner_id || '—'}
                      {g.owner_id && g.owner_name ? <div className="cell-secondary mono">{g.owner_id}</div> : null}
                    </td>
                    <td>{g.owner_country || '—'}</td>
                    <td>{g.owner_is_government ? 'Yes' : 'No'}</td>
                    <td>{g.owner_is_resident ? 'Yes' : 'No'}</td>
                    <td>{g.ownership_pct ?? '—'}</td>
                    <td>{g.voting_pct ?? '—'}</td>
                    <td>{g.control_indicator || '—'}</td>
                    <td>{g.is_ultimate ? 'Yes' : 'No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty label="No ownership edges recorded." />
        )}
      </Card>

      <Card title="Add Ownership Edge">
        <form className="form-grid" onSubmit={addOwner}>
          <label className="field">
            <span>Owner ID</span>
            <input value={form.owner_id} onChange={(e) => setForm({ ...form, owner_id: e.target.value })} />
          </label>
          <label className="field">
            <span>Owner name</span>
            <input value={form.owner_name} onChange={(e) => setForm({ ...form, owner_name: e.target.value })} />
          </label>
          <label className="field">
            <span>Owner country</span>
            <input value={form.owner_country} onChange={(e) => setForm({ ...form, owner_country: e.target.value })} />
          </label>
          <label className="field">
            <span>Ownership %</span>
            <input type="number" value={form.ownership_pct} onChange={(e) => setForm({ ...form, ownership_pct: e.target.value })} />
          </label>
          <label className="field">
            <span>Voting %</span>
            <input type="number" value={form.voting_pct} onChange={(e) => setForm({ ...form, voting_pct: e.target.value })} />
          </label>
          <label className="field">
            <span>Control indicator</span>
            <input value={form.control_indicator} onChange={(e) => setForm({ ...form, control_indicator: e.target.value })} />
          </label>
          <div className="checkbox-row full">
            <label className="checkbox">
              <input type="checkbox" checked={form.owner_is_government} onChange={(e) => setForm({ ...form, owner_is_government: e.target.checked })} />
              <span>Owner is government</span>
            </label>
            <label className="checkbox">
              <input type="checkbox" checked={form.owner_is_resident} onChange={(e) => setForm({ ...form, owner_is_resident: e.target.checked })} />
              <span>Owner is resident</span>
            </label>
            <label className="checkbox">
              <input type="checkbox" checked={form.is_ultimate} onChange={(e) => setForm({ ...form, is_ultimate: e.target.checked })} />
              <span>Is ultimate</span>
            </label>
          </div>
          <div className="full">
            <ErrorBox error={error} />
            {ok && <div className="success-box">Ownership edge added. Refresh the page to see the recomputed chain.</div>}
            <button className="btn btn-primary" disabled={busy}>
              {busy ? 'Adding…' : 'Add Edge'}
            </button>
          </div>
        </form>
      </Card>
    </div>
  )
}

const DIMENSIONS = [
  ['sector_code', 'Sector'],
  ['public_private', 'Public / Private'],
  ['control_flag', 'Control'],
  ['market_status', 'Market status'],
  ['size_class', 'Size class'],
  ['fdi_flag', 'FDI flag'],
  ['special_entity_flag', 'Special entity'],
]

// ---------- Classification ----------
function Classification({ id, classification, onReclassify }) {
  const { user } = useAuth()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const [overrideOpen, setOverrideOpen] = useState(false)
  const [ov, setOv] = useState({ field: 'sector_code', value: '', reason: '' })
  const [ovBusy, setOvBusy] = useState(false)
  const [ovError, setOvError] = useState(null)
  const canOverride = hasRole(user, 'reviewer', 'admin')

  const c = classification || {}

  async function reclassify() {
    setBusy(true)
    setError(null)
    try {
      const r = await api.classify(id)
      onReclassify && onReclassify(r)
    } catch (e) {
      setError(e)
    } finally {
      setBusy(false)
    }
  }

  async function submitOverride(e) {
    e.preventDefault()
    setOvBusy(true)
    setOvError(null)
    try {
      const r = await api.override(id, ov)
      setOverrideOpen(false)
      onReclassify && onReclassify(r)
    } catch (err) {
      setOvError(err)
    } finally {
      setOvBusy(false)
    }
  }

  const conf =
    c.confidence == null
      ? null
      : (Number(c.confidence) <= 1 ? c.confidence * 100 : c.confidence).toFixed(1)

  return (
    <div>
      <Card
        title="Current Classification"
        actions={
          <>
            <button className="btn btn-primary btn-sm" onClick={reclassify} disabled={busy}>
              {busy ? 'Classifying…' : 'Re-classify'}
            </button>
            {canOverride && (
              <button className="btn btn-sm" onClick={() => setOverrideOpen((s) => !s)}>
                Override
              </button>
            )}
          </>
        }
      >
        <ErrorBox error={error} />
        {Object.keys(c).length === 0 ? (
          <Empty label="Not yet classified. Click Re-classify." />
        ) : (
          <>
            <div className="dim-grid">
              {DIMENSIONS.map(([k, label]) => (
                <div className="dim-card" key={k}>
                  <div className="dim-label">{label}</div>
                  <div className="dim-value">{String(c[k] ?? '—')}</div>
                </div>
              ))}
            </div>
            <div className="conf-row">
              <span>Confidence</span>
              <div className="gauge-track small">
                <div className="gauge-fill gauge-good" style={{ width: `${conf || 0}%` }} />
              </div>
              <strong>{conf != null ? `${conf}%` : '—'}</strong>
              {c.version != null && <Badge>v{c.version}</Badge>}
            </div>
          </>
        )}

        {overrideOpen && canOverride && (
          <form className="override-form" onSubmit={submitOverride}>
            <h4>Manual Override (Reviewer / Admin)</h4>
            <div className="form-grid">
              <label className="field">
                <span>Dimension</span>
                <select value={ov.field} onChange={(e) => setOv({ ...ov, field: e.target.value })}>
                  {DIMENSIONS.map(([k, label]) => (
                    <option key={k} value={k}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
              <label className="field">
                <span>New value</span>
                <input value={ov.value} onChange={(e) => setOv({ ...ov, value: e.target.value })} />
              </label>
              <label className="field full">
                <span>Reason</span>
                <textarea
                  value={ov.reason}
                  onChange={(e) => setOv({ ...ov, reason: e.target.value })}
                  required
                />
              </label>
            </div>
            <ErrorBox error={ovError} />
            <button className="btn btn-primary" disabled={ovBusy}>
              {ovBusy ? 'Submitting…' : 'Submit Override'}
            </button>
          </form>
        )}
      </Card>

      {c.trace && c.trace.length > 0 && (
        <Card title="Classification Trace">
          <Json value={c.trace} />
        </Card>
      )}
    </div>
  )
}

// ---------- Explainability ----------
function Explainability({ explain }) {
  if (!explain) return <Empty label="No explanation available." />
  const rules = explain.applied_rules || []
  return (
    <div>
      <Card title="Explainability — Applied Rules" className="explain-card">
        <div className="explain-meta">
          {explain.methodology_version && (
            <Badge>Methodology {explain.methodology_version}</Badge>
          )}
          {explain.confidence != null && (
            <Badge tone="good">
              Confidence{' '}
              {(Number(explain.confidence) <= 1 ? explain.confidence * 100 : explain.confidence).toFixed(1)}%
            </Badge>
          )}
          {explain.is_override && <Badge tone="warn">Overridden</Badge>}
          {explain.reviewer && <span className="muted">Reviewer: {explain.reviewer}</span>}
          {explain.classification_timestamp && (
            <span className="muted">{explain.classification_timestamp}</span>
          )}
        </div>
        {explain.override_reason && (
          <div className="info-box">Override reason: {explain.override_reason}</div>
        )}

        {rules.length ? (
          <div className="rule-trace">
            {rules.map((r, i) => (
              <div className="rule-step" key={i}>
                <div className="rule-step-head">
                  <span className="rule-step-no">{i + 1}</span>
                  <span className="rule-test">{r.test || '—'}</span>
                  <Badge tone="accent">{r.output}</Badge>
                </div>
                <div className="rule-step-body">
                  <div className="rule-name">
                    {r.rule_name || r.rule_id}{' '}
                    {r.rule_id && <span className="mono muted">({r.rule_id})</span>}
                  </div>
                  {r.rationale && <p className="rationale">{r.rationale}</p>}
                  {r.standard_ref && (
                    <div className="standard-ref">Standard: {r.standard_ref}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <Empty label="No applied rules recorded." />
        )}
      </Card>

      {explain.data_fields_used && (
        <Card title="Data Fields Used">
          <Json value={explain.data_fields_used} />
        </Card>
      )}
      {explain.data_sources && explain.data_sources.length > 0 && (
        <Card title="Data Sources">
          <ul className="plain-list">
            {explain.data_sources.map((s, i) => (
              <li key={i}>{typeof s === 'string' ? s : JSON.stringify(s)}</li>
            ))}
          </ul>
        </Card>
      )}
      {explain.full_trace && (
        <Card title="Full Trace">
          <Json value={explain.full_trace} />
        </Card>
      )}
    </div>
  )
}

// ---------- History ----------
function History({ history }) {
  const versions = Array.isArray(history) ? history : []
  if (!versions.length) return <Empty label="No classification history." />
  return (
    <Card title="Classification History">
      <div className="timeline">
        {versions.map((v, i) => (
          <div className="timeline-item" key={i}>
            <div className="timeline-dot" />
            <div className="timeline-body">
              <div className="timeline-head">
                <strong>Version {v.version}</strong>
                {v.is_current && <Badge tone="good">Current</Badge>}
                {v.is_override && <Badge tone="warn">Override</Badge>}
                <span className="muted">{v.created_at}</span>
              </div>
              <div className="timeline-dims">
                {DIMENSIONS.map(([k, label]) =>
                  v[k] != null ? (
                    <span key={k} className="mini-dim">
                      <em>{label}:</em> {String(v[k])}
                    </span>
                  ) : null
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}

// ---------- Quality ----------
const QUALITY_DIMS = [
  ['completeness', 'Completeness'],
  ['validity', 'Validity'],
  ['consistency', 'Consistency'],
  ['uniqueness', 'Uniqueness'],
  ['accuracy', 'Accuracy'],
  ['timeliness', 'Timeliness'],
]

function QualityView({ quality }) {
  if (!quality) return <Empty label="No quality data." />
  const exceptions = quality.exceptions || []
  return (
    <div>
      <Card title="Data Quality — 6 Dimensions">
        <div className="gauge-grid">
          {QUALITY_DIMS.map(([k, label]) =>
            quality[k] != null ? <Gauge key={k} label={label} value={quality[k]} /> : null
          )}
        </div>
        {quality.overall_score != null && (
          <div className="overall-score">
            <Gauge label="Overall Score" value={quality.overall_score} />
          </div>
        )}
      </Card>
      <Card title={`Exceptions (${exceptions.length})`}>
        {exceptions.length ? (
          <ul className="exception-list">
            {exceptions.map((ex, i) => (
              <li key={i}>{typeof ex === 'string' ? ex : JSON.stringify(ex)}</li>
            ))}
          </ul>
        ) : (
          <Empty label="No exceptions." />
        )}
      </Card>
    </div>
  )
}

// ---------- Audit ----------
function Audit({ audit }) {
  const rows = Array.isArray(audit) ? audit : []
  if (!rows.length) return <Empty label="No audit entries." />
  return (
    <Card title="Audit History">
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Action</th>
              <th>Actor</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((a, i) => (
              <tr key={i}>
                <td className="mono">{a.timestamp || a.created_at || a.ts || '—'}</td>
                <td>{a.action || a.event || a.type || '—'}</td>
                <td>{a.actor || a.user || a.username || '—'}</td>
                <td>
                  <span className="muted small">
                    {a.details
                      ? typeof a.details === 'string'
                        ? a.details
                        : JSON.stringify(a.details)
                      : a.message || ''}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export default function EnterpriseProfile() {
  const { id } = useParams()
  const [tab, setTab] = useState('Master Data')
  const { data, error, loading, reload, setData } = useAsync(
    () => api.enterpriseProfile(id),
    [id]
  )

  if (loading) return <Loading label="Loading enterprise profile…" />
  if (error) return <ErrorBox error={error} onRetry={reload} />

  const p = data || {}
  const e = p.enterprise || {}

  function onReclassify() {
    // After re-classify / override, reload the full profile.
    reload()
  }

  return (
    <div>
      <PageHeader
        title={e.legal_name_en || `Enterprise ${id}`}
        subtitle={
          <span>
            <span className="mono">{e.enterprise_id || id}</span>
            {e.sector_code ? ` · ${e.sector_code}` : ''}
            {e.public_private ? ` · ${e.public_private}` : ''}
          </span>
        }
        actions={
          <Link className="btn btn-ghost" to="/enterprises">
            ← Back
          </Link>
        }
      />

      <div className="tabs">
        {TABS.map((t) => (
          <button
            key={t}
            className={'tab' + (tab === t ? ' active' : '')}
            onClick={() => setTab(t)}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="tab-panel">
        {tab === 'Master Data' && (
          <Card title="Master Data">
            <MasterData e={e} />
            {p.legal_units && p.legal_units.length > 0 && (
              <>
                <h3 className="section-h">Legal Units ({p.legal_units.length})</h3>
                <Json value={p.legal_units} />
              </>
            )}
            {p.establishments && p.establishments.length > 0 && (
              <>
                <h3 className="section-h">Establishments ({p.establishments.length})</h3>
                <Json value={p.establishments} />
              </>
            )}
          </Card>
        )}
        {tab === 'Ownership' && <Ownership id={id} ownership={p.ownership} />}
        {tab === 'Classification' && (
          <Classification id={id} classification={p.current_classification} onReclassify={onReclassify} />
        )}
        {tab === 'Explainability' && <ExplainTab id={id} />}
        {tab === 'History' && <HistoryTab id={id} />}
        {tab === 'Quality' && <QualityView quality={p.quality} />}
        {tab === 'Audit' && <Audit audit={p.audit} />}
      </div>
    </div>
  )
}

// Lazily-loaded sub-tabs (separate API calls for freshest data).
function ExplainTab({ id }) {
  const { data, error, loading, reload } = useAsync(() => api.explain(id), [id])
  if (loading) return <Loading />
  if (error) return <ErrorBox error={error} onRetry={reload} />
  return <Explainability explain={data} />
}

function HistoryTab({ id }) {
  const { data, error, loading, reload } = useAsync(() => api.history(id), [id])
  if (loading) return <Loading />
  if (error) return <ErrorBox error={error} onRetry={reload} />
  return <History history={data} />
}
