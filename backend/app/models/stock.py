"""
SQLAlchemy models for stock data
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger, Index
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class StockData(Base):
    """Stock data model"""
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(BigInteger, default=0)
    daily_return = Column(Float, nullable=True)
    moving_avg_7 = Column(Float, nullable=True)
    volatility_30 = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes for common queries
    __table_args__ = (
        Index('idx_symbol_date', 'symbol', 'date'),
        Index('idx_symbol', 'symbol'),
        Index('idx_date', 'date'),
    )

    def __repr__(self):
        return f"<StockData(symbol={self.symbol}, date={self.date}, close={self.close_price})>"
