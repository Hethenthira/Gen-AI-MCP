from fastmcp import FastMCP
import requests
from urllib.parse import quote

mcp = FastMCP("search_wikipedia")


@mcp.tool()
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia and return a short summary.
    """

    encoded_query = quote(query.replace(" ", "_"))

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"

    response = requests.get(
        url,
        headers={
            "User-Agent": "MCP-Wikipedia-Client/1.0"
        },
        timeout=10
    )

    if response.status_code != 200:
        return f"Wikipedia request failed: HTTP {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        return "Wikipedia returned an invalid response."

    summary = data.get("extract")

    if not summary:
        return f"No summary found for '{query}'."

    return summary


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        path="/mcp"
    )