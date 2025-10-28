from __future__ import annotations
import json, argparse, os, sys
from .agent import make_agent, ask

def main():
    parser = argparse.ArgumentParser(
        description="sqlmap-agent: AI-powered SQL injection testing with sqlmap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Test http://example.com/page?id=1 with level 5 and risk 3"
  %(prog)s "Scan http://target.com/login with --forms --banner --dbs"
  %(prog)s "Check http://site.com for SQLi using --level 5 --risk 3 --dump"

Common sqlmap flags:
  --level (1-5)      Detection depth
  --risk (1-3)       Risk level
  --banner           Retrieve DBMS banner
  --dbs              Enumerate databases
  --tables           Enumerate tables
  --dump             Dump table data
  --forms            Test forms
  --threads N        Use N threads

Environment variables:
  OPENAI_API_KEY     Required: OpenAI API key
  LLM_MODEL          Optional: LLM model (default: gpt-5-nano)
  SQLMAP_TIMEOUT_S   Optional: Timeout in seconds (default: 900)
        """
    )
    parser.add_argument(
        "query", 
        help="Natural language instruction for sqlmap scan"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()

    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set", file=sys.stderr)
        print("\nSet it with: export OPENAI_API_KEY=sk-your-key-here", file=sys.stderr)
        return 1

    try:
        
        if args.verbose:
            print(f"Initializing sqlmap-agent...")
            print(f"Query: {args.query}\n")
        
        executor = make_agent()
        result = ask(executor, args.query)
        
        if args.verbose:
            print("\n" + "=" * 60)
            print("Result:")
            print("=" * 60)
        
        print(json.dumps(result, indent=2, default=str))
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
