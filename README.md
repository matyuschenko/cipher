Cipher is an AI agent with long-term memory and a distinct persona shaped by you.

**Credentials Setup**
- Copy `config_example.py` to `config.py`
- Fill in your actual credentials
- `base_url` and `folder_id` are required by [Yandex Cloud](https://aistudio.yandex.ru); for other providers you can comment out the respective lines in OpenAI declaration of _agent.py_

You can add any information you want the model to know about you to `setup/user.md`.

Once everything is set up, navigate to the project folder, run `python3 agent.py` and start chatting. Cipher will record important information and use it in future sessions.

Feel free to change the agent's personality in _setup/system_prompt.py_.

*Cipher was inspired by [Molty](https://www.molty.me/), and some approaches from Molty and [Openclaw](https://openclaw.ai/) were reused in the system prompt.*
