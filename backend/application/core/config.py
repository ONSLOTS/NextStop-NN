from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class QdrantSettings(BaseModel):
    """Qdrant config"""
    host: str = Field('localhost', env='QDRANT_HOST')
    port: int = Field(6333, env='QDRANT_PORT')
    collection: str = Field('nn_places', env='QDRANT_COLLECTION')
    vector_size: int = Field(1536, env='VECTOR_SIZE')
        
    @property
    def connection_string(self) -> str:
        return f'http://{self.host}:{self.port}'

class Settings(BaseSettings):
    qdrant: QdrantSettings = QdrantSettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
