import os, sys, time, subprocess
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
import requests
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()
client = OpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd: str):
    print(f"\n⚙️ EXECUTING SYSTEM COMMAND: {cmd}")
    result = subprocess.getoutput(cmd)
    # Using subprocess to capture the actual output of the command for the AI to read
    return result

available_tools = {
    "run_command" : run_command
}

# industry level prompt- persona, engine, the boundaries/ rules, Schema Descriptions(pydantic)
system_prompt = """
You are an expert Autonomous AI Assistant.
You solve problems by using a loop of PLAN -> TOOL_CALL -> OUTPUT.

Rules:
1. Break down the task into logical steps.
2. If you need to interact with the computer, output a 'tool_call' step.
3. Wait for the user system to provide the OBSERVATION from your tool.
4. Once the task is complete, provide an 'output' step.
"""
# Defining the strict Pydantic structure for the AI's response
class output_format(BaseModel):
    step: str = Field(..., description="Must be exactly one of: 'plan', 'tool_call', 'output'")
    content: Optional[str] = Field(None, description="Your thought process or final answer")
    tool: Optional[str] = Field(None, description="Name of the tool, exactly 'run_command'")
    input: Optional[str] = Field(None, description="The system command to execute (e.g., 'mkdir my_app')")

# wrap api call in a fxn so that tenacity avoid max limit error
# It will give up after 5 tries.
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=60), 
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(RateLimitError)
)
def get_ai_response(history):
    return client.beta.chat.completions.parse(
        model="models/gemini-2.5-flash",
        response_format=output_format,
        messages=history,
    )

msg_history = [{"role": "system", "content": system_prompt}]
user_query = input("\n👉 Enter your problem: ")
msg_history.append({"role": "user", "content": user_query})   # in list - system instructions + user's prompt = sent to the AI

print("\n🚀 Agent Initialized...\n")

while True:
    try:
       
        # Extracting the validated Pydantic object directly
        response = get_ai_response(msg_history)
        # Extracting the validated Pydantic object directly
        # ai_response = response.output_parsed
        ai_response = response.choices[0].message.parsed

        # append AI's exact thoughts back into history so it remembers what it just did in the next loop iteration.
        msg_history.append({"role": "assistant", "content": ai_response.model_dump_json()})

        # 1. agent is planning
        if ai_response.step == "plan":
            print(f"🧠 PLAN: {ai_response.content}")

        # 2. AI decides it needs to run a terminal cmd
        elif ai_response.step == "tool_call":
            print(f"🛠️ TOOL DECISION: Needs to run '{ai_response.tool}' with command: [{ai_response.input}]")

            if ai_response.tool in available_tools:
                # Execute the tool
                cmd_output = available_tools[ai_response.tool](ai_response.input)
                print(f"🖥️ SYSTEM OUTPUT:\n{cmd_output}\n")

                msg_history.append({
                    "role": "user", 
                    "content": f"OBSERVATION from {ai_response.tool}:\n{cmd_output}\nWhat is the next step?"
                })

            else:
                # Failsafe
                print(f"⚠️ ERROR: Tool '{ai_response.tool}' does not exist.")
                msg_history.append({"role": "user", "content": f"OBSERVATION: Tool {ai_response.tool} failed. Tool not found."})

            # 3. task completed successfully
        elif ai_response.step == "output":
            print(f"📢 FINAL OUTPUT: {ai_response.content}")
            break # The Agent has finished the task

       
    except Exception as e:
        print(f"\n❌ : Error: {e}")
        break

print("\n✅ Agent Session Ended.\n")