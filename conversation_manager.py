import os
import time
from config import OPENAI_API_KEY, SYSTEM_PROMPT
from openai import OpenAI

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(history):
    print("Generating response...")
    messages = [SYSTEM_PROMPT] + history[-10:]
    full_response = ""

    for chunk in openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages, stream=True):
        if (text_chunk := chunk.choices[0].delta.content):
            full_response += text_chunk

    return full_response

def create_conversation_directory():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    conversation_id = f"conv_{timestamp}"
    conversation_path = os.path.join("output", conversation_id)

    if not os.path.exists(conversation_path):
        os.makedirs(conversation_path)

    return conversation_id, conversation_path
