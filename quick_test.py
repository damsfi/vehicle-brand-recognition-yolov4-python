# Quick API test - Replace YOUR_URL with your Railway URL
import requests

# ⬇️ REPLACE THIS WITH YOUR RAILWAY URL ⬇️
YOUR_URL = "https://your-app.up.railway.app"  # Change this!

print(f"Testing API: {YOUR_URL}")
print("-" * 50)

# Test health
print("\n1. Health Check:")
try:
    r = requests.get(f"{YOUR_URL}/health", timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    if r.status_code == 200:
        print("   ✅ API is online!")
    else:
        print("   ❌ API returned error")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test detection
print("\n2. Detection Test:")
try:
    with open('volkswagen.jpg', 'rb') as f:
        files = {'image': f}
        data = {'confidence': 0.5}
        r = requests.post(f"{YOUR_URL}/detect", files=files, data=data, timeout=30)
        print(f"   Status: {r.status_code}")
        print(f"   Response: {r.json()}")
        if r.status_code == 200:
            count = r.json().get('count', 0)
            print(f"   ✅ Detection works! Found {count} objects")
        else:
            print(f"   ❌ Detection failed: {r.text}")
except FileNotFoundError:
    print("   ⚠️  volkswagen.jpg not found - skipping detection test")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "-" * 50)
print("Done!")

