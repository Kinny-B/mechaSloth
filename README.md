# mechaSloth
A mechanized sloth. Powered by 'ollama deepseek-r1-1.5B LLM' distilled onto a raspberry-Pi-5. Able to to communicate via; Listening through microphones with 'VOSK Offline Speech Recognition API'. Speech using 'Piper Text-to-Speech' and speakers. Able to observe its environment via camera and 'Ultralytics YOLOv5 computer vision model'. Able to move itself via DC bi-directional motors. 

setup/dependencies:
    $sudo apt install curl -y
    $curl -fsSL https://ollama.com/install.sh | sh
    $ollama run deepseeek-r1:1.5b # to end session /bye #
    $sudo apt install python3-pyaudio python3-picamera2 espeak-ng
    create virtual enviroment with system site packages
    $python3 -m venv --system-site-packages ~/venv
    $source .venv/bin/activate
    $pip install torch transformers piper-tts vosk ultralytics
    cd yolov5
    pip install -r requirements.txt

run:
    $source .venv/bin/activate
    $cd /mechasloth/src
    $python3 main.py
