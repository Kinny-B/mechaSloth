import piper
import io
import pygame
import time
# Text-to-Speech with Piper Voice
def speak(pip, response):
	# test print response then speak
	print("\nspeaking...\n", response)
	if not response or not isinstance(response, str):
		response = f"{response.strip()}"
	try:
		# init pygame mixer
		pygame.mixer.pre_init(
		frequency=22050,
		size=-16,
		channels=1,
		buffer=2,
		devicename='sysdefault'
		)
		pygame.mixer.init()
		# synthesize to in-memory buffer  
		audioBuffer = io.BytesIO()
		pip.synthesize(response, audioBuffer)
		# rewind and load buffer to mixer
		audioBuffer.seek(0)
		pygame.mixer.music.load(audioBuffer)
		# playback
		pygame.mixer.music.play()
		# wait for playback
		while pygame.mixer.music.get_busy():
			time.sleep(0.1)
	except Exception as e:
		print("/n!*error speaking*!")
	finally:
		pygame.mixer.quit()