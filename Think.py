from ollama import Client 
import json
from Load import getDpsk  # Import the model loader

# Initialize the client and model state
_client = None
_model_name = None

def _load_model_once():
    """Ensure the model is loaded only once when the module is imported"""
    global _client, _model_name
    
    if _client is None:
        _client = Client()
        _model_name = getDpsk() or 'mecha-sloth'  # Use configured model or default
        print(f"\nModel '{_model_name}' loaded successfully (ready for thinking)\n")

# Load the model immediately when this module is imported
_load_model_once()

def think(prompt, objects=None):
    """
    Generate a thoughtful response using the loaded LLM
    
    Args:
        prompt (str): The input prompt/question
        objects (str/list/dict, optional): Detected objects from Look.py
    
    Returns:
        str: The generated response
    """
    print("\n[THINKING ENGINE ACTIVATED]")
    print(f"Input prompt: {prompt[:100]}...")  # Show first 100 chars of prompt
    
    # Input validation
    if not isinstance(prompt, str):
        error_msg = "Error: Prompt must be a string"
        print(error_msg)
        return error_msg
    
    # Enhance prompt with object detection if available
    full_prompt = prompt
    if objects:
        if isinstance(objects, (list, dict)):
            objects_str = json.dumps(objects, indent=2)
        else:
            objects_str = str(objects)
        full_prompt += f"\n\nCONTEXT - Detected Objects:\n{objects_str}"
        print(f"Added {len(objects_str.split())} object tokens to prompt")

    try:
        # Generate response using the pre-loaded model
        response = _client.chat(
            model=_model_name,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=False,
        )
        
        # Process response
        if response and 'message' in response and 'content' in response['message']:
            content = response['message']['content'].strip()
            print("\n[THOUGHT GENERATION COMPLETE]")
            print(f"Response length: {len(content)} characters")
            return content
        else:
            error_msg = "Error: Invalid response structure from model"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Generation Error: {str(e)}"
        print(error_msg)
        return error_msg