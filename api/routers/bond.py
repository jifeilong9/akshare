#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: 债券数据相关 API 路由
"""
from typing import Optional

import akshare as ak
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import validate_limit, verify_token
from api.schemas import DataResponse

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get(
    "/zh_cov_spot",
    response_model=DataResponse,
    summary="可转债实时行情",
)
async def get_bond_zh_cov_spot(
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取可转债实时行情
    
    数据来源: 新浪财经
    接口: bond_zh_cov_spot
    """
    try:
        df = ak.bond_zh_cov_spot()

        # 限制返回行数
        limit = validate_limit(limit)
        if len(df) > limit:
            df = df.head(limit)

        return DataResponse(
            code=200,
            message="success",
            data=df.to_dict(orient="records"),
            total=len(df),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据失败: {str(e)}",
        )


@router.get(
    "/china_bond_spot",
    response_model=DataResponse,
    summary="现券市场成交行情",
)
async def get_bond_china_spot(
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取中国债券信息网-现券市场成交行情
    
    数据来源: 中国债券信息网
    接口: bond_china_spot
    """
    try:
        df = ak.bond_china_spot()

        # 限制返回行数
        limit = validate_limit(limit)
        if len(df) > limit:
            df = df.head(limit)

        return DataResponse(
            code=200,
            message="success",
            data=df.to_dict(orient="records"),
            total=len(df),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据失败: {str(e)}",
        )


@router.get(
    "/zh_cov_value_analysis",
    response_model=DataResponse,
    summary="可转债价值分析",
)
async def get_bond_zh_cov_value_analysis(
    symbol: str = Query(..., description="可转债代码,如: 113050"),
) -> DataResponse:
    """
    获取可转债价值分析
    
    数据来源: 集思录
    接口: bond_zh_cov_value_analysis
    """
    try:
        df = ak.bond_zh_cov_value_analysis(symbol=symbol)

        return DataResponse(
            code=200,
            message="success",
            data=df.to_dict(orient="records"),
            total=len(df),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据失败: {str(e)}",
        )

