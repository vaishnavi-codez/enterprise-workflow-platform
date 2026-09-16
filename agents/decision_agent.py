from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY
from agents.state import AgentState


class DecisionAgent:

    def __init__(self,model: str = "openai/gpt-oss-120b"):
        self.name = "Decision Agent"

        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=model,
            temperature=0.1
        )

    def run(self, state: AgentState) -> AgentState:

        if state.get("error"):
            return state

        query = state.get("user_query", "")
        research = state.get("research_results", "")
        analysis = state.get("analysis", "")

        if not research.strip():
            return {
                **state,
                "error": "Decision Agent cannot proceed because research results are missing."
            }

        if not analysis.strip():
            return {
                **state,
                "error": "Decision Agent cannot proceed because analysis is missing."
            }

        prompt = f"""
You are the Decision Agent in a multi-agent AI system.

Your responsibility is to provide the final answer to the user.

Use the Research Agent results and Analysis Agent output.
Do not ignore factual tool results.

IMPORTANT:
- If the Research Agent provides a calculator result, use that result.
- If the Research Agent provides weather data, use that weather data.
- Never replace valid tool results with a statement saying that
  real-time data is unavailable.
- Do not invent facts.
- Do not mention internal agents or implementation details.
- Keep the answer concise and directly answer the user's question.

User request:
{query}

Research Agent results:
{research}

Analysis Agent output:
{analysis}

Return ONLY the final answer for the user.
"""

        try:
            response = self.llm.invoke(prompt)

            return {
                **state,
                "final_decision": response.content.strip()
            }

        except Exception as e:
            return {
                **state,
                "error": f"Decision Agent failed: {str(e)}"
            }