#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: 期货数据相关 API 路由
"""
from typing import Literal, Optional

import akshare as ak
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import validate_limit, verify_token
from api.schemas import DataResponse

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get(
    "/futures_main_sina",
    response_model=DataResponse,
    summary="期货主力合约实时行情",
)
async def get_futures_main_sina(
    symbol: str = Query(..., description="期货品种代码,如: CU"),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取期货主力合约实时行情
    
    数据来源: 新浪财经
    接口: futures_main_sina
    """
    try:
        df = ak.futures_main_sina(symbol=symbol)

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
    "/futures_zh_spot",
    response_model=DataResponse,
    summary="期货实时行情",
)
async def get_futures_zh_spot(
    symbol: str = Query(..., description="期货合约代码,如: al2503"),
    market: Literal["CFFEX", "DCE", "CZCE", "SHFE", "INE", "GFEX"] = Query(
        ..., description="交易所代码"
    ),
) -> DataResponse:
    """
    获取期货实时行情
    
    数据来源: 新浪财经
    接口: futures_zh_spot
    """
    try:
        df = ak.futures_zh_spot(symbol=symbol, market=market)

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
    "/futures_comm_info",
    response_model=DataResponse,
    summary="期货品种信息",
)
async def get_futures_comm_info(
    symbol: str = Query(
        default="玻璃", description="期货品种名称,如: 玻璃, 燃油, PTA"
    ),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取期货品种信息
    
    数据来源: 生意社
    接口: futures_comm_info
    """
    try:
        df = ak.futures_comm_info(symbol=symbol)

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

