BASE_DIR=$(dirname "$0")/..

# Check for Python installation
if command -v "uv" &>/dev/null; then
    PYTHON="uv run --project $BASE_DIR python"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Check for nodemon installation
if ! command -v nodemon &>/dev/null; then
    echo "Installing nodemon for hot-reloading..."
    npm install -g nodemon
fi

# Run services concurrently with hot-reloading
nodemon --exec "$PYTHON -m graph.src.dev_research_agent.langgraph-studio" --watch "graph/" --ext "py"

# Trap SIGINT to kill all background processes
trap "kill 0" SIGINT

wait