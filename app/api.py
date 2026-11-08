"""Top-level API router. Domain routers are included here as they are built."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health", tags=["system"], summary="健康检查")
async def health() -> dict[str, Any]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "env": settings.app_env,
    }


@router.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {
        "name": "nexora-agent-backend",
        "docs": "/docs",
        "health": "/health",
    }


api_router = APIRouter()
api_router.include_router(router)