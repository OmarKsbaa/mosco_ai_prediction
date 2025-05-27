#!/bin/bash

# Test the microservices
echo "Waiting for services to be up..."
sleep 5

# Test the gateway health
echo "Testing Gateway health..."
curl -s http://localhost:8000/health

# Test model1 health
echo -e "\n\nTesting Model 1 health..."
curl -s http://localhost:8001/health

# Test model2 health
echo -e "\n\nTesting Model 2 health..."
curl -s http://localhost:8002/health

# Test model1 prediction
echo -e "\n\nTesting Model 1 prediction..."
curl -s -X POST http://localhost:8000/predict/model1 \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# Test model2 prediction
echo -e "\n\nTesting Model 2 prediction..."
curl -s -X POST http://localhost:8000/predict/model2 \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

echo -e "\n\nTests complete. Access the frontend at http://localhost:8000/"
