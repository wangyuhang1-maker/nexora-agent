"""Application settings loaded from environment variables / .env."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """Runtime configuration.

    Field names map to upper-case environment variables, e.g. ``app_port`` -> ``APP_PORT``.
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ----- 应用 -----
    app_name: str = "nexora-agent-backend"
    app_version: str = "0.1.0"
    app_env: str = "dev"
    debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 9082
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # ----- 数据库 -----
    mysql_dsn: str = (
        "mysql+aiomysql://root:root@127.0.0.1:3306/nexora_agent?charset=utf8mb4"
    )
    pg_dsn: str = (
        "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/nexora_agent_pgvector"
    )

    # ----- Redis -----
    redis_url: str = "redis://127.0.0.1:6379/0"

    # ----- Kafka -----
    kafka_bootstrap_servers: str = "127.0.0.1:9092"
    kafka_group_id: str = "nexora-agent-document-manage"
    kafka_parse_topic: str = "nexora-agent-document-parse-route"
    kafka_index_topic: str = "nexora-agent-document-index-build"

    # ----- MinIO -----
    minio_endpoint: str = "127.0.0.1:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "nexora-agent-document"
    minio_secure: bool = False

    # ----- Elasticsearch -----
    elasticsearch_urls: str = "http://127.0.0.1:9200"
    elasticsearch_username: str = "elastic"
    elasticsearch_password: str = "elastic"
    elasticsearch_keyword_index: str = "nexora-agent-document-keyword"
    elasticsearch_navigation_index: str = "nexora-agent-document-navigation"
    elasticsearch_route_index: str = "nexora-agent-knowledge-route"

    # ----- Neo4j -----
    neo4j_uri: str = "bolt://127.0.0.1:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "12345678"
    neo4j_database: str = "neo4j"

    # ----- Tika -----
    tika_url: str = "http://127.0.0.1:9998"

    # ----- LLM -----
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_api_key: str = ""
    llm_model: str = "qwen-plus-latest"
    embedding_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    embedding_api_key: str = ""
    embedding_model: str = "text-embedding-v4"

    # ----- Rerank -----
    rerank_enabled: bool = False
    rerank_url: str = "https://api.siliconflow.cn/v1/rerank"
    rerank_api_key: str = ""
    rerank_model: str = "BAAI/bge-reranker-v2-m3"

    # ----- tavily -----
    tavily_enabled: bool = True
    tavily_base_url: str = "https://api.tavily.com"
    tavily_api_key: str = ""

    # ----- 管理后台 -----
    admin_username: str = "admin"
    admin_password: str = "admin123456"
    admin_token_secret: str = "change-me"
    admin_token_expire_minutes: int = 720
    preview_mode_enabled: bool = False
    preview_mode_message: str = "线上环境为只读展示模式，仅开放浏览与检索能力"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def elasticsearch_url_list(self) -> list[str]:
        return [url.strip() for url in self.elasticsearch_urls.split(",") if url.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()