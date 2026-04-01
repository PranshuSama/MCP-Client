#!/usr/bin/env python3
"""
FastMCP Expense Tracking Server
Provides expense tracking and management tools via MCP protocol.
"""

from fastmcp import FastMCP
from datetime import datetime
from typing import Dict, List
from starlette.responses import HTMLResponse
import os
import json

# Create FastMCP server instance
mcp = FastMCP("Expense Server")

# Simple in-memory expense storage
expenses: List[Dict] = []


@mcp.tool()
async def add_expense(amount: float, category: str, description: str, date: str = None) -> dict:
    """Add a new expense entry. Date format: YYYY-MM-DD (defaults to today)."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    expenses.append(expense)
    return {"status": "success", "expense": expense}


@mcp.tool()
async def get_all_expenses() -> dict:
    """Retrieve all expenses."""
    return {"expenses": expenses, "total": len(expenses)}


@mcp.tool()
async def get_expenses_by_category(category: str) -> dict:
    """Get all expenses for a specific category."""
    category_expenses = [e for e in expenses if e["category"].lower() == category.lower()]
    total = sum(e["amount"] for e in category_expenses)
    return {"category": category, "expenses": category_expenses, "total": total}


@mcp.tool()
async def get_expenses_by_date(date: str) -> dict:
    """Get all expenses for a specific date (format: YYYY-MM-DD)."""
    date_expenses = [e for e in expenses if e["date"] == date]
    total = sum(e["amount"] for e in date_expenses)
    return {"date": date, "expenses": date_expenses, "total": total}


@mcp.tool()
async def get_total_expenses() -> dict:
    """Get the total amount spent across all expenses."""
    total = sum(e["amount"] for e in expenses)
    return {"total_expenses": total, "number_of_expenses": len(expenses)}


@mcp.tool()
async def get_category_summary() -> dict:
    """Get spending summary by category."""
    summary = {}
    for expense in expenses:
        cat = expense["category"]
        if cat not in summary:
            summary[cat] = {"total": 0, "count": 0}
        summary[cat]["total"] += expense["amount"]
        summary[cat]["count"] += 1
    
    return {"category_summary": summary}


@mcp.tool()
async def delete_expense(expense_id: int) -> dict:
    """Delete an expense by ID."""
    global expenses
    expense_to_delete = next((e for e in expenses if e["id"] == expense_id), None)
    if expense_to_delete is None:
        return {"error": f"Expense with ID {expense_id} not found"}
    
    expenses = [e for e in expenses if e["id"] != expense_id]
    return {"status": "success", "deleted_expense": expense_to_delete}


@mcp.tool()
async def get_monthly_total(year: int, month: int) -> dict:
    """Get total expenses for a specific month (format: year=2026, month=4)."""
    monthly_expenses = [
        e for e in expenses 
        if e["date"].startswith(f"{year:04d}-{month:02d}")
    ]
    total = sum(e["amount"] for e in monthly_expenses)
    return {"year": year, "month": month, "expenses": monthly_expenses, "total": total}



@mcp.custom_route("/", methods=["GET"])
async def root(request):
    """Browser-friendly health check page."""
    return HTMLResponse("""
    <html>
        <head>
            <title>MCP Expense Server</title>
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
                <h1>MCP Expense Server</h1>
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
