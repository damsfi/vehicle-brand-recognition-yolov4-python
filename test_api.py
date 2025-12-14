# Simple test script for the API
import requests
import time

# Wait for server to start
print("Waiting for server to start...")
time.sleep(3)

# Test health endpoint
try:
    response = requests.get("http://localhost:5000/health")
    print("Health check:", response.json())
except Exception as e:
    print(f"Health check failed: {e}")
    exit(1)

# Test detection endpoint
try:
    url = "http://localhost:5000/detect"
    files = {'image': open('volkswagen.jpg', 'rb')}
    data = {'confidence': 0.5}
    
    print("\nTesting detection endpoint...")
    response = requests.post(url, files=files, data=data)
    result = response.json()
    print(f"Response: {result}")
    print(f"Total count (cars + trucks + cell phones): {result.get('count', 0)}")
except Exception as e:
    print(f"Detection test failed: {e}")

