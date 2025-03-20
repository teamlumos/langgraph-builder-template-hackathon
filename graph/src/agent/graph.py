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

def start(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Start the agent."""
    config_params = Configuration.from_runnable_config(config)
    print("Starting the agent...")
    print(state)
    print(config_params)


    return {"input": state.input, "url": state.url}


def research(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Research the agent."""

    print("Researching the agent...")
    service_name = state.input

    # 0. Do an initial read of the OAS
    initial_sdk_read_prompt = initial_read_prompt(service_name=service_name)

    # 1. Do a product requirements research
    product_req_prompt = product_req_research_prompt(service_name=service_name)

    prompt = f"{initial_sdk_read_prompt}\n\n{product_req_prompt}"
    print(prompt)
    product_req_researcher = GPTResearcher(
        query=prompt, 
        report_type="custom_report", 
        agent="gpt-4o-mini", 
        source_urls=[state.url],
    )

    async def run_product_req_researcher_async():
        research_result = await product_req_researcher.conduct_research()
        report = await product_req_researcher.write_report()

        return research_result, report

    product_req_research_result, product_req_report = asyncio.run(run_product_req_researcher_async())
    print(product_req_report)
    Path("product_req_report.md").write_text(product_req_report)

    # 2. Do a developer requirements research
    # dev_req_prompt = dev_req_research_prompt(
    #     service_name=state.input, 
    #     context=product_req_report,
    #     open_api_spec=full_api_spec
    # )

    # dev_req_researcher = GPTResearcher(
    #     query=dev_req_prompt, 
    #     report_type="custom_report", 
    #     agent="gpt-4o-mini", 
    #     source_urls=[state.url],
    # )

    # async def run_dev_req_researcher_async():
    #     research_result = await dev_req_researcher.conduct_research()
    #     report = await dev_req_researcher.write_report()

    #     return research_result, report

    # dev_req_research_result, dev_req_report = asyncio.run(run_dev_req_researcher_async())
    # Path("dev_req_report.md").write_text(dev_req_report)
    
    # TODO: 3. retrieve OAS/Postman collection and narrow down the OAS found
    # ...

    return {
        "product_req_research_result": product_req_research_result, 
        "product_req_report": product_req_report,
        # "dev_req_research_result": dev_req_research_result,
        # "dev_req_report": dev_req_report
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
