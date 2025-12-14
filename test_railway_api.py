# Test script for Railway API
import requests
import sys

# Get URL from command line or use default
if len(sys.argv) > 1:
    API_URL = sys.argv[1].rstrip('/')
else:
    print("Usage: python test_railway_api.py <your-railway-url>")
    print("Example: python test_railway_api.py https://your-app.up.railway.app")
    sys.exit(1)

print(f"Testing API at: {API_URL}")
print("-" * 50)

# Test 1: Health Check
print("\n1. Testing /health endpoint...")
try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 200:
        print("   ✅ Health check passed!")
    else:
        print("   ❌ Health check failed!")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Detection Endpoint
print("\n2. Testing /detect endpoint...")
try:
    # Test with volkswagen.jpg if it exists
    import os
    test_image = "volkswagen.jpg"
    
    if not os.path.exists(test_image):
        print(f"   ⚠️  Test image '{test_image}' not found")
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
            print(f"   ✅ Detection successful! Count: {count}")
        else:
            print(f"   ❌ Detection failed!")
            print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "-" * 50)
print("Testing complete!")

