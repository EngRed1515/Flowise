// Small shared presentational components used across pages.

export function Loading({ label = 'Loading…' }) {
  return (
    <div className="loading">
      <div className="spinner" aria-hidden />
      <span>{label}</span>
    </div>
  )
}

export function ErrorBox({ error, onRetry }) {
  if (!error) return null
  const msg =
    error instanceof Error ? error.message : typeof error === 'string' ? error : 'Unexpected error'
  const status = error && error.status ? ` (HTTP ${error.status})` : ''
  return (
    <div className="error-box" role="alert">
      <strong>Error{status}:</strong> {msg}
      {error && error.status === 403 && (
        <div className="error-hint">
          Your role does not have permission to perform this action.
        </div>
      )}
      {onRetry && (
        <button className="btn btn-sm" onClick={onRetry} style={{ marginTop: 8 }}>
          Retry
        </button>
      )}
    </div>
  )
}

export function Empty({ label = 'No records found.' }) {
  return <div className="empty">{label}</div>
}

export function Card({ title, actions, children, className = '' }) {
  return (
    <section className={`card ${className}`}>
      {(title || actions) && (
        <div className="card-head">
          {title && <h2 className="card-title">{title}</h2>}
          {actions && <div className="card-actions">{actions}</div>}
        </div>
      )}
      <div className="card-body">{children}</div>
    </section>
  )
}

export function Badge({ children, tone = 'neutral' }) {
  return <span className={`badge badge-${tone}`}>{children}</span>
}

export function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="page-header">
      <div>
        <h1 className="page-title">{title}</h1>
        {subtitle && <p className="page-subtitle">{subtitle}</p>}
      </div>
      {actions && <div className="page-actions">{actions}</div>}
    </div>
  )
}

// Simple horizontal CSS bar chart from an object {key: count}.
export function BarBreakdown({ data, emptyLabel = 'No data' }) {
  const entries = Object.entries(data || {}).filter(([, v]) => v != null)
  if (!entries.length) return <Empty label={emptyLabel} />
  const max = Math.max(...entries.map(([, v]) => Number(v) || 0), 1)
  return (
    <div className="bars">
      {entries.map(([k, v]) => (
        <div className="bar-row" key={k}>
          <div className="bar-label" title={k}>
            {k}
          </div>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${((Number(v) || 0) / max) * 100}%` }} />
          </div>
          <div className="bar-value">{v}</div>
        </div>
      ))}
    </div>
  )
}

// A 0..1 (or 0..100) gauge rendered as a labeled bar.
export function Gauge({ label, value }) {
  let pct = Number(value)
  if (Number.isNaN(pct)) pct = 0
  if (pct <= 1) pct = pct * 100
  pct = Math.max(0, Math.min(100, pct))
  const tone = pct >= 85 ? 'good' : pct >= 60 ? 'warn' : 'bad'
  return (
    <div className="gauge">
      <div className="gauge-top">
        <span className="gauge-label">{label}</span>
        <span className="gauge-pct">{pct.toFixed(1)}%</span>
      </div>
      <div className="gauge-track">
        <div className={`gauge-fill gauge-${tone}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

export function KpiCard({ label, value, accent }) {
  return (
    <div className="kpi-card">
      <div className="kpi-value" style={accent ? { color: accent } : undefined}>
        {value ?? '—'}
      </div>
      <div className="kpi-label">{label}</div>
    </div>
  )
}

// Generic JSON viewer.
export function Json({ value }) {
  return <pre className="json-view">{JSON.stringify(value, null, 2)}</pre>
}
