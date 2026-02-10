from sqlalchemy import DateTime, String, Text, Float, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase): 
    create: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Bets(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name:   Mapped[str] = mapped_column(String(150), nullable=False)
    descriptio: Mapped[str] = mapped_column(Text)
    coefficient: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
