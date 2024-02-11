from flask import Flask, jsonify, request
import pickle
from geopy.geocoders import Nominatim
import json
import pandas as pd

app = Flask(__name__)

model_path = "model/model.pkl"
pipeline_path = "model/pipeline.pkl"

model = pickle.load(open(model_path, 'rb'))
pipeline = pickle.load(open(pipeline_path, 'rb'))

sample_data = {
    "location": "Bendungan Hilir, Jakarta Pusat",
    "certif": "SHM",
    "furnish": "furnished",
    "bed": 4,
    "bath": 3,
    "carport": 1,
    "land_area": 148,
    "building_area": 110
}

def loc_to_geo(location):
    geolocator = Nominatim(user_agent="house_predict_app")
    loc = geolocator.geocode(location)

    return loc.latitude, loc.longitude

def determine_price(price):
    if price/1000000000 < 1:
        return str(round(price/1000000, 2)) + " Juta"
    else:
        return str(round(price/1000000000, 2)) + " Miliar"

@app.route("/", methods=["GET"])
def index():
    return jsonify(sample_data)

@app.route("/predict", methods=["POST"])
def predict():
    # Retrieve input from user
    X = json.loads(request.data)

    # Convert location to geopoints
    lat, long = loc_to_geo(X["location"])
    X["latitude"] = lat
    X["longitude"] = long
    del X['location']

    # Preprocess the data
    X_trans = pipeline.transform(
        pd.DataFrame.from_dict(X, orient="index").transpose()
    )

    # Predict the house price
    price_prediction = determine_price(model.predict(X_trans)[0])
    response = {"price": price_prediction}

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)