from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    PaginatedResponse,
    TronAddressRequest,
    TronAddressRequestCreate,
    TronAddressResponse,
)
from app.services.tron_service import tron_service

router = APIRouter()


@router.post("/address-info", response_model=TronAddressResponse)
async def get_address_info(
    request: TronAddressRequestCreate, session: Session = Depends(get_session)
):
    try:
        if (
            not request.address
            or len(request.address) != 34
            or not request.address.startswith("T")
        ):
            raise HTTPException(status_code=400, detail="Invalid TRON address format")

        tron_data = await tron_service.get_address_info(request.address)

        db_request = TronAddressRequest(
            address=request.address,
            bandwidth=tron_data["bandwidth"],
            energy=tron_data["energy"],
            trx_balance=tron_data["trx_balance"],
        )

        session.add(db_request)
        session.commit()
        session.refresh(db_request)

        return TronAddressResponse.model_validate(db_request)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/requests", response_model=PaginatedResponse)
async def get_requests(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    session: Session = Depends(get_session),
):
    try:
        total_query = select(TronAddressRequest)
        total = len(session.exec(total_query).all())

        offset = (page - 1) * size
        query = (
            select(TronAddressRequest)
            .order_by(TronAddressRequest.requested_at.desc())
            .offset(offset)
            .limit(size)
        )

        requests = session.exec(query).all()

        items = [TronAddressResponse.model_validate(req) for req in requests]

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=ceil(total / size) if total > 0 else 0,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
