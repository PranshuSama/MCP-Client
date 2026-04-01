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


if __name__ == "__main__":
    mcp.run()
