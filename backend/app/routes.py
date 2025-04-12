from flask import Blueprint, request, jsonify, current_app
url = Blueprint("url", __name__)

@url.route("/")
def main():
    return "Hello"

@url.route("/signup", methods = "GET")

@url.route("/login")
def login():
    return "Logged"
