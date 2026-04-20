from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings

engine=create_engine(settings.DATABASE_URL)

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
