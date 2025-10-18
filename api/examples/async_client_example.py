#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: AKShare API 异步客户端使用示例
支持并发请求,提高数据获取效率
"""
import asyncio
from typing import Dict, List, Optional

import aiohttp
import pandas as pd


class AsyncAKShareAPIClient:
    """
    AKShare API 异步客户端封装
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

    async def _request(
        self, session: aiohttp.ClientSession, endpoint: str, params: Optional[Dict] = None
    ) -> Dict:
        """
        发送异步请求
        
        :param session: aiohttp 会话
        :param endpoint: 接口路径
        :param params: 请求参数
        :return: 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        async with session.get(url, headers=self.headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(
                    f"API 请求失败: {response.status} - {error_data.get('message', 'Unknown error')}"
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

    async def get_stock_hist(
        self,
        session: aiohttp.ClientSession,
        symbol: str,
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        异步获取 A股历史行情
        
        :param session: aiohttp 会话
        :param symbol: 股票代码
        :param period: 周期
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param adjust: 复权类型
        :return: DataFrame
        """
        data = await self._request(
            session,
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

    async def get_multiple_stocks(
        self, symbols: List[str], **kwargs
    ) -> Dict[str, pd.DataFrame]:
        """
        并发获取多只股票的历史行情
        
        :param symbols: 股票代码列表
        :param kwargs: 其他参数
        :return: 股票代码到 DataFrame 的映射
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.get_stock_hist(session, symbol, **kwargs) for symbol in symbols
            ]
            results = await asyncio.gather(*tasks)
            return dict(zip(symbols, results))


async def main():
    """异步使用示例"""
    # 初始化客户端
    client = AsyncAKShareAPIClient(
        base_url="http://localhost:8000",
        api_token="your-secret-token-here"  # 请修改为你的 token
    )

    print("=" * 50)
    print("AKShare API 异步客户端使用示例")
    print("=" * 50)
    print()

    # 并发获取多只股票数据
    symbols = ["000001", "000002", "600000", "600036"]
    print(f"并发获取 {len(symbols)} 只股票的历史行情...")
    print(f"股票代码: {', '.join(symbols)}")
    print()

    import time
    start_time = time.time()

    results = await client.get_multiple_stocks(
        symbols=symbols,
        period="daily",
        start_date="20240101",
        end_date="20241231",
    )

    elapsed_time = time.time() - start_time

    print(f"✓ 完成! 耗时: {elapsed_time:.2f} 秒")
    print()

    # 显示结果
    for symbol, df in results.items():
        print(f"股票代码: {symbol}, 数据行数: {len(df)}")
        if not df.empty:
            print(df.head(3))
        print()

    print("=" * 50)
    print("异步示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

