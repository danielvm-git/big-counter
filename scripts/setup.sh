#!/usr/bin/env bash
# BCP Calculator — idempotent environment setup
# Safe to run multiple times. Each step checks if already done before acting.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== BCP Calculator Setup ==="

# 1. Python version check
PYTHON_MIN="3.10"
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python $PYTHON_MIN+."
    exit 1
fi
PYTHON_VER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "  Python: $PYTHON_VER (min $PYTHON_MIN)"

# 2. Virtual environment (idempotent)
if [ ! -d "venv" ]; then
    echo "  Creating venv..."
    python3 -m venv venv
else
    echo "  venv already exists, skipping"
fi

# 3. Dependencies (idempotent via pip's own caching)
echo "  Installing dependencies..."
venv/bin/pip install -q -r requirements.txt -r requirements-dev.txt

# 4. Environment file (idempotent — never overwrite)
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "  Created .env from .env.example — EDIT THIS FILE with your API keys"
    else
        echo "  WARNING: .env.example not found, skipping .env creation"
    fi
else
    echo "  .env already exists, skipping"
fi

# 5. Pre-commit hooks (idempotent)
if [ -f ".pre-commit-config.yaml" ] && [ ! -f ".git/hooks/pre-commit" ]; then
    echo "  Installing pre-commit hooks..."
    venv/bin/pre-commit install --hook-type pre-commit
elif [ -f ".git/hooks/pre-commit" ]; then
    echo "  Pre-commit hooks already installed, skipping"
fi

echo ""
echo "=== Setup complete ==="
echo "  Run tests:        venv/bin/python -m pytest tests/unit/ -v"
echo "  Run CLI:          venv/bin/python run_cli.py <story.md>"
echo "  Run API server:   venv/bin/python run_api_server.py"
echo "  Run MCP (stdio):  venv/bin/python run_mcp.py"
