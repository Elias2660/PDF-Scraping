from openai import OpenAI
import os


def perform_gpt_query(context: str, query: str, model: str = "gpt-4o") -> str:
    api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": query},
        ],
    )
    return f"""{completion.choices[0].message.content}"""
