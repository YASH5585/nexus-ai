# Installation Guide

This guide provides detailed instructions for installing and setting up Nexus AI on your local machine or production environment.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Docker Setup](#docker-setup)
- [Production Deployment](#production-deployment)
- [Environment Variables](#environment-variables)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Recommended | Purpose |
|----------|----------------|-------------|---------|
| Node.js | 20.0.0 | 22.x LTS | Frontend runtime |
| Python | 3.12.0 | 3.12.x | Backend runtime |
| Docker | 24.0.0 | 24.x | Containerization |
| Git | 2.40.0 | Latest | Version control |
| OpenAI API Key | - | GPT-4o | AI model access |

### Optional Software

- **PostgreSQL** 16+ - For production database
- **Redis** 7+ - For caching and session storage
- **Nginx** - For reverse proxy and load balancing
- **Prometheus + Grafana** - For monitoring and observability

### System Requirements

#### Minimum (Development)
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 20 GB free space
- **OS**: Windows 10+, macOS 13+, or Ubuntu 20.04+

#### Recommended (Production)
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 50+ GB SSD
- **OS**: Ubuntu 22.04 LTS or Docker-supported OS

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/nexus-ai.git
cd nexus-ai
```

### Step 2: Install System Dependencies

#### On macOS (using Homebrew)
```bash
brew install node@20 python@3.12 docker git
```

#### On Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y nodejs npm python3.12 python3.12-venv docker.io git
```

#### On Windows (using Chocolatey)
```bash
choco install nodejs python docker-desktop git
```

### Step 3: Verify Installations

```bash
# Verify Node.js
node --version  # Should be >= 20.0.0
npm --version   # Should be >= 10.0.0

# Verify Python
python3 --version  # Should be >= 3.12.0
pip3 --version     # Should be >= 24.0.0

# Verify Docker
docker --version   # Should be >= 24.0.0
docker-compose --version  # Should be >= 2.0.0

# Verify Git
git --version      # Should be >= 2.40.0
```

---

## Backend Setup

### Step 1: Create Python Virtual Environment

```bash
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 2: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Install Development Dependencies (Optional)

```bash
pip install -r requirements-dev.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

### Step 5: Run Database Migrations (if using PostgreSQL)

```bash
# Install Alembic for migrations
pip install alembic

# Initialize database
alembic upgrade head
```

### Step 6: Start Backend Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Step 7: Verify Backend

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"nexus-ai"}
```

---

## Frontend Setup

### Step 1: Install Node.js Dependencies

```bash
cd frontend
npm install
```

### Step 2: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local with your settings
nano .env.local
```

### Step 3: Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Step 4: Verify Frontend

Open your browser and navigate to `http://localhost:3000`. You should see the Nexus AI landing page with a 3D particle background.

---

## Docker Setup

### Option 1: Using Docker Compose (Recommended)

```bash
# Start all services (frontend, backend, database, redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Option 2: Using Docker CLI

```bash
# Build backend image
docker build -t nexus-ai-backend ./backend

# Build frontend image
docker build -t nexus-ai-frontend ./frontend

# Run backend
docker run -p 8000:8000 --env-file .env nexus-ai-backend

# Run frontend
docker run -p 3000:3000 nexus-ai-frontend
```

### Docker Services

The `docker-compose.yml` includes:
- **nexus-ai-backend** - FastAPI backend
- **nexus-ai-frontend** - Next.js frontend
- **postgres** - PostgreSQL database
- **redis** - Redis cache
- **prometheus** - Metrics collection
- **grafana** - Monitoring dashboard

---

## Production Deployment

### Option 1: Railway Deployment

Nexus AI includes a `railway.toml` for easy deployment to Railway:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Option 2: Vercel + Railway

Deploy frontend to Vercel and backend to Railway:

```bash
# Deploy frontend to Vercel
cd frontend
vercel --prod

# Deploy backend to Railway
cd backend
railway up
```

### Option 3: AWS/GCP/Azure

Use the provided Terraform configurations (if available):

```bash
# Initialize Terraform
cd infra/terraform
terraform init

# Plan deployment
terraform plan

# Apply deployment
terraform apply
```

### Production Checklist

- [ ] Set `ENVIRONMENT=production` in environment variables
- [ ] Configure strong `SECRET_KEY` for session encryption
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Set up PostgreSQL with connection pooling
- [ ] Configure Redis for caching
- [ ] Set up Prometheus + Grafana for monitoring
- [ ] Configure log aggregation (ELK stack or similar)
- [ ] Set up automated backups
- [ ] Configure CDN for frontend assets
- [ ] Enable rate limiting
- [ ] Set up health checks and alerts

---

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o
OPENAI_ORG_ID=org-your-org-id  # Optional
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional, for custom endpoints

# Application Configuration
APP_NAME=Nexus AI Backend
APP_VERSION=0.1.0
ENVIRONMENT=development  # development, staging, production
DEBUG=true  # Set to false in production
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4  # Number of worker processes (production)

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/nexus_ai
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=  # Optional

# Sandbox Configuration
SANDBOX_TIMEOUT=30  # Maximum execution time in seconds
SANDBOX_MEMORY_LIMIT=512  # Memory limit in MB
SANDBOX_CPU_LIMIT=1.0  # CPU limit in cores

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
ALLOWED_HOSTS=localhost,127.0.0.1
RATE_LIMIT_REQUESTS=100  # Requests per minute
RATE_LIMIT_WINDOW=60  # Window in seconds

# Feature Flags
ENABLE_AGENT=true
ENABLE_SELF_HEALING=true
ENABLE_CODE_REVIEW=true
ENABLE_SECURITY_SCAN=true
ENABLE_PERFORMANCE_ANALYSIS=true

# Monitoring
SENTRY_DSN=  # Optional, for error tracking
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Application Configuration
NEXT_PUBLIC_APP_NAME=Nexus AI
NEXT_PUBLIC_APP_VERSION=0.1.0
NEXT_PUBLIC_ENVIRONMENT=development  # development, staging, production

# Feature Flags
NEXT_PUBLIC_ENABLE_3D_BACKGROUND=true
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG_MODE=true

# Third-party Services
NEXT_PUBLIC_GA_TRACKING_ID=  # Google Analytics
NEXT_PUBLIC_SENTRY_DSN=  # Sentry error tracking
```

---

## Verification

### Verify Backend Installation

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs  # OpenAPI documentation
```

### Verify Frontend Installation

```bash
# Start frontend
cd frontend
npm run dev

# Open browser
# Navigate to http://localhost:3000
```

### Run Test Suite

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# Run all tests
npm test
```

### Verify Docker Setup

```bash
# Start services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure you're running from the `backend/` directory and the virtual environment is activated.

```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn app.main:app --reload
```

#### Issue: `Permission denied` when running Docker

**Solution**: Add your user to the Docker group or use `sudo`.

```bash
# On Linux
sudo usermod -aG docker $USER
# Log out and back in
```

#### Issue: `npm install` fails with permission errors

**Solution**: Fix npm permissions or use a version manager.

```bash
# On macOS/Linux
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Or use nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

#### Issue: Backend starts but frontend can't connect

**Solution**: Check CORS configuration and API URL.

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Check backend CORS settings in .env
CORS_ORIGINS=http://localhost:3000
```

#### Issue: `OpenAI API key invalid`

**Solution**: Verify your API key is correctly set in `.env`.

```bash
# Check backend .env
OPENAI_API_KEY=sk-your-actual-api-key-here

# Restart backend after changing .env
uvicorn app.main:app --reload
```

#### Issue: Tests fail with `TimeoutError`

**Solution**: Increase sandbox timeout in `.env`.

```env
SANDBOX_TIMEOUT=60  # Increase from 30 to 60 seconds
```

---

## Next Steps

After installation, check out:

- [Usage Guide](./USAGE.md) - Learn how to use Nexus AI
- [API Documentation](./API.md) - Explore available endpoints
- [Best Practices](./BEST_PRACTICES.md) - Learn development guidelines
- [Architecture](./ARCHITECTURE.md) - Understand system design

---

## Getting Help

If you encounter issues not covered here:

1. Check [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/yourusername/nexus-ai/issues)
3. Join our [Discord Community](https://discord.gg/nexusai)
4. Open a new issue with details about your problem
