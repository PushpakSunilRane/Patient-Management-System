"""
Database setup script for the Healthcare Dashboard.
This script creates the database and tables if they don't exist.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def create_database():
    """Create the healthcare_dashboard database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' created successfully or already exists")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

def setup_tables():
    """Create all necessary tables"""
    from database import DatabaseManager
    
    try:
        db = DatabaseManager()
        db.create_tables()
        print("All tables created successfully")
        db.disconnect()
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Setting up Healthcare Dashboard Database...")
    print("=" * 50)
    
    # Step 1: Create database
    print("1. Creating database...")
    if create_database():
        print("✓ Database created successfully")
    else:
        print("✗ Failed to create database")
        exit(1)
    
    # Step 2: Create tables
    print("\n2. Creating tables...")
    if setup_tables():
        print("✓ Tables created successfully")
    else:
        print("✗ Failed to create tables")
        exit(1)
    
    print("\n" + "=" * 50)
    print("Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python sample_data.py' to add sample data")
    print("2. Run 'streamlit run app.py' to start the dashboard")
