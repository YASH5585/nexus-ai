# Backend Deployment Guide

## Current Status
- Frontend: https://yash5585.github.io/nexus-ai/
- Backend: Suspended on Render
- Repository: https://github.com/YASH5585/nexus-ai

## Deploy Backend on Render

1. Go to https://dashboard.render.com/
2. Click **New +** → **Web Service**
3. Connect your GitHub repo `YASH5585/nexus-ai`
4. Set **Root Directory** to `backend`
5. Set **Build Command** to `pip install -r requirements.txt`
6. Set **Start Command** to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `OPENAI_API_KEY` = your OpenAI API key
   - `FRONTEND_URL` = `https://yash5585.github.io`
   - `CORS_ORIGINS` = `https://yash5585.github.io,https://nexus-ai.vercel.app,https://*.vercel.app`
8. Click **Create Web Service**
9. Copy the new Render URL (e.g., `https://nexus-ai-backend.onrender.com`)

## Deploy Backend on Railway

1. Go to https://railway.app/
2. Click **New Project** → **Deploy from GitHub repo**
3. Select `YASH5585/nexus-ai`
4. Set **Root Directory** to `backend`
5. Add environment variables:
   - `OPENAI_API_KEY` = your OpenAI API key
   - `FRONTEND_URL` = `https://yash5585.github.io`
   - `CORS_ORIGINS` = `https://yash5585.github.io,https://nexus-ai.vercel.app,https://*.vercel.app`
6. Deploy and copy the public Railway URL

## Deploy Backend on Fly.io

1. Install Fly CLI: https://fly.io/docs/hands-on/installing/
2. Run `fly auth login`
3. Run `fly launch` in the `backend` directory
4. Set env vars and deploy

## After Backend Deployment

1. Copy your new backend URL
2. Update `frontend/lib/api.ts` line 1:
   ```typescript
   const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "YOUR_NEW_BACKEND_URL";
   ```
3. Rebuild frontend:
   ```bash
   cd frontend
   npm run build
   ```
4. Push to GitHub Pages:
   ```bash
   cd ..
   git add -A
   git commit -m "deploy: update backend URL"
   git push origin master
   ```
5. Update GitHub Pages source to `master` branch root if needed

## One-Command Deploy Script

After you have your backend URL, run:
```bash
cd C:\Users\ASUS\nexus-ai
$backendUrl = "YOUR_NEW_BACKEND_URL"
(Get-Content "frontend\lib\api.ts") -replace 'const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL \|\| "[^"]*";', "const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || `"$backendUrl`";" | Set-Content "frontend\lib\api.ts"
cd frontend; npm run build
cd ..
git add -A
git commit -m "deploy: update backend URL to $backendUrl"
git push origin master
```
