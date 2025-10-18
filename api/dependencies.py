#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: FastAPI 依赖注入
提供认证、参数验证等通用依赖
"""
from typing import Optional

from fastapi import Header, HTTPException, status

from api.config import settings


async def verify_token(
    x_api_token: Optional[str] = Header(None, description="API 访问 Token")
) -> str:
    """
    验证 API Token
    
    :param x_api_token: 请求头中的 Token
    :type x_api_token: Optional[str]
    :return: 验证通过的 Token
    :rtype: str
    :raises HTTPException: Token 无效或缺失时抛出 401 异常
    """
    if not x_api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少认证 Token,请在请求头中添加 X-API-Token",
            headers={"WWW-Authenticate": "Token"},
        )

    if x_api_token not in settings.API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 API Token",
            headers={"WWW-Authenticate": "Token"},
        )

    return x_api_token


def validate_limit(limit: Optional[int] = None) -> int:
    """
    验证并限制返回数据的行数
    
    :param limit: 请求的数据行数
    :type limit: Optional[int]
    :return: 验证后的行数限制
    :rtype: int
    """
    if limit is None:
        return settings.MAX_ROWS

    if limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit 参数必须大于 0",
        )

    if limit > settings.MAX_ROWS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"limit 参数不能超过 {settings.MAX_ROWS}",
        )

    return limit

