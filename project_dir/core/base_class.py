from sqlalchemy.orm import declarative_base, Mapped, mapped_column


class Base(declarative_base):
    id: Mapped[int] = mapped_column(primary_key=True)

