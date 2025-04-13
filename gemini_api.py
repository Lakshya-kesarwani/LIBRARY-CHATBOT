import requests
from together import Together
from dotenv import load_dotenv
import os
from flask import jsonify


from openai import OpenAI
load_dotenv()
client = OpenAI(base_url ="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_GEMINI_API_KEY"))
def ask_model(prompt):
    
    completion = client.chat.completions.create(
    extra_body={},
    model="google/gemini-flash-1.5-8b-exp",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type":"text",
            "text":prompt
            }
            ]
        }
    ]
    )
    return completion.choices[0].message.content

