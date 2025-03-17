import Load, Listen, Look, Move, Speak, Think
# main
if __name__ == "__main__":
    running = True
    prompt = ""
    # Load AI Models
    dpsk, vosk, pip, yolo = Load.load_models()
    # Load Camera
    picam2 = Load.setup_camera()
    # run main loop
    while(running):
        # 'Listen' for speech and generate prompt string
        prompt = Listen.listen(vosk)
        # 'Look' for and identify objects list
        objects = Look.look(yolo, picam2)
        # 'Think' and generate a response string
        response = Think.think(dpsk, prompt, objects)
        # 'Speak' the generated respone
        Speak.speak(pip, response)
        # 'Move' a direction by parsing the response for commands
        Move.move(response)