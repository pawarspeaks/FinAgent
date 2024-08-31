from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt3_response(prompt, user_context):
    full_prompt = f"{user_context}\n\nUser: {prompt}\nAssistant:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant. Use the user context provided to tailor your responses."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()