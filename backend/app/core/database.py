from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

#Engine - connection to DB
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, #Keeps connection healthy
    pool_size=5, #basic connection pool
    max_overflow=10
)

#Session factory 
Sessionlocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

#base calss for models
Base = declarative_base()

#FastAPI dependencies
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()