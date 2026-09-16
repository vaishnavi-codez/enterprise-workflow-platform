import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import agent_tools

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Milestone 2 - Agent Tool Integration API",
    description="LangChain Agent API with Groq LLM, Calculator, and Weather tools.",
    version="1.0.0"
)

# Initialize Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in .env file")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# Define Agent Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant capable of using specialized tools for math calculations and weather inquiries. "
               "When a user asks a question, intelligently select the appropriate tool if required. "
               "If no tool is needed, answer directly using your language capabilities."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create Agent and Executor
agent = create_tool_calling_agent(llm, agent_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=agent_tools, verbose=True)

# Request schema
class QueryRequest(BaseModel):
    prompt: str

# API Endpoint
@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        response = agent_executor.invoke({"input": request.prompt})
        return {
            "status": "success",
            "user_query": request.prompt,
            "agent_response": response["output"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Execution Error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Milestone 2 Agent API is running!"}