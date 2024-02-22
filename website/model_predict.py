import pandas as pd
import pickle
from geopy.geocoders import Nominatim

def load_model(path):
    model_path = f"{path}/model.pkl"
    pipeline_path = f"{path}/pipeline.pkl"

    model = pickle.load(open(model_path, 'rb'))
    pipeline = pickle.load(open(pipeline_path, 'rb'))

    return model, pipeline

def loc_to_geo(location):
    geolocator = Nominatim(user_agent="house_predict_app")
    loc = geolocator.geocode(location)

    return loc.latitude, loc.longitude

def determine_price(price):
    if price/1000000000 < 1:
        return str(round(price/1000000, 2)) + " Juta"
    else:
        return str(round(price/1000000000, 2)) + " Miliar"
    
def prediction(X, pipeline, model):
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

    return price_prediction