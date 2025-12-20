from sqlalchemy.orm import Mapped, mapped_column

from ..core import Base
from ..models import Gener


class Movie(Base):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column()
    year_of_issue: Mapped[int] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)
    genre: Mapped[Gener] = mapped_column()

    # author: Mapped[str] = mapped_column()
