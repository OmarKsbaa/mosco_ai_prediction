from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import httpx
import os

app = FastAPI(
    title="Moscow Apartment Price Prediction - API Gateway",
    description="API Gateway for routing requests to prediction models and serving frontend",
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

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Service URLs
MODEL1_SERVICE_URL = os.getenv("MODEL1_SERVICE_URL", "http://model1-service:8001")
MODEL2_SERVICE_URL = os.getenv("MODEL2_SERVICE_URL", "http://model2-service:8002")

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
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MODEL1_SERVICE_URL}/predict",
                json=features.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Model 1 service unavailable: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Model 1 service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/model2")
async def predict_price_model2(features: ApartmentFeatures):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MODEL2_SERVICE_URL}/predict",
                json=features.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Model 2 service unavailable: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Model 2 service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check health of gateway and both model services"""
    health_status = {"gateway": "healthy", "services": {}}
    
    # Check Model 1 service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MODEL1_SERVICE_URL}/health", timeout=5.0)
            health_status["services"]["model1"] = response.json() if response.status_code == 200 else "unhealthy"
    except:
        health_status["services"]["model1"] = "unavailable"
    
    # Check Model 2 service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MODEL2_SERVICE_URL}/health", timeout=5.0)
            health_status["services"]["model2"] = response.json() if response.status_code == 200 else "unhealthy"
    except:
        health_status["services"]["model2"] = "unavailable"
    
    return health_status

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
