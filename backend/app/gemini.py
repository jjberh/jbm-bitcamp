# gemini.py

import os
import requests
from dotenv import load_dotenv
from dining import get_dining_meals  # Import the dining hall function

load_dotenv()

GEMINI_API_URL = os.getenv("GEMINI_API_URL")  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_meal_recommendation(user_data):
    """
    Build a Gemini prompt that includes the dining hall meal data.
    Depending on user_data, use provided macros or physical details to calculate macros.
    
    user_data should be a dictionary containing either:
      - "macros": {"protein": value, "carbs": value, "fats": value}
    or
      - "height", "weight", "age", "goal" (e.g., "lose" or "gain")
    """
    
    # Fetches from dining hall meal data from TerpAlert API
    dining_data = get_dining_meals()
    dining_summary = ""
    
    if dining_data:
        #Assumes dining_data contains a list of meals under a key "meals"
        meal_summaries = []
        for meal in dining_data.get('meals', []):
            #Need to Adjust field names to match the API response.
            name = meal.get('name', 'Unknown Meal')
            nutrition = meal.get('nutrition', {})
            protein = nutrition.get('protein', 'N/A')
            carbs = nutrition.get('carbs', 'N/A')
            fats = nutrition.get('fats', 'N/A')
            meal_summaries.append(f"{name} (P:{protein}g, C:{carbs}g, F:{fats}g)")
        dining_summary = "\n".join(meal_summaries)
    else:
        dining_summary = "No dining hall data available."

    # the prompt depending on if we have the macros or not
    if "macros" in user_data:
        macros = user_data["macros"]
        prompt = (
            f"I need meal recommendations based on these daily macro goals: "
            f"Protein: {macros.get('protein')}, Carbs: {macros.get('carbs')}, Fats: {macros.get('fats')}. "
            "Below are some dining hall meals and their nutritional details:\n"
            f"{dining_summary}\n"
            "Please suggest one or more meal options that best meet these macro goals."
        )
    elif all(key in user_data for key in ["height", "weight", "age", "goal"]):
        height = user_data["height"]
        weight = user_data["weight"]
        age = user_data["age"]
        goal = user_data["goal"]
        prompt = (
            f"I don't have my daily macros. Based on my details (Height: {height} cm, Weight: {weight} kg, Age: {age}, Goal: {goal}), "
            "please calculate my recommended daily macros. "
            "Below are some dining hall meals and their nutritional details:\n"
            f"{dining_summary}\n"
            "Then suggest one or more meal options available that match these macros."
        )
    else:
        return "Insufficient data provided. Please provide either daily macros or your physical details (height, weight, age, goal)."
    
    #Builds the full Gemini API URL with the API key
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    #Creates the payload according to Gemini's API requirements.
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
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0].get("output", "No 'output' field found.")
        return "No candidates returned."
    except requests.RequestException as e:
        print(f"Error contacting Gemini API: {e}")
        return "An error occurred while contacting the Gemini API."
