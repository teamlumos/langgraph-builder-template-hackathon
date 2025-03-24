"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class State:
    """Defines the input state for the agent, representing a narrower interface to the outside world.

    This class is used to define the initial state and structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    for more information.
    """

    input: str = ""
    oas_discovery_report: str = ""
    oas_discovery_urls: str = ""
    oas_discovery_oas_url: str = ""
    pre_research_report: str = ""
    product_req_report: str = ""
    dev_req_report: str = ""
    oas_retrieval_report: str = ""
