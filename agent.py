import json

from openai import OpenAI

from config import API_KEY, BASE_URL, FOLDER_ID, MODEL
from setup.system_prompt import SYSTEM_PROMPT

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    default_headers={"x-folder-id": FOLDER_ID},  # project is transfered via header
)

# system prompt
# with open("setup/system_prompt.md") as f:
#     SYSTEM_PROMPT = f.read().strip()
messages = [{"role": "system", "content": SYSTEM_PROMPT}]


# tool definitions
def write_user_info(user_information: str) -> None:
    """
    Record some information about user to the agent's long term memory.
    """
    with open("memory/user.md", "a") as f:
        f.write("\n" + user_information)


def write_memory(memory_information: str) -> None:
    """
    Record some information (other than related to the user) to the agent's long term memory.
    """
    with open("memory/memory.md", "a") as f:
        f.write("\n" + memory_information)


tools = [
    {
        "type": "function",
        "function": {
            "name": "write_user_info",
            "description": "Record some information about user to the agent's long term memory.",
            "parameters": {
                "type": "string",
                "properties": {
                    "user_information": {
                        "type": "string",
                        "description": "Information about user which may be useful in the future.",
                    }
                },
                "required": ["user_information"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_memory",
            "description": "Record some information (other than related to the user) to the agent's long term memory.",
            "parameters": {
                "type": "string",
                "properties": {
                    "memory_information": {
                        "type": "string",
                        "description": "Information (not about the user) which may be useful in the future.",
                    }
                },
                "required": ["memory_information"],
            },
        },
    },
]

tool_map = {
    "write_user_info": write_user_info,
    "write_memory": write_memory,
}


def chat(user_input: str, messages, tools):
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

        result = chat(user_input, messages, tools)
        messages = result["messages"]
        print(f"\n<<< Assistant: {result['content']}\n")
