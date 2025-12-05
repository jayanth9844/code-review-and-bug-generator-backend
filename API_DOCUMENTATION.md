# Code Review and Bug Generator API - Frontend Documentation

**Base URL (Production)**: `https://code-review-and-bug-generator-backend-2.onrender.com`  
**Base URL (Local)**: `http://localhost:8000`

**API Docs**: `/docs` (Swagger UI)

---

## Important Notes for Frontend

### 1. Code Input Format
- **Code must be a string** with `\n` for newlines
- Example: `"def hello():\n    print('world')"`
- DO NOT send actual newlines in JSON, use escape sequence `\n`

### 2. API Key (Optional)
- All endpoints have optional `api_key` parameter
- If not provided, server uses environment variable
- For production, leave `api_key` as `null` or don't include it

### 3. Error Handling
- All responses have `status` field: `"success"` or `"error"`
- On error, check `error_message` field for details
- Common errors:
  - Missing API key
  - Invalid code format
  - AI service timeout

---

## Endpoint 1: Code Input (Store Code)

**Optional step** - Store code for later analysis without sending it in every request.

### Request
```
POST /api/code-input
Content-Type: application/json
```

**Body:**
```json
{
  "code_snippets": [
    "def hello():\n    print('world')",
    "def add(a, b):\n    return a + b"
  ]
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code_snippets` | array[string] | ✅ Yes | List of code snippets to store (min 1) |

### Response

**Success (200):**
```json
{
  "status": "success",
  "message": "Loaded 2 code snippet(s) into memory",
  "snippets_loaded": 2
}
```

**Error (200):**
```json
{
  "status": "error",
  "message": "Error loading code: [error details]",
  "snippets_loaded": 0
}
```

### Frontend Usage Example (JavaScript)
```javascript
const storeCode = async (codeArray) => {
  const response = await fetch('https://code-review-and-bug-generator-backend-2.onrender.com/api/code-input', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code_snippets: codeArray
    })
  });
  return await response.json();
};
```

---

## Endpoint 2: Analyze Code

Analyzes code for bugs, security issues, and best practices.

### Request
```
POST /api/analyze-code
Content-Type: application/json
```

**Body:**
```json
{
  "code": "def divide(a, b):\n    return a / b",
  "api_key": null
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | ❌ No | Code to analyze. If not provided, uses stored code from `/code-input` |
| `api_key` | string\|null | ❌ No | Gemini API key. Use `null` or omit for server's key |

### Response

**Success (200):**
```json
{
  "status": "success",
  "issues": [
    {
      "title": "Division by Zero Risk",
      "type": "Bug",
      "severity": "High",
      "lineNumber": 2,
      "description": "The function does not handle the case when b is zero, which will raise a ZeroDivisionError.",
      "suggestedFix": "Add a check: if b == 0: raise ValueError('Cannot divide by zero')"
    }
  ],
  "total_issues": 1,
  "error_message": null
}
```

**Error (200):**
```json
{
  "status": "error",
  "issues": [],
  "total_issues": 0,
  "error_message": "API_KEY is required. Provide it in the request or set API_KEY environment variable."
}
```

**Issue Object Structure:**
| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Short issue title |
| `type` | string | Type: "Bug", "Security", "Code Smell", "Best Practice" |
| `severity` | string | "Low", "Medium", "High", "Critical" |
| `lineNumber` | number\|null | Line number where issue occurs |
| `description` | string | Detailed description of the issue |
| `suggestedFix` | string | Recommended solution |

### Frontend Usage Example (JavaScript)
```javascript
const analyzeCode = async (codeString) => {
  const response = await fetch('https://code-review-and-bug-generator-backend-2.onrender.com/api/analyze-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code: codeString,
      api_key: null  // Use server's API key
    })
  });
  
  const result = await response.json();
  
  if (result.status === "error") {
    console.error("Error:", result.error_message);
    return null;
  }
  
  return result.issues;  // Array of issues
};

// Usage
const code = "def divide(a, b):\\n    return a / b";
const issues = await analyzeCode(code);
```

---

## Endpoint 3: Code Metrics

Calculates code quality scores and issue distribution.

### Request
```
POST /api/code-metrics
Content-Type: application/json
```

**Body:**
```json
{
  "code": "def hello():\n    print('world')",
  "api_key": null
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | ❌ No | Code to analyze. If not provided, uses stored code |
| `api_key` | string\|null | ❌ No | Gemini API key. Use `null` or omit |

### Response

**Success (200):**
```json
{
  "status": "success",
  "summary_metrics": {
    "code_quality_score": 85,
    "security_rating": 90,
    "bug_density": 1,
    "critical_issue_count": 0
  },
  "issue_distribution": {
    "security_vulnerabilities": 0,
    "code_smells": 2,
    "best_practices": 1,
    "performance_issues": 0
  },
  "error_message": null
}
```

**Error (200):**
```json
{
  "status": "error",
  "summary_metrics": {
    "code_quality_score": 0,
    "security_rating": 0,
    "bug_density": 0,
    "critical_issue_count": 0
  },
  "issue_distribution": {
    "security_vulnerabilities": 0,
    "code_smells": 0,
    "best_practices": 0,
    "performance_issues": 0
  },
  "error_message": "No code provided. Please provide code in request or load code using /code-input endpoint"
}
```

**Metrics Structure:**

**Summary Metrics:**
| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `code_quality_score` | number | 0-100 | Overall code quality (higher is better) |
| `security_rating` | number | 0-100 | Security score (higher is better) |
| `bug_density` | number | 0+ | Count of bugs/runtime errors |
| `critical_issue_count` | number | 0+ | Count of critical severity issues |

**Issue Distribution:**
| Field | Type | Description |
|-------|------|-------------|
| `security_vulnerabilities` | number | Count of security issues |
| `code_smells` | number | Count of code smell issues |
| `best_practices` | number | Count of best practice violations |
| `performance_issues` | number | Count of performance issues |

### Frontend Usage Example (JavaScript)
```javascript
const getCodeMetrics = async (codeString) => {
  const response = await fetch('https://code-review-and-bug-generator-backend-2.onrender.com/api/code-metrics', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code: codeString,
      api_key: null
    })
  });
  
  const result = await response.json();
  
  if (result.status === "error") {
    console.error("Error:", result.error_message);
    return null;
  }
  
  return {
    metrics: result.summary_metrics,
    distribution: result.issue_distribution
  };
};
```

---

## Endpoint 4: Inject Bugs

Injects specified bugs into code for testing purposes.

### Request
```
POST /api/inject-bugs
Content-Type: application/json
```

**Body:**
```json
{
  "code": "def add(a, b):\n    return a + b",
  "bug_type": "Security Vulnerability",
  "severity_level": 5,
  "num_bugs": 2,
  "api_key": null
}
```

**Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `code` | string | ❌ No | - | Code to inject bugs into. If not provided, uses stored code |
| `bug_type` | string | ❌ No | "Security Vulnerability" | Type of bug (e.g., "SQL Injection", "Division by Zero", "Memory Leak") |
| `severity_level` | number | ❌ No | 5 | Severity: 1=Low, 2=Medium, 3=High, 4=Critical, 5=Extreme |
| `num_bugs` | number | ❌ No | 2 | Number of bugs to inject (1-10) |
| `api_key` | string\|null | ❌ No | null | Gemini API key |

### Response

**Success (200):**
```json
{
  "status": "success",
  "buggy_code": "import sqlite3\n\ndef get_user(username):\n    conn = sqlite3.connect('users.db')\n    cursor = conn.cursor()\n    query = f\"SELECT * FROM users WHERE username = '{username}'\"\n    cursor.execute(query)\n    return cursor.fetchall()",
  "bugs_injected": [
    {
      "type": "SQL Injection",
      "line_number": 6,
      "description": "The code uses string formatting to construct SQL query, making it vulnerable to SQL injection attacks."
    },
    {
      "type": "Resource Leak",
      "line_number": 7,
      "description": "Database connection is not properly closed, leading to resource leaks."
    }
  ],
  "total_bugs_injected": 2,
  "error_message": null
}
```

**Error (200):**
```json
{
  "status": "error",
  "buggy_code": "",
  "bugs_injected": [],
  "total_bugs_injected": 0,
  "error_message": "No code provided. Please provide code in request or load code using /code-input endpoint"
}
```

**Bug Object Structure:**
| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Type of bug injected |
| `line_number` | number | Line where bug was injected |
| `description` | string | Explanation of the bug |

### Frontend Usage Example (JavaScript)
```javascript
const injectBugs = async (codeString, bugType = "Security Vulnerability", severity = 5, numBugs = 2) => {
  const response = await fetch('https://code-review-and-bug-generator-backend-2.onrender.com/api/inject-bugs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code: codeString,
      bug_type: bugType,
      severity_level: severity,
      num_bugs: numBugs,
      api_key: null
    })
  });
  
  const result = await response.json();
  
  if (result.status === "error") {
    console.error("Error:", result.error_message);
    return null;
  }
  
  return {
    buggyCode: result.buggy_code,
    bugs: result.bugs_injected
  };
};

// Usage
const originalCode = "def add(a, b):\\n    return a + b";
const result = await injectBugs(originalCode, "SQL Injection", 5, 2);
console.log("Buggy code:", result.buggyCode);
console.log("Bugs:", result.bugs);
```

---

## Complete Frontend Integration Example (React)

```javascript
import React, { useState } from 'react';

const API_BASE = 'https://code-review-and-bug-generator-backend-2.onrender.com';

function CodeAnalyzer() {
  const [code, setCode] = useState('');
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeCode = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE}/api/analyze-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: code,  // Code from textarea (with \n)
          api_key: null
        })
      });
      
      const result = await response.json();
      
      if (result.status === "error") {
        setError(result.error_message);
      } else {
        setIssues(result.issues);
      }
    } catch (err) {
      setError("Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Enter your Python code here..."
        rows={10}
        cols={50}
      />
      <button onClick={analyzeCode} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Code'}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {issues.length > 0 && (
        <div className="issues">
          <h3>Found {issues.length} issue(s):</h3>
          {issues.map((issue, idx) => (
            <div key={idx} className={`issue ${issue.severity.toLowerCase()}`}>
              <h4>{issue.title} ({issue.severity})</h4>
              <p><strong>Line {issue.lineNumber}:</strong> {issue.description}</p>
              <p><strong>Fix:</strong> {issue.suggestedFix}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CodeAnalyzer;
```

---

## Common Bug Types for Injection

- `"SQL Injection"`
- `"Cross-Site Scripting (XSS)"`
- `"Buffer Overflow"`
- `"Memory Leak"`
- `"Division by Zero"`
- `"Null Pointer Dereference"`
- `"Race Condition"`
- `"Path Traversal"`
- `"Command Injection"`
- `"Insecure Deserialization"`
- `"Security Vulnerability"` (generic)

---

## Error Codes and Handling

All endpoints return **HTTP 200** even on errors. Check the `status` field:

```javascript
if (response.status === "error") {
  // Handle error - check error_message field
  console.error(response.error_message);
} else {
  // Success - process data
}
```

**Common Errors:**
- `"No code provided. Please provide code in request or load code using /code-input endpoint"`
- `"API_KEY is required. Provide it in the request or set API_KEY environment variable."`
- `"SystemMessages are not yet supported!"` (Fixed in latest version)
- Network timeout (Gemini API slow)

---

## Rate Limiting and Performance

- **Response Time**: 3-30 seconds (depends on code size and Gemini API)
- **Rate Limits**: Subject to Gemini API limits
- **Timeout**: Consider 60-second timeout on frontend
- **Code Size**: Works best with < 1000 lines

---

## Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "code-analyzer"
}
```

Use this to check if the API is alive before making requests.
