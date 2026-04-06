# this is the database initialization file

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin-3311:Team9courseproject@eecs3311.database.windows.net/Team9-ConsultingService") # put database URL here

engine = create_engine(DATABASE_URL, echo=True) # echo=True for logging SQL queries, set to False in production
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db(retries=5):
    """Create all database tables"""
    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as e:
            if attempt < retries - 1:
                print(f"Database not ready. Retrying in 2 seconds... ({attempt+1}/{retries})")
                time.sleep(2)
            else:
                raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

