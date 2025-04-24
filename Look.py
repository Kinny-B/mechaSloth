#Look Function
import cv2
def look(yolo, picam2):
    # take picture
    picam2.capture_file("image.jpg")
    # Load image with OpenCV
    image = cv2.imread("/home/kinbok/mechasloth/src/image.jpg")
    image = cv2.rotate(image, cv2.ROTATE_180)
    # return Inference
    return yolo(image)