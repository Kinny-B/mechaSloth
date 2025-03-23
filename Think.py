from ollama import Client
# Large-Language-Model Ollama Distilled 'DeepSeek-R1:1b'
# 'Think' of a response and direction from prompt and objects using DeepSeek LLM
def think(dpsk, prompt, objects):
    print("\nThinking...\n")
    # add objects to prompt if there are any
    full_prompt = f"{prompt}. Detected objects: {', '.join(objects)}" if objects else prompt
    # generate response
    response = Client().chat(
        model=dpsk,
        messages=[{'role': 'user', 'content': full_prompt}],
        stream=False
    )
    # test print b4 return
    print(response)
    return response['message']['content']