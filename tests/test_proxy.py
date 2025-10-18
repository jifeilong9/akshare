#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 23:00
Desc: 代理功能测试
"""

import unittest
from akshare.utils.proxy import (
    ProxyConfig,
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


class TestProxyConfig(unittest.TestCase):
    """代理配置测试"""
    
    def setUp(self):
        """每个测试前清除配置"""
        clear_proxy_config()
    
    def tearDown(self):
        """每个测试后清除配置"""
        clear_proxy_config()
    
    def test_global_proxy(self):
        """测试全局代理配置"""
        # 设置全局代理
        set_global_proxy(
            http="http://127.0.0.1:7890",
            https="http://127.0.0.1:7890"
        )
        
        # 获取代理
        proxies = get_proxy()
        self.assertIsNotNone(proxies)
        self.assertEqual(proxies['http'], "http://127.0.0.1:7890")
        self.assertEqual(proxies['https'], "http://127.0.0.1:7890")
    
    def test_website_specific_proxy(self):
        """测试网站特定代理"""
        # 为东方财富设置代理
        set_website_proxy(
            Website.EASTMONEY,
            http="http://proxy1:8080",
            https="http://proxy1:8080"
        )
        
        # 获取东方财富的代理
        proxies = get_proxy(Website.EASTMONEY)
        self.assertIsNotNone(proxies)
        self.assertEqual(proxies['http'], "http://proxy1:8080")
        
        # 获取其他网站的代理(应该是None)
        proxies = get_proxy(Website.SINA)
        self.assertIsNone(proxies)
    
    def test_proxy_priority(self):
        """测试代理优先级"""
        # 设置全局代理
        set_global_proxy(
            http="http://global:8080",
            https="http://global:8080"
        )
        
        # 设置网站特定代理
        set_website_proxy(
            Website.EASTMONEY,
            http="http://specific:8080",
            https="http://specific:8080"
        )
        
        # 东方财富应该使用特定代理
        proxies = get_proxy(Website.EASTMONEY)
        self.assertEqual(proxies['http'], "http://specific:8080")
        
        # 其他网站应该使用全局代理
        proxies = get_proxy(Website.SINA)
        self.assertEqual(proxies['http'], "http://global:8080")
    
    def test_proxy_pool(self):
        """测试代理池"""
        proxy_list = [
            {"http": "http://p1:8080", "https": "http://p1:8080"},
            {"http": "http://p2:8080", "https": "http://p2:8080"},
            {"http": "http://p3:8080", "https": "http://p3:8080"},
        ]
        
        # 设置代理池
        set_proxy_pool(Website.EASTMONEY, proxy_list, strategy="random")
        
        # 获取代理(应该从池中选择)
        proxies = get_proxy(Website.EASTMONEY)
        self.assertIsNotNone(proxies)
        
        # 验证返回的代理在列表中
        proxy_urls = [p['http'] for p in proxy_list]
        self.assertIn(proxies['http'], proxy_urls)
    
    def test_disable_proxy_for_website(self):
        """测试禁用特定网站代理"""
        # 设置全局代理
        set_global_proxy(
            http="http://127.0.0.1:7890",
            https="http://127.0.0.1:7890"
        )
        
        # 禁用东方财富代理
        disable_proxy_for_website(Website.EASTMONEY)
        
        # 东方财富不应该使用代理
        proxies = get_proxy(Website.EASTMONEY)
        self.assertIsNone(proxies)
        
        # 其他网站应该使用代理
        proxies = get_proxy(Website.SINA)
        self.assertIsNotNone(proxies)
    
    def test_force_proxy_for_website(self):
        """测试强制使用代理"""
        # 不设置代理
        # 强制雅虎使用代理
        force_proxy_for_website(Website.YAHOO)
        
        # 应该抛出异常(因为没有配置代理)
        with self.assertRaises(ValueError):
            get_proxy(Website.YAHOO)
        
        # 设置全局代理后应该正常
        set_global_proxy(
            http="http://127.0.0.1:7890",
            https="http://127.0.0.1:7890"
        )
        proxies = get_proxy(Website.YAHOO)
        self.assertIsNotNone(proxies)
    
    def test_config_info(self):
        """测试配置信息获取"""
        # 设置一些配置
        set_global_proxy(http="http://127.0.0.1:7890", https="http://127.0.0.1:7890")
        set_website_proxy(Website.YAHOO, proxies={"http": "http://p:8080", "https": "http://p:8080"})
        disable_proxy_for_website(Website.EASTMONEY)
        
        # 获取配置信息
        config = get_proxy_config_info()
        
        self.assertTrue(config['enabled'])
        self.assertIsNotNone(config['global_proxy'])
        self.assertIn('yahoo', config['website_proxies'])
        self.assertIn('eastmoney', config['disabled_proxy_websites'])
    
    def test_clear_config(self):
        """测试清除配置"""
        # 设置配置
        set_global_proxy(http="http://127.0.0.1:7890", https="http://127.0.0.1:7890")
        set_website_proxy(Website.EASTMONEY, proxies={"http": "http://p:8080", "https": "http://p:8080"})
        
        # 清除配置
        clear_proxy_config()
        
        # 应该没有代理
        proxies = get_proxy()
        self.assertIsNone(proxies)
        
        # 配置信息应该为空
        config = get_proxy_config_info()
        self.assertIsNone(config['global_proxy'])
        self.assertEqual(len(config['website_proxies']), 0)


def run_tests():
    """运行测试"""
    print("=" * 60)
    print("运行代理功能测试")
    print("=" * 60)
    print()
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProxyConfig)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    print(f"测试结果: {'通过' if result.wasSuccessful() else '失败'}")
    print(f"运行: {result.testsRun} 个测试")
    print(f"失败: {len(result.failures)} 个")
    print(f"错误: {len(result.errors)} 个")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

