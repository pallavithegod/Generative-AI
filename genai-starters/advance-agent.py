import os, subprocess, json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

def run_command(cmd: str):
    print(f"\n⚙️ EXECUTING SYSTEM COMMAND: {cmd}")
    result = subprocess.getoutput(cmd)
    return result

available_tools = {
    "run_command" : run_command
}

system_prompt = """
You are an expert Autonomous AI Assistant.
You solve problems by using a loop of PLAN -> TOOL_CALL -> OUTPUT.

Rules:
1. Break down the task into logical steps.
2. If you need to interact with the computer, output a 'tool_call' step.
3. Wait for the user system to provide the OBSERVATION from your tool.
4. Once the task is complete, provide an 'output' step.

File Creation Rules (CRITICAL):
5. To create or modify files via system commands, ALWAYS use the `cat << 'EOF' > filepath/filename.ext` pattern.
6. NEVER compress code into single-line `echo` statements with escaped newlines.

Example:
cat << 'EOF' > app.py
print("Hello World")
EOF
"""
class output_format(BaseModel):
    step: str = Field(..., description="Must be exactly one of: 'plan', 'tool_call', 'output'")
    content: Optional[str] = Field(None, description="Your thought process or final answer")
    tool: Optional[str] = Field(None, description="Name of the tool, exactly 'run_command'")
    input: Optional[str] = Field(None, description="The system command to execute (e.g., 'mkdir my_app')")


msg_history = [{"role": "system", "content": system_prompt}]
user_query = input("\n👉 Enter your problem: ")
msg_history.append({"role": "user", "content": user_query})

print("\n🚀 Agent Initialized...\n")

while True:
    try:

        # Direct API call using the latest structured output syntax
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            text_format=output_format,
            input=msg_history,
        )
       
        # Extract the validated Pydantic object directly.
        ai_response = response.output_parsed

        # object to JSON string
        msg_history.append({"role": "assistant", "content": ai_response.model_dump_json()})

        # 1. ai is planning
        if ai_response.step == "plan":
            print(f"🧠 PLAN: {ai_response.content}")

        # 2. AI decides it needs to run a terminal cmd
        elif ai_response.step == "tool_call":
            print(f"🛠️ TOOL DECISION: Needs to run '{ai_response.tool}' with command:\n[{ai_response.input}]")

            if ai_response.tool in available_tools:
                # Execute the tool
                cmd_output = available_tools[ai_response.tool](ai_response.input)
                #  

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
            break

       
    except Exception as e:
        print(f"\n❌ : Error: {e}")
        break

print("\n✅ Agent Session Ended.\n")