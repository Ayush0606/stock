# Quick Render Deployment Guide

## Prerequisites
- GitHub repo connected to Render
- Render account

## Deploy Backend

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +"** → **"Web Service"**
3. **Connect GitHub**
   - Select repository: `Ayush0606/stock`
   - Select branch: `main` (or your deployment branch)

4. **Configure Service**
   - **Name:** `stock-dashboard-backend`
   - **Environment:** `Python 3`
   - **Build Command:** 
     ```bash
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command:** 
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type:** Free (for testing) or Starter Pro

5. **Add Environment Variables**
   - Click "Advanced"
   - Add:
     ```
     ENVIRONMENT = production
     DATABASE_URL = sqlite:///./stock_data.db
     FRONTEND_URL = https://stock-dashboard.onrender.com
     ```

6. **Click "Create Web Service"**
7. **Wait for deployment** (2-3 min)
8. **Copy your backend URL** (e.g., `https://stock-dashboard-backend.onrender.com`)

---

## Deploy Frontend

1. **Back in Render Dashboard**
2. **Click "New +"** → **"Static Site"**
3. **Connect GitHub**
   - Select same repository
   - Select branch: `main`

4. **Configure Service**
   - **Name:** `stock-dashboard`
   - **Build Command:** 
     ```bash
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory:** `frontend/dist`

5. **Add Environment Variables**
   - **VITE_API_URL:** `https://stock-dashboard-backend.onrender.com/api`
     (Replace with your actual backend URL from step 8 above)

6. **Click "Create Static Site"**
7. **Wait for deployment** (1-2 min)

---

## After Deployment

### Test Backend
Visit: `https://stock-dashboard-backend.onrender.com/api/docs`
- You should see SwaggerUI
- Try `/api/companies` endpoint

### Test Frontend
Visit: `https://stock-dashboard.onrender.com`
- You should see the dashboard
- Try selecting a stock
- Try dark mode toggle
- Test comparisons

### Verify Database
- SQLite will auto-create on first run
- Data persists between redeploys (within same service)

---

## Common Issues & Solutions

### Frontend shows "Failed to fetch stock data"
- Check backend URL in frontend environment variables
- Verify VITE_API_URL matches your actual backend URL
- Redeploy frontend after updating

### Backend returns 404 on `/api/companies`
- Check logs: click service → "Logs" tab
- Verify `cd backend` is in build command
- Ensure only _backend_ dependencies are installed

### Logs show "ModuleNotFoundError"
- Check Python version (should be 3.10)
- Verify all dependencies in `backend/requirements.txt`
- Rebuild service

### Dark mode not persisting
- It uses localStorage, which works in production
- Check browser console for errors (F12)

---

## Upgrade to PostgreSQL (Optional - Recommended for Production)

1. Create PostgreSQL instance:
   - Render Dashboard → "New +" → "PostgreSQL"
   - Click "Create Database"
   - Copy connection string

2. Update backend environment variable:
   - Set `DATABASE_URL` = `<your-postgres-connection-string>`

3. Redeploy backend

---

## Custom Domain (Optional)

1. In Render service settings
2. Go to "Custom Domains"
3. Add your domain and follow DNS instructions

---

## Monitoring & Logs

### View Logs
- Backend: Render Dashboard → `stock-dashboard-backend` → "Logs"
- Frontend: Render Dashboard → `stock-dashboard` → "Logs"

### Metrics
- Render Dashboard shows:
  - CPU usage
  - Memory usage
  - Requests per minute

---

## Redeploy After Code Changes

1. Push changes to GitHub
2. Render automatically redeploys both services
3. Or manually redeploy:
   - Service → "Deployments" → "Trigger Deploy"

---

## Helpful Commands for Local Testing Before Deploy

```bash
# Test backend locally
cd backend
python -m uvicorn app.main:app --reload

# Test frontend locally in production mode
cd frontend
npm run build
npm run preview

# Test API endpoint
curl http://localhost:8000/api/companies
```

---

## Next Steps

- [ ] Deploy backend
- [ ] Test backend at `/api/docs`
- [ ] Deploy frontend
- [ ] Test frontend at main domain
- [ ] Share URL with others
- [ ] Monitor logs for errors
- [ ] Consider upgrading to PostgreSQL for production data

**Deployed! 🎉**
