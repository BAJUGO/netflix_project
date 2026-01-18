from sqlalchemy.orm import mapped_column, Mapped

from backend.core import Base


class User(Base):
    __tablename__ = "users"

    visible_name: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes] = mapped_column()
    role: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column()
