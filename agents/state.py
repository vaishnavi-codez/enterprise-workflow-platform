from typing import TypedDict


class AgentState(TypedDict, total=False):

    # User input
    user_query: str

    # Planning
    plan: list[str]

    # Research
    research_results: str

    # Analysis
    analysis: str

    # Final output
    final_decision: str

    # Memory
    conversation_history: list
    long_term_memories: list

    # Error handling
    error: str