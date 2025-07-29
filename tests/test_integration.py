from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_address_info_endpoint(client):
    mock_tron_data = {"bandwidth": 1500, "energy": 2500, "trx_balance": 150.5}

    with patch(
        "app.api.endpoints.tron_service.get_address_info", new_callable=AsyncMock
    ) as mock_service:
        mock_service.return_value = mock_tron_data

        test_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

        response = client.post("/api/v1/address-info", json={"address": test_address})

        assert response.status_code == 200
        data = response.json()

        assert data["address"] == test_address
        assert data["bandwidth"] == 1500
        assert data["energy"] == 2500
        assert float(data["trx_balance"]) == 150.5
        assert "id" in data
        assert "requested_at" in data

        mock_service.assert_called_once_with(test_address)


def test_get_address_info_invalid_address(client):
    response = client.post("/api/v1/address-info", json={"address": "invalid_address"})

    assert response.status_code == 400
    assert "Invalid TRON address format" in response.json()["detail"]


def test_get_requests_endpoint(client, session):
    from app.models import TronAddressRequest

    test_requests = [
        TronAddressRequest(
            address=f"TTest{i:030d}",
            bandwidth=1000 + i,
            energy=2000 + i,
            trx_balance=Decimal(f"{100 + i}.123456"),
        )
        for i in range(15)
    ]

    for req in test_requests:
        session.add(req)
    session.commit()

    response = client.get("/api/v1/requests?page=1&size=10")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 15
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["pages"] == 2
    assert len(data["items"]) == 10

    items = data["items"]
    for i in range(len(items) - 1):
        assert items[i]["requested_at"] >= items[i + 1]["requested_at"]


def test_get_requests_pagination(client, session):
    from app.models import TronAddressRequest

    for i in range(5):
        req = TronAddressRequest(
            address=f"TTest{i:030d}",
            bandwidth=1000,
            energy=2000,
            trx_balance=Decimal("100.0"),
        )
        session.add(req)
    session.commit()

    response = client.get("/api/v1/requests?page=2&size=3")

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["size"] == 3
    assert len(data["items"]) == 2


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "TRON Address Info Service" in response.json()["message"]
