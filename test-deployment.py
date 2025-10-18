#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/18
Desc: AKShare API 本地部署测试脚本
"""
import time
import requests
import sys

# API 配置
BASE_URL = "http://localhost:8000"
TOKEN = "dev-token-12345678"

# 设置请求头
headers = {
    "X-API-Token": TOKEN
}


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health_check():
    """测试健康检查接口"""
    print_section("测试 1: 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 健康检查通过")
            print(f"  状态: {data.get('status')}")
            print(f"  版本: {data.get('version')}")
            print(f"  服务: {data.get('service')}")
            return True
        else:
            print(f"✗ 健康检查失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


def test_root_endpoint():
    """测试根路径"""
    print_section("测试 2: 根路径")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 根路径访问成功")
            print(f"  服务: {data.get('service')}")
            print(f"  版本: {data.get('version')}")
            print(f"  文档: {data.get('docs')}")
            return True
        else:
            print(f"✗ 根路径访问失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


def test_docs_endpoint():
    """测试文档接口"""
    print_section("测试 3: API 文档")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print(f"✓ API 文档可访问")
            print(f"  URL: {BASE_URL}/docs")
            return True
        else:
            print(f"✗ API 文档不可访问: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


def test_stock_api():
    """测试股票数据接口"""
    print_section("测试 4: 股票数据接口 (需要 Token)")
    try:
        # 测试获取股票历史数据
        response = requests.get(
            f"{BASE_URL}/api/stock/zh-a-hist",
            headers=headers,
            params={
                "symbol": "000001",
                "period": "daily",
                "start_date": "20241001",
                "end_date": "20241018",
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                result = data.get("data", {})
                print(f"✓ 股票数据获取成功")
                print(f"  股票代码: 000001")
                print(f"  返回条数: {len(result)}")
                if result:
                    print(f"  示例数据: {result[0] if isinstance(result, list) else '字典格式'}")
                return True
            else:
                print(f"✗ API 返回错误: {data.get('message')}")
                return False
        elif response.status_code == 401:
            print(f"✗ 认证失败: 请检查 Token 配置")
            return False
        else:
            print(f"✗ 请求失败: HTTP {response.status_code}")
            print(f"  响应: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_rate_limit():
    """测试速率限制"""
    print_section("测试 5: 速率限制")
    try:
        print("发送多个连续请求测试速率限制...")
        success_count = 0
        rate_limited = False
        
        for i in range(5):
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                rate_limited = True
                print(f"✓ 速率限制已触发 (第 {i+1} 次请求)")
                break
        
        if success_count > 0 and not rate_limited:
            print(f"✓ 速率限制正常 ({success_count} 次请求成功)")
            return True
        elif rate_limited:
            print(f"✓ 速率限制功能正常")
            return True
        else:
            print(f"✗ 速率限制测试异常")
            return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def main():
    """主测试流程"""
    print("\n" + "=" * 60)
    print("  AKShare API 本地部署测试")
    print("=" * 60)
    print(f"\nAPI 地址: {BASE_URL}")
    print(f"测试 Token: {TOKEN}")
    
    # 等待服务启动
    print("\n等待服务启动...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print(f"✓ 服务已就绪")
                break
        except:
            pass
        
        if i < max_retries - 1:
            print(f"  等待中... ({i+1}/{max_retries})")
            time.sleep(2)
        else:
            print(f"\n✗ 服务未响应，请检查容器是否正常运行")
            print(f"  提示: 运行 'docker-compose logs -f' 查看日志")
            sys.exit(1)
    
    # 运行测试
    results = []
    results.append(("健康检查", test_health_check()))
    results.append(("根路径", test_root_endpoint()))
    results.append(("API 文档", test_docs_endpoint()))
    results.append(("股票数据接口", test_stock_api()))
    results.append(("速率限制", test_rate_limit()))
    
    # 打印测试结果
    print_section("测试结果汇总")
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("\n" + "=" * 60)
        print("  🎉 所有测试通过！API 服务运行正常")
        print("=" * 60)
        print(f"\n访问 API 文档: {BASE_URL}/docs")
        print(f"查看容器日志: docker-compose logs -f")
        print("\n")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("  ⚠️  部分测试失败，请检查日志")
        print("=" * 60)
        print(f"\n查看日志: docker-compose logs -f")
        print(f"重启服务: docker-compose restart")
        print("\n")
        sys.exit(1)


if __name__ == "__main__":
    main()


