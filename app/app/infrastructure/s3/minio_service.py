from fastapi import UploadFile
from miniopy_async import Minio
import io
from uuid import uuid4
from datetime import timedelta
import shortuuid
from aiohttp import ClientSession

from app.schemas.file import S3FileResult


class MinioStorage:
    def __init__(self, minio_client: Minio, session_client: ClientSession):
        self.client = minio_client
        self.client_session = session_client

    async def generate_short_name(self, file_name):
        return shortuuid.uuid(name=file_name)

    async def get_presigned_url(self, bucket: str, path: str) -> str:
        return await self.client.get_presigned_url('GET', bucket, path, expires=timedelta(days=1),)

    async def save(self, file: UploadFile) -> S3FileResult | None:
        bucket_name = "movies"

        # Генерируем уникальный идентификатор для файла и добавляем его к имени файла
        unique_id = str(uuid4())
        destination_file = f"{file.filename}{unique_id}"

        found = await self.client.bucket_exists(bucket_name)
        if not found:
            await self.client.make_bucket(bucket_name)
            print(f"Created bucket {bucket_name}")
        else:
            print(f"Bucket {bucket_name} already exists")

        file_content = await file.read()
        file_content_stream = io.BytesIO(file_content)

        # Загружаем файл
        try:
            await self.client.put_object(
                bucket_name=bucket_name,
                object_name=destination_file,
                content_type=file.content_type,
                data=file_content_stream,
                length=-1, part_size=10 * 1024 * 1024,
            )
        except Exception:
            return None
        finally:
            file_content_stream.close()

        short_name = await self.generate_short_name(destination_file)
        # статистика по загруженному файлу
        stat = await self.client.stat_object(bucket_name, destination_file)

        # Возвращаем расширенную информацию о файле
        result = S3FileResult(
            path_in_storage=f"{bucket_name}/{destination_file}",
            filename=file.filename,
            size=stat.size,
            file_type=file.content_type,
            short_name=short_name,
        )

        return result

    async def get_file_stream(self, bucket: str, path: str):
        try:
            # Получаем объект из Minio
            response = await self.client.get_object(bucket, path, session=self.client_session)
            # Возвращаем асинхронный генератор, который будет читать и возвращать содержимое файла
            async def streamer():
                async for chunk in response.stream(32 * 1024):
                    yield chunk
            return streamer
        except Exception as err:
            print(f"Ошибка при получении файла из Minio: {err}")
            return None