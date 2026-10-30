"""Application configuration loaded from environment variables for NOVA."""

import os
from functools import lru_cache
from typing import Optional
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """NOVA system configuration settings."""

    # Product Identity
    app_name: str = Field(
        "NOVA",
        validation_alias=AliasChoices("nova_app_name", "app_name", "axio_app_name"),
    )
    product_name: str = "NOVA"
    product_full_name: str = "NOVA – Personal AI Operating System"
    tagline: str = "Think. Remember. Orchestrate. Execute."
    environment: str = Field(
        "development",
        validation_alias=AliasChoices("nova_env", "environment", "env", "axio_env"),
    )
    host: str = Field("127.0.0.1", validation_alias=AliasChoices("nova_host", "host", "axio_host"))
    port: int = Field(8000, validation_alias=AliasChoices("nova_port", "port", "axio_port"))
    log_level: str = Field("INFO", validation_alias=AliasChoices("log_level", "nova_log_level", "axio_log_level"))

    # Persistence
    database_url: str = Field(
        "sqlite:///./nova.db",
        validation_alias=AliasChoices("database_url", "nova_database_url", "axio_database_url"),
    )
    redis_url: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("redis_url", "nova_redis_url"),
    )

    # Nebius Token Factory & NVIDIA Nemotron Configuration
    nebius_api_key: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("nebius_api_key", "NEBIUS_API_KEY"),
    )
    nebius_base_url: str = Field(
        "https://api.studio.nebius.ai/v1",
        validation_alias=AliasChoices("nebius_base_url", "NEBIUS_BASE_URL"),
    )
    nebius_model_lightning: str = Field(
        "nvidia/nemotron-mini-4b-instruct",
        validation_alias=AliasChoices("nebius_model_lightning", "NEBIUS_MODEL_LIGHTNING"),
    )
    nebius_model_super: str = Field(
        "nvidia/llama-3.1-nemotron-70b-instruct",
        validation_alias=AliasChoices("nebius_model_super", "NEBIUS_MODEL_SUPER"),
    )

    # Tavily Web Research
    tavily_api_key: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("tavily_api_key", "TAVILY_API_KEY"),
    )

    # MCP Server
    mcp_server_name: str = Field(
    	"nova",
    	validation_alias=AliasChoices("mcp_server_name", "nova_mcp_server_name", "axio_mcp_server_name"),
    )

    mcp_server_version: str = Field(
    	"2.0.0",
    	validation_alias=AliasChoices("mcp_server_version", "nova_mcp_server_version", "axio_mcp_server_version"),
    )
    mcp_mount_path: str = Field(
        "/mcp",
        validation_alias=AliasChoices("mcp_mount_path", "nova_mcp_mount_path", "axio_mcp_mount_path"),
    )

    # Model Execution Controls
    llm_timeout_seconds: float = 30.0
    llm_max_retries: int = 3
    mock_llm_if_no_key: bool = True  # Allows offline and CI test execution with realistic simulated Nemotron responses

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
