# Development of Enterprise Workflow Platform with Decision Automation System

An AI-powered multi-agent decision automation system built using **LangChain, LangGraph, Groq, FastAPI, PostgreSQL, and external tools**.

## Milestone 1 - Agent Foundation Development

### Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run

```bash
uvicorn api.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to test.

### What's built

* Basic LangChain Agent using Groq LLM
* FastAPI `POST /ask` endpoint
* Pydantic request/response validation

## Milestone 2 - Tool Integration & Intelligent Action Execution

### What's new

* Weather Tool for retrieving current weather information using WeatherAPI
* Calculator Tool for basic mathematical calculations
* Tool selection and execution through the agent
* Input validation and error handling for tool operations

### Setup

Add the WeatherAPI key to `.env`:

```env
WEATHER_API_KEY=your_weather_api_key_here
```

The WeatherAPI key can be obtained from the WeatherAPI website.

## Milestone 3 - Multi-Agent Coordination, Decision Automation & Memory

### What's new

* Multi-agent workflow using **LangGraph**
* Planning Agent for breaking requests into tasks
* Research Agent for collecting information and using available tools
* Analysis Agent for analyzing research results
* Decision Agent for generating the final response
* Shared state between agents
* Short-term and long-term memory using **PostgreSQL**
* Error handling and validation between workflow stages
* Simple web frontend for interacting with the system

### Workflow

```text
User
  ↓
FastAPI
  ↓
Planning Agent
  ↓
Research Agent
  ↓
Analysis Agent
  ↓
Decision Agent
  ↓
Final Response
```

### PostgreSQL Setup

PostgreSQL is required for Milestone 3 memory functionality.

1. Install PostgreSQL and ensure the PostgreSQL service is running.
2. Create a database named `ai_agent_db`.
3. Add the database connection details to `.env`:

```env
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/ai_agent_db
```

4. Initialize the database tables:

```bash
python memory/init_db.py
```

### Complete `.env`

```env
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/ai_agent_db
```

### Frontend

After starting the FastAPI server, open:

```text
Frontend/index.html
```

The frontend communicates with the FastAPI `/ask` endpoint and supports session-based conversations.

### Project Structure

```text
ai-agent-coordination-engine-teamB/
├── agents/
│   ├── analysis_agent.py
│   ├── decision_agent.py
│   ├── planning_agent.py
│   ├── research_agent.py
│   ├── state.py
│   └── workflow.py
├── api/
│   └── main.py
├── config/
│   ├── database.py
│   └── settings.py
├── memory/
│   ├── database_models.py
│   ├── init_db.py
│   ├── long_term_memory.py
│   └── short_term_memory.py
├── tools/
│   ├── calculator_tool.py
│   └── weather_tool.py
├── Frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── test_memory.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

### Technologies

**Python · LangChain · LangGraph · Groq · FastAPI · PostgreSQL · SQLAlchemy · Pydantic · WeatherAPI · Requests · Git/GitHub**

> **Security:** API keys and database credentials are stored locally in `.env`. The `.env` file is excluded from Git; only `.env.example` is committed.
