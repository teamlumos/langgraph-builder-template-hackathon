"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

import asyncio
from graph.src.agent.graph import graph

graph = graph()

if __name__ == "__main__":
    def sync_call():
        # Sync call. Optionally use `graph.invoke_sync` if you need to run the graph synchronously.
        result = graph.invoke({"changeme": "start"})
        return result

    async def async_call():
        # Async call
        result = await graph.ainvoke({"changeme": "start"})
        return result

    result = asyncio.run(async_call())
    print(result, flush=True)
