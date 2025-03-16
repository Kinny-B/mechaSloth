import pyaudio
import numpy
# speech to text, using vosk and kaldi
prompt = ""
RATE = 16000
CHUNK = 512
CHANNELS = 1
FORMAT = pyaudio.paInt32
SILENCE_THRESHOLD = 300
MIN_SPEECH = 0.5
listening = False
# capture audio
def audio():
    mic = pyaudio.PyAudio()
    stream = mic.open(
                    format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    frames = []
    speech_buffer = []
    speech_start = 0
    print("\nlistening...\n")
    while(listening):
        speech = stream.read(512, exception_on_overflow = False)
        audio_frame = numpy.frombuffer(speech, dtype = numpy.int32)
        rms = numpy.sqrt(numpy.mean(audio_frame**2))
        # voice activity check
        if(rms > SILENCE_THRESHOLD):
            if not(listening):
                listening = True
                speech_start = len(frames)
            speech_buffer.append(speech)
        elif(listening):
            if( ( (len(frames) - speech_start) / RATE > MIN_SPEECH) ):
                frames.extend(speech_buffer)
                break
            speech_buffer = []
            listening = False
        frames.append(speech)
        #finish
        stream.stop_stream()
        stream.close()
        mic.terminate()
        return b''.join(frames)
# use captured audio to generate prompt
def speech2text(audio_data, vosk):
    print("\t...speech recognized\n")
    if (vosk.AcceptWaveform(audio_data)):
        prompt = vosk.Result()
    return prompt
# get audio then prompt
def listen(vosk):
    audio_data = audio()
    prompt = speech2text(audio_data, vosk)
    print("\t...prompt generated\n")
    return prompt