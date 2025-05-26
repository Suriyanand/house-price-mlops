# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained pipeline
model = joblib.load("model/model.pkl")

# Define request body
class HouseFeatures(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str          # yes / no
    guestroom: str         # yes / no
    basement: str          # yes / no
    hotwaterheating: str   # yes / no
    airconditioning: str   # yes / no
    parking: int
    prefarea: str          # yes / no
    furnishingstatus: str  # furnished / semi-furnished / unfurnished

@app.post("/predict")
def predict_price(features: HouseFeatures):
    data = [[
        features.area,
        features.bedrooms,
        features.bathrooms,
        features.stories,
        features.mainroad,
        features.guestroom,
        features.basement,
        features.hotwaterheating,
        features.airconditioning,
        features.parking,
        features.prefarea,
        features.furnishingstatus
    ]]
    
    # Match column order from training
    column_order = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom',
                    'basement', 'hotwaterheating', 'airconditioning', 'parking',
                    'prefarea', 'furnishingstatus']
    
    # Convert to DataFrame
    input_df = pd.DataFrame(data, columns=column_order)

    # Make prediction
    prediction = model.predict(input_df)
    return {"predicted_price": round(prediction[0], 2)}
