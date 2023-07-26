import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from fastapi import Depends

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(
    DATABASE_URL.replace("postgres", "postgresql"), pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
