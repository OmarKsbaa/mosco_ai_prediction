from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import joblib
import numpy as np
import tensorflow as tf
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom model loading functions with error handling
def load_traditional_model(path):
    try:
        return joblib.load(path)
    except Exception as e:
        logger.error(f"Error loading traditional model: {str(e)}")
        raise RuntimeError(f"Failed to load traditional model: {str(e)}")

def load_deep_learning_model(path):
    try:
        # Configure TensorFlow to use CPU and reduce warnings
        tf.config.set_visible_devices([], 'GPU')
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        
        # Load the model weights without the architecture
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(11,), name='input_layer'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        
        # Try to load the weights
        try:
            model.load_weights(path)
        except:
            # If direct weight loading fails, try loading as full model
            temp_model = tf.keras.models.load_model(
                path,
                compile=False,
                custom_objects=None
            )
            model.set_weights(temp_model.get_weights())
        
        # Compile the model
        model.compile(optimizer='adam', loss='mse')
        return model
    except Exception as e:
        logger.error(f"Error loading deep learning model: {str(e)}")
        raise RuntimeError(f"Failed to load deep learning model: {str(e)}")

# Load both models with error handling
try:
    model1 = load_traditional_model('Moscowregion.pkl')
    model2 = load_deep_learning_model('model2.h5')
    logger.info("Both models loaded successfully")
except Exception as e:
    logger.error(f"Failed to load models: {str(e)}")
    # We'll continue running the app, but some endpoints might not work

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