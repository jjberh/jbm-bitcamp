from flask import Flask
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from app import routes

def create_app():

    app = Flask(__name__)

    CORS(app, origins=[
        "https://jbm-bitcamp-jjberhs-projects.vercel.app",
        "https://jbm-bitcamp.vercel.app",
        "https://jbm-bitcamp-git-frontend-jjberhs-projects.vercel.app",
        "http://localhost:5175"
    ])
    #CORS(app)
    #Connect to Supabase
    supabase_url = os.getenv("DB_URL") #Uses our env var
    supabase_key = os.getenv("DB_BACKEND_KEY")
    app.supabase = create_client(supabase_url, supabase_key)
    
    app.register_blueprint(routes.url)


    return app