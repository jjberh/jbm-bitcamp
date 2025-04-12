from flask import Blueprint, request, jsonify, current_app
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
        return jsonify({"Missing email, username, or password"})
    
    try:
        result = current_app.supabase.auth.sign_up({

            "email": email,
            "username": username,
            "password": password
            

        })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
   

@url.route("/users/")
def users():
    response = (
        current_app.supabase.table("users").select("*").execute()
    )

    return response


@url.route("/login")
def login():
    return "Logged"
