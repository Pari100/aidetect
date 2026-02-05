# Voice Authenticator - Deployment Guide

This guide covers deploying Voice Authenticator to Vercel for production use.

## 📋 Prerequisites

- [Vercel Account](https://vercel.com/signup) (free tier available)
- [GitHub Account](https://github.com/signup) with repository
- Node.js 18+ and Python 3.10+ installed locally
- Git CLI

## 🚀 Quick Start (Vercel)

### 1. Prepare Local Build

```bash
# Option A: Linux/macOS
bash scripts/deploy-vercel.sh

# Option B: Windows PowerShell
.\scripts\deploy-vercel.ps1
```

### 2. Create GitHub Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Voice Authenticator production build"
git branch -M main
git remote add origin https://github.com/yourusername/Voice-Authenticator.git
git push -u origin main
```

### 3. Deploy to Vercel

**Option A: Using Vercel Dashboard**

1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Import Project"
3. Choose your GitHub repository
4. Click "Import"
5. Add environment variables (see step 4 below)
6. Click "Deploy"

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI
npm i -g vercel

# Link to Vercel project
vercel link

# Set environment variables (see .env.example)
vercel env add PYTHON_EXE
vercel env add VITE_API_URL

# Deploy to production
vercel --prod
```

### 4. Configure Environment Variables

In Vercel Dashboard → Project Settings → Environment Variables, add:

```
PYTHON_EXE=python3
VITE_API_URL=/api
NODE_ENV=production
```

For API authentication, generate a secure key:

```bash
node -e "console.log('sk_' + require('crypto').randomBytes(24).toString('hex'))"
```

Then add to Vercel:

```
VALID_API_KEYS=sk_xxxxxxxxxxxxx
```

### 5. Verify Deployment

After deployment completes:

```bash
# Test API endpoint
curl https://your-project.vercel.app/api/voiceDetection/detect \
  -H "x-api-key: sk_test_123456789" \
  -X POST

# Visit dashboard
https://your-project.vercel.app
```

## 📦 Build Configuration

The project uses `vercel.json` for deployment configuration:

- **Framework**: Other (custom Node.js + Vite)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Node Version**: 18.x

## 🔐 Security Considerations

1. **API Keys**: Use strong, randomly generated keys
2. **Environment Variables**: Never commit `.env` files
3. **HTTPS**: Vercel provides automatic SSL/TLS
4. **Rate Limiting**: Implement rate limiting for production
5. **Database**: SQLite included; consider PostgreSQL for scaling

## 📊 Performance Tips

1. **Cold Start**: Python initialization may take 1-2 seconds on first request
2. **Memory**: Allocate 1GB+ for audio processing
3. **Timeout**: Set function timeout to 60+ seconds for large files
4. **Caching**: Frontend assets are automatically cached by Vercel

## 🔄 Updating Your Deployment

To deploy updates:

```bash
git add .
git commit -m "Update: [your changes]"
git push origin main
# Vercel automatically redeploys on push
```

Or manually with Vercel CLI:

```bash
vercel --prod
```

## 📞 Troubleshooting

### "Module not found" errors

Ensure all Python dependencies are in `requirements.txt` and installed:

```bash
pip freeze > requirements.txt
vercel env add PYTHON_EXE python3
```

### Cold start taking too long

- Increase function memory allocation
- Consider caching frequently used models
- Use asynchronous processing for heavy workloads

### Database issues

SQLite is included by default. For scaling, migrate to PostgreSQL:

1. Create PostgreSQL database (AWS RDS, Railway, etc.)
2. Update `DATABASE_URL` environment variable
3. Run migrations

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Node.js Runtime](https://vercel.com/docs/runtimes/nodejs)
- [Python on Vercel](https://vercel.com/docs/runtimes/python)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)

## 🎯 Production Checklist

- [ ] All environment variables set in Vercel
- [ ] Database tables created and initialized
- [ ] API keys configured
- [ ] CORS origins configured correctly
- [ ] Testing API endpoints working
- [ ] Monitoring/logging enabled
- [ ] Backup strategy in place
- [ ] Domain configured (optional)
- [ ] SSL certificate active (automatic with Vercel)

## 📝 Support

For issues or questions:

1. Check [GitHub Issues](https://github.com/yourusername/Voice-Authenticator/issues)
2. Review [Vercel Status](https://www.vercelstatus.com/)
3. Contact support on your platform
