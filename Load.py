# Load AI Models
import ollama
import piper
import torch
from ollama import Client
from vosk import Model, KaldiRecognizer
from piper import PiperVoice
import libcamera
from libcamera import controls
from picamera2 import Picamera2
import time
def getDeepseek():
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
# camera setup
def setup_camera():
    print("\nchecking camera...\n")
    global picam2
    picam2 = Picamera2()
    main = {'size': (1000, 1000), 'format': 'YUV420'}
    picam2.start_preview()
    preview_config = picam2.create_preview_configuration()
    preview_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picam2.configure(preview_config)
    picam2.set_controls({
                        "AwbEnable": 1,
                        "AeEnable": 1,
                        "ExposureTime":1000,
                        "AnalogueGain":10.0,
                        "LensPosition":1
                        })
    picam2.start()
    time.sleep(5)
    return picam2
