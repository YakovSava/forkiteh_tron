from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class TronAddressRequest(SQLModel, table=True):
    __tablename__ = "tron_address_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(index=True)
    bandwidth: int
    energy: int
    trx_balance: Decimal = Field(decimal_places=6)
    requested_at: datetime = Field(default_factory=datetime.utcnow)


class TronAddressRequestCreate(SQLModel):
    address: str


class TronAddressResponse(SQLModel):
    id: int
    address: str
    bandwidth: int
    energy: int
    trx_balance: Decimal
    requested_at: datetime


class PaginatedResponse(SQLModel):
    items: list[TronAddressResponse]
    total: int
    page: int
    size: int
    pages: int
