"""Main application entry point."""

import argparse
import sys
from rag.orchestrator import RagOrchestrator


def main():
    """Main function."""
    # Default values
    config_path = "resources/config.json"
    chunk_path = "resources/chunks.json"
    question = "Mazeret sınavı başvurusu nasıl yapılır?"
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="RAG Application")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--chunks", type=str, help="Path to chunks file")
    parser.add_argument("-q", "--question", type=str, help="Question to ask")
    
    args = parser.parse_args()
    
    # Override defaults with command line arguments
    if args.config:
        config_path = args.config
    if args.chunks:
        chunk_path = args.chunks
    if args.question:
        question = args.question
    
    print("Başlatılıyor...")
    print(f"Config: {config_path}")
    print(f"Soru: {question}")
    
    try:
        # Initialize orchestrator
        orchestrator = RagOrchestrator(config_path, chunk_path)
        
        # Run scenario
        answer = orchestrator.answer_question(question)
        
        # Print output
        print(f"\n{answer}")
        
    except Exception as e:
        print(f"Uygulama Hatası: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
