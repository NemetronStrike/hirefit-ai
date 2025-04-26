import os
from dotenv import load_dotenv
import google.generativeai as genai

# 🔒 Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔧 Set up Gemini configuration
genai.configure(api_key=GEMINI_API_KEY)

# 🤖 Models
model_flash = genai.GenerativeModel("gemini-2.0-flash")  # For analysis (Flash is faster)

# 🔍 Resume-JD Analysis
def get_structured_analysis(resume, jd):
    prompt = f"""
You are an expert AI assistant for resume evaluation. Given the RESUME and JOB DESCRIPTION below, provide a clear, structured response in the following format (using the same headings):

Match Percentage:
[Only numeric value as percentage]

Strengths:
- [List strengths based on JD]

Weaknesses:
- [List weaknesses or missing aspects]

Conclusion:
[Give a 2-3 line summary of overall alignment]

Resume:
{resume}

Job Description:
{jd}
"""
    response = model_flash.generate_content(prompt)
    return response.text

# 🧩 Resume Generator
def generate_resume_from_prompt(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro")  # Use gemini-1.5-pro for resume generation
    response = model.generate_content(prompt)
    return response.text
