from app import create_app
from app.routes import *


app = create_app()

app.register_blueprint(url)
# only used if running local
#if __name__ == "__main__":
    #app.run(debug=True)
