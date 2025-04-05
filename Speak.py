import os
import wave
# Text-to-Speech with Piper Voice
def speak(pip, response):
	# test print response then speak
	print("\nspeaking...\n", response, '\n')
	if not response or not isinstance(response, str):
		response = f"{response.strip()}"
	#
	wav_file = wave.open('output.wav','w')
	pip.synthesize(response,wav_file)
	os.system("aplay /home/kinbok/mechasloth/src/output.wav")
