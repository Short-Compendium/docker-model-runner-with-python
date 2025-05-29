import os
from litellm import completion

response = completion(
    model="openai/ai/qwen2.5:latest", 
    api_key="tada",
    api_base=f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1",
    messages=[
        {
            "role": "user", 
            "content": "Who is James T. Kirk's best friend?"
        }
    ],
    stream=True,
)

# Stream the answer
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
