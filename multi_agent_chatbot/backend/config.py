import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-1.5-flash"

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not set.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

def get_model(system_instruction: str):
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL_NAME,
        system_instruction=system_instruction
    )
