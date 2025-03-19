"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

import asyncio

from graph.src.agent.graph import graph

graph = graph()

if __name__ == "__main__":
    print("Starting the agent...")
    
    while True:
        # Get user input from console
        user_input = input("You: ")
        
        # Exit condition
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
    
        result = graph.invoke({"input": user_input})
        print(result, flush=True)
