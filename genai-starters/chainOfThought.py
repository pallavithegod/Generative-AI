import os, sys, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# models = client.models.list()
# for m in models:
#     print(f"Available Model: {m.id}")

system_prompt = """
You're an expert AI Assistant that resolves user queries using Chain of Thought.

Rules:
- Think step-by-step.
- Prefix every single thinking step with "🧠 PLAN: "
- Prefix your final answer with "📢 OUTPUT: "
- Put each step on a new line.

Example:
User: Solve 2 + 3 * 5
🧠 PLAN: The user wants a math problem solved.
🧠 PLAN: Using BODMAS, multiply first: 3 * 5 = 15.
🧠 PLAN: The new equation is 2 + 15.
🧠 PLAN: Add the remaining numbers: 2 + 15 = 17.
📢 OUTPUT: 17
"""

print("\n")

msg_history = [{"role": "system", "content": system_prompt}]
user_query = input("\n👉 Enter your math problem: ")
msg_history.append({"role": "user", "content": user_query})   # now 2 items in list - system instructions + user's prompt = complete package sent to the AI
print("\n")

try:
    response = client.chat.completions.create(
        model="models/gemini-2.5-flash",
        messages=msg_history,
        stream=True    # The API sends the text back chunk-by-chunk (now response is no more a static object)
    )

    # Loop through the stream pipe
    for chunk in response:
        # 1. Safely check if the chunk has data
        if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:

            # 2. Extract the content from the CHUNK (not the response)
            content = chunk.choices[0].delta.content

            # 3. UX - Print it OS-level flush with 0.2 sec delay per letter
            for char in content:
                print(char, end="")
                sys.stdout.flush()     #sys module acceses the std output stream of terminal
                time.sleep(0.02)

except Exception as e:
    print(f"\n❌ : Error: {e}")

print("\n")