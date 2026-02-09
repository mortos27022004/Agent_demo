from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY_opr"),  # Use OpenRouter API key
    base_url=os.getenv("OPENAI_API_BASE_URL")
)

resp = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Xin chào"}
    ]
)

print(resp.choices[0].message.content)
