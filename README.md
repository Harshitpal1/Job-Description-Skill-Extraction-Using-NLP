# Job Description Skill Extraction Using NLP

An NLP-based application that automatically extracts, normalizes, and categorizes technical skills from job descriptions. The project also provides resume-based candidate skill matching, MySQL search history, and Power BI analytics.

## Project Overview

Job descriptions contain important technical requirements in unstructured text, making manual skill identification time-consuming. This project uses Natural Language Processing and Machine Learning techniques to identify technical skills and convert them into structured information.

## Features

- Job Description Skill Extraction
- Skill Normalization and Categorization
- Dictionary and Regex-based Matching
- TF-IDF and N-Gram Analysis
- Named Entity Recognition (NER)
- Machine Learning-based Skill Classification
- Transformer-based Skill Extraction
- Resume Upload and Skill Extraction
- Candidate Skill Matching
- Matched and Missing Skills
- Skill-based Match Percentage
- MySQL Search History
- Power BI Dashboard
- Streamlit Web Application

## Technologies Used

Python, Pandas, NumPy, NLTK, spaCy, Scikit-learn, Transformers, Streamlit, MySQL, Power BI, Joblib, Git and GitHub.

## Dataset

The project uses a job-description dataset containing 10,100+ job records with information such as job title, company, location, job description, experience, education, salary, and job type.

After processing and skill extraction, a structured skill-level dataset containing 34,757 skill records was generated.

## Skill Categories

The extracted skills are organized into categories including Programming, Database, Data Science, Machine Learning, Cloud, BI/Analytics, Big Data, DevOps, and Version Control.

## NLP Approaches

Multiple approaches were implemented and compared:

1. Dictionary-Based Matching
2. Regex-Based Matching
3. TF-IDF
4. N-Grams
5. Named Entity Recognition (NER)
6. Machine Learning
7. Transformer-Based NLP

## System Workflow

Job Description → Text Preprocessing → Skill Extraction → Skill Normalization → Category Mapping → Final Skills → Candidate Matching / Analytics

## Streamlit Application

The Streamlit application provides an interactive interface where users can enter a job description, extract technical skills, view their categories, upload resumes, and compare candidate skills with job requirements.

The application also provides recent search history through MySQL integration.

## Candidate Matching

The candidate matching feature compares technical skills extracted from a resume with skills identified from a job description. It provides matched skills, missing skills, and a skill-based match percentage.

The matching score is intended as an initial technical-skill screening indicator and does not represent a complete hiring decision.

## Power BI Dashboard

The Power BI dashboard provides recruitment-oriented insights including total jobs, unique skills, top skills, top job roles, skill demand by job role, and skill category distribution.

## Model Evaluation

The different approaches were evaluated using Precision, Recall, F1-Score, Accuracy, and Confusion Matrix. The evaluation results are specific to the project's dataset and evaluation methodology.

## Installation

```bash
git clone https://github.com/Harshitpal1/Job-Description-Skill-Extraction-Using-NLP.git
cd Job-Description-Skill-Extraction-Using-NLP
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

## MySQL Setup

Create the required database:

```sql
CREATE DATABASE job_skill_extractor;
```

The application uses MySQL to store recent search information such as job descriptions, detected skills, and timestamps.

For security, database credentials should be stored using environment variables or Streamlit secrets rather than directly in the source code.

## Future Scope

Future improvements may include advanced resume-job matching, candidate ranking, skill-gap analysis, personalized learning recommendations, job recommendations, an expanded skill taxonomy, and improved domain-specific Transformer models.

## Demo
To try out the Job Skill Extractor model, visit [here](https://job-skill-extractor.streamlit.app/).

## Author

**Harshit Pal**

GitHub: https://github.com/Harshitpal1/Job-Description-Skill-Extraction-Using-NLP

## License

This project is developed for educational and internship purposes.
