from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    aadhar_number:Mapped[int]
    