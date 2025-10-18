#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: API 数据模型定义
使用 Pydantic 定义请求和响应模型
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DataResponse(BaseModel):
    """
    统一的数据响应模型
    """

    code: int = Field(description="响应状态码")
    message: str = Field(description="响应消息")
    data: Optional[List[Dict[str, Any]]] = Field(default=None, description="返回的数据")
    total: Optional[int] = Field(default=None, description="数据总条数")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": [
                    {
                        "日期": "2024-01-01",
                        "开盘": 10.5,
                        "收盘": 10.6,
                        "最高": 10.7,
                        "最低": 10.4,
                    }
                ],
                "total": 1,
            }
        }


class ErrorResponse(BaseModel):
    """
    错误响应模型
    """

    code: int = Field(description="错误状态码")
    message: str = Field(description="错误消息")
    detail: Optional[str] = Field(default=None, description="详细错误信息")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 400,
                "message": "请求参数错误",
                "detail": "symbol 参数不能为空",
            }
        }

