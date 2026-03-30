"""
ML prediction utility
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class MLPredictor:
    """Simple linear regression for stock price prediction"""

    @staticmethod
    def predict_next_day(df: pd.DataFrame, lookback: int = 30) -> Optional[Tuple[float, float]]:
        """
        Predict next day closing price using linear regression
        
        Args:
            df: Stock data with close prices (must have at least lookback days)
            lookback: Number of days to use for training
        
        Returns:
            Tuple of (predicted_price, confidence) or None
        """
        if len(df) < lookback:
            logger.warning(f"Insufficient data. Have {len(df)}, need {lookback}")
            return None
        
        try:
            # Use last N days
            data = df.tail(lookback).copy()
            
            # Create features and target
            X = np.arange(len(data)).reshape(-1, 1)
            y = data['close'].values
            
            # Train model
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict next value
            next_X = np.array([[len(data)]])
            prediction = model.predict(next_X)[0]
            
            # Calculate R-squared as confidence (0-1)
            r_squared = model.score(X, y)
            confidence = max(0, min(1, r_squared))
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return None

    @staticmethod
    def get_trend(current_price: float, predicted_price: float, threshold: float = 0.01) -> str:
        """
        Determine trend based on prediction
        
        Args:
            current_price: Current closing price
            predicted_price: Predicted closing price
            threshold: Threshold for neutral trend (1%)
        
        Returns:
            "UP", "DOWN", or "NEUTRAL"
        """
        percent_change = (predicted_price - current_price) / current_price
        
        if percent_change > threshold:
            return "UP"
        elif percent_change < -threshold:
            return "DOWN"
        else:
            return "NEUTRAL"
