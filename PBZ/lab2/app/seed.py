import random
from datetime import date, timedelta
from decimal import Decimal

from .base import SessionLocal, drop_db, init_db
from .models import (
    Bank,
    Buyer,
    Category,
    City,
    Country,
    Invoice,
    InvoiceItem,
    Manufacturer,
    PriceHistory,
    Product,
    Region,
)

random.seed(42)


def seed() -> None:
    drop_db()
    init_db()

    with SessionLocal() as s:
        cat_industrial = Category(category_name="Industrial")
        cat_household = Category(category_name="Household")
        cat_retail = Category(category_name="Retail equipment")
        categories = [cat_industrial, cat_household, cat_retail]

        m1 = Manufacturer(
            manufacturer_name='ОАО "Белпромтех"',
            manufacturer_address="г. Минск, ул. Промышленная, 12",
        )
        m2 = Manufacturer(
            manufacturer_name='ЗАО "Гомельмаш"',
            manufacturer_address="г. Гомель, пр. Победы, 45",
        )
        manufacturers = [m1, m2]

        specs = [
            ("PR-001", "Станок токарный ТС-16", "шт", cat_industrial, m1, "8400.00"),
            ("PR-002", "Компрессор КВ-200", "шт", cat_industrial, m1, "3250.00"),
            ("PR-003", "Насос центробежный НЦ-50", "шт", cat_industrial, m2, "1780.50"),
            ("PR-004", "Конвейер ленточный КЛ-8", "шт", cat_industrial, m2, "12600.00"),
            ("BT-001", "Чайник электрический ЧЭ-17", "шт", cat_household, m1, "45.90"),
            ("BT-002", "Мясорубка МЭ-300", "шт", cat_household, m1, "128.00"),
            ("BT-003", "Обогреватель масляный ОМ-9", "шт", cat_household, m2, "215.40"),
            ("BT-004", "Пылесос ПС-1600", "шт", cat_household, m2, "310.00"),
            ("TO-001", "Витрина холодильная ВХ-2.0", "шт", cat_retail, m1, "2450.00"),
            ("TO-002", "Стеллаж торговый СТ-4", "шт", cat_retail, m2, "185.30"),
            ("TO-003", "Касса-терминал КТ-11", "шт", cat_retail, m2, "1120.00"),
            ("TO-004", "Тележка покупательская ТП-90", "шт", cat_retail, m1, "96.70"),
        ]

        products = []
        price_rows = []
        base_day = date(2025, 1, 10)

        for code, name, unit, cat, man, start_price in specs:
            p = Product(
                product_code=code,
                product_name=name,
                product_unit=unit,
                category=cat,
                manufacturer=man,
            )
            products.append(p)

            price = Decimal(start_price)
            day = base_day
            for _ in range(random.randint(3, 5)):
                price_rows.append(PriceHistory(product=p, price=price, start_date=day))
                factor = Decimal(str(round(random.uniform(1.02, 1.12), 3)))
                price = (price * factor).quantize(Decimal("0.01"))
                day += timedelta(days=random.randint(40, 90))

        belarus = Country(country_name="Беларусь", country_kind="BY")
        russia = Country(country_name="Россия", country_kind="near")
        kazakhstan = Country(country_name="Казахстан", country_kind="near")
        poland = Country(country_name="Польша", country_kind="far")
        germany = Country(country_name="Германия", country_kind="far")
        countries = [belarus, russia, kazakhstan, poland, germany]

        regions_by_name = {}
        for rname in [
            "Минская область",
            "Гомельская область",
            "Брестская область",
            "Витебская область",
            "Гродненская область",
            "Могилёвская область",
        ]:
            regions_by_name[rname] = Region(region_name=rname, country=belarus)

        moscow_region = Region(region_name="Московская область", country=russia)
        regions = list(regions_by_name.values()) + [moscow_region]

        cities = [
            City(city_name="Минск", region=regions_by_name["Минская область"], country=belarus),
            City(city_name="Борисов", region=regions_by_name["Минская область"], country=belarus),
            City(city_name="Гомель", region=regions_by_name["Гомельская область"], country=belarus),
            City(city_name="Мозырь", region=regions_by_name["Гомельская область"], country=belarus),
            City(city_name="Брест", region=regions_by_name["Брестская область"], country=belarus),
            City(city_name="Витебск", region=regions_by_name["Витебская область"], country=belarus),
            City(city_name="Гродно", region=regions_by_name["Гродненская область"], country=belarus),
            City(city_name="Могилёв", region=regions_by_name["Могилёвская область"], country=belarus),
            City(city_name="Москва", region=moscow_region, country=russia),
            City(city_name="Алматы", region=None, country=kazakhstan),
            City(city_name="Варшава", region=None, country=poland),
            City(city_name="Берлин", region=None, country=germany),
        ]

        b1 = Bank(bank_name='ОАО "Приорбанк"', bank_code="PJCBBY2X")
        b2 = Bank(bank_name='ОАО "Белагропромбанк"', bank_code="BAPBBY2X")
        b3 = Bank(bank_name='ОАО "БПС-Сбербанк"', bank_code="BPSBBY2X")
        banks = [b1, b2, b3]

        buyers = [
            Buyer(
                buyer_type="legal",
                buyer_name='ООО "ТоргСервис"',
                buyer_address="г. Минск, ул. Кальварийская, 24",
                bank=b1,
                account="BY13NBRB30120000000000000001",
            ),
            Buyer(
                buyer_type="legal",
                buyer_name='ЗАО "СтройМаркет"',
                buyer_address="г. Гомель, ул. Советская, 7",
                bank=b2,
                account="BY13NBRB30120000000000000002",
            ),
            Buyer(
                buyer_type="legal",
                buyer_name='ИООО "ЕвроТрейд"',
                buyer_address="г. Брест, б-р Шевченко, 3",
                bank=b3,
                account="BY13NBRB30120000000000000003",
            ),
            Buyer(
                buyer_type="legal",
                buyer_name='ООО "Восток-Импорт"',
                buyer_address="г. Москва, Ленинский пр-т, 90",
                bank=b1,
                account="BY13NBRB30120000000000000004",
            ),
            Buyer(
                buyer_type="natural",
                buyer_name="Иванов Иван Иванович",
                buyer_address="г. Минск, ул. Одоевского, 15-42",
                doc_series="МР",
                doc_number="1234567",
            ),
            Buyer(
                buyer_type="natural",
                buyer_name="Петрова Анна Сергеевна",
                buyer_address="г. Витебск, ул. Ленина, 8-11",
                doc_series="КН",
                doc_number="7654321",
            ),
            Buyer(
                buyer_type="natural",
                buyer_name="Сидорчук Павел Олегович",
                buyer_address="г. Гродно, ул. Горького, 51-3",
                doc_series="МС",
                doc_number="9988776",
            ),
        ]

        s.add_all(categories + manufacturers + products + price_rows)
        s.add_all(countries + regions + cities + banks + buyers)
        s.flush()

        def price_at(product: Product, on: date) -> Decimal:
            rows = [r for r in product.price_histories if r.start_date <= on]
            if not rows:
                return min(product.price_histories, key=lambda r: r.start_date).price
            return max(rows, key=lambda r: r.start_date).price

        invoices = []
        start = date(2025, 3, 1)
        for n in range(1, 41):
            doc_date = start + timedelta(days=random.randint(0, 300))
            inv = Invoice(
                invoice_number=f"ТН-{n:04d}",
                doc_date=doc_date,
                buyer=random.choice(buyers),
                city=random.choice(cities),
            )
            for prod in random.sample(products, random.randint(1, 4)):
                inv.items.append(
                    InvoiceItem(
                        product=prod,
                        quantity=Decimal(random.randint(1, 20)),
                        price=price_at(prod, doc_date),
                    )
                )
            invoices.append(inv)

        s.add_all(invoices)
        s.commit()

        print(f"категорий: {len(categories)}")
        print(f"производителей: {len(manufacturers)}")
        print(f"товаров: {len(products)}")
        print(f"записей истории цен: {len(price_rows)}")
        print(f"стран: {len(countries)}")
        print(f"регионов: {len(regions)}")
        print(f"городов: {len(cities)}")
        print(f"банков: {len(banks)}")
        print(f"покупателей: {len(buyers)}")
        print(f"накладных: {len(invoices)}")


if __name__ == "__main__":
    seed()