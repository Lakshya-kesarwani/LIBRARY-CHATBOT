import requests
from together import Together
from dotenv import load_dotenv
import os
from flask import jsonify


from openai import OpenAI
load_dotenv()
client = OpenAI(base_url ="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_API_KEY"))
def ask_model(prompt):
    
    completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-r1:free",
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ]
    )
    return completion.choices[0].message.content

# {"id":"npbKzfA-zqrih-92e6162efd9f8afd","object":"chat.completion","created":1744328399,"model":"meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8","choices":[{"index":0,"logprobs":null,"seed":null,"finish_reason":"stop","message":{"role":"assistant","content":"Hello! How are you today? Is there something I can help you with or would you like to chat?","tool_calls":[]}}],"prompt":[],"usage":{"prompt_tokens":12,"completion_tokens":23,"total_tokens":35}}