from collections import deque
from typing import List, Dict


class ConversationMemory:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.messages: deque = deque(maxlen=max_turns * 2)

    def add_user(self, text: str):
        self.messages.append({"role": "user", "content": text})

    def add_assistant(self, text: str):
        self.messages.append({"role": "assistant", "content": text})

    def get_context(self) -> List[Dict[str, str]]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()
