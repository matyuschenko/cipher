import base64
import json

from openai import OpenAI

from config import API_KEY, BASE_URL, FOLDER_ID, MODEL
from setup.system_prompt import SYSTEM_PROMPT
from tools import tool_map, tools


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def parse_user_input(ui: str):
    if ui.startswith("cmd_read_image "):
        ui_spl = ui.split(" ")
        base_image = encode_image(ui_spl[1])
        ui_text = " ".join(ui_spl[2:])
        return [
            {"type": "text", "text": ui_text},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base_image}"},
            },
        ]
    else:
        return [{"type": "text", "text": ui}]


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    default_headers={"x-folder-id": FOLDER_ID},  # project is transfered via header
)

# system prompt
# with open("setup/system_prompt.md") as f:
#     SYSTEM_PROMPT = f.read().strip()
messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def chat(user_input, messages, tools):
    """Send user message, handle tool‑call loop, return final text reply."""
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            # temperature=0,
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message
        messages.append(msg)

        if msg.tool_calls:
            for tc in msg.tool_calls:
                func_name = tc.function.name
                func = tool_map[func_name]
                args = json.loads(tc.function.arguments)
                print(f"tool called: {func_name}, args: {args}")
                result = func(**args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    }
                )
            # loop back so the model can process tool results
        else:
            return {"content": msg.content, "messages": messages}


# interactive terminal loop
if __name__ == "__main__":
    while True:
        try:
            user_input = input(">>> You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "stop"):
            break

        user_input = parse_user_input(user_input)

        result = chat(user_input, messages, tools)
        messages = result["messages"]
        print(f"\n<<< Assistant: {result['content']}\n")
