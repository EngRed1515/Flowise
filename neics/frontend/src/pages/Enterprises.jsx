import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
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

function qualityTone(flag) {
  const f = String(flag || '').toUpperCase()
  if (f.includes('GREEN') || f.includes('PASS') || f.includes('OK')) return 'good'
  if (f.includes('AMBER') || f.includes('WARN') || f.includes('YELLOW')) return 'warn'
  if (f.includes('RED') || f.includes('FAIL')) return 'bad'
  return 'neutral'
}

function UploadPanel({ onDone }) {
  const [file, setFile] = useState(null)
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    if (!file) return
    setBusy(true)
    setError(null)
    setResult(null)
    try {
      const r = await api.ingestUpload(file)
      setResult(r)
      onDone && onDone()
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form onSubmit={submit} className="upload-panel">
      <input
        type="file"
        accept=".csv,.json,.xlsx,.xls"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button className="btn btn-sm btn-primary" disabled={!file || busy}>
        {busy ? 'Uploading…' : 'Upload & Ingest'}
      </button>
      <ErrorBox error={error} />
      {result && (
        <div className="ingest-result">
          <div>
            Received <b>{result.received}</b> · Created <b>{result.created}</b> · Rejected{' '}
            <b>{result.rejected}</b>
          </div>
          {result.results && <Json value={result.results} />}
        </div>
      )}
    </form>
  )
}

export default function Enterprises() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState({
    q: '',
    sector: '',
    public_private: '',
    size: '',
  })
  const [applied, setApplied] = useState({ q: '', sector: '', public_private: '', size: '' })
  const [showUpload, setShowUpload] = useState(false)

  const sectors = useAsync(() => api.refSectors().catch(() => []), [])
  const { data, error, loading, reload } = useAsync(
    () => api.enterprises({ ...applied, limit: 200, offset: 0 }),
    [applied]
  )

  const rows = Array.isArray(data) ? data : data?.items || []

  function applyFilters(e) {
    e.preventDefault()
    setApplied({ ...filters })
  }

  function reset() {
    const empty = { q: '', sector: '', public_private: '', size: '' }
    setFilters(empty)
    setApplied(empty)
  }

  const sectorOptions = Array.isArray(sectors.data) ? sectors.data : []

  return (
    <div>
      <PageHeader
        title="Enterprises"
        subtitle="Search and classify enterprises in the national register"
        actions={
          <>
            <button className="btn" onClick={() => setShowUpload((s) => !s)}>
              {showUpload ? 'Hide Upload' : 'Upload'}
            </button>
            <Link className="btn btn-primary" to="/enterprises/new">
              + New Enterprise
            </Link>
          </>
        }
      />

      {showUpload && (
        <Card title="Bulk Ingestion">
          <p className="muted">
            Upload a CSV / JSON / Excel file of enterprises. Records are validated and classified on
            ingestion.
          </p>
          <UploadPanel onDone={reload} />
        </Card>
      )}

      <Card title="Filters">
        <form className="filter-bar" onSubmit={applyFilters}>
          <input
            placeholder="Search name / LEI / id…"
            value={filters.q}
            onChange={(e) => setFilters({ ...filters, q: e.target.value })}
          />
          <select
            value={filters.sector}
            onChange={(e) => setFilters({ ...filters, sector: e.target.value })}
          >
            <option value="">All sectors</option>
            {sectorOptions.map((s) => {
              const code = s.sector_code || s.code || s.id
              const name = s.name || s.label || code
              return (
                <option key={code} value={code}>
                  {code} — {name}
                </option>
              )
            })}
          </select>
          <select
            value={filters.public_private}
            onChange={(e) => setFilters({ ...filters, public_private: e.target.value })}
          >
            <option value="">Public / Private (all)</option>
            <option value="PUBLIC">Public</option>
            <option value="PRIVATE">Private</option>
          </select>
          <select
            value={filters.size}
            onChange={(e) => setFilters({ ...filters, size: e.target.value })}
          >
            <option value="">All sizes</option>
            <option value="MICRO">Micro</option>
            <option value="SMALL">Small</option>
            <option value="MEDIUM">Medium</option>
            <option value="LARGE">Large</option>
          </select>
          <button className="btn btn-primary" type="submit">
            Apply
          </button>
          <button className="btn btn-ghost" type="button" onClick={reset}>
            Reset
          </button>
        </form>
      </Card>

      <Card title={`Results${rows.length ? ` (${rows.length})` : ''}`}>
        {loading ? (
          <Loading />
        ) : error ? (
          <ErrorBox error={error} onRetry={reload} />
        ) : !rows.length ? (
          <Empty />
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Legal Name</th>
                  <th>Sector</th>
                  <th>Public/Private</th>
                  <th>Size</th>
                  <th>Control</th>
                  <th>Quality</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((e) => (
                  <tr
                    key={e.enterprise_id}
                    className="clickable"
                    onClick={() => navigate(`/enterprises/${e.enterprise_id}`)}
                  >
                    <td className="mono">{e.enterprise_id}</td>
                    <td>
                      <div className="cell-primary">{e.legal_name_en || '—'}</div>
                      {e.legal_name_ar && <div className="cell-secondary">{e.legal_name_ar}</div>}
                    </td>
                    <td>{e.sector_code || '—'}</td>
                    <td>{e.public_private || '—'}</td>
                    <td>{e.size_class || '—'}</td>
                    <td>{e.control_flag || '—'}</td>
                    <td>
                      {e.quality_flag ? (
                        <Badge tone={qualityTone(e.quality_flag)}>
                          {e.quality_flag}
                          {e.quality_score != null
                            ? ` · ${Number(e.quality_score) <= 1 ? (e.quality_score * 100).toFixed(0) : e.quality_score}`
                            : ''}
                        </Badge>
                      ) : (
                        '—'
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}
