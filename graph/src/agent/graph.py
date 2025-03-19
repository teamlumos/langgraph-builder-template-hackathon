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
    config_params = Configuration.from_runnable_config(config)
    print("Starting the agent...")
    print(state)
    print(config_params)

    return {"input": state.input}


def research(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Research the agent."""

    print("Researching the agent...")

    from gpt_researcher import GPTResearcher
    import asyncio

    researcher = GPTResearcher(query=state.input, report_type="research_report", agent="gpt-4o-mini")

    async def run_async():
        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report

    research_result, report = asyncio.run(run_async())
    print(research_result, flush=True)
    print(report, flush=True)
    return {"research_result": research_result, "report": report}


def graph() -> StateGraph:
    # Define a new graph
    workflow = StateGraph(State, config_schema=Configuration)

    # Add the nodes to the graph
    workflow.add_node("start", start)
    workflow.add_node("research", research)
    workflow.add_edge("__start__", "start")
    workflow.add_edge("start", "research")
    workflow.add_edge("research", "__end__")

    # Compile the workflow into an executable graph
    graph = workflow.compile()
    graph.name = "New Graph"  # This defines the custom name in LangSmith

    return graph
