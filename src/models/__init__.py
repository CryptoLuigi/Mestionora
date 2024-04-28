from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .clubs import ClubMember, Club
