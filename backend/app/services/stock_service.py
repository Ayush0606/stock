"""
Stock data service - handles business logic and database operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Optional, Dict
import logging

from app.models import StockData
from app.utils.data_processor import DataProcessor
from app.utils.ml_predictor import MLPredictor

logger = logging.getLogger(__name__)


class StockService:
    """Service for stock data operations"""

    @staticmethod
    def save_stock_data(db: Session, df: pd.DataFrame) -> int:
        """
        Save stock data to database
        
        Args:
            db: Database session
            df: DataFrame with stock data
        
        Returns:
            Number of records saved
        """
        count = 0
        try:
            # Prepare data for insertion
            for _, row in df.iterrows():
                # Check if record already exists
                existing = db.query(StockData).filter(
                    StockData.symbol == row['symbol'],
                    StockData.date == row['date']
                ).first()
                
                if existing:
                    # Update existing record
                    existing.open_price = row['open']
                    existing.close_price = row['close']
                    existing.high_price = row['high']
                    existing.low_price = row['low']
                    existing.volume = int(row['volume'])
                    existing.daily_return = row.get('daily_return')
                    existing.moving_avg_7 = row.get('moving_avg_7')
                    existing.volatility_30 = row.get('volatility_30')
                else:
                    # Create new record
                    stock_data = StockData(
                        symbol=row['symbol'],
                        date=row['date'],
                        open_price=row['open'],
                        close_price=row['close'],
                        high_price=row['high'],
                        low_price=row['low'],
                        volume=int(row['volume']),
                        daily_return=row.get('daily_return'),
                        moving_avg_7=row.get('moving_avg_7'),
                        volatility_30=row.get('volatility_30')
                    )
                    db.add(stock_data)
                
                count += 1
            
            db.commit()
            logger.info(f"Saved {count} records to database")
            return count
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving stock data: {str(e)}")
            raise

    @staticmethod
    def fetch_symbol_data(db: Session, symbol: str, days: int = 30) -> List[StockData]:
        """
        Fetch stock data for a symbol from database
        
        Args:
            db: Database session
            symbol: Stock symbol
            days: Number of days to fetch
        
        Returns:
            List of StockData records
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = db.query(StockData).filter(
                StockData.symbol == symbol,
                StockData.date >= cutoff_date
            ).order_by(StockData.date.asc()).all()
            
            logger.info(f"Fetched {len(records)} records for {symbol}")
            return records
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return []

    @staticmethod
    def get_summary(db: Session, symbol: str) -> Optional[Dict]:
        """
        Get summary statistics for a stock
        
        Args:
            db: Database session
            symbol: Stock symbol
        
        Returns:
            Dictionary with summary statistics
        """
        try:
            records = db.query(StockData).filter(StockData.symbol == symbol).all()
            
            if not records:
                return None
            
            df = pd.DataFrame([
                {
                    'close': r.close_price,
                    'high': r.high_price,
                    'low': r.low_price,
                    'date': r.date
                }
                for r in records
            ])
            
            summary = {
                'symbol': symbol,
                'current_price': float(df['close'].iloc[-1]),
                'high_52_week': float(df['high'].max()),
                'low_52_week': float(df['low'].min()),
                'average_close': float(df['close'].mean()),
                'volatility': float(df['close'].std()),
                'last_updated': df['date'].max().isoformat() if len(df) > 0 else None
            }
            
            logger.info(f"Generated summary for {symbol}")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary for {symbol}: {str(e)}")
            return None

    @staticmethod
    def compare_symbols(db: Session, symbol1: str, symbol2: str) -> Optional[Dict]:
        """
        Compare two stocks
        
        Args:
            db: Database session
            symbol1: First stock symbol
            symbol2: Second stock symbol
        
        Returns:
            Comparison dictionary
        """
        try:
            # Fetch data for both symbols
            records1 = db.query(StockData).filter(StockData.symbol == symbol1).all()
            records2 = db.query(StockData).filter(StockData.symbol == symbol2).all()
            
            if not records1 or not records2:
                return None
            
            df1 = pd.DataFrame([
                {'date': r.date, 'close': r.close_price, 'daily_return': r.daily_return}
                for r in records1
            ])
            
            df2 = pd.DataFrame([
                {'date': r.date, 'close': r.close_price, 'daily_return': r.daily_return}
                for r in records2
            ])
            
            df1['symbol'] = symbol1
            df2['symbol'] = symbol2
            
            comparison = DataProcessor.compare_stocks(df1, df2)
            
            logger.info(f"Compared {symbol1} and {symbol2}")
            return comparison
        except Exception as e:
            logger.error(f"Error comparing {symbol1} and {symbol2}: {str(e)}")
            return None

    @staticmethod
    def predict_price(db: Session, symbol: str) -> Optional[Dict]:
        """
        Predict next day price for a stock
        
        Args:
            db: Database session
            symbol: Stock symbol
        
        Returns:
            Prediction dictionary with prediction, confidence, and trend
        """
        try:
            records = db.query(StockData).filter(
                StockData.symbol == symbol
            ).order_by(StockData.date.asc()).all()
            
            if len(records) < 30:
                logger.warning(f"Insufficient data for prediction: {symbol}")
                return None
            
            df = pd.DataFrame([
                {'close': r.close_price}
                for r in records
            ])
            
            result = MLPredictor.predict_next_day(df, lookback=30)
            
            if result is None:
                return None
            
            predicted_price, confidence = result
            current_price = float(records[-1].close_price)
            trend = MLPredictor.get_trend(current_price, predicted_price)
            
            prediction = {
                'symbol': symbol,
                'next_day_prediction': round(predicted_price, 2),
                'confidence': round(confidence, 4),
                'trend': trend,
                'base_price': round(current_price, 2)
            }
            
            logger.info(f"Generated prediction for {symbol}: {prediction}")
            return prediction
        except Exception as e:
            logger.error(f"Error predicting price for {symbol}: {str(e)}")
            return None

    @staticmethod
    def get_all_symbols(db: Session) -> List[str]:
        """
        Get list of all available symbols in database
        
        Args:
            db: Database session
        
        Returns:
            List of unique symbols
        """
        try:
            symbols = db.query(StockData.symbol).distinct().all()
            symbol_list = [s[0] for s in symbols]
            return symbol_list
        except Exception as e:
            logger.error(f"Error fetching symbols: {str(e)}")
            return []

    @staticmethod
    def get_symbol_info(db: Session, symbol: str) -> Optional[Dict]:
        """
        Get information about a symbol
        
        Args:
            db: Database session
            symbol: Stock symbol
        
        Returns:
            Symbol info dictionary
        """
        try:
            count = db.query(StockData).filter(StockData.symbol == symbol).count()
            
            if count == 0:
                return None
            
            info = {
                'symbol': symbol,
                'name': DataProcessor.STOCK_NAMES.get(symbol, symbol),
                'data_points': count
            }
            
            return info
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return None
