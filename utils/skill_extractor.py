skill_dictionary = [
    "python", "java", "c++", "javascript",
    "sql", "mysql", "postgresql", "mongodb",
    "power bi", "tableau", "excel",
    "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch",
    "aws", "azure", "gcp",
    "spark", "hadoop",
    "docker", "kubernetes", "git"
]

skill_categories = {
    "python": "Programming",
    "java": "Programming",
    "c++": "Programming",
    "javascript": "Programming",
    "sql": "Database",
    "mysql": "Database",
    "postgresql": "Database",
    "mongodb": "Database",
    "power bi": "BI",
    "tableau": "BI",
    "excel": "Analytics",
    "pandas": "Data Science",
    "numpy": "Data Science",
    "scikit-learn": "Machine Learning",
    "tensorflow": "Machine Learning",
    "pytorch": "Machine Learning",
    "aws": "Cloud",
    "azure": "Cloud",
    "gcp": "Cloud",
    "spark": "Big Data",
    "hadoop": "Big Data",
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "git": "Version Control"
}

def extract_skills(text):
    text = text.lower()
    detected_skills = []

    for skill in skill_dictionary:
        if skill in text:
            detected_skills.append(skill)

    return detected_skills