from aiohttp import ClientSession
from miniopy_async import Minio

minio_client: Minio | None = None
client_session: ClientSession | None = None


def get_minio() -> Minio | None:
    return minio_client


def get_client_session() -> ClientSession:
    return client_session or ClientSession()


