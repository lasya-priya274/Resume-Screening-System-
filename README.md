# Resume Screening System

An intelligent resume screening system that automates candidate shortlisting by analyzing resumes and matching them with job descriptions using Natural Language Processing (NLP).

## Features

- Upload multiple resumes in PDF, DOC, or DOCX format
- Enter a job description and automatically score candidate resumes
- Compare matched and missing keywords between resumes and job descriptions
- Download or view uploaded resumes directly from the app

## Tech Stack

- Python
- Flask
- NLTK
- scikit-learn
- pandas
- PyPDF2
- python-docx

## Setup

1. Activate the virtual environment:

```powershell
& env\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

4. Open the app in your browser:

```
http://127.0.0.1:5000
```

## Notes

- Make sure `uploads/` is writable by the app.
- If you add new dependencies, update `requirements.txt`.
- For production, use a proper WSGI server instead of the Flask development server.

## Files

- `app.py`: Main Flask application
- `model.py`: Resume parsing and scoring logic
- `utils.py`: Text cleaning utilities
- `templates/`: HTML templates
- `uploads/`: Uploaded resume files
