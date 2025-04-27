import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

# 🔒 Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔧 Set up Gemini configuration
genai.configure(api_key=GEMINI_API_KEY)

# 🤖 Models
model_flash = genai.GenerativeModel("gemini-2.0-flash")  # For analysis (Flash is faster)
model_pro = genai.GenerativeModel("gemini-1.5-pro")      # For resume generation

# ⚡ Quick Summarizer
async def quick_summarize_async(text: str, type: str = "resume") -> str:
    summarization_prompt = f"""
You are a skilled summarizer AI. Summarize the following {type} by extracting ONLY:
- Key skills
- Important experiences
- Major highlights

Keep the summary concise (under 300 words).

--- Text ---
{text}
"""
    try:
        response = model_flash.generate_content(summarization_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error summarizing {type}: {e}"

# 🔍 Resume-JD Analysis
async def get_structured_analysis_async(resume: str, jd: str) -> str:
    try:
        # ⚡ First, summarize both to speed up
        resume_summary = await quick_summarize_async(resume, type="resume")
        jd_summary = await quick_summarize_async(jd, type="job description")
        
        # 🔥 Limit summarized text
        max_resume_tokens = 2000
        max_jd_tokens = 1000
        resume_summary = resume_summary[:max_resume_tokens]
        jd_summary = jd_summary[:max_jd_tokens]
        
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
{resume_summary}

Job Description:
{jd_summary}
"""
        response = model_flash.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing resume and JD: {e}"

# 🧩 Resume Generator
async def generate_resume_from_prompt_async(prompt: str) -> str:
    try:
        response = model_pro.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating resume: {e}"
