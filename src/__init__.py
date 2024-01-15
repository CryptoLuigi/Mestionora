from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base


engine = create_engine("sqlite:///clubs_database.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autoflush=True)
