"""
Script to recreate all database tables
"""
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from database import engine, test_connection, logger
from models import Base
from dotenv import load_dotenv

def recreate_all_tables():
    """
    Drop and recreate all tables in the database
    """
    try:
        # Test connection first
        if not test_connection():
            logger.error("Cannot connect to database. Exiting.")
            return False
        
        logger.info("Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        logger.info("Creating all database tables...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Successfully recreated all database tables!")
        return True
        
    except Exception as e:
        logger.error(f"Error recreating tables: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Recreate tables
    if recreate_all_tables():
        logger.info("✅ Database recreation completed successfully!")
    else:
        logger.error("❌ Database recreation failed!")
        sys.exit(1)