# sqlmap-agent

An AI-powered agent for running sqlmap scans using natural language commands.

## Features

- 🤖 Natural language interface to sqlmap
- 🚀 Accept any sqlmap flags directly from the LLM
- 🐳 Docker-ready (no allowlist restrictions)
- ⚡ Simple and flexible flag passing

## Quick Usage (Recommended)

```bash
docker run --rm -it -e OPENAI_API_KEY=$env:OPENAI_API_KEY ramkansal/sqlmap-agent:latest
```

## How It Works

The agent accepts a target URL and space-separated sqlmap flags, then executes sqlmap with those parameters. All flags are passed directly to sqlmap without restrictions.

## Configuration

Environment variables:

```bash
OPENAI_API_KEY=your-api-key      # Required
LLM_MODEL=gpt-5-nano            # Optional (default: gpt-5-nano)
SQLMAP_TIMEOUT_S=900             # Optional (default: 900 = 15 minutes)
```

## Common sqlmap Flags

- `--level (1-5)`: Detection depth
- `--risk (1-3)`: Risk level
- `--banner`: Retrieve DBMS banner
- `--dbs`: Enumerate databases
- `--tables`: Enumerate tables
- `--columns`: Enumerate columns
- `--dump`: Dump table data
- `--threads N`: Use N concurrent threads
- `--technique TECH`: Injection technique (B/E/U/Q/T/S)
- `--dbms TYPE`: Force DBMS (mysql, pgsql, mssql, oracle)
- `--random-agent`: Use random User-Agent
- `--crawl N`: Crawl website N levels deep
- `--forms`: Test forms
- `--os-shell`: Get OS shell
- `--sql-shell`: Get SQL shell

## Example Usage

```bash
# Basic scan
python -m src.sqlmap_agent.run "Scan http://example.com/page?id=1"

# Advanced scan with flags
python -m src.sqlmap_agent.run "Test http://target.com/login with --level 5 --risk 3 --banner --dbs --tables"

# Form testing
python -m src.sqlmap_agent.run "Check http://site.com for SQL injection using --forms --crawl 2"
```

## Changes from Original

- ✅ Removed TARGET_ALLOWLIST requirement
- ✅ Removed banned flags restrictions  
- ✅ Simplified to accept any flags from the model
- ✅ Direct flag passing to sqlmap
- ✅ Better error handling and timeout management

## Security Note

This tool has NO built-in restrictions on targets or flags. It's designed to run in a controlled Docker environment. Ensure proper network isolation and access controls at the infrastructure level.

