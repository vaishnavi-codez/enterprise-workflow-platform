from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY
from agents.state import AgentState

from tools.weather_tool import get_weather
from tools.calculator_tool import calculator_tool

from monitoring.logger import logger


class ResearchAgent:

    def __init__(self, model: str = "openai/gpt-oss-120b"):

        self.name = "Research Agent"

        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=model,
            temperature=0.2
        )

        self.tools = {
            "get_weather": get_weather,
            "calculator_tool": calculator_tool
        }

        self.llm_with_tools = self.llm.bind_tools(
            list(self.tools.values())
        )

    def run(self, state: AgentState) -> AgentState:

        if state.get("error"):
            return state

        query = state["user_query"]

        plan = state.get(
            "plan",
            []
        )

        conversation_history = state.get(
            "conversation_history",
            []
        )

        long_term_memories = state.get(
            "long_term_memories",
            []
        )

        logger.info(
            f"Research Agent started | question={query}"
        )

        # Log weather tool access for weather-related questions
        weather_keywords = [
            "weather",
            "rain",
            "raining",
            "temperature",
            "humidity",
            "wind",
            "forecast",
            "climate"
        ]

        if any(
            keyword in query.lower()
            for keyword in weather_keywords
        ):
            logger.info(
                "Weather-related query detected | "
                "Weather Tool available: get_weather | "
                "Weather Tool access: ENABLED"
            )

        logger.info(
            "Research Agent tools available | "
            "get_weather, calculator_tool"
        )

        prompt = f"""
You are the Research Agent in a multi-agent AI system.

Your responsibility is to collect accurate information required
to answer the user's request.

User request:
{query}

Plan:
{plan}

Previous conversation:
{conversation_history}

Relevant long-term memories:
{long_term_memories}

Available tools:

1. get_weather(city)
   Use this for current weather information.

2. calculator_tool
   Use this for mathematical calculations.

IMPORTANT WEATHER RULES:

- If the user asks about current weather, use get_weather.
- If multiple cities are mentioned, call get_weather for each
  requested city when possible.
- Do not ignore available weather tool results.
- Do not claim real-time weather is unavailable if the tool
  provides the required information.

IMPORTANT CALCULATION RULES:

- If the user asks for a calculation, use calculator_tool.
- Preserve the calculated result.

For requests that do not require a tool, use the LLM's
general knowledge.

Collect the required information and return concise research results.
"""

        try:

            response = self.llm_with_tools.invoke(
                [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Execute requested tools
            if response.tool_calls:

                tool_results = []

                logger.info(
                    f"Research Agent tool calls detected | "
                    f"count={len(response.tool_calls)}"
                )

                for tool_call in response.tool_calls:

                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]

                    logger.info(
                        f"Research Agent calling tool | "
                        f"tool={tool_name} | args={tool_args}"
                    )

                    if tool_name not in self.tools:
                        raise ValueError(
                            f"Unknown tool requested: {tool_name}"
                        )

                    tool = self.tools[tool_name]

                    result = tool.invoke(tool_args)

                    logger.info(
                        f"Research Agent tool completed | "
                        f"tool={tool_name}"
                    )

                    tool_results.append(
                        f"{tool_name}: {result}"
                    )

                research_results = "\n".join(
                    tool_results
                )

            else:

                research_results = response.content

            if not research_results:
                research_results = (
                    "No additional research was required."
                )

            logger.info(
                "Research Agent completed successfully"
            )

            return {
                **state,
                "research_results": research_results
            }

        except Exception as e:

            logger.exception(
                f"Research Agent failed | error={str(e)}"
            )

            return {
                **state,
                "error": f"Research Agent failed: {str(e)}"
            }