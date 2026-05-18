import { useState } from 'react'
import { api } from '../api'

export default function UserSetup({ onUserCreated }) {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!name.trim()) return
    setLoading(true)
    setError(null)
    try {
      const user = await api.createUser(name.trim())
      onUserCreated(user)
    } catch {
      setError('Could not create user — is the API running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="setup-container">
      <div className="setup-card">
        <h1 className="setup-title">Recommendation Engine</h1>
        <p className="setup-subtitle">
          Rate courses you've taken and get personalised learning path recommendations
          powered by collaborative filtering.
        </p>
        <form onSubmit={handleSubmit} className="setup-form">
          <input
            className="setup-input"
            type="text"
            placeholder="Enter your name to get started"
            value={name}
            onChange={e => setName(e.target.value)}
            autoFocus
          />
          <button className="btn-primary" type="submit" disabled={loading || !name.trim()}>
            {loading ? 'Creating…' : 'Start →'}
          </button>
        </form>
        {error && <p className="error-msg">{error}</p>}
      </div>
    </div>
  )
}
