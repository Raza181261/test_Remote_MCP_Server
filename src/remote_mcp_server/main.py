from fastmcp import FastMCP
import random
import json

# create an instance of FastMCP
mcp = FastMCP("Simple Calculator Server")

# tool: Add two numbers
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers.
    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b


# Tool: Generate a random number
@mcp.tool
def random_number(min_value: int = 1, max_value: int = 100) -> int:
    """
    Generate a random number within a specified range.

    Args:
        min_value (int): The minimum value (inclusive).
        max_value (int): The maximum value (inclusive).

    Returns:
        int: A random number within the specified range.
    """
    return random.randint(min_value, max_value)


# Resource: Server information
@mcp.resource("info://server")
def server_info() -> dict:
    """
    Get information about the server.
    """
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0",
        "description": "A simple calculator server that can add numbers and generate random numbers.",
        "tools": ["add", "random_number"],
        "authors": ["Your Name"],
    }
    return json.dumps(info, indent=2)

def main():
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
    )

if __name__ == "__main__":
    main()


# Start the server
# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8000)