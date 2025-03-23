import pyaudio
import numpy
import vosk
# speech to text, using vosk and kaldi
RATE = 16000
CHUNK = 4096
CHANNELS = 1
FORMAT = pyaudio.paInt16
SILENCE_THRESHOLD = 300
LEN = 5
def listen(voskRec):
    # capture audio
	mic = pyaudio.PyAudio()
	stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
	print("\nlistening...\n")
	speech = bytearray()
	# try to listen
	try:
		for _ in range(int(LEN*RATE/CHUNK)):  # 5 seconds
			data = stream.read(CHUNK, exception_on_overflow=False)
			speech.extend(data)
            # Process incrementally
			if voskRec.AcceptWaveform(data):
				result = voskRec.Result()
				print("Partial result:", result)
                
	finally:
		stream.stop_stream()
		stream.close()
		mic.terminate()
    # Get final result
	result = voskRec.FinalResult()
	print("Final result:", result)
	return result