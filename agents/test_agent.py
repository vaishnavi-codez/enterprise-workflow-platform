from agents.base_agent import Agent
agent = Agent(name="Planning Agent")

question = input("Enter your question: ")

try:
    answer = agent.think(question)
    print("\nAgent Response:")
    print(answer)

except Exception as e:
    print("\nError:")
    print(e)