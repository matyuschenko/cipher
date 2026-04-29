Cipher is an AI agent with long-term memory and a distinct persona, formed by you.

**Credentials Setup**
- Copy `config_example.py` to `config.py`
- Fill in your actual credentials
- `base_url` and `folder_id` are required by [Yandex Cloud](https://aistudio.yandex.ru); for other providers you can comment out the respective lines in OpenAI declaration of _agent.py_

You can fill _setup/user.md_ with any information you want the model to know about you.

Once set up, navigate to the project folder, run `python3 agent.py` and start chatting. Cipher will record important information and use it in future sessions.

Feel free to change the agent's personality in _setup/system_prompt.py_.

*Inspired by [Molty](https://www.molty.me/), and some of its and [Openclaw's](https://openclaw.ai/) approaches were reused in the system prompt.*
