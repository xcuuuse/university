from sqlalchemy import select, func
from sqlalchemy.orm import query

from .base import SessionLocal
from .models import (
    Bank,
    Buyer,
    Category,
    City,
    Invoice,
    InvoiceItem,
    Manufacturer,
    PriceHistory,
    Product
)

session = SessionLocal()

def get_categories():
    return session.scalars(select(Category).order_by(Category.category_name)).all()

def get_manufacturers():
    return session.scalars(
        select(Manufacturer).order_by(Manufacturer.manufacturer_name)
    ).all()

def get_buyers():
    return session.scalars(
        select(Buyer).order_by(Buyer.buyer_name)
    ).all()

def get_cities():
    return session.scalars(
        select(City).order_by(City.city_name)
    ).all()

def get_banks():
    return session.scalars(select(Bank).order_by(Bank.bank_name)).all()


def get_products(name=None, category_id=None):
    query = select(Product)
    if category_id:
        query = query.where(Product.category_id == category_id)
    products = session.scalars(query.order_by(Product.product_name)).all()
    if name:
        products = [p for p in products if name.lower() in p.product_name.lower()]
    return products

def get_product(product_id):
    return session.get(Product, product_id)

def add_product(code, name, unit, category_id, manufacturer_id):
    product = Product(
        product_code=code,
        product_name=name,
        product_unit=unit,
        category_id=category_id,
        manufacturer_id=manufacturer_id
    )
    session.add(product)
    session.commit()
    return product

def update_product(product_id, code, name, unit, category_id, manufacturer_id):
    product = session.get(Product, product_id)
    product.product_code = code,
    product.product_name = name,
    product.product_unit = unit,
    product.category_id = category_id,
    product.manufacturer_id = manufacturer_id
    session.commit()
    return product

def delete_product(product_id):
    product = session.get(Product, product_id)
    used = session.scalar(
        select(func.count()).select_from(InvoiceItem)
        .where(InvoiceItem.product_id == product_id)
    )
    if used:
        raise ValueError("Cannot delete")
    session.delete(product)
    session.commit()


def get_prices(product_id):
    return session.scalars(
        select(PriceHistory).
        where(PriceHistory.product_id == product_id).
        order_by(PriceHistory.start_date)
    ).all()

def add_price(product_id, price, start_date):
    session.add(
        PriceHistory(
            product_id=product_id,
            price=price,
            start_date=start_date
        )
    )
    session.commit()

def delete_price(price_id):
    session.delete(session.get(PriceHistory, price_id))
    session.commit()


def get_invoices(date_from=None, date_to=None):
    invoices_query = select(Invoice)
    if date_from:
        invoices_query = invoices_query.where(Invoice.doc_date >= date_from)
    if date_to:
        invoices_query = invoices_query.where(Invoice.doc_date <= date_to)
    return session.scalars(invoices_query.order_by(Invoice.doc_date.desc())).all()


def get_invoice(invoice_id):
    return session.get(Invoice, invoice_id)

def add_invoice(number, doc_date, buyer_id, city_id, items):
    invoice = Invoice(
        invoice_number=number,
        doc_date=doc_date,
        buyer_id=buyer_id,
        city_id=city_id,
    )
    for product_id, quantity, price in items:
        invoice.items.append(
            InvoiceItem(
                product_id=product_id,
                quantity=quantity,
                price=price
            )
        )
    session.commit()
    return invoice

def delete_invoice(invoice_id):
    session.delete(session.get(Invoice, invoice_id))
    session.commit()


def top_buyers(day):
    total = func.sum(InvoiceItem.quantity * InvoiceItem.price)
    rows = session.execute(
        select(
            Buyer.buyer_name,
            Buyer.buyer_address,
            total)
        .join(Invoice, Invoice.buyer_id == Buyer.buyer_id)
        .join(InvoiceItem, InvoiceItem.invoice_id == Invoice.invoice_id)
        .where(Invoice.doc_date == day)
        .group_by(Buyer.buyer_id)
        .order_by(total.desc())
    ).all()
    if not rows:
        return []
    best = rows[0][2]
    return [
        (day, name, addr, round(float(s), 2))
        for name, addr, s in rows if s == best
    ]

def price_changes(product_id, date_from, date_to):
    rows = session.execute(
        select(
            Manufacturer.manufacturer_name,
            Product.product_name,
            PriceHistory.start_date,
            PriceHistory.price
        )
        .join(Product, Product.product_id == PriceHistory.product_id)
        .join(Manufacturer, Manufacturer.manufacturer_id == Product.manufacturer_id)
        .where(
            PriceHistory.product_id == product_id,
            PriceHistory.start_date >= date_from,
            PriceHistory.start_date <= date_to,
        )
        .order_by(PriceHistory.start_date)
    ).all()
    return [(m, p, d, round(float(pr), 2)) for m, p, d, pr in rows]


