# Usage Guide

This guide provides comprehensive usage examples and tutorials for Nexus AI.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)
- [API Usage](#api-usage)
- [Frontend Usage](#frontend-usage)
- [Common Workflows](#common-workflows)
- [Tips and Tricks](#tips-and-tricks)

---

## Quick Start

### 1. Start the Application

```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### 2. Open the Dashboard

Navigate to `http://localhost:3000` in your browser.

### 3. Enter Your First Prompt

Try this example:
```
Write a Python function to calculate the factorial of a number
```

### 4. Watch the Magic

The agent will:
1. Generate code using AI
2. Run tests automatically
3. Fix any failures
4. Retry until all tests pass

---

## Basic Usage

### Via Web Interface

#### Landing Page
- Visit `http://localhost:3000`
- Explore the 3D particle background
- Click "Get Started" to navigate to the dashboard

#### Dashboard
1. **Enter Prompt**: Type your coding problem in natural language
2. **Configure Settings** (optional):
   - Maximum repair attempts (1-10)
   - Execution timeout (10-120 seconds)
   - Enable/disable features (code review, security scan, etc.)
3. **Execute**: Click "Generate and Heal"
4. **Monitor**: Watch real-time logs and progress
5. **Review**: Examine the final code, test results, and confidence score

### Via API

#### Generate Code

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to reverse a linked list",
    "language": "python"
  }'
```

#### Run Tests

```bash
curl -X POST http://localhost:8000/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def reverse_list(head): ...",
    "language": "python"
  }'
```

#### Full Self-Healing Loop

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Implement binary search with comprehensive tests",
    "max_attempts": 5,
    "timeout": 30
  }'
```

---

## Advanced Usage

### Custom Test Cases

You can provide custom test cases for more precise validation:

```bash
curl -X POST http://localhost:8000/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b): return a + b",
    "test_cases": [
      {"name": "test_add_positive", "call": "add(2, 3)", "expected": 5},
      {"name": "test_add_negative", "call": "add(-1, 1)", "expected": 0},
      {"name": "test_add_zero", "call": "add(0, 0)", "expected": 0}
    ]
  }'
```

### Code Review

Review generated code for quality issues:

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b): return a + b",
    "strict": true
  }'
```

### Security Scanning

Scan code for security vulnerabilities:

```bash
curl -X POST http://localhost:8000/security/scan \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import os; os.system(user_input)",
    "strict": false
  }'
```

### Performance Analysis

Analyze code performance and get optimization suggestions:

```bash
curl -X POST http://localhost:8000/performance \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def bubble_sort(arr): ...",
    "input_size": 1000,
    "strict": false
  }'
```

### Confidence Scoring

Calculate confidence score for generated code:

```bash
curl -X POST http://localhost:8000/confidence \
  -H "Content-Type: application/json" \
  -d '{
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
    "repair_attempts": 1,
    "max_attempts": 5
  }'
```

---

## API Usage

### Authentication

Currently, Nexus AI uses API keys for authentication (optional in development):

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "prompt": "Write a Python function"
  }'
```

### Rate Limiting

API requests are rate-limited to prevent abuse:
- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per API key

### Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2026-07-15T10:00:00Z"
}
```

### Error Handling

Errors are returned with appropriate HTTP status codes:

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

## Frontend Usage

### Landing Page Features

1. **3D Particle Background**: Interactive Three.js visualization
2. **Feature Showcase**: Animated cards highlighting key features
3. **Tech Stack Display**: Badges showing technologies used
4. **Call-to-Action**: Buttons to get started or view demo

### Dashboard Features

1. **Prompt Input**: Text area for coding problems
2. **Configuration Panel**:
   - Max attempts slider
   - Timeout setting
   - Feature toggles
3. **Real-time Logs**: Live streaming of agent thoughts and actions
4. **Code Viewer**: Syntax-highlighted code display
5. **Test Results**: Visual test pass/fail indicators
6. **Timeline**: Chronological view of execution steps
7. **Confidence Score**: Visual gauge showing code confidence

### Navigation

- **/** - Landing page
- **/dashboard** - Main agent interaction interface
- **/agent-demo** - Hackathon demo flow
- **/timeline** - Execution history
- **/history** - Past executions
- **/settings** - User preferences

---

## Common Workflows

### Workflow 1: Basic Code Generation

```bash
# 1. Generate code
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to check if a string is a palindrome"
  }'

# 2. Review the generated code
# 3. Run tests
# 4. Iterate if needed
```

### Workflow 2: Autonomous Self-Healing

```bash
# Let the agent handle everything
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Implement a calculator with add, subtract, multiply, divide",
    "max_attempts": 5,
    "timeout": 30
  }'

# The agent will:
# 1. Generate code
# 2. Run tests
# 3. Fix failures
# 4. Retry until success or max attempts
```

### Workflow 3: Code Quality Analysis

```bash
# 1. Generate code
# 2. Review for quality issues
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "your_code_here"}'

# 3. Scan for security issues
curl -X POST http://localhost:8000/security/scan \
  -H "Content-Type: application/json" \
  -d '{"code": "your_code_here"}'

# 4. Analyze performance
curl -X POST http://localhost:8000/performance \
  -H "Content-Type: application/json" \
  -d '{"code": "your_code_here"}'

# 5. Calculate confidence
curl -X POST http://localhost:8000/confidence \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your_code_here",
    "test_results": {...},
    "security_scan": {...}
  }'
```

---

## Tips and Tricks

### Tip 1: Write Clear Prompts

**Good**:
```
Write a Python function that takes a list of integers and returns the sum of all even numbers
```

**Bad**:
```
make a function
```

### Tip 2: Use Specific Test Cases

Provide detailed test cases for better validation:

```json
{
  "test_cases": [
    {
      "name": "test_empty_list",
      "call": "sum_even([])",
      "expected": 0
    },
    {
      "name": "test_all_odd",
      "call": "sum_even([1, 3, 5])",
      "expected": 0
    },
    {
      "name": "test_all_even",
      "call": "sum_even([2, 4, 6])",
      "expected": 12
    }
  ]
}
```

### Tip 3: Enable Strict Mode

For production code, enable strict mode for thorough analysis:

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "your_code", "strict": true}'
```

### Tip 4: Monitor Execution

Use the dashboard's real-time logs to:
- Understand agent reasoning
- Debug failures
- Optimize prompts

### Tip 5: Iterate on Results

If the agent fails after max attempts:
1. Review the logs to understand the failure
2. Refine your prompt with more details
3. Increase max attempts if needed
4. Provide custom test cases

---

## Next Steps

- [API Reference](./API.md) - Detailed API documentation
- [Best Practices](./BEST_PRACTICES.md) - Development guidelines
- [Architecture](./ARCHITECTURE.md) - System design overview
- [Troubleshooting](./TROUBLESHOOTING.md) - Common issues and solutions
