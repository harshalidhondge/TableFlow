from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from utils.extensions import db, bcrypt

auth = Blueprint("auth", __name__)


# ------------------ REGISTER ------------------

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        print("========== REGISTER ==========")
        print("Original Password:", password)

        # Hash Password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        print("Generated Hash:", hashed_password)

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        print("✅ User Registered Successfully")
        print("==============================")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ------------------ LOGIN ------------------

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        print("========== LOGIN ==========")
        print("Entered Email:", email)
        print("Entered Password:", password)

        user = User.query.filter_by(email=email).first()

        if user:

            print("Password from DB:", user.password)
            print("Type:", type(user.password))

            match = bcrypt.check_password_hash(user.password, password)
            print("Password Match:", match)

            if match:

                print("✅ Login Successful")
                print("Welcome,", user.name)
                print("========================")

                return redirect(url_for("home"))

            else:

                print("❌ Invalid Password")

        else:

            print("❌ User Not Found")

    return render_template("auth/login.html")