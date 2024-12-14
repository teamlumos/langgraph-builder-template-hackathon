"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

import asyncio

from agent.graph import graph
from agent.state import SearchState
from dotenv import load_dotenv

load_dotenv()

initial_state = SearchState(
    user_query="Find pre-K schools in SF Bay Area that offer Japanese."
)
graph = graph()
if __name__ == "__main__":

    def print_results(state: SearchState):
        """Print results."""

        print("Filtered Results:")
        for result in state.results:
            print(f"Name: {result['name']}")
            print(f"Location: {result['location']}")
            print(f"Website: {result['website']}")
            print(f"Rating: {result['rating']}")
            print("-" * 40)

    def sync_call():
        """Sync call. Optionally use `graph.invoke_sync` if you need to run the graph synchronously."""

        result = graph.invoke(initial_state, {"configurable": {"thread_id": 1}})
        return result

    async def async_call():
        """Async call."""

        result = await graph.ainvoke(initial_state, {"configurable": {"thread_id": 1}})
        return result

    result = asyncio.run(async_call())
    print(result, flush=True)
