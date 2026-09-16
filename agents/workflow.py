from langgraph.graph import StateGraph, START, END

from agents.state import AgentState
from agents.planning_agent import PlanningAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent


planning_agent = PlanningAgent()
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
decision_agent = DecisionAgent()


def planning_node(state: AgentState):
    return planning_agent.run(state)


def research_node(state: AgentState):
    return research_agent.run(state)


def analysis_node(state: AgentState):
    return analysis_agent.run(state)


def decision_node(state: AgentState):
    return decision_agent.run(state)


def build_workflow():

    workflow = StateGraph(AgentState)

    workflow.add_node("planning", planning_node)
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("decision", decision_node)

    workflow.add_edge(START, "planning")
    workflow.add_edge("planning", "research")
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "decision")
    workflow.add_edge("decision", END)

    return workflow.compile()


app_workflow = build_workflow()