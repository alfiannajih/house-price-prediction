import re
import json
import pandas as pd

def open_file(file):
    data = []
    with open(file) as f:
        for line in f:
            data.append(json.loads(line))

    return data

def clean_house_facility(house_detail, house_facility):
    attribute = [x.split("-")[2] for x in house_facility] + ["land_area", "building_area"]
    value = [int(x) for x in re.findall(r"\b\d+\b", house_detail)]

    for item in ["bed", "bath", "car"]:
        if item not in attribute:
            attribute.append(item)
            value.append(None)

    return dict(zip(attribute, value))

def clean_price(price_raw):
    if "juta" in price_raw.lower():
        price = int(re.findall(r"\d+", price_raw)[0]) * 1000000
    elif "miliar" in price_raw.lower():
        price = price = int(re.findall(r"\d+", price_raw)[0]) * 1000000000
    else:
        price = None

    return price

def clean_certif(certif_raw):
    if certif_raw == 1:
        return "SHM"
    else:
        return "HGB"
    
def clean_furnish(furnish_raw):
    if furnish_raw == 1:
        return "furnished"
    else:
        return "unfurnished"

def clean_entity(house_entity):
    house_location = house_entity["location"]
    house_detail = house_entity["detail"]
    house_facility = house_entity["facility"]
    house_price = house_entity["price"].split("\n")[0]
    house_certif = house_entity["certif"]
    house_furnish = house_entity["furnish"]

    return {
        "location": house_location,
        "price": clean_price(house_price),
        "certif": clean_certif(house_certif),
        "furnish": clean_furnish(house_furnish)
    } | clean_house_facility(house_detail, house_facility)

def concat_raw_data(files_name):
    raw_data = []
    
    for file in files_name:
        raw_data.extend(open_file(file))
    
    return raw_data

def data_cleaning(raw_data):
    clean_data = []

    for entity in raw_data:
        clean_house = clean_entity(entity)
        clean_data.append(clean_house)
    
    return pd.json_normalize(clean_data)

def rename_columns(df):
    column_map = {"car": "carport"}

    return df.rename(column_map, axis=1)

files_name =[
    "dki-jakarta.txt",
    "jakarta-pusat.txt",
    "jakarta-timur.txt",
    "jakarta-barat.txt",
    "jakarta-utara.txt",
    "jakarta-selatan.txt"
]

raw_data = concat_raw_data(files_name)
#raw_data = open_file("dki-jakarta.txt")
clean_data = data_cleaning(raw_data)
clean_data = rename_columns(clean_data.drop_duplicates())

print(clean_data["location"].str.split(",", expand=True)[1].value_counts())

clean_data.to_csv(
    "clean_jakarta.csv",
    index=False
)
