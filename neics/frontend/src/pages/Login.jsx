import { useState } from 'react'
import { useNavigate, useLocation, Navigate } from 'react-router-dom'
import { useAuth } from '../auth.jsx'
import { ErrorBox } from '../components/ui.jsx'

const DEMO_USERS = [
  { username: 'admin', password: 'admin123', role: 'Administrator' },
  { username: 'methodologist', password: 'methodologist123', role: 'Methodologist' },
  { username: 'steward', password: 'steward123', role: 'Data Steward' },
  { username: 'classifier', password: 'classifier123', role: 'Classifier' },
  { username: 'reviewer', password: 'reviewer123', role: 'Reviewer' },
  { username: 'auditor', password: 'auditor123', role: 'Auditor' },
  { username: 'analyst', password: 'analyst123', role: 'Analyst' },
]

export default function Login() {
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  const from = location.state?.from?.pathname || '/'

  if (isAuthenticated) return <Navigate to={from} replace />

  async function doLogin(u, p) {
    setBusy(true)
    setError(null)
    try {
      await login(u, p)
      navigate(from, { replace: true })
    } catch (e) {
      setError(e)
    } finally {
      setBusy(false)
    }
  }

  function onSubmit(e) {
    e.preventDefault()
    doLogin(username, password)
  }

  function quickLogin(u) {
    setUsername(u.username)
    setPassword(u.password)
    doLogin(u.username, u.password)
  }

  return (
    <div className="login-page">
      <div className="login-banner">STAGING / UAT ENVIRONMENT — Not for production</div>
      <div className="login-wrap">
        <div className="login-card">
          <div className="login-brand">
            <div className="brand-mark big">NEICS</div>
            <div className="login-title">
              National Enterprise Intelligence &amp; Classification System
            </div>
            <div className="login-sub">Qatar · National Statistics</div>
          </div>

          <form onSubmit={onSubmit} className="login-form">
            <label className="field">
              <span>Username</span>
              <input
                autoFocus
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
              />
            </label>
            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </label>
            <ErrorBox error={error} />
            <button className="btn btn-primary btn-block" disabled={busy}>
              {busy ? 'Signing in…' : 'Sign in'}
            </button>
          </form>
        </div>

        <div className="login-card demo-card">
          <h3>Demo Users (UAT)</h3>
          <p className="muted">Click a role to sign in instantly.</p>
          <div className="demo-list">
            {DEMO_USERS.map((u) => (
              <button
                key={u.username}
                className="demo-btn"
                onClick={() => quickLogin(u)}
                disabled={busy}
              >
                <span className="demo-role">{u.role}</span>
                <span className="demo-user">{u.username}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
