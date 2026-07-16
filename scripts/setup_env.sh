#!/bin/bash
set -e

echo "============================================="
echo "  THE COUNCIL: ENVIRONMENT SETUP"
echo "================================l"

# Exit if not in the project directory
if [[ "$PWD" != *"/the-council"* ]]; then
    echo "Error: Please run this script from the /home/anonz/Documents/the-council directory."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[STEP 1] Creating Virtual Environment..."
    python3 -m venv .venv
else
    echo "[INFO] Virtual environment (.venv) already exists."
fi

# Activate the environment
source .venv/bin/activate

# Install system-level requirements for development
echo "[STEP 2] Installing core dependencies (numpy, pandas, matplotlib)..."
pip install --upgrade pip
pip install numpy pandas matplotlib scipy

# Install the project itself in editable mode to solve the ModuleNotFoundError issue
echo "[STEP 3] Installing The Council as an editable package..."
if [ -f "pyproject.toml" ]; then
    pip install -e .
else:
    echo "Error: pyproject.lml not found. Cannot perform editable install."
    exit 1

echo ""
echo "============================================="
echo "  ✅ SETUP COMPLETE. USE THE FOLLOWING TO START:"
echo ". .venv/bin/activate"
echo "============================================="
