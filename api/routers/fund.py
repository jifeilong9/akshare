#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: 基金数据相关 API 路由
"""
from typing import Optional

import akshare as ak
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import validate_limit, verify_token
from api.schemas import DataResponse

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get("/open_fund_info_em", response_model=DataResponse, summary="开放式基金信息")
async def get_fund_open_fund_info_em(
    symbol: str = Query(..., description="基金代码,如: 000001"),
    indicator: str = Query(default="单位净值走势", description="指标名称"),
) -> DataResponse:
    """
    获取开放式基金信息
    
    数据来源: 东方财富
    接口: fund_open_fund_info_em
    """
    try:
        df = ak.fund_open_fund_info_em(symbol=symbol, indicator=indicator)

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


@router.get("/etf_fund_info_em", response_model=DataResponse, summary="ETF基金信息")
async def get_fund_etf_fund_info_em(
    symbol: str = Query(..., description="ETF代码,如: 512690"),
    start_date: str = Query(default="20200101", description="开始日期,格式: YYYYMMDD"),
    end_date: str = Query(default="20250101", description="结束日期,格式: YYYYMMDD"),
) -> DataResponse:
    """
    获取 ETF 基金净值走势
    
    数据来源: 东方财富
    接口: fund_etf_fund_info_em
    """
    try:
        df = ak.fund_etf_fund_info_em(
            fund=symbol, start_date=start_date, end_date=end_date
        )

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
    "/fund_portfolio_hold_em",
    response_model=DataResponse,
    summary="基金持仓",
)
async def get_fund_portfolio_hold_em(
    symbol: str = Query(..., description="基金代码,如: 000001"),
    date: str = Query(..., description="查询日期,格式: YYYY-MM-DD"),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取基金持仓信息
    
    数据来源: 东方财富
    接口: fund_portfolio_hold_em
    """
    try:
        df = ak.fund_portfolio_hold_em(symbol=symbol, date=date)

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
    "/fund_name_em",
    response_model=DataResponse,
    summary="基金列表",
)
async def get_fund_name_em(
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取所有基金代码和名称
    
    数据来源: 东方财富
    接口: fund_name_em
    """
    try:
        df = ak.fund_name_em()

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

