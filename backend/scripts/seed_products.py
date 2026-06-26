from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from faker import Faker
from sqlalchemy import delete, insert

from app.db.session import SessionLocal
from app.models.product import Product

TOTAL_PRODUCTS = 200_000
BATCH_SIZE = 10_000
CATEGORIES = [
    "Books",
    "Clothing",
    "Electronics",
    "Grocery",
    "Health",
    "Home",
    "Outdoors",
    "Toys",
]


def batched_products(fake: Faker, size: int) -> list[dict[str, object]]:
    now = datetime.now(UTC)
    rows: list[dict[str, object]] = []
    for _ in range(size):
        created_at = now - timedelta(days=random.randint(0, 730), seconds=random.randint(0, 86_400))
        updated_at = created_at + timedelta(days=random.randint(0, 90), seconds=random.randint(0, 86_400))
        rows.append(
            {
                "name": f"{fake.word().title()} {fake.word().title()} {fake.random_int(1000, 9999)}",
                "category": random.choice(CATEGORIES),
                "price": Decimal(random.randrange(199, 250_000)) / Decimal("100"),
                "created_at": created_at,
                "updated_at": min(updated_at, now),
            }
        )
    return rows


def main() -> None:
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    with SessionLocal() as session:
        session.execute(delete(Product))
        session.commit()

        inserted = 0
        while inserted < TOTAL_PRODUCTS:
            batch_size = min(BATCH_SIZE, TOTAL_PRODUCTS - inserted)
            session.execute(insert(Product), batched_products(fake, batch_size))
            session.commit()
            inserted += batch_size
            print(f"Inserted {inserted:,}/{TOTAL_PRODUCTS:,} products")


if __name__ == "__main__":
    main()