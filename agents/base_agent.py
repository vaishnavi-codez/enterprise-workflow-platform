from langchain_groq import ChatGroq
from langchain.agents import create_agent

from config.settings import GROQ_API_KEY
from tools.weather_tool import get_weather


class Agent:

    def __init__(
        self,
        name: str,
        model: str = "llama-3.3-70b-versatile"
    ):
        self.name = name

        # Initialize the Groq LLM
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=model,
            temperature=0.7
        )

        # Register available tools
        self.tools = [
            get_weather
        ]

        # Create LangChain agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=(
                "You are a helpful AI agent. "
                "Answer general questions using your knowledge. "
                "When the user asks for current weather information, "
                "temperature, humidity, wind speed, or weather "
                "conditions for a city, use the weather tool. "
                "Do not use the weather tool for unrelated questions."
            )
        )

    def think(self, question: str) -> str:
        """
        Send a user question to the LangChain agent.

        The agent decides whether to answer directly
        or use an available tool.
        """

        result = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )

        # Get the final AI message
        return result["messages"][-1].content