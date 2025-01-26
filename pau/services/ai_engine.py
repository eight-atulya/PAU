# pau/services/ai_engine.py

import requests
from pau.config import Config


def generate_chat_response(messages, model="llama-3.2-1b-instruct", temperature=0.7, stream=False):
    """
    Call your local LM Studio API to get a response.
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": -1,
        "stream": stream
    }

    resp = requests.post(
        Config.LMSTUDIO_API_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    data = resp.json()
    return data
