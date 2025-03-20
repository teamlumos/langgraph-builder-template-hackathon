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

    return {"input": state.input, "urls": state.urls}



def get_improved_prompt(context: str, urls: str) -> str:

    prompt = (
    f"""
<goal>
- Understand the context: what is the account, what are the resources, what are the entitlements, what are the relationships between them.
- Follow the context to research the API endpoints.
- Identify authentication methods and implementation details.
- Analyze pagination structure and parameters.
- Locate OpenAPI Specification (OAS) references or documentation links.
- Provide the OpenAPI Specification (OAS) URL in the output.
- Follow the output-format to generate the output.

</goal>

<context>
{context}
</context>

<important-URLs>
{urls}
</important-URLs>

<output-format>
## Authentication

...fill in

- **Scope Requirements**
...fill in

| Tenant ID |  Details (How is the tenant ID identified) |
| --- | --- |
| ...fill in | ...fill in |


## API Endpoints

...fill in

**Milestone 1: Read Capabilities** 

## List user accounts, resources, and entitlements

...fill in

**Milestone 2: Write Capabilities** 

### Deprovisioning

...fill in

### Provisioning

...fill in

### OpenAPI Specification (OAS) URL

...fill in

</output-format>
  """
) 
    return prompt


def research(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Research the agent."""

    print("Researching the agent...")

    from gpt_researcher import GPTResearcher
    import asyncio

    researcher = GPTResearcher(query=get_improved_prompt(state.input, state.urls), report_type="custom_report", agent="gpt-4o-mini")

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
