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
        user_urls_input = input("URLs: ")
        user_context_input = """
## Resources & Entitlement Diagram + Details

### Account

| Account type |   |
| --- | --- |
| - User |  |

### **Resource Types**

| Resource Type |  |
| --- | --- |
| - Global Resource |  |

### **Entitlement Types**

| In Scope (Y/N) | Entitlement Type | Column Name | Resource Type | Min | Max | Assignable | Standard or Custom | Documentation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y | Role |  | Global Resource  | 0 | * | N/A | Standard  | https://help.rapid7.com/insightAccount/en-us/api/v1/docs.html#tag/Roles/operation/getCustomerRoles |
| Y | Group | User Groups | Global Resource  |  |  |  |  |  |

### Relationship Diagram

```mermaid
graph TD
  
  
  B[Group] --> |contains| C(Users)
  
  A[Role] --> |can be assigned to| C[Users]
```

## **Supports usage data?**

| In Scope? | Usage Data | Definition | Available via API? |
| --- | --- | --- | --- |
|  | Last Login | Last time someone logged into the application | Y |
|  | Last Activity  |  | N |
"""

        
        # Exit condition
        if user_urls_input.lower() in ['quit', 'exit', 'bye'] or user_context_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
    
        result = graph.invoke({"input": user_context_input, "urls": user_urls_input})
        print(result, flush=True)
