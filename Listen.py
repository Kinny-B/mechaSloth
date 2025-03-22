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
global prompt = 'hello mechasloth, '

# capture audio
def audio():
	listening = 1
	speech = ' '
	mic = pyaudio.PyAudio()
	stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
#	frames = []
#	speech_buffer = []
#	speech_start = 0
	print("\nlistening...\n")
	for i in range(int(LEN*RATE/CHUNK)): #go for a LEN seconds
			speech = stream.read(CHUNK)
#	while(listening):
#		rms = numpy.sqrt(numpy.mean(audio_frame**2))
#		# voice activity check
#		if(rms > SILENCE_THRESHOLD):
#			if not(listening):
#				listening = True
#				speech_start = len(frames)
#				speech_buffer.append(speech)
#		elif(listening):
#			if(( (len(frames) - speech_start) / RATE > MIN_SPEECH)):
#				frames.extend(speech_buffer)
#				break
#			speech_buffer = []
#			listening = False
#		frames.append(speech)
#		audio_data = b''.join(frames)
	stream.stop_stream()
	stream.close()
	mic.terminate()
	return speech
# use captured audio to generate prompt
def speech2text(audio_data, vosk_m):
	if (vosk_m.AcceptWaveform(audio_data)):
		prompt += vosk_m.Result()
		print("\t...speech recognized\n")
	return prompt
# get audio then prompt
def listen(vosk_m):
	audio_data = audio()
	prompt = speech2text(audio_data, vosk_m)
	print("\t...prompt generated\n")
	return prompt
