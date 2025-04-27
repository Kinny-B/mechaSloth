import Load, Look
# main
if __name__ == "__main__":
    yolo = Load.getYolo()
    # 'Look' for and identify objects, print results
    results = Look.look(yolo)
    print(results.xyxy[0],"\n\n")
    results.print()