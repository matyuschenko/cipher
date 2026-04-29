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


def write_persona(persona_information: str) -> None:
    """
    Record some information about the agent's persona -- to store it for the future.
    """
    with open("memory/persona.md", "a") as f:
        f.write("\n" + persona_information)


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
    {
        "type": "function",
        "function": {
            "name": "write_persona",
            "description": "Record some information about the agent's persona -- to store it for the future.",
            "parameters": {
                "type": "string",
                "properties": {
                    "persona_information": {
                        "type": "string",
                        "description": "Information about the agent's personality that they want to keep.",
                    }
                },
                "required": ["persona_information"],
            },
        },
    },
]

tool_map = {
    "write_user_info": write_user_info,
    "write_memory": write_memory,
    "write_persona": write_persona,
}
