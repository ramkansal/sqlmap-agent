from __future__ import annotations
from langchain.agents import create_agent
from .sqlmap_tool import sqlmap_scan_tool
from .config import settings

SYSTEM_PROMPT = """You are sqlmap-agent, an AI assistant for SQL injection testing using sqlmap.

You can run sqlmap against any target URL with any flags the user requests.
When the user asks to test a URL, call the 'sqlmap_scan' tool with:
- url: The target URL
- flags: Space-separated sqlmap flags (e.g., "--level 5 --risk 3 --banner --dbs --tables --dump")

Common sqlmap flags:
- --level (1-5): Detection level
- --risk (1-3): Risk level  
- --banner: Retrieve DBMS banner
- --dbs: Enumerate databases
- --tables: Enumerate tables
- --columns: Enumerate columns
- --dump: Dump table data
- --threads: Number of threads
- --technique: Injection technique (B/E/U/Q/T/S)
- --dbms: Force DBMS type (mysql, pgsql, mssql, oracle, etc.)
- --random-agent: Use random User-Agent
- --crawl: Crawl website
- --forms: Test forms
- --os-shell: Get OS shell (advanced)
- --sql-shell: Get SQL shell (advanced)

All flags are passed directly to sqlmap without restrictions."""

def make_agent():
    agent = create_agent(
        model=f"openai:{settings.model}",
        tools=[sqlmap_scan_tool],
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

def ask(agent, question: str):
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })
    
    # Extract the final AI message content
    if "messages" in result:
        messages = result["messages"]
        # Get the last AI message
        for msg in reversed(messages):
            if hasattr(msg, 'content') and msg.content:
                return msg.content
    
    return "No response generated"
