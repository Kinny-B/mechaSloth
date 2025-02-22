# mechaSloth
A mechanized sloth. Powered by deepseek-r1-1.5B LLM distilled onto a raspberry-Pi-5. Able to to communicate via microphones and speakers. Able to observe its environment via camera. Able to move itself via 4 DC bi-directional motors. 

setup/dependencies:
    $sudo apt install curl -y
    $curl -fsSL https://ollama.com/install.sh | sh
    $ollama run deepseeek-r1:1.5b
    $sudo apt install python3-pyaudio python3-picamera2 espeak-ng
    $pip install transformers torch piper-tts vosk ultralytics
    $pip install torch transformers piper-tts vosk ultralytics
    Run the script once to automatically download missing models (Vosk, YOLOv5n).

to end session
    $/bye
to remove from files
    $ollama rm deepseeek-r1:1.5b
