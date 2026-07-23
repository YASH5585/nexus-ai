# Best Practices

Development guidelines and best practices for working with Nexus AI.

## 📋 Table of Contents

- [Code Style](#code-style)
- [Backend Development](#backend-development)
- [Frontend Development](#frontend-development)
- [API Design](#api-design)
- [Testing](#testing)
- [Security](#security)
- [Performance](#performance)
- [Documentation](#documentation)
- [Git Workflow](#git-workflow)
- [Code Review](#code-review)

---

## Code Style

### Python (Backend)

#### Formatting
- Use **Black** formatter with default settings
- Line length: 88 characters (Black default)
- Use double quotes for strings

```bash
# Format code
black backend/

# Check formatting
black --check backend/
```

#### Type Hints
- All function signatures must include type hints
- Use `typing` module for complex types
- Use `List`, `Dict`, `Optional` instead of `list`, `dict`, `Union`

```python
# Good
def process_data(items: List[Dict[str, Any]]) -> Optional[str]:
    pass

# Bad
def process_data(items):
    pass
```

#### Docstrings
- All public functions, classes, and modules must have docstrings
- Use Google-style docstrings

```python
def calculate_factorial(n: int) -> int:
    """
    Calculate the factorial of a number.

    Args:
        n: Non-negative integer

    Returns:
        Factorial of n

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return 1 if n == 0 else n * calculate_factorial(n - 1)
```

#### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### TypeScript/JavaScript (Frontend)

#### Formatting
- Use **Prettier** with project configuration
- Use single quotes for strings
- Semicolons required

```bash
# Format code
npm run format

# Check formatting
npm run format:check
```

#### TypeScript
- All components must have TypeScript types
- Avoid `any` type - use proper types or `unknown`
- Use interfaces for object shapes

```typescript
// Good
interface User {
  id: string;
  name: string;
  email: string;
}

function getUser(id: string): Promise<User> {
  // ...
}

// Bad
function getUser(id: any): Promise<any> {
  // ...
}
```

#### Naming Conventions
- Components: `PascalCase`
- Functions/variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Files: `kebab-case` for pages, `PascalCase` for components

---

## Backend Development

### Service Layer

#### Structure
- One service per domain concern
- Services should be stateless
- Use dependency injection for testability

```python
# Good
class CodeReviewer:
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger

    def review(self, code: str) -> CodeReviewReport:
        # Implementation
        pass

# Bad
class CodeReviewer:
    def review(self, code: str):
        # No type hints, no dependency injection
        pass
```

#### Error Handling
- Use custom exceptions from `app.core.exceptions`
- Catch specific exceptions, not generic `Exception`
- Always log errors with context

```python
# Good
try:
    result = await self._execute_pytest(test_file)
except subprocess.TimeoutExpired:
    self.logger.error("Test execution timed out", timeout=self.timeout)
    raise TestExecutionError(f"Timeout after {self.timeout}s")
except Exception as e:
    self.logger.error("Unexpected error", error=str(e))
    raise

# Bad
try:
    result = await self._execute_pytest(test_file)
except:
    pass  # Silent failure
```

#### Logging
- Use `structlog` for structured logging
- Include contextual fields (run_id, step, attempt)
- Use appropriate log levels

```python
# Good
self.logger.info(
    "Test execution completed",
    passed=report.passed,
    tests_passed=report.tests_passed,
    tests_failed=report.tests_failed,
    duration_ms=report.duration_ms
)

# Bad
print("Test execution completed")
```

### API Design

#### Route Handlers
- Keep route handlers thin - delegate to services
- Use Pydantic models for request/response validation
- Return consistent response format

```python
# Good
@router.post("/run", response_model=TestResponse)
async def run_tests(request: TestRequest) -> TestResponse:
    engine = TestingEngine(timeout=30)
    report = await engine.run_tests(
        code=request.code,
        test_cases=request.test_cases,
        attempt=request.attempt
    )
    return engine.to_dict(report)

# Bad
@router.post("/run")
async def run_tests(request):
    # No type hints, no validation, no error handling
    pass
```

#### Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error (Pydantic)
- `500` - Internal Server Error

---

## Frontend Development

### Component Structure

```
components/
├── ui/                    # Base UI primitives
│   ├── Button.tsx
│   ├── Card.tsx
│   └── Input.tsx
├── landing/               # Landing page sections
│   ├── Hero.tsx
│   ├── Features.tsx
│   └── TechStack.tsx
├── dashboard/             # Dashboard components
│   ├── PromptInput.tsx
│   ├── CodeViewer.tsx
│   └── TestResults.tsx
└── three-background/      # 3D components
    └── ParticleBackground.tsx
```

### Component Best Practices

- Use functional components with hooks
- Keep components small and focused (< 200 lines)
- Extract reusable logic into custom hooks
- Use `memo` for expensive components

```typescript
// Good
export const PromptInput = memo(function PromptInput({
  value,
  onChange,
  onSubmit
}: PromptInputProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    await onSubmit(value);
    setIsSubmitting(false);
  };

  return (
    <div>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter your prompt..."
      />
      <Button onClick={handleSubmit} disabled={isSubmitting}>
        {isSubmitting ? 'Generating...' : 'Generate'}
      </Button>
    </div>
  );
});
```

### State Management

- Use React Context for global state
- Keep state as local as possible
- Use `useReducer` for complex state logic

```typescript
// Good
interface AppState {
  prompt: string;
  isRunning: boolean;
  logs: LogEntry[];
}

const AppContext = createContext<AppState | null>(null);

function appReducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_PROMPT':
      return { ...state, prompt: action.payload };
    case 'SET_RUNNING':
      return { ...state, isRunning: action.payload };
    default:
      return state;
  }
}
```

### Styling

- Use Tailwind CSS for styling
- Follow utility-first approach
- Create reusable component variants

```typescript
// Good
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-white hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);
```

---

## API Design

### RESTful Conventions

- Use nouns, not verbs, in endpoints: `/generate` not `/doGenerate`
- Use HTTP methods appropriately: GET (read), POST (create), PUT (update), DELETE (delete)
- Use plural nouns: `/agents` not `/agent`
- Version APIs: `/api/v1/endpoint`

### Request/Response Design

- Use Pydantic models for validation
- Return consistent response structure
- Include timestamps in all responses
- Use appropriate HTTP status codes

```python
# Good
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    language: str = Field(default="python", pattern="^(python|javascript)$")

class GenerateResponse(BaseModel):
    code: str
    language: str
    tokens_used: int
```

### Error Responses

```python
class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
```

---

## Testing

### Backend Tests

- Use **pytest** for testing
- Write unit tests for all services
- Write integration tests for API endpoints
- Aim for 80%+ code coverage

```python
# Good
import pytest
from app.services.tester import TestingEngine

@pytest.mark.asyncio
async def test_run_tests_success():
    engine = TestingEngine(timeout=30)
    code = "def add(a, b): return a + b"
    report = await engine.run_tests(code, attempt=1)

    assert report.passed is True
    assert report.tests_passed > 0
    assert report.tests_failed == 0
```

### Frontend Tests

- Use **Jest** and **React Testing Library**
- Test component behavior, not implementation
- Mock API calls

```typescript
// Good
import { render, screen, fireEvent } from '@testing-library/react';
import { PromptInput } from './PromptInput';

test('calls onSubmit when form is submitted', async () => {
  const mockOnSubmit = jest.fn();
  render(<PromptInput onSubmit={mockOnSubmit} />);

  const input = screen.getByPlaceholderText('Enter your prompt...');
  const button = screen.getByRole('button', { name: 'Generate' });

  fireEvent.change(input, { target: { value: 'Write a factorial function' } });
  fireEvent.click(button);

  expect(mockOnSubmit).toHaveBeenCalledWith('Write a factorial function');
});
```

### Test Organization

```
tests/
├── unit/                   # Unit tests
│   ├── services/
│   │   ├── test_tester.py
│   │   ├── test_decision_engine.py
│   │   └── test_code_reviewer.py
│   └── models/
│       └── test_schemas.py
├── integration/            # Integration tests
│   ├── test_api.py
│   └── test_websocket.py
├── fixtures/               # Test fixtures
│   ├── sample_code.py
│   └── test_cases.json
└── conftest.py            # Pytest configuration
```

---

## Security

### Input Validation
- Always validate user input with Pydantic
- Sanitize code before execution
- Limit input sizes

```python
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    code: Optional[str] = Field(default=None, max_length=100000)
```

### Sandbox Isolation
- Execute code in isolated subprocesses
- Set resource limits (timeout, memory, CPU)
- Use temporary directories that are cleaned up

```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Code executes here
    # Directory is automatically cleaned up
    pass
```

### Secrets Management
- Never commit secrets to version control
- Use environment variables for configuration
- Rotate API keys regularly

```bash
# Good - use environment variables
OPENAI_API_KEY=sk-...

# Bad - hardcoded in code
api_key = "sk-..."
```

### Dependency Security
- Regularly update dependencies
- Use `pip-audit` or `safety` to check for vulnerabilities
- Review dependencies before adding

```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

## Performance

### Backend Performance

- Use async/await for I/O-bound operations
- Use connection pooling for databases
- Cache frequently accessed data
- Profile code before optimizing

```python
# Good - async for I/O
async def generate_code(prompt: str) -> str:
    response = await openai_client.generate(prompt)
    return response

# Bad - blocking I/O
def generate_code(prompt: str) -> str:
    response = openai_client.generate(prompt)  # Blocks event loop
    return response
```

### Frontend Performance

- Use code splitting and lazy loading
- Optimize images and assets
- Minimize bundle size
- Use React.memo for expensive components

```typescript
// Good - lazy loading
const CodeViewer = lazy(() => import('./CodeViewer'));

function Dashboard() {
  return (
    <Suspense fallback={<Loading />}>
      <CodeViewer />
    </Suspense>
  );
}
```

### Database Performance

- Use indexes for frequently queried fields
- Avoid N+1 queries
- Use connection pooling
- Monitor query performance

---

## Documentation

### Code Documentation

- Write docstrings for all public functions/classes
- Include examples in docstrings
- Document complex algorithms
- Keep comments up-to-date

```python
def analyze_execution_result(
    self,
    stdout: str,
    stderr: str,
    exit_code: int,
    execution_time: float,
    timeout: int = 30
) -> DecisionEngineResult:
    """
    Analyze execution results and classify any failures.

    This method processes the output from code execution and uses
    pattern matching to classify the failure type and determine
    the appropriate repair strategy.

    Args:
        stdout: Standard output from execution
        stderr: Standard error from execution
        exit_code: Process exit code (0 = success)
        execution_time: Execution time in seconds
        timeout: Timeout threshold in seconds

    Returns:
        DecisionEngineResult with classification and repair strategy

    Example:
        >>> engine = DecisionEngine()
        >>> result = engine.analyze_execution_result(
        ...     stdout="",
        ...     stderr="TypeError: unsupported operand type(s)",
        ...     exit_code=1,
        ...     execution_time=0.05
        ... )
        >>> result.classification.failure_type
        <FailureType.RUNTIME: 'runtime'>
    """
```

### README Documentation

- Keep README up-to-date
- Include quick start guide
- Document environment variables
- Add troubleshooting section

---

## Git Workflow

### Branch Naming

```
feature/add-code-review-service
bugfix/fix-test-timeout
hotfix/security-patch
refactor/improve-decision-engine
docs/update-installation-guide
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

**Examples**:
```
feat(services): add performance analyzer service

Implements AST-based performance analysis with complexity estimation
and optimization suggestions.

Closes #123
```

```
fix(api): handle timeout errors in test runner

Previously, timeout errors were not properly caught and resulted in
500 errors. Now they're handled gracefully with a meaningful error
message.

Fixes #456
```

### Pull Request Process

1. Create feature branch from `main`
2. Make changes and commit
3. Push branch to remote
4. Create pull request with description
5. Wait for CI checks to pass
6. Address review comments
7. Squash and merge

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] All tests passing
- [ ] No merge conflicts
```

---

## Code Review

### Review Checklist

- [ ] Code is readable and well-structured
- [ ] Functions are small and focused
- [ ] Type hints are present
- [ ] Docstrings are complete
- [ ] Error handling is appropriate
- [ ] Tests are included
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Documentation updated
- [ ] No unnecessary complexity

### Review Guidelines

- Be respectful and constructive
- Focus on code, not the author
- Explain why changes are needed
- Suggest alternatives, don't just criticize
- Approve when satisfied, don't nitpick

---

## Next Steps

- [Architecture](./ARCHITECTURE.md) - System design overview
- [API Documentation](./API.md) - Complete API reference
- [Troubleshooting](./TROUBLESHOOTING.md) - Common issues and solutions
