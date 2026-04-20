from openai import OpenAI
from google import genai

from dotenv import load_dotenv
load_dotenv()

#OPENAI
client = OpenAI()   # this automatically infers the apiKey etc. from their corresponding env var
# Client WITH MORE PARAMS CAN BE USED IN THE SAME WAY AS #1 TO ACCESS GEMINI API THRU OPENAI, #2 NOT NEEDED

question = "Name the richest individual on globe"
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages = [
        {"role": "user", "content":question}
    ]
)

print("openai - " ,response.choices[0].message.content)

#GEMINI
client2 = genai.Client()

response2 = client2.models.generate_content(
    model="gemini-3-flash-preview",
    contents = question
)

print("gemini - " ,response2.text) 