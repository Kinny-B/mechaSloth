from ollama import Client
import json
# Large-Language-Model Ollama Distilled 'DeepSeek-R1:1b'
# 'Think' of a response and direction from prompt and objects using DeepSeek LLM
def think(dpsk, prompt):
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
