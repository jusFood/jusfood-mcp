from mcp.server.fastmcp import FastMCP

mcp = FastMCP("jusfood")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b