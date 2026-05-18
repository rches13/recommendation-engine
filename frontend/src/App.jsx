import { useState, useEffect, useCallback } from 'react'
import { api } from './api'
import UserSetup from './components/UserSetup'
import CourseCard from './components/CourseCard'
import RecommendationList from './components/RecommendationList'

const CATEGORIES = ['All', 'Programming', 'Backend', 'Frontend', 'Databases', 'DevOps', 'Cloud', 'AI/ML', 'Architecture', 'Tools', 'Career']

export default function App() {
  const [user, setUser] = useState(null)
  const [courses, setCourses] = useState([])
  const [interactions, setInteractions] = useState({})
  const [recommendations, setRecommendations] = useState([])
  const [recsLoading, setRecsLoading] = useState(false)
  const [ratingLoading, setRatingLoading] = useState(false)
  const [activeCategory, setActiveCategory] = useState('All')
  const [error, setError] = useState(null)

  useEffect(() => {
    api.getCourses().then(setCourses).catch(() => setError('Could not load courses — is the API running?'))
  }, [])

  const fetchRecs = useCallback(async (userId) => {
    setRecsLoading(true)
    try {
      const recs = await api.getRecommendations(userId)
      setRecommendations(recs)
    } finally {
      setRecsLoading(false)
    }
  }, [])

  async function handleUserCreated(newUser) {
    setUser(newUser)
    fetchRecs(newUser.id)
  }

  async function handleRate(courseId, rating) {
    if (!user || ratingLoading) return
    setRatingLoading(true)
    try {
      await api.rate(user.id, courseId, rating)
      setInteractions(prev => ({ ...prev, [courseId]: rating }))
      await fetchRecs(user.id)
    } catch {
      setError('Failed to save rating.')
    } finally {
      setRatingLoading(false)
    }
  }

  function handleSwitchUser() {
    setUser(null)
    setInteractions({})
    setRecommendations([])
  }

  const filtered = activeCategory === 'All'
    ? courses
    : courses.filter(c => c.category === activeCategory)

  if (!user) return <UserSetup onUserCreated={handleUserCreated} />

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <span className="header-logo">⚡</span>
          <span className="header-title">Recommendation Engine</span>
        </div>
        <div className="header-right">
          <span className="header-user">
            {user.name}
            <span className="rated-count">{Object.keys(interactions).length} rated</span>
          </span>
          <button className="btn-ghost" onClick={handleSwitchUser}>Switch user</button>
        </div>
      </header>

      {error && <div className="error-banner">{error} <button onClick={() => setError(null)}>✕</button></div>}

      <div className="app-body">
        <main className="courses-panel">
          <div className="courses-header">
            <h2 className="section-title">Course Catalogue</h2>
            <div className="category-filters">
              {CATEGORIES.map(cat => (
                <button
                  key={cat}
                  className={`filter-btn ${activeCategory === cat ? 'active' : ''}`}
                  onClick={() => setActiveCategory(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
          <div className="course-grid">
            {filtered.map(course => (
              <CourseCard
                key={course.id}
                course={course}
                rating={interactions[course.id] || 0}
                onRate={handleRate}
                loading={ratingLoading}
              />
            ))}
          </div>
        </main>

        <aside className="sidebar">
          <RecommendationList recommendations={recommendations} loading={recsLoading} />
        </aside>
      </div>
    </div>
  )
}
