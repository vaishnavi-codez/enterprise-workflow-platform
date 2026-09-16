from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY
from agents.state import AgentState


class AnalysisAgent:

    def __init__(self, model: str = "openai/gpt-oss-120b"):
        self.name = "Analysis Agent"

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

        conversation_history = state.get(
            "conversation_history", []
        )

        long_term_memories = state.get(
            "long_term_memories", []
        )

        # Do not call the LLM with empty research.
        if not research.strip():
            return {
                **state,
                "analysis": "No research information was returned."
            }

        prompt = f"""
You are the Analysis Agent in a multi-agent AI system.

Your job is to analyze the information returned by the Research Agent
and produce a concise factual analysis for the Decision Agent.

IMPORTANT:
- Use the Research Agent's results as the primary source.
- Do not ignore tool results.
- Do not claim that real-time information is unavailable if the Research
  Agent already provided current tool data.
- Do not invent information.
- For simple calculations, preserve the calculated result.
- For weather requests, preserve the city, temperature, condition,
  humidity and wind speed returned by the weather tool.

User request:
{query}

Research Agent results:
{research}

Previous conversation:
{conversation_history}

Relevant long-term memories:
{long_term_memories}

Return a concise analysis containing:
1. Relevant facts
2. Important conclusion
3. Any limitation, only if one actually exists
"""

        try:
            response = self.llm.invoke(prompt)

            return {
                **state,
                "analysis": response.content
            }

        except Exception as e:
            return {
                **state,
                "error": f"Analysis Agent failed: {str(e)}"
            }