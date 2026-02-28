from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url="postgresql://postgres:123qwe@localhost:5432"
engine=create_engine(db_url)

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)