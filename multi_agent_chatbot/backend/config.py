import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

if not OPENAI_API_KEY:
    # We'll allow it for now but it should be set in production
    print("Warning: OPENAI_API_KEY not set.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
