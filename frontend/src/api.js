const BASE = import.meta.env.VITE_API_URL || '/api'

async function request(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(`${method} ${path} → ${res.status}`)
  return res.json()
}

export const api = {
  createUser:       (name)                  => request('POST', '/users', { name }),
  getCourses:       ()                      => request('GET', '/courses'),
  getInteractions:  (userId)                => request('GET', `/users/${userId}/interactions`),
  rate:             (userId, courseId, rating) => request('POST', `/users/${userId}/interactions`, { course_id: courseId, rating }),
  getRecommendations: (userId, topN = 5)    => request('GET', `/users/${userId}/recommendations?top_n=${topN}`),
}
