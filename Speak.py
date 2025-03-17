from piper import PiperVoice
# Text-to-Speech with Piper Voice
def speak(pip, response):
    pip.PiperVoice.synthesize_stream_raw(response)