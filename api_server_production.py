# Production Flask API server for object detection
# Returns count of cars, trucks, and cell phones

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
import tempfile
import logging
from logging.handlers import RotatingFileHandler
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Configure logging
# Create logs directory if it doesn't exist
try:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handler = RotatingFileHandler('logs/api.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
except Exception as e:
    # If logging setup fails, use console logging
    logging.basicConfig(level=logging.INFO)
    app.logger.warning(f'Could not set up file logging: {e}, using console logging')

app.logger.info('API server startup')

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load YOLO model (load once at startup)
yolo_path = 'yolov4'
weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])
labelsPath = os.path.sep.join([yolo_path, "coco.names"])

# Global variables for model
net = None
output_layers = None
LABELS = None

def download_weights_if_missing():
    """Download YOLO weights if missing (for Heroku/Railway deployment)"""
    import urllib.request
    
    if not os.path.exists(weightsPath):
        app.logger.info('YOLO weights not found, downloading...')
        try:
            os.makedirs(yolo_path, exist_ok=True)
            url = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights"
            app.logger.info(f'Downloading from {url}...')
            # Use urllib with progress indication
            def show_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(downloaded * 100 / total_size, 100)
                if block_num % 100 == 0:  # Log every 100 blocks
                    app.logger.info(f'Download progress: {percent:.1f}%')
            
            urllib.request.urlretrieve(url, weightsPath, show_progress)
            app.logger.info('Weights downloaded successfully!')
            return True
        except Exception as e:
            app.logger.error(f'Failed to download weights: {str(e)}')
            app.logger.error(traceback.format_exc())
            return False
    return True

def load_model():
    """Load YOLO model - called at startup"""
    global net, output_layers, LABELS
    
    try:
        app.logger.info('Loading YOLO model...')
        
        # Check and download weights if missing
        if not download_weights_if_missing():
            app.logger.error('Could not obtain YOLO weights')
            return False
        
        # Verify weights file exists
        if not os.path.exists(weightsPath):
            app.logger.error(f'Weights file not found at {weightsPath}')
            return False
        
        # Load labels
        LABELS = open(labelsPath).read().strip().split("\n")
        
        # Load YOLO network
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        
        # Get output layer names
        layer_names = net.getLayerNames()
        unconnected_out_layers = net.getUnconnectedOutLayers()
        if hasattr(unconnected_out_layers, 'shape') and len(unconnected_out_layers.shape) == 1:
            output_layers = [layer_names[int(i) - 1] for i in unconnected_out_layers]
        else:
            output_layers = [layer_names[int(i[0]) - 1] for i in unconnected_out_layers]
        
        app.logger.info('YOLO model loaded successfully!')
        return True
    except Exception as e:
        app.logger.error(f'Failed to load YOLO model: {str(e)}')
        app.logger.error(traceback.format_exc())
        return False

# Load model at startup
if not load_model():
    app.logger.error('CRITICAL: Could not load YOLO model. Server may not work correctly.')

# Class IDs we want to count: car=2, truck=7, cell phone=67
TARGET_CLASSES = {2: 'car', 7: 'truck', 67: 'cell phone'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_objects(image_path, confidence_threshold=0.5):
    """Detect objects in image and return count of cars, trucks, and cell phones"""
    global net, output_layers, LABELS
    
    if net is None or output_layers is None:
        return None, "Model not loaded"
    
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return None, "Could not load image"
        
        (H, W) = image.shape[:2]
        
        # Create blob and run detection
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (608, 608), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)
        
        # Process detections
        boxes = []
        confidences = []
        classIDs = []
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                
                if confidence > confidence_threshold and classID in TARGET_CLASSES:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        
        # Apply NMS
        if len(boxes) > 0:
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.3)
            
            if idxs is None:
                idxs = []
            elif isinstance(idxs, tuple):
                idxs = list(idxs)
            elif hasattr(idxs, 'flatten'):
                idxs = idxs.flatten()
            else:
                idxs = list(idxs) if idxs else []
            
            # Count objects by type
            counts = {'car': 0, 'truck': 0, 'cell phone': 0}
            for i in idxs:
                class_id = classIDs[i]
                if class_id in TARGET_CLASSES:
                    counts[TARGET_CLASSES[class_id]] += 1
            
            total = counts['car'] + counts['truck'] + counts['cell phone']
            return total, None
        else:
            return 0, None
    except Exception as e:
        app.logger.error(f'Detection error: {str(e)}')
        app.logger.error(traceback.format_exc())
        return None, f"Detection error: {str(e)}"

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_status = "loaded" if net is not None else "not loaded"
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "model_status": model_status
    })

@app.route('/detect', methods=['POST'])
def detect():
    """Main detection endpoint"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, gif, bmp"}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Get confidence threshold from request (optional, default 0.5)
            confidence = float(request.form.get('confidence', 0.5))
            if confidence < 0.1 or confidence > 1.0:
                confidence = 0.5
        except:
            confidence = 0.5
        
        # Detect objects
        count, error = detect_objects(filepath, confidence)
        
        # Clean up temp file
        try:
            os.remove(filepath)
        except:
            pass
        
        if error:
            app.logger.error(f'Detection failed: {error}')
            return jsonify({"error": error}), 500
        
        app.logger.info(f'Detection successful: count={count}')
        return jsonify({"count": count})
        
    except Exception as e:
        app.logger.error(f'Request error: {str(e)}')
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # For development only - use gunicorn for production
    app.run(host='0.0.0.0', port=5000, debug=False)

