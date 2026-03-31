"""
Stock data routes/endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.services.stock_service import StockService
from app.schemas import (
    StockData as StockDataSchema,
    StockSummary,
    StockComparison,
    CompanyInfo,
    MLPrediction
)
from app.utils.data_processor import DataProcessor

logger = logging.getLogger(__name__)

router = APIRouter(tags=["stocks"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@router.get("/companies", response_model=List[CompanyInfo])
async def get_companies(db: Session = Depends(get_db)):
    """
    Get list of available stock symbols
    
    Returns:
        List of company information with available data points
    """
    try:
        symbols = StockService.get_all_symbols(db)
        companies = []
        
        for symbol in symbols:
            info = StockService.get_symbol_info(db, symbol)
            if info:
                companies.append(CompanyInfo(**info))
        
        if not companies:
            raise HTTPException(
                status_code=404,
                detail="No companies found in database. Please load data first."
            )
        
        return companies
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_companies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data/{symbol}", response_model=List[StockDataSchema])
async def get_stock_data(
    symbol: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get last N days of stock data for a symbol
    
    Args:
        symbol: Stock symbol (e.g., 'INFY.NS')
        days: Number of days to fetch (1-365, default 30)
    
    Returns:
        List of stock data records with calculated metrics
    """
    try:
        symbol = symbol.upper()
        
        # Fetch from database
        records = StockService.fetch_symbol_data(db, symbol, days)
        
        if not records:
            # Try to fetch from yfinance
            logger.info(f"No data for {symbol} in DB, fetching from yfinance...")
            df = DataProcessor.process_stock_data(symbol, period="1y")
            
            if df is None or df.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data available for symbol: {symbol}"
                )
            
            # Save to database
            StockService.save_stock_data(db, df)
            
            # Fetch again
            records = StockService.fetch_symbol_data(db, symbol, days)
        
        # Convert to schema
        result = [
            StockDataSchema(
                id=r.id,
                symbol=r.symbol,
                date=r.date,
                open_price=r.open_price,
                close_price=r.close_price,
                high_price=r.high_price,
                low_price=r.low_price,
                volume=r.volume,
                daily_return=r.daily_return,
                moving_avg_7=r.moving_avg_7,
                volatility_30=r.volatility_30,
                created_at=r.created_at
            )
            for r in records
        ]
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{symbol}", response_model=StockSummary)
async def get_summary(symbol: str, db: Session = Depends(get_db)):
    """
    Get summary statistics for a stock
    
    Args:
        symbol: Stock symbol (e.g., 'INFY.NS')
    
    Returns:
        Summary with 52-week high/low, average price, volatility
    """
    try:
        symbol = symbol.upper()
        
        # Try database first
        summary = StockService.get_summary(db, symbol)
        
        if not summary:
            # Fetch from yfinance
            logger.info(f"No summary for {symbol} in DB, fetching from yfinance...")
            df = DataProcessor.process_stock_data(symbol, period="1y")
            
            if df is None or df.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data available for symbol: {symbol}"
                )
            
            # Save to database
            StockService.save_stock_data(db, df)
            
            # Get summary again
            summary = StockService.get_summary(db, symbol)
        
        if not summary:
            raise HTTPException(status_code=404, detail=f"Could not generate summary for {symbol}")
        
        return StockSummary(**summary)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare", response_model=StockComparison)
async def compare_stocks(
    symbol1: str = Query(..., description="First stock symbol"),
    symbol2: str = Query(..., description="Second stock symbol"),
    db: Session = Depends(get_db)
):
    """
    Compare performance of two stocks
    
    Args:
        symbol1: First stock symbol (e.g., 'INFY.NS')
        symbol2: Second stock symbol (e.g., 'TCS.NS')
    
    Returns:
        Comparison with returns, correlation, and better performer
    """
    try:
        symbol1 = symbol1.upper()
        symbol2 = symbol2.upper()
        
        if symbol1 == symbol2:
            raise HTTPException(
                status_code=400,
                detail="Cannot compare a stock with itself"
            )
        
        # Ensure data exists for both
        for symbol in [symbol1, symbol2]:
            records = StockService.get_all_symbols(db)
            if symbol not in records:
                logger.info(f"Fetching data for {symbol}...")
                df = DataProcessor.process_stock_data(symbol, period="1y")
                if df is not None and not df.empty:
                    StockService.save_stock_data(db, df)
        
        # Compare
        comparison = StockService.compare_symbols(db, symbol1, symbol2)
        
        if not comparison:
            raise HTTPException(
                status_code=404,
                detail=f"Could not compare {symbol1} and {symbol2}"
            )
        
        return StockComparison(**comparison)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in compare_stocks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict/{symbol}", response_model=MLPrediction)
async def predict_stock_price(symbol: str, db: Session = Depends(get_db)):
    """
    Predict next day closing price using linear regression
    
    Args:
        symbol: Stock symbol (e.g., 'INFY.NS')
    
    Returns:
        Prediction with confidence score and trend
    """
    try:
        symbol = symbol.upper()
        
        # Ensure data exists
        records = StockService.get_all_symbols(db)
        if symbol not in records:
            logger.info(f"Fetching data for {symbol}...")
            df = DataProcessor.process_stock_data(symbol, period="1y")
            if df is not None and not df.empty:
                StockService.save_stock_data(db, df)
        
        # Predict
        prediction = StockService.predict_price(db, symbol)
        
        if not prediction:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data to predict price for {symbol}"
            )
        
        return MLPrediction(**prediction)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in predict_stock_price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh/{symbol}")
async def refresh_stock_data(symbol: str, db: Session = Depends(get_db)):
    """
    Refresh stock data from yfinance
    
    Args:
        symbol: Stock symbol to refresh
    
    Returns:
        Number of records updated
    """
    try:
        symbol = symbol.upper()
        
        # Fetch latest data
        df = DataProcessor.process_stock_data(symbol, period="1y")
        
        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for symbol: {symbol}"
            )
        
        # Save to database
        count = StockService.save_stock_data(db, df)
        
        return {
            "symbol": symbol,
            "records_updated": count,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in refresh_stock_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
