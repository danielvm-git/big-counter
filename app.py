#!/usr/bin/env python3
"""
BCP Calculator — BigBase Deployment Entry Point

BigBase runs `python3 app.py` for Python apps. It auto-detects Python when
app.py or main.py exists at the repo root. The PORT env var is injected by
BigBase's proxy.

Pipeline:
    git push → pip install -r requirements.txt → python3 app.py
"""

import logging
import os

from dotenv import load_dotenv

from run_mcp_http_server import create_mcp_server
from src.bcp.logger import setup_logger

load_dotenv()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "51617"))
    logger = setup_logger(logging.INFO)
    logger.info(f"BCP MCP Server starting on port {port} (BigBase deployment)")

    mcp = create_mcp_server(host="0.0.0.0", port=port)
    mcp.run(transport="streamable-http")
