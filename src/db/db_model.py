from sqlalchemy import TEXT, REAL, INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import db_settings


class Base(DeclarativeBase):
    pass


class RentApartments(Base):
    __tablename__ = db_settings.RENT_APARTMENTS_TABLE_NAME
    address: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    area: Mapped[float] = mapped_column(REAL())
    constraction_year: Mapped[int] = mapped_column(INTEGER())
    rooms: Mapped[int] = mapped_column(INTEGER())
    bedrooms: Mapped[int] = mapped_column(INTEGER())
    bathrooms: Mapped[int] = mapped_column(INTEGER())
    balcony: Mapped[str] = mapped_column(TEXT())
    storage: Mapped[str] = mapped_column(TEXT())
    parking: Mapped[str] = mapped_column(TEXT())
    furnished: Mapped[str] = mapped_column(TEXT())
    garage: Mapped[str] = mapped_column(TEXT())
    garden: Mapped[str] = mapped_column(TEXT())
    energy: Mapped[str] = mapped_column(TEXT())
    facilities: Mapped[str] = mapped_column(TEXT())
    zip: Mapped[str] = mapped_column(TEXT())
    neighborhood: Mapped[str] = mapped_column(TEXT())
    rent: Mapped[int] = mapped_column(INTEGER())