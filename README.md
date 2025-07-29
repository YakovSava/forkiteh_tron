# TRON Address Info Microservice

Microservice for getting TRON address information with request logging.

## Features

- **POST /api/v1/address-info** - get TRON address info (bandwidth, energy, TRX balance)
- **GET /api/v1/requests** - get requests history with pagination
- Automatic request logging to PostgreSQL
- Docker-compose deployment
- Nginx reverse proxy

## Tech Stack

- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL
- TronPy
- Docker & Docker Compose
- Nginx
- Pytest

## Quick Start

1. Copy environment file:
```bash
cp .env.example .env
```

2. Start services:
```bash
docker-compose up --build
```

3. Service available at: http://localhost
4. API docs: http://localhost/docs

## Testing

```bash
pip install -r requirements.txt
pytest
```

## API Examples

### Get address info
```bash
curl -X POST "http://localhost/api/v1/address-info" \
     -H "Content-Type: application/json" \
     -d '{"address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"}'
```

### Get requests history
```bash
curl "http://localhost/api/v1/requests?page=1&size=10"
```

## Response Format

### Address Info Response
```json
{
  "id": 1,
  "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "bandwidth": 1500,
  "energy": 25000,
  "trx_balance": 100.123456,
  "requested_at": "2024-01-15T10:30:00"
}
```

### Paginated Response
```json
{
  "items": [...],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```