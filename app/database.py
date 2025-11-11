import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load ENV variables from .env file
load_dotenv()

# Read database URL from environment, fallback to local if missing
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")

# Safely encode password
parsed_url = urllib.parse.urlparse(DATABASE_URL)
password = urllib.parse.quote_plus(parsed_url.password)
SQLALCHEMY_DATABASE_URL = f"postgresql://{parsed_url.username}:{password}@{parsed_url.hostname}:{parsed_url.port}{parsed_url.path}"

# Engine with SSL for Railway
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"} if "railway" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
