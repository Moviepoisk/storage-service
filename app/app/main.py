from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from miniopy_async import Minio
import aiohttp

from app.core.config import settings
from app.infrastructure.redis import redis
from app.api.v1.api import api_router
from app.infrastructure.s3 import minio

app = FastAPI(
    title='Movies Storage',
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    minio.minio_client = Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
    )
    minio.client_session = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await minio.client_session.close()


app.include_router(api_router, prefix="/api/v1")
