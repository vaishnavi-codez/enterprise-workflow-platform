from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY
from agents.state import AgentState


class PlanningAgent:

    def __init__(self, model: str = "openai/gpt-oss-120b"):
        self.name = "Planning Agent"

        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=model,
            temperature=0.2
        )

    def run(self, state: AgentState) -> AgentState:

        if state.get("error"):
            return state

        query = state["user_query"]

        conversation_history = state.get(
            "conversation_history", []
        )

        long_term_memories = state.get(
            "long_term_memories", []
        )

        prompt = f"""
You are the Planning Agent in a multi-agent AI system.

Your responsibility is to break the user's request into clear tasks
that other agents can execute.

User request:
{query}

Previous conversation:
{conversation_history}

Relevant long-term memories:
{long_term_memories}

Use the previous conversation and memories when they are relevant
to understanding the current request.

Create a short numbered plan.

Return ONLY the tasks, one task per line.
"""

        try:
            response = self.llm.invoke(prompt)

            tasks = [
                line.strip()
                for line in response.content.splitlines()
                if line.strip()
            ]

            return {
                **state,
                "plan": tasks
            }

        except Exception as e:
            return {
                **state,
                "error": f"Planning Agent failed: {str(e)}"
            }