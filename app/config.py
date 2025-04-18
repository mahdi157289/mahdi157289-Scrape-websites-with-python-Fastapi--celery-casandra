from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    astra_db_client_id: str = Field(..., alias="ASTRA_DB_CLIENT_ID")
    astra_db_client_secret: str = Field(..., alias="ASTRA_DB_CLIENT_SECRET")
    astra_db_application_token: str = Field(..., alias="ASTRA_DB_APPLICATION_TOKEN")
    cqleng_allow_schema_management: str = Field("1", alias="CQLENG_ALLOW_SCHEMA_MANAGEMENT")
    proj_name: str = Field("FASTAPIAstraDB", alias="PROJ_Name")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # Allows PROJ_Name and PROJ_name
    )

@lru_cache
def get_settings():
    return Settings()
