import Load, Listen, Look, Move, Speak, Think
# main
if __name__ == "__main__":
	running = 1
    # Load AI Models
	vosk = Load.getVosk()
	pip = Load.getPiper()
	yolo = Load.getYolo()
	Load.getDpsk()
	# run main loop with keyboard interupt block
	try:
		while(running):
			# 'Listen' for speech and generate prompt string
			prompt = Listen.listen(vosk)
			# 'Look' for and identify objects list
			vision = Look.look(yolo)
			# 'context' the visualized scene into the prompt
			full_prompt = Think.context(prompt, vision)
			# 'Think' and generate a response string
			response = Think.think(str(full_prompt))
			# 'Speak' the generated respone
			Speak.speak(pip, response)
			# 'Move' a direction by parsing the response for commands
			Move.move(response)
	except KeyboardInterrupt:
		running = 0
		print("\nInterrupted!, exiting")
