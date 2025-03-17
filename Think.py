from ollama import generate
# Large-Language-Model Ollama Distilled 'DeepSeek-R1:1b'
# 'Think' of a response and direction from prompt and objects using DeepSeek LLM
def think(dpsk, prompt, objects):
    print("\nthinking...\n")
    prompt += ",detected objects: {objects}"
    return generate(dpsk, prompt)