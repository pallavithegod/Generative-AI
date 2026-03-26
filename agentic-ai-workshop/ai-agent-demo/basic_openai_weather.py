import logging

from shared_utils import OPENAI_MODEL, get_openai_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def get_basic_llm_response(message: str, instruction: str | None = None) -> str:
    logger.info("Generating direct LLM response.")
    client = get_openai_client()
    system_instruction = instruction or "You are a helpful assistant. Answer clearly and briefly."

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": message},
        ],
    )
    logger.info("Direct LLM response generated successfully.")
    return response.output_text


def run_chat():
    logger.info("Starting interactive chat session.")
    client = get_openai_client()

    #  Conversation history (memory)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful weather assistant.\n"
                "- Answer clearly and briefly.\n"
                "- If unsure, say it's an estimate.\n"
                "- Maintain conversation context."
            )
        }
    ]

    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            logger.info("Chat session ended by user.")
            break

        # Add user message to history
        messages.append({
            "role": "user",
            "content": user_input
        })

        # Call LLM with full history
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=messages
        )

        answer = response.output_text

        # Add assistant response to history
        messages.append({
            "role": "assistant",
            "content": answer
        })

        print(f"Bot: {answer}\n")
        logger.info("Assistant response sent in chat session.")


if __name__ == "__main__":
    run_chat()