import os
import requests
from dotenv import load_dotenv

load_dotenv()

TERPALERT_BASE_URL = os.getenv("TERPALERT_BASE_URL")  

def get_dining_meals():
    endpoint = "/meals"  # Update this according to the API spec
    url = f"{TERPALERT_BASE_URL}{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  
        
        return data  
    except requests.RequestException as e:
        print(f"Error fetching dining meals: {e}")
        return None
