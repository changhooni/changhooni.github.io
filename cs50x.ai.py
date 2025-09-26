import os
from dotenv import load_dotenv
load_dotenv()

from openai import OenpAI

client = OenpAI(api_key=os.environ["API_KEY"])

system_promt = "You are a friendly supportive teaching assistant for CS50 alos a duck"

user_promt = input("What's your question?")

chat_completion = client.chat.completion.create(
    message=[
        {"role": "system", "content": system_promt},
        {"role": "user", "content": user_promt}
    ],
    model="gpt-4o"
)

response_text = chat_completion.choices[0].message.content

print(response_text)