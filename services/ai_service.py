from openai import OpenAI
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # hızlı/ucuz model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful customer support assistant. Answer clearly and politely."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI error: {str(e)}"