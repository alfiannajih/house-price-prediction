from fastapi import FastAPI
from pydantic import BaseModel, Field

import pickle
import pandas as pd

# Load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# Load data processing pipeline
with open("model/pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

class HouseInformation(BaseModel):
    latitude: float = Field(description="Latitude of house location")
    longitude: float = Field(description="Longitude of house location")
    certif: str = Field(description="Certification of the house (SHM/HGB)")
    furnish: str = Field(description="Furniture of the house (furnished/unfurnished)")
    bed: int = Field(description="Number of bedroom in the house")
    bath: int = Field(description="Number of bathroom in the house")
    carport: int = Field(description="Number of carport in the house")
    land_area: float = Field(description="Land area in meter square")
    building_area: float = Field(description="Building area in meter square")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "latitude": -6.271720,
                    "longitude": 106.804921,
                    "certif": "SHM",
                    "furnish": "furnished",
                    "bed": 2,
                    "bath": 1,
                    "carport": 1,
                    "land_area": 120,
                    "building_area": 150
                }
            ]
        }
    }

class HousePrice(BaseModel):
    price: str

app = FastAPI()

@app.post("/v1/price")
async def predict_price(payload: HouseInformation):
    df = pd.DataFrame(payload.model_dump(), index=[0])
    test = pipeline.transform(df)

    price = model.predict(test)[0]
    if price < 1000000000:
        output = f"IDR {price/1000000} juta"
    else:
        output = f"IDR {price/1000000000} miliar"

    return {"price": output}