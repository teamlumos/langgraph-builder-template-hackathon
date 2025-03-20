"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from pathlib import Path

from graph.src.agent.graph import graph

compiled_graph = graph()

if __name__ == "__main__":
    print("Starting the agent...")
    
    while True:
        # Get user input from console
        url_input = input("docs URL: ")
        service_input = input("Service name: ")
        
        result = compiled_graph.invoke({"input": service_input, "url": url_input})

