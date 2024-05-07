from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_host: str = Field('storage-db', env="STORAGE_DATABASE_HOST")
    db_port: int = Field('5432', env="STORAGE_DATABASE_PORT")
    db_user: str = Field('devuser', env="STORAGE_DATABASE_USER")
    db_password: str = Field('changeme', env="STORAGE_DATABASE_PASSWORD")
    db_name: str = Field('devdb', env="STORAGE_DATABASE_NAME")
    minio_endpoint: str = 'minio:9000'
    minio_access_key: str = ...
    minio_secret_key: str = ...
    minio_bucket_name: str = 'movies'

    @property
    def database_url(self) -> str:
        return (f"postgresql://{self.db_user}:"
                f"{self.db_password}@{self.db_host}:"
                f"{self.db_port}/{self.db_name}")

    @property
    def database_url_async(self) -> str:
        return (f"postgresql+asyncpg://{self.db_user}:"
                f"{self.db_password}@{self.db_host}:"
                f"{self.db_port}/{self.db_name}")

    class Config:
        env_file = "../../.env"


settings = Settings()
