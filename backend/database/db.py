# this is the database initialization file

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin-3311:Team9courseproject@db:3306/Team9-ConsultingService") # put database URL here

engine = create_engine(DATABASE_URL, echo=True) # echo=True for logging SQL queries, set to False in production
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

