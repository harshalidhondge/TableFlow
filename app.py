from flask import Flask
from config import Config
from utils.extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from models.user import User
from routes.auth import auth

app.register_blueprint(auth)
with app.app_context():
    db.create_all()
    print("Tables Created Successfully!")

@app.route("/")
def home():
    return "<h1>Welcome to TableFlow 🚀</h1>"

if __name__ == "__main__":
    app.run(debug=True)