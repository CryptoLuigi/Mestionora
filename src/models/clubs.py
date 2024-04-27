import typing
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    guild_id: Mapped[int] = mapped_column(index=True, nullable=False)
    creator_id: Mapped[int] = mapped_column(index=True, nullable=False)

    members: Mapped[typing.List["ClubMember"]] = relationship(
        "ClubMember", back_populates="club"
    )


class ClubMember(Base):
    __tablename__ = "club_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)

    club: Mapped["Club"] = relationship("Club", back_populates="members")

