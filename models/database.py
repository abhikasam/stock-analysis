from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from core.config import Configuration

engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

Entity = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

