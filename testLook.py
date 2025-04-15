import Load, Look
# main
if __name__ == "__main__":
    yolo = Load.getYolo()
    picam2 = Load.setup_camera()
    # 'Look' for and identify objects list
    objects = Look.look(yolo, picam2)
    print(objects)