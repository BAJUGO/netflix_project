from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core import Base

if TYPE_CHECKING:
    from ..models import Movie, Series


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()

    movies: Mapped[list["Movie"]] = relationship(back_populates="author")
    series: Mapped[list["Series"]] = relationship(back_populates="author")