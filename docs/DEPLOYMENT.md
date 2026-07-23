# Nexus AI Deployment Guide

This guide will help you deploy Nexus AI for free using Vercel (frontend) and Render (backend).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Backend Deployment (Render)](#backend-deployment-render)
4. [Connecting Frontend and Backend](#connecting-frontend-and-backend)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- [GitHub account](https://github.com)
- [Vercel account](https://vercel.com) (free tier)
- [Render account](https://render.com) (free tier)
- [OpenAI API key](https://platform.openai.com/api-keys)

---

## Frontend Deployment (Vercel)

### Step 1: Connect GitHub

1. Push your code to a GitHub repository
2. Log into [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"

### Step 2: Import Project

1. Select your GitHub repository
2. Configure the project:

| Setting | Value |
|---------|-------|
| **Framework Preset** | Next.js |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `.next` |

### Step 3: Configure Environment Variables

Add these environment variables in Vercel → Settings → Environment Variables:

| Variable | Value | Type |
|----------|-------|------|
| `OPENAI_API_KEY` | Your OpenAI API key | Plain Text |
| `FRONTEND_URL` | `https://your-project.vercel.app` | Plain Text |
| `BACKEND_URL` | (Set after backend deployment) | Plain Text |

### Step 4: Deploy

1. Click "Deploy"
2. Vercel will build and deploy your frontend
3. Note the URL provided (e.g., `https://nexus-ai.vercel.app`)

---

## Backend Deployment (Render)

### Step 1: Create Web Service

1. Log into [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"

### Step 2: Configure Service

| Setting | Value |
|---------|-------|
| **Name** | `nexus-ai-backend` |
| **Region** | Auto |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Environment** | Python 3.11 |

### Step 3: Configure Environment Variables

Add these environment variables in Render → Environment:

| Variable | Value | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key | API key for OpenAI |
| `OPENAI_MODEL` | `gpt-4o` | Model to use |
| `DEBUG` | `false` | Disable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `FRONTEND_URL` | Vercel URL | For CORS configuration |
| `BACKEND_URL` | Render URL | Will be auto-generated |

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will build and deploy your backend
3. Note the URL provided (e.g., `https://nexus-ai-backend.onrender.com`)

---

## Connecting Frontend and Backend

### Update Frontend with Backend URL

1. Go to Vercel → Your Project → Settings → Environment Variables
2. Set `BACKEND_URL` to your Render URL
3. Redeploy your frontend

### Update Backend with Frontend URL

1. Go to Render → Your Service → Environment
2. Set `FRONTEND_URL` to your Vercel URL
3. The changes will apply automatically

### Test the Connection

1. Visit your Vercel URL
2. Try a simple code generation prompt
3. Check that the frontend can communicate with the backend

---

## Troubleshooting

### Frontend Build Errors

**Problem**: Build fails with "Module not found" errors

**Solution**: 
1. Check that `frontend/package.json` has correct dependencies
2. Clear Vercel cache: Vercel → Project → Settings → Git → Clear Build Cache

### Backend Build Errors

**Problem**: Build fails with pip install errors

**Solution**:
1. Check `requirements.txt` for correct package versions
2. Review Render build logs for specific errors

### CORS Errors

**Problem**: Frontend cannot access backend API

**Solution**:
1. Verify `FRONTEND_URL` is set correctly in Render
2. Check backend CORS middleware configuration in `app/main.py`

### API Key Errors

**Problem**: OpenAI API errors

**Solution**:
1. Verify `OPENAI_API_KEY` is set in both Vercel and Render
2. Check that the API key is valid at [platform.openai.com](https://platform.openai.com)

### Health Check Fails

**Problem**: Backend shows as unhealthy

**Solution**:
1. Check Render service logs
2. Verify `/health` endpoint is accessible
3. Check that `uvicorn` is running correctly

---

## Production Best Practices

1. **Environment Variables**: Never commit `.env` files to version control
2. **HTTPS**: Both Vercel and Render provide HTTPS by default
3. **Monitoring**: Use the health endpoint `/health` for monitoring
4. **Logging**: Check Render logs for debugging
5. **Scaling**: Free tiers have usage limits; upgrade if needed

---

## Cost Summary (Free Tier)

| Service | Free Tier |
|---------|-----------|
| Vercel | 100 GB bandwidth, 1000 hours/month |
| Render | 750 hours/month, 512 MB RAM |
| OpenAI | Pay-as-you-go (check pricing at openai.com) |

Both Vercel and Render offer generous free tiers that should be sufficient for development and small-scale production use.