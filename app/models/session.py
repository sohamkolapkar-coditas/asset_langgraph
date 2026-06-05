from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.config.env import settings

engine = create_engine(
    f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
db = SessionLocal()
