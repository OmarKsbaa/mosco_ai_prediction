from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# Load the trained model
model = joblib.load('final_model.pkl')

app = FastAPI(
    title="Moscow Apartment Price Prediction API",
    description="API for predicting apartment prices in Moscow and Moscow region",
    version="1.0.0"
)

class ApartmentFeatures(BaseModel):
    minutes_to_metro: float
    number_of_rooms: int
    area: float
    living_area: float
    kitchen_area: float
    floor: int
    number_of_floors: int
    apartment_type: int  # 0 for Secondary, 1 for New building
    renovation_european: int  # 0 or 1
    renovation_designer: int  # 0 or 1
    renovation_without: int   # 0 or 1

@app.post("/predict")
async def predict_price(features: ApartmentFeatures):
    try:
        # Convert input features to numpy array in the correct order
        features_array = np.array([
            features.minutes_to_metro,
            features.number_of_rooms,
            features.area,
            features.living_area,
            features.kitchen_area,
            features.floor,
            features.number_of_floors,
            features.apartment_type,
            features.renovation_european,
            features.renovation_designer,
            features.renovation_without
        ]).reshape(1, -1)
        
        # Make prediction (log price)
        log_price = model.predict(features_array)[0]
        
        # Convert log price back to actual price
        predicted_price = np.expm1(log_price)
        
        return {
            "predicted_price": round(predicted_price, 2),
            "log_price": round(log_price, 4)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Moscow Apartment Price Prediction API"}