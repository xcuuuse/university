from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True)
    products: Mapped[list[Product]] = relationship(back_populates="category")


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    manufacturer_id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_name: Mapped[str] = mapped_column(String(150))
    manufacturer_address: Mapped[str | None] = mapped_column(String(255))
    products: Mapped[list[Product]] = relationship(back_populates="manufacturer")


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column(String(20), unique=True)
    product_name: Mapped[str] = mapped_column(String(200))
    product_unit: Mapped[str] = mapped_column(String(20))
    product_is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"))
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.manufacturer_id")
    )
    category: Mapped[Category] = relationship(back_populates="products")
    manufacturer: Mapped[Manufacturer] = relationship(back_populates="products")
    price_histories: Mapped[list[PriceHistory]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="PriceHistory.start_date",
    )
    invoice_items: Mapped[list[InvoiceItem]] = relationship(back_populates="product")


class PriceHistory(Base):
    __tablename__ = "price_histories"
    __table_args__ = (UniqueConstraint("product_id", "start_date"),)
    price_history_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    start_date: Mapped[date] = mapped_column(Date)
    product: Mapped[Product] = relationship(back_populates="price_histories")


class Country(Base):
    __tablename__ = "countries"
    country_id: Mapped[int] = mapped_column(primary_key=True)
    country_name: Mapped[str] = mapped_column(String(100), unique=True)
    country_kind: Mapped[str] = mapped_column(String(10))
    regions: Mapped[list[Region]] = relationship(back_populates="country")
    cities: Mapped[list[City]] = relationship(back_populates="country")


class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (UniqueConstraint("region_name", "country_id"),)
    region_id: Mapped[int] = mapped_column(primary_key=True)
    region_name: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.country_id"))
    country: Mapped[Country] = relationship(back_populates="regions")
    cities: Mapped[list[City]] = relationship(back_populates="region")


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("city_name", "region_id", "country_id"),)
    city_id: Mapped[int] = mapped_column(primary_key=True)
    city_name: Mapped[str] = mapped_column(String(100))
    region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.region_id"))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.country_id"))
    region: Mapped[Region | None] = relationship(back_populates="cities")
    country: Mapped[Country] = relationship(back_populates="cities")
    invoices: Mapped[list[Invoice]] = relationship(back_populates="city")


class Bank(Base):
    __tablename__ = "banks"
    bank_id: Mapped[int] = mapped_column(primary_key=True)
    bank_name: Mapped[str] = mapped_column(String(200))
    bank_code: Mapped[str] = mapped_column(String(20), unique=True)
    buyers: Mapped[list[Buyer]] = relationship(back_populates="bank")


class Buyer(Base):
    __tablename__ = "buyers"
    buyer_id: Mapped[int] = mapped_column(primary_key=True)
    buyer_type: Mapped[str] = mapped_column(String(10))
    buyer_name: Mapped[str] = mapped_column(String(200))
    buyer_address: Mapped[str] = mapped_column(String(255))
    doc_series: Mapped[str | None] = mapped_column(String(10))
    doc_number: Mapped[str | None] = mapped_column(String(20))
    account: Mapped[str | None] = mapped_column(String(34))
    bank_id: Mapped[int | None] = mapped_column(ForeignKey("banks.bank_id"))
    bank: Mapped[Bank | None] = relationship(back_populates="buyers")
    invoices: Mapped[list[Invoice]] = relationship(back_populates="buyer")


class Invoice(Base):
    __tablename__ = "invoices"
    invoice_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(20), unique=True)
    doc_date: Mapped[date] = mapped_column(Date, index=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.buyer_id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
    buyer: Mapped[Buyer] = relationship(back_populates="invoices")
    city: Mapped[City] = relationship(back_populates="invoices")
    items: Mapped[list[InvoiceItem]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan"
    )
    @property
    def total(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal("0.00"))


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    __table_args__ = (UniqueConstraint("invoice_id", "product_id"),)
    invoice_item_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.invoice_id"), index=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    invoice: Mapped[Invoice] = relationship(back_populates="items")
    product: Mapped[Product] = relationship(back_populates="invoice_items")

    @property
    def total(self) -> Decimal:
        return self.quantity * self.price