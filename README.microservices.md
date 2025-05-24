# Moscow Apartment Price Prediction - Microservices Architecture

This project has been restructured into a microservices architecture with separate services for each AI model and a frontend gateway.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Port 8000)                     │
│                     Static Files + Gateway                      │
└─────────────────┬───────────────────────────────────────────────┘
                  │
            ┌─────▼─────┐
            │  Gateway  │
            │ (Port 8000)│
            └─────┬─────┘
                  │
        ┌─────────┼─────────┐
        │                   │
   ┌────▼────┐         ┌────▼────┐
   │ Model 1 │         │ Model 2 │
   │Traditional│       │Deep Learning│
   │ML Service│        │ Service │
   │(Port 8001)│       │(Port 8002)│
   └─────────┘         └─────────┘
```

## Services

### 1. Gateway Service (Port 8000)
- **Location**: `backend/gateway/`
- **Purpose**: API Gateway and static file server
- **Responsibilities**:
  - Serves the frontend application
  - Routes prediction requests to appropriate model services
  - Handles CORS and load balancing
  - Health checks for all services

### 2. Model 1 Service (Port 8001)
- **Location**: `backend/model1-service/`
- **Purpose**: Traditional Machine Learning model
- **Model**: `Moscowregion.pkl` (scikit-learn)
- **Features**: 
  - Returns both predicted price and log price
  - Lighter resource requirements
  - Faster prediction times

### 3. Model 2 Service (Port 8002)
- **Location**: `backend/model2-service/`
- **Purpose**: Deep Learning model
- **Model**: `model2.keras` (TensorFlow)
- **Features**:
  - Neural network-based predictions
  - Higher resource requirements
  - Potentially more complex pattern recognition

## Directory Structure

```
mosco_ai_prediction/
├── frontend/                    # Frontend static files
│   └── index.html              # Main web interface
├── backend/
│   ├── gateway/                # API Gateway service
│   │   ├── app.py             # Gateway FastAPI application
│   │   ├── requirements.txt   # Gateway dependencies
│   │   └── Dockerfile         # Gateway container config
│   ├── model1-service/        # Traditional ML service
│   │   ├── app.py            # Model 1 FastAPI application
│   │   ├── Moscowregion.pkl  # Traditional ML model
│   │   ├── requirements.txt  # Model 1 dependencies
│   │   └── Dockerfile        # Model 1 container config
│   └── model2-service/        # Deep Learning service
│       ├── app.py            # Model 2 FastAPI application
│       ├── model2.keras      # Deep learning model
│       ├── requirements.txt  # Model 2 dependencies
│       └── Dockerfile        # Model 2 container config
├── docker-compose.yml         # Multi-service orchestration
└── README.md                  # This file
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- At least 4GB of available RAM (for TensorFlow service)

### Running the Application

1. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Start in background**:
   ```bash
   docker-compose up -d --build
   ```

3. **View logs**:
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f gateway
   docker-compose logs -f model1-service
   docker-compose logs -f model2-service
   ```

4. **Stop services**:
   ```bash
   docker-compose down
   ```

### Access Points

- **Main Application**: http://localhost:8000
- **Gateway Health**: http://localhost:8000/health
- **Model 1 Service**: http://localhost:8001/health
- **Model 2 Service**: http://localhost:8002/health

### API Endpoints

#### Gateway Service (Port 8000)
- `GET /` - Redirects to frontend
- `GET /static/index.html` - Frontend application
- `POST /predict/model1` - Predict using traditional ML model
- `POST /predict/model2` - Predict using deep learning model
- `GET /health` - Health check for all services

#### Model Services (Ports 8001, 8002)
- `POST /predict` - Make prediction
- `GET /health` - Service health check

### Request Format

```json
{
  "minutes_to_metro": 15,
  "number_of_rooms": 2,
  "area": 65,
  "living_area": 40,
  "kitchen_area": 12,
  "floor": 5,
  "number_of_floors": 12,
  "apartment_type": 0,
  "renovation_european": 1,
  "renovation_designer": 0,
  "renovation_without": 0
}
```

### Response Format

**Model 1 (Traditional ML)**:
```json
{
  "predicted_price": 8500000.50,
  "log_price": 15.9534,
  "model_type": "traditional_ml"
}
```

**Model 2 (Deep Learning)**:
```json
{
  "predicted_price": 8750000.25,
  "model_type": "deep_learning"
}
```

## Development

### Running Individual Services

Each service can be run independently for development:

```bash
# Gateway
cd backend/gateway
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000

# Model 1 Service
cd backend/model1-service
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001

# Model 2 Service
cd backend/model2-service
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8002
```

### Environment Variables

- `MODEL1_SERVICE_URL`: URL for Model 1 service (default: http://model1-service:8001)
- `MODEL2_SERVICE_URL`: URL for Model 2 service (default: http://model2-service:8002)
- `TF_CPP_MIN_LOG_LEVEL`: TensorFlow logging level (default: 2)

## Resource Requirements

- **Gateway**: 0.25-0.5 CPU cores, 256-512MB RAM
- **Model 1 Service**: 0.5-1 CPU cores, 512MB-1GB RAM
- **Model 2 Service**: 1-2 CPU cores, 1.5-3GB RAM

## Benefits of This Architecture

1. **Scalability**: Each model can be scaled independently
2. **Isolation**: Model failures don't affect other services
3. **Maintainability**: Each service has its own dependencies
4. **Deployment**: Services can be deployed and updated separately
5. **Resource Optimization**: Different resource allocations per service
6. **Development**: Teams can work on different models independently
