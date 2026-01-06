from sqlalchemy.orm import Mapped, mapped_column

from .mixins import AuthorRelationMixin
from project_dir.core import Base



class Movie(AuthorRelationMixin, Base):
    __tablename__ = "movies"
    _author_back_populates_ = "movies"

    title: Mapped[str] = mapped_column()
    year_of_issue: Mapped[int] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)
    genre: Mapped[str] = mapped_column()
