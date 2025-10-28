from src.sqlmap_agent.agent import make_agent, ask

def main():
    print("SQLMap Agent - Ready for continuous scanning!")
    print("Type 'quit', 'exit', or 'q' to stop the agent.")
    print("-" * 60)
    
    agent = make_agent()
    
    while True:
        try:
            query = input("\nEnter your sqlmap query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q', '']:
                print("\nGoodbye! Stay secure!")
                break
            
            print(f"\nProcessing: {query}")
            print("-" * 40)
            
            result = ask(agent, query)
            
            print("\nResult:")
            print("-" * 40)
            print(result)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Try again with a different query.")


if __name__ == "__main__":
    main()
