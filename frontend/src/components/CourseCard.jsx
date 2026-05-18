import StarRating from './StarRating'

export default function CourseCard({ course, rating, onRate, loading }) {
  return (
    <div className={`course-card ${rating ? 'rated' : ''}`}>
      <div className="course-card-header">
        <span className="course-category">{course.category}</span>
        {rating && <span className="rated-badge">Rated</span>}
      </div>
      <h3 className="course-title">{course.title}</h3>
      <div className="course-tags">
        {course.tags.map(tag => (
          <span key={tag} className="tag">{tag}</span>
        ))}
      </div>
      <div className="course-footer">
        <StarRating
          value={rating || 0}
          onChange={r => onRate(course.id, r)}
          disabled={loading}
        />
        {!rating && <span className="rate-hint">Rate to get recommendations</span>}
      </div>
    </div>
  )
}
