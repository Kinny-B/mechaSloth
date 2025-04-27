# Look Function
import cv2
def look(yolo):
    # initialize camera
    _cam = cv2.VideoCapture(0)
    # capture frame
    result, frame =_cam.read()
    # save frame as image
    if result:
        cv2.imwrite('image.png', frame)
    # Load image with OpenCV
    image = cv2.imread("/home/kinbok/mechasloth/src/image.png")
    # Release the webcam
    _cam.release()
    # return Inference
    return yolo(image)    