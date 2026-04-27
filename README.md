Cipher is an AI agent with long-term memory and a distinct persona.

This repository requires a few extra files to work properly:
- _config.py_: specifying API key and model name; as well as `base_url` and `folder_id` required by Yandex Cloud (for other providers you can comment out the respective lines in _agent.py_)
- _memory/memory.md_: blank by default
- _memory/persona.md_: blank by default
- _memory/user.md_: blank by default
- _setup/user.md_: containing any information you want the model to know about you

Once set up, navigate to the project folder, run `python3 agent.py` and start chatting. Cipher will record important information and use it in future sessions.

Feel free to change the agent's personality in _setup/system_prompt.py_.

Inspired by [Molty](https://www.molty.me/), and some of its and [Openclaw's](https://openclaw.ai/) approaches were reused in the system prompt.
