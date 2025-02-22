import pyaudio
import numpy as np
import torch
import time
import gc
import urllib.request
import os
import RPi.GPIO as GPIO
from transformers import AutoModelForCausalLM, AutoTokenizer
from picamera2 import Picamera2
from piper import PiperVoice
from vosk import Model, KaldiRecognizer

# configs
# audio
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 16000
CHUNK = 512
SILENCE_THRESHOLD = 300
MIN_SPEECH_DURATION = 0.5
# LLM
MAX_RESPONSE_TOKENS = 50
MODEL_TEMPERATURE = 0.7
# video
VIDEO_WIDTH = 320
VIDEO_HEIGHT = 240
VIDEO_FPS = 10
# motors
MOTOR_PINS = {'IN1': 17, 'IN2': 18, 'IN3': 22, 'IN4': 23}
MOVE_DURATION = 2  # Seconds for movement actions

# move
def move_forward():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    time.sleep(MOVE_DURATION)
    stop_motors()
def move_backward():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.HIGH)
    time.sleep(MOVE_DURATION)
    stop_motors()
def turn_left():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    time.sleep(1)  # Shorter duration for turning
    stop_motors()
def turn_right():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.HIGH)
    time.sleep(1)
    stop_motors()
def stop_motors():
    for pin in MOTOR_PINS.values():
        GPIO.output(pin, GPIO.LOW)
#def test_motors():
#    setup_motors()
#    move_forward()
#    time.sleep(2)
#    turn_left()
#    time.sleep(1)
#    stop_motors()

# Hardware init
def setup_hardware():
    print("\nInitialize all hardware components....\n")
    # Motor control
    GPIO.setmode(GPIO.BCM)
    for pin in MOTOR_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
    stop_motors()
    
    # Camera
    global picam2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(
        main={"size": (VIDEO_WIDTH, VIDEO_HEIGHT)}
    ))
    
# loading
VOSK_PATH = "vosk-model-small-en-us-0.15"
DEEPSEEK_PATH = "deepseek-r1-1.5b"
YOLO_PATH = "yolov5n.pt"
PIPER_PATH = "en_US-lessac-medium.onnx"
def download_models():
    if not os.path.exists(VOSK_PATH):
        print("\nDownloading Vosk...\n")
        urllib.request.urlretrieve(
            "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
            "vosk-model-small-en-us-0.15.zip"
        )
        os.system("unzip vosk-model-small-en-us-0.15.zip -d vosk-model-small-en-us-0.15")

    if not os.path.exists(YOLO_PATH):
        print("\nDownloading YOLOv5n...\n")
        urllib.request.urlretrieve(
            "https://github.com/ultralytics/yolov5/releases/download/v6.2/yolov5n.pt",
            "yolov5n.pt"
        )
def load_models():
    print("\nLoading...\n")
    # Vosk speech recognition
    vosk_model = Model(VOSK_PATH)
    recognizer = KaldiRecognizer(vosk_model, RATE)
    # DeepSeek LLM
    llm_model = AutoModelForCausalLM.from_pretrained(
        DEEPSEEK_PATH,
        torch_dtype=torch.float16,
        device_map="auto",
        low_cpu_mem_usage=True,
        offload_folder="./offload",
        offload_state_dict=True
    )
    tokenizer = AutoTokenizer.from_pretrained(DEEPSEEK_PATH)
    # Piper TTS
    tts_voice = PiperVoice.load(PIPER_PATH)
    
    return recognizer, llm_model, tokenizer, tts_voice

# Audio
def check_microphone():
    p = pyaudio.PyAudio()
    if p.get_device_count() < 1:
        raise Exception("No microphone detected!")
    p.terminate()

def get_sound_direction(sound):
    if CHANNELS == 2:
        sound = sound.reshape(-1, 2)
        left = sound[:, 0]
        right = sound[:, 1]
        avg_left = np.mean(np.abs(left))
        avg_right = np.mean(np.abs(right))
        if avg_left > avg_right:
            return "sound from left"
        elif avg_right > avg_left:
            return "sound from right"
        else:
            return "sound from center"
    else:
        return "sound from mono"

def capture_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    speech_buffer = []
    in_speech = False
    speech_start = 0
    print("\nlistening...\n")
    try:
        while True:
            sound = stream.read(CHUNK, exception_on_overflow=False)
            audio_frame = np.frombuffer(sound, dtype=np.int16)
            rms = np.sqrt(np.mean(audio_frame**2))
            # voice activity check
            if rms > SILENCE_THRESHOLD:
                if not in_speech:
                    in_speech = True
                    speech_start = len(frames)
                speech_buffer.append(sound)
            elif in_speech:
                if (len(frames) - speech_start) / RATE > MIN_SPEECH_DURATION:
                    frames.extend(speech_buffer)
                    break
                speech_buffer = []
                in_speech = False
            frames.append(sound)
    except KeyboardInterrupt:
        raise
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        return b''.join(frames)

# Speech Recognition
def speech_to_text(audio_data, recognizer):
    print("\nrecognizing speech...\n")
    if recognizer.AcceptWaveform(audio_data):
        result = recognizer.Result()
        return result["text"]
    return ""

# Video
def capture_video():
    print("\nvideoing...\n")
    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(
            main={"size": (VIDEO_WIDTH, VIDEO_HEIGHT)}
        ))
        picam2.start()
        frame = picam2.capture_array()
        picam2.stop()
        # Load YOLOv5n *Object Detect*
        model = torch.hub.load("ultralytics/yolov5", "custom", path=YOLO_PATH)
        results = model(frame)
        objects = results.pandas().xyxy[0]["name"].tolist()
        return objects
    except Exception as e:
            print(f"error capturing video: {e}")
            return []

# LLM Response Generation
def generate_response(prompt, model, tokenizer, objects=None):
    print("\nresponse...\n")
    response = ""  # Init
    try:
        if objects:
            prompt += f" detected objects: {objects}"
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_RESPONSE_TOKENS,
                temperature=MODEL_TEMPERATURE,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        del inputs, outputs
    
    except Exception as e:
        print(f"Error generating response: {e}")
        response = "Sorry, I encountered an error."
        stop_motors()  # safe stop on error
        
    # motor control based on response
        execute_commands(response.lower())

    gc.collect()
    return response

# Text-to-Speech
def speak(text, tts_voice):
    print("Speaking...")
    tts_voice.speak(text)

def execute_commands(response_text):
    print("\nCommands...\n")
    if any(cmd in response_text for cmd in ["forward", "move ahead"]):
        move_forward()
    elif "backward" in response_text:
        move_backward()
    elif "left" in response_text:
        turn_left()
    elif "right" in response_text:
        turn_right()
    else:
        stop_motors()

# main
if __name__ == "__main__":
    # Download missing models
    download_models()
    
    # Initialize components
    check_microphone()
    recognizer, llm_model, tokenizer, tts_voice = load_models()
    setup_hardware()
    
    try:
        while True:
            # audio
            sound = capture_audio()
            
            # speech to text
            prompt = speech_to_text(sound, recognizer)
            print(f"\nUser: {prompt}\n")
            
            # video
            video = capture_video()
            print(f"\nEnviroment: {video}\n")
            
            # Generate
            response = generate_response(prompt, llm_model, tokenizer, video)
            print(f"\nAI: {response}\n")
            
            # Speak
            tts_voice.speak(response)
            
            # Clean up
            gc.collect()
            
    except KeyboardInterrupt:
        print("\nexiting...\n")
    finally:
        # clean up
        stop_motors()
        GPIO.cleanup()
        del llm_model, tokenizer
        torch.cuda.empty_cache()