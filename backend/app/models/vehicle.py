from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    brand: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    km_driven: Mapped[int] = mapped_column(Integer)

    usage: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    payload: Mapped[float] = mapped_column(Float)

    city: Mapped[str] = mapped_column(String)
    body_type: Mapped[str] = mapped_column(String)
    fuel_type: Mapped[str] = mapped_column(String)
    
    papers_verified: Mapped[bool] = mapped_column(Boolean)