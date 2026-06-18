import { Link } from 'react-router-dom'
import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import {
  PageHeader,
  Card,
  Loading,
  ErrorBox,
  Empty,
  Gauge,
  Badge,
} from '../components/ui.jsx'

function fmtScore(v) {
  if (v == null) return '—'
  const n = Number(v)
  if (Number.isNaN(n)) return String(v)
  return (n <= 1 ? n * 100 : n).toFixed(1) + '%'
}

export default function Quality() {
  const { data, error, loading, reload } = useAsync(() => api.quality(), [])

  if (loading) return <Loading label="Loading quality report…" />
  if (error) return <ErrorBox error={error} onRetry={reload} />

  const d = data || {}
  const dataset = d.dataset_scores || {}
  const entScores = d.enterprise_scores || []
  const exceptions = d.exceptions || []

  return (
    <div>
      <PageHeader
        title="Data Quality"
        subtitle="Dataset-level scores, per-enterprise scores, and exception report"
      />

      <Card title="Dataset Scores">
        {Object.keys(dataset).length ? (
          <div className="gauge-grid">
            {Object.entries(dataset).map(([k, v]) => (
              <Gauge key={k} label={k.replace(/_/g, ' ')} value={v} />
            ))}
          </div>
        ) : (
          <Empty />
        )}
      </Card>

      <Card title={`Exceptions (${d.exception_count ?? exceptions.length})`}>
        {exceptions.length ? (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Enterprise</th>
                  <th>Dimension</th>
                  <th>Severity</th>
                  <th>Message</th>
                </tr>
              </thead>
              <tbody>
                {exceptions.map((ex, i) => {
                  const obj = typeof ex === 'string' ? { message: ex } : ex
                  const ent = obj.enterprise_id || obj.record_id
                  return (
                    <tr key={i}>
                      <td>
                        {ent ? (
                          <Link className="mono link" to={`/enterprises/${ent}`}>
                            {ent}
                          </Link>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td>{obj.dimension || obj.rule || '—'}</td>
                      <td>
                        {obj.severity ? <Badge tone="warn">{obj.severity}</Badge> : '—'}
                      </td>
                      <td className="small">{obj.message || obj.detail || JSON.stringify(obj)}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty label="No exceptions." />
        )}
      </Card>

      <Card title={`Per-Enterprise Scores (${entScores.length})`}>
        {entScores.length ? (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Enterprise</th>
                  <th>Name</th>
                  <th>Completeness</th>
                  <th>Validity</th>
                  <th>Consistency</th>
                  <th>Uniqueness</th>
                  <th>Accuracy</th>
                  <th>Timeliness</th>
                  <th>Overall</th>
                  <th>Flag</th>
                </tr>
              </thead>
              <tbody>
                {entScores.map((s, i) => {
                  const ent = s.enterprise_id || s.record_id
                  return (
                    <tr key={ent || i}>
                      <td>
                        {ent ? (
                          <Link className="mono link" to={`/enterprises/${ent}`}>
                            {ent}
                          </Link>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td>{s.legal_name_en || s.name || '—'}</td>
                      <td>{fmtScore(s.completeness)}</td>
                      <td>{fmtScore(s.validity)}</td>
                      <td>{fmtScore(s.consistency)}</td>
                      <td>{fmtScore(s.uniqueness)}</td>
                      <td>{fmtScore(s.accuracy)}</td>
                      <td>{fmtScore(s.timeliness)}</td>
                      <td>
                        <strong>{fmtScore(s.overall_score ?? s.overall)}</strong>
                      </td>
                      <td>{s.quality_flag ? <Badge>{s.quality_flag}</Badge> : '—'}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty />
        )}
      </Card>
    </div>
  )
}
