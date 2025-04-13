import os

import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_meal_recommendation(prompt_text):
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    payload = {
        "prompt": {
            "text": prompt_text
        }
    }
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    candidates = data.get("candidates", [])
    if candidates:
        return candidates[0].get("output", "No 'output' field found.")
    return "No candidates returned."
