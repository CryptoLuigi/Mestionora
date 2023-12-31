from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from src.clubs.models import Club, ClubMember