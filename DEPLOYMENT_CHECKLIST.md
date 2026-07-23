# Nexus AI - Production Deployment Checklist

## Pre-Deployment

- [x] Remove all localhost references from source code
- [x] Replace hardcoded URLs with environment variables
- [x] Fix CORS configuration
- [x] Update .env.example files
- [x] Create vercel.json for frontend
- [x] Create render.yaml for backend
- [x] Ensure npm run build succeeds without warnings

## Frontend Deployment (Vercel)

1. Push code to GitHub repository
2. Connect repository to Vercel
3. Set environment variables in Vercel:
   - `NEXT_PUBLIC_BACKEND_URL` = `https://nexus-ai-backend.onrender.com`
   - `NEXT_PUBLIC_FRONTEND_URL` = `https://nexus-ai.vercel.app`
   - `BACKEND_URL` = `https://nexus-ai-backend.onrender.com`
   - `FRONTEND_URL` = `https://nexus-ai.vercel.app`
4. Deploy to Vercel
5. Note the production URL (e.g., `https://nexus-ai.vercel.app`)

## Backend Deployment (Render)

1. Push code to GitHub repository
2. Connect repository to Render
3. Set environment variables in Render:
   - `OPENAI_API_KEY` = your OpenAI API key
   - `FRONTEND_URL` = `https://nexus-ai.vercel.app`
   - `BACKEND_URL` = `https://nexus-ai-backend.onrender.com`
   - `CORS_ORIGINS` = `https://nexus-ai.vercel.app,https://*.vercel.app`
4. Deploy to Render
5. Note the production URL (e.g., `https://nexus-ai-backend.onrender.com`)

## Post-Deployment

1. Update frontend environment variables with actual backend URL
2. Update backend CORS_ORIGINS with actual frontend URL
3. Test health endpoint: `https://nexus-ai-backend.onrender.com/health`
4. Test frontend: `https://nexus-ai.vercel.app`
5. Test API connectivity from frontend to backend
6. Verify CORS headers are correct

## Production URLs

- Frontend: `https://nexus-ai.vercel.app`
- Backend: `https://nexus-ai-backend.onrender.com`
- API Docs: `https://nexus-ai-backend.onrender.com/docs`

## Security

- [x] No localhost references in production code
- [x] CORS restricted to production domains
- [x] Environment variables used for all URLs
- [x] OpenAI API key in environment variables only
- [x] Debug mode disabled in production

## Notes

- The frontend uses mock data for demonstration
- The backend requires an OpenAI API key
- All URLs are configured via environment variables
- CORS origins include Vercel preview deployments (*.vercel.app)