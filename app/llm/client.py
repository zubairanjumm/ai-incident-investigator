import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment.")

if not OPENAI_MODEL:
    raise RuntimeError("OPENAI_MODEL is not set in the environment.")


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_text(prompt: str) -> str:
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text