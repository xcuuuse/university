from sqlalchemy import func, select

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
    Product,
)

# Одна сессия на всё время работы приложения: связанные объекты
# (категория товара, покупатель накладной) подгружаются в любой момент.
session = SessionLocal()


def _commit():
    """Фиксирует транзакцию. При ошибке (нарушение уникальности, триггер,
    внешний ключ) откатывает её, иначе сессия останется в сломанном
    состоянии и все следующие запросы будут падать."""
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise


# ------------------------------------------------------------ справочники

def get_categories():
    """Список существующих категорий товаров в алфавитном порядке."""
    return session.scalars(select(Category).order_by(Category.category_name)).all()


def get_manufacturers():
    return session.scalars(
        select(Manufacturer).order_by(Manufacturer.manufacturer_name)
    ).all()


def get_buyers():
    return session.scalars(select(Buyer).order_by(Buyer.buyer_name)).all()


def get_cities():
    return session.scalars(select(City).order_by(City.city_name)).all()


def get_banks():
    return session.scalars(select(Bank).order_by(Bank.bank_name)).all()


# ----------------------------------------------------------------- товары

def get_products(name=None, category_id=None):
    """Список товаров с необязательными фильтрами."""
    query = select(Product)
    if category_id:
        # фильтр по категории выполняется на стороне СУБД
        query = query.where(Product.category_id == category_id)
    products = session.scalars(query.order_by(Product.product_name)).all()
    if name:
        # поиск по названию выполняется в Python: встроенная функция lower()
        # в SQLite не переводит кириллицу в нижний регистр
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
        manufacturer_id=manufacturer_id,
    )
    session.add(product)
    _commit()
    return product


def update_product(product_id, code, name, unit, category_id, manufacturer_id):
    product = session.get(Product, product_id)
    product.product_code = code
    product.product_name = name
    product.product_unit = unit
    product.category_id = category_id
    product.manufacturer_id = manufacturer_id
    _commit()
    return product


def delete_product(product_id):
    """Удаляет товар вместе с историей цен. Товар, который уже продавался,
    удалить нельзя: иначе накладные потеряют ссылку на него."""
    product = session.get(Product, product_id)
    used = session.scalar(
        select(func.count())
        .select_from(InvoiceItem)
        .where(InvoiceItem.product_id == product_id)
    )
    if used:
        raise ValueError("Товар есть в накладных, удалить его нельзя")
    session.delete(product)  # история цен удалится каскадом
    _commit()


# ------------------------------------------------------------------- цены

def get_prices(product_id):
    return session.scalars(
        select(PriceHistory)
        .where(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.start_date)
    ).all()


def price_at(product_id, on_date):
    """Цена товара, действовавшая на указанную дату: последняя запись
    истории цен с датой начала не позже on_date. None, если цены нет."""
    return session.scalar(
        select(PriceHistory.price)
        .where(
            PriceHistory.product_id == product_id,
            PriceHistory.start_date <= on_date,
        )
        .order_by(PriceHistory.start_date.desc())
        .limit(1)
    )


def add_price(product_id, price, start_date):
    session.add(
        PriceHistory(product_id=product_id, price=price, start_date=start_date)
    )
    _commit()


def delete_price(price_id):
    session.delete(session.get(PriceHistory, price_id))
    _commit()


# -------------------------------------------------------------- накладные

def get_invoices(date_from=None, date_to=None):
    """Накладные за период; обе границы необязательны и включаются."""
    query = select(Invoice)
    if date_from:
        query = query.where(Invoice.doc_date >= date_from)
    if date_to:
        query = query.where(Invoice.doc_date <= date_to)
    return session.scalars(query.order_by(Invoice.doc_date.desc())).all()


def get_invoice(invoice_id):
    return session.get(Invoice, invoice_id)


def add_invoice(number, doc_date, buyer_id, city_id, items):
    """Проводит накладную со всеми позициями одной транзакцией.
    items — список кортежей (product_id, quantity, price)."""
    if not items:
        raise ValueError("Накладная должна содержать хотя бы одну позицию")
    invoice = Invoice(
        invoice_number=number,
        doc_date=doc_date,
        buyer_id=buyer_id,
        city_id=city_id,
    )
    for product_id, quantity, price in items:
        # позиции добавляются в коллекцию накладной, invoice_id
        # подставится автоматически при сохранении
        invoice.items.append(
            InvoiceItem(product_id=product_id, quantity=quantity, price=price)
        )
    session.add(invoice)
    _commit()  # накладная и позиции сохраняются вместе или не сохраняются вовсе
    return invoice


def update_invoice(invoice_id, number, doc_date, buyer_id, city_id, items):
    """Изменяет шапку накладной и полностью заменяет её позиции."""
    if not items:
        raise ValueError("Накладная должна содержать хотя бы одну позицию")
    invoice = session.get(Invoice, invoice_id)
    invoice.invoice_number = number
    invoice.doc_date = doc_date
    invoice.buyer_id = buyer_id
    invoice.city_id = city_id
    invoice.items.clear()  # старые позиции помечаются на удаление
    # flush выполняет удаление сразу, до вставки новых позиций,
    # иначе нарушится уникальность пары (invoice_id, product_id)
    session.flush()
    for product_id, quantity, price in items:
        invoice.items.append(
            InvoiceItem(product_id=product_id, quantity=quantity, price=price)
        )
    _commit()
    return invoice


def delete_invoice(invoice_id):
    session.delete(session.get(Invoice, invoice_id))  # позиции удалятся каскадом
    _commit()


# ----------------------------------------------------------------- отчёты

def top_buyers(day):
    """Покупатели, сделавшие покупку на максимальную сумму на дату.
    Возвращает кортежи (дата, название покупателя, адрес, сумма)."""
    # сумма покупки = сумма по всем позициям всех накладных покупателя за день
    total = func.sum(InvoiceItem.quantity * InvoiceItem.price)
    rows = session.execute(
        select(Buyer.buyer_name, Buyer.buyer_address, total)
        .join(Invoice, Invoice.buyer_id == Buyer.buyer_id)
        .join(InvoiceItem, InvoiceItem.invoice_id == Invoice.invoice_id)
        .where(Invoice.doc_date == day)
        .group_by(Buyer.buyer_id)  # по id: названия покупателей могут совпадать
        .order_by(total.desc())
    ).all()
    if not rows:
        return []
    best = rows[0][2]  # после сортировки максимум стоит первым
    # максимум могут набрать несколько покупателей, выводятся все
    return [
        (day, name, addr, round(float(s), 2))
        for name, addr, s in rows
        if s == best
    ]


def price_changes(product_id, date_from, date_to):
    """Изменения стоимости товара за период. Возвращает кортежи
    (предприятие-производитель, наименование товара, дата, стоимость)."""
    rows = session.execute(
        select(
            Manufacturer.manufacturer_name,
            Product.product_name,
            PriceHistory.start_date,
            PriceHistory.price,
        )
        .join(Product, Product.product_id == PriceHistory.product_id)
        .join(Manufacturer, Manufacturer.manufacturer_id == Product.manufacturer_id)
        .where(
            PriceHistory.product_id == product_id,
            PriceHistory.start_date >= date_from,
            PriceHistory.start_date <= date_to,
        )
        .order_by(PriceHistory.start_date)  # хронологический порядок
    ).all()
    return [(m, p, d, round(float(pr), 2)) for m, p, d, pr in rows]