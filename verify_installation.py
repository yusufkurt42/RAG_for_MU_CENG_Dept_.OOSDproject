#!/usr/bin/env python3
"""
Verification script for RAG project installation.
Run this after installation to verify everything is working.
"""

import sys
import os

def check_python_version():
    """Check Python version."""
    print("1. Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_imports():
    """Check if all modules can be imported."""
    print("\n2. Checking module imports...")
    
    modules = [
        'rag',
        'rag.model',
        'rag.detector',
        'rag.writer',
        'rag.retriever',
        'rag.reranker',
        'rag.answer',
        'rag.orchestrator',
        'rag.tracer',
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if required files exist."""
    print("\n3. Checking required files...")
    
    files = [
        'python/main.py',
        'python/resources/config.json',
        'python/resources/chunks.json',
        'setup.py',
        'requirements.txt',
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
            all_ok = False
    
    return all_ok

def check_components():
    """Check if components can be instantiated."""
    print("\n4. Checking components...")
    
    try:
        from python.rag.detector import Intent, RuleIntentDetector
        from python.rag.model import Chunk, ChunkStore
        from python.rag.orchestrator import Context
        
        # Test Context
        context = Context("test question")
        print(f"   ✅ Context created")
        
        # Test Chunk
        chunk = Chunk("id1", "doc1", 0, 100, "test text")
        print(f"   ✅ Chunk created")
        
        # Test Intent Detector
        detector = RuleIntentDetector({Intent.UNKNOWN: ["test"]}, [])
        print(f"   ✅ IntentDetector created")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Component error: {e}")
        return False

def run_simple_test():
    """Run a simple end-to-end test."""
    print("\n5. Running simple test...")
    
    try:
        from python.rag.detector import Intent, RuleIntentDetector
        from python.rag.orchestrator import Context
        
        # Create detector
        rules = {
            Intent.STAFF_LOOKUP: ["professor", "teacher"],
            Intent.REGISTRATION: ["register", "enrollment"]
        }
        detector = RuleIntentDetector(rules, [1, 0])
        
        # Test detection
        context = Context("Who is the professor?")
        detector.execute(context)
        
        if context.current_intent == Intent.STAFF_LOOKUP:
            print(f"   ✅ Intent detection works")
            return True
        else:
            print(f"   ❌ Intent detection failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("RAG Project Installation Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_files(),
        check_imports(),
        check_components(),
        run_simple_test(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ ALL CHECKS PASSED!")
        print("=" * 60)
        print("\nYou can now run:")
        print('  python python/main.py --question "Your question?"')
        print("\nOr run tests:")
        print("  pytest python/tests/")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 60)
        print("\nPlease run: pip install -e .")
        return 1

if __name__ == "__main__":
    sys.exit(main())
