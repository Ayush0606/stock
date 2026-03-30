"""
Main FastAPI application
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging

from app.database import init_db
from app.routes import stocks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Get environment variables
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Configure CORS based on environment
if ENVIRONMENT == 'production':
    # Production: restrict to specific origins
    allow_origins = [
        FRONTEND_URL,
        'https://stock-dashboard-frontend.onrender.com'  # Render frontend URL
    ]
else:
    # Development: allow localhost
    allow_origins = [
        'http://localhost:3000',
        'http://localhost:3001',
        'http://localhost:8000',
        FRONTEND_URL
    ]

logger.info(f"Running in {ENVIRONMENT} mode with CORS origins: {allow_origins}")

# Create FastAPI app
app = FastAPI(
    title="Stock Data Intelligence Dashboard",
    description="API for fetching, analyzing, and predicting stock data",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routes
app.include_router(stocks.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Stock Data Intelligence Dashboard",
        "docs": "/api/docs",
        "health": "/api/health"
    }


@app.get("/api/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Stock Data Intelligence Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "companies": "/api/companies",
            "data": "/api/data/{symbol}",
            "summary": "/api/summary/{symbol}",
            "compare": "/api/compare?symbol1=INFY.NS&symbol2=TCS.NS",
            "predict": "/api/predict/{symbol}",
            "refresh": "/api/refresh/{symbol}",
            "docs": "/api/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
