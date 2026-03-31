"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stock_data.db")

# For SQLite, use StaticPool to avoid threading issues
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables and load initial data"""
    Base.metadata.create_all(bind=engine)
    
    # Load initial data if database is empty
    db = SessionLocal()
    try:
        from app.models import StockData
        
        # Check if database is empty
        count = db.query(StockData).count()
        if count == 0:
            logger.info("Database is empty. Loading initial stock data...")
            from app.utils.data_processor import DataProcessor
            
            symbols = ['INFY.NS', 'TCS.NS', 'RELIANCE.NS']
            for symbol in symbols:
                try:
                    logger.info(f"Loading data for {symbol}...")
                    DataProcessor.fetch_and_save_stock_data(symbol, db)
                except Exception as e:
                    logger.warning(f"Failed to load data for {symbol}: {str(e)}")
            
            logger.info("Initial data loading complete.")
        else:
            logger.info(f"Database already has {count} records.")
    except Exception as e:
        logger.error(f"Error during init_db: {str(e)}")
    finally:
        db.close()
