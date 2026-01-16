from agent.agent import Agent

agent = Agent()

print(agent.run("Hello"))
print(agent.run("My name is Yash"))
print(agent.run("What is my name?"))

print("\n--- MEMORY ---")
print(agent.run("show memory"))

print("\n--- RESET ---")
print(agent.run("reset session"))

print("\n--- AFTER RESET ---")
print(agent.run("What is my name?"))
