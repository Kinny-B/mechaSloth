from picamera2 import Picamera2
# Object Detection with Yolov5
objects = []
# capture video
def video(picam2):
    print("\t...videoing\n")
    picam2.start()
    frame = picam2.capture_array()
    picam2.stop()
    return frame
# Yolov5 object detection
def detect(yolo, frame):
    print("\t...detecting objects\n")
    results = yolo(frame)
    objects = results.pandas().xyxy[0]["name"].toList()
    return objects
# 'Look' using the camera and object detection
def look(yolo, picam2):
    print("\nlooking...\n")
    frame = video(picam2)
    return detect(frame)