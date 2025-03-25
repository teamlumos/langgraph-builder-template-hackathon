from typing import Tuple, Dict, Any, List, Generator
from graph.src.agent.graph import graph
agent = graph()
    
def run_agent(user_input: str, thread_id: str) -> Generator[str, None, None]:
    response = agent.stream(
        {"input": user_input}, {"configurable": {"thread_id": thread_id}},
        stream_mode="custom"
    )

    for chunk in response:
        yield f"**Agent:** {chunk}\n\n\n"
