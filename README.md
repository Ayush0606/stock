# 📈 Stock Data Intelligence Dashboard

A complete mini financial data platform built with Python/FastAPI and React, providing real-time stock analysis, data visualization, and ML-powered price predictions.

## 🎯 Features

### Core Features
- ✅ **Real-time Stock Data**: Fetch data from yfinance for Indian stocks (INFY, TCS, RELIANCE)
- ✅ **Data Storage**: SQLite database with SQLAlchemy ORM
- ✅ **REST API**: FastAPI with Swagger documentation
- ✅ **Data Processing**: Pandas/NumPy for advanced analytics
- ✅ **Calculated Metrics**:
  - Daily Returns
  - 7-day Moving Average
  - 30-day Volatility
  - 52-week High/Low
  - Price Correlation

### Advanced Features
- ✅ **ML Predictions**: Linear regression for next-day price prediction
- ✅ **Stock Comparison**: Compare returns and correlation between two stocks
- ✅ **Interactive Dashboard**: React frontend with Chart.js visualizations
- ✅ **API Caching**: Optimized data retrieval
- ✅ **Async Operations**: Non-blocking API calls
- ✅ **Docker Support**: Easy deployment with Docker & Docker Compose

## 🏗️ Architecture

```
Stock Data Intelligence Dashboard
├── Backend (FastAPI)
│   ├── Data Collection (yfinance)
│   ├── Data Processing (Pandas/NumPy)
│   ├── Database (SQLAlchemy + SQLite)
│   ├── REST APIs (FastAPI)
│   └── ML Models (scikit-learn)
│
└── Frontend (React)
    ├── Component Library
    ├── Chart Visualizations (Chart.js)
    ├── API Integration (Axios)
    └── Responsive UI (CSS)
```

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── schemas.py              # Pydantic models
│   │   ├── models/
│   │   │   └── stock.py            # Database models
│   │   ├── routes/
│   │   │   └── stocks.py           # API endpoints
│   │   ├── services/
│   │   │   └── stock_service.py    # Business logic
│   │   └── utils/
│   │       ├── data_processor.py   # Data processing
│   │       └── ml_predictor.py     # ML predictions
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx                # React entry point
│   │   ├── App.jsx                 # Main component
│   │   ├── index.css               # Global styles
│   │   └── components/
│   │       ├── Dashboard.jsx       # Main dashboard  
│   │       ├── Sidebar.jsx         # Company list
│   │       ├── StockChart.jsx      # Price chart
│   │       ├── StockSummary.jsx    # Summary stats
│   │       ├── Comparison.jsx      # Compare stocks
│   │       └── Prediction.jsx      # Price prediction
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── init_data.py                    # Initialize database with data
├── Dockerfile                      # Docker image for backend
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This file
└── .gitignore
```

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone/Extract the project
cd Stock

# Build and run everything
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with stock data
cd ..
python init_data.py

# Run the backend server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Interactive API Docs
```
http://localhost:8000/api/docs
```

### Endpoints

#### 1. Get Available Companies
```
GET /api/companies

Response:
[
    {
        "symbol": "INFY.NS",
        "name": "Infosys",
        "data_points": 252
    },
    ...
]
```

#### 2. Get Stock Data
```
GET /api/data/{symbol}?days=30

Parameters:
  - symbol: Stock symbol (e.g., "INFY.NS")
  - days: Number of days to fetch (1-365, default 30)

Response:
[
    {
        "id": 1,
        "symbol": "INFY.NS",
        "date": "2024-01-01T00:00:00",
        "open_price": 1500.50,
        "close_price": 1550.75,
        "high_price": 1560.00,
        "low_price": 1490.25,
        "volume": 5000000,
        "daily_return": 3.35,
        "moving_avg_7": 1520.43,
        "volatility_30": 2.15,
        "created_at": "2024-03-30T10:00:00"
    },
    ...
]
```

#### 3. Get Stock Summary
```
GET /api/summary/{symbol}

Response:
{
    "symbol": "INFY.NS",
    "current_price": 1550.75,
    "high_52_week": 1800.00,
    "low_52_week": 1200.00,
    "average_close": 1450.25,
    "volatility": 25.5,
    "last_updated": "2024-03-30T00:00:00"
}
```

#### 4. Compare Two Stocks
```
GET /api/compare?symbol1=INFY.NS&symbol2=TCS.NS

Response:
{
    "symbol1": "INFY.NS",
    "symbol2": "TCS.NS",
    "symbol1_returns": 8.5,
    "symbol2_returns": 12.3,
    "correlation": 0.85,
    "better_performer": "TCS.NS",
    "data_points": 250
}
```

#### 5. Predict Next Day Price
```
GET /api/predict/{symbol}

Response:
{
    "symbol": "INFY.NS",
    "next_day_prediction": 1560.50,
    "confidence": 0.82,
    "trend": "UP",
    "base_price": 1550.75
}
```

#### 6. Refresh Stock Data
```
POST /api/refresh/{symbol}

Response:
{
    "symbol": "INFY.NS",
    "records_updated": 252,
    "status": "success"
}
```

## 📊 Data Processing Pipeline

### 1. Data Fetching
```python
DataProcessor.fetch_stock_data(symbol, period="1y")
# Fetches OHLCV data using yfinance
```

### 2. Data Cleaning
```python
DataProcessor.clean_data(df)
# - Handle missing values
# - Convert date columns
# - Ensure numeric types
# - Remove outliers
```

### 3. Metric Calculation
```python
# Daily Returns
df['daily_return'] = ((df['close'] - df['open']) / df['open']) * 100

# 7-day Moving Average
df['moving_avg_7'] = df['close'].rolling(window=7).mean()

# 30-day Volatility
df['volatility_30'] = df['daily_return'].rolling(window=30).std()
```

### 4. ML Prediction
```python
MLPredictor.predict_next_day(df, lookback=30)
# Uses linear regression on last 30 days to predict closing price
```

## 🗄️ Database Schema

### StockData Table
```sql
CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATETIME NOT NULL,
    open_price FLOAT NOT NULL,
    close_price FLOAT NOT NULL,
    high_price FLOAT NOT NULL,
    low_price FLOAT NOT NULL,
    volume BIGINT DEFAULT 0,
    daily_return FLOAT,
    moving_avg_7 FLOAT,
    volatility_30 FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_symbol_date ON stock_data(symbol, date);
CREATE INDEX idx_symbol ON stock_data(symbol);
CREATE INDEX idx_date ON stock_data(date);
```

## 🎨 Frontend Features

### Dashboard Components
- **Sidebar**: List of available companies with search
- **Stock Chart**: Interactive line chart with moving averages
- **Summary Stats**: Key metrics (52-week high/low, volatility, etc.)
- **Comparison Tab**: Compare two stocks side-by-side
- **Prediction Tab**: ML-powered price predictions
- **Responsive Design**: Mobile-friendly UI

### Charts & Visualizations
- Chart.js for interactive line charts
- Real-time data updates
- Multiple date range filters (30/90/180 days, 1 year)

## 🔧 Technologies Used

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **Database**: SQLite + SQLAlchemy ORM
- **Data Processing**: Pandas, NumPy
- **Stock Data**: yfinance
- **ML**: scikit-learn (Linear Regression)
- **Validation**: Pydantic
- **API Docs**: Swagger/OpenAPI

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite
- **Charts**: Chart.js + react-chartjs-2
- **HTTP Client**: Axios
- **Styling**: CSS3
- **Date Handling**: date-fns

## 📈 Sample Metrics

### Daily Return
Calculate percentage change from opening to closing price:
```
Daily Return = (Close - Open) / Open * 100
```

### Moving Average
7-day moving average of closing prices smooths trends:
```
MA7 = Average(Close[t-6] to Close[t])
```

### Volatility
30-day standard deviation of daily returns measures risk:
```
Volatility = StdDev(Daily Returns[last 30 days])
```

### Correlation
Pearson correlation between two stocks' closing prices:
```
Correlation = Cov(Stock1, Stock2) / (σ1 * σ2)
```

## 🚢 Deployment

### Using Docker
```bash
# Build Docker image
docker build -t stock-dashboard .

# Run container
docker run -p 8000:8000 stock-dashboard
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Variables
Create `.env` file in the root directory:
```
DATABASE_URL=sqlite:///./stock_data.db
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

## 🔐 Error Handling

All endpoints include proper error handling:
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (symbol not found)
- **500**: Internal Server Error

Example error response:
```json
{
    "detail": "No data available for symbol: UNKNOWN.NS"
}
```

## 📝 Code Quality

- ✅ Modular, clean, readable code
- ✅ Comprehensive comments and docstrings
- ✅ Type hints throughout
- ✅ Following PEP 8 standards
- ✅ Proper error handling
- ✅ Logging at appropriate levels

## 🧪 Testing

### Test the Backend API
```bash
# Using curl
curl http://localhost:8000/api/health

# Using Python requests
import requests
response = requests.get('http://localhost:8000/api/companies')
print(response.json())
```

### Test the Frontend
- Open http://localhost:3000
- Select a company from sidebar
- View charts and metrics
- Try comparisons and predictions

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in code or:
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Database Issues
```bash
# Reset database
rm stock_data.db
python init_data.py
```

### Frontend Not Connecting to Backend
- Ensure backend is running on http://localhost:8000
- Check Vite proxy settings in vite.config.js
- Open browser dev tools to see network requests

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/)
- [React Documentation](https://react.dev/)
- [Chart.js Guide](https://www.chartjs.org/)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Contributing

Feel free to fork, modify, and improve this project!

### Future Enhancements
- [ ] WebSocket support for real-time updates
- [ ] Advanced ML models (LSTM, XGBoost)
- [ ] Portfolio management
- [ ] Alert system
- [ ] User authentication
- [ ] Advanced charting with Plotly
- [ ] Email notifications
- [ ] Mobile app (React Native)

## 📞 Support

For issues, questions, or suggestions, please reach out or open an issue in the repository.

---

**Built with ❤️ for financial data analysis and learning**
