"""Main application entry point."""
import os
import argparse
import sys
from dotenv import load_dotenv
from rag.orchestrator import RagOrchestrator

# Load environment variables
load_dotenv()


def main():
    """Main function."""
    # Default values
    # os.chdir(".\\OOSD_RAG\\rag_python\\")
    config_path = "resources/config.json"
    chunk_path = "resources/chunks.json"
    question = "en düşük geçme notu ne?"
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="RAG Application")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--chunks", type=str, help="Path to chunks file")
    # Allow multiple questions by repeating -q/--question. Example:
    # python main.py -q "Question 1" -q "Question 2"
    parser.add_argument("-q", "--question", action="append", help="Question to ask. Provide multiple -q for batch processing")
    
    args = parser.parse_args()
    
    # Override defaults with command line arguments
    if args.config:
        config_path = args.config
    if args.chunks:
        chunk_path = args.chunks
    # args.question will be a list if provided multiple times (action='append')
    questions = None
    if args.question:
        questions = args.question
    
    #print("Başlatılıyor...")
    #print(f"Config: {config_path}")
    #print(f"Soru: {question}")
    
    try:
        # Initialize orchestrator
        orchestrator = RagOrchestrator(config_path, chunk_path)

        # Run scenario. If multiple questions were provided, process them as a batch.
        if questions and len(questions) > 1:
            answers = orchestrator.answer_questions(questions)
            # Print each question/answer pair
            for q, a in zip(questions, answers):
                print("---------------------------------------------------")
                print(f"Soru: {q}\n")
                print(f"Cevap: {a}\n")
            print("---------------------------------------------------")
        else:
            # Single question handling. Use provided question or default.
            single_q = questions[0] if questions and len(questions) == 1 else question
            answer = orchestrator.answer_question(single_q)
            print(f"\n{answer}")
        
    except Exception as e:
        print(f"Uygulama Hatası: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
