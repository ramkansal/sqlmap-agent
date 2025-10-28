from __future__ import annotations
import re, shlex, subprocess, json, tempfile, os
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain.tools import tool
from .config import settings

class SqlmapArgs(BaseModel):
    url: str = Field(..., description="Target URL to test for SQL injection vulnerabilities.")
    flags: Optional[str] = Field(
        None, 
        description="Space-separated sqlmap flags (e.g., '--level 5 --risk 3 --banner --dbs --tables --dump'). All flags will be passed directly to sqlmap."
    )
    dry_run: bool = Field(False, description="Return planned command without executing.")

def _build_sqlmap_cmd(args: SqlmapArgs) -> List[str]:
    """Build sqlmap command from URL and flags."""
    cmd = ["sqlmap", "--batch", "-u", args.url]
    
    
    if args.flags:
        
        parsed_flags = shlex.split(args.flags)
        cmd.extend(parsed_flags)
    
    return cmd


def _summarize_sqlmap_output(txt: str) -> dict:
    """Parse sqlmap output for key findings."""
    
    found = bool(re.search(r"(?i)(parameter.*appears to be vulner|injection point|vulnerable)", txt))
    
    
    dbms = None
    m = re.search(r"back-end DBMS:\s*([^\n\r]+)", txt, flags=re.I)
    if m:
        dbms = m.group(1).strip()
    
    
    banner = None
    m2 = re.search(r"banner:\s*'([^']+)'", txt, flags=re.I)
    if m2:
        banner = m2.group(1)
    
    
    vulns = re.findall(r"Type:\s*([^\n\r]+)", txt)
    
    return {
        "injectable": found,
        "dbms": dbms,
        "banner": banner,
        "vuln_types": list(set(v.strip() for v in vulns))[:10],
        "output_excerpt": txt[-4000:],  
    }

@tool("sqlmap_scan", args_schema=SqlmapArgs, return_direct=False)
def sqlmap_scan_tool(**kwargs) -> str:
    """
    Run sqlmap against a target URL with custom flags.
    Accepts space-separated flags that will be passed directly to sqlmap.
    Returns JSON with command, summary, and captured output.
    
    Example usage:
    - url: "http://example.com/page?id=1"
    - flags: "--level 5 --risk 3 --banner --dbs --tables"
    """
    args = SqlmapArgs(**kwargs)
    
    
    cmd = _build_sqlmap_cmd(args)
    
    
    if args.dry_run:
        return json.dumps({"dry_run": True, "cmd": cmd}, indent=2)
    
    
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=settings.sqlmap_timeout_s,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        out = proc.stdout
        summary = _summarize_sqlmap_output(out)
        
        return json.dumps({
            "cmd": cmd,
            "summary": summary,
            "returncode": proc.returncode
        }, indent=2)
    except subprocess.TimeoutExpired:
        return json.dumps({
            "cmd": cmd,
            "error": f"sqlmap execution timed out after {settings.sqlmap_timeout_s} seconds"
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "cmd": cmd,
            "error": f"Failed to execute sqlmap: {str(e)}"
        }, indent=2)

