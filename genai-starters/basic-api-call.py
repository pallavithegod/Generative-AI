import os, json
from openai import OpenAI
from google import genai

from dotenv import load_dotenv
load_dotenv()

#OPENAI
client = OpenAI(                 # this gets apiKey from their corresponding env var
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)  
# STANDARDIZATION: Client WITH MORE PARAMS USED TO ACCESS GEMINI API THRU OPENAI, #2 NOT NEEDED

# question = "Name the richest individual on globe"
question = "square root of 23 upto 5 decimal places"

sys_prompt = "you are a expert in math and only answer math related questions. for math unrelated query, say sorry and do not answer the query"
# enhance the response by few shot prompting - 
# rules: 
# output format : eg json {"role": , "mode": ,  "ans":}
# examples : 


response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages = [
        {"role": "system", "content":sys_prompt},
        {"role": "user", "content":question}
    ]
)

print("gemini via openai - " ,response.choices[0].message.content)


#GEMINI - less use
client2 = genai.Client()       # this automatically infers the apiKey etc. from their corresponding env var

response2 = client2.models.generate_content(
    model="gemini-3-flash-preview",
    config={
        "system_instruction": "you are a expert in math and only answer math related questions. for math unrelated query, say sorry and do not answer the query"
    },
    contents = question
)

# print("gemini - ", response2.text)    