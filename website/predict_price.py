from flask import Blueprint, render_template, request
from flask_login import login_required
import json
from . import db
from .model_predict import load_model, prediction

predict_price = Blueprint("predict_price", __name__)

model, pipeline = load_model("model")

@predict_price.route("/predict-price", methods=["GET", "POST"])
@login_required
def predict_home():
    price_prediction = None
    if request.method == "POST":
        X = request.form.to_dict()
        price_prediction = prediction(X, pipeline=pipeline, model=model)

    return render_template("predict_price.html", price=price_prediction)
"""
@predict_price.route("/predict-price/predicted", methods=["POST"])
@login_required
def predict_post():"""
