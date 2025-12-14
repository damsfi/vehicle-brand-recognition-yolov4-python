# Object Detection API Server

Simple Flask API server that detects cars, trucks, and cell phones in images and returns the total count.

## Setup

1. Install dependencies:
```bash
pip install -r requirements_api.txt
```

2. Make sure you have the YOLOv4 weights file in `yolov4/yolov4.weights`

3. Run the server:
```bash
python api_server.py
```

The server will start on `http://0.0.0.0:5000`

## API Endpoints

### POST /detect
Detects cars, trucks, and cell phones in an uploaded image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - `image` (file, required): Image file to process
  - `confidence` (float, optional): Confidence threshold (default: 0.5)

**Response:**
```json
{
  "count": 5
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/detect \
  -F "image=@your_image.jpg" \
  -F "confidence=0.5"
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:5000/detect"
files = {'image': open('your_image.jpg', 'rb')}
data = {'confidence': 0.5}
response = requests.post(url, files=files, data=data)
result = response.json()
print(f"Total count: {result['count']}")
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## Mobile App Integration

### Android (Kotlin/Java)
```kotlin
val client = OkHttpClient()
val requestBody = MultipartBody.Builder()
    .setType(MultipartBody.FORM)
    .addFormDataPart("image", "image.jpg",
        RequestBody.create(MediaType.parse("image/jpeg"), imageFile))
    .addFormDataPart("confidence", "0.5")
    .build()

val request = Request.Builder()
    .url("http://your-server-ip:5000/detect")
    .post(requestBody)
    .build()

val response = client.newCall(request).execute()
val json = JSONObject(response.body()?.string() ?: "")
val count = json.getInt("count")
```

### iOS (Swift)
```swift
let url = URL(string: "http://your-server-ip:5000/detect")!
var request = URLRequest(url: url)
request.httpMethod = "POST"

let boundary = UUID().uuidString
request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

var body = Data()
body.append("--\(boundary)\r\n".data(using: .utf8)!)
body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
body.append(imageData)
body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

request.httpBody = body

URLSession.shared.dataTask(with: request) { data, response, error in
    if let data = data {
        let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any]
        let count = json?["count"] as? Int ?? 0
        print("Total count: \(count)")
    }
}.resume()
```

## Deployment

### Local Development
Just run `python api_server.py`

### Production (using gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

### Docker (optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_api.txt .
RUN pip install -r requirements_api.txt

COPY . .

EXPOSE 5000
CMD ["python", "api_server.py"]
```

Build and run:
```bash
docker build -t object-detection-api .
docker run -p 5000:5000 object-detection-api
```

