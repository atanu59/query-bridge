import os
from dotenv import load_dotenv
from google import genai 
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("AI_API_KEY"),
    http_options=types.HttpOptions(timeout=15000), 
)


def ask_cloud(prompt, system_prompt):
    response = client.models.generate_content(
        model=os.getenv("AI_MODEL"),
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text