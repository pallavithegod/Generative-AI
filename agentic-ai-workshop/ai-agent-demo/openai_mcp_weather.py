import json
import logging
import sys
import requests

from shared_utils import OPENAI_MODEL, get_openai_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# -------------------- TOOLS --------------------

def get_coordinates(city: str):
    logger.info("Fetching coordinates for city: %s", city)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    res = requests.get(url).json()

    if "results" not in res:
        logger.warning("City not found in geocoding response: %s", city)
        return {"error": "City not found"}

    loc = res["results"][0]
    return {
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
        "name": loc["name"]
    }


def get_weather(latitude: float, longitude: float):
    logger.info("Fetching weather for coordinates: %s, %s", latitude, longitude)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    res = requests.get(url).json()
    return res.get("current_weather", {})


# -------------------- AGENT --------------------

def run_agent(prompt: str):
    logger.info("Running weather tool-calling agent.")
    client = get_openai_client()

    # System + User input
    input_messages = [
        {
            "role": "system",
            "content": (
                "You are a weather assistant.\n"
                "- Extract city from user query.\n"
                "- First call get_coordinates.\n"
                "- Then call get_weather.\n"
                "- Always use tools, never guess.\n"
                "- Return short and clear answer."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    #  Tool definitions
    tools = [
        {
            "type": "function",
            "name": "get_coordinates",
            "description": "Get latitude and longitude of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        },
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get weather using latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    ]

    # Safety: avoid infinite loops
    MAX_STEPS = 5

    response = client.responses.create(model=OPENAI_MODEL, input=input_messages, tools=tools)

    for step in range(MAX_STEPS):
        output_types = [getattr(item, "type", "unknown") for item in response.output]
        logger.info("Weather agent step %s output types: %s", step + 1, output_types)

        function_calls = [item for item in response.output if getattr(item, "type", "") == "function_call"]

        # ---------------- FINAL ANSWER ----------------
        if not function_calls:
            final_text = (response.output_text or "").strip()
            if not final_text:
                logger.warning(
                    "Weather agent returned empty output_text. response_id=%s output_types=%s",
                    response.id,
                    output_types,
                )
                return "I could not generate a weather response. Please try again."

            logger.info("Weather agent returned final response.")
            return final_text

        # ---------------- TOOL CALL ----------------
        tool_outputs = []
        for call in function_calls:
            tool_name = call.name
            logger.info("Tool call requested: %s", tool_name)

            raw_args = call.arguments
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError as exc:
                    logger.exception("Failed to parse tool arguments for '%s': %s", tool_name, raw_args)
                    args = {"_raw": raw_args, "error": str(exc)}
            else:
                args = raw_args

            try:
                if tool_name == "get_coordinates":
                    result = get_coordinates(args["city"])
                elif tool_name == "get_weather":
                    result = get_weather(args["latitude"], args["longitude"])
                else:
                    logger.error("Unknown tool requested by model: %s", tool_name)
                    result = {"error": "Unknown tool"}
            except Exception as e:
                logger.exception("Tool execution failed for '%s': %s", tool_name, e)
                result = {"error": str(e)}

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                }
            )

        response = client.responses.create(
            model=OPENAI_MODEL,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools,
        )

    logger.error("Weather agent exceeded max steps (possible loop).")
    return "Error: Too many steps (possible loop)"


# -------------------- MAIN --------------------

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What's the weather in Delhi today?"
    result = run_agent(prompt)
    print(result)


if __name__ == "__main__":
    main()