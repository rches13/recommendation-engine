import { useState } from 'react'

export default function StarRating({ value, onChange, disabled }) {
  const [hovered, setHovered] = useState(0)
  const display = hovered || value || 0

  return (
    <div className="stars" aria-label="Rate this course">
      {[1, 2, 3, 4, 5].map(n => (
        <button
          key={n}
          type="button"
          className={`star ${n <= display ? 'filled' : ''} ${disabled ? 'disabled' : ''}`}
          onClick={() => !disabled && onChange(n)}
          onMouseEnter={() => !disabled && setHovered(n)}
          onMouseLeave={() => !disabled && setHovered(0)}
          aria-label={`${n} star${n > 1 ? 's' : ''}`}
        >
          ★
        </button>
      ))}
    </div>
  )
}
