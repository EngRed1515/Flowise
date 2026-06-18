import api from '../api/client.js'
import { useAsync } from '../hooks.js'
import { useAuth, hasRole } from '../auth.jsx'
import { PageHeader, Card, Loading, ErrorBox, Empty, Badge } from '../components/ui.jsx'

function UsersTable() {
  const { data, error, loading, reload } = useAsync(() => api.adminUsers(), [])
  if (loading) return <Loading />
  if (error) return <ErrorBox error={error} onRetry={reload} />
  const users = Array.isArray(data) ? data : data?.items || data?.users || []
  if (!users.length) return <Empty />
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>Role</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u, i) => (
            <tr key={u.username || i}>
              <td>{u.username || u.name || '—'}</td>
              <td>
                <Badge tone="accent">{u.role || '—'}</Badge>
              </td>
              <td>{u.active === false ? 'Disabled' : 'Active'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function RolesMatrix() {
  const { data, error, loading, reload } = useAsync(() => api.adminRoles(), [])
  if (loading) return <Loading />
  if (error) return <ErrorBox error={error} onRetry={reload} />

  // data is a role -> permissions map.
  const map = data && typeof data === 'object' && !Array.isArray(data) ? data : {}
  const roles = Object.keys(map)
  if (!roles.length) return <Empty label="No roles defined." />

  // Build the union of all permissions for matrix columns.
  const allPerms = Array.from(
    new Set(roles.flatMap((r) => (Array.isArray(map[r]) ? map[r] : Object.keys(map[r] || {}))))
  ).sort()

  function roleHas(role, perm) {
    const v = map[role]
    if (Array.isArray(v)) return v.includes(perm)
    if (v && typeof v === 'object') return !!v[perm]
    return false
  }

  return (
    <div className="table-wrap">
      <table className="data-table matrix">
        <thead>
          <tr>
            <th>Permission \ Role</th>
            {roles.map((r) => (
              <th key={r}>{r}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {allPerms.map((p) => (
            <tr key={p}>
              <td className="perm-name">{p}</td>
              {roles.map((r) => (
                <td key={r} className="matrix-cell">
                  {roleHas(r, p) ? <span className="check">✓</span> : <span className="dash">·</span>}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function Admin() {
  const { user } = useAuth()
  if (!hasRole(user, 'admin')) {
    return (
      <div>
        <PageHeader title="Administration" />
        <ErrorBox error={{ status: 403, message: 'Administrator access required.' }} />
      </div>
    )
  }
  return (
    <div>
      <PageHeader title="Administration" subtitle="Users and role-based access control" />
      <Card title="Users">
        <UsersTable />
      </Card>
      <Card title="Roles → Permissions Matrix">
        <RolesMatrix />
      </Card>
    </div>
  )
}
