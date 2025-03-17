# Load AI Models
import ollama
import piper
import torch
from ollama import Client
from vosk import Model, KaldiRecognizer
from piper import PiperVoice
from picamera2 import Picamera2
def load_models():
    print("\n loading AI models...\n")
    # load DeepSeek LLM
    dpsk = Client().create(
        model = 'mecha-sloth',
        from_ = 'deepseek-r1:1.5b',
        system = 'you are a robot assitant named mecha-sloth',
        stream = False,
    )
    print("\n\t...loaded DeepSeek\n")
    # load Vosk Speach Recognition
    vosk = KaldiRecognizer(
        Model("vosk-model-small-en-us-0.15"),
        16000
    ) # (VOSK_PATH, RATE)
    print("\n\t...loaded Vosk STT\n")
    # load Piper TTS
    pip = piper.PiperVoice.load(
        model_path = "/path/to/en_US-lessac-medium.onnx",
        config_path = "/path/to/config",
    )
    print("\n\t...loaded Piper TTS\n")
    # load YOLOv5n *Object Detection*
    yolo = torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path = "yolov5n.pt"
    )
    print("\n\t...loaded yolo object detection\n")
    # arrange models
    return dpsk, vosk, pip, yolo
# camera setup
def setup_camera():
    print("\nchecking camera...\n")
    global picam2
    picam2 = Picamera2()
    # preview window
    picam2.configure(
        picam2.create_preview_configuration(
            main={
                "size": (320,240)# (WIDTH,HEIGHT)
            }
        )
    )
    return picam2