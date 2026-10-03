import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is not set in the environment.")

if not HF_MODEL:
    raise RuntimeError("HF_MODEL is not set in the environment.")


client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN,
)


def generate_text(prompt: str) -> str:
    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=1000,
        temperature=0.1,
    )

    return response.choices[0].message.content or ""