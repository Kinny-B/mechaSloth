# Load AI Models
import ollama
import piper
import torch
from ollama import Client
from vosk import Model, KaldiRecognizer
from piper import PiperVoice
from picamera2 import Picamera2
def getDeepseek():
    print("\n loading AI models...\n")
    # load DeepSeek LLM
    dpsk = Client().create(
        model = 'mecha-sloth',
        from_ = 'deepseek-r1:1.5b',
        system = 'you are a robot assitant named mecha-sloth',
        stream = False,
    )
    print("\n\t...loaded DeepSeek\n")
    return dpsk
def getVosk():
    # load Vosk Speach Recognition model
    vosk = KaldiRecognizer(
        Model("vosk-model-small-en-us-0.15"),
        16000
    ) # (VOSK_PATH, RATE)
    print("\n\t...loaded Vosk STT\n")
    return vosk
def getPiper():
    # load Piper TTS model
    pip = piper.PiperVoice.load(
        model_path = "rhaspy/en_US-lessac-low.onnx",
        config_path = "rhaspy/en_US-lessac-low.onnx.json",
    )
    print("\n\t...loaded Piper TTS\n")
    return pip
def getYolo():
    # load YOLOv5n *Object Detection*
    yolo = torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path = "yolo/yolov5n.pt"
    )
    print("\n\t...loaded yolo object detection\n")
    return yolo
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
