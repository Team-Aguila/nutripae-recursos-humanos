import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from .seeder import seed_db

def run_seeder():
    sync_database_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_database_url)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    
    try:
        print("Starting to seed database...")
        seed_db(db_session)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db_session.rollback()
    finally:
        db_session.close()

if __name__ == "__main__":
    run_seeder() 