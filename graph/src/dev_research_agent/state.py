"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class State:
    """Defines the input state for the agent, representing a narrower interface to the outside world.

    This class is used to define the initial state and structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    for more information.
    """

    input: str = ""
<<<<<<<< HEAD:graph/src/product_research_agent/state.py
    url: str = ""
========
    urls: str = ""
>>>>>>>> team-2:graph/src/dev_research_agent/state.py
    changeme: str = "example"
