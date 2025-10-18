#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 23:00
Desc: 代理功能演示脚本(独立运行)
"""

import sys
sys.path.insert(0, '.')

from akshare.utils.proxy import (
    Website,
    get_proxy,
    set_global_proxy,
    set_website_proxy,
    set_proxy_pool,
    force_proxy_for_website,
    disable_proxy_for_website,
    clear_proxy_config,
    get_proxy_config_info,
)


def test_demo():
    """演示代理功能"""
    print("=" * 70)
    print(" " * 20 + "AKShare 代理功能演示")
    print("=" * 70)
    print()
    
    # 1. 全局代理
    print("【1】设置全局代理")
    print("-" * 70)
    set_global_proxy(
        http="http://127.0.0.1:7890",
        https="http://127.0.0.1:7890"
    )
    proxies = get_proxy()
    print(f"✓ 全局代理: {proxies}")
    print()
    
    # 2. 网站特定代理
    print("【2】设置网站特定代理")
    print("-" * 70)
    set_website_proxy(
        Website.EASTMONEY,
        http="http://proxy-eastmoney:8080",
        https="http://proxy-eastmoney:8080"
    )
    set_website_proxy(
        Website.YAHOO,
        proxies={"http": "http://proxy-yahoo:1080", "https": "http://proxy-yahoo:1080"}
    )
    
    proxies_em = get_proxy(Website.EASTMONEY)
    proxies_yahoo = get_proxy(Website.YAHOO)
    proxies_sina = get_proxy(Website.SINA)  # 未设置,应使用全局代理
    
    print(f"✓ 东方财富代理: {proxies_em}")
    print(f"✓ 雅虎财经代理: {proxies_yahoo}")
    print(f"✓ 新浪财经代理(使用全局): {proxies_sina}")
    print()
    
    # 3. 代理池
    print("【3】设置代理池")
    print("-" * 70)
    proxy_list = [
        {"http": "http://pool-proxy1:8080", "https": "http://pool-proxy1:8080"},
        {"http": "http://pool-proxy2:8080", "https": "http://pool-proxy2:8080"},
        {"http": "http://pool-proxy3:8080", "https": "http://pool-proxy3:8080"},
    ]
    set_proxy_pool(Website.SINA, proxy_list, strategy="random")
    
    print(f"✓ 为新浪财经设置 {len(proxy_list)} 个代理")
    print("  获取3次,查看随机效果:")
    for i in range(3):
        proxies = get_proxy(Website.SINA)
        print(f"  第{i+1}次: {proxies['http']}")
    print()
    
    # 4. 禁用特定网站代理
    print("【4】禁用特定网站代理")
    print("-" * 70)
    disable_proxy_for_website(Website.CNINFO)
    proxies = get_proxy(Website.CNINFO)
    print(f"✓ 巨潮资讯代理(已禁用): {proxies}")
    print()
    
    # 5. 强制使用代理
    print("【5】强制使用代理")
    print("-" * 70)
    force_proxy_for_website(Website.BLOOMBERG)
    try:
        # 清除全局代理测试
        clear_proxy_config()
        proxies = get_proxy(Website.BLOOMBERG)
        print(f"✗ 不应该到这里")
    except ValueError as e:
        print(f"✓ 正确抛出异常: {str(e)[:60]}...")
    
    # 恢复全局代理
    set_global_proxy(http="http://127.0.0.1:7890", https="http://127.0.0.1:7890")
    force_proxy_for_website(Website.BLOOMBERG)
    proxies = get_proxy(Website.BLOOMBERG)
    print(f"✓ 设置全局代理后成功: {proxies}")
    print()
    
    # 6. 查看完整配置
    print("【6】查看完整配置")
    print("-" * 70)
    
    # 重新设置一些配置用于展示
    clear_proxy_config()
    set_global_proxy(http="http://127.0.0.1:7890", https="http://127.0.0.1:7890")
    set_website_proxy(Website.EASTMONEY, proxies={"http": "http://em:8080", "https": "http://em:8080"})
    set_website_proxy(Website.YAHOO, proxies={"http": "http://yahoo:8080", "https": "http://yahoo:8080"})
    set_proxy_pool(Website.SINA, [{"http": "http://p1:8080", "https": "http://p1:8080"}])
    disable_proxy_for_website(Website.CNINFO)
    force_proxy_for_website(Website.BLOOMBERG)
    
    config = get_proxy_config_info()
    
    print(f"启用状态: {config['enabled']}")
    print(f"全局代理: {config['global_proxy']}")
    print(f"网站特定代理: {config['website_proxies']}")
    print(f"代理池: {config['proxy_pools']}")
    print(f"强制代理网站: {config['force_proxy_websites']}")
    print(f"禁用代理网站: {config['disabled_proxy_websites']}")
    print()
    
    # 7. 实际使用示例
    print("【7】实际使用示例")
    print("-" * 70)
    print("在接口中使用代理的代码:")
    print()
    print("```python")
    print("from akshare.utils.proxy import get_proxy, Website")
    print("import requests")
    print()
    print("def stock_data_interface(symbol: str):")
    print("    url = 'https://api.eastmoney.com/data'")
    print("    params = {'symbol': symbol}")
    print("    ")
    print("    # 获取东方财富的代理配置")
    print("    proxies = get_proxy(Website.EASTMONEY)")
    print("    ")
    print("    # 在请求中使用代理")
    print("    r = requests.get(url, params=params, proxies=proxies)")
    print("    return r.json()")
    print("```")
    print()
    
    print("=" * 70)
    print(" " * 25 + "演示完成!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_demo()
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

