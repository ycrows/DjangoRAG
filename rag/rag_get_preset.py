import os
import requests
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

def rag_get_preset():
    response = requests.get(
        "https://openrouter.ai/api/v1/presets",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        params={
            "limit": 100
        }
    )

    response.raise_for_status()

    data = response.json()

    presetDict = {}

    for preset in data["data"]:
        #print(f"{preset['name']}  ->  {preset['slug']}")
        presetDict.update({preset['name']: preset['slug']})

    return presetDict