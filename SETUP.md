# Setup Instructions for Stock Data Intelligence Dashboard

## Prerequisites
- Python 3.9+
- Node.js 16+ & npm
- Git
- Docker & Docker Compose (optional)

## Quick Setup (5 minutes)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
cd ..
python init_data.py

# Start backend
cd backend
python -m uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000

### 2. Frontend Setup (in new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend will run on: http://localhost:3000

## Accessing the Application

1. **Frontend Dashboard**: http://localhost:3000
2. **API Documentation**: http://localhost:8000/api/docs
3. **API Redoc**: http://localhost:8000/api/redoc

## Using Docker

```bash
# Build and run with Docker Compose
docker-compose up

# Stop services
docker-compose down

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

## Environment Variables

Create `.env` file in root directory:

```
DATABASE_URL=sqlite:///./stock_data.db
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

For production:
```
DATABASE_URL=postgresql://user:password@localhost:5432/stock_db
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=WARNING
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution**: Make sure you're in the backend directory when running the app

### Issue: "Port 8000 already in use"
**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### Issue: "npm: command not found"
**Solution**: Install Node.js from https://nodejs.org/

### Issue: Database is empty (no companies showing)
**Solution**: Run the initialization script again
```bash
python init_data.py
```

## Project Structure

```
Stock/
├── backend/
│   └── app/              # FastAPI application
├── frontend/
│   └── src/              # React components
├── init_data.py          # Initialize database
├── docker-compose.yml    # Docker setup
└── README.md             # Full documentation
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/companies | List all companies |
| GET | /api/data/{symbol} | Stock data for N days |
| GET | /api/summary/{symbol} | Stock summary stats |
| GET | /api/compare | Compare two stocks |
| GET | /api/predict/{symbol} | Predict next day price |
| POST | /api/refresh/{symbol} | Refresh stock data |

## Development Tips

1. **Frontend Development**:
   - Vite provides hot module reload
   - Check browser console for errors
   - API proxy is configured in vite.config.js

2. **Backend Development**:
   - FastAPI auto-reload enabled
   - Swagger docs auto-update
   - Check terminal for logging output

3. **Database**:
   - SQLite file: `stock_data.db`
   - Reset: Delete the file and run `python init_data.py`

## Installing Additional Packages

### Backend
```bash
cd backend
pip install package_name
pip freeze > requirements.txt
```

### Frontend
```bash
cd frontend
npm install package-name
npm update package-name
```

## Building for Production

### Backend
```bash
cd backend
# Just run with uvicorn in production settings
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend
```bash
cd frontend
npm run build
# Deploy dist/ folder to CDN or web server
```

## Performance Optimization

- API responses are cached where applicable
- Database has indexes on frequently queried columns
- Frontend uses React memoization to prevent unnecessary re-renders
- Chart.js is optimized for large datasets

## Security Notes

- Input validation is done via Pydantic
- SQL injection is prevented by SQLAlchemy ORM
- CORS is enabled for local development (update for production)
- Environment variables should be used for sensitive data

## Support & Learning

- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- Vite Guide: https://vitejs.dev/guide/
- Chart.js: https://www.chartjs.org/docs/latest/

---

**Happy coding! 🚀**
