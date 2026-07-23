# Architecture

System architecture and design decisions for Nexus AI.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Decisions](#design-decisions)
- [Scalability](#scalability)
- [Security Architecture](#security-architecture)
- [Deployment Architecture](#deployment-architecture)

---

## Overview

Nexus AI follows a **layered microservices architecture** designed for scalability, maintainability, and extensibility. The system is built around the concept of an **autonomous agent** that can generate code, test it, identify failures, and iteratively repair itself until all tests pass.

### Key Architectural Principles

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Dependency Injection**: Promotes testability and loose coupling
3. **Stateless Services**: Enables horizontal scaling
4. **Event-Driven Communication**: Loose coupling between components
5. **Fail-Safe Defaults**: Secure by default configuration

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Presentation Layer                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Next.js 15 Frontend                     │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │   Landing    │  │  Dashboard   │  │Agent Demo    │   │  │
│  │  │   Page       │  │              │  │              │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │           React Components + Tailwind CSS            │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST + WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          API Gateway Layer                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Backend                         │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │                   API Routers                         │ │  │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │  │
│  │  │  │   /generate │  │   /execute  │  │   /repair   │  │ │  │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  │ │  │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │  │
│  │  │  │ /agent/run  │  │   /test     │  │  /review    │  │ │  │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  │ │  │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │  │
│  │  │  │ /security   │  │ /performance│  │ /confidence │  │ │  │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │              Middleware (CORS, Auth, etc.)           │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Internal Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Service Layer                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │    OpenAI    │  │   Sandbox    │  │    Agent     │   │  │
│  │  │   Service    │  │   Service    │  │   Engine     │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │   Testing    │  │  Decision    │  │    Code      │   │  │
│  │  │   Engine     │  │   Engine     │  │   Reviewer   │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │   Security   │  │Performance   │  │ Confidence   │   │  │
│  │  │   Scanner    │  │  Analyzer    │  │   Engine     │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Subprocess / HTTP
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Infrastructure Layer                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │   OpenAI     │  │   pytest     │  │   Python     │   │  │
│  │  │   API        │  │   Runner     │  │  Sandbox     │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │  PostgreSQL  │  │    Redis     │  │ Prometheus   │   │  │
│  │  │  Database    │  │    Cache     │  │  Monitoring  │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Presentation Layer (Frontend)

```
frontend/
├── app/                      # Next.js App Router
│   ├── page.tsx             # Landing page with 3D background
│   ├── dashboard/           # Agent interaction dashboard
│   ├── agent-demo/          # Hackathon demo flow
│   ├── timeline/            # Execution history timeline
│   ├── history/             # Past executions list
│   └── settings/            # User preferences
├── components/              # Reusable UI components
│   ├── ui/                  # Base primitives (Button, Card, Input)
│   ├── landing/             # Landing page sections
│   ├── dashboard/           # Dashboard components
│   └── three-background/    # 3D particle system
├── lib/                     # Utilities and helpers
│   └── utils.ts             # Utility functions
├── styles/                  # Global styles and themes
└── public/                  # Static assets
```

**Key Technologies**:
- Next.js 15 with App Router
- React 19 with Server Components
- TypeScript for type safety
- Tailwind CSS for styling
- Framer Motion for animations
- Three.js for 3D graphics
- Lucide React for icons

### API Gateway Layer (Backend)

```
backend/app/
├── main.py                  # FastAPI app entry point
├── core/                    # Core utilities
│   ├── config.py           # Pydantic Settings
│   ├── logging.py          # Structured logging (structlog)
│   ├── exceptions.py       # Custom exception hierarchy
│   └── di.py               # Dependency injection
├── models/                  # Data models
│   ├── schemas.py          # Pydantic request/response models
│   └── entities.py         # Domain models (dataclasses)
├── services/                # Business logic
│   ├── openai_service.py   # OpenAI API client
│   ├── sandbox_service.py  # Secure code execution
│   ├── tester.py           # Testing engine
│   ├── decision_engine.py  # Failure classification
│   ├── code_reviewer.py    # Static code analysis
│   ├── security_scanner.py # Security vulnerability scanning
│   ├── performance_analyzer.py # Performance analysis
│   ├── confidence_engine.py # Confidence scoring
│   └── healing_service.py  # Self-healing orchestrator
├── routers/                 # API route handlers
│   ├── generate.py         # POST /generate
│   ├── execute.py          # POST /execute
│   ├── repair.py           # POST /repair
│   ├── test.py             # POST /test/run
│   ├── agent.py            # POST /agent/run
│   └── status.py           # GET /status
└── api/                     # Additional API routers
    └── routers/             # Modular routers
        ├── decision.py      # Decision engine endpoints
        ├── reviewer.py      # Code review endpoints
        ├── security.py      # Security scan endpoints
        ├── performance.py   # Performance analysis endpoints
        └── confidence.py    # Confidence scoring endpoints
```

**Key Technologies**:
- FastAPI for REST API
- Pydantic for validation
- Structlog for structured logging
- Uvicorn as ASGI server

### Service Layer

Each service is responsible for a specific domain concern:

| Service | Responsibility |
|---------|---------------|
| **OpenAIService** | Communicate with OpenAI API for code generation and repair |
| **SandboxService** | Execute code in isolated subprocesses with resource limits |
| **TestingEngine** | Generate and run pytest tests against code |
| **DecisionEngine** | Classify failures and determine repair strategies |
| **CodeReviewer** | Static analysis for code quality issues |
| **SecurityScanner** | Scan for security vulnerabilities |
| **PerformanceAnalyzer** | Analyze performance and suggest optimizations |
| **ConfidenceEngine** | Calculate confidence scores across multiple dimensions |
| **HealingService** | Orchestrate the self-healing loop |

---

## Data Flow

### Self-Healing Loop

```
User Prompt
    │
    ▼
┌─────────────────┐
│  Code Generator  │ ← OpenAI API
│  (OpenAI Service)│
└────────┬────────┘
         │ Generated Code
         ▼
┌─────────────────┐
│  Code Reviewer   │ ← Static Analysis
│ (Code Reviewer)  │
└────────┬────────┘
         │ Review Suggestions
         ▼
┌─────────────────┐
│ Security Scanner │ ← Vulnerability Scan
│(Security Scanner)│
└────────┬────────┘
         │ Security Report
         ▼
┌─────────────────┐
│Performance Analy│ ← Complexity Analysis
│(Performance Analy)│
└────────┬────────┘
         │ Performance Report
         ▼
┌─────────────────┐
│  Test Runner     │ ← pytest execution
│ (TestingEngine)  │
└────────┬────────┘
         │ Test Results
         ▼
    ┌────────────┐
    │ All Pass?  │
    └─────┬──────┘
          │
    ┌─────┴─────┐
    │           │
   Yes          No
    │           │
    │           ▼
    │   ┌─────────────────┐
    │   │ Decision Engine  │ ← Classify failure
    │   └────────┬────────┘
    │            │ Classification
    │            ▼
    │   ┌─────────────────┐
    │   │  Repair Engine   │ ← Generate fix
    │   └────────┬────────┘
    │            │ Repaired Code
    │            ▼
    │   (Loop back to Test Runner)
    │
    ▼
┌─────────────────┐
│ Confidence Engine│ ← Multi-factor scoring
└────────┬────────┘
         │ Confidence Score
         ▼
    Final Result
```

### Request Flow

```
Client Request
    │
    ▼
FastAPI Router
    │
    ▼
Dependency Injection
    │
    ▼
Service Layer
    │
    ▼
External APIs / Subprocess
    │
    ▼
Response Formatting
    │
    ▼
Client Response
```

---

## Technology Stack

### Frontend Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| Next.js | React framework | 15.x |
| React | UI library | 19.x |
| TypeScript | Type safety | 5.x |
| Tailwind CSS | Styling | 4.x |
| Framer Motion | Animations | 11.x |
| Three.js | 3D graphics | 0.162.x |
| React Three Fiber | Three.js React bindings | 8.x |
| React Three Drei | Three.js helpers | 3.x |
| Lucide React | Icons | 0.454.x |

### Backend Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| FastAPI | Web framework | 0.115.x |
| Python | Runtime | 3.12.x |
| Pydantic | Data validation | 2.x |
| OpenAI API | AI code generation | 1.x |
| Structlog | Structured logging | 24.x |
| Uvicorn | ASGI server | 0.32.x |
| pytest | Testing framework | 8.x |
| Docker | Containerization | 24.x |

### Infrastructure Stack

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Railway | Backend deployment |
| Vercel | Frontend deployment |
| PostgreSQL | Database (optional) |
| Redis | Caching (optional) |
| Prometheus | Metrics collection |
| Grafana | Monitoring dashboard |

---

## Design Decisions

### 1. Dependency Injection

**Decision**: Use a DI container for service instantiation.

**Rationale**:
- Promotes testability by enabling easy mocking
- Decouples route handlers from concrete implementations
- Centralizes service configuration

**Implementation**:
```python
class Container:
    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        self._services[interface] = implementation

    def get(self, interface):
        return self._services[interface]()
```

### 2. Modular Routers

**Decision**: Separate routers for each domain concern.

**Rationale**:
- Easy to extend or version
- Clear separation of concerns
- Simplifies testing

**Implementation**:
```python
# Each domain has its own router
router = APIRouter(prefix="/test", tags=["testing"])
router = APIRouter(prefix="/review", tags=["reviewer"])
router = APIRouter(prefix="/security", tags=["security"])
```

### 3. Structured Logging

**Decision**: Use structlog with JSON output.

**Rationale**:
- Structured logs are machine-readable
- Easy to query and analyze
- Consistent logging format across services

**Implementation**:
```python
logger.info(
    "Test execution completed",
    passed=report.passed,
    tests_passed=report.tests_passed,
    duration_ms=report.duration_ms
)
```

### 4. Sandbox Isolation

**Decision**: Execute code in subprocesses with timeouts.

**Rationale**:
- Simple and reliable isolation
- No need for containerization
- Easy to set resource limits

**Implementation**:
```python
result = subprocess.run(
    cmd,
    cwd=temp_dir,
    capture_output=True,
    text=True,
    timeout=self.timeout
)
```

### 5. Self-Healing Loop

**Decision**: Centralized HealingService orchestrator.

**Rationale**:
- Single source of truth for healing logic
- Easy to configure retry limits
- Clear execution flow

**Implementation**:
```python
class HealingService:
    async def run(self, context: ExecutionContext) -> ExecutionContext:
        for attempt in range(self._max_retries):
            # Generate → Test → Classify → Repair → Retest
            pass
```

### 6. Decision Engine

**Decision**: Pattern-based classification instead of always calling OpenAI.

**Rationale**:
- Reduces API costs
- Faster response times
- Deterministic behavior for common errors

**Implementation**:
```python
FAILURE_PATTERNS = {
    FailureType.SYNTAX: ["SyntaxError", "IndentationError"],
    FailureType.RUNTIME: ["TypeError", "ValueError", "AttributeError"],
    # ...
}
```

---

## Scalability

### Horizontal Scaling

- **Stateless Services**: All services are stateless, enabling horizontal scaling
- **Load Balancing**: Multiple backend instances behind a load balancer
- **Database Sharding**: PostgreSQL can be sharded by user/project
- **Caching**: Redis for frequently accessed data

### Vertical Scaling

- **Worker Processes**: Uvicorn with multiple workers
- **Connection Pooling**: Database connection pools
- **Resource Limits**: Configurable memory/CPU limits for sandboxes

### Performance Optimization

- **Async I/O**: All I/O operations use async/await
- **Connection Reuse**: HTTP connection pooling
- **Caching**: Redis for session data and frequent queries
- **CDN**: Frontend assets served from CDN

---

## Security Architecture

### Defense in Depth

1. **Network Layer**: Firewall rules, VPN for internal services
2. **Application Layer**: Input validation, authentication, authorization
3. **Service Layer**: Rate limiting, API key validation
4. **Execution Layer**: Sandbox isolation, resource limits
5. **Data Layer**: Encryption at rest, secure backups

### Sandbox Security

- **Process Isolation**: Code runs in separate subprocesses
- **Resource Limits**: CPU, memory, and time limits
- **File System Isolation**: Temporary directories with restricted access
- **Network Isolation**: No outbound network access from sandbox

### Authentication & Authorization

- **API Keys**: Simple API key authentication for development
- **JWT Tokens**: Token-based auth for production
- **OAuth 2.0**: Social login and enterprise SSO
- **Rate Limiting**: Per-user and per-IP rate limits

---

## Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────────┐
│         Development Machine              │
│  ┌─────────────┐  ┌─────────────┐      │
│  │  Frontend   │  │   Backend   │      │
│  │  (Port 3000)│  │ (Port 8000) │      │
│  └─────────────┘  └─────────────┘      │
│         │                │              │
│         └────────────────┘              │
│              Localhost                  │
└─────────────────────────────────────────┘
```

### Production Environment

```
                         ┌───────────┐
                         │   CDN     │
                         │ (Vercel)  │
                         └─────┬─────┘
                               │
                         ┌─────┴─────┐
                         │   Nginx   │
                         │ (Reverse  │
                         │  Proxy)   │
                         └─────┬─────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
    │ Backend │          │ Backend │          │ Backend │
    │ Instance│          │ Instance│          │ Instance│
    │  #1     │          │  #2     │          │  #3     │
    └────┬────┘          └────┬────┘          └────┬────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
               ┌────┴────┐          ┌────┴────┐
               │PostgreSQL│          │  Redis  │
               │ Primary  │          │ Cluster │
               └──────────┘          └─────────┘
```

### Docker Compose (Development)

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_DB=nexus_ai
      - POSTGRES_USER=nexus
      - POSTGRES_PASSWORD=nexus

  redis:
    image: redis:7-alpine
```

---

## Next Steps

- [Services Documentation](./SERVICES.md) - Detailed service documentation
- [Schemas Reference](./SCHEMAS.md) - Data models and schemas
- [API Documentation](./API.md) - Complete API reference
- [Best Practices](./BEST_PRACTICES.md) - Development guidelines
