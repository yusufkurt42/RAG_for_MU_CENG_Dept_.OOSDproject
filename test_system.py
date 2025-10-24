#!/usr/bin/env python3
"""
Simple test script to verify RAG system functionality
"""
import os
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from src.config import Config
        from src.document_processor import DocumentProcessor
        from src.vector_store import VectorStore
        from src.gemini_generator import GeminiGenerator
        from src.rag_system import RAGSystem
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_document_processor():
    """Test document processor functionality"""
    print("\nTesting Document Processor...")
    try:
        from src.document_processor import DocumentProcessor
        
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        
        # Test chunking
        text = "This is a test. " * 50  # Long text
        chunks = processor.chunk_text(text)
        
        assert len(chunks) > 1, "Should create multiple chunks"
        print(f"✓ Created {len(chunks)} chunks from text")
        
        # Test document processing
        docs = [{'content': text, 'source': 'test.txt', 'metadata': {}}]
        processed = processor.process_documents(docs)
        
        assert len(processed) > 0, "Should process documents"
        print(f"✓ Processed {len(processed)} document chunks")
        
        return True
    except Exception as e:
        print(f"✗ Document processor test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting Configuration...")
    try:
        from src.config import Config
        
        # Test config attributes exist
        assert hasattr(Config, 'GOOGLE_API_KEY')
        assert hasattr(Config, 'CHROMA_PERSIST_DIRECTORY')
        assert hasattr(Config, 'COLLECTION_NAME')
        assert hasattr(Config, 'GEMINI_MODEL')
        
        print("✓ Configuration loaded successfully")
        print(f"  - Collection: {Config.COLLECTION_NAME}")
        print(f"  - Model: {Config.GEMINI_MODEL}")
        print(f"  - API Key: {'Set' if Config.GOOGLE_API_KEY else 'Not set'}")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_data_directory():
    """Test that data directory exists and contains files"""
    print("\nTesting Data Directory...")
    try:
        data_dir = 'data'
        
        if not os.path.exists(data_dir):
            print(f"✗ Data directory '{data_dir}' not found")
            return False
        
        txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
        
        if len(txt_files) == 0:
            print(f"✗ No .txt files found in '{data_dir}'")
            return False
        
        print(f"✓ Found {len(txt_files)} .txt files in data directory:")
        for f in txt_files:
            size = os.path.getsize(os.path.join(data_dir, f))
            print(f"  - {f} ({size} bytes)")
        
        return True
    except Exception as e:
        print(f"✗ Data directory test failed: {e}")
        return False

def test_document_loading():
    """Test loading documents from data directory"""
    print("\nTesting Document Loading...")
    try:
        from src.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        documents = processor.load_documents_from_directory('data')
        
        if len(documents) == 0:
            print("✗ No documents loaded")
            return False
        
        print(f"✓ Loaded {len(documents)} documents")
        
        # Process documents
        processed = processor.process_documents(documents)
        print(f"✓ Created {len(processed)} chunks from documents")
        
        return True
    except Exception as e:
        print(f"✗ Document loading test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting File Structure...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'main.py',
        'src/__init__.py',
        'src/config.py',
        'src/document_processor.py',
        'src/vector_store.py',
        'src/gemini_generator.py',
        'src/rag_system.py',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 70)
    print("RAG System Test Suite")
    print("=" * 70)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Data Directory", test_data_directory),
        ("Document Processor", test_document_processor),
        ("Document Loading", test_document_loading),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} - EXCEPTION: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:30s} {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
