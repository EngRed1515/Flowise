import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client.js'
import { PageHeader, Card, ErrorBox } from '../components/ui.jsx'

const NUMERIC = new Set([
  'employment',
  'turnover_qar',
  'total_assets_qar',
  'sales',
  'production_costs',
])
const BOOL = new Set([
  'is_nonprofit',
  'is_financial',
  'has_premises',
  'has_employees',
  'has_autonomy',
])

export default function NewEnterprise() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    legal_name_en: '',
    legal_name_ar: '',
    lei: '',
    legal_form_code: '',
    residence: '',
    isic_class: '',
    employment: '',
    turnover_qar: '',
    total_assets_qar: '',
    sales: '',
    production_costs: '',
    is_nonprofit: false,
    is_financial: false,
    has_premises: true,
    has_employees: true,
    has_autonomy: true,
    jurisdiction: '',
    group_id: '',
    birth_date: '',
  })
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  function set(k, v) {
    setForm((f) => ({ ...f, [k]: v }))
  }

  function buildPayload() {
    const out = {}
    Object.entries(form).forEach(([k, v]) => {
      if (BOOL.has(k)) {
        out[k] = !!v
      } else if (v === '' || v == null) {
        // skip empties (optional fields)
      } else if (NUMERIC.has(k)) {
        const n = Number(v)
        if (!Number.isNaN(n)) out[k] = n
      } else {
        out[k] = v
      }
    })
    return out
  }

  async function submit(e) {
    e.preventDefault()
    if (!form.legal_name_en.trim()) {
      setError(new Error('Legal name (English) is required.'))
      return
    }
    setBusy(true)
    setError(null)
    try {
      const created = await api.createEnterprise(buildPayload())
      navigate(`/enterprises/${created.enterprise_id}`)
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <PageHeader
        title="New Enterprise"
        subtitle="Register an enterprise. It will be validated and classified."
        actions={
          <button className="btn btn-ghost" onClick={() => navigate('/enterprises')}>
            Cancel
          </button>
        }
      />
      <Card>
        <form onSubmit={submit} className="form-grid">
          <label className="field">
            <span>Legal name (EN) *</span>
            <input value={form.legal_name_en} onChange={(e) => set('legal_name_en', e.target.value)} />
          </label>
          <label className="field">
            <span>Legal name (AR)</span>
            <input value={form.legal_name_ar} onChange={(e) => set('legal_name_ar', e.target.value)} />
          </label>
          <label className="field">
            <span>LEI</span>
            <input value={form.lei} onChange={(e) => set('lei', e.target.value)} />
          </label>
          <label className="field">
            <span>Legal form code</span>
            <input value={form.legal_form_code} onChange={(e) => set('legal_form_code', e.target.value)} />
          </label>
          <label className="field">
            <span>Residence</span>
            <input value={form.residence} onChange={(e) => set('residence', e.target.value)} placeholder="e.g. RESIDENT" />
          </label>
          <label className="field">
            <span>ISIC class</span>
            <input value={form.isic_class} onChange={(e) => set('isic_class', e.target.value)} />
          </label>
          <label className="field">
            <span>Employment</span>
            <input type="number" value={form.employment} onChange={(e) => set('employment', e.target.value)} />
          </label>
          <label className="field">
            <span>Turnover (QAR)</span>
            <input type="number" value={form.turnover_qar} onChange={(e) => set('turnover_qar', e.target.value)} />
          </label>
          <label className="field">
            <span>Total assets (QAR)</span>
            <input type="number" value={form.total_assets_qar} onChange={(e) => set('total_assets_qar', e.target.value)} />
          </label>
          <label className="field">
            <span>Sales</span>
            <input type="number" value={form.sales} onChange={(e) => set('sales', e.target.value)} />
          </label>
          <label className="field">
            <span>Production costs</span>
            <input type="number" value={form.production_costs} onChange={(e) => set('production_costs', e.target.value)} />
          </label>
          <label className="field">
            <span>Jurisdiction</span>
            <input value={form.jurisdiction} onChange={(e) => set('jurisdiction', e.target.value)} />
          </label>
          <label className="field">
            <span>Group ID</span>
            <input value={form.group_id} onChange={(e) => set('group_id', e.target.value)} />
          </label>
          <label className="field">
            <span>Birth date</span>
            <input type="date" value={form.birth_date} onChange={(e) => set('birth_date', e.target.value)} />
          </label>

          <div className="checkbox-row full">
            {[...BOOL].map((b) => (
              <label key={b} className="checkbox">
                <input type="checkbox" checked={!!form[b]} onChange={(e) => set(b, e.target.checked)} />
                <span>{b.replace(/_/g, ' ')}</span>
              </label>
            ))}
          </div>

          <div className="full">
            <ErrorBox error={error} />
            <button className="btn btn-primary" disabled={busy}>
              {busy ? 'Creating…' : 'Create Enterprise'}
            </button>
          </div>
        </form>
      </Card>
    </div>
  )
}
