import argparse
import sys
import json
import time
import os
from rag.orchestrator.rag_orchestrator import RagOrchestrator

def run_batch(orchestrator, batch_file_path, output_file="batch_results.json"):
    """
    Executes batch processing from a JSON file.
    Logs latency and answers.
    """
    print(f"Starting batch processing. Input: {batch_file_path}")
    
    # 1. Load Questions
    try:
        with open(batch_file_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except Exception as e:
        print(f"Error reading batch file: {e}")
        return

    results = []
    total_latency = 0
    
    # 2. Process Loop
    for i, item in enumerate(questions):
        # Handle format: [{"id":1, "question":"..."}]
        q_id = item.get("id", i+1)
        q_text = item.get("question", "")
        
        print(f"[{i+1}/{len(questions)}] Processing Question ID: {q_id}")
        
        start_time = time.time()
        
        # Call Orchestrator
        answer_obj = orchestrator.answer_question(q_text)
        
        duration = time.time() - start_time
        total_latency += duration
        
        # Store Result
        results.append({
            "id": q_id,
            "question": q_text,
            "answer": answer_obj.text,
            "citations": answer_obj.citations,
            "latency_seconds": round(duration, 3)
        })

    # 3. Generate Report
    avg_latency = total_latency / len(questions) if questions else 0
    report = {
        "summary": {
            "total_questions": len(questions),
            "average_latency_seconds": round(avg_latency, 3)
        },
        "results": results
    }
    
    # 4. Save to File
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Batch completed successfully. Report saved to: {output_file}")
    except Exception as e:
        print(f"Error saving report: {e}")


def main():
    parser = argparse.ArgumentParser(description="RAG System - Batch Processing")
    parser.add_argument("--config", type=str, default="resources/config.json", help="Path to config")
    parser.add_argument("--chunks", type=str, default="resources/chunks.json", help="Path to chunks")
    
    # Mutually exclusive: either single question OR batch file
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-q", "--question", type=str, help="Single question to ask")
    group.add_argument("--batch", type=str, help="Path to JSON file with questions")
    
    args = parser.parse_args()
    
    orchestrator = None
    try:
        # Initialize Orchestrator (Log file opens here)
        orchestrator = RagOrchestrator(args.config, args.chunks)
        
        if args.batch:
            # Run Batch Mode
            run_batch(orchestrator, args.batch)
        else:
            # Run Single Question Mode
            ans = orchestrator.answer_question(args.question)
            print(f"\nANSWER:\n{ans.text}")
            print(f"CITATIONS: {ans.citations}")
            
    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # IMPORTANT: Close logs only when the program exits
        if orchestrator:
            orchestrator.close()

if __name__ == "__main__":
    main()
