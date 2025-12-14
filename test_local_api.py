# Quick test script for local API
import requests
import time

API_URL = "http://localhost:5000"

print("Testing Local API")
print("=" * 50)

# Wait a moment for server to start
print("\nWaiting for server to be ready...")
time.sleep(2)

# Test 1: Health Check
print("\n1. Testing /health endpoint...")
try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 200:
        print("   [OK] Health check passed!")
    else:
        print("   [FAIL] Health check failed!")
except Exception as e:
    print(f"   [ERROR] {e}")
    print("   Make sure the server is running: python run_local.py")

# Test 2: Detection
print("\n2. Testing /detect endpoint...")
try:
    import os
    test_image = "volkswagen.jpg"
    
    if not os.path.exists(test_image):
        print(f"   [WARN] Test image '{test_image}' not found")
        print("   Skipping detection test")
    else:
        print(f"   Using test image: {test_image}")
        with open(test_image, 'rb') as f:
            files = {'image': f}
            data = {'confidence': 0.5}
            response = requests.post(
                f"{API_URL}/detect",
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result}")
            count = result.get('count', 0)
            print(f"   [OK] Detection successful! Count: {count}")
        else:
            print(f"   [FAIL] Detection failed!")
            print(f"   Response: {response.text}")
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "=" * 50)
print("Testing complete!")

