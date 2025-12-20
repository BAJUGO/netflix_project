from sqlalchemy.orm import declarative_base, Mapped, mapped_column


BaseModel_not_pyd = declarative_base()

class Base(BaseModel_not_pyd):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
