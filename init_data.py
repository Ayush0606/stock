"""
Initialize stock data from yfinance
Run this script to load initial data into the database
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import init_db, SessionLocal
from app.services.stock_service import StockService
from app.utils.data_processor import DataProcessor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_initial_data():
    """Load stock data for predefined symbols"""
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    symbols = DataProcessor.STOCK_SYMBOLS
    
    logger.info(f"Loading data for symbols: {symbols}")
    
    for symbol in symbols:
        try:
            logger.info(f"\n{'='*50}")
            logger.info(f"Processing {symbol}...")
            logger.info(f"{'='*50}")
            
            # Fetch and process data
            df = DataProcessor.process_stock_data(symbol, period="1y")
            
            if df is None or df.empty:
                logger.warning(f"No data available for {symbol}")
                continue
            
            logger.info(f"Fetched {len(df)} records for {symbol}")
            
            # Save to database
            count = StockService.save_stock_data(db, df)
            logger.info(f"✅ Saved {count} records for {symbol}")
            
        except Exception as e:
            logger.error(f"❌ Error processing {symbol}: {str(e)}")
            continue
    
    db.close()
    logger.info(f"\n{'='*50}")
    logger.info("✅ Data initialization complete!")
    logger.info(f"{'='*50}")


if __name__ == "__main__":
    load_initial_data()
