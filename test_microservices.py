#!/usr/bin/env python3
"""
Test script for the microservices architecture
"""
import requests
import json
import time

# Test data
test_data = {
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

def test_service_health(service_name, url):
    """Test if a service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name} is healthy")
            return True
        else:
            print(f"❌ {service_name} health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} is not accessible: {e}")
        return False

def test_prediction(model_name, url):
    """Test prediction endpoint"""
    try:
        response = requests.post(url, json=test_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {model_name} prediction successful:")
            print(f"   Price: ₽{result['predicted_price']:,.2f}")
            print(f"   Model: {result['model_type']}")
            if 'log_price' in result:
                print(f"   Log Price: {result['log_price']}")
            return True
        else:
            print(f"❌ {model_name} prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {model_name} prediction error: {e}")
        return False

def main():
    print("🧪 Testing Moscow Apartment Price Prediction Microservices")
    print("=" * 60)
    
    # Service URLs
    gateway_url = "http://localhost:8000"
    model1_url = "http://localhost:8001"
    model2_url = "http://localhost:8002"
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    print("\n📋 Health Checks:")
    print("-" * 20)
    
    # Test health endpoints
    gateway_healthy = test_service_health("Gateway", gateway_url)
    model1_healthy = test_service_health("Model 1 Service", model1_url)
    model2_healthy = test_service_health("Model 2 Service", model2_url)
    
    print("\n🧮 Prediction Tests:")
    print("-" * 20)
    
    # Test predictions through gateway
    if gateway_healthy:
        print("\nTesting via Gateway:")
        test_prediction("Model 1 (via Gateway)", f"{gateway_url}/predict/model1")
        test_prediction("Model 2 (via Gateway)", f"{gateway_url}/predict/model2")
    
    # Test direct service endpoints
    if model1_healthy:
        print("\nTesting Model 1 directly:")
        test_prediction("Model 1 (Direct)", f"{model1_url}/predict")
    
    if model2_healthy:
        print("\nTesting Model 2 directly:")
        test_prediction("Model 2 (Direct)", f"{model2_url}/predict")
    
    print("\n🌐 Frontend Test:")
    print("-" * 15)
    
    # Test frontend
    try:
        response = requests.get(gateway_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible at http://localhost:8000")
        else:
            print(f"❌ Frontend access failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend is not accessible: {e}")
    
    print("\n🏁 Test completed!")
    print("\nTo access the application, open: http://localhost:8000")

if __name__ == "__main__":
    main()
