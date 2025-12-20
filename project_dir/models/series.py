from sqlalchemy.orm import Mapped, mapped_column

from .mixins import AuthorRelationMixin
from ..core import Base
from ..models import Gener


class Series(AuthorRelationMixin, Base):
    __tablename__ = "series"
    _author_back_populates = "series"

    title: Mapped[str] = mapped_column()
    episodes: Mapped[int] = mapped_column()
    seasons: Mapped[int] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)
    genre: Mapped[str] = mapped_column()


