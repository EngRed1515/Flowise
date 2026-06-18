import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './auth.jsx'
import { Loading } from './components/ui.jsx'
import Layout from './components/Layout.jsx'

import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Enterprises from './pages/Enterprises.jsx'
import EnterpriseProfile from './pages/EnterpriseProfile.jsx'
import NewEnterprise from './pages/NewEnterprise.jsx'
import Rules from './pages/Rules.jsx'
import Methodology from './pages/Methodology.jsx'
import Reviews from './pages/Reviews.jsx'
import Quality from './pages/Quality.jsx'
import Simulate from './pages/Simulate.jsx'
import Admin from './pages/Admin.jsx'

function Protected({ children }) {
  const { isAuthenticated, loading } = useAuth()
  const location = useLocation()
  if (loading) return <Loading label="Authenticating…" />
  if (!isAuthenticated) return <Navigate to="/login" state={{ from: location }} replace />
  return <Layout>{children}</Layout>
}

export default function App() {
  const { loading } = useAuth()
  if (loading) return <Loading label="Starting NEICS…" />

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Protected><Dashboard /></Protected>} />
      <Route path="/enterprises" element={<Protected><Enterprises /></Protected>} />
      <Route path="/enterprises/new" element={<Protected><NewEnterprise /></Protected>} />
      <Route path="/enterprises/:id" element={<Protected><EnterpriseProfile /></Protected>} />
      <Route path="/rules" element={<Protected><Rules /></Protected>} />
      <Route path="/methodology" element={<Protected><Methodology /></Protected>} />
      <Route path="/reviews" element={<Protected><Reviews /></Protected>} />
      <Route path="/quality" element={<Protected><Quality /></Protected>} />
      <Route path="/simulate" element={<Protected><Simulate /></Protected>} />
      <Route path="/admin" element={<Protected><Admin /></Protected>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
