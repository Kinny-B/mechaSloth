# mechaSloth
A first attempt at a social robot, able to casually interact with the environment. Came up with this idea after hearing how the statical majority of chatGPT users, use the AI chat for personal questions, or even to socialize. By giving the chat a physical construct, people would anthropomorphize the chat-bot, making this already existing niche of social AI more comfortable to interact with.
The AI is also hosted locally inside the bot itself, this would remove any worry of data-harvesting on the user-end. Local-hosting the chat LLMs made the bot considerably slower, hence the name mechaSloth.
In future iterations would like to: swap to a different chat LLM(not happy with deepseek performance), upgrade hardware(new board, proximity sensors for better obstacle avoidance)
Powered by; raspberry pi 5 4GB, Ollama distilled deepseek-r1-1.5B LLM, Yolov5 Object Detection, Vosk Speech-to-Text, and PiperVoice Text-to-speech. Able to communicate via microphones & speakers. Able to observe it environment via camera. Able to move itself via DC bi-directional motors.

A mechanized sloth. Powered by 'ollama deepseek-r1-1.5B LLM' distilled onto a raspberry-Pi-5. Able to to communicate via; Listening through microphones with 'VOSK Offline Speech Recognition API'. Speech using 'Piper Text-to-Speech' and speakers. Able to observe its environment via camera and 'Ultralytics YOLOv5 computer vision model'. Able to move itself via DC bi-directional motors. 

setup/dependencies:
    $sudo apt install curl -y
    $curl -fsSL https://ollama.com/install.sh | sh
    $ollama run deepseeek-r1:1.5b # to end session /bye #
    $sudo apt install python3-pyaudio python3-picamera2 espeak-ng
    create virtual enviroment with system site packages
    $python3 -m venv2 --system-site-packages ~/venv2
    $source .venv2/bin/activate
    $pip3 install torch transformers piper-tts vosk ultralytics ollama adafruit-circuitpython-motorkit

run:
    $source .venv/bin/activate
    $cd /mechasloth/src
    $python3 main.py
