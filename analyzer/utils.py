import os
import json
from docx import Document
from django.conf import settings
import fitz
from google import genai
from google.genai import types
from django.core.exceptions import ValidationError


GEMINI_API_KEY = settings.GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)


def extract_text(file_path):
  ext = os.path.splitext(file_path)[1].lower()
  text = ""

  if ext == '.pdf':
    doc = fitz.open(file_path)
    for page in doc:
      text += page.get_text() + "\n"
    doc.close()

  elif ext in ['.doc', '.docx']:
    doc = Document(file_path)
    for para in doc.paragraphs:
      text += para.text + "\n"

  return text


prompt_data = """
You are an AI bot designed to act as a professional for parsing resumes. You are given a resume  and your job is to
extract the following information from the resume:

1. applicant_name: ""
2. highest_level_of_education: ""
3. area_of_study: ""
4. institution:""
5. introduction : ""
6. skills: string []
7. english_proficiency_level: ""
8. experiences: [{"employer_name":"", role:"",  duration:""}]

Give the extracted info in JSON format only.
Note: if the info is not present, leave the field blank. If the given text doesn't represent a CV or resume, then return an pdf message in json format only.
message: The extracted text doesn't represent a CV or resume.
"""


def extract_resume_info(text: str):
  try:
    prompt = f"{prompt_data}\n\nResume Content:\n{text.strip()}\n"

    response = client.models.generate_content(
      model="gemini-2.0-flash",
      config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant that extracts structured resume data."
      ),
      contents=prompt
    )

    response_text = response.text

    # Extract valid JSON from the text
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    json_str = response_text[start:end]
    data = json.loads(json_str)

  except Exception as err:
    raise ValidationError(f"Something went wrong: {err}", 500)

  return data


jd_prompt = """
You are an AI bot designed to extract key skills and technologies mentioned in a job description.
Your job is to return a list of concrete skills, tools, or technologies required for the role.

Respond only in JSON format like this:
{ "skills": ["Python", "Django", "REST APIs", "PostgreSQL"] }

Job Description:
"""


def extract_jd_skills(text: str):
  try:
    prompt = f"{jd_prompt}\n{text.strip()}\n"
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      config=types.GenerateContentConfig(
        system_instruction="You extract key skills from job descriptions."
      ),
      contents=prompt
    )
    response_text = response.text
    json_str = response_text[response_text.find("{"):response_text.rfind("}") + 1]
    data = json.loads(json_str)
    return data.get("skills", [])
  except Exception as err:
    raise ValidationError(f"Job description parsing failed: {err}", 500)
