from app.ai.prompts import SYSTEM_PROMPT


def build_prompt(history, current_message: str):

    prompt = SYSTEM_PROMPT + "\n\n"

    for item in history:
        role = "User" if item.role == "user" else "Assistant"
        prompt += f"{role}: {item.message}\n"

    prompt += f"\nUser: {current_message}\nAssistant:"

    return prompt