import pyaudio
import json
from vosk import KaldiRecognizer
# speech to text, using vosk and kaldi
RATE = 16000
CHUNK = 4096
CHANNELS = 1
FORMAT = pyaudio.paInt16
LEN = 8
# get audio then prompt
def listen(voskRec):
	# capture audio
	data = bytearray()
	fragments = []
	mic = pyaudio.PyAudio()
	stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
	print("\nlistening...\n")
	try:
		for _ in range(int(LEN*RATE/CHUNK)): #go for a LEN seconds
			speech = stream.read(CHUNK, exception_on_overflow=False)
			data.extend(speech)
			# process incrementally
			if (voskRec.AcceptWaveform(speech)):
				result = json.loads(voskRec.Result())
				if 'text' in result:
					fragments.append(result['text'].strip())
		# get final result
		fullResult = json.loads(voskRec.FinalResult())
		if 'text' in fullResult:
			fragments.append(fullResult['text'].strip())
		# assemble prompt
		prompt = " ".join(fragments)
		prompt = f"{prompt.strip()}"
	finally:
		stream.stop_stream()
		stream.close()
		mic.terminate()
	# test print prompt then return
	print("\t...speech recognized:\n", prompt)
	return prompt
