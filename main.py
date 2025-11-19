from fastapi import FastAPI, UploadFile, File
import PyPDF2
import re
import openai
import os

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI(title="Resume Parser API")

# -----------------------------
# Set OpenAI API key (environment variable recommended)
# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# Resume parsing function
# -----------------------------
def parse_resume(file) -> dict:
    # Read PDF
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Extract Email
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email = re.findall(email_pattern, text)

    # Extract Phone (Indian numbers)
    phone_pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"
    phone = re.findall(phone_pattern, text)

    # Extract Name (first line assumption)
    lines = text.split("\n")
    name = lines[0].strip()

    # Extract Skills (basic keyword matching)
    skill_keywords = [
        "python","java","c++","sql","html","css","javascript","fastapi","django",
        "ml","machine learning","ai","react","php","flutter","data science"
    ]
    found_skills = []
    lower_text = text.lower()
    for skill in skill_keywords:
        if skill in lower_text:
            found_skills.append(skill)

    # Optional: Use OpenAI to refine skills
    # Uncomment below if you want AI skill extraction
    """
    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user", "content": f"Extract skills from this resume text: {text}"}]
    )
    ai_skills = response.choices[0].message.content
    found_skills = [s.strip() for s in ai_skills.split(",")]
    """

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills
    }

# -----------------------------
# API Endpoint: Upload Resume
# -----------------------------
@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    parsed_data = parse_resume(file.file)
    return parsed_data
