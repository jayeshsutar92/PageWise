from datetime import datetime

from sqlalchemy import Select, desc, select, tuple_
from sqlalchemy.orm import Session

from app.models.product import Product


ProductKey = tuple[datetime, int]


def get_high_watermark(session: Session, category: str | None) -> ProductKey | None:
    stmt = select(Product.updated_at, Product.id).order_by(
        desc(Product.updated_at),
        desc(Product.id),
    )
    if category:
        stmt = stmt.where(Product.category == category)
    row = session.execute(stmt.limit(1)).one_or_none()
    return (row.updated_at, row.id) if row else None


def list_products(
    session: Session,
    *,
    limit: int,
    category: str | None,
    after: ProductKey | None,
    fence: ProductKey,
) -> list[Product]:
    stmt: Select[tuple[Product]] = select(Product).where(
        tuple_(Product.updated_at, Product.id) <= fence,
    )
    if category:
        stmt = stmt.where(Product.category == category)
    if after:
        stmt = stmt.where(tuple_(Product.updated_at, Product.id) < after)

    stmt = stmt.order_by(desc(Product.updated_at), desc(Product.id)).limit(limit)
    return list(session.scalars(stmt).all())