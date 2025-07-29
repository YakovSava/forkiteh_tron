from datetime import datetime
from decimal import Decimal

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.models import TronAddressRequest


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={
            "check_same_thread": False
        },
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


def test_create_tron_address_request(session: Session):
    test_address = "TTest123456789012345678901234567890"
    test_bandwidth = 1000
    test_energy = 2000
    test_balance = Decimal("100.123456")

    db_request = TronAddressRequest(
        address=test_address,
        bandwidth=test_bandwidth,
        energy=test_energy,
        trx_balance=test_balance
    )

    session.add(db_request)
    session.commit()
    session.refresh(db_request)

    assert db_request.id is not None
    assert db_request.address == test_address
    assert db_request.bandwidth == test_bandwidth
    assert db_request.energy == test_energy
    assert db_request.trx_balance == test_balance
    assert isinstance(db_request.requested_at, datetime)


def test_tron_address_request_validation():
    valid_request = TronAddressRequest(
        address="TTest123456789012345678901234567890",
        bandwidth=1000,
        energy=2000,
        trx_balance=Decimal("100.123456")
    )
    assert valid_request.address == "TTest123456789012345678901234567890"

    request_with_decimal = TronAddressRequest(
        address="TTest123456789012345678901234567890",
        bandwidth=1000,
        energy=2000,
        trx_balance=Decimal("100.123456789")
    )
    assert request_with_decimal.trx_balance == Decimal("100.123456789")


def test_model_validation_negative_values():
    request_with_zero = TronAddressRequest(
        address="TTest123456789012345678901234567890",
        bandwidth=0,
        energy=0,
        trx_balance=Decimal("0.0")
    )
    assert request_with_zero.bandwidth == 0
    assert request_with_zero.energy == 0
    assert request_with_zero.trx_balance == Decimal("0.0")