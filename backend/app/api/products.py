from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.products import get_high_watermark, list_products
from app.schemas.product import ProductsResponse
from app.services.cursor import CursorPayload, decode_cursor, encode_cursor

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductsResponse)
def get_products(
    limit: int = Query(default=50, ge=1, le=100),
    cursor: str | None = Query(default=None),
    category: str | None = Query(default=None, min_length=1, max_length=80),
    session: Session = Depends(get_session),
) -> ProductsResponse:
    if cursor:
        payload = decode_cursor(cursor)
        if payload.category != category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cursor does not match the requested category filter.",
            )
        fence = (payload.fence_updated_at, payload.fence_id)
        after = (payload.last_updated_at, payload.last_id)
    else:
        high_watermark = get_high_watermark(session, category)
        if high_watermark is None:
            return ProductsResponse(products=[], next_cursor=None)
        fence = high_watermark
        after = None

    products = list_products(
        session,
        limit=limit + 1,
        category=category,
        after=after,
        fence=fence,
    )
    page = products[:limit]
    next_cursor = None

    if len(products) > limit and page:
        last = page[-1]
        next_cursor = encode_cursor(
            CursorPayload(
                last_updated_at=last.updated_at,
                last_id=last.id,
                fence_updated_at=fence[0],
                fence_id=fence[1],
                category=category,
            )
        )

    return ProductsResponse(products=page, next_cursor=next_cursor)

