# TRON Address Info Microservice

A FastAPI-based microservice for retrieving TRON blockchain address information including bandwidth, energy, and TRX balance. All requests are automatically logged to a PostgreSQL database with pagination support.

## 🚀 Features

- **Address Information Retrieval**: Get bandwidth, energy, and TRX balance for any TRON address
- **Request Logging**: Automatically saves all requests to PostgreSQL database
- **Pagination**: Browse historical requests with configurable page size
- **Docker Support**: Full containerization with Docker Compose
- **Nginx Proxy**: Production-ready reverse proxy setup
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Health Checks**: Built-in health monitoring endpoints
- **TRON Network Status**: Real-time connection status to TRON network

## 🛠 Tech Stack

- **Backend**: FastAPI with Python 3.11
- **Database**: PostgreSQL 15 with SQLModel (SQLAlchemy + Pydantic)
- **Blockchain**: TronPy for TRON network interaction
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx reverse proxy
- **Testing**: Pytest with async support
- **Environment**: Python-dotenv for configuration

## 📁 Project Structure

```
tron-microservice/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models.py               # SQLModel database models
│   ├── database.py             # Database configuration
│   ├── config.py               # Settings and environment variables
│   ├── services/
│   │   ├── __init__.py
│   │   └── tron_service.py     # TRON blockchain interaction
│   └── api/
│       ├── __init__.py
│       └── endpoints.py        # API route definitions
├── tests/
│   ├── __init__.py
│   ├── test_integration.py     # Integration tests
│   └── test_unit.py           # Unit tests
├── docker-compose.yml          # Multi-container configuration
├── Dockerfile                  # Application container
├── nginx.conf                  # Nginx configuration
├── requirements.txt            # Python dependencies
├── pytest.ini                 # Test configuration
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🏗 Installation & Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tron-microservice
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file if needed
   ```

3. **Start services**
   ```bash
   docker-compose up --build -d
   ```

4. **Verify installation**
   ```bash
   curl http://localhost/health
   curl http://localhost/api/v1/tron-status
   ```

The service will be available at:
- **API**: http://localhost
- **API Documentation**: http://localhost/docs
- **Health Check**: http://localhost/health

### Local Development

For development without Docker:

1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup local database**
   ```bash
   # Install PostgreSQL or use SQLite
   echo "DATABASE_URL=sqlite:///./tron_service.db" > .env
   ```

3. **Run application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📖 API Documentation

### Base URL
- **Production**: `http://localhost/api/v1`
- **Development**: `http://localhost:8000/api/v1`

### Endpoints

#### 1. Get Address Information
Retrieve bandwidth, energy, and TRX balance for a TRON address.

**POST** `/address-info`

**Request Body:**
```json
{
  "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
}
```

**Response:**
```json
{
  "id": 1,
  "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "bandwidth": 5000,
  "energy": 50000,
  "trx_balance": 1000.123456,
  "requested_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid TRON address format
- `500`: Internal server error or TRON network issue

#### 2. Get Request History
Retrieve paginated list of previous address requests.

**GET** `/requests?page=1&size=10`

**Query Parameters:**
- `page` (integer, default: 1): Page number
- `size` (integer, default: 10, max: 100): Items per page

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
      "bandwidth": 5000,
      "energy": 50000,
      "trx_balance": 1000.123456,
      "requested_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

#### 3. Check TRON Network Status
Verify connection to TRON network and get network information.

**GET** `/tron-status`

**Response:**
```json
{
  "status": "connected",
  "network": "4.7.4",
  "test_data": {
    "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
    "bandwidth": 5000,
    "energy": 50000,
    "trx_balance": 1000.123456
  }
}
```

#### 4. Health Check Endpoints

**GET** `/health`
```json
{
  "status": "healthy"
}
```

**GET** `/` (Root)
```json
{
  "message": "TRON Address Info Service"
}
```

### cURL Examples

```bash
# Check service health
curl http://localhost/health

# Check TRON network connection
curl http://localhost/api/v1/tron-status

# Get address information
curl -X POST "http://localhost/api/v1/address-info" \
     -H "Content-Type: application/json" \
     -d '{"address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"}'

# Get request history (first page, 5 items)
curl "http://localhost/api/v1/requests?page=1&size=5"

# Get second page
curl "http://localhost/api/v1/requests?page=2&size=10"
```

## 🧪 Testing

### Running Tests

**With Docker:**
```bash
# All tests
docker-compose exec app pytest

# Specific test file
docker-compose exec app pytest tests/test_integration.py -v

# With coverage
docker-compose exec app pytest --cov=app tests/
```

**Local Development:**
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_unit.py::test_create_tron_address_request
```

### Test Coverage

The project includes comprehensive testing:

- **Unit Tests**: Database operations, model validation
- **Integration Tests**: API endpoints, request/response flow
- **Mocking**: TRON service calls for reliable testing
- **Fixtures**: Database setup and cleanup

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@db:5432/tron_service

# TRON Network Configuration
TRON_NETWORK=mainnet  # or 'testnet' for testing

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### TRON Network Options

- **mainnet**: Production TRON network (default)
- **testnet**: TRON Shasta testnet for development

### Database Configuration

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://username:password@host:port/database
```

**SQLite (Development):**
```env
DATABASE_URL=sqlite:///./tron_service.db
```

## 🚀 Deployment

### Docker Compose (Recommended)

The included `docker-compose.yml` provides a complete production setup:

- **App Container**: FastAPI application
- **PostgreSQL**: Database with persistent volume
- **Nginx**: Reverse proxy with load balancing

```bash
# Production deployment
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Scale application (if needed)
docker-compose up -d --scale app=3
```

### Manual Deployment

1. **Build application image**
   ```bash
   docker build -t tron-microservice .
   ```

2. **Run with external database**
   ```bash
   docker run -d \
     --name tron-app \
     -p 8000:8000 \
     -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
     tron-microservice
   ```

### Kubernetes

Example Kubernetes deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tron-microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tron-microservice
  template:
    metadata:
      labels:
        app: tron-microservice
    spec:
      containers:
      - name: app
        image: tron-microservice:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: tron-secrets
              key: database-url
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Docker Connection Errors
```
Error: unable to get image 'postgres:15'
```

**Solution:**
- Ensure Docker Desktop is running
- Check internet connectivity
- Try `docker compose up` instead of `docker-compose up`

#### 2. Database Connection Failed
```
Error: could not connect to database
```

**Solution:**
- Verify DATABASE_URL in `.env`
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check database logs: `docker-compose logs db`

#### 3. TRON Network Timeout
```
Error: Error getting TRON data: timeout
```

**Solution:**
- Check internet connectivity
- Verify TRON network status at https://tronscan.org
- Try switching to testnet: `TRON_NETWORK=testnet`

#### 4. Import Errors in Tests
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
- Run tests from project root directory
- Use pytest instead of direct Python execution
- Ensure `__init__.py` files exist in all directories

### Debugging

**View application logs:**
```bash
docker-compose logs -f app
```

**Access container shell:**
```bash
docker-compose exec app bash
```

**Database inspection:**
```bash
docker-compose exec db psql -U postgres -d tron_service
```

## 📊 Monitoring & Performance

### Health Monitoring

The service provides several monitoring endpoints:

- `/health`: Basic health check
- `/api/v1/tron-status`: TRON network connectivity
- Database connection is verified on startup

### Performance Considerations

- **Database Indexing**: Address field is indexed for fast queries
- **Connection Pooling**: SQLAlchemy manages database connections
- **Async Operations**: TRON API calls are async for better throughput
- **Nginx Caching**: Can be configured for static responses

### Scaling

For high-traffic scenarios:

1. **Horizontal Scaling**: Run multiple app containers
2. **Database Optimization**: Use connection pooling, read replicas
3. **Caching**: Implement Redis for frequently requested addresses
4. **Load Balancing**: Nginx handles multiple backend instances

## 🛡 Security

### Best Practices Implemented

- **Non-root User**: Application runs as non-privileged user
- **Environment Variables**: Secrets stored in `.env` files
- **Input Validation**: TRON address format validation
- **Error Handling**: Sanitized error responses
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

### Additional Security Measures

For production deployment:

- **HTTPS**: Use TLS certificates with Nginx
- **Rate Limiting**: Implement request rate limiting
- **Authentication**: Add API key authentication if needed
- **Monitoring**: Log suspicious activity patterns

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make changes and test**
   ```bash
   pytest
   ```

5. **Submit pull request**

### Code Standards

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations throughout
- **Documentation**: Comment complex business logic
- **Testing**: Maintain test coverage above 80%

### Pull Request Process

1. Ensure all tests pass
2. Update documentation for new features
3. Follow commit message conventions
4. Request review from maintainers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🆘 Support

### Getting Help

- **Documentation**: Check this README and `/docs` endpoint
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join discussions in GitHub Discussions

### TRON Address Examples

For testing, use these known TRON addresses:

- `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` - Binance Hot Wallet (USDT)
- `TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH` - Justin Sun's address
- `TMuA6YqfCeX8EhbfYEg5y7S4DqzSJireY9` - TRON Foundation

### Useful Links

- [TRON Documentation](https://developers.tron.network/)
- [TronPy Library](https://github.com/andelf/tronpy)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

---

**Built with ❤️ using FastAPI, SQLModel, and TronPy**