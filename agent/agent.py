import re
from tools.calculator import calculate
from tools.time_tool import current_time
from llm.ollama_llm import OllamaLLM


def decide_tool(user_input: str):
    text = user_input.lower()

    if any(op in text for op in ["+", "-", "*", "/", "(", ")"]):
        return "calculator"

    if "time" in text:
        return "time"

    return None


def extract_expression(text: str) -> str:
    match = re.search(r"(\d[\d\s+\-*/().]*\d|\d)", text)
    if not match:
        raise ValueError("No valid math expression found")

    return match.group(1).strip()


def is_balanced(expression: str) -> bool:
    stack = []
    for ch in expression:
        if ch == "(":
            stack.append(ch)
        elif ch == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0


class Agent:
    def __init__(self, memory_limit: int = 6):
        self.llm = OllamaLLM()
        self.memory = []
        self.memory_limit = memory_limit

    # 🔐 SYSTEM COMMANDS (NO LLM)
    def reset_session(self):
        self.memory.clear()
        return "Session reset. Memory cleared."

    def inspect_memory(self):
        if not self.memory:
            return "Memory is empty."

        return "\n".join(
            f"{i+1}. {m['role']}: {m['content']}"
            for i, m in enumerate(self.memory)
        )

    def add_to_memory(self, role: str, content: str):
        self.memory.append({"role": role, "content": content})
        if len(self.memory) > self.memory_limit:
            self.memory = self.memory[-self.memory_limit:]

    def run(self, user_input: str) -> str:
        command = user_input.lower().strip()

        # 🛑 INTERCEPT SYSTEM COMMANDS
        if command == "reset session":
            return self.reset_session()

        if command == "show memory":
            return self.inspect_memory()

        tool = decide_tool(user_input)

        if tool is None:
            prompt = self.build_prompt(user_input)
            response = self.llm.generate(prompt).strip()
            self.add_to_memory("user", user_input)
            self.add_to_memory("assistant", response)
            return response

        if tool == "calculator":
            return self.run_calculator(user_input)

        if tool == "time":
            return self.run_time()

        return "Unsupported tool requested."

    def build_prompt(self, user_input: str) -> str:
        context = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in self.memory
        )
        return f"{context}\nUser: {user_input}" if context else user_input

    def run_calculator(self, user_input: str) -> str:
        try:
            expression = extract_expression(user_input)
            expression = re.sub(r"[^\d+\-*/().\s]", "", expression)

            if not is_balanced(expression):
                return "Calculation error: unbalanced parentheses."

            result = calculate(expression)
            response = f"The result is {result}."

            self.add_to_memory("user", user_input)
            self.add_to_memory("assistant", response)

            return response

        except Exception as e:
            return f"Calculation error: {e}"

    def run_time(self) -> str:
        response = f"The current time is {current_time()}."
        self.add_to_memory("user", "What time is it?")
        self.add_to_memory("assistant", response)
        return response
