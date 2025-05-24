from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import joblib
import numpy as np
import tensorflow as tf

# Load both models
model1 = joblib.load('Moscowregion.pkl')
model2 = tf.keras.models.load_model('model2.keras', custom_objects={'InputLayer': tf.keras.layers.InputLayer})

app = FastAPI(
    title="Moscow Apartment Price Prediction API",
    description="API for predicting apartment prices in Moscow and Moscow region",
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

# Mount static files only for /static path
app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.post("/predict/model1")
async def predict_price_model1(features: ApartmentFeatures):
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

@app.post("/predict/model2")
async def predict_price_model2(features: ApartmentFeatures):
    try:
        # Convert input features to numpy array in the correct order
        features_array = np.array([
            features.apartment_type,
            features.minutes_to_metro,
            features.number_of_rooms,
            features.area,
            features.living_area,
            features.kitchen_area,
            features.floor,
            features.number_of_floors,
            features.renovation_designer,
            features.renovation_european,
            features.renovation_without
        ]).reshape(1, -1)
        
        # Make prediction using the deep learning model
        predicted_price = float(model2.predict(features_array)[0][0])
        
        return {
            "predicted_price": round(predicted_price, 2),
            "model_type": "deep_learning"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")