#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: FastAPI 应用配置管理
使用 Pydantic Settings 管理环境变量和配置
"""
import secrets
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    # 基础配置
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="运行环境: development, production")
    HOST: str = Field(default="0.0.0.0", description="服务监听地址")
    PORT: int = Field(default=8000, description="服务监听端口")
    WORKERS: int = Field(default=4, description="生产环境 Worker 数量")

    # Token 认证配置
    API_TOKENS: List[str] = Field(
        default_factory=lambda: [
            "dev-token-12345678",  # 开发测试用 token
            secrets.token_urlsafe(32),  # 自动生成一个安全 token
        ],
        description="有效的 API Token 列表",
    )
    TOKEN_HEADER_NAME: str = Field(default="X-API-Token", description="Token 请求头名称")

    # CORS 配置
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["*"],
        description="允许的跨域来源",
    )

    # 可信主机配置 (生产环境使用)
    ALLOWED_HOSTS: List[str] = Field(
        default_factory=lambda: ["*"],
        description="允许的主机列表",
    )

    # 速率限制配置
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="是否启用速率限制")
    RATE_LIMIT_TIMES: int = Field(default=100, description="速率限制: 请求次数")
    RATE_LIMIT_SECONDS: int = Field(default=60, description="速率限制: 时间窗口(秒)")

    # 缓存配置
    CACHE_ENABLED: bool = Field(default=False, description="是否启用缓存")
    CACHE_EXPIRE_SECONDS: int = Field(default=300, description="缓存过期时间(秒)")

    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    LOG_FILE: str = Field(default="logs/akshare_api.log", description="日志文件路径")

    # 数据返回配置
    MAX_ROWS: int = Field(default=10000, description="单次请求最大返回行数")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# 创建全局配置实例
settings = Settings()


# 在开发环境下打印配置的 Token (方便测试)
if settings.ENVIRONMENT == "development":
    print("\n" + "=" * 50)
    print("开发环境 API Tokens:")
    for idx, token in enumerate(settings.API_TOKENS, 1):
        print(f"  {idx}. {token}")
    print("=" * 50 + "\n")

