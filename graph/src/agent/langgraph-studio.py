"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from graph.src.agent.graph import graph

compiled_graph = graph()

if __name__ == "__main__":
    print("Starting the agent...")
    thread_id = "1"
    while True:
        # Get user input from console
        service_input = input("Service name: ")

        result = compiled_graph.invoke(
            {"input": service_input}, {"configurable": {"thread_id": thread_id}}
        )
        print(result)
