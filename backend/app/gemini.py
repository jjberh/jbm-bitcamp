import os
import requests
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_URL = os.getenv("GEMINI_API_URL")  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_meal_recommendation(user_data):
    """
  
    user_data: dict expected to have either:
       - "macros": { "protein": value, "carbs": value, "fats": value }
       OR
       - "height", "weight", "age", "goal" (e.g., "lose" or "gain")
    """
    
    if "macros" in user_data:
        # Use the provided macros
        macros = user_data["macros"]
        prompt = (
            f"I am planning my meals and I have these daily macro goals: "
            f"Protein: {macros.get('protein', 'N/A')}, Carbs: {macros.get('carbs', 'N/A')}, "
            f"Fats: {macros.get('fats', 'N/A')}. Please suggest one or more meal options from a school dining hall that "
            f"match these macros, including an approximate nutritional breakdown for each meal."
        )
    elif all(key in user_data for key in ["height", "weight", "age", "goal"]):
        # Use physical info to calculate daily macros and then provide meal suggestions.
        height = user_data["height"]
        weight = user_data["weight"]
        age = user_data["age"]
        goal = user_data["goal"]
        prompt = (
            f"I don't have my daily macros. Based on my details: Height: {height} cm, Weight: {weight} kg, "
            f"Age: {age}, and my goal to {goal} weight, please calculate my recommended daily macros and "
            f"then suggest one or more meal options available at a school dining hall that meet these macros. "
            f"Include an approximate nutritional breakdown for each meal option."
        )
    else:
        return "Insufficient data provided. Please provide either daily macros or your physical details (height, weight, age, goal)."
    
    
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
   
    payload = {
        "prompt": {
            "text": prompt
        }
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Gemini will typically returns a candidates list, We extract the first candidate.
        
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0].get("output", "No 'output' field found.")
        else:
            return "No candidates returned."
    except requests.RequestException as e:
        print(f"Error contacting Gemini API: {e}")
        return "An error occurred while contacting the Gemini API."
