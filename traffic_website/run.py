from flask import Flask
from flask_cors import CORS

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")
cors = CORS(app)

from project.main.views import main
app.register_blueprint(main)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)