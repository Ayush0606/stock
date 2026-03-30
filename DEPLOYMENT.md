# Stock Data Intelligence Dashboard - Deployment Configuration

This project is configured for deployment on Render.

## Prerequisites
- GitHub account with this repo connected
- Render.com account

## Deployment Steps

### Step 1: Connect GitHub to Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `https://github.com/Ayush0606/stock.git`

### Step 2: Configure Backend Service
**Service Settings:**
- Name: `stock-dashboard-backend`
- Runtime: Python 3.10
- Build Command: `cd backend && pip install -r requirements.txt`
- Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Instance Type: Free tier is OK for testing

**Environment Variables:**
```
DATABASE_URL=sqlite:///./stock_data.db
ENVIRONMENT=production
```

### Step 3: Configure Frontend Service
1. After backend deploys, create new Static Site:
2. Click "New +" → "Static Site"
3. Connect same GitHub repo
4. **Build Settings:**
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

**Environment Variables:**
```
VITE_API_URL=https://your-backend-url.onrender.com/api
```

### Step 4: Connect Services
In **backend** environment variables, add:
```
FRONTEND_URL=https://your-frontend-url.onrender.com
```

In **frontend** `.env.production`, the API URL should point to your backend service URL.

## Step-by-Step in Render UI

### Backend:
1. **New Web Service**
2. Connect repo
3. **Name:** `stock-dashboard-backend`
4. **Runtime:** Python 3.10
5. **Build Command:** 
   ```
   cd backend && pip install -r requirements.txt
   ```
6. **Start Command:** 
   ```
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
7. **Environment Variables:**
   - `DATABASE_URL` = `sqlite:///./stock_data.db`
   - `ENVIRONMENT` = `production`
8. **Deploy**

### Frontend:
1. **New Static Site**
2. Connect same repo
3. **Name:** `stock-dashboard-frontend`
4. **Build Command:** 
   ```
   cd frontend && npm install && npm run build
   ```
5. **Publish directory:** `frontend/dist`
6. **Environment Variables:**
   - Copy your backend service URL from Render
   - `VITE_API_URL` = `https://stock-dashboard-backend.onrender.com/api` (replace with your actual backend URL)
7. **Deploy**

## Expected URLs After Deployment

- **Backend API:** `https://stock-dashboard-backend.onrender.com`
- **API Docs:** `https://stock-dashboard-backend.onrender.com/api/docs`
- **Frontend Dashboard:** `https://stock-dashboard-frontend.onrender.com`

## Troubleshooting

**Backend won't start:**
- Check logs for import errors
- Ensure Python 3.10 is selected
- Verify all dependencies in requirements.txt

**Frontend build fails:**
- Clear build cache and redeploy
- Check Node version (should be 18+)
- Verify VITE_API_URL is correct

**CORS errors:**
- Update `FRONTEND_URL` in backend env vars
- Ensure backend CORS is configured correctly

**Database issues:**
- SQLite will create/persist in the service
- Data persists between redeploys within same service
- For production, consider upgrading to PostgreSQL (Render offers free tier)

## Upgrade to PostgreSQL (Optional)

For a production-ready database:
1. In Render dashboard, create new PostgreSQL instance
2. Copy connection string
3. Set `DATABASE_URL` in backend to PostgreSQL connection string
4. Redeploy backend

## Next Steps After Deployment

1. Test all endpoints: `/api/docs`
2. Click through dashboard UI
3. Try stock comparisons
4. Check dark mode toggle
5. Monitor logs for errors

Good luck! 🚀
