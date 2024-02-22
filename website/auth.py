from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    user = db.session.execute(text("SELECT * FROM User WHERE username = :username"), {"username": username}).first()
    if user:
        flash("Username already exists.")
        return redirect(url_for("auth.signup"))
    elif password != confirm_password:
        flash("Passwords don't match.")
        return redirect(url_for("auth.signup"))

    db.session.execute(text("INSERT INTO User (username, password) VALUES (:username, :password)"), {"username": username, "password": generate_password_hash(password)})
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    user = db.session.execute(text("SELECT * FROM User WHERE username = :username"), {"username": username}).first()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid username or password")
        return redirect(url_for("auth.login"))

    login_user(User(id=user.id))
    return redirect(url_for("predict_price.predict_home"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
