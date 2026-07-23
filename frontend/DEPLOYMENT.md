# Nexus AI Frontend

Next.js 16 frontend for the Nexus AI autonomous self-healing software engineer.

## 🚀 Deployment to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier at [vercel.com](https://vercel.com))
- OpenAI API key

### Quick Deploy

1. **Connect GitHub**
   - Push your code to a GitHub repository
   - Log into [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"

2. **Import Project**
   - Select your GitHub repository
   - Framework: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Environment Variables**
   
   Add in Vercel → Settings → Environment Variables:
   
   | Variable | Value |
   |----------|-------|
   | `OPENAI_API_KEY` | Your OpenAI API key |
   | `FRONTEND_URL` | `https://your-project.vercel.app` |
   | `BACKEND_URL` | (Set after backend deployment) |

4. **Deploy**
   - Click "Deploy"
   - Vercel automatically builds and deploys
   - Your app is available at the Vercel URL

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |
| `BACKEND_URL` | Backend API URL | `http://localhost:8000` |

## 🛠️ Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run linter
npm run lint

# Run build
npm run build
```

## 📁 Folder Structure

```
frontend/
├── app/                 # App router (pages, layouts)
│   ├── page.tsx         # Main landing page
│   ├── dashboard/       # Agent interaction dashboard
│   └── ...              # Other pages
├── components/          # Reusable UI components
│   ├── landing/         # Landing page sections
│   ├── dashboard/       # Dashboard components
│   ├── ui/              # Base UI primitives
│   └── three-background/ # 3D particle background
├── lib/                 # Utilities
├── public/              # Static assets
└── styles/              # Global styles
```

## 🔧 Configuration

- `next.config.ts` - Next.js configuration
- `tailwind.config.ts` - Tailwind CSS configuration
- `tsconfig.json` - TypeScript configuration
- `package.json` - Node.js dependencies

## 📊 Monitoring

- Vercel Analytics (built-in)
- Check `/health` endpoint on backend for API health
- Monitor Vercel deployment logs

## 🚨 Troubleshooting

### Build Failures
- Clear cache: Vercel → Project → Settings → Git → Clear Build Cache
- Check build logs in Vercel dashboard

### CORS Errors
- Ensure `BACKEND_URL` is set correctly in Vercel
- Check backend CORS configuration

### API Connection Issues
- Verify `BACKEND_URL` points to correct Render URL
- Test backend directly: `curl https://your-backend.onrender.com/health`