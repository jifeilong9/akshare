#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: AKShare FastAPI 主应用入口
提供统一的 HTTP API 接口访问 AKShare 数据
"""
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from api.config import settings
from api.routers import bond, forex, fund, futures, index, stock
from api.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("=" * 50)
    print("AKShare FastAPI Service Starting...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"API Version: {settings.API_VERSION}")
    print(f"Rate Limit: {settings.RATE_LIMIT_TIMES}/{settings.RATE_LIMIT_SECONDS}s")
    print("=" * 50)
    yield
    # 关闭时执行
    print("AKShare FastAPI Service Shutting down...")


# 创建 FastAPI 应用实例
app = FastAPI(
    title="AKShare API Service",
    description="基于 AKShare 的财经数据 HTTP API 服务",
    version=settings.API_VERSION,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan,
)


# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加可信主机中间件 (生产环境)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


# 添加速率限制中间件
app.add_middleware(RateLimitMiddleware)


# 全局异常处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """请求参数验证异常处理"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "请求参数验证失败",
            "detail": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "detail": str(exc) if settings.ENVIRONMENT == "development" else None,
        },
    )


# 注册路由
app.include_router(stock.router, prefix="/api/stock", tags=["股票数据"])
app.include_router(fund.router, prefix="/api/fund", tags=["基金数据"])
app.include_router(futures.router, prefix="/api/futures", tags=["期货数据"])
app.include_router(bond.router, prefix="/api/bond", tags=["债券数据"])
app.include_router(index.router, prefix="/api/index", tags=["指数数据"])
app.include_router(forex.router, prefix="/api/forex", tags=["外汇数据"])


# 健康检查接口
@app.get("/health", tags=["系统"])
async def health_check() -> Dict[str, str]:
    """
    健康检查接口
    """
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "service": "AKShare API",
    }


# 根路径
@app.get("/", tags=["系统"])
async def root() -> Dict[str, str]:
    """
    根路径欢迎信息
    """
    return {
        "service": "AKShare API Service",
        "version": settings.API_VERSION,
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled",
        "message": "AKShare 财经数据 API 服务运行中",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        workers=settings.WORKERS if settings.ENVIRONMENT == "production" else 1,
        log_level="info",
    )

