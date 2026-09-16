# Development of Enterprise Workflow Platform with Decision Automation System

An AI-powered multi-agent decision automation platform built with **LangGraph, FastAPI, Groq, tool integration, memory, authentication, and a web interface**.

**Live Application:** https://enterprise-workflow-platform-chi.vercel.app/
**Backend API:** https://enterprise-workflow-platform.onrender.com

## Overview

The project was developed across four milestones, evolving from a basic LLM agent into a secure, integrated, and deployable multi-agent decision automation system.

### Milestone 1 — Agent Foundation

* Built a LangChain agent using Groq.
* Exposed the agent through a FastAPI `POST /ask` endpoint.
* Added Pydantic request and response validation.
* Added environment-based configuration.

### Milestone 2 — Tool Integration

* Integrated WeatherAPI and calculator tools.
* Enabled agent-based tool selection and execution.
* Added input validation and error handling.

### Milestone 3 — Multi-Agent Coordination & Memory

* Built a LangGraph workflow with Planning, Research, Analysis, and Decision agents.
* Implemented shared `AgentState` for communication between agents.
* Added short-term conversation memory.
* Added long-term memory using PostgreSQL and SQLAlchemy.
* Added session-based interactions and frontend integration.

### Milestone 4 — Security, Monitoring & Deployment

* Integrated the complete multi-agent system, tools, memory, and API.
* Added user registration and login with bcrypt and JWT authentication.
* Added session-level authorization and request validation.
* Added structured application logging and execution monitoring.
* Configured **Neon PostgreSQL** for cloud-based persistent storage.
* Deployed the backend on Render and frontend on Vercel.
* Verified end-to-end authentication, tool, memory, and workflow scenarios.

## System Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                                    v
                         ┌──────────────────────┐
                         │    Web Frontend      │
                         │    HTML / CSS / JS   │
                         └──────────┬───────────┘
                                    │
                                    v
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         │  API & Validation    │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    v                               v
          ┌──────────────────┐            ┌──────────────────┐
          │ Authentication   │            │ Session / Access │
          │ JWT + bcrypt     │            │   Authorization  │
          └──────────────────┘            └──────────────────┘
                                    │
                                    v
                         ┌──────────────────────┐
                         │ LangGraph Workflow   │
                         │  Shared AgentState   │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             v                      v                      v
      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
      │   Planning   │ ───> │   Research   │ ───> │   Analysis   │
      │    Agent     │      │    Agent     │      │    Agent     │
      └──────────────┘      └──────┬───────┘      └──────┬───────┘
                                   │                     │
                         ┌─────────┴─────────┐           │
                         │                   │           │
                         v                   v           │
                  ┌─────────────┐    ┌─────────────┐    │
                  │ Weather API │    │ Calculator  │    │
                  │    Tool     │    │    Tool     │    │
                  └─────────────┘    └─────────────┘    │
                                                        │
                                                        v
                                               ┌────────────────┐
                                               │ Decision Agent │
                                               └───────┬────────┘
                                                       │
                              ┌────────────────────────┴────────────────────┐
                              │                                             │
                              v                                             v
                    ┌──────────────────┐                         ┌────────────────────┐
                    │ Short-Term       │                         │ Long-Term Memory   │
                    │ Memory           │                         │ Neon PostgreSQL    │
                    └──────────────────┘                         └────────────────────┘
                              │                                             │
                              └──────────────────┬──────────────────────────┘
                                                 v
                                      ┌──────────────────────┐
                                      │    Final Response    │
                                      └──────────────────────┘
```

## Technology Stack

| Category          | Technologies                                          |
| ----------------- | ----------------------------------------------------- |
| Backend           | Python, FastAPI, LangChain, LangGraph, Groq, Pydantic |
| Database & Memory | Neon PostgreSQL, SQLAlchemy                           |
| Tools & APIs      | WeatherAPI, Calculator, Requests                      |
| Authentication    | JWT, bcrypt                                           |
| Frontend          | HTML, CSS, JavaScript                                 |
| Deployment        | Render, Vercel, Neon                                  |
| Version Control   | Git, GitHub                                           |

## Project Structure

```text
enterprise-workflow-platform/
├── agents/
│   ├── analysis_agent.py
│   ├── base_agent.py
│   ├── decision_agent.py
│   ├── planning_agent.py
│   ├── research_agent.py
│   ├── state.py
│   ├── test_agent.py
│   └── workflow.py
├── api/
│   ├── auth.py
│   ├── dependencies.py
│   └── main.py
├── config/
│   ├── database.py
│   └── settings.py
├── memory/
│   ├── database_models.py
│   ├── init_db.py
│   ├── long_term_memory.py
│   └── short_term_memory.py
├── monitoring/
│   └── logger.py
├── prompts/
├── tools/
│   ├── calculator_tool.py
│   └── weather_tool.py
├── Frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .env.example
├── .gitignore
├── requirements.txt
├── test_memory.py
├── tools.py
└── mian.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/vaishnavi-codez/enterprise-workflow-platform.git
cd enterprise-workflow-platform
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
DATABASE_URL=your_neon_postgresql_connection_string
SECRET_KEY=your_secret_key_here
```

Do not commit `.env` or real credentials to GitHub.

### 5. Start the backend

```bash
uvicorn api.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

For local frontend development, open `Frontend/index.html` or serve the `Frontend` directory using a local web server.

## Testing

The system was verified through end-to-end scenarios covering authentication, protected requests, tool execution, multi-agent workflows, short-term memory, long-term memory, validation, and error handling.

## Security

* Environment variables are used for API keys and database credentials.
* `.env` is excluded from version control.
* Passwords are hashed using bcrypt.
* JWT bearer tokens protect authenticated API access.
* Session ownership is validated before accessing existing sessions.
* Request validation is handled through Pydantic and application-level checks.

## Deployment

The application uses three cloud services:

* **Frontend:** Vercel
* **Backend:** Render
* **Database:** Neon PostgreSQL

The frontend communicates with the deployed FastAPI backend, which connects to Neon PostgreSQL for persistent data and long-term memory.

**Live Application:**
https://enterprise-workflow-platform-chi.vercel.app/

**Backend API:**
https://enterprise-workflow-platform.onrender.com

## Internship Context

Developed as part of the **Infosys Springboard Virtual Internship**, progressing through Milestones 1–4 from agent development and tool integration to multi-agent orchestration, memory, security, monitoring, testing, and deployment.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
