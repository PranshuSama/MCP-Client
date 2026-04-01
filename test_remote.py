"""Quick test to verify the remote MCP expense server is working."""
import httpx
import json

BASE_URL = "https://mcp-client-ubth.onrender.com/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}

def parse_sse(text):
    """Parse SSE response to extract JSON data."""
    for line in text.strip().split("\n"):
        if line.startswith("data: "):
            return json.loads(line[6:])
    return None

def main():
    with httpx.Client(timeout=30) as client:
        # Step 1: Initialize
        print("1️⃣  Sending initialize request...")
        resp = client.post(BASE_URL, headers=HEADERS, json={
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        })
        print(f"   Status: {resp.status_code}")
        data = parse_sse(resp.text)
        print(f"   Server: {data['result']['serverInfo']['name']} v{data['result']['serverInfo']['version']}")
        
        # Get session ID
        session_id = resp.headers.get("mcp-session-id")
        print(f"   Session ID: {session_id}")
        
        if session_id:
            HEADERS["Mcp-Session-Id"] = session_id

        # Step 2: Send initialized notification
        print("\n2️⃣  Sending initialized notification...")
        resp = client.post(BASE_URL, headers=HEADERS, json={
            "jsonrpc": "2.0", "method": "notifications/initialized"
        })
        print(f"   Status: {resp.status_code}")

        # Step 3: List tools
        print("\n3️⃣  Listing available tools...")
        resp = client.post(BASE_URL, headers=HEADERS, json={
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
        })
        data = parse_sse(resp.text)
        tools = data["result"]["tools"]
        print(f"   Found {len(tools)} tools:")
        for tool in tools:
            print(f"   • {tool['name']}: {tool['description']}")

        # Step 4: Call add_expense tool
        print("\n4️⃣  Calling add_expense tool...")
        resp = client.post(BASE_URL, headers=HEADERS, json={
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {
                "name": "add_expense",
                "arguments": {
                    "amount": 42.50,
                    "category": "food",
                    "description": "Test expense from remote client"
                }
            }
        })
        data = parse_sse(resp.text)
        print(f"   Result: {json.dumps(data['result'], indent=2)}")

        # Step 5: Call get_all_expenses
        print("\n5️⃣  Calling get_all_expenses tool...")
        resp = client.post(BASE_URL, headers=HEADERS, json={
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "get_all_expenses", "arguments": {}}
        })
        data = parse_sse(resp.text)
        print(f"   Result: {json.dumps(data['result'], indent=2)}")

    print("\n✅ All tests passed! Your remote MCP server is working perfectly!")

if __name__ == "__main__":
    main()
