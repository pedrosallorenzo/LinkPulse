from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv('postgresql://link_pulse_db_user:X3tPIOciBc3o2bGootVXHHDSUBYWJw7T@dpg-d00n03qdbo4c73dgbv80-a/link_pulse_db')

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()