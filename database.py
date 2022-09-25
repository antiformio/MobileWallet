from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


import os


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv(".env")

# POSTGRES doesnt have the check_same_thread, only SQLITE
if os.environ["DATABASE_URL"] == 'postgresql+psycopg2://root:password@db:5432/mobilewallet':
    engine = create_engine(
        os.environ["DATABASE_URL"]
    )
else:
    engine = create_engine(
        os.environ["DATABASE_URL"], connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()
