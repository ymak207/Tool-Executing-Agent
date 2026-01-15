import re

def parse_tool_call(text: str):
    match = re.search(
        r"TOOL_CALL:\s*tool_name:\s*(\w+)\s*tool_input:\s*(.+)",
        text,
        re.DOTALL
    )
    if not match:
        return None

    return {
        "tool_name": match.group(1).strip(),
        "tool_input": match.group(2).strip()
    }
