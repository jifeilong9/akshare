#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: 外汇数据相关 API 路由
"""
from typing import Literal, Optional

import akshare as ak
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import validate_limit, verify_token
from api.schemas import DataResponse

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get(
    "/spot_quote",
    response_model=DataResponse,
    summary="外汇实时行情",
)
async def get_forex_spot_quote(
    symbol: str = Query(default="USDCNY", description="外汇代码"),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取外汇实时行情
    
    数据来源: 新浪财经
    接口: fx_spot_quote
    """
    try:
        df = ak.fx_spot_quote(symbol=symbol)

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
    "/pair_quote_hist",
    response_model=DataResponse,
    summary="外汇货币对历史数据",
)
async def get_currency_hist(
    symbol: str = Query(default="USDCNY", description="货币对代码"),
    period: Literal["daily", "weekly", "monthly"] = Query(
        default="daily", description="周期: daily-日, weekly-周, monthly-月"
    ),
    start_date: str = Query(default="19700101", description="开始日期,格式: YYYYMMDD"),
    end_date: str = Query(default="20500101", description="结束日期,格式: YYYYMMDD"),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取外汇货币对历史数据
    
    数据来源: 新浪财经
    接口: currency_hist
    """
    try:
        df = ak.currency_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )

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

