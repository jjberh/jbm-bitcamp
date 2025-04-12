from app import create_app

app = create_app()

# only used if running local
if __name__ == "__main__":
    app.run(debug=True)
