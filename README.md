# LangGraph Builder Template

Welcome to the LangGraph Builder Template! This template serves as a starting point for building applications using LangGraph, a powerful framework for creating language-based applications.

This is a ready-to-use template for building applications using LangGraph and encapsulates the graph in the `graph` directory so that you can use LangStudio to build your application in a new or existing application.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Easy setup for LangGraph applications
- Modular architecture for scalability
- Customizable agent configurations
- Simple state management for agents

## Installation

To get started with your LangGraph application, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/langgraph-builder-template.git
   cd langgraph-builder-template
   ```

2. **Install dependencies:**

   Make sure you have Python 3.7 or higher installed. Then, install the required packages using pip:

   ```bash
   ./graph/scripts/setup.sh
   ```

3. **Set up your environment:**

   Create a `.env` file in the root directory and configure your environment variables as needed.

4. **Run the application:**

   ```bash
   ./graph/scripts/start.sh
   ```

## Usage

### Using LangStudio

Download LangStudio and open the graph directory. You can start building your application by defining agents and their configurations.

### Using Terminal

```bash
./graph/scripts/start.sh
```

### Integrating into an existing application

Notice that `pyproject.toml` and `langgraph.json` are required by LangStudio, so they've been added in the `graph` folder for convenience and should not conflict with existing dependency and configuration files in the top-level of your application.

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### About the Author

Armando Murga [[LinkedIn]](https://linkedin.com/in/armandomurga) is a seasoned technical leader with 15+ years of expertise in full-stack development. Currently the Lead Principal Software Engineer at Gusto, spearheading R&D initiatives within the AI Core Platform team to integrate AI and LLM technologies into Gusto's suite of products. Gusto is a premier cloud-based platform catering to payroll and benefits needs for small and medium-sized businesses. Open to advisory roles, board positions, and other exciting opportunities.
