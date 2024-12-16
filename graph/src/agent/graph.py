"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

import os
from typing import Literal

import requests
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command, interrupt
from tavily import TavilyClient

from .configuration import Configuration
from .state import SearchState


# Node: Interpret Query
def interpret_query(state: SearchState) -> SearchState:
    """Interpret the user's query."""

    print("interpret_query", state)

    # Simulate LLM parsing (replace with actual LLM calls)
    state.filters = {
        "location": "SF Bay Area",
        "type": "daycare",
    }
    state.status = "query_interpreted"
    return state


def search_with_tavily(state: SearchState) -> SearchState:
    """Search with Tavily."""

    print("search_with_tavily", state)
    params = {
        "query": state.filters.get("type", "daycare"),
        "location": state.filters.get("location", "SF Bay Area"),
        "radius": 50,
        "limit": 10,
    }

    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

        response = client.search(", ".join(f"{k}: {v}" for k, v in params.items()))
        # Normalize Tavily results
        state.results = [
            {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
                "score": result["score"],
                "raw_content": result["raw_content"],
            }
            for result in response["results"]
        ]
        state.status = "results_found"
    except Exception as e:
        state.results = []
        state.status = f"error: {str(e)}"

    return state


# Node: Apply Filters (Validate Japanese Offering)
def scrape_website_for_japanese(website_url: str) -> bool:
    """Scrape website for Japanese criteria."""

    print("scrape_website_for_japanese", website_url)
    return True

    try:
        response = requests.get(website_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        keywords = ["Japanese", "日本語", "language immersion", "bilingual"]
        content = soup.get_text().lower()

        return any(keyword.lower() in content for keyword in keywords)
    except Exception:
        return False


def apply_filters(state: SearchState) -> SearchState:
    """Apply filters to results."""

    print("apply_filters", state)
    filtered_results = []
    for result in state.results:
        website = result.get("url")
        if website and scrape_website_for_japanese(website):
            filtered_results.append(result)

    state.results = filtered_results
    state.status = "results_filtered"
    return state


def human_review(state: SearchState) -> Command[Literal[END]]:
    """Human review of results."""

    print("human_review", state)
    interrupt({"results": state.results, "state": state})

    if state.user_query == "yes":
        state.status = "review_completed"
        return Command(goto=END, update=state)
    else:
        state.status = "review_completed_retry"
        return Command(goto="interpret_query", update=state)


def should_apply_filters(state: MessagesState) -> Literal["apply_filters", END]:
    """Whether to apply filters."""

    print("should_apply_filters", state)
    if state.status == "results_found":
        return "apply_filters"
    return END


def graph() -> StateGraph:
    """Define and Compile the Graph."""

    graph = StateGraph(SearchState, config_schema=Configuration)
    checkpointer = MemorySaver()

    # Add nodes
    graph.add_node("interpret_query", interpret_query)
    graph.add_node("search_with_tavily", search_with_tavily)
    graph.add_node("apply_filters", apply_filters)
    graph.add_node("human_review", human_review)

    # Add edges
    graph.add_edge(START, "interpret_query")
    graph.add_edge("interpret_query", "search_with_tavily")
    graph.add_edge("search_with_tavily", "apply_filters")
    graph.add_conditional_edges("search_with_tavily", should_apply_filters)
    graph.add_edge("apply_filters", "human_review")

    graph.add_edge("human_review", END)

    graph.name = "New Graph"

    return graph.compile(checkpointer=checkpointer)
