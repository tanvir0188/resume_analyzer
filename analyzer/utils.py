import os
import re
from PyPDF2 import PdfReader
from docx import Document
import spacy
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP models once (global)
nlp = spacy.load("en_core_web_sm")

def extract_text(file_path):
  ext = os.path.splitext(file_path)[1].lower()
  text = ""
  if ext == '.pdf':
    reader = PdfReader(file_path)
    for page in reader.pages:
      page_text = page.extract_text()
      if page_text:
        text += page_text + "\n"
  elif ext in ['.doc', '.docx']:
    doc = Document(file_path)
    for para in doc.paragraphs:
      text += para.text + "\n"
  doc = nlp(text)

  names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
  emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
  phones = re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", text)
  orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
  gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
  skills = [chunk.text for chunk in doc.noun_chunks if chunk.root.dep_ == "pobj"]
  
  return {
    "raw_text": text,
    "names": names,
    "emails": emails,
    "phones": phones,
    "organizations": orgs,
    "locations": gpes,
    "skills": skills,
  }
