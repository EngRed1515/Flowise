// Lightweight fetch-based API client for NEICS (no axios).
// In dev, Vite proxies /api and /health to the backend.
// In production (nginx), the same paths are proxied to the backend container.

const TOKEN_KEY = 'neics_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export class ApiError extends Error {
  constructor(status, message, detail) {
    super(message)
    this.status = status
    this.detail = detail
  }
}

async function parseError(res) {
  let detail = null
  let message = `Request failed (${res.status})`
  try {
    const data = await res.json()
    if (data && data.detail) {
      detail = data.detail
      message = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
    }
  } catch {
    /* non-JSON body */
  }
  return new ApiError(res.status, message, detail)
}

async function request(method, path, { body, form, headers = {}, auth = true } = {}) {
  const opts = { method, headers: { ...headers } }

  if (auth) {
    const token = getToken()
    if (token) opts.headers['Authorization'] = `Bearer ${token}`
  }

  if (form) {
    // application/x-www-form-urlencoded
    const params = new URLSearchParams()
    Object.entries(form).forEach(([k, v]) => params.append(k, v))
    opts.body = params.toString()
    opts.headers['Content-Type'] = 'application/x-www-form-urlencoded'
  } else if (body instanceof FormData) {
    opts.body = body // let browser set multipart boundary
  } else if (body !== undefined) {
    opts.body = JSON.stringify(body)
    opts.headers['Content-Type'] = 'application/json'
  }

  const res = await fetch(path, opts)

  if (res.status === 401 && auth) {
    clearToken()
    // Force the app to re-evaluate auth state.
    if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
      window.location.assign('/login')
    }
    throw await parseError(res)
  }

  if (!res.ok) throw await parseError(res)

  if (res.status === 204) return null
  const ct = res.headers.get('content-type') || ''
  if (ct.includes('application/json')) return res.json()
  return res.text()
}

function qs(params = {}) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') search.append(k, v)
  })
  const s = search.toString()
  return s ? `?${s}` : ''
}

export const api = {
  // ---- Auth ----
  login: (username, password) =>
    request('POST', '/api/auth/login', { form: { username, password }, auth: false }),
  me: () => request('GET', '/api/auth/me'),

  // ---- Dashboard ----
  dashboard: () => request('GET', '/api/dashboard'),

  // ---- Enterprises ----
  enterprises: (params) => request('GET', `/api/enterprises${qs(params)}`),
  enterprise: (id) => request('GET', `/api/enterprises/${id}`),
  createEnterprise: (body) => request('POST', '/api/enterprises', { body }),
  updateEnterprise: (id, body) => request('PUT', `/api/enterprises/${id}`, { body }),
  enterpriseProfile: (id) => request('GET', `/api/enterprises/${id}/profile`),
  enterpriseOwnership: (id) => request('GET', `/api/enterprises/${id}/ownership`),
  addOwnership: (id, body) => request('POST', `/api/enterprises/${id}/ownership`, { body }),
  classify: (id) => request('POST', `/api/enterprises/${id}/classify`),
  classification: (id) => request('GET', `/api/enterprises/${id}/classification`),
  history: (id) => request('GET', `/api/enterprises/${id}/history`),
  explain: (id) => request('GET', `/api/enterprises/${id}/explain`),
  override: (id, body) => request('POST', `/api/enterprises/${id}/override`, { body }),

  // ---- Rules ----
  rules: (params) => request('GET', `/api/rules${qs(params)}`),
  rule: (ruleId) => request('GET', `/api/rules/${ruleId}`),
  testRule: (ruleId, facts) => request('POST', `/api/rules/${ruleId}/test`, { body: facts }),

  // ---- Methodology ----
  tests: () => request('GET', '/api/tests'),
  standards: () => request('GET', '/api/standards'),
  metadata: (entity) => request('GET', `/api/metadata${qs({ entity })}`),

  // ---- Reference ----
  refSectors: () => request('GET', '/api/reference/sectors'),
  refLegalForms: () => request('GET', '/api/reference/legal-forms'),
  refIsic: () => request('GET', '/api/reference/isic'),
  refSizeThresholds: () => request('GET', '/api/reference/size-thresholds'),
  refCodelist: (domain) => request('GET', `/api/reference/codelist/${domain}`),

  // ---- Simulation ----
  simulate: (body) => request('POST', '/api/simulate', { body }),

  // ---- Ingest ----
  ingestEnterprises: (arr) => request('POST', '/api/ingest/enterprises', { body: arr }),
  ingestUpload: (file) => {
    const fd = new FormData()
    fd.append('file', file)
    return request('POST', '/api/ingest/upload', { body: fd })
  },

  // ---- Governance ----
  reviews: (status) => request('GET', `/api/reviews${qs({ status })}`),
  resolveReview: (id, body) => request('POST', `/api/reviews/${id}/resolve`, { body }),
  audit: (recordId) => request('GET', `/api/audit${qs({ record_id: recordId })}`),
  quality: () => request('GET', '/api/quality'),

  // ---- Admin ----
  adminUsers: () => request('GET', '/api/admin/users'),
  adminRoles: () => request('GET', '/api/admin/roles'),
}

export default api
