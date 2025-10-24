#!/usr/bin/env python3
"""
Main application for RAG System
Interactive query interface for Marmara University CENG Department information
"""
import sys
import os
from src.rag_system import RAGSystem

def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("RAG System for Marmara University Computer Engineering Department")
    print("=" * 70)
    print()

def print_help():
    """Print help information"""
    print("\nAvailable Commands:")
    print("  query <question>  - Ask a question about the department")
    print("  stats             - Show system statistics")
    print("  help              - Show this help message")
    print("  exit              - Exit the application")
    print()

def main():
    """Main application loop"""
    print_banner()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found!")
        print("Please create a .env file based on .env.example and add your GOOGLE_API_KEY")
        print("\nYou can continue with default settings, but queries will fail without a valid API key.")
        response = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Exiting...")
            return
        print()
    
    try:
        # Initialize RAG system
        print("Initializing RAG system...")
        rag = RAGSystem()
        
        # Load documents from data directory
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        if os.path.exists(data_dir):
            rag.load_documents(data_dir)
        else:
            print(f"Warning: Data directory '{data_dir}' not found.")
            print("No documents loaded. You can still add documents manually.")
        
        print("\nRAG system ready!")
        print_help()
        
        # Interactive loop
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Thank you for using the RAG system. Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print_help()
                    continue
                
                if user_input.lower() == 'stats':
                    stats = rag.get_stats()
                    print("\n" + "=" * 50)
                    print("System Statistics:")
                    print("=" * 50)
                    for key, value in stats.items():
                        print(f"{key}: {value}")
                    print("=" * 50)
                    continue
                
                # Process as query
                if user_input.lower().startswith('query '):
                    question = user_input[6:].strip()
                else:
                    question = user_input
                
                if not question:
                    print("Please provide a question.")
                    continue
                
                # Execute query
                result = rag.query(question)
                
                # Display results
                print("\n" + "=" * 70)
                print("ANSWER:")
                print("=" * 70)
                print(result['answer'])
                print("\n" + "=" * 70)
                print(f"Based on {len(result['retrieved_documents'])} retrieved documents")
                print("=" * 70)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Type 'exit' to quit.")
                continue
            except Exception as e:
                print(f"\nError processing request: {str(e)}")
                continue
    
    except Exception as e:
        print(f"\nError initializing system: {str(e)}")
        print("\nPlease check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
