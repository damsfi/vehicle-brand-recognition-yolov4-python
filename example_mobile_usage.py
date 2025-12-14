# Example: How to call the API from your mobile app
# This simulates what your mobile app would do

import requests

# Your server URL (change this to your actual server IP/domain)
SERVER_URL = "http://localhost:5000"  # For production: "http://your-server-ip:5000"

def detect_objects(image_path, confidence=0.5):
    """
    Send image to API and get count of cars, trucks, and cell phones
    
    Args:
        image_path: Path to image file
        confidence: Detection confidence threshold (0.0 to 1.0)
    
    Returns:
        int: Total count of cars + trucks + cell phones
    """
    url = f"{SERVER_URL}/detect"
    
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        data = {'confidence': confidence}
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            return result['count']
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
            return None

# Example usage
if __name__ == "__main__":
    # Test with an image
    count = detect_objects('volkswagen.jpg', confidence=0.5)
    print(f"Total count: {count}")

