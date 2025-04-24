import Load, Look
# main
if __name__ == "__main__":
    yolo = Load.getYolo()
    picam2 = Load.setup_camera()
    # 'Look' for and identify objects, print results
    results = Look.look(yolo, picam2)
    print(results.xyxy[0],"\n\n")
    results.print()