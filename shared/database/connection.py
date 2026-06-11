import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 1. Import find_dotenv along with load_dotenv
from dotenv import load_dotenv, find_dotenv

# 2. Tell dotenv to look up the directory tree until it finds the .env file
load_dotenv(find_dotenv())

# 3. Pull variables with safe fallbacks (like default Postgres port 5432)
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST', 'localhost')
port = os.getenv('POSTGRES_PORT', '5432')  # Prevents the "None" string bug
db_name = os.getenv('POSTGRES_DB')

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()