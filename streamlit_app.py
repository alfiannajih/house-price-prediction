import streamlit as st
import pickle
from geopy.geocoders import Nominatim
import pandas as pd

model_path = "model/model.pkl"
pipeline_path = "model/pipeline.pkl"

model = pickle.load(open(model_path, "rb"))
pipeline = pickle.load(open(pipeline_path, "rb"))

st.set_page_config("House Price Prediction", page_icon="🏡")
st.header("House Price Prediction in Jakarta 🏡")

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
        return str(round(price/1000000, 2)) + " Million"
    else:
        return str(round(price/1000000000, 2)) + " Billion"

def predict(location, certif, furnish, bed, bath, carport, land_area, building_area):
    # Convert to dict
    lat, long = loc_to_geo(location)

    input_data = {
        "latitude": lat,
        "longitude": long,
        "certif": certif,
        "furnish": furnish,
        "bed": bed,
        "bath": bath,
        "carport": carport,
        "land_area": land_area,
        "building_area": building_area
    }

    # Convert to dataframe
    X = pipeline.transform(
        pd.DataFrame.from_dict(input_data, orient="index").transpose()
    )

    # Predict the price
    return determine_price(model.predict(X)[0])

def main():
    # following lines create boxes in which user can enter data required to make prediction 
    location = st.text_input("Location")
    certif = st.selectbox("Certificate",("SHM","HGB")) 
    furnish = st.selectbox("Furniture",("furnished","unfurnished"))
    bed = st.number_input(label="Number of Bedroom", step=1)
    bath = st.number_input(label="Number of Bathroom", step=1)
    carport = st.number_input(label="Number of Carport", step=1)
    land_area = st.number_input(label="Size of Land Area", step=0.1)
    building_area = st.number_input(label="Size of Building Area", step=0.1)
    result =""

    if st.button("Predict"): 
        result = predict(
            location,
            certif,
            furnish,
            bed,
            bath,
            carport,
            land_area,
            building_area
        ) 
        st.success("The house price is IDR {}".format(result))

if __name__=='__main__':
    main()