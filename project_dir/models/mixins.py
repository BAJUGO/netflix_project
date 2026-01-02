from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .author import Author


class AuthorRelationMixin:
    _author_back_populates: str | None = None

    @declared_attr
    def author_id(self) -> Mapped[int]:
        return mapped_column(ForeignKey("authors.id"))

    @declared_attr
    def author(self) -> Mapped["Author"]:
        return relationship("Author", back_populates=self._author_back_populates)
