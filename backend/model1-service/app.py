from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Load the traditional ML model
model_path = os.path.join(os.path.dirname(__file__), 'Moscowregion.pkl')
model1 = joblib.load(model_path)

app = FastAPI(
    title="Moscow Apartment Price Prediction - Traditional ML Model",
    description="Traditional machine learning model for predicting apartment prices",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        log_price = model1.predict(features_array)[0]
        
        # Convert log price back to actual price
        predicted_price = np.expm1(log_price)
        
        return {
            "predicted_price": round(predicted_price, 2),
            "log_price": round(log_price, 4),
            "model_type": "traditional_ml"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "model1-traditional-ml"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
