"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from typing import Any, Dict, Literal

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from .configuration import Configuration
from .state import State


def start(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Start the agent."""
    return {"changeme": "done"}


def graph() -> StateGraph:
    # Define a new graph
    workflow = StateGraph(State, config_schema=Configuration)

    # Add the nodes to the graph
    workflow.add_node("start", start)

    workflow.add_edge("__start__", "start")
    workflow.add_edge("start", "__end__")

    # Compile the workflow into an executable graph
    graph = workflow.compile()
    graph.name = "New Graph"  # This defines the custom name in LangSmith

    return graph
