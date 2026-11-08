"""Unified application errors and exception handlers.

  The JSON envelope follows the legacy Java ``ApiResponse`` shape::

      {"code": 0, "message": null, "data": ...}

  Step 2 will replace the inline payload helper with ``app.common.response.ApiResponse``.
  """

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base class for expected business errors."""

    def __init__(
            self,
            message: str,
            *,
            code: int = -100,
            status_code: int = 400,
            data: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data


class UnauthorizedError(AppError):
    def __init__(self, message: str = "未登录或登录已过期") -> None:
        super().__init__(message, code=401, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, message: str = "没有权限执行该操作") -> None:
        super().__init__(message, code=403, status_code=403)


class NotFoundError(AppError):
    def __init__(self, message: str = "资源不存在") -> None:
        super().__init__(message, code=404, status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str = "资源状态冲突") -> None:
        super().__init__(message, code=409, status_code=409)


def _payload(
        code: int,
        message: str | None,
        data: Any = None,
) -> dict[str, Any]:
    return {"code": code, "message": message, "data": data}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload(exc.code, exc.message, exc.data),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
            request: Request,
            exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_payload(422, "请求参数校验失败", jsonable_encoder(exc.errors())),
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(
            request: Request,
            exc: StarletteHTTPException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload(exc.status_code, str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
            request: Request,
            exc: Exception,
    ) -> JSONResponse:
        logger.exception("unhandled error | path=%s", request.url.path)
        settings = getattr(request.app.state, "settings", None)
        data = {"detail": str(exc)} if settings is not None and settings.debug else None
        return JSONResponse(
            status_code=500,
            content=_payload(500, "系统错误，请稍后重试", data),
        )