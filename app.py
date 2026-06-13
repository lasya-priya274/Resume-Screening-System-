from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

from model import extract_text, process_resume
from utils import clean_text

app = Flask(__name__)

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'change-this-key'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HELPERS ----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def boost_jd(text):
    keywords = [
        "python", "flask", "django", "rest apis",
        "sql", "postgresql", "git", "github",
        "docker", "aws", "microservices"
    ]
    for word in keywords:
        text += " " + (word + " ") * 2
    return text


# ---------------- ROUTES ----------------
@app.route("/view/<filename>")
def view_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- MAIN ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":

        job_description = request.form.get("job_description", "").strip()

        if not job_description:
            flash("Please enter job description", "danger")
            return redirect(url_for("index"))

        job_desc = clean_text(job_description)
        job_desc = boost_jd(job_desc)

        files = request.files.getlist("resumes")

        if not files or files[0].filename == "":
            flash("Please upload resumes", "danger")
            return redirect(url_for("index"))

        for file in files:
            if file and allowed_file(file.filename):

                try:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    file.save(filepath)

                    resume_text = extract_text(filepath)
                    resume_text = clean_text(resume_text)

                    data = process_resume(job_desc, resume_text)

                    results.append({
                        "name": filename,
                        "score": data["score"],
                        "matched": data["matched"],
                        "missing": data["missing"]
                    })

                except Exception as e:
                    flash(f"Error processing {file.filename}: {str(e)}", "danger")

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        if not results:
            flash("No valid resumes processed", "warning")

    return render_template("index.html", results=results)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)