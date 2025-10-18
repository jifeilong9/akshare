#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: AKShare API 客户端使用示例
"""
import requests
import pandas as pd
from typing import Dict, List, Optional


class AKShareAPIClient:
    """
    AKShare API 客户端封装
    """

    def __init__(self, base_url: str = "http://localhost:8000", api_token: str = None):
        """
        初始化客户端
        
        :param base_url: API 服务地址
        :param api_token: API Token
        """
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.headers = {"X-API-Token": api_token} if api_token else {}

    def _request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Dict:
        """
        发送请求
        
        :param endpoint: 接口路径
        :param params: 请求参数
        :return: 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            raise Exception(
                f"API 请求失败: {response.status_code} - {error_data.get('message', 'Unknown error')}"
            )

    def to_dataframe(self, data: Dict) -> pd.DataFrame:
        """
        将 API 响应转换为 DataFrame
        
        :param data: API 响应数据
        :return: DataFrame
        """
        if data.get("code") == 200 and data.get("data"):
            return pd.DataFrame(data["data"])
        else:
            return pd.DataFrame()

    # ========== 股票接口 ==========

    def get_stock_hist(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        获取 A股历史行情
        
        :param symbol: 股票代码
        :param period: 周期 (daily/weekly/monthly)
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param adjust: 复权类型 (qfq/hfq/"")
        :return: DataFrame
        """
        data = self._request(
            "/api/stock/zh_a_hist",
            params={
                "symbol": symbol,
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
                "adjust": adjust,
            },
        )
        return self.to_dataframe(data)

    def get_stock_spot(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        获取 A股实时行情
        
        :param limit: 返回行数限制
        :return: DataFrame
        """
        params = {"limit": limit} if limit else {}
        data = self._request("/api/stock/zh_a_spot_em", params=params)
        return self.to_dataframe(data)

    def get_stock_info(self, symbol: str) -> pd.DataFrame:
        """
        获取个股详细信息
        
        :param symbol: 股票代码
        :return: DataFrame
        """
        data = self._request("/api/stock/individual_info_em", params={"symbol": symbol})
        return self.to_dataframe(data)

    # ========== 基金接口 ==========

    def get_fund_info(
        self, symbol: str, indicator: str = "单位净值走势"
    ) -> pd.DataFrame:
        """
        获取开放式基金信息
        
        :param symbol: 基金代码
        :param indicator: 指标名称
        :return: DataFrame
        """
        data = self._request(
            "/api/fund/open_fund_info_em",
            params={"symbol": symbol, "indicator": indicator},
        )
        return self.to_dataframe(data)

    def get_etf_info(
        self, symbol: str, start_date: str = "20200101", end_date: str = "20250101"
    ) -> pd.DataFrame:
        """
        获取 ETF 基金信息
        
        :param symbol: ETF 代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: DataFrame
        """
        data = self._request(
            "/api/fund/etf_fund_info_em",
            params={"symbol": symbol, "start_date": start_date, "end_date": end_date},
        )
        return self.to_dataframe(data)

    # ========== 期货接口 ==========

    def get_futures_main(self, symbol: str) -> pd.DataFrame:
        """
        获取期货主力合约实时行情
        
        :param symbol: 期货品种代码
        :return: DataFrame
        """
        data = self._request("/api/futures/futures_main_sina", params={"symbol": symbol})
        return self.to_dataframe(data)

    # ========== 债券接口 ==========

    def get_bond_spot(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        获取可转债实时行情
        
        :param limit: 返回行数限制
        :return: DataFrame
        """
        params = {"limit": limit} if limit else {}
        data = self._request("/api/bond/zh_cov_spot", params=params)
        return self.to_dataframe(data)

    # ========== 指数接口 ==========

    def get_index_hist(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
    ) -> pd.DataFrame:
        """
        获取指数历史行情
        
        :param symbol: 指数代码
        :param period: 周期
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: DataFrame
        """
        data = self._request(
            "/api/index/zh_a_hist",
            params={
                "symbol": symbol,
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        return self.to_dataframe(data)

    # ========== 外汇接口 ==========

    def get_forex_spot(self, symbol: str = "USDCNY") -> pd.DataFrame:
        """
        获取外汇实时行情
        
        :param symbol: 外汇代码
        :return: DataFrame
        """
        data = self._request("/api/forex/spot_quote", params={"symbol": symbol})
        return self.to_dataframe(data)


def main():
    """使用示例"""
    # 初始化客户端
    client = AKShareAPIClient(
        base_url="http://localhost:8000",
        api_token="your-secret-token-here"  # 请修改为你的 token
    )

    print("=" * 50)
    print("AKShare API 客户端使用示例")
    print("=" * 50)
    print()

    # 示例 1: 获取股票历史行情
    print("1. 获取平安银行(000001)历史行情...")
    df_stock = client.get_stock_hist(
        symbol="000001",
        period="daily",
        start_date="20240101",
        end_date="20241231"
    )
    print(f"获取到 {len(df_stock)} 条数据")
    print(df_stock.head())
    print()

    # 示例 2: 获取实时行情
    print("2. 获取 A股实时行情 (前10条)...")
    df_spot = client.get_stock_spot(limit=10)
    print(f"获取到 {len(df_spot)} 条数据")
    print(df_spot.head())
    print()

    # 示例 3: 获取个股信息
    print("3. 获取平安银行详细信息...")
    df_info = client.get_stock_info(symbol="000001")
    print(df_info)
    print()

    # 示例 4: 获取基金信息
    print("4. 获取华夏成长基金(000001)信息...")
    df_fund = client.get_fund_info(symbol="000001")
    print(f"获取到 {len(df_fund)} 条数据")
    print(df_fund.head())
    print()

    # 示例 5: 获取可转债行情
    print("5. 获取可转债实时行情 (前5条)...")
    df_bond = client.get_bond_spot(limit=5)
    print(f"获取到 {len(df_bond)} 条数据")
    print(df_bond)
    print()

    # 示例 6: 获取指数行情
    print("6. 获取上证指数(000001)历史行情...")
    df_index = client.get_index_hist(
        symbol="000001",
        start_date="20240101",
        end_date="20241231"
    )
    print(f"获取到 {len(df_index)} 条数据")
    print(df_index.head())
    print()

    print("=" * 50)
    print("示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()

