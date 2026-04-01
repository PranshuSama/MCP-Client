#!/usr/bin/env python3
"""
FastMCP Math Server
Provides arithmetic and mathematical calculation tools via MCP protocol.
"""

from fastmcp import FastMCP
import math

# Create FastMCP server instance
mcp = FastMCP("Math Server")


@mcp.tool()
async def add(a: float, b: float) -> dict:
    """Add two numbers together."""
    result = a + b
    return {"operation": "add", "a": a, "b": b, "result": result}


@mcp.tool()
async def subtract(a: float, b: float) -> dict:
    """Subtract b from a."""
    result = a - b
    return {"operation": "subtract", "a": a, "b": b, "result": result}


@mcp.tool()
async def multiply(a: float, b: float) -> dict:
    """Multiply two numbers together."""
    result = a * b
    return {"operation": "multiply", "a": a, "b": b, "result": result}


@mcp.tool()
async def divide(a: float, b: float) -> dict:
    """Divide a by b. Returns error if b is zero."""
    if b == 0:
        return {"error": "Division by zero is not allowed", "operation": "divide"}
    result = a / b
    return {"operation": "divide", "a": a, "b": b, "result": result}


@mcp.tool()
async def modulo(a: float, b: float) -> dict:
    """Calculate the modulo (remainder) of a divided by b."""
    if b == 0:
        return {"error": "Modulo by zero is not allowed", "operation": "modulo"}
    result = a % b
    return {"operation": "modulo", "a": a, "b": b, "result": result}


@mcp.tool()
async def power(base: float, exponent: float) -> dict:
    """Raise base to the power of exponent."""
    result = base ** exponent
    return {"operation": "power", "base": base, "exponent": exponent, "result": result}


@mcp.tool()
async def square_root(n: float) -> dict:
    """Calculate the square root of a number."""
    if n < 0:
        return {"error": "Cannot calculate square root of negative number", "operation": "square_root"}
    result = math.sqrt(n)
    return {"operation": "square_root", "n": n, "result": result}


@mcp.tool()
async def absolute_value(n: float) -> dict:
    """Calculate the absolute value of a number."""
    result = abs(n)
    return {"operation": "absolute_value", "n": n, "result": result}


@mcp.tool()
async def floor(n: float) -> dict:
    """Round down to the nearest integer."""
    result = math.floor(n)
    return {"operation": "floor", "n": n, "result": result}


@mcp.tool()
async def ceil(n: float) -> dict:
    """Round up to the nearest integer."""
    result = math.ceil(n)
    return {"operation": "ceil", "n": n, "result": result}


@mcp.custom_route("/", methods=["GET"])
async def root(request):
    """Browser-friendly health check page."""
    return HTMLResponse("""
    <html>
        <head>
            <title>MCP Math Server</title>
            <style>
                body { font-family: -apple-system, system-ui, sans-serif; background: #0f172a; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .card { background: #1e293b; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #334155; text-align: center; }
                .status { color: #22c55e; font-weight: bold; margin-bottom: 1rem; }
                .url { background: #0f172a; padding: 0.5rem 1rem; border-radius: 0.5rem; font-family: monospace; color: #38bdf8; }
                h1 { margin-top: 0; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="status">● SERVER IS LIVE</div>
                <h1>MCP Math Server</h1>
                <p>To use this server, connect your MCP client to:</p>
                <div class="url">https://""" + request.headers.get("host", "your-url") + """/mcp</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 2rem;">Note: Browsers use GET requests. MCP uses POST. This page confirms the service is running.</p>
            </div>
        </body>
    </html>
    """)


if __name__ == "__main__":
    # Local default: stdio. For cloud deploy, set FASTMCP_TRANSPORT=streamable-http.
    transport = os.getenv("FASTMCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        path = os.getenv("MCP_PATH", "/mcp")
        mcp.run(transport="streamable-http", host=host, port=port, path=path)
    else:
        mcp.run(transport="stdio")
