import PyPDF2
import re

with open("Pratiksha_engii.pdf", "rb") as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

# Step 2: Extract Email

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
email = re.findall(email_pattern, text)

# Step 3: Extract Phone Number
phone_pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"
phone = re.findall(phone_pattern, text)

# Step 4: Extract Name (Simple method)
# assuming the first line is name
lines = text.split("\n")
name = lines[0].strip()

# Step 5: Extract Skills
skill_keywords = [
    "python","java","c++","sql","html","css","javascript","fastapi","django",
    "ml","machine learning","ai","react","php","flutter","data science"
]

found_skills = []

lower_text = text.lower()
for skill in skill_keywords:
    if skill in lower_text:
        found_skills.append(skill)

# Step 6: Print all extracted data
print("Name:", name)
print("Email:", email)
print("Phone:", phone)
print("Skills:", found_skills)