import os
import openai
from dotenv import load_dotenv
import requests

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Default model settings
DEFAULT_MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  # openai | openrouter
DEFAULT_MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")    # or mistral, claude-3-haiku vs.

def call_llm(prompt: str, provider: str = None, model: str = None) -> str:
    provider = provider or DEFAULT_MODEL_PROVIDER
    model = model or DEFAULT_MODEL_NAME

    if provider == "openai":
        return _call_openai(prompt, model)
    elif provider == "openrouter":
        return _call_openrouter(prompt, model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _call_openai(prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"].strip()

def _call_openrouter(prompt, model):
    """
    OpenRouter API (Claude, Mistral, Mixtral, vs.)
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",  # Gerekli olabilir
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
