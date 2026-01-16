import re
from tools.calculator import calculate
from tools.time_tool import current_time
from llm.ollama_llm import OllamaLLM
from agent.memory import ConversationMemory



def decide_tool(user_input: str):
    text = user_input.lower()

    if any(op in text for op in ["+", "-", "*", "/", "(", ")"]):
        return "calculator"

    if "time" in text:
        return "time"

    return None


def extract_expression(text: str) -> str:
    """
    Extract math expression safely from natural language.
    Strategy:
    - Keep only math characters
    - Trim leading/trailing operators
    - Auto-fix unbalanced parentheses
    """
    cleaned = re.sub(r"[^0-9+\-*/().]", "", text)

    if not cleaned:
        raise ValueError("No valid math expression found")

    # Balance parentheses automatically
    open_count = cleaned.count("(")
    close_count = cleaned.count(")")

    if open_count > close_count:
        cleaned += ")" * (open_count - close_count)
    elif close_count > open_count:
        cleaned = cleaned.lstrip(")")

    return cleaned


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
    def __init__(self):
        self.llm = OllamaLLM()
        self.memory = ConversationMemory(max_turns=5)

    def run(self, user_input: str) -> str:
        self.memory.add_user(user_input)
    
        tool = decide_tool(user_input)
    
        if tool == "calculator":
            response = self.run_calculator(user_input)
            self.memory.add_assistant(response)
            return response
    
        if tool == "time":
            response = self.run_time()
            self.memory.add_assistant(response)
            return response
    
        prompt = self.build_prompt(user_input)
        response = self.llm.generate(prompt).strip()
    
        self.memory.add_assistant(response)
        return response


    def run_calculator(self, user_input: str) -> str:
      try:
        expression = extract_expression(user_input)

        if not is_balanced(expression):
            return "Calculation error: unbalanced parentheses."

        result = calculate(expression)
        return f"The result is {result}."
      except Exception as e:
        return f"Calculation error: {e}"

    def run_time(self) -> str:
        return f"The current time is {current_time()}."
    
    
    def build_prompt(self, user_input: str) -> str:
        context = ""
    
        for msg in self.memory.get_context():
            role = msg["role"].capitalize()
            context += f"{role}: {msg['content']}\n"
    
        context += f"User: {user_input}\nAssistant:"
    
        return context
    
