import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import api, { getToken, setToken, clearToken } from './api/client.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // On mount, if we have a token, fetch the current user.
  useEffect(() => {
    let active = true
    async function bootstrap() {
      const token = getToken()
      if (!token) {
        setLoading(false)
        return
      }
      try {
        const me = await api.me()
        if (active) setUser(me)
      } catch {
        clearToken()
        if (active) setUser(null)
      } finally {
        if (active) setLoading(false)
      }
    }
    bootstrap()
    return () => {
      active = false
    }
  }, [])

  const login = useCallback(async (username, password) => {
    const data = await api.login(username, password)
    setToken(data.access_token)
    // The login response carries role + username; hydrate from /me for completeness.
    let me = { username: data.username, role: data.role }
    try {
      me = await api.me()
    } catch {
      /* fall back to login payload */
    }
    setUser(me)
    return me
  }, [])

  const logout = useCallback(() => {
    clearToken()
    setUser(null)
  }, [])

  const value = { user, loading, login, logout, isAuthenticated: !!user }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

// Helper: does the current user's role match any of the allowed roles?
export function hasRole(user, ...roles) {
  if (!user || !user.role) return false
  const r = String(user.role).toLowerCase()
  return roles.map((x) => String(x).toLowerCase()).includes(r)
}
