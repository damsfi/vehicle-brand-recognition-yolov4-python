# Copyright © 2020 by Spectrico
# Licensed under the MIT License
# Based on the tutorial by Adrian Rosebrock: https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
# Modified to detect all objects
# Usage: $ python car_brand_classifier_yolo4.py --image cars.jpg

# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-y", "--yolo", default='yolov4',
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applying non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov4.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov4.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# load our input image and grab its spatial dimensions
image = cv2.imread(args["image"])
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
layer_names = net.getLayerNames()
unconnected_out_layers = net.getUnconnectedOutLayers()
# Handle different OpenCV versions - newer versions return numpy array directly
if hasattr(unconnected_out_layers, 'shape') and len(unconnected_out_layers.shape) == 1:
	output_layers = [layer_names[int(i) - 1] for i in unconnected_out_layers]
else:
	output_layers = [layer_names[int(i[0]) - 1] for i in unconnected_out_layers]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (608, 608),
	swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
outputs = net.forward(output_layers)
end = time.time()

# show timing information on YOLO
print("[INFO] YOLO took {:.6f} seconds".format(end - start))

# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []
all_detections = {}  # Track all detections for debugging

# loop over each of the layer outputs
for output in outputs:
	# loop over each of the detections
	for detection in output:
		# extract the class ID and confidence (i.e., probability) of
		# the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]

		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
		if confidence > args["confidence"]:
			# Track all detections for debugging
			label = LABELS[classID]
			if label not in all_detections:
				all_detections[label] = 0
			all_detections[label] += 1
			
			# Detect all objects (not just cars)
			# scale the bounding box coordinates back relative to the
			# size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding
			# box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")

			# use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))

			# update our list of bounding box coordinates, confidences,
			# and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

# Print all detected objects for debugging
if all_detections:
	print("[INFO] All detected objects:", all_detections)
else:
	print("[INFO] No objects detected above confidence threshold")

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
print("[INFO] Found {} object detections before NMS".format(len(boxes)))

if len(boxes) > 0:
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])
	
	# Handle case where idxs might be None, tuple, or numpy array
	if idxs is None:
		idxs = []
	elif isinstance(idxs, tuple):
		idxs = list(idxs)
	elif hasattr(idxs, 'flatten'):
		idxs = idxs.flatten()
	else:
		idxs = list(idxs) if idxs else []
	
	print("[INFO] Found {} object detections after NMS".format(len(idxs)))
else:
	idxs = []
	print("[INFO] No objects detected in the image")

# ensure at least one detection exists
if len(idxs) > 0:
	# loop over the indexes we are keeping
	# Handle idxs flattening for different types
	if hasattr(idxs, 'flatten'):
		idxs_flat = idxs.flatten()
	else:
		idxs_flat = idxs
	for i in idxs_flat:
		# extract the bounding box coordinates
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])

		# draw a bounding box rectangle and label on the image
		color = [int(c) for c in COLORS[classIDs[i]]]
		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, color, 2)

# save the output image
cv2.imwrite("output.jpg", image)
print("[INFO] Output image saved as output.jpg")

# Try to show the output image if GUI is available
try:
	cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Image', W, H)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
except cv2.error:
	print("[INFO] GUI not available. Image saved to output.jpg")
