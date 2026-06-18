import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import {
  PageHeader,
  Card,
  Loading,
  ErrorBox,
  KpiCard,
  BarBreakdown,
} from '../components/ui.jsx'

export default function Dashboard() {
  const { data, error, loading, reload } = useAsync(() => api.dashboard(), [])

  if (loading) return <Loading label="Loading dashboard…" />
  if (error) return <ErrorBox error={error} onRetry={reload} />

  const d = data || {}
  const avg = d.avg_quality_score
  const avgPct = avg == null ? '—' : (avg <= 1 ? (avg * 100).toFixed(1) : Number(avg).toFixed(1)) + '%'

  return (
    <div>
      <PageHeader
        title="Dashboard"
        subtitle="National enterprise register — classification & quality overview"
      />

      <div className="kpi-grid">
        <KpiCard label="Total Enterprises" value={d.total_enterprises} accent="#8A1538" />
        <KpiCard label="Classified" value={d.classified} />
        <KpiCard label="Pending Reviews" value={d.pending_reviews} />
        <KpiCard label="Avg Quality Score" value={avgPct} />
        <KpiCard label="Active Rules" value={d.rules_active} />
      </div>

      <div className="grid-2">
        <Card title="By Sector">
          <BarBreakdown data={d.by_sector} />
        </Card>
        <Card title="By Public / Private">
          <BarBreakdown data={d.by_public_private} />
        </Card>
        <Card title="By Size Class">
          <BarBreakdown data={d.by_size} />
        </Card>
        <Card title="By Control">
          <BarBreakdown data={d.by_control} />
        </Card>
        {d.by_quality_flag && (
          <Card title="By Quality Flag">
            <BarBreakdown data={d.by_quality_flag} />
          </Card>
        )}
      </div>
    </div>
  )
}
