"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

import os
from typing import Any, Dict
from pathlib import Path

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from gpt_researcher import GPTResearcher
import asyncio

from .configuration import Configuration
from .state import State
from graph.src.prompts.product_req_research import product_req_research_prompt
from graph.src.prompts.sdk_open_api import initial_read_prompt
from graph.src.prompts.pre_research import pre_research_prompt

import time

from graph.src.agent.agent import PreResearchAgent, ProductReqResearchAgent, DevReqResearchAgent

def start(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Start the agent."""
    config_params = Configuration.from_runnable_config(config)
    print("Starting the agent...")
    print(state)
    print(config_params)


    return {"input": state.input, "url": state.url}


def research(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Research the agent."""

    # agent = "gpt-4o"
    # agent = "google_genai:gemini-1.5-pro"
    agent = "anthropic:claude-3-7-sonnet-latest"
    service_name = state.input

    print("Starting research...\nSCRAPER: ", os.getenv("SCRAPER"))

    # 0. Initialize 
    pre_research_agent = PreResearchAgent(agent, service_name, [state.url])

    # 1. Do a pre-research
    async def pre_research() -> str:
        try:
            _, pre_research_report = await pre_research_agent.research()
            print(pre_research_report)
            Path("pre_research_report.md").write_text(pre_research_report)
        except Exception as e:
            print(f"Error in pre-research: {e}")
            raise e
        
        return pre_research_report
        
    pre_research_report = asyncio.run(pre_research())

    time.sleep(20)


    # 2. Do a product requirements research
    product_req_research_agent = ProductReqResearchAgent(agent, service_name, [state.url], pre_research_report)

    async def product_req_research() -> str:
        try:
            _, product_req_report = await product_req_research_agent.research()
            print(product_req_report)
            Path("product_req_report.md").write_text(product_req_report)
        except Exception as e:
            print(f"Error in product requirements research: {e}")
            raise e
        
        return product_req_report

    product_req_report = asyncio.run(product_req_research())

    time.sleep(20)

    # 3. Do a developer requirements research
    dev_req_research_agent = DevReqResearchAgent(agent, service_name, [state.url], pre_research_report)

    async def dev_req_research() -> str:
        try:
            _, dev_req_report = await dev_req_research_agent.research()
            print(dev_req_report)
            Path("dev_req_report.md").write_text(dev_req_report)
        except Exception as e:
            print(f"Error in developer requirements research: {e}")
            raise e
        
        return dev_req_report

    dev_req_report = asyncio.run(dev_req_research())
    
    # TODO: 3. retrieve OAS/Postman collection (currently manually done)

    return {
        # "product_req_research_result": product_req_research_result, 
        "product_req_report": product_req_report,
        # "dev_req_research_result": dev_req_research_result,
        "dev_req_report": dev_req_report
    }


def graph():
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
