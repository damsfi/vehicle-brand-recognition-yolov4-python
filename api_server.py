# Flask API server for object detection
# Returns count of cars, trucks, and cell phones

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load YOLO model (load once at startup)
print("[INFO] Loading YOLO model...")
yolo_path = 'yolov4'
weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])
labelsPath = os.path.sep.join([yolo_path, "coco.names"])

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

print("[INFO] YOLO model loaded successfully!")

# Class IDs we want to count: car=2, truck=7, cell phone=67
TARGET_CLASSES = {2: 'car', 7: 'truck', 67: 'cell phone'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_objects(image_path, confidence_threshold=0.5):
	"""Detect objects in image and return count of cars, trucks, and cell phones"""
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

@app.route('/health', methods=['GET'])
def health():
	"""Health check endpoint"""
	return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/detect', methods=['POST'])
def detect():
	"""Main detection endpoint"""
	if 'image' not in request.files:
		return jsonify({"error": "No image file provided"}), 400
	
	file = request.files['image']
	if file.filename == '':
		return jsonify({"error": "No file selected"}), 400
	
	if file and allowed_file(file.filename):
		# Save uploaded file temporarily
		filename = secure_filename(file.filename)
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(filepath)
		
		try:
			# Get confidence threshold from request (optional, default 0.5)
			confidence = float(request.form.get('confidence', 0.5))
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
			return jsonify({"error": error}), 500
		
		return jsonify({"count": count})
	else:
		return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, gif, bmp"}), 400

if __name__ == '__main__':
	print("[INFO] Starting API server...")
	print("[INFO] Send POST requests to /detect with 'image' file and optional 'confidence' parameter")
	app.run(host='0.0.0.0', port=5000, debug=False)

