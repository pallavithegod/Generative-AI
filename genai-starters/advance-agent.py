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

# Directory Confinement (Sandboxing)
def write_file(filepath: str, file_content: str):
    print(f"\n📝 WRITING FILE: {filepath}")
    try:
        # sandbox= cwd
        # abspath turn relative path to full
        workspace_dir = os.path.abspath(os.getcwd())

        # see the path that the ai has requested
        target_path = os.path.abspath(filepath)

        # intersection of path = common path to check
        if os.path.commonpath([workspace_dir, target_path]) != workspace_dir:
            print("🛑 SECURITY BLOCK: Agent tried to escape the sandbox!")
            return f"Access Denied: You are restricted to the workspace folder ({workspace_dir}). You cannot access or modify external files."

        # ensures subdir exist fisr where ai want to work
        target_dir = os.path.dirname(target_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok = True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(file_content)

        return f"Success: File '{filepath}' created successfully."
    
    except Exception as e:
        return f"Error writing file: {e}"
    
available_tools = {
    "run_command": run_command,
    "write_file": write_file
}

system_prompt = """
You are an expert Autonomous AI Assistant.
You solve problems by using a loop of PLAN -> TOOL_CALL -> OUTPUT.

Rules:
1. Break down the task into logical steps.
2. If you need to interact with the computer, output a 'tool_call' step.
3. Wait for the user system to provide the OBSERVATION from your tool.
4. Once the task is complete, provide an 'output' step.

Available Tools:
- 'run_command': Use this to run terminal commands (e.g., mkdir, npm install, dir).
- 'write_file': Use this to create or modify code files. Provide the 'filepath' and clean, multi-line 'file_content'. NEVER use run_command to echo or cat text into a file.
"""

class output_format(BaseModel):
    step: str = Field(..., description="Must be exactly one of: 'plan', 'tool_call', 'output'")
    content: Optional[str] = Field(None, description="Your thought process or final answer")
    tool: Optional[str] = Field(None, description="Name of the tool: 'run_command' or 'write_file'")
    input: Optional[str] = Field(None, description="The system command to execute (if using run_command)")
    filepath: Optional[str] = Field(None, description="Path of the file to save (if using write_file)")
    file_content: Optional[str] = Field(None, description="The multi-line code/text to save (if using write_file)")


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
            print(f"🛠️ TOOL DECISION: Needs to run '{ai_response.tool}'")

            if ai_response.tool == "run_command":
                print(f"[{ai_response.input}]")
                cmd_output = available_tools["run_command"](ai_response.input)
                # availabl_tools = dict
                # ai_response.tool = run_command (here)
                # ai_response.input = terminal command to execute
                # hence, run_command(mkdir tic-tac-toe)

            elif ai_response.tool == "write_file":
                print(f"[Target: {ai_response.filepath}]")
                cmd_output = available_tools["write_file"](ai_response.filepath, ai_response.file_content)
            
            else:
                # Failsafe
                cmd_output = f"⚠️ ERROR: Tool '{ai_response.tool}' does not exist."


            print(f"🖥️ SYSTEM OUTPUT:\n{cmd_output}\n")    
            msg_history.append({
                    "role": "user", 
                    "content": f"OBSERVATION from {ai_response.tool}:\n{cmd_output}\nWhat is the next step?"
            })

        # 3. task completed successfully
        elif ai_response.step == "output":
            print(f"📢 FINAL OUTPUT: {ai_response.content}")
            break

       
    except Exception as e:
        print(f"\n❌ : Error: {e}")
        break

print("\n✅ Agent Session Ended.\n")