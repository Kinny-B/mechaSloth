from ollama import Client
import json
# Large-Language-Model Ollama Distilled 'DeepSeek-R1:1b'
# prepare the prompt by adding objects and context
def context(prompt, vision):
	objects = vision.pandas().xyxy[0].name
	print("\n\tobjects identified:\n")
	print(objects)
	context = "you are a robot with camera and wheels attached to you. you can move a direction simply by including it in your next response. you see the following objects: "
	objects_str = ", ".join(objects)
	print(f"Added {len(objects_str.split())} object tokens to prompt")
	prompt_parts = [prompt, context, objects_str]
	full_prompt = " ".join(prompt_parts)
	return(full_prompt)
# 'Think' of a response and direction from prompt and objects using DeepSeek LLM
def think(prompt):
	print("\nthinking...\n", prompt)
	# str type check
	if not isinstance(prompt, str):
		response = "is not a valid string"
		print(response)
		return response
#   prompt += ",detected objects: {objects}"
	# generate
	response = Client().chat(
		model='mecha-sloth',
		messages=[{'role': 'user', 'content': prompt}],
		stream=False,
	)
	# seperate response
	if response and 'message' in response and 'content' in response['message']:
		content = response['message']['content'].strip()
	else:
		print("/*!*thinking error*!*/n")
	# test print response then return
	print(response, "\t...thought generated:\n")
	return content
