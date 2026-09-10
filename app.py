# ============================================================
# JOB DESCRIPTION SKILL EXTRACTION APPLICATION
# ============================================================

import streamlit as st
import joblib
import os
from pypdf import PdfReader
from docx import Document
import mysql.connector


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Job Skill Extractor",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="6057",
        database="job_skill_extractor"
    )


# ============================================================
# SAVE SEARCH TO DATABASE
# ============================================================

def save_search_to_database(job_description, skills):

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        skills_text = ", ".join(skills)

        query = """
        INSERT INTO recent_searches
        (job_description, detected_skills)
        VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (job_description, skills_text)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    except Exception as e:

        st.error(f"Database Error: {e}")

        return False


# ============================================================
# LOAD ML MODEL
# ============================================================

MODEL_PATH = "model/skill_classifier.pkl"

if os.path.exists(MODEL_PATH):

    ml_model = joblib.load(MODEL_PATH)

else:

    ml_model = None


# ============================================================
# SKILL DICTIONARY
# ============================================================

skill_dictionary = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "power bi",
    "tableau",
    "excel",

    "pandas",
    "numpy",

    "scikit-learn",
    "tensorflow",
    "pytorch",

    "machine learning",
    "deep learning",
    "natural language processing",

    "aws",
    "azure",
    "gcp",

    "spark",
    "hadoop",

    "docker",
    "kubernetes",

    "git"
]


# ============================================================
# SKILL CATEGORIES
# ============================================================

skill_categories = {

    "python": "Programming",
    "java": "Programming",
    "c++": "Programming",
    "javascript": "Programming",
    "typescript": "Programming",

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

    "machine learning": "Machine Learning",
    "deep learning": "Machine Learning",
    "natural language processing": "Machine Learning",

    "aws": "Cloud",
    "azure": "Cloud",
    "gcp": "Cloud",

    "spark": "Big Data",
    "hadoop": "Big Data",

    "docker": "DevOps",
    "kubernetes": "DevOps",

    "git": "Version Control"
}


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    text_lower = text.lower()

    detected_skills = []

    for skill in skill_dictionary:

        if skill in text_lower:

            # Use ML model if available
            if ml_model is not None:

                try:

                    prediction = ml_model.predict(
                        [skill]
                    )[0]

                    if prediction in [
                        "SKILL",
                        "CLOUD",
                        "DATABASE",
                        "BI_TOOL",
                        "TECHNOLOGY"
                    ]:

                        detected_skills.append(skill)

                except Exception:

                    # Fallback to dictionary matching
                    detected_skills.append(skill)

            else:

                # Fallback if model is not available
                detected_skills.append(skill)

    return sorted(set(detected_skills))


# ============================================================
# READ RESUME
# ============================================================

def read_resume(uploaded_file):

    file_name = uploaded_file.name.lower()

    # TXT
    if file_name.endswith(".txt"):

        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    # PDF
    elif file_name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

        return text

    # DOCX
    elif file_name.endswith(".docx"):

        document = Document(uploaded_file)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text

    return ""


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.title("🎯 Job Skill Extractor")

    st.subheader(
        "Streamline your technical recruiting with NLP & Machine Learning."
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        ["Login", "Sign Up"]
    )

    # -------------------------
    # LOGIN
    # -------------------------

    with login_tab:

        st.header("Welcome Back")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Log In",
            use_container_width=True,
            key="login_button"
        ):

            if email.strip() and password.strip():

                st.session_state.logged_in = True
                st.session_state.page = "dashboard"

                st.rerun()

            else:

                st.warning(
                    "Please enter email and password."
                )

    # -------------------------
    # SIGN UP
    # -------------------------

    with signup_tab:

        st.header("Create Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="signup_name"
        )

        new_email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True,
            key="signup_button"
        ):

            if (
                name.strip()
                and new_email.strip()
                and new_password.strip()
            ):

                st.success(
                    "Account created successfully!"
                )

            else:

                st.warning(
                    "Please fill all fields."
                )


# ============================================================
# SIDEBAR
# ============================================================

def show_sidebar():

    with st.sidebar:

        st.title("⚙️ Workspace")

        st.write("Welcome back! 👋")

        st.divider()

        if st.button(
            "🔍 Skill Extractor",
            use_container_width=True,
            key="nav_extractor"
        ):

            st.session_state.page = "extractor"

            st.rerun()

        if st.button(
            "🎯 Candidate Matching",
            use_container_width=True,
            key="nav_matching"
        ):

            st.session_state.page = "matching"

            st.rerun()

        if st.button(
            "🕘 Recent Searches",
            use_container_width=True,
            key="nav_recent"
        ):

            st.session_state.page = "recent"

            st.rerun()

        st.divider()

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            key="nav_dashboard"
        ):

            st.session_state.page = "dashboard"

            st.rerun()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="nav_logout"
        ):

            st.session_state.logged_in = False
            st.session_state.page = "login"

            st.rerun()


# ============================================================
# DASHBOARD DATABASE STATISTICS
# ============================================================

def get_dashboard_stats():

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        # Total searches
        cursor.execute(
            "SELECT COUNT(*) FROM recent_searches"
        )

        total_jobs = cursor.fetchone()[0]

        # Total detected skills
        cursor.execute(
            """
            SELECT detected_skills
            FROM recent_searches
            """
        )

        rows = cursor.fetchall()

        all_skills = []

        for row in rows:

            if row[0]:

                skills = [
                    skill.strip().lower()
                    for skill in row[0].split(",")
                    if skill.strip()
                ]

                all_skills.extend(skills)

        unique_skills = len(set(all_skills))

        cursor.close()
        connection.close()

        return total_jobs, unique_skills

    except Exception as e:

        st.error(f"Database Error: {e}")

        return 0, 0


# ============================================================
# GET SKILL STATISTICS
# ============================================================

def get_skill_statistics():

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT detected_skills FROM recent_searches"
        )

        rows = cursor.fetchall()

        skill_counts = {}

        for row in rows:

            if row[0]:

                skills = [
                    skill.strip().lower()
                    for skill in row[0].split(",")
                    if skill.strip()
                ]

                for skill in skills:

                    skill_counts[skill] = (
                        skill_counts.get(skill, 0) + 1
                    )

        cursor.close()
        connection.close()

        return skill_counts

    except Exception as e:

        st.error(f"Database Error: {e}")

        return {}


# ============================================================
# GET SKILL CATEGORY STATISTICS
# ============================================================

def get_category_statistics():

    category_mapping = {

        "python": "Programming",
        "java": "Programming",
        "c++": "Programming",
        "javascript": "Programming",
        "typescript": "Programming",

        "sql": "Database",
        "mysql": "Database",
        "postgresql": "Database",
        "mongodb": "Database",

        "power bi": "BI / Analytics",
        "tableau": "BI / Analytics",
        "excel": "BI / Analytics",

        "pandas": "Data Science",
        "numpy": "Data Science",

        "scikit-learn": "Machine Learning",
        "tensorflow": "Machine Learning",
        "pytorch": "Machine Learning",
        "machine learning": "Machine Learning",
        "deep learning": "Machine Learning",
        "natural language processing": "Machine Learning",

        "aws": "Cloud",
        "azure": "Cloud",
        "gcp": "Cloud",

        "spark": "Big Data",
        "hadoop": "Big Data",

        "docker": "DevOps",
        "kubernetes": "DevOps",

        "git": "Version Control"
    }

    skill_counts = get_skill_statistics()

    category_counts = {}

    for skill, count in skill_counts.items():

        category = category_mapping.get(
            skill.lower(),
            "Other"
        )

        category_counts[category] = (
            category_counts.get(category, 0) + count
        )

    return category_counts


# ============================================================
# DASHBOARD PAGE
# ============================================================

def dashboard_page():

    total_jobs, unique_skills = get_dashboard_stats()

    skill_counts = get_skill_statistics()

    category_counts = get_category_statistics()

    st.title("🎯 Job Skill Extractor")

    st.subheader(
        "Extract, classify and analyze technical skills from job descriptions."
    )

    st.divider()

    # -------------------------
    # KPI METRICS
    # -------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Jobs Analyzed",
            total_jobs
        )

    with col2:

        st.metric(
            "Skills Extracted",
            unique_skills
        )

    with col3:

        st.metric(
            "Model Status",
            "Ready"
        )

    st.divider()

    # -------------------------
    # TOP SKILLS
    # -------------------------

    st.subheader("📊 Top Skills")

    if skill_counts:

        top_skills = sorted(
            skill_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        for skill, count in top_skills:

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    skill.title()
                )

            with col2:

                st.write(
                    f"**{count}**"
                )

    else:

        st.info(
            "No skill data available yet."
        )

    st.divider()

    # -------------------------
    # CATEGORY DISTRIBUTION
    # -------------------------

    st.subheader(
        "📂 Skill Category Distribution"
    )

    if category_counts:

        category_data = {

            "Category":
                list(category_counts.keys()),

            "Count":
                list(category_counts.values())
        }

        st.bar_chart(
            category_data,
            x="Category",
            y="Count"
        )

    else:

        st.info(
            "No category data available yet."
        )

    st.divider()

    st.info(
        "Choose a feature from the sidebar to get started."
    )


# ============================================================
# SKILL EXTRACTOR PAGE
# ============================================================

def extractor_page():

    st.title("🔍 Job Skill Extraction")

    st.write(
        "Paste a job description to automatically detect and classify technical skills."
    )

    st.divider()

    job_description = st.text_area(
        "📝 Job Description",
        height=200,
        placeholder=(
            "Looking for Data Analyst with SQL, Python, "
            "Power BI and Excel experience."
        ),
        key="job_description"
    )

    if st.button(
        "🔍 Extract & Classify Skills",
        key="extract_button"
    ):

        if not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

            return

        # -------------------------
        # Extract skills
        # -------------------------

        skills = extract_skills(
            job_description
        )

        # -------------------------
        # Save to MySQL ONCE
        # -------------------------

        save_search_to_database(
            job_description,
            skills
        )

        # -------------------------
        # Save to session
        # -------------------------

        st.session_state.recent_searches.insert(
            0,
            {
                "job_description":
                    job_description,

                "skills":
                    skills
            }
        )

        st.session_state.recent_searches = (
            st.session_state.recent_searches[:10]
        )

        # -------------------------
        # Check result
        # -------------------------

        if len(skills) == 0:

            st.warning(
                "No known technical skills were detected."
            )

            return

        # -------------------------
        # Success message
        # -------------------------

        st.success(
            "✅ Analysis Complete!"
        )

        st.subheader(
            "🎯 Detected Skills"
        )

        # -------------------------
        # Create result data
        # -------------------------

        results = []

        for skill in skills:

            category = skill_categories.get(
                skill,
                "Other"
            )

            results.append(
                {
                    "Detected Skill":
                        skill.title(),

                    "Category":
                        category
                }
            )

        # -------------------------
        # Display result
        # -------------------------

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------
        # Skill Summary
        # -------------------------

        st.subheader(
            "📊 Skill Summary"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Skills Detected",
                len(skills)
            )

        with col2:

            categories = set(
                skill_categories.get(
                    skill,
                    "Other"
                )
                for skill in skills
            )

            st.metric(
                "Categories",
                len(categories)
            )

        # -------------------------
        # Category Mapping
        # -------------------------

        st.subheader(
            "🏷️ Category Mapping"
        )

        for skill in skills:

            category = skill_categories.get(
                skill,
                "Other"
            )

            st.write(
                f"**{skill.title()}** → `{category}`"
            )


# ============================================================
# CANDIDATE MATCHING PAGE
# ============================================================

def matching_page():

    st.title(
        "🎯 Candidate Match Scoring"
    )

    st.write(
        "Compare candidate skills with the skills required in a job description."
    )

    st.divider()

    # -------------------------
    # Job Description
    # -------------------------

    job_description = st.text_area(
        "📋 Job Description",
        height=180,
        placeholder=(
            "Example: Looking for a Data Analyst with "
            "Python, SQL, Power BI and Excel experience."
        ),
        key="matching_job_description"
    )

    # -------------------------
    # Resume upload
    # -------------------------

    uploaded_file = st.file_uploader(
        "📄 Upload Candidate Resume",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        key="candidate_resume"
    )

    if st.button(
        "🎯 Calculate Match Score",
        use_container_width=True,
        key="calculate_match"
    ):

        if not job_description.strip():

            st.warning(
                "Please enter a job description."
            )

            return

        if uploaded_file is None:

            st.warning(
                "Please upload a resume."
            )

            return

        # -------------------------
        # Read resume
        # -------------------------

        resume_text = read_resume(
            uploaded_file
        )

        # -------------------------
        # Extract skills
        # -------------------------

        job_skills = extract_skills(
            job_description
        )

        resume_skills = extract_skills(
            resume_text
        )

        # -------------------------
        # Convert to sets
        # -------------------------

        job_skill_set = set(
            job_skills
        )

        resume_skill_set = set(
            resume_skills
        )

        if not job_skill_set:

            st.warning(
                "No known technical skills were detected "
                "in the job description."
            )

            return

        # -------------------------
        # Matching skills
        # -------------------------

        matched_skills = (
            job_skill_set
            .intersection(
                resume_skill_set
            )
        )

        # -------------------------
        # Missing skills
        # -------------------------

        missing_skills = (
            job_skill_set
            - resume_skill_set
        )

        # -------------------------
        # Calculate percentage
        # -------------------------

        match_score = (
            len(matched_skills)
            / len(job_skill_set)
        ) * 100

        st.success(
            "✅ Match Analysis Complete!"
        )

        st.divider()

        # -------------------------
        # Score
        # -------------------------

        st.subheader(
            "📊 Candidate Match Score"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Match Score",
                f"{match_score:.1f}%"
            )

        with col2:

            st.metric(
                "Matched Skills",
                len(matched_skills)
            )

        with col3:

            st.metric(
                "Missing Skills",
                len(missing_skills)
            )

        # Progress bar
        st.progress(
            min(int(match_score), 100)
        )

        # Match message
        if match_score >= 80:

            st.success(
                "Excellent match! This candidate has most of the required skills."
            )

        elif match_score >= 60:

            st.warning(
                "Good match, but some required skills are missing."
            )

        else:

            st.error(
                "Low match. The candidate may need additional skills."
            )

        st.divider()

        # -------------------------
        # Matched skills
        # -------------------------

        st.subheader(
            "✅ Matched Skills"
        )

        if matched_skills:

            for skill in sorted(
                matched_skills
            ):

                category = skill_categories.get(
                    skill,
                    "Other"
                )

                st.write(
                    f"🟢 **{skill.title()}** → `{category}`"
                )

        else:

            st.write(
                "No matching skills found."
            )

        # -------------------------
        # Missing skills
        # -------------------------

        st.subheader(
            "❌ Missing Skills"
        )

        if missing_skills:

            for skill in sorted(
                missing_skills
            ):

                category = skill_categories.get(
                    skill,
                    "Other"
                )

                st.write(
                    f"🔴 **{skill.title()}** → `{category}`"
                )

        else:

            st.success(
                "Candidate has all required skills!"
            )


# ============================================================
# RECENT SEARCHES PAGE
# ============================================================

def recent_searches_page():

    st.title(
        "🕘 Recent Searches"
    )

    st.write(
        "View your recently analyzed job descriptions and extracted skills."
    )

    st.divider()

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT
            id,
            job_description,
            detected_skills,
            created_at
        FROM recent_searches
        ORDER BY created_at DESC
        LIMIT 10
        """

        cursor.execute(
            query
        )

        searches = cursor.fetchall()

        cursor.close()
        connection.close()

        if not searches:

            st.info(
                "No recent searches yet. "
                "Analyze a job description first."
            )

            return

        for search in searches:

            skills = (
                search["detected_skills"]
                or ""
            )

            skill_list = [

                skill.strip()

                for skill in skills.split(",")

                if skill.strip()
            ]

            with st.expander(
                f"Search #{search['id']} — "
                f"{len(skill_list)} skills detected"
            ):

                st.write(
                    "**Job Description:**"
                )

                st.write(
                    search["job_description"]
                )

                st.write(
                    "**Detected Skills:**"
                )

                if skill_list:

                    skill_text = ", ".join(

                        skill.title()

                        for skill in skill_list
                    )

                    st.success(
                        skill_text
                    )

                else:

                    st.write(
                        "No technical skills detected."
                    )

                st.caption(
                    f"Analyzed on: "
                    f"{search['created_at']}"
                )

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

if not st.session_state.logged_in:

    login_page()

else:

    show_sidebar()

    if st.session_state.page == "dashboard":

        dashboard_page()

    elif st.session_state.page == "extractor":

        extractor_page()

    elif st.session_state.page == "matching":

        matching_page()

    elif st.session_state.page == "recent":

        recent_searches_page()