"""Application lifespan: startup / shutdown hooks."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logger.info(
        "%s starting | env=%s | port=%s",
        settings.app_name,
        settings.app_env,
        settings.app_port,
    )

    # 后续步骤在这里初始化：DB 连接池、Redis、Kafka、ES、Neo4j、MinIO。

    yield

    # 后续步骤在这里释放资源。
    logger.info("%s stopped", settings.app_name)