import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import { PageHeader, Card, Loading, ErrorBox, Empty, Badge } from '../components/ui.jsx'

function ResolveForm({ review, onResolved }) {
  const [decision, setDecision] = useState('APPROVED')
  const [note, setNote] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  const id = review.review_id || review.id

  async function resolve(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await api.resolveReview(id, { decision, resolution: decision, note, notes: note })
      onResolved && onResolved()
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="resolve-form" onSubmit={resolve}>
      <select value={decision} onChange={(e) => setDecision(e.target.value)}>
        <option value="APPROVED">Approve</option>
        <option value="REJECTED">Reject</option>
        <option value="ESCALATED">Escalate</option>
      </select>
      <input
        placeholder="Resolution note…"
        value={note}
        onChange={(e) => setNote(e.target.value)}
      />
      <button className="btn btn-sm btn-primary" disabled={busy}>
        {busy ? 'Saving…' : 'Resolve'}
      </button>
      <ErrorBox error={error} />
    </form>
  )
}

export default function Reviews() {
  const [status, setStatus] = useState('OPEN')
  const { data, error, loading, reload } = useAsync(() => api.reviews(status), [status])

  const rows = Array.isArray(data) ? data : data?.items || []

  return (
    <div>
      <PageHeader
        title="Review Center"
        subtitle="Queue of classification items requiring human review"
        actions={
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="OPEN">Open</option>
            <option value="ALL">All</option>
          </select>
        }
      />
      <Card title={`Reviews${rows.length ? ` (${rows.length})` : ''}`}>
        {loading ? (
          <Loading />
        ) : error ? (
          <ErrorBox error={error} onRetry={reload} />
        ) : !rows.length ? (
          <Empty label="No reviews in this queue." />
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Enterprise</th>
                  <th>Reason</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => {
                  const ent = r.enterprise_id || r.record_id
                  const open = String(r.status || '').toUpperCase() === 'OPEN'
                  return (
                    <tr key={r.review_id || r.id}>
                      <td className="mono">{r.review_id || r.id}</td>
                      <td>
                        {ent ? (
                          <Link to={`/enterprises/${ent}`} className="mono link">
                            {ent}
                          </Link>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td>{r.reason || r.type || r.description || '—'}</td>
                      <td>
                        <Badge tone={open ? 'warn' : 'good'}>{r.status || '—'}</Badge>
                      </td>
                      <td className="mono small">{r.created_at || r.timestamp || '—'}</td>
                      <td>
                        {open ? (
                          <ResolveForm review={r} onResolved={reload} />
                        ) : (
                          <span className="muted small">
                            {r.resolution || r.decision || 'Resolved'}
                          </span>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}
