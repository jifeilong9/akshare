#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 23:00
Desc: AKShare 代理使用示例
演示各种代理配置场景
"""

import akshare as ak
from akshare.utils.proxy import (
    set_global_proxy,
    set_website_proxy,
    set_proxy_pool,
    force_proxy_for_website,
    disable_proxy_for_website,
    get_proxy_config_info,
    Website,
)


def example_1_basic_usage():
    """示例1: 基本使用 - 全局代理"""
    print("=" * 60)
    print("示例1: 基本使用 - 全局代理")
    print("=" * 60)
    
    # 设置全局代理
    set_global_proxy(
        http="http://127.0.0.1:7890",
        https="http://127.0.0.1:7890"
    )
    
    # 使用接口(会自动应用代理)
    df = ak.stock_individual_info_em(symbol="000001")
    print(f"获取到 {len(df)} 条数据")
    print(df.head())
    print()


def example_2_website_specific():
    """示例2: 网站特定代理"""
    print("=" * 60)
    print("示例2: 网站特定代理")
    print("=" * 60)
    
    # 为东方财富设置专用代理
    set_website_proxy(
        Website.EASTMONEY,
        http="http://proxy1.com:8080",
        https="http://proxy1.com:8080"
    )
    
    # 为新浪设置另一个代理
    set_website_proxy(
        Website.SINA,
        proxies={
            "http": "http://proxy2.com:8080",
            "https": "http://proxy2.com:8080"
        }
    )
    
    print("✓ 已为不同网站配置不同代理")
    print()


def example_3_proxy_pool():
    """示例3: 代理池配置"""
    print("=" * 60)
    print("示例3: 代理池配置")
    print("=" * 60)
    
    # 准备代理列表
    proxy_list = [
        {"http": "http://proxy1:8080", "https": "http://proxy1:8080"},
        {"http": "http://proxy2:8080", "https": "http://proxy2:8080"},
        {"http": "http://proxy3:8080", "https": "http://proxy3:8080"},
    ]
    
    # 随机策略
    set_proxy_pool(
        Website.EASTMONEY,
        proxy_list,
        strategy="random"
    )
    
    print(f"✓ 已为东方财富配置代理池,共 {len(proxy_list)} 个代理")
    print("  策略: 随机选择")
    print()


def example_4_force_and_disable():
    """示例4: 强制使用和禁用代理"""
    print("=" * 60)
    print("示例4: 强制使用和禁用代理")
    print("=" * 60)
    
    # 设置全局代理
    set_global_proxy(
        http="http://127.0.0.1:7890",
        https="http://127.0.0.1:7890"
    )
    
    # 强制国际网站使用代理
    force_proxy_for_website(Website.YAHOO)
    force_proxy_for_website(Website.BLOOMBERG)
    print("✓ 强制国际网站使用代理")
    
    # 禁用国内网站代理
    disable_proxy_for_website(Website.EASTMONEY)
    disable_proxy_for_website(Website.SINA)
    print("✓ 禁用国内网站代理")
    print()


def example_5_mixed_scenario():
    """示例5: 混合场景 - 实际应用"""
    print("=" * 60)
    print("示例5: 混合场景 - 实际应用")
    print("=" * 60)
    
    # 场景: 国内用户,需要访问国际网站
    
    # 1. 为国际网站配置代理
    international_proxy = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    
    set_website_proxy(Website.YAHOO, proxies=international_proxy)
    set_website_proxy(Website.BLOOMBERG, proxies=international_proxy)
    set_website_proxy(Website.INVESTING, proxies=international_proxy)
    
    # 2. 国内网站不使用代理(提高速度)
    disable_proxy_for_website(Website.EASTMONEY)
    disable_proxy_for_website(Website.SINA)
    disable_proxy_for_website(Website.CNINFO)
    
    print("✓ 已配置混合代理策略:")
    print("  - 国际网站: 使用代理")
    print("  - 国内网站: 不使用代理")
    
    # 3. 查看配置
    config = get_proxy_config_info()
    print(f"\n当前配置:")
    print(f"  - 启用状态: {config['enabled']}")
    print(f"  - 网站特定代理数: {len(config['website_proxies'])}")
    print(f"  - 禁用代理网站数: {len(config['disabled_proxy_websites'])}")
    print()


def example_6_view_config():
    """示例6: 查看代理配置"""
    print("=" * 60)
    print("示例6: 查看代理配置")
    print("=" * 60)
    
    # 先设置一些配置
    set_global_proxy(http="http://127.0.0.1:7890", https="http://127.0.0.1:7890")
    set_website_proxy(Website.YAHOO, proxies={"http": "http://proxy:8080", "https": "http://proxy:8080"})
    
    proxy_list = [
        {"http": "http://p1:8080", "https": "http://p1:8080"},
        {"http": "http://p2:8080", "https": "http://p2:8080"},
    ]
    set_proxy_pool(Website.EASTMONEY, proxy_list)
    
    # 查看配置
    config = get_proxy_config_info()
    
    print("当前代理配置:")
    print(f"  启用状态: {config['enabled']}")
    print(f"  全局代理: {config['global_proxy']}")
    print(f"  网站特定代理: {config['website_proxies']}")
    print(f"  代理池: {config['proxy_pools']}")
    print(f"  强制代理网站: {config['force_proxy_websites']}")
    print(f"  禁用代理网站: {config['disabled_proxy_websites']}")
    print()


def example_7_environment_based():
    """示例7: 根据环境自动配置"""
    print("=" * 60)
    print("示例7: 根据环境自动配置")
    print("=" * 60)
    
    import os
    
    # 检查是否在需要代理的环境中
    # 例如: 通过环境变量判断
    if os.getenv("USE_PROXY", "false").lower() == "true":
        proxy_url = os.getenv("PROXY_URL", "http://127.0.0.1:7890")
        set_global_proxy(http=proxy_url, https=proxy_url)
        print(f"✓ 已从环境变量配置代理: {proxy_url}")
    else:
        print("✓ 当前环境不需要代理")
    
    print()


def example_8_error_handling():
    """示例8: 错误处理"""
    print("=" * 60)
    print("示例8: 错误处理")
    print("=" * 60)
    
    from requests.exceptions import ProxyError, ConnectTimeout
    
    # 设置一个不存在的代理(用于演示)
    set_global_proxy(
        http="http://non-existent-proxy:9999",
        https="http://non-existent-proxy:9999"
    )
    
    try:
        # 尝试使用接口
        df = ak.stock_individual_info_em(symbol="000001")
        print("✓ 请求成功")
    except (ProxyError, ConnectTimeout) as e:
        print(f"✗ 代理错误: {type(e).__name__}")
        print("  建议:")
        print("  1. 检查代理服务器是否运行")
        print("  2. 检查代理地址和端口是否正确")
        print("  3. 尝试禁用代理或使用其他代理")
    except Exception as e:
        print(f"✗ 其他错误: {e}")
    
    print()


def example_9_real_world():
    """示例9: 真实场景 - 获取多个股票数据"""
    print("=" * 60)
    print("示例9: 真实场景 - 获取多个股票数据")
    print("=" * 60)
    
    # 配置代理
    set_global_proxy(
        http="http://127.0.0.1:7890",
        https="http://127.0.0.1:7890"
    )
    
    # 禁用国内网站代理(提高速度)
    disable_proxy_for_website(Website.EASTMONEY)
    
    # 批量获取股票信息
    symbols = ["000001", "000002", "600000"]
    
    print(f"正在获取 {len(symbols)} 只股票的信息...")
    
    results = []
    for symbol in symbols:
        try:
            df = ak.stock_individual_info_em(symbol=symbol)
            stock_name = df[df['item'] == '股票简称']['value'].values[0]
            print(f"  ✓ {symbol} - {stock_name}")
            results.append((symbol, stock_name))
        except Exception as e:
            print(f"  ✗ {symbol} - 错误: {e}")
    
    print(f"\n成功获取 {len(results)}/{len(symbols)} 只股票信息")
    print()


def main():
    """主函数 - 运行所有示例"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "AKShare 代理使用示例" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    examples = [
        ("基本使用", example_1_basic_usage),
        ("网站特定代理", example_2_website_specific),
        ("代理池配置", example_3_proxy_pool),
        ("强制使用和禁用代理", example_4_force_and_disable),
        ("混合场景", example_5_mixed_scenario),
        ("查看代理配置", example_6_view_config),
        ("根据环境配置", example_7_environment_based),
        ("错误处理", example_8_error_handling),
        ("真实场景", example_9_real_world),
    ]
    
    print("可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. 运行所有示例")
    print()
    
    choice = input("请选择要运行的示例 (0-9): ").strip()
    
    if choice == "0":
        # 运行所有示例
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"✗ 示例出错: {e}")
                print()
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        # 运行指定示例
        idx = int(choice) - 1
        name, func = examples[idx]
        try:
            func()
        except Exception as e:
            print(f"✗ 示例出错: {e}")
    else:
        print("无效的选择")
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    # 注意: 实际运行前请根据您的环境配置正确的代理地址
    print("提示: 运行前请确保:")
    print("1. 代理服务器正常运行")
    print("2. 代理地址和端口配置正确")
    print("3. 网络连接正常")
    print()
    
    # main()
    
    # 简单演示(不需要真实代理)
    print("运行简单演示...")
    example_6_view_config()

