import Load, Listen, Look, Move, Speak, Think
# main
if __name__ == "__main__":
    running = True
    prompt = ""
    # Load AI Models
    dpsk, vosk, tts, yolo = Load.load_models()
    # Load Camera
    picam2 = Load.setup_camera()
    # run main loop
    while(running):
        # 'Listen' for speech and generate prompt
        prompt = Listen.listen(vosk)
        # 'Look' for and identify objects
        
        # 'Think' and generate a response and seek a direction
        
        # 'Speak' the respone
        
        # 'move' the direction
