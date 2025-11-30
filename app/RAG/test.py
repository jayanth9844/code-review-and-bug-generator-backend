"""
Test module for RAG system.
Tests all core functionalities: code analysis, metrics calculation, and bug injection.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from RAG import (
    initialize_vector_store_and_embeddings,
    load_and_index_code,
    analyze_code,
    get_code_metrics,
    inject_bugs,
)


# Sample code for testing
SAMPLE_CODE = """import sqlite3
import threading
import time

class UserManager:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cache = {}

    def add_user(self, username, password):
        # Logic error: storing password in plain text
        self.cursor.execute(f"INSERT INTO users (name, password) VALUES ('{username}', '{password}')")
        self.conn.commit()

    def get_user(self, username):
        # Security vulnerability: SQL injection risk
        query = f"SELECT * FROM users WHERE name = '{username}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def cache_user(self, username):
        # Potential memory leak: cache never cleared
        user = self.get_user(username)
        self.cache[username] = user

def worker_task(manager, username):
    # Concurrency bug: race condition on shared cache
    for _ in range(1000):
        manager.cache_user(username)

def heavy_computation(n):
    # Performance issue: inefficient recursion
    if n <= 1:
        return n
    return heavy_computation(n-1) + heavy_computation(n-2)

def main():
    manager = UserManager()
    manager.add_user("Alice", "password123")
    manager.add_user("Bob", "hunter2")

    # Start multiple threads (race condition risk)
    threads = []
    for name in ["Alice", "Bob"]:
        t = threading.Thread(target=worker_task, args=(manager, name))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Trigger performance bottleneck
    print("Fibonacci(30):", heavy_computation(30))

    # Crash bug: division by zero
    print("Divide:", 10 / 0)

if __name__ == "__main__":
    main()
"""


def test_vector_store_initialization():
    """Test vector store and embedding model initialization."""
    print("\n" + "="*70)
    print("TEST 1: Vector Store & Embeddings Initialization")
    print("="*70)
    
    try:
        embedding_model, vector_store = initialize_vector_store_and_embeddings()
        print("✓ Vector store initialized successfully")
        print(f"✓ Embedding model loaded: {type(embedding_model).__name__}")
        print(f"✓ Vector store type: {type(vector_store).__name__}")
        return embedding_model, vector_store
    except Exception as e:
        print(f"✗ Error: {e}")
        return None, None


def test_code_loading(embedding_model, vector_store):
    """Test loading and indexing code snippets."""
    print("\n" + "="*70)
    print("TEST 2: Code Loading & Indexing")
    print("="*70)
    
    try:
        result = load_and_index_code([SAMPLE_CODE], embedding_model, vector_store)
        print(f"✓ {result}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_analyze_code(embedding_model, vector_store):
    """Test code analysis functionality."""
    print("\n" + "="*70)
    print("TEST 3: Code Analysis")
    print("="*70)
    
    try:
        query = "Analyze the code for potential bugs, security risks, performance issues, and best-practice violations."
        print(f"Query: {query}")
        
        result = analyze_code(
            query=query,
            embedding_model=embedding_model,
            vector_store=vector_store
        )
        
        print(f"✓ Analysis completed successfully")
        print(f"✓ Number of issues found: {len(result.get('issues', []))}")
        print("\nAnalysis Results:")
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_metrics(embedding_model, vector_store):
    """Test code metrics calculation."""
    print("\n" + "="*70)
    print("TEST 4: Code Metrics Calculation")
    print("="*70)
    
    try:
        query = "Provide overall code quality, security metrics, bug density, and issue distribution."
        print(f"Query: {query}")
        
        result = get_code_metrics(
            query=query,
            embedding_model=embedding_model,
            vector_store=vector_store
        )
        
        print(f"✓ Metrics calculated successfully")
        print("\nMetrics Results:")
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_inject_bugs(embedding_model, vector_store):
    """Test bug injection functionality."""
    print("\n" + "="*70)
    print("TEST 5: Bug Injection")
    print("="*70)
    
    try:
        query = "Inject bugs into the code and return details."
        print(f"Query: {query}")
        print(f"Bug Type: Security Vulnerability")
        print(f"Severity Level: 5")
        print(f"Number of Bugs: 2")
        
        result = inject_bugs(
            query=query,
            embedding_model=embedding_model,
            vector_store=vector_store,
            bug_type="Security Vulnerability",
            severity_level=5,
            num_bugs=2
        )
        
        print(f"✓ Bug injection completed successfully")
        print(f"✓ Number of bugs injected: {len(result.get('bugs_injected', []))}")
        print("\nBug Injection Results:")
        print("\nBuggy Code:")
        print("```python")
        print(result.get('buggy_code', 'N/A'))
        print("```")
        print("\nBugs Injected:")
        print(json.dumps(result.get('bugs_injected', []), indent=2))
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "#"*70)
    print("# RAG Module Test Suite")
    print("#"*70)
    
    # Test 1: Initialize vector store and embeddings
    embedding_model, vector_store = test_vector_store_initialization()
    if embedding_model is None or vector_store is None:
        print("\n✗ Failed to initialize vector store and embeddings. Exiting tests.")
        return
    
    # Test 2: Load and index code
    if not test_code_loading(embedding_model, vector_store):
        print("\n✗ Failed to load and index code. Exiting tests.")
        return
    
    # Test 3: Analyze code
    test_analyze_code(embedding_model, vector_store)
    
    # Test 4: Get code metrics
    test_get_metrics(embedding_model, vector_store)
    
    # Test 5: Inject bugs
    test_inject_bugs(embedding_model, vector_store)
    
    print("\n" + "#"*70)
    print("# All Tests Completed")
    print("#"*70 + "\n")


if __name__ == "__main__":
    main()
