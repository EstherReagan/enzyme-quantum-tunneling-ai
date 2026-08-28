# DEPLOYMENT GUIDE: Enzyme Quantum Tunneling AI (Premium Edition)

This guide covers deploying the complete Dash + FastAPI stack to production.

---

## **ARCHITECTURE OVERVIEW**

```
┌─────────────────┐         ┌──────────────────┐
│   Vercel        │◄────────┤     Render       │
│  (Dash App)     │         │  (FastAPI)       │
│  Frontend       │         │  Backend         │
└─────────────────┘         └──────────────────┘
```

---

## **OPTION 1: LOCAL DEVELOPMENT (Test First)**

### Step 1: Setup

```bash
# Clone your repo
git clone https://github.com/EstherReagan/enzyme-quantum-tunneling-ai.git
cd enzyme-quantum-tunneling-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_dash.txt
```

### Step 2: Run Locally

**Terminal 1 - Start Backend:**
```bash
python backend.py
# Output: Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Start Frontend:**
```bash
python app_dash.py
# Output: Running on http://127.0.0.1:8050
```

Visit: **http://localhost:8050**

---

## **OPTION 2: DEPLOY TO RENDER (Backend)**

Render is perfect for FastAPI backend (free tier + GPU available).

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up (free)
3. Connect your GitHub account

### Step 2: Create Web Service

1. Dashboard → **New +** → **Web Service**
2. Connect repository: `enzyme-quantum-tunneling-ai`
3. Fill in:
   - **Name**: `enzyme-quantum-backend`
   - **Environment**: `Python 3.11`
   - **Build Command**: `pip install -r requirements_dash.txt`
   - **Start Command**: `uvicorn backend:app --host 0.0.0.0 --port 8000`
   - **Instance Type**: `Standard`
   - **Region**: `Ohio` (or closest to you)

4. Click **Create Web Service**

### Step 3: Get Backend URL

Once deployed, you'll get a URL like:
```
https://enzyme-quantum-backend.onrender.com
```

**Note this URL** - you'll need it for the frontend.

---

## **OPTION 3: DEPLOY TO VERCEL (Frontend)**

Vercel is perfect for Dash frontend (free tier, instant deployment).

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Sign up (free, use GitHub)

### Step 2: Create Environment File

Create `.env` in your repo root:

```env
BACKEND_URL=https://enzyme-quantum-backend.onrender.com
```

Update `app_dash.py` line 20:
```python
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

### Step 3: Deploy

1. Go to https://vercel.com/dashboard
2. Click **Add New...** → **Project**
3. Select your GitHub repo
4. Environment Variables:
   - Key: `BACKEND_URL`
   - Value: `https://enzyme-quantum-backend.onrender.com`
5. **Deploy**

You'll get a live URL like:
```
https://enzyme-quantum-tunneling-ai.vercel.app
```

---

## **OPTION 4: DOCKER DEPLOYMENT (Optional)**

For advanced deployments.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_dash.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_dash.txt

# Copy code
COPY . .

# Expose ports
EXPOSE 8000 8050

# Start both services
CMD ["sh", "-c", "python backend.py & python app_dash.py"]
```

### Deploy with Docker

```bash
# Build
docker build -t enzyme-tunneling .

# Run
docker run -p 8000:8000 -p 8050:8050 enzyme-tunneling
```

---

## **COMPLETE PRODUCTION CHECKLIST**

### Before Deploying:

- [ ] Update `BACKEND_URL` in `app_dash.py` to your Render URL
- [ ] Test locally first
- [ ] Commit all changes to GitHub
- [ ] Create `.env` for production secrets
- [ ] Add requirements_dash.txt to repo

### Deployment:

- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set correctly
- [ ] CORS enabled (✅ already done in `backend.py`)
- [ ] Test full workflow on live site

### After Deploying:

- [ ] Test enzyme search works
- [ ] Test quantum calculations
- [ ] Test AI mutations
- [ ] Check performance (Vercel Analytics)
- [ ] Monitor backend logs (Render Dashboard)
- [ ] Share live URL with recruiters

---

## **TROUBLESHOOTING**

### Backend not responding

```
Error: Connection refused on BACKEND_URL
```

**Solution:**
1. Check Render dashboard - service running?
2. Verify URL in `app_dash.py`
3. Check CORS settings in `backend.py` (already enabled)

### Mutations not working

```
Error: Model loading failed
```

**Solution:**
1. Render might be downloading ESM-2 model (first run is slow)
2. Wait 5-10 minutes for model cache
3. Check Render logs: Dashboard → Service → Logs

### Slow calculations

**Solution:**
1. Upgrade Render instance (paid)
2. Enable Redis caching (advanced)
3. Optimize model loading (cache to disk)

---

## **FINAL URLS**

Once deployed, you'll have:

**Backend API:**
```
https://enzyme-quantum-backend.onrender.com
```

**Live App:**
```
https://enzyme-quantum-tunneling-ai.vercel.app
```

**Share with recruiters:** The Vercel URL (they click → instant working app)

---

## **CUSTOMIZATION**

### Add More Enzymes

Edit `backend.py` → `featured_enzymes()` function

```python
{
    "name": "Your Enzyme",
    "pdb_id": "YOUR_ID",
    "description": "...",
    "barrier_height": 0.6,
    "tunneling_width": 1.2
}
```

### Change Colors

Edit `app_dash.py` → `DARK_THEME` dict

```python
DARK_THEME = {
    "primary": "#00D9FF",  # Change this
    "accent": "#39FF14",   # Or this
    ...
}
```

### Optimize Performance

Add caching to `backend.py`:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_quantum_tunneling(...):
    # Caches results for repeated calls
```

---

## **NEXT STEPS**

1. **Local Testing** (Option 1) - Make sure it works locally first
2. **Deploy Backend** (Option 2) - Render
3. **Deploy Frontend** (Option 3) - Vercel
4. **Share with recruiters** - They can instantly see your working app

**Total time:** 30 minutes setup + 10 minutes deployment = **40 minutes to production**

---

## **SUPPORT**

- Render docs: https://render.com/docs
- Vercel docs: https://vercel.com/docs
- FastAPI docs: https://fastapi.tiangolo.com
- Dash docs: https://dash.plotly.com
