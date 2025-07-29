from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="TRON Address Info Service",
    description="Microservice for getting TRON address information",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1", tags=["tron"])


@app.get("/")
async def root():
    return {"message": "TRON Address Info Service"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
