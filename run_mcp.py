import logging

from mcp.server.fastmcp import FastMCP

from src.bcp.bcp_calculator import BCPCalculator
from src.bcp.logger import setup_logger

# Initialize FastMCP server
mcp = FastMCP("bcp-calculator-mcp")

logger = setup_logger(logging.INFO)


@mcp.tool()
async def calculate_bcp(story_content: str, provider: str = "deepseek") -> dict:
    """Calculate BCP.

    Args:
        story: User story content
        provider: LLM provider to use (openai or claude)
    """
    """Start BCP calculation job."""
    calculator = BCPCalculator(logger, provider_name=provider)
    result = calculator.calculate_bcp(story_content)

    return {"result": result}


if __name__ == "__main__":
    logger.info("MCP Server starting...")
    mcp.run(transport="stdio")
