# Troubleshooting Guide

Common issues and solutions for Nexus AI.

## 📋 Table of Contents

- [Installation Issues](#installation-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [API Issues](#api-issues)
- [Docker Issues](#docker-issues)
- [Testing Issues](#testing-issues)
- [Performance Issues](#performance-issues)
- [Security Issues](#security-issues)

---

## Installation Issues

### Issue: `python: command not found`

**Symptoms**: Cannot run Python commands

**Solution**:
```bash
# Check if Python is installed
python --version  # Windows
python3 --version  # macOS/Linux

# Install Python 3.12+
# On macOS:
brew install python@3.12

# On Ubuntu:
sudo apt install python3.12 python3.12-venv

# On Windows:
# Download from python.org or use Chocolatey:
choco install python
```

### Issue: `npm: command not found`

**Symptoms**: Cannot run npm commands

**Solution**:
```bash
# Install Node.js 20+
# On macOS:
brew install node@20

# On Ubuntu:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# On Windows:
choco install nodejs

# Verify installation
node --version
npm --version
```

### Issue: `pip install` fails with permission errors

**Symptoms**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: `git clone` fails with SSL certificate error

**Symptoms**: `SSL certificate problem: self signed certificate`

**Solution**:
```bash
# Disable SSL verification (not recommended for production)
git config --global http.sslVerify false

# Or update certificates
git config --global http.sslCAInfo /path/to/certificate.pem
```

---

## Backend Issues

### Issue: `ModuleNotFoundError: No module named 'app'`

**Symptoms**: `ModuleNotFoundError` when starting backend

**Solution**:
```bash
# Ensure you're in the backend directory
cd backend

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run from backend directory
uvicorn app.main:app --reload
```

### Issue: `ImportError: cannot import name 'XXX'`

**Symptoms**: Import errors for existing modules

**Solution**:
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for circular imports
# Review import statements in affected files
```

### Issue: Backend starts but returns 500 errors

**Symptoms**: API returns 500 Internal Server Error

**Solution**:
```bash
# Check logs for error details
uvicorn app.main:app --reload --log-level debug

# Common causes:
# 1. Missing environment variables
cat .env  # Verify OPENAI_API_KEY is set

# 2. Database connection issues
# Check DATABASE_URL in .env

# 3. OpenAI API errors
# Verify API key is valid and has credits
```

### Issue: `OpenAI API rate limit exceeded`

**Symptoms**: `RateLimitError` from OpenAI

**Solution**:
```bash
# Wait for rate limit to reset (usually 1 minute)

# Or upgrade OpenAI plan

# Or reduce request frequency in development
```

### Issue: Tests timeout

**Symptoms**: Tests fail with `TimeoutError`

**Solution**:
```bash
# Increase timeout in .env
SANDBOX_TIMEOUT=60  # Increase from 30 to 60

# Or optimize code to run faster
# Check for infinite loops or slow operations
```

### Issue: `structlog` not found

**Symptoms**: `ModuleNotFoundError: No module named 'structlog'`

**Solution**:
```bash
# Install structlog
pip install structlog

# Or reinstall all dependencies
pip install -r requirements.txt
```

---

## Frontend Issues

### Issue: `npm install` fails

**Symptoms**: `npm ERR!` during installation

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, try with legacy peer deps
npm install --legacy-peer-deps
```

### Issue: `next dev` fails with port already in use

**Symptoms**: `Error: listen EADDRINUSE: address already in use :::3000`

**Solution**:
```bash
# Find process using port 3000
# On macOS/Linux:
lsof -ti:3000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
PORT=3001 npm run dev
```

### Issue: Hydration errors in browser console

**Symptoms**: `Hydration failed because the initial UI does not match`

**Solution**:
```typescript
// Ensure server and client render the same content
// Use useEffect for client-only code
useEffect(() => {
  // Client-only code here
}, []);

// Or use dynamic import with ssr: false
const Component = dynamic(() => import('./Component'), { ssr: false });
```

### Issue: `NEXT_PUBLIC_API_URL` not working

**Symptoms**: Frontend cannot connect to backend

**Solution**:
```bash
# Check .env.local file exists
cat frontend/.env.local

# Verify API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Restart dev server after changing .env.local
npm run dev
```

### Issue: Three.js performance issues

**Symptoms**: Low FPS, laggy 3D background

**Solution**:
```typescript
// Reduce particle count
const PARTICLE_COUNT = 500  // Instead of 2000

// Use simpler materials
const material = new THREE.PointsMaterial({
  size: 0.05,
  sizeAttenuation: true
});

// Disable shadows
renderer.shadowMap.enabled = false;
```

---

## API Issues

### Issue: `CORS error` in browser console

**Symptoms**: `Access to fetch at 'http://localhost:8000' has been blocked by CORS policy`

**Solution**:
```bash
# Check CORS configuration in backend .env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Verify backend is running
curl http://localhost:8000/health

# Check frontend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Issue: `401 Unauthorized`

**Symptoms**: API returns 401 Unauthorized

**Solution**:
```bash
# Ensure API key is included in request
curl -H "X-API-Key: your-api-key" http://localhost:8000/generate

# Or disable auth in development
# Set in .env:
REQUIRE_AUTH=false
```

### Issue: `422 Validation Error`

**Symptoms**: API returns 422 for seemingly valid requests

**Solution**:
```bash
# Check request body format
# Ensure all required fields are present
# Check field types match schema

# Example valid request:
{
  "prompt": "Write a function",
  "language": "python"
}

# Example invalid request:
{
  "prompt": "",  # Empty string not allowed
  "language": "python"
}
```

### Issue: `429 Rate Limit Exceeded`

**Symptoms**: Too many requests error

**Solution**:
```bash
# Wait for rate limit to reset
# Check X-RateLimit-Reset header

# Or increase rate limits in .env
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60

# Or use API key for higher limits
curl -H "X-API-Key: your-key" http://localhost:8000/generate
```

---

## Docker Issues

### Issue: `Cannot connect to the Docker daemon`

**Symptoms**: `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`

**Solution**:
```bash
# Start Docker Desktop
# On macOS/Windows: Open Docker Desktop application

# On Linux:
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and back in
```

### Issue: `docker-compose` fails

**Symptoms**: `ERROR: Service 'backend' failed to build`

**Solution**:
```bash
# Check Dockerfile for errors
cat backend/Dockerfile

# Rebuild without cache
docker-compose build --no-cache

# Check logs
docker-compose logs backend

# Common issues:
# - Missing .env file
# - Incorrect file paths
# - Port conflicts
```

### Issue: Container exits immediately

**Symptoms**: Container starts then stops

**Solution**:
```bash
# Check container logs
docker logs <container-id>

# Common causes:
# 1. Missing environment variables
# 2. Command syntax error
# 3. Port already in use

# Run container interactively to debug
docker run -it <image> /bin/bash
```

---

## Testing Issues

### Issue: `pytest` not found

**Symptoms**: `command not found: pytest`

**Solution**:
```bash
# Install pytest
pip install pytest pytest-asyncio

# Or use virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Tests fail with `ModuleNotFoundError`

**Symptoms**: Tests cannot import project modules

**Solution**:
```bash
# Run tests from backend directory
cd backend
pytest tests/

# Or add backend to PYTHONPATH
export PYTHONPATH=/path/to/nexus-ai/backend:$PYTHONPATH
pytest tests/
```

### Issue: Tests hang or timeout

**Symptoms**: Tests take too long or hang indefinitely

**Solution**:
```bash
# Increase test timeout
pytest tests/ --timeout=60

# Check for infinite loops in code
# Review async/await usage
# Ensure proper cleanup in fixtures
```

### Issue: `SQLAlchemy` errors in tests

**Symptoms**: Database connection errors during tests

**Solution**:
```bash
# Use test database
export DATABASE_URL=sqlite:///./test.db

# Or mock database in tests
# Use pytest fixtures for database setup/teardown
```

---

## Performance Issues

### Issue: High memory usage

**Symptoms**: Process uses too much RAM

**Solution**:
```bash
# Check memory usage
# On macOS:
ps aux | grep python

# On Linux:
top -p <pid>

# Reduce worker count
uvicorn app.main:app --workers 2

# Optimize code
# - Use generators instead of lists
# - Close file handles
# - Clear caches regularly
```

### Issue: Slow API responses

**Symptoms**: API takes too long to respond

**Solution**:
```bash
# Check OpenAI API latency
# Consider using faster model or caching responses

# Optimize database queries
# Add indexes to frequently queried fields

# Use connection pooling
# Enable Redis caching

# Profile code
python -m cProfile -o profile.stats app/main.py
```

### Issue: Frontend is slow

**Symptoms**: UI lags, slow page loads

**Solution**:
```bash
# Analyze bundle size
npm run build
npm run analyze

# Optimize images
# Use next/image for automatic optimization

# Reduce component re-renders
# Use React.memo, useMemo, useCallback

# Code splitting
const HeavyComponent = dynamic(() => import('./HeavyComponent'));
```

---

## Security Issues

### Issue: `SECRET_KEY` warning

**Symptoms**: Warning about weak or missing SECRET_KEY

**Solution**:
```bash
# Generate strong secret key
openssl rand -hex 32

# Add to .env
SECRET_KEY=<generated-key>

# Never commit .env to version control
```

### Issue: Code execution fails with permission errors

**Symptoms**: `PermissionError` when executing code

**Solution**:
```bash
# Check sandbox directory permissions
ls -la /tmp/

# Ensure backend has write access
sudo chown -R $USER:$USER /tmp/

# Check SELinux (Linux)
sudo setenforce 0  # Temporary
```

### Issue: `pickle` security warning

**Symptoms**: Warning about unsafe pickle usage

**Solution**:
```python
# Use JSON instead of pickle for untrusted data
import json

# If pickle is required, use restricted unpickler
import pickle

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes
        if module == "builtins" and name in {"int", "str", "list"}:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")
```

---

## Getting Help

If your issue is not listed here:

1. Search [GitHub Issues](https://github.com/yourusername/nexus-ai/issues)
2. Join our [Discord Community](https://discord.gg/nexusai)
3. Check [API Documentation](./API.md)
4. Review [Architecture](./ARCHITECTURE.md)
5. Open a new issue with:
   - Nexus AI version
   - Operating system
   - Error messages
   - Steps to reproduce

---

## Related Documentation

- [Installation Guide](./INSTALLATION.md) - Setup instructions
- [Usage Guide](./USAGE.md) - How to use Nexus AI
- [Best Practices](./BEST_PRACTICES.md) - Development guidelines
