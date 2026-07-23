import requests
import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

def rag_create_preset(slug=0, model="~openai/gpt-mini-latest", **kwargs):
    if slug == 0:
        return 
    
    url = f"https://openrouter.ai/api/v1/presets/{slug}/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,

        # These will be ignored when creating the preset
        "messages": [
            {
                "role": "user",
                "content": "Hello!"
            }
        ],
    }

    data.update(kwargs)

    response = requests.post(url, headers=headers, json=data)
    print("Status code:", response.status_code)
    print("Response:", response.text)

    return response


'''
rag_create_preset(slug="my-chat-preset-testing-4")
rag_create_preset(slug="my-chat-preset-testing-5", temperature=0.5)
rag_create_preset(slug="my-chat-preset-testing-6", temperature=1, max_tokens=100)
rag_create_preset(slug="my-chat-preset-testing-7", temperature=1, max_tokens=100, frequency_penalty=-1)
'''