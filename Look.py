#Look Function
from ultralytics import YOLO
import cv2

def look(yolo, picam2):
    """
    Detects objects in the given image using a YOLO model.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        list of dict: A list containing detected objects with their class names and confidence scores.
    """
    picam2.capture_file("image.jpg")
    results = yolo("/home/kinbok/mechasloth/src/image.jpg")
    
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