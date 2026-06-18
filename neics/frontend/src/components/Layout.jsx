import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth, hasRole } from '../auth.jsx'

const NAV = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/enterprises', label: 'Enterprises' },
  { to: '/rules', label: 'Rules Repository' },
  { to: '/methodology', label: 'Methodology' },
  { to: '/reviews', label: 'Review Center' },
  { to: '/quality', label: 'Quality' },
  { to: '/simulate', label: 'Simulation Sandbox' },
  { to: '/admin', label: 'Administration', adminOnly: true },
]

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">NEICS</div>
          <div className="brand-sub">
            National Enterprise Intelligence &amp; Classification System
          </div>
        </div>
        <nav className="nav">
          {NAV.filter((n) => !n.adminOnly || hasRole(user, 'admin')).map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              className={({ isActive }) => 'nav-item' + (isActive ? ' active' : '')}
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="env-tag">STAGING / UAT</div>
          <div className="version">v1.0 · UAT</div>
        </div>
      </aside>

      <div className="main">
        <div className="uat-banner">
          STAGING / UAT ENVIRONMENT — Not for production. Data may be reset at any time.
        </div>
        <header className="topbar">
          <div className="topbar-title">Qatar · National Statistics</div>
          <div className="topbar-user">
            {user && (
              <>
                <span className="user-name">{user.username}</span>
                <span className="role-chip">{user.role}</span>
              </>
            )}
            <button className="btn btn-ghost" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>
        <main className="content">{children}</main>
      </div>
    </div>
  )
}
