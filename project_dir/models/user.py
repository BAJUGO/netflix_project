from sqlalchemy.orm import mapped_column, Mapped

from ..core import Base


class User(Base):
    __tablename__ = "users"

    visible_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    hashed_password: Mapped[bytes] = mapped_column()
    role: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column()

