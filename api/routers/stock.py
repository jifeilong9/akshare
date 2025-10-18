#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: 股票数据相关 API 路由
"""
from typing import Literal, Optional

import akshare as ak
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import validate_limit, verify_token
from api.schemas import DataResponse

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get("/zh_a_hist", response_model=DataResponse, summary="A股历史行情数据")
async def get_stock_zh_a_hist(
    symbol: str = Query(..., description="股票代码,如: 000001"),
    period: Literal["daily", "weekly", "monthly"] = Query(
        default="daily", description="周期: daily-日, weekly-周, monthly-月"
    ),
    start_date: str = Query(default="19700101", description="开始日期,格式: YYYYMMDD"),
    end_date: str = Query(default="20500101", description="结束日期,格式: YYYYMMDD"),
    adjust: Literal["", "qfq", "hfq"] = Query(
        default="", description="复权类型: qfq-前复权, hfq-后复权, 空-不复权"
    ),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取 A股历史行情数据
    
    数据来源: 东方财富
    接口: stock_zh_a_hist
    """
    try:
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust,
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


@router.get("/zh_a_spot_em", response_model=DataResponse, summary="A股实时行情数据")
async def get_stock_zh_a_spot_em(
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取沪深京 A 股实时行情数据
    
    数据来源: 东方财富
    接口: stock_zh_a_spot_em
    """
    try:
        df = ak.stock_zh_a_spot_em()

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


@router.get("/info_sh", response_model=DataResponse, summary="上交所股票信息")
async def get_stock_info_sh_name_code(
    symbol: str = Query(default="主板A股", description="市场类型"),
    limit: Optional[int] = Query(default=None, description="返回数据行数限制"),
) -> DataResponse:
    """
    获取上交所股票信息
    
    数据来源: 上海证券交易所
    接口: stock_info_sh_name_code
    """
    try:
        df = ak.stock_info_sh_name_code(symbol=symbol)

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
    "/individual_info_em", response_model=DataResponse, summary="个股信息查询"
)
async def get_stock_individual_info_em(
    symbol: str = Query(..., description="股票代码,如: 000001"),
) -> DataResponse:
    """
    获取个股详细信息
    
    数据来源: 东方财富
    接口: stock_individual_info_em
    """
    try:
        df = ak.stock_individual_info_em(symbol=symbol)

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


@router.get("/zyjs_ths", response_model=DataResponse, summary="股票主营介绍")
async def get_stock_zyjs_ths(
    symbol: str = Query(..., description="股票代码,如: 000001"),
) -> DataResponse:
    """
    获取股票主营介绍
    
    数据来源: 同花顺
    接口: stock_zyjs_ths
    """
    try:
        df = ak.stock_zyjs_ths(symbol=symbol)

        return DataResponse(
            code=200,
            message="success",
            data=df.to_dict(orient="records") if not df.empty else [],
            total=len(df),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据失败: {str(e)}",
        )

