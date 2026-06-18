import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import { PageHeader, Card, Loading, ErrorBox, Empty, Badge, Json } from '../components/ui.jsx'

function Tests() {
  const { data, error, loading, reload } = useAsync(() => api.tests(), [])
  if (loading) return <Loading />
  if (error) return <ErrorBox error={error} onRetry={reload} />
  const tests = Array.isArray(data) ? data : data?.items || []
  const sorted = [...tests].sort((a, b) => (a.seq ?? 0) - (b.seq ?? 0))
  if (!sorted.length) return <Empty />
  return (
    <div className="test-list">
      {sorted.map((t) => (
        <div className="test-card" key={t.test_code}>
          <div className="test-seq">{t.seq ?? '·'}</div>
          <div className="test-body">
            <div className="test-head">
              <strong>{t.name}</strong>
              <Badge tone="accent">{t.test_code}</Badge>
              {t.phase && <Badge>{t.phase}</Badge>}
              {t.output_dimension && <Badge tone="good">{t.output_dimension}</Badge>}
            </div>
            {t.description && <p className="muted">{t.description}</p>}
            {t.standard_ref && <div className="standard-ref">Standard: {t.standard_ref}</div>}
          </div>
        </div>
      ))}
    </div>
  )
}

function Standards() {
  const { data, error, loading, reload } = useAsync(() => api.standards(), [])
  if (loading) return <Loading />
  if (error) return <ErrorBox error={error} onRetry={reload} />
  const standards = Array.isArray(data) ? data : data?.items || []
  if (!standards.length) return <Empty />
  return (
    <div className="standard-list">
      {standards.map((s, i) => (
        <div className="standard-block" key={s.standard_id || s.code || i}>
          <div className="standard-head">
            <strong>{s.name || s.title || s.standard_id || s.code}</strong>
            {s.version && <Badge>v{s.version}</Badge>}
            {(s.code || s.standard_id) && <Badge tone="accent">{s.code || s.standard_id}</Badge>}
          </div>
          {s.description && <p className="muted">{s.description}</p>}
          {s.concepts && s.concepts.length > 0 && (
            <details className="concepts">
              <summary>{s.concepts.length} concepts</summary>
              <Json value={s.concepts} />
            </details>
          )}
        </div>
      ))}
    </div>
  )
}

export default function Methodology() {
  return (
    <div>
      <PageHeader
        title="Methodology"
        subtitle="The 18-test classification framework and the standards repository"
      />
      <Card title="Classification Tests (18)">
        <Tests />
      </Card>
      <Card title="Standards Repository">
        <Standards />
      </Card>
    </div>
  )
}
