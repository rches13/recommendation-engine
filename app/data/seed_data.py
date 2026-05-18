"""
Seed data: learning paths and simulated user interactions for bootstrapping
the collaborative filter.
"""

COURSES = [
    {"id": "c001", "title": "Python Fundamentals",         "category": "Programming",       "tags": ["python", "beginner"]},
    {"id": "c002", "title": "Data Structures & Algorithms", "category": "Programming",       "tags": ["python", "cs-fundamentals"]},
    {"id": "c003", "title": "REST API Design",              "category": "Backend",           "tags": ["api", "backend", "http"]},
    {"id": "c004", "title": "FastAPI in Practice",          "category": "Backend",           "tags": ["fastapi", "python", "api"]},
    {"id": "c005", "title": "SQL & PostgreSQL",             "category": "Databases",         "tags": ["sql", "postgresql", "databases"]},
    {"id": "c006", "title": "Docker & Containers",          "category": "DevOps",            "tags": ["docker", "devops", "containers"]},
    {"id": "c007", "title": "CI/CD with GitHub Actions",   "category": "DevOps",            "tags": ["cicd", "github-actions", "automation"]},
    {"id": "c008", "title": "AWS Cloud Essentials",         "category": "Cloud",             "tags": ["aws", "cloud", "ec2", "s3"]},
    {"id": "c009", "title": "Machine Learning Foundations", "category": "AI/ML",             "tags": ["ml", "scikit-learn", "python"]},
    {"id": "c010", "title": "React.js for Beginners",       "category": "Frontend",          "tags": ["react", "javascript", "frontend"]},
    {"id": "c011", "title": "TypeScript Essentials",        "category": "Frontend",          "tags": ["typescript", "javascript", "frontend"]},
    {"id": "c012", "title": "System Design Basics",         "category": "Architecture",      "tags": ["system-design", "scalability"]},
    {"id": "c013", "title": "Git & Version Control",        "category": "Tools",             "tags": ["git", "collaboration"]},
    {"id": "c014", "title": "Intro to AI Agents",           "category": "AI/ML",             "tags": ["ai-agents", "llm", "python"]},
    {"id": "c015", "title": "Career Pathways in Tech",      "category": "Career",            "tags": ["career", "job-search", "portfolio"]},
]

# Simulated historical interactions: (user_id, course_id, rating 1-5)
SEED_INTERACTIONS = [
    ("u001", "c001", 5), ("u001", "c002", 4), ("u001", "c003", 5), ("u001", "c004", 5), ("u001", "c005", 3),
    ("u002", "c001", 4), ("u002", "c009", 5), ("u002", "c014", 4), ("u002", "c002", 3), ("u002", "c012", 4),
    ("u003", "c006", 5), ("u003", "c007", 5), ("u003", "c008", 4), ("u003", "c005", 4), ("u003", "c012", 3),
    ("u004", "c010", 5), ("u004", "c011", 4), ("u004", "c003", 3), ("u004", "c013", 5), ("u004", "c015", 4),
    ("u005", "c001", 3), ("u005", "c004", 4), ("u005", "c006", 5), ("u005", "c007", 5), ("u005", "c008", 5),
    ("u006", "c009", 5), ("u006", "c014", 5), ("u006", "c002", 4), ("u006", "c012", 5), ("u006", "c005", 3),
    ("u007", "c003", 5), ("u007", "c004", 5), ("u007", "c005", 4), ("u007", "c006", 3), ("u007", "c013", 4),
    ("u008", "c010", 4), ("u008", "c011", 5), ("u008", "c015", 5), ("u008", "c013", 4), ("u008", "c001", 3),
    ("u009", "c008", 5), ("u009", "c006", 4), ("u009", "c007", 5), ("u009", "c012", 4), ("u009", "c005", 5),
    ("u010", "c001", 5), ("u010", "c002", 5), ("u010", "c009", 4), ("u010", "c014", 3), ("u010", "c015", 4),
]
