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
    
    signup_options = {
            "data": {
                "username": username
            }
        }

    try:
        result = current_app.supabase.auth.sign_up({

            "email": email,
            #"username": username,
            "password": password,
            "options": signup_options
        })

        return jsonify(result.user.id), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@url.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    # Get the current user's session
    session = current_app.supabase.auth.get_session()
    if not session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session.user.id
    
    if request.method == "GET":
        try:
            # Get user's profile information
            response = current_app.supabase.table("users").select("*").eq("user_id", user_id).execute()
            if not response.data:
                return jsonify({"error": "User not found"}), 404
            return jsonify(response.data[0]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == "POST":
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Update user's information
            response = current_app.supabase.table("users").update(data).eq("user_id", user_id).execute()
            return jsonify(response.data[0]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

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
        return jsonify(result.user.id), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@url.route("/recommend-meals", methods=["POST"])
def recommend_meals():
    
    user_data = request.json or {}
    recommendation = gemini.get_meal_recommendation(user_data)
    return jsonify({"recommendation": recommendation}), 200