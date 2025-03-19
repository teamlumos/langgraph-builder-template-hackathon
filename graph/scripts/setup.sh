BASE_DIR=$(dirname "$0")/..

# Check for Python installation
if command -v "uv" &>/dev/null; then
    PYTHON="uv run python"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Check for npm installation
if ! command -v "npm" &>/dev/null; then
    brew install npm
else
    echo "npm is already installed"
fi

# Check for nodemon installation
if ! command -v "nodemon" &>/dev/null; then
    npm i -g nodemon
else
    echo "nodemon is already installed"
fi

uv sync --extra dev --project $BASE_DIR
