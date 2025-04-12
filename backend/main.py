from app import create_app

app = create_app()

@app.route("/")
def hello():
    return "Hello"
# only used if running local
#if __name__ == "__main__":
    #app.run(debug=True)
