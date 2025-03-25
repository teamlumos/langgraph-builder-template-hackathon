"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, Generator

import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt
from langgraph.types import StreamWriter
from graph.src.agent.agent import (
    DevReqResearchAgent,
    OASDiscoveryAgent,
    OASRetrievalAgent,
    PreResearchAgent,
    ProductReqResearchAgent,
)
from langchain_core.output_parsers import StrOutputParser
from .configuration import Configuration
from .state import State


def summarize(text: str) -> str:
    """Summarize the text."""
    prompt = ChatPromptTemplate.from_template(
        """
        Summarize the following text in 30 words or less:
        <text>
        {text}
        </text>

        Return the summary exclusively, without any other text.
        """
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": text})

def start(state: State, config: RunnableConfig, writer: StreamWriter) -> Dict[str, Any]:
    """Start the agent."""
    writer("Starting the agent.")
    config_params = Configuration.from_runnable_config(config)
    
    # Create directory if it doesn't exist
    Path(f"my-docs/{config_params.thread_id}").mkdir(parents=True, exist_ok=True)
    writer("Creating directory for the agent.")
    return {"input": state.input, "thread_id": config_params.thread_id}


def oas_discovery(state: State, writer: StreamWriter) -> Dict[str, Any]:
    """OAS discovery."""
    writer("OAS discovery...")
    service_name = state.input
    oas_discovery_agent = OASDiscoveryAgent(None, service_name)

    async def oas_discovery() -> str:
        try:
            oas_discovery_report, oas_url_list = await oas_discovery_agent.research()
            Path(f"my-docs/{state.thread_id}/1_oas_discovery_report.md").write_text(oas_discovery_report)
            Path(f"my-docs/{state.thread_id}/2_oas_url_list.md").write_text(oas_url_list)

            writer(summarize(oas_discovery_report))
        except Exception as e:
            writer(f"Error in OAS discovery: {e}")
            print(f"Error in OAS discovery: {e}")
            raise e

        return oas_discovery_report, oas_url_list

    oas_discovery_report, oas_url_list = asyncio.run(oas_discovery())

    return {
        "oas_discovery_report": oas_discovery_report,
        "oas_discovery_urls": oas_url_list,
    }


def oas_discovery_url(state: State) -> Dict[str, Any]:
    """Get the OAS URL."""

    prompt = ChatPromptTemplate.from_template(
        """
        Select the highest confidence OAS URL from the following list:
        <urls>
        {oas_discovery_urls}
        </urls>

        Return the URL exclusively, without any other text. If there's no URL, return "".
        """
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm
    oas_url = chain.invoke({"oas_discovery_urls": state.oas_discovery_urls})
    return {"oas_discovery_oas_url": oas_url.content}


def pre_research(state: State, writer: StreamWriter) -> Dict[str, Any]:
    """Pre-research."""
    service_name = state.input
    writer("Pre-research...")

    def fetch_html(url: str) -> str:
        """Fetches HTML content from a given URL.
        
        Args:
            url (str): The URL to fetch content from
            
        Returns:
            str: The HTML content of the page, or error message if fetch fails
        """

        try:
            from playwright.sync_api import sync_playwright

            html = ""
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                page.wait_for_load_state('networkidle')

                html = page.locator('body').all_text_contents()
                
                browser.close()
                
            return html

        except requests.RequestException as e:
            return f"Error fetching URL: {str(e)}"
    
    html = fetch_html(state.oas_discovery_oas_url)

    # 0. Initialize
    pre_research_agent = PreResearchAgent(
        None, service_name, html
    )

    # 1. Do a pre-research
    async def pre_research() -> str:
        try:
            _, pre_research_report = await pre_research_agent.research()
            writer(summarize(pre_research_report))
            Path(f"my-docs/{state.thread_id}/3_pre_research_report.md").write_text(pre_research_report)
        except Exception as e:
            writer(f"Error in pre-research: {e}")
            print(f"Error in pre-research: {e}")
            raise e

        return pre_research_report

    pre_research_report = asyncio.run(pre_research())

    return {"pre_research_report": pre_research_report}


def product_req_research(state: State, writer: StreamWriter) -> Dict[str, Any]:
    """Product requirements research."""
    agent = "anthropic:claude-3-7-sonnet-latest"
    service_name = state.input
    writer("Product requirements research...")

    # 2. Do a product requirements research
    product_req_research_agent = ProductReqResearchAgent(
        agent, service_name, [state.oas_discovery_oas_url], state.pre_research_report
    )

    async def product_req_research() -> str:
        try:
            _, product_req_report = await product_req_research_agent.research()
            writer(summarize(product_req_report))
            Path(f"my-docs/{state.thread_id}/4_product_req_report.md").write_text(product_req_report)
        except Exception as e:
            writer(f"Error in product requirements research: {e}")
            print(f"Error in product requirements research: {e}")
            raise e

        return product_req_report

    product_req_report = asyncio.run(product_req_research())

    return {"product_req_report": product_req_report}


def dev_req_research(state: State, writer: StreamWriter) -> Dict[str, Any]:
    """Developer requirements research."""
    agent = "anthropic:claude-3-7-sonnet-latest"
    service_name = state.input
    writer("Developer requirements research...")

    # 3. Do a developer requirements research
    dev_req_research_agent = DevReqResearchAgent(
        agent, service_name, [state.oas_discovery_oas_url], state.pre_research_report
    )

    async def dev_req_research() -> str:
        try:
            _, dev_req_report = await dev_req_research_agent.research()
            writer(summarize(dev_req_report))
            Path(f"my-docs/{state.thread_id}/5_dev_req_report.md").write_text(dev_req_report)
        except Exception as e:
            writer(f"Error in developer requirements research: {e}")
            print(f"Error in developer requirements research: {e}")
            raise e

        return dev_req_report

    dev_req_report = asyncio.run(dev_req_research())

    return {"dev_req_report": dev_req_report}


# TODO: This is a placeholder for the OAS retrieval agent
def oas_retrieval(state: State, writer: StreamWriter) -> Dict[str, Any]:
    """OAS retrieval."""
    agent = "anthropic:claude-3-7-sonnet-latest"
    service_name = state.input
    writer("OAS retrieval...")
    # TODO: 4. retrieve OAS/Postman collection (currently manually done)
    oas_retrieval_agent = OASRetrievalAgent(
        agent, service_name, [state.oas_discovery_oas_url]
    )

    async def oas_retrieval() -> str:
        try:
            _, oas_retrieval_report = await oas_retrieval_agent.research()
            writer(summarize(oas_retrieval_report))
            Path(f"my-docs/{state.thread_id}/6_oas_retrieval_report.md").write_text(oas_retrieval_report)
        except Exception as e:
            print(f"Error in OAS retrieval: {e}")
            raise e

        return oas_retrieval_report

    oas_retrieval_report = asyncio.run(oas_retrieval())

    return {"oas_retrieval_report": oas_retrieval_report}


def graph():
    # Define a new graph
    workflow = StateGraph(State, config_schema=Configuration)

    memory = MemorySaver()

    # Add the nodes to the graph
    workflow.add_node("start", start)
    workflow.add_node("oas_discovery", oas_discovery)
    workflow.add_node("oas_discovery_url", oas_discovery_url)
    workflow.add_node("pre_research", pre_research)
    workflow.add_node("product_req_research", product_req_research)
    workflow.add_node("dev_req_research", dev_req_research)
    workflow.add_node("oas_retrieval", oas_retrieval)

    workflow.add_edge("__start__", "start")
    workflow.add_edge("start", "oas_discovery")
    workflow.add_edge("oas_discovery", "oas_discovery_url")
    workflow.add_edge("oas_discovery_url", "pre_research")
    workflow.add_edge("pre_research", "product_req_research")
    workflow.add_edge("product_req_research", "dev_req_research")
    workflow.add_edge("dev_req_research", "__end__")

    # Compile the workflow into an executable graph
    graph = workflow.compile(checkpointer=memory)
    graph.name = "CLI Graph"

    return graph
