#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: 速率限制中间件
基于 IP 地址和 Token 的简单速率限制实现
"""
import time
from collections import defaultdict
from typing import Callable, Dict, Tuple

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    速率限制中间件
    使用滑动窗口算法限制请求频率
    """

    def __init__(self, app):
        super().__init__(app)
        # 存储每个客户端的请求历史: {client_key: [timestamp1, timestamp2, ...]}
        self.request_history: Dict[str, list] = defaultdict(list)

    def _get_client_key(self, request: Request) -> str:
        """
        获取客户端唯一标识
        优先使用 Token, 其次使用 IP 地址
        
        :param request: 请求对象
        :type request: Request
        :return: 客户端唯一标识
        :rtype: str
        """
        # 优先使用 Token 作为标识
        token = request.headers.get(settings.TOKEN_HEADER_NAME)
        if token:
            return f"token:{token}"

        # 获取真实 IP (考虑代理情况)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"

        return f"ip:{ip}"

    def _is_rate_limited(self, client_key: str) -> Tuple[bool, int]:
        """
        检查是否超过速率限制
        
        :param client_key: 客户端唯一标识
        :type client_key: str
        :return: (是否超限, 剩余请求次数)
        :rtype: Tuple[bool, int]
        """
        if not settings.RATE_LIMIT_ENABLED:
            return False, settings.RATE_LIMIT_TIMES

        current_time = time.time()
        time_window = settings.RATE_LIMIT_SECONDS

        # 清理过期的请求记录
        self.request_history[client_key] = [
            timestamp
            for timestamp in self.request_history[client_key]
            if current_time - timestamp < time_window
        ]

        # 检查是否超限
        request_count = len(self.request_history[client_key])
        if request_count >= settings.RATE_LIMIT_TIMES:
            return True, 0

        # 记录本次请求
        self.request_history[client_key].append(current_time)

        return False, settings.RATE_LIMIT_TIMES - request_count - 1

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        处理请求
        
        :param request: 请求对象
        :type request: Request
        :param call_next: 下一个处理器
        :type call_next: Callable
        :return: 响应对象
        :rtype: Response
        """
        # 健康检查接口不限流
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        client_key = self._get_client_key(request)
        is_limited, remaining = self._is_rate_limited(client_key)

        if is_limited:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "code": 429,
                    "message": f"请求过于频繁,请稍后再试 (限制: {settings.RATE_LIMIT_TIMES}/{settings.RATE_LIMIT_SECONDS}秒)",
                },
                headers={
                    "X-RateLimit-Limit": str(settings.RATE_LIMIT_TIMES),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + settings.RATE_LIMIT_SECONDS)),
                },
            )

        # 继续处理请求
        response = await call_next(request)

        # 添加速率限制信息到响应头
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_TIMES)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

