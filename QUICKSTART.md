# Stock Data Intelligence Dashboard - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- Node.js 16+
- pip and npm

### Step 1: Clone/Extract Project
```bash
cd Stock
```

### Step 2: Start Backend (Terminal 1)
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install and run
pip install -r requirements.txt
cd ..
python init_data.py
cd backend
python -m uvicorn app.main:app --reload
```

### Step 3: Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### Step 4: Open Browser
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/docs

---

## 📋 What You'll See

1. **Sidebar with Companies**: INFY, TCS, RELIANCE
2. **Main Dashboard**:
   - Stock price chart with moving averages
   - Summary statistics (high/low, volatility)
   - Comparison tool
   - Price predictions

3. **API Documentation**: Full interactive API docs

---

## 🔧 Common Commands

### Backend
```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_data.py

# Run backend
python -m uvicorn app.main:app --reload

# Run from backend directory
cd backend && python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🗄️ Database

First time setup automatically creates:
- Database file: `stock_data.db`
- 3 Tables with 1 year of data
- ~252 records per stock

Reset database:
```bash
# Delete the database file and run init again
rm stock_data.db  # or del stock_data.db on Windows
python init_data.py
```

---

## 📊 Features

### Dashboard Tabs

1. **Overview** 📈
   - Interactive price chart
   - Moving averages
   - Summary statistics
   - Date range filters

2. **Compare** 🔄
   - Compare two stocks
   - View correlation
   - See total returns
   - Find better performer

3. **Predict** 🎯
   - Next day price prediction
   - Confidence level
   - Trend indicator
   - ML-powered (Linear Regression)

---

## 🔗 API Highlights

| Endpoint | Purpose |
|----------|---------|
| `/api/companies` | List available stocks |
| `/api/data/{symbol}` | Get stock data (30/90/180/365 days) |
| `/api/summary/{symbol}` | Key statistics |
| `/api/compare` | Compare two stocks |
| `/api/predict/{symbol}` | Next day prediction |
| `/api/docs` | Interactive API documentation |

---

## 🎨 Customization

### Add More Stocks

Edit `backend/app/utils/data_processor.py`:

```python
STOCK_SYMBOLS = ["INFY.NS", "TCS.NS", "RELIANCE.NS", "ITC.NS"]  # Add more
STOCK_NAMES = {
    "INFY.NS": "Infosys",
    # ... add names
}
```

Then refresh:
```bash
python init_data.py
```

### Change Color Scheme

Edit `frontend/src/App.css` and component CSS files:

```css
--primary: #667eea;  /* Change gradient colors */
--secondary: #764ba2;
```

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### "Module not found" error
```bash
# Make sure venv is activated
# Check you're in the backend directory
cd backend && python -m uvicorn app.main:app --reload
```

### No data showing
```bash
python init_data.py  # Re-initialize database
```

---

## 📚 Next Steps

1. **Explore the API**: Visit http://localhost:8000/api/docs
2. **Test Endpoints**: Use the Swagger UI to test
3. **Customize**: Add more stocks or features
4. **Deploy**: Use Docker or cloud services
5. **Learn**: Study the code structure

---

## 🚢 Docker Option (Easiest)

```bash
# One command to run everything
docker-compose up

# Access at:
# Frontend: http://localhost:3000
# API: http://localhost:8000/api
# Docs: http://localhost:8000/api/docs
```

---

## 📖 Full Documentation

- `README.md` - Complete documentation
- `SETUP.md` - Detailed setup instructions
- `API_EXAMPLES.md` - API response examples
- `test_api.py` - API testing script

---

## 💡 Tips

1. **Hot Reload**: Both backend and frontend auto-reload on file changes
2. **API Testing**: Use Swagger UI at `/api/docs`
3. **Browser DevTools**: Check Network tab for API calls
4. **Database**: SQLRite file is `stock_data.db` in backend folder
5. **Logs**: Check terminal output for debugging

---

## 🎯 Next Projects

- Add PostgreSQL for production
- Deploy to Heroku/AWS
- Add user authentication
- Build mobile app
- Add more ML models
- Real-time WebSocket updates

---

**You're all set! Happy coding! 🚀**
