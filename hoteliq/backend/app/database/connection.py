from sqlalchemy import create_engine  #to create the engine for database url, for sqlite
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os 
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hoteliq.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args = {"check_same_thread":False} if "sqlite" in DATABASE_URL else {},
    echo= True
)

#Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()