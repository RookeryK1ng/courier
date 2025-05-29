# Courier Email API Backend

## Deployment Instructions

This FastAPI backend is ready to deploy to Railway. Follow these steps:

### 1. Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Railway will automatically detect it's a Python project

### 2. Set Environment Variables

In Railway dashboard, go to Variables tab and add:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Custom Domain (Optional)

1. In Railway dashboard, go to Settings → Domains
2. Add a custom domain or use the Railway-provided URL

### 4. Update Frontend

Update your frontend's API_URL to point to your deployed Railway URL.

## Local Development

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /generate-emails/` - Generate personalized emails
- `POST /send-emails/` - Send emails (simulated for now)

## Files

- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment command
- `railway.json` - Railway configuration
- `runtime.txt` - Python version specification 