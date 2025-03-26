# embeddings/deepseek_client.py

from openai import OpenAI
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


# Load from environment or manually paste your key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY

# Or replace with your actual key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Model for generation
DEEPSEEK_MODEL = "deepseek-chat"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def generate_response(
    system_prompt: str, user_prompt: str, temperature: float = 1.0
) -> str:
    """
    Generate a completion using DeepSeek V3 (deepseek-chat).

    Parameters:
        system_prompt (str): Context instruction for the assistant.
        user_prompt (str): User query or input.
        temperature (float): Sampling temperature.

    Returns:
        str: Generated response from DeepSeek.
    """
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        stream=False,
    )
    return response.choices[0].message.content.strip()
