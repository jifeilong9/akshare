#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: AKShare API 测试脚本
用于验证 API 服务是否正常运行
"""
import sys
import time
from typing import Dict

import requests


class APITester:
    """API 测试工具"""

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.headers = {"X-API-Token": api_token}
        self.passed = 0
        self.failed = 0

    def test_request(self, name: str, endpoint: str, params: Dict = None) -> bool:
        """
        测试单个接口
        
        :param name: 测试名称
        :param endpoint: 接口路径
        :param params: 请求参数
        :return: 是否通过
        """
        try:
            url = f"{self.base_url}{endpoint}"
            print(f"  测试: {name}")
            print(f"    URL: {url}")
            if params:
                print(f"    参数: {params}")

            start_time = time.time()
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elapsed = time.time() - start_time

            print(f"    状态码: {response.status_code}")
            print(f"    响应时间: {elapsed:.2f}s")

            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    data_count = len(data["data"]) if data["data"] else 0
                    print(f"    数据条数: {data_count}")
                print(f"    ✓ 通过")
                self.passed += 1
                return True
            else:
                print(f"    ✗ 失败: {response.text}")
                self.failed += 1
                return False
        except Exception as e:
            print(f"    ✗ 异常: {str(e)}")
            self.failed += 1
            return False
        finally:
            print()

    def run_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("AKShare API 测试")
        print("=" * 60)
        print(f"API 地址: {self.base_url}")
        print()

        # 测试健康检查
        print("[1] 健康检查测试")
        print("-" * 60)
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                print("✓ 服务运行正常")
                print(f"  响应: {response.json()}")
                self.passed += 1
            else:
                print("✗ 服务异常")
                self.failed += 1
        except Exception as e:
            print(f"✗ 无法连接到服务: {str(e)}")
            print("\n请确保:")
            print("  1. 服务已启动")
            print("  2. 服务地址正确")
            print("  3. 网络连接正常")
            sys.exit(1)
        print()

        # 测试 Token 认证
        print("[2] Token 认证测试")
        print("-" * 60)

        # 测试无 Token 请求
        print("  测试: 无 Token 请求 (应该失败)")
        response = requests.get(f"{self.base_url}/api/stock/zh_a_spot_em")
        if response.status_code == 401:
            print("    ✓ 正确拒绝无 Token 请求")
            self.passed += 1
        else:
            print(f"    ✗ 应该返回 401,实际返回 {response.status_code}")
            self.failed += 1
        print()

        # 测试错误 Token
        print("  测试: 错误 Token (应该失败)")
        response = requests.get(
            f"{self.base_url}/api/stock/zh_a_spot_em",
            headers={"X-API-Token": "invalid-token"},
        )
        if response.status_code == 401:
            print("    ✓ 正确拒绝错误 Token")
            self.passed += 1
        else:
            print(f"    ✗ 应该返回 401,实际返回 {response.status_code}")
            self.failed += 1
        print()

        # 测试股票接口
        print("[3] 股票接口测试")
        print("-" * 60)
        self.test_request(
            "A股历史行情",
            "/api/stock/zh_a_hist",
            params={
                "symbol": "000001",
                "period": "daily",
                "start_date": "20240101",
                "end_date": "20240131",
            },
        )
        self.test_request("A股实时行情", "/api/stock/zh_a_spot_em", params={"limit": 5})
        self.test_request("个股信息", "/api/stock/individual_info_em", params={"symbol": "000001"})

        # 测试基金接口
        print("[4] 基金接口测试")
        print("-" * 60)
        self.test_request(
            "基金信息",
            "/api/fund/open_fund_info_em",
            params={"symbol": "000001", "indicator": "单位净值走势"},
        )

        # 测试债券接口
        print("[5] 债券接口测试")
        print("-" * 60)
        self.test_request("可转债行情", "/api/bond/zh_cov_spot", params={"limit": 5})

        # 测试指数接口
        print("[6] 指数接口测试")
        print("-" * 60)
        self.test_request(
            "指数历史行情",
            "/api/index/zh_a_hist",
            params={
                "symbol": "000001",
                "period": "daily",
                "start_date": "20240101",
                "end_date": "20240131",
            },
        )

        # 测试速率限制
        print("[7] 速率限制测试")
        print("-" * 60)
        print("  发送连续请求测试速率限制...")
        rate_limit_headers = None
        for i in range(5):
            response = requests.get(
                f"{self.base_url}/api/stock/zh_a_spot_em",
                headers=self.headers,
                params={"limit": 1},
            )
            if i == 0:
                rate_limit_headers = {
                    "X-RateLimit-Limit": response.headers.get("X-RateLimit-Limit"),
                    "X-RateLimit-Remaining": response.headers.get("X-RateLimit-Remaining"),
                }
        if rate_limit_headers.get("X-RateLimit-Limit"):
            print(f"    速率限制配置: {rate_limit_headers['X-RateLimit-Limit']} 次/周期")
            print(f"    剩余请求次数: {rate_limit_headers['X-RateLimit-Remaining']}")
            print("    ✓ 速率限制正常工作")
            self.passed += 1
        else:
            print("    ⚠ 未检测到速率限制")
        print()

        # 测试结果汇总
        print("=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        print(f"总计: {self.passed + self.failed} 个测试")
        print(f"✓ 通过: {self.passed}")
        print(f"✗ 失败: {self.failed}")
        print()

        if self.failed == 0:
            print("🎉 所有测试通过!")
            return 0
        else:
            print(f"⚠ {self.failed} 个测试失败")
            return 1


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="AKShare API 测试工具")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API 服务地址 (默认: http://localhost:8000)",
    )
    parser.add_argument(
        "--token",
        default="dev-token-12345678",
        help="API Token (默认: dev-token-12345678)",
    )
    args = parser.parse_args()

    tester = APITester(base_url=args.url, api_token=args.token)
    exit_code = tester.run_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

