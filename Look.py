from picamera2 import Picamera2
from ultralytics import YOLO
import cv2

# Load the YOLOv8 model (you can specify your own model path)
model = YOLO("yolov8n.pt")  # Or yolov8s.pt, yolov8m.pt, etc.

def look(image_path):
    """
    Detects objects in the given image using a YOLO model.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        list of dict: A list containing detected objects with their class names and confidence scores.
    """
    results = model(image_path)
    
    # Get the first result (assumes batch size = 1)
    detections = results[0]

    objects = []
    for box in detections.boxes:
        class_id = int(box.cls)
        class_name = model.names[class_id]
        confidence = float(box.conf)
        objects.append({
            "name": class_name,
            "confidence": confidence
        })
    
    return objects

