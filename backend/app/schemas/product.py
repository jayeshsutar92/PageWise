from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductsResponse(BaseModel):
    products: list[ProductOut]
    next_cursor: str | None = Field(default=None)

