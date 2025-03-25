# Integration Research Agent
This repository contains a specialized agent designed for researching API integrations. It uses LangGraph, Streamlit, and GPT-Researcher to automate the discovery and analysis of third-party APIs.
## Overview
1. Discovering OpenAPI Specifications (OAS)
2. Researching product requirements
3. Analyzing developer requirements
4. Retrieving API documentation
The agent follows a structured workflow to gather comprehensive information about services, making it easier to plan and implement integrations.
## Project Structure

```
.
├── graph/                  # LangGraph agent implementation
│   ├── src/                # Source code for the agent
│   │   ├── agent/          # Agent implementation
│   │   └── prompts/        # Prompts for different research stages
│   └── scripts/            # Scripts for running and managing the agent
├── streamlit/              # Streamlit web interface
│   ├── app.py              # Main application entry point
│   ├── pages/              # Additional pages for the web interface
│   └── utils.py            # Utility functions for the web interface
├── scripts/                # Project management scripts
│   ├── start.sh            # Start the Streamlit server
│   └── deploy.sh           # Deploy the application
└── my-docs/                # Generated research documents
```

## Components
The core research agent is implemented using LangGraph, which orchestrates a series of specialized research steps:
- **OAS Discovery**: Finds OpenAPI Specifications for the target service
- **Pre-Research**: Gathers initial information about the service
- **Product Requirements Research**: Analyzes product features, tiers, and limitations
- **Developer Requirements Research**: Examines authentication, pagination, and API endpoints
- **OAS Retrieval**: Retrieves detailed API specifications
Each step is implemented as a node in the LangGraph workflow, with specialized agents handling different aspects of the research process.
### Streamlit Interface
- Create new research sessions
- View and edit research results
- Navigate between different research documents
- Interact with the agent through a chat interface
The interface is designed to make it easy to review and refine the research results.
## Getting Started
### Prerequisites
- Python 3.9-3.11
- [uv](https://github.com/astral-sh/uv) (Python package manager)
### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/integration-research-agent.git
cd integration-research-agent
```
2. Install dependencies:
```bash
uv sync
```
3. Start the Streamlit server:
```bash
uv run scripts/start.sh
```
This will launch the web interface at http://localhost:5002.
## Usage
1. Open the web interface
2. Create a new session
3. Enter the name of the service you want to research (e.g., "Slack", "GitHub", "Salesforce")
4. Wait for the agent to complete its research
5. Review and edit the generated documents
## Development
### Running the LangGraph Studio
For development and debugging of the agent graph:
```bash
cd graph
./scripts/langgraph-studio.sh
```

### Linting
Run linting checks:
```bash
cd graph
./scripts/lint.sh
```

## Environment Variables
Create a .env file with the following variables:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
```
