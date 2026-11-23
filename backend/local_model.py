import os
import requests
from dotenv import load_dotenv

load_dotenv()


def ask_local(prompt, system_prompt):
    url = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/") + "/api/chat"
    payload = {
        "model": os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {"temperature": 0},
        "keep_alive": "10m",
    }
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["message"]["content"]