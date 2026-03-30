"""
Data processing and cleaning utilities
"""
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handle stock data fetching, cleaning, and metric calculation"""

    STOCK_SYMBOLS = ["INFY.NS", "TCS.NS", "RELIANCE.NS"]  # India-focused stocks
    STOCK_NAMES = {
        "INFY.NS": "Infosys",
        "TCS.NS": "Tata Consultancy Services",
        "RELIANCE.NS": "Reliance Industries"
    }

    @staticmethod
    def fetch_stock_data(symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch stock data using yfinance
        
        Args:
            symbol: Stock symbol (e.g., 'INFY.NS')
            period: Time period ('1y', '3mo', '1mo', etc.)
        
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            logger.info(f"Fetching data for {symbol} with period {period}")
            df = yf.download(symbol, period=period, progress=False)
            
            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            logger.info(f"After yfinance download - shape: {df.shape}, columns: {df.columns.tolist()}")
            
            # Reset index to convert Date to a column
            df.reset_index(inplace=True)
            
            logger.info(f"After reset_index - shape: {df.shape}, columns: {df.columns.tolist()}")
            
            # Handle MultiIndex columns from yfinance (when downloading single symbol)
            if isinstance(df.columns, pd.MultiIndex):
                # Flatten the MultiIndex by taking the first level (the price type)
                df.columns = [col[0].lower() if isinstance(col, tuple) else str(col).lower() for col in df.columns]
            else:
                # Standard single-level columns
                df.columns = [str(col).lower() for col in df.columns]
            
            logger.info(f"After flattening columns - columns: {df.columns.tolist()}")
            
            # Select only the columns we actually need
            available = [c for c in ['date', 'open', 'high', 'low', 'close', 'volume'] if c in df.columns]
            logger.info(f"Available columns to select: {available}")
            
            if not available:
                logger.error(f"No valid columns found! Available: {df.columns.tolist()}")
                return None
            
            df = df[available].copy()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate stock data
        
        Args:
            df: Raw stock data
        
        Returns:
            Cleaned DataFrame
        """
        # Make a copy to avoid modifying original
        df = df.copy()
        logger.info(f"Initial dataframe shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        
        # Ensure date column is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Drop rows with missing critical values
        critical_cols = ['open', 'close', 'high', 'low']
        before_drop = len(df)
        df = df.dropna(subset=critical_cols)
        logger.info(f"After dropna: {len(df)} rows (dropped {before_drop - len(df)})")
        
        # Fill missing volume with 0
        df['volume'] = df['volume'].fillna(0)
        
        # Ensure numeric columns are correct type
        numeric_cols = [col for col in ['open', 'close', 'high', 'low', 'volume'] if col in df.columns]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with non-positive prices
        before_filter = len(df)
        df = df[(df['open'] > 0) & (df['close'] > 0) & (df['high'] > 0) & (df['low'] > 0)]
        logger.info(f"After filtering positive prices: {len(df)} rows (filtered {before_filter - len(df)})")
        
        # Sort by date
        df = df.sort_values('date', ascending=True).reset_index(drop=True)
        
        logger.info(f"Data cleaned. Shape: {df.shape}, Missing values: {df.isnull().sum().sum()}")
        return df

    @staticmethod
    def calculate_daily_return(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily returns: (Close - Open) / Open"""
        df['daily_return'] = ((df['close'] - df['open']) / df['open']) * 100
        return df

    @staticmethod
    def calculate_moving_average(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
        """Calculate moving average of close price"""
        df[f'moving_avg_{window}'] = df['close'].rolling(window=window, min_periods=1).mean()
        return df

    @staticmethod
    def calculate_volatility(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
        """Calculate volatility (standard deviation of returns)"""
        df['volatility_30'] = df['daily_return'].rolling(window=window, min_periods=1).std()
        return df

    @staticmethod
    def calculate_52week_stats(df: pd.DataFrame) -> Tuple[float, float]:
        """Calculate 52-week high and low"""
        high_52w = df['high'].max()
        low_52w = df['low'].min()
        return high_52w, low_52w

    @staticmethod
    def process_stock_data(symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Complete pipeline: fetch → clean → calculate metrics
        
        Args:
            symbol: Stock symbol
            period: Time period
        
        Returns:
            Processed DataFrame with all metrics
        """
        # Fetch and clean
        df = DataProcessor.fetch_stock_data(symbol, period)
        if df is None:
            logger.warning(f"fetch_stock_data returned None for {symbol}")
            return None
        
        logger.info(f"After fetch: {df.shape}, columns: {df.columns.tolist()}")
        
        df = DataProcessor.clean_data(df)
        
        if df.empty:
            logger.warning(f"DataFrame is empty after cleaning for {symbol}")
            return None
        
        logger.info(f"After clean: {df.shape}")
        
        # Calculate metrics
        df = DataProcessor.calculate_daily_return(df)
        df = DataProcessor.calculate_moving_average(df, window=7)
        df = DataProcessor.calculate_volatility(df, window=30)
        
        # Add symbol column
        df['symbol'] = symbol
        
        logger.info(f"Processing complete for {symbol}. Shape: {df.shape}")
        return df

    @staticmethod
    def get_last_n_days(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
        """Get last N days of data"""
        return df.tail(days).copy()

    @staticmethod
    def compare_stocks(df1: pd.DataFrame, df2: pd.DataFrame) -> dict:
        """
        Compare two stock DataFrames
        
        Args:
            df1: First stock data
            df2: Second stock data
        
        Returns:
            Dictionary with comparison metrics
        """
        returns1 = df1['daily_return'].sum()
        returns2 = df2['daily_return'].sum()
        
        # Calculate correlation for common dates
        common_dates = pd.merge(
            df1[['date']], df2[['date']], 
            on='date', how='inner'
        )
        
        if len(common_dates) > 1:
            df1_common = df1[df1['date'].isin(common_dates['date'])].copy()
            df2_common = df2[df2['date'].isin(common_dates['date'])].copy()
            correlation = df1_common['close'].corr(df2_common['close'])
        else:
            correlation = 0.0
        
        return {
            "symbol1": df1['symbol'].iloc[0],
            "symbol2": df2['symbol'].iloc[0],
            "symbol1_returns": round(returns1, 2),
            "symbol2_returns": round(returns2, 2),
            "correlation": round(correlation, 4),
            "better_performer": df1['symbol'].iloc[0] if returns1 > returns2 else df2['symbol'].iloc[0],
            "data_points": len(common_dates)
        }
