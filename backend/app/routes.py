from flask import Blueprint, request, jsonify, current_app
from app.gemini import *

url = Blueprint("url", __name__)

@url.route("/")
def main():
    return "Hello"

@url.route("/signup", methods = ["POST"])
def signup():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"Missing email, username, or password"}), 400
    
    try:
        result = current_app.supabase.auth.sign_up({

            "email": email,
            "username": username,
            "password": password
            

        })

        current_app.supabase.table("users").insert({"user_id": result.user.id, "username": username, "email": email}).execute()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@url.route("/dashboard")
def dashboard():
    return "dashboard"
    
   
@url.route("/users", strict_slashes=False)
def users():
    response = (
        current_app.supabase.table("users").select("*").execute()
    )

    return response.data


@url.route("/login")
def login():
    return "Logged"

@url.route("/recommend-meals", methods=["POST"])
def recommend_meals():
    
    user_data = request.json or {}
    recommendation = get_meal_recommendation(user_data)
    return jsonify({"recommendation": recommendation}), 200