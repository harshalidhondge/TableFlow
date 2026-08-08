import os

from flask import Flask, redirect, url_for

from config import Config
from utils.extensions import db, bcrypt


app = Flask(__name__)

app.secret_key = "tableflow_secret_key"

app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(__file__),
    "static",
    "images"
)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)


# Import models
from models.user import User
from models.table import Table


# Import and register blueprint
from routes.auth import auth

app.register_blueprint(auth)


# Create database tables
with app.app_context():
    db.create_all()
    print("Tables Created Successfully!")


# Home route
@app.route("/")
def home():
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(debug=True)