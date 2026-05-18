export default function RecommendationList({ recommendations, loading }) {
  if (loading) {
    return (
      <div className="rec-panel">
        <h2 className="rec-title">Recommended for you</h2>
        <div className="rec-loading">Calculating…</div>
      </div>
    )
  }

  return (
    <div className="rec-panel">
      <h2 className="rec-title">Recommended for you</h2>
      {recommendations.length === 0 ? (
        <p className="rec-empty">Rate at least one course to get recommendations.</p>
      ) : (
        <ol className="rec-list">
          {recommendations.map((rec, i) => (
            <li key={rec.course_id} className="rec-item">
              <div className="rec-rank">{i + 1}</div>
              <div className="rec-info">
                <span className="rec-course-title">{rec.title}</span>
                <span className="rec-category">{rec.category}</span>
                <div className="rec-tags">
                  {rec.tags.map(t => <span key={t} className="tag small">{t}</span>)}
                </div>
              </div>
              <div className="rec-score">
                <span className="score-value">{rec.score.toFixed(2)}</span>
                <span className="score-label">score</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}
