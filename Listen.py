import pyaudio
import numpy
import vosk
# speech to text, using vosk and kaldi
RATE = 16000
CHUNK = 2**5
CHANNELS = 1
FORMAT = pyaudio.paInt16
SILENCE_THRESHOLD = 300
LEN = 5
def listen(vosk_m):
	# capture audio
	speech = ' '
	mic = pyaudio.PyAudio()
	stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
	print("\nlistening...\n")
	for i in range(int(LEN*RATE/CHUNK)): #go for a LEN seconds
		speech = stream.read(CHUNK)
	print("\t...speech recognized\n")
	stream.stop_stream()
	stream.close()
	mic.terminate()
	# use captured audio to generate prompt
	prompt = ' '
	if (vosk_m.AcceptWaveform(speech)):
		prompt += vosk_m.Result()
		print("\t...prompt generated\n")
	return prompt
