# API Documentation

Complete API reference for Nexus AI backend services.

## 📋 Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Code Generation](#code-generation)
  - [Code Execution](#code-execution)
  - [Testing](#testing)
  - [Self-Healing Agent](#self-healing-agent)
  - [Code Review](#code-review)
  - [Security Scanning](#security-scanning)
  - [Performance Analysis](#performance-analysis)
  - [Confidence Scoring](#confidence-scoring)
  - [Decision Engine](#decision-engine)
- [WebSocket Events](#websocket-events)
- [SDKs and Clients](#sdks-and-clients)

---

## Base URL

```
Production: https://api.nexus-ai.com
Development: http://localhost:8000
```

All endpoints are prefixed with `/api/v1` in production.

---

## Authentication

### API Key Authentication

Include your API key in the request headers:

```bash
curl -H "X-API-Key: your-api-key-here" \
  http://localhost:8000/generate
```

### Bearer Token Authentication

```bash
curl -H "Authorization: Bearer your-token-here" \
  http://localhost:8000/generate
```

> **Note**: Authentication is optional in development mode but required in production.

---

## Rate Limiting

| Tier | Requests per Minute | Burst Limit |
|------|---------------------|-------------|
| Anonymous | 100 | 20 |
| Authenticated | 1000 | 100 |
| Enterprise | 10000 | 1000 |

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1690000000
```

---

## Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    // Response payload
  },
  "error": null,
  "timestamp": "2026-07-15T10:00:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "prompt",
      "issue": "Prompt cannot be empty"
    }
  },
  "timestamp": "2026-07-15T10:00:00Z"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Endpoint doesn't exist |
| 422 | Validation Error - Input validation failed |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Input validation failed |
| `AUTHENTICATION_ERROR` | Missing or invalid API key |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `SANDBOX_ERROR` | Code execution failed |
| `TEST_FAILED` | Tests did not pass |
| `MAX_RETRIES_EXCEEDED` | Maximum repair attempts reached |
| `OPENAI_ERROR` | OpenAI API call failed |
| `INTERNAL_ERROR` | Unexpected server error |

---

## Endpoints

### Health Check

#### `GET /health`

Check if the API is healthy.

**Response**:
```json
{
  "status": "healthy",
  "service": "nexus-ai",
  "version": "0.1.0",
  "timestamp": "2026-07-15T10:00:00Z"
}
```

---

### Code Generation

#### `POST /generate`

Generate code from a natural language prompt.

**Request Body**:
```json
{
  "prompt": "Write a Python function to calculate the factorial of a number",
  "language": "python",
  "max_tokens": 2048,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
    "language": "python",
    "tokens_used": 150,
    "model": "gpt-4o"
  }
}
```

---

### Code Execution

#### `POST /execute`

Execute code in a secure sandbox.

**Request Body**:
```json
{
  "code": "print('Hello, World!')",
  "language": "python",
  "timeout": 30
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "stdout": "Hello, World!\n",
    "stderr": "",
    "exit_code": 0,
    "execution_time": 0.05,
    "timed_out": false
  }
}
```

---

### Testing

#### `POST /test/run`

Run tests for provided code.

**Request Body**:
```json
{
  "code": "def add(a, b): return a + b",
  "language": "python",
  "test_cases": [
    {
      "name": "test_add_positive",
      "call": "add(2, 3)",
      "expected": 5
    }
  ],
  "attempt": 1
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "passed": true,
    "attempt": 1,
    "execution_time": 0.12,
    "tests_passed": 1,
    "tests_failed": 0,
    "stdout": "test_add_positive PASSED\n",
    "stderr": "",
    "errors": [],
    "exit_code": 0
  }
}
```

#### `GET /test/health`

Health check for testing service.

**Response**:
```json
{
  "status": "healthy",
  "service": "testing"
}
```

---

### Self-Healing Agent

#### `POST /agent/run`

Run the autonomous self-healing agent.

**Request Body**:
```json
{
  "prompt": "Implement a binary search tree with insert and search operations",
  "max_attempts": 5,
  "timeout": 30,
  "language": "python",
  "enable_review": true,
  "enable_security_scan": true,
  "enable_performance_analysis": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "success",
    "attempts": 2,
    "final_code": "class BinarySearchTree:\n    ...",
    "test_results": {
      "passed": true,
      "tests_passed": 5,
      "tests_failed": 0
    },
    "repair_history": [
      {
        "attempt": 1,
        "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
        "fix": "Converted string input to integer",
        "success": false
      },
      {
        "attempt": 2,
        "error": null,
        "fix": null,
        "success": true
      }
    ],
    "logs": [
      "[INFO] Starting agent execution",
      "[INFO] Generated code successfully",
      "[INFO] Running tests...",
      "[ERROR] Test failed: TypeError",
      "[INFO] Analyzing failure...",
      "[INFO] Repairing code...",
      "[INFO] Re-running tests...",
      "[INFO] All tests passed!"
    ],
    "confidence_score": 92.5,
    "execution_time": 15.3
  }
}
```

---

### Code Review

#### `POST /review`

Review code for quality issues.

**Request Body**:
```json
{
  "code": "def add(a, b): return a + b",
  "language": "python",
  "strict": false
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "passed": false,
    "total_issues": 3,
    "suggestions": [
      {
        "category": "missing_comments",
        "severity": "medium",
        "line_number": 1,
        "message": "Function 'add' is missing a docstring",
        "suggestion": "Add a docstring explaining the purpose, parameters, and return value"
      }
    ],
    "summary": {
      "missing_comments": 1,
      "missing_type_hints": 2
    },
    "review_time": 0.002
  }
}
```

---

### Security Scanning

#### `POST /security/scan`

Scan code for security vulnerabilities.

**Request Body**:
```json
{
  "code": "import os; os.system(user_input)",
  "language": "python",
  "strict": false
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "passed": false,
    "total_issues": 1,
    "issues": [
      {
        "category": "command_injection",
        "severity": "critical",
        "risk": "Command injection vulnerability: shell=True allows arbitrary command execution",
        "line_number": 2,
        "code_snippet": "os.system(user_input)",
        "recommendation": "Avoid using shell=True. Use array-style arguments instead"
      }
    ],
    "summary": {
      "command_injection": 1
    },
    "scan_time": 0.003
  }
}
```

---

### Performance Analysis

#### `POST /performance`

Analyze code performance.

**Request Body**:
```json
{
  "code": "def bubble_sort(arr): ...",
  "language": "python",
  "input_size": 1000,
  "strict": false
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "passed": false,
    "total_suggestions": 4,
    "complexity": {
      "time_complexity": "O(n^2)",
      "space_complexity": "O(1)",
      "estimated_memory_mb": 0.1
    },
    "suggestions": [
      {
        "category": "nested_loops",
        "severity": "high",
        "message": "Nested loops detected - potential O(n^2) complexity",
        "suggestion": "Consider using a hash table (dict) to reduce complexity to O(n)"
      }
    ],
    "alternative_algorithms": [
      {
        "name": "Timsort (Python's built-in sort)",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)"
      }
    ],
    "summary": {
      "nested_loops": 1
    },
    "analysis_time": 0.004
  }
}
```

---

### Confidence Scoring

#### `POST /confidence`

Calculate confidence score for code.

**Request Body**:
```json
{
  "code": "def add(a, b): return a + b",
  "test_results": {
    "passed": true,
    "tests_passed": 3,
    "tests_failed": 0
  },
  "security_scan": {
    "passed": true,
    "total_issues": 0
  },
  "performance_analysis": {
    "passed": true,
    "time_complexity": "O(1)",
    "space_complexity": "O(1)"
  },
  "repair_attempts": 1,
  "max_attempts": 5,
  "has_documentation": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "score": 96.4,
    "letter_grade": "A",
    "production_ready": true,
    "explanation": "Code is production-ready with a confidence score of 96.4/100 (Grade: A)...",
    "breakdown": {
      "test_score": 100.0,
      "security_score": 100.0,
      "performance_score": 100.0,
      "repair_score": 64.0,
      "documentation_score": 100.0,
      "complexity_score": 100.0,
      "weights": {
        "test": 0.30,
        "security": 0.20,
        "performance": 0.15,
        "repair": 0.10,
        "documentation": 0.10,
        "complexity": 0.15
      }
    },
    "recommendations": []
  }
}
```

---

### Decision Engine

#### `POST /decision/classify`

Classify a failure and determine repair strategy.

**Request Body**:
```json
{
  "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "stdout": "",
  "stderr": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "exit_code": 1,
  "execution_time": 0.05,
  "timeout": 30
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "failure_type": "runtime",
    "severity": "medium",
    "repair_strategy": "Fix runtime errors by handling edge cases and type mismatches",
    "confidence": 0.9,
    "suggested_prompt": "Fix the following Python runtime error:\nTypeError: ...\n\nCode:\ndef add(a, b): return a + b\n\nReturn ONLY the corrected code. No explanations.",
    "original_error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
    "metadata": {
      "matched_pattern": "TypeError",
      "context": {}
    }
  }
}
```

#### `POST /decision/repair-prompt`

Get repair prompt for a specific error.

**Request Body**:
```json
{
  "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "code": "def add(a, b): return a + b"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "repair_prompt": "Fix the following Python runtime error:\nTypeError: ...\n\nCode:\ndef add(a, b): return a + b\n\nReturn ONLY the corrected code. No explanations."
  }
}
```

#### `GET /decision/failure-types`

List all registered failure types.

**Response**:
```json
{
  "success": true,
  "data": {
    "failure_types": ["syntax", "runtime", "assertion", "import", "timeout", "security", "performance", "unknown"]
  }
}
```

#### `POST /decision/register-failure-type`

Register a new failure type.

**Request Body**:
```json
{
  "failure_type": "custom_error",
  "patterns": ["CustomError", "custom error"],
  "severity": "medium",
  "repair_strategy": "Fix custom errors by following error message instructions",
  "base_prompt": "Fix the following custom error:\n{error}\n\nCode:\n{code}\n\nReturn ONLY the corrected code."
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "message": "Failure type 'custom_error' registered successfully"
  }
}
```

---

## WebSocket Events

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to Nexus AI');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

### Event Types

| Event | Description | Payload |
|-------|-------------|---------|
| `agent.start` | Agent execution started | `{ prompt, max_attempts }` |
| `agent.thought` | Agent reasoning step | `{ thought, step }` |
| `agent.action` | Agent action executed | `{ action, input, output }` |
| `agent.observation` | Agent observation | `{ observation, step }` |
| `test.run` | Tests are running | `{ attempt, total_tests }` |
| `test.result` | Test result received | `{ passed, tests_passed, tests_failed }` |
| `repair.start` | Repair started | `{ attempt, error }` |
| `repair.complete` | Repair completed | `{ attempt, success, fixed_code }` |
| `agent.complete` | Agent execution completed | `{ status, attempts, confidence }` |
| `agent.error` | Agent error occurred | `{ error, step }` |

### Example Events

```json
{
  "event": "agent.thought",
  "data": {
    "thought": "I need to implement a factorial function. I'll use recursion.",
    "step": 1
  }
}
```

```json
{
  "event": "test.result",
  "data": {
    "passed": false,
    "tests_passed": 2,
    "tests_failed": 1,
    "errors": ["AssertionError: factorial(5) != 120"]
  }
}
```

```json
{
  "event": "agent.complete",
  "data": {
    "status": "success",
    "attempts": 2,
    "confidence": 92.5
  }
}
```

---

## SDKs and Clients

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

class NexusAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["X-API-Key"] = api_key

    def generate(self, prompt: str, language: str = "python"):
        response = requests.post(
            f"{BASE_URL}/generate",
            headers=self.headers,
            json={"prompt": prompt, "language": language}
        )
        return response.json()

    def run_tests(self, code: str, test_cases: list = None):
        response = requests.post(
            f"{BASE_URL}/test/run",
            headers=self.headers,
            json={"code": code, "test_cases": test_cases}
        )
        return response.json()

    def agent_run(self, prompt: str, max_attempts: int = 5):
        response = requests.post(
            f"{BASE_URL}/agent/run",
            headers=self.headers,
            json={"prompt": prompt, "max_attempts": max_attempts}
        )
        return response.json()

# Usage
client = NexusAIClient(api_key="your-api-key")
result = client.generate("Write a factorial function")
print(result)
```

### JavaScript/TypeScript Client

```typescript
class NexusAIClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(baseUrl: string, apiKey?: string) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (this.apiKey) {
      headers["X-API-Key"] = this.apiKey;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    return response.json();
  }

  async generate(prompt: string, language: string = "python") {
    return this.request("/generate", {
      method: "POST",
      body: JSON.stringify({ prompt, language }),
    });
  }

  async runTests(code: string, testCases?: any[]) {
    return this.request("/test/run", {
      method: "POST",
      body: JSON.stringify({ code, test_cases: testCases }),
    });
  }

  async agentRun(prompt: string, maxAttempts: number = 5) {
    return this.request("/agent/run", {
      method: "POST",
      body: JSON.stringify({ prompt, max_attempts: maxAttempts }),
    });
  }
}

// Usage
const client = new NexusAIClient("http://localhost:8000", "your-api-key");
const result = await client.generate("Write a factorial function");
console.log(result);
```

---

## Next Steps

- [Usage Guide](./USAGE.md) - Learn how to use Nexus AI
- [Best Practices](./BEST_PRACTICES.md) - Development guidelines
- [Architecture](./ARCHITECTURE.md) - System design overview
