# API Example Responses

## 1. GET /api/companies

**Request:**
```
GET http://localhost:8000/api/companies
```

**Response (200 OK):**
```json
[
  {
    "symbol": "INFY.NS",
    "name": "Infosys",
    "data_points": 252
  },
  {
    "symbol": "TCS.NS",
    "name": "Tata Consultancy Services",
    "data_points": 252
  },
  {
    "symbol": "RELIANCE.NS",
    "name": "Reliance Industries",
    "data_points": 252
  }
]
```

---

## 2. GET /api/data/{symbol}?days=30

**Request:**
```
GET http://localhost:8000/api/data/INFY.NS?days=30
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "symbol": "INFY.NS",
    "date": "2023-12-01T00:00:00",
    "open_price": 1480.50,
    "close_price": 1490.75,
    "high_price": 1500.00,
    "low_price": 1475.00,
    "volume": 4250000,
    "daily_return": 0.692,
    "moving_avg_7": 1485.43,
    "volatility_30": 1.85,
    "created_at": "2024-03-29T10:30:45"
  },
  {
    "id": 2,
    "symbol": "INFY.NS",
    "date": "2023-12-02T00:00:00",
    "open_price": 1490.75,
    "close_price": 1505.25,
    "high_price": 1520.00,
    "low_price": 1485.00,
    "volume": 5120000,
    "daily_return": 0.970,
    "moving_avg_7": 1495.21,
    "volatility_30": 1.92,
    "created_at": "2024-03-29T10:30:45"
  }
]
```

---

## 3. GET /api/summary/{symbol}

**Request:**
```
GET http://localhost:8000/api/summary/INFY.NS
```

**Response (200 OK):**
```json
{
  "symbol": "INFY.NS",
  "current_price": 1550.75,
  "high_52_week": 1850.50,
  "low_52_week": 1200.25,
  "average_close": 1450.32,
  "volatility": 25.4,
  "last_updated": "2024-03-30T00:00:00"
}
```

---

## 4. GET /api/compare?symbol1=INFY.NS&symbol2=TCS.NS

**Request:**
```
GET http://localhost:8000/api/compare?symbol1=INFY.NS&symbol2=TCS.NS
```

**Response (200 OK):**
```json
{
  "symbol1": "INFY.NS",
  "symbol2": "TCS.NS",
  "symbol1_returns": 8.50,
  "symbol2_returns": 12.30,
  "correlation": 0.8543,
  "better_performer": "TCS.NS",
  "data_points": 250
}
```

---

## 5. GET /api/predict/{symbol}

**Request:**
```
GET http://localhost:8000/api/predict/INFY.NS
```

**Response (200 OK):**
```json
{
  "symbol": "INFY.NS",
  "next_day_prediction": 1560.50,
  "confidence": 0.8234,
  "trend": "UP",
  "base_price": 1550.75
}
```

---

## 6. POST /api/refresh/{symbol}

**Request:**
```
POST http://localhost:8000/api/refresh/INFY.NS
```

**Response (200 OK):**
```json
{
  "symbol": "INFY.NS",
  "records_updated": 252,
  "status": "success"
}
```

---

## 7. GET /api/health

**Request:**
```
GET http://localhost:8000/api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## Error Examples

### 404 Not Found - Company Not Found

**Request:**
```
GET http://localhost:8000/api/summary/INVALID.NS
```

**Response:**
```json
{
  "detail": "No data available for symbol: INVALID.NS"
}
```

### 400 Bad Request - Invalid Symbols

**Request:**
```
GET http://localhost:8000/api/compare?symbol1=INFY.NS&symbol2=INFY.NS
```

**Response:**
```json
{
  "detail": "Cannot compare a stock with itself"
}
```

### 400 Bad Request - Insufficient Data

**Request:**
```
GET http://localhost:8000/api/predict/NEWSTOCK.NS
```

**Response:**
```json
{
  "detail": "Insufficient data to predict price for NEWSTOCK.NS"
}
```

---

## Using the APIs with Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# 1. Get all companies
response = requests.get(f"{BASE_URL}/companies")
print(response.json())

# 2. Get stock data
response = requests.get(f"{BASE_URL}/data/INFY.NS", params={"days": 30})
data = response.json()
print(f"Got {len(data)} records")

# 3. Get summary
response = requests.get(f"{BASE_URL}/summary/INFY.NS")
summary = response.json()
print(f"Current Price: ₹{summary['current_price']}")

# 4. Compare stocks
response = requests.get(
    f"{BASE_URL}/compare",
    params={"symbol1": "INFY.NS", "symbol2": "TCS.NS"}
)
comparison = response.json()
print(f"Better performer: {comparison['better_performer']}")

# 5. Get prediction
response = requests.get(f"{BASE_URL}/predict/INFY.NS")
prediction = response.json()
print(f"Predicted price: {prediction['next_day_prediction']}")
```

---

## Using the APIs with JavaScript/Fetch

```javascript
const BASE_URL = 'http://localhost:8000/api';

// 1. Get all companies
async function getCompanies() {
  const response = await fetch(`${BASE_URL}/companies`);
  const companies = await response.json();
  console.log(companies);
}

// 2. Get stock data
async function getStockData(symbol, days = 30) {
  const response = await fetch(
    `${BASE_URL}/data/${symbol}?days=${days}`
  );
  const data = await response.json();
  console.log(data);
}

// 3. Get summary
async function getSummary(symbol) {
  const response = await fetch(`${BASE_URL}/summary/${symbol}`);
  const summary = await response.json();
  console.log(`Current Price: ₹${summary.current_price}`);
}

// 4. Compare stocks
async function compareStocks(symbol1, symbol2) {
  const response = await fetch(
    `${BASE_URL}/compare?symbol1=${symbol1}&symbol2=${symbol2}`
  );
  const comparison = await response.json();
  console.log(comparison);
}

// 5. Get prediction
async function getPrediction(symbol) {
  const response = await fetch(`${BASE_URL}/predict/${symbol}`);
  const prediction = await response.json();
  console.log(prediction);
}

// Call functions
getCompanies();
```

---

## Pagination Example (Future Feature)

```
GET /api/data/INFY.NS?days=30&page=1&page_size=50
```

Response would include:
```json
{
  "data": [...],
  "pagination": {
    "total": 252,
    "page": 1,
    "page_size": 50,
    "total_pages": 6
  }
}
```

---

## Rate Limiting (Best Practice)

Each API endpoint should respect rate limits:
- 100 requests per minute per IP
- 1000 requests per hour per IP

Headers in response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890
```

---

**All responses use timezone-aware UTC datetime strings (ISO 8601 format)**
