"""Application configuration settings."""
from functools import lru_cache
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Info
    app_name: str = "Aegis-JKN MHGSL Fraud Intelligence API"
    app_version: str = "1.0.0"
    app_description: str = (
        "Multi-Hospital Graph-based Suspicious Claim Detection "
        "for JKN (Jaminan Kesehatan Nasional) Fraud Intelligence"
    )

    # Environment
    environment: str = Field(default="development", description="Environment: development, staging, production")
    debug: bool = Field(default=True, description="Debug mode")

    # API
    api_prefix: str = "/api"
    api_v1_prefix: str = "/api/v1"

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8010"],
        description="Allowed CORS origins"
    )
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = Field(default=["*"])
    cors_allow_headers: List[str] = Field(default=["*"])

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./aegis_jkn.db",
        description="Database connection URL"
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis (for caching/sessions)
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")

    # Qdrant Vector Database
    qdrant_url: Optional[str] = Field(default=None, description="Qdrant connection URL")
    qdrant_api_key: Optional[str] = Field(default=None, description="Qdrant API key")
    qdrant_timeout: int = Field(default=30, description="Qdrant connection timeout in seconds")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")

    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT/signing"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Requests per minute")
    rate_limit_window_seconds: int = 60

    # Simulation Settings
    simulation_default_iterations: int = 1000
    simulation_max_iterations: int = 10000
    simulation_timeout_seconds: int = 300

    # Graph Analysis
    graph_max_depth: int = 3
    graph_max_nodes: int = 1000
    graph_community_resolution: float = 1.0

    # 9router AI Reporting & Clinical Reasoning
    router_base_url: str = Field(default="https://9router.biezz.my.id/v1", description="9router base URL")
    router_api_key: str = Field(default="", description="9router API key")
    reporting_model_name: str = Field(default="aegis-jkn", description="Designated reporting model")

    # Embedding Models Configuration
    embedding_api_key: str = Field(default="", description="Embedding API Key")
    embedding_model_name: str = Field(default="openrouter/openai/text-embedding-3-large", description="Primary embedding model")
    embedding_fallback_model: str = Field(default="openrouter/nvidia/llama-nemotron-embed-vl-1b-v2:free", description="Fallback embedding model")
    embedding_endpoint: str = Field(default="https://9router.biezz.my.id/v1/embeddings", description="Embedding endpoint")

    # MHGSL Mathematical Hyperparameters (Heliyon 2024 Paper)
    mhgsl_alpha: float = Field(default=0.0001, description="Discrepancy loss coefficient alpha")
    mhgsl_beta: float = Field(default=0.5, description="Consistency loss coefficient beta")
    mhgsl_knn_k: int = Field(default=4, description="KNN k neighbors for cosine feature graph")

    # Self-Hosted Supabase / External DB
    supabase_url: Optional[str] = Field(default=None, description="Supabase URL")
    supabase_anon_key: Optional[str] = Field(default=None, description="Supabase Anon Key")

    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()