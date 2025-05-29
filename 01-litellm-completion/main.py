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
    #max_tokens=100
)
print(response.choices[0].message.content)

