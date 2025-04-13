from flask import Blueprint, request, jsonify, current_app
from app import gemini

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

        return jsonify(result.user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@url.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    
    #if request.method == "POST":
        #data = request.json
        #pass
        #current_app.supabase.table("")
    
    #elif request.method == "GET":
        #pass
    return "dashboard"

@url.route("/users", strict_slashes=False)
def users():
    response = (
        current_app.supabase.table("users").select("*").execute()
    )

    return response.data

@url.route("/login", methods=["POST"])
def login():
    data = request.json
    id = data.get("id")
    password = data.get("password")

    if not id or not password:
        return jsonify({"Missing email/username, or password"}), 400
    

    # using username to login
    if "@" not in id: 
        response = current_app.supabase.table("users").select("email").eq("username", id).execute()

        if response.data:
            id = response.data[0]["email"]
        else:
            return jsonify({"Error": "Username not found"}), 404
    
    # proceed with login
    try:
        result = current_app.supabase.auth.sign_in_with_password({
            "email": id,
            "password": password
        })
        return jsonify(result.user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@url.route("/recommend-meals", methods=["POST"])
def recommend_meals():
    
    user_data = request.json or {}
    recommendation = gemini.get_meal_recommendation(user_data)
    return jsonify({"recommendation": recommendation}), 200