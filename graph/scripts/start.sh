BASE_DIR=$(dirname "$0")/..

# Check for Python installation
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

$PYTHON -m venv $BASE_DIR/.venv
source $BASE_DIR/.venv/bin/activate

cd $BASE_DIR/src
$PYTHON -m agent.langgraph-studio