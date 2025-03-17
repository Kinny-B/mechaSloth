from ollama import generate
# Large-Language-Model
direction, response = ""

# 'Think' of a response and direction from prompt and objects using DeepSeek LLM
def think(dpsk, prompt, objects):
    print("\nthinking...\n")
    prompt += ",detected objects: {objects}"
    response = generate(dpsk, prompt)