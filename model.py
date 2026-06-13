from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import re


# ---------------- TEXT EXTRACTION ----------------
def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text

    else:
        with open(file_path, "r", errors="ignore") as f:
            text = f.read()

    return text.lower()


# ---------------- SKILLS ----------------
SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "sql", "html", "css", "javascript", "react", "node.js",
    "flask", "django", "aws", "docker", "kubernetes",
    "pandas", "numpy", "tensorflow", "pytorch",
    "git", "github", "postgresql", "rest apis", "microservices"
]


# ---------------- CLEAN ----------------
def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\.\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    return list(set([skill for skill in SKILLS if skill in text]))


# ---------------- SKILL SCORE ----------------
def skill_match(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    if len(jd_skills) == 0:
        return 0

    return len(set(resume_skills) & set(jd_skills)) / len(jd_skills)


# ---------------- MAIN ML FUNCTION ----------------
def process_resume(job_desc, resume_text):

    resume_text = clean(resume_text)
    job_desc = clean(job_desc)

    # safety check (IMPORTANT)
    if len(resume_text) < 5 or len(job_desc) < 5:
        return {
            "score": 0,
            "tfidf_score": 0,
            "skill_score": 0,
            "matched": [],
            "missing": []
        }

    documents = [job_desc, resume_text]

    tfidf = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=8000
    )

    matrix = tfidf.fit_transform(documents)

    tfidf_score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    matched = list(set(extract_skills(resume_text)) & set(extract_skills(job_desc)))
    missing = list(set(extract_skills(job_desc)) - set(extract_skills(resume_text)))

    skill_score = skill_match(resume_text, job_desc)

    final_score = (0.7 * tfidf_score) + (0.3 * skill_score)

    return {
        "score": round(final_score * 100, 2),
        "tfidf_score": round(tfidf_score * 100, 2),
        "skill_score": round(skill_score * 100, 2),
        "matched": matched,
        "missing": missing
    }