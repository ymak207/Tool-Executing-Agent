🛠 Tool-Executing Agent (Local LLM, CPU-First)

A deterministic, tool-executing AI agent built in pure Python that decides when to use tools vs when to use an LLM, running entirely on CPU using Ollama.

This project demonstrates production-grade agent fundamentals without heavy frameworks.

---

🚀 What This Project Does

The agent:

Accepts natural language input

Decides whether a tool is required

Executes the tool deterministically

Falls back to an LLM when no tool is needed

---

Supported Tools

🧮 Calculator (safe expression evaluation)

⏰ Current time tool

LLM

Local LLM via Ollama

No OpenAI / no cloud dependency

CPU-first design

---

📂 Project Structure
tool-executing-agent/
│
├── agent/
│ ├── agent.py # Core agent logic
│ ├── parser.py # Input parsing & routing helpers
│ └── prompt.txt # System prompt (LLM discipline)
│
├── llm/
│ ├── ollama_llm.py # Ollama LLM wrapper
│ └── mock_llm.py # Mock LLM for testing
│
├── tools/
│ ├── calculator.py # Calculator tool
│ └── time_tool.py # Time tool
│
├── test_agent.py # Manual test runner
├── requirements.txt
├── README.md
└── .env

---

🧠 How the Agent Works
1️⃣ Tool Decision

The agent inspects the user input and determines:

Tool required? → Execute tool

No tool needed? → Use LLM

"What is 25 \* (3 + 7)?" → Calculator
"What time is it now?" → Time tool
"What is capital of America?" → LLM

2️⃣ Deterministic Tool Execution

Mathematical expressions are extracted and validated

Parentheses are balanced

Only safe characters are allowed

Tools are executed without LLM hallucination

3️⃣ LLM Fallback

If no tool applies:

Prompt is sent to local Ollama model

Response is returned directly

---

🧪 Example Output
$ python test_agent.py

The current time is 11:58.
The result is 250.
Washington, D.C. is the capital of the United States.

---

⚙️ Setup Instructions

1️⃣ Create Virtual Environment
python -m venv .venv_toolexecutingagent
source .venv_toolexecutingagent/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Ollama

Ensure Ollama is running with a model installed:

ollama run llama3

4️⃣ Run Tests
python test_agent.py

---

Conversational Memory & Session Control (Extension)

---

This phase extends the Tool-Executing Agent with explicit, bounded conversational memory, enabling multi-turn reasoning and context continuity while remaining CPU-safe and deterministic.

All changes were implemented incrementally in the same repository.

---

🔖 Commit 1 — Bounded Conversational Memory

feat(agent): add bounded conversational memory with context injection

---

What Was Added

Short-term conversational memory (last N interactions)

Automatic context injection into LLM prompts

Memory trimming to prevent context explosion

Why This Matters

Stateless agents fail in real systems.

This change enables:

Follow-up questions

Contextual reasoning

Tool usage across turns

Without:

LangChain

Vector DBs

Heavy abstractions

---

How It Works (High Level)

Each user/assistant exchange is stored in memory

Memory is capped (FIFO eviction)

On each run:

Memory is formatted

Injected before the user prompt

Sent to the local LLM (Ollama)

Result

The agent can now handle conversations like:

User: What is 25 \* (3 + 7)?
User: Add 10 to that

---

🔖 Commit 2 — Memory Reset & Inspection
feat(agent): added memory reset

What Was Added

Explicit memory reset capability

Deterministic session control

Ability to start fresh conversations safely

Why This Matters

In production systems:

Sessions must be resettable

Context leakage is dangerous

Debugging requires memory visibility

This commit prepares the agent for:

Multi-user systems

Long-running services

Enterprise safety requirements

Example Use Cases

Restart a conversation cleanly

Prevent old context influencing new tasks

Debug agent behavior deterministically

---

🧪 How to Test this extension
python test_agent.py

Suggested flow:

Ask a question

Ask a follow-up that depends on prior context

Reset memory

Ask again and verify clean behavior

---
