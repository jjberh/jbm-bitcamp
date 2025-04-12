from flask import Blueprint

url = Blueprint("url", __name__)

@url.route("/")
def main():
    return "Hello"

@url.route("/login")
def login():
    return "Logged"