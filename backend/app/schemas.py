"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class StockDataBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=15)
    date: datetime
    open_price: float = Field(..., gt=0)
    close_price: float = Field(..., gt=0)
    high_price: float = Field(..., gt=0)
    low_price: float = Field(..., gt=0)
    volume: int = Field(default=0, ge=0)
    daily_return: Optional[float] = None
    moving_avg_7: Optional[float] = None
    volatility_30: Optional[float] = None


class StockDataCreate(StockDataBase):
    """Schema for creating stock data"""
    pass


class StockData(StockDataBase):
    """Schema for returning stock data"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StockSummary(BaseModel):
    """Schema for stock summary"""
    symbol: str
    current_price: float
    high_52_week: float
    low_52_week: float
    average_close: float
    volatility: float
    last_updated: datetime

    class Config:
        from_attributes = True


class StockComparison(BaseModel):
    """Schema for comparing two stocks"""
    symbol1: str
    symbol2: str
    symbol1_returns: float
    symbol2_returns: float
    correlation: float
    better_performer: str
    data_points: int

    class Config:
        from_attributes = True


class CompanyInfo(BaseModel):
    """Schema for company information"""
    symbol: str
    name: str
    sector: Optional[str] = None
    data_points: int

    class Config:
        from_attributes = True


class DatabaseStockData(BaseModel):
    """Schema for database response"""
    id: int
    symbol: str
    date: datetime
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int
    daily_return: Optional[float]
    moving_avg_7: Optional[float]
    volatility_30: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class MLPrediction(BaseModel):
    """Schema for ML predictions"""
    symbol: str
    next_day_prediction: float
    confidence: float
    trend: str  # "UP", "DOWN", "NEUTRAL"
    base_price: float
