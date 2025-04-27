# Load AI Models
import ollama
import piper
import torch
from ollama import Client
from vosk import Model, KaldiRecognizer
from piper import PiperVoice
import time
def getDpsk():
    print("\n loading AI models...\n")
    # load DeepSeek LLM
    dpsk = Client().create(
        model = 'mecha-sloth',
        from_ = 'deepseek-r1:1.5b',
        system = 'you are a robot assitant named mecha-sloth.',
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
    vosk.SetWords(True) # word level timings
    vosk.SetPartialWords(True) # get partial results
    print("\n\t...loaded Vosk STT\n")
    return vosk
def getPiper():
    # load Piper TTS model
    pip = PiperVoice.load(
        model_path = "piper/en_US-ryan-low.onnx",
        config_path = "piper/en_US-ryan-low.onnx.json",
    )
    print("\n\t...loaded Piper TTS\n")
    return pip
def getYolo():
    # load pre-trained YOLOv5n *Object Detection*
    yolo = torch.hub.load(
        "ultralytics/yolov5",
        "yolov5s",
        pretrained=True
    )
    yolo.conf = 0.3  # NMS confidence threshold
    yolo.iou = 0.5  # NMS IoU threshold
    yolo.agnostic = False  # NMS class-agnostic
    yolo.multi_label = False  # NMS multiple labels per box
    yolo.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
    yolo.max_det = 10  # maximum number of detections per image
    yolo.amp = False  # Automatic Mixed Precision (AMP) inference
    print("\n\t...loaded yolo object detection\n")
    return yolo