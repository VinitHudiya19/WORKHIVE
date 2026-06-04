from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

connect_args = {}
# Enable SSL automatically for cloud-hosted databases (e.g. Aiven, Render)
if "localhost" not in settings.DATABASE_URL and "127.0.0.1" not in settings.DATABASE_URL:
    connect_args["ssl"] = {}

engine = create_engine(
    settings.DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
