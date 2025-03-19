BASE_DIR=$(dirname "$0")/..

# Check for Python installation
if command -v "uv" &>/dev/null; then
    PYTHON="uv run --project $BASE_DIR python"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

$PYTHON $BASE_DIR/../graph/scripts/lint.py
