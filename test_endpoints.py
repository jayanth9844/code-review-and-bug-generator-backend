"""
Test script for RAG API endpoints
"""
import requests
import json

# Your JWT token (from login)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2NDUxMTk0N30.SuFo8ZfAAQ0UVZ2kve0qJTkJUk4Ho8_3BA0QhlgD2zY"
API_KEY = "AIzaSyCxKS_4nxUKREl2uER3A-FQXvEkHbBHZcY"
BASE_URL = "http://127.0.0.1:8000"

# Headers for all requests
headers = {
    "token": TOKEN,
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Sample code to test
sample_code = """import sqlite3
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

print("=" * 60)
print("Testing Code Review and Bug Generator API")
print("=" * 60)

# Test 1: Load code snippets
print("\n1. Testing /rag/code-input endpoint...")
print("-" * 60)
payload = {
    "code_snippets": [sample_code]
}

try:
    response = requests.post(
        f"{BASE_URL}/rag/code-input",
        headers=headers,
        json=payload
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Analyze code
print("\n2. Testing /rag/analyze-code endpoint...")
print("-" * 60)
analyze_payload = {
    "query": "Analyze the code for potential bugs, security risks, performance issues, and best-practice violations."
}

try:
    response = requests.post(
        f"{BASE_URL}/rag/analyze-code",
        headers=headers,
        json=analyze_payload
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Get code metrics
print("\n3. Testing /rag/code-metrics endpoint...")
print("-" * 60)
metrics_payload = {
    "query": "Provide overall code quality, security metrics, bug density, and issue distribution."
}

try:
    response = requests.post(
        f"{BASE_URL}/rag/code-metrics",
        headers=headers,
        json=metrics_payload
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Inject bugs
print("\n4. Testing /rag/inject-bugs endpoint...")
print("-" * 60)
inject_payload = {
    "query": "Inject bugs into the code and return details.",
    "bug_type": "Security Vulnerability",
    "severity_level": 5,
    "num_bugs": 2
}

try:
    response = requests.post(
        f"{BASE_URL}/rag/inject-bugs",
        headers=headers,
        json=inject_payload
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing Complete")
print("=" * 60)
