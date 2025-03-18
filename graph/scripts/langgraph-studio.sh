BASE_DIR=$(dirname "$0")/..

# Check for Python installation
if command -v "uv" &>/dev/null; then
    PYTHON="uv run python"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

uv run langgraph dev
