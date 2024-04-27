__all__ = ("bot", "Session", "c")

import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.bot import bot

conn = sqlite3.connect("db_tags.db")
c = conn.cursor()

engine = create_engine("sqlite:///clubs_database.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autoflush=True)
