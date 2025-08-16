"""
Script to create all database tables based on the MASTER_DATABASE_SCHEMA.md
This will create the initial database structure in AWS MySQL
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from database import engine, test_connection, logger
from models import Base
from dotenv import load_dotenv

def create_all_tables():
    """
    Create all tables in the database
    """
    try:
        # Test connection first
        if not test_connection():
            logger.error("Cannot connect to database. Exiting.")
            return False
        
        logger.info("Creating all database tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Successfully created all database tables!")
        return True
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

def drop_all_tables():
    """
    Drop all tables in the database (use with caution!)
    """
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Successfully dropped all database tables!")
        return True
        
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--drop":
            logger.warning("⚠️  WARNING: This will drop all existing tables!")
            confirm = input("Are you sure you want to continue? (type 'yes' to confirm): ")
            if confirm.lower() == 'yes':
                if drop_all_tables():
                    logger.info("Tables dropped successfully.")
                else:
                    logger.error("Failed to drop tables.")
                    sys.exit(1)
            else:
                logger.info("Operation cancelled.")
                sys.exit(0)
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python create_tables.py        - Create all tables")
            print("  python create_tables.py --drop - Drop all tables (with confirmation)")
            print("  python create_tables.py --help - Show this help")
            sys.exit(0)
    
    # Create tables
    if create_all_tables():
        logger.info("✅ Database setup completed successfully!")
    else:
        logger.error("❌ Database setup failed!")
        sys.exit(1)