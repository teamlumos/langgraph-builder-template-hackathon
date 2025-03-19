BASE_DIR=$(dirname "$0")/..

# Check for Python installation
if command -v "uv" &>/dev/null; then
    echo "uv is installed"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

uv run --project $BASE_DIR langgraph dev
