"""forge-forge MCP server — thin shell over `lib.py`.

Tools:
  forge_find         — "I need to do X" → here's the forge for that
  forge_list         — list all forges (optionally filter by type)
  forge_info         — full details on a specific forge
  forge_how          — invocation instructions for a forge
  forge_for_project  — recommend forges for a project's filesystem signals

All real logic lives in `lib.py`. This file only translates between MCP's
typed tool API and the plain functions.
"""

from mcp.server.fastmcp import FastMCP

import lib

mcp = FastMCP("eidos-forge-forge")


@mcp.tool()
def forge_find(query: str, top_k: int = 3) -> dict:
    """Find the best forge for a task.

    Args:
        query: What you need to do, in plain language.
              Examples: "test my API", "release on PyPI", "write a book"
        top_k: Number of results to return (default 3).
    """
    return lib.find_forges(query, top_k)


@mcp.tool()
def forge_list(type_filter: str = "") -> dict:
    """List all forges in the Eidos ecosystem.

    Args:
        type_filter: Optional — "knowledge" or "tool" to filter by type.
    """
    return lib.list_forges(type_filter)


@mcp.tool()
def forge_info(name: str) -> dict:
    """Get full details on a specific forge.

    Args:
        name: Forge name (e.g. "test-forge", "ml-forge").
    """
    return lib.get_forge_info(name)


@mcp.tool()
def forge_how(name: str) -> dict:
    """How to use a specific forge right now — prerequisites, invocation, expected output.

    Args:
        name: Forge name (e.g. "improve-forge", "loss-forge").
    """
    return lib.get_forge_how(name)


@mcp.tool()
def forge_for_project(path: str = ".", description: str = "") -> dict:
    """Recommend forges for a project based on its characteristics.

    Args:
        path: Path to the project root (default: current dir).
        description: Optional description of what the project does.
    """
    return lib.recommend_for_project(path, description)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
