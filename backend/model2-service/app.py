from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import os

# Load the deep learning model
model_path = None
for model_file in ['model2.keras', 'model2.h5']:
    if os.path.exists(os.path.join(os.path.dirname(__file__), model_file)):
        model_path = os.path.join(os.path.dirname(__file__), model_file)
        break

if model_path is None:
    raise FileNotFoundError("Could not find model file (model2.keras or model2.h5)")

print(f"Loading model from: {model_path}")
model2 = tf.keras.models.load_model(model_path, custom_objects={'InputLayer': tf.keras.layers.InputLayer})

app = FastAPI(
    title="Moscow Apartment Price Prediction - Deep Learning Model",
    description="Deep learning neural network model for predicting apartment prices",
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
        # Convert input features to numpy array in the correct order for model2
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
        log_price = float(model2.predict(features_array)[0][0])
        predicted_price = np.expm1(log_price)
        return {
            "predicted_price": round(predicted_price, 2),
            "log_price": round(log_price, 4),
            "model_type": "deep_learning"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "model2-deep-learning"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
