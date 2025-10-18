#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 23:00
Desc: AKShare 统一代理管理模块
支持按网站配置不同的代理策略
"""

import random
from typing import Dict, List, Optional, Union
from enum import Enum


class ProxyType(Enum):
    """代理类型枚举"""
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"


class Website(Enum):
    """支持的网站标识"""
    # 财经数据源
    EASTMONEY = "eastmoney"  # 东方财富
    SINA = "sina"  # 新浪财经
    TENCENT = "tencent"  # 腾讯财经
    TONGHUASHUN = "ths"  # 同花顺
    CNINFO = "cninfo"  # 巨潮资讯
    
    # 交易所
    SSE = "sse"  # 上海证券交易所
    SZSE = "szse"  # 深圳证券交易所
    BSE = "bse"  # 北京证券交易所
    HKEX = "hkex"  # 香港交易所
    
    SHFE = "shfe"  # 上海期货交易所
    DCE = "dce"  # 大连商品交易所
    CZCE = "czce"  # 郑州商品交易所
    CFFEX = "cffex"  # 中国金融期货交易所
    INE = "ine"  # 上海国际能源交易中心
    GFEX = "gfex"  # 广州期货交易所
    
    # 监管机构
    CSRC = "csrc"  # 证监会
    CBIRC = "cbirc"  # 银保监会
    PBOC = "pboc"  # 人民银行
    CHINAMONEY = "chinamoney"  # 中国货币网
    
    # 国际数据源
    YAHOO = "yahoo"  # 雅虎财经
    GOOGLE = "google"  # 谷歌财经
    INVESTING = "investing"  # 英为财情
    BLOOMBERG = "bloomberg"  # 彭博
    
    # 其他
    XUEQIU = "xueqiu"  # 雪球
    CAIXIN = "caixin"  # 财新
    BAIDU = "baidu"  # 百度
    DEFAULT = "default"  # 默认


class ProxyConfig:
    """代理配置管理类"""
    
    def __init__(self):
        """初始化代理配置"""
        # 全局默认代理
        self._global_proxy: Optional[Dict[str, str]] = None
        
        # 按网站配置的代理
        self._website_proxies: Dict[str, Dict[str, str]] = {}
        
        # 代理池(支持多个代理轮询)
        self._proxy_pools: Dict[str, List[Dict[str, str]]] = {}
        
        # 代理策略配置
        self._proxy_strategies: Dict[str, str] = {}
        
        # 是否启用代理
        self._enabled: bool = True
        
        # 需要强制使用代理的网站
        self._force_proxy_websites: set = set()
        
        # 禁用代理的网站
        self._disabled_proxy_websites: set = set()
    
    def set_global_proxy(
        self, 
        http: str = None, 
        https: str = None,
        proxies: Dict[str, str] = None
    ) -> None:
        """
        设置全局默认代理
        
        :param http: HTTP 代理地址
        :type http: str
        :param https: HTTPS 代理地址
        :type https: str
        :param proxies: 代理字典 {"http": "...", "https": "..."}
        :type proxies: dict
        """
        if proxies:
            self._global_proxy = proxies
        else:
            self._global_proxy = {}
            if http:
                self._global_proxy['http'] = http
            if https:
                self._global_proxy['https'] = https
    
    def set_website_proxy(
        self,
        website: Union[str, Website],
        http: str = None,
        https: str = None,
        proxies: Dict[str, str] = None
    ) -> None:
        """
        为特定网站设置代理
        
        :param website: 网站标识
        :type website: str or Website
        :param http: HTTP 代理地址
        :type http: str
        :param https: HTTPS 代理地址
        :type https: str
        :param proxies: 代理字典
        :type proxies: dict
        """
        website_key = website.value if isinstance(website, Website) else website
        
        if proxies:
            self._website_proxies[website_key] = proxies
        else:
            proxy_dict = {}
            if http:
                proxy_dict['http'] = http
            if https:
                proxy_dict['https'] = https
            self._website_proxies[website_key] = proxy_dict
    
    def set_proxy_pool(
        self,
        website: Union[str, Website],
        proxies_list: List[Dict[str, str]],
        strategy: str = "random"
    ) -> None:
        """
        为特定网站设置代理池
        
        :param website: 网站标识
        :type website: str or Website
        :param proxies_list: 代理列表
        :type proxies_list: list
        :param strategy: 选择策略 ("random": 随机, "round_robin": 轮询)
        :type strategy: str
        """
        website_key = website.value if isinstance(website, Website) else website
        self._proxy_pools[website_key] = proxies_list
        self._proxy_strategies[website_key] = strategy
    
    def add_proxy_to_pool(
        self,
        website: Union[str, Website],
        proxy: Dict[str, str]
    ) -> None:
        """
        向代理池添加代理
        
        :param website: 网站标识
        :type website: str or Website
        :param proxy: 代理配置
        :type proxy: dict
        """
        website_key = website.value if isinstance(website, Website) else website
        
        if website_key not in self._proxy_pools:
            self._proxy_pools[website_key] = []
        
        self._proxy_pools[website_key].append(proxy)
    
    def force_proxy_for_website(self, website: Union[str, Website]) -> None:
        """
        强制某个网站必须使用代理
        
        :param website: 网站标识
        :type website: str or Website
        """
        website_key = website.value if isinstance(website, Website) else website
        self._force_proxy_websites.add(website_key)
        self._disabled_proxy_websites.discard(website_key)
    
    def disable_proxy_for_website(self, website: Union[str, Website]) -> None:
        """
        禁用某个网站的代理
        
        :param website: 网站标识
        :type website: str or Website
        """
        website_key = website.value if isinstance(website, Website) else website
        self._disabled_proxy_websites.add(website_key)
        self._force_proxy_websites.discard(website_key)
    
    def enable(self) -> None:
        """启用代理系统"""
        self._enabled = True
    
    def disable(self) -> None:
        """禁用代理系统"""
        self._enabled = False
    
    def get_proxy(
        self, 
        website: Union[str, Website] = Website.DEFAULT,
        force: bool = False
    ) -> Optional[Dict[str, str]]:
        """
        获取指定网站的代理配置
        
        :param website: 网站标识
        :type website: str or Website
        :param force: 是否强制返回代理(即使全局禁用)
        :type force: bool
        :return: 代理配置字典,如 {"http": "...", "https": "..."}
        :rtype: dict or None
        """
        website_key = website.value if isinstance(website, Website) else website
        
        # 检查是否禁用代理
        if not self._enabled and not force:
            return None
        
        # 检查该网站是否被禁用代理
        if website_key in self._disabled_proxy_websites:
            return None
        
        # 1. 优先检查代理池
        if website_key in self._proxy_pools and self._proxy_pools[website_key]:
            return self._get_proxy_from_pool(website_key)
        
        # 2. 检查网站特定代理
        if website_key in self._website_proxies:
            return self._website_proxies[website_key].copy()
        
        # 3. 检查是否强制需要代理
        if website_key in self._force_proxy_websites:
            if self._global_proxy:
                return self._global_proxy.copy()
            else:
                raise ValueError(
                    f"网站 '{website_key}' 需要代理,但未配置代理。"
                    f"请使用 set_global_proxy() 或 set_website_proxy() 设置代理。"
                )
        
        # 4. 返回全局代理
        if self._global_proxy:
            return self._global_proxy.copy()
        
        # 5. 无代理配置
        return None
    
    def _get_proxy_from_pool(self, website_key: str) -> Dict[str, str]:
        """
        从代理池中获取代理
        
        :param website_key: 网站标识
        :type website_key: str
        :return: 代理配置
        :rtype: dict
        """
        proxy_pool = self._proxy_pools[website_key]
        strategy = self._proxy_strategies.get(website_key, "random")
        
        if strategy == "random":
            # 随机选择
            return random.choice(proxy_pool).copy()
        elif strategy == "round_robin":
            # 轮询选择 (简单实现,可以优化)
            proxy = proxy_pool[0]
            # 将使用过的代理移到末尾
            self._proxy_pools[website_key] = proxy_pool[1:] + [proxy_pool[0]]
            return proxy.copy()
        else:
            return random.choice(proxy_pool).copy()
    
    def clear(self) -> None:
        """清除所有代理配置"""
        self._global_proxy = None
        self._website_proxies.clear()
        self._proxy_pools.clear()
        self._proxy_strategies.clear()
        self._force_proxy_websites.clear()
        self._disabled_proxy_websites.clear()
    
    def get_config_info(self) -> Dict:
        """
        获取当前代理配置信息
        
        :return: 配置信息字典
        :rtype: dict
        """
        return {
            "enabled": self._enabled,
            "global_proxy": self._global_proxy,
            "website_proxies": list(self._website_proxies.keys()),
            "proxy_pools": {k: len(v) for k, v in self._proxy_pools.items()},
            "force_proxy_websites": list(self._force_proxy_websites),
            "disabled_proxy_websites": list(self._disabled_proxy_websites),
        }


# 全局单例
_proxy_config = ProxyConfig()


def get_proxy(
    website: Union[str, Website] = Website.DEFAULT,
    force: bool = False
) -> Optional[Dict[str, str]]:
    """
    获取指定网站的代理配置(便捷函数)
    
    :param website: 网站标识
    :type website: str or Website
    :param force: 是否强制返回代理
    :type force: bool
    :return: 代理配置字典
    :rtype: dict or None
    
    Example::
    
        from akshare.utils.proxy import get_proxy, Website
        
        # 获取东方财富的代理
        proxies = get_proxy(Website.EASTMONEY)
        
        # 在接口中使用
        r = requests.get(url, params=params, proxies=proxies)
    """
    return _proxy_config.get_proxy(website, force)


def set_global_proxy(
    http: str = None,
    https: str = None,
    proxies: Dict[str, str] = None
) -> None:
    """
    设置全局代理(便捷函数)
    
    :param http: HTTP 代理地址
    :type http: str
    :param https: HTTPS 代理地址
    :type https: str
    :param proxies: 代理字典
    :type proxies: dict
    
    Example::
    
        from akshare.utils.proxy import set_global_proxy
        
        # 方式1: 分别设置
        set_global_proxy(
            http="http://127.0.0.1:7890",
            https="http://127.0.0.1:7890"
        )
        
        # 方式2: 使用字典
        set_global_proxy(proxies={
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        })
    """
    _proxy_config.set_global_proxy(http, https, proxies)


def set_website_proxy(
    website: Union[str, Website],
    http: str = None,
    https: str = None,
    proxies: Dict[str, str] = None
) -> None:
    """
    为特定网站设置代理(便捷函数)
    
    :param website: 网站标识
    :type website: str or Website
    :param http: HTTP 代理地址
    :type http: str
    :param https: HTTPS 代理地址
    :type https: str
    :param proxies: 代理字典
    :type proxies: dict
    
    Example::
    
        from akshare.utils.proxy import set_website_proxy, Website
        
        # 为东方财富设置专用代理
        set_website_proxy(
            Website.EASTMONEY,
            http="http://proxy1.com:8080",
            https="http://proxy1.com:8080"
        )
        
        # 为国际网站设置不同代理
        set_website_proxy(
            Website.YAHOO,
            proxies={
                "http": "http://proxy2.com:1080",
                "https": "http://proxy2.com:1080"
            }
        )
    """
    _proxy_config.set_website_proxy(website, http, https, proxies)


def set_proxy_pool(
    website: Union[str, Website],
    proxies_list: List[Dict[str, str]],
    strategy: str = "random"
) -> None:
    """
    为特定网站设置代理池(便捷函数)
    
    :param website: 网站标识
    :type website: str or Website
    :param proxies_list: 代理列表
    :type proxies_list: list
    :param strategy: 选择策略
    :type strategy: str
    
    Example::
    
        from akshare.utils.proxy import set_proxy_pool, Website
        
        # 为东方财富设置代理池
        proxies = [
            {"http": "http://proxy1:8080", "https": "http://proxy1:8080"},
            {"http": "http://proxy2:8080", "https": "http://proxy2:8080"},
            {"http": "http://proxy3:8080", "https": "http://proxy3:8080"},
        ]
        set_proxy_pool(Website.EASTMONEY, proxies, strategy="random")
    """
    _proxy_config.set_proxy_pool(website, proxies_list, strategy)


def force_proxy_for_website(website: Union[str, Website]) -> None:
    """
    强制某个网站必须使用代理(便捷函数)
    
    :param website: 网站标识
    :type website: str or Website
    
    Example::
    
        from akshare.utils.proxy import force_proxy_for_website, Website
        
        # 强制国际网站使用代理
        force_proxy_for_website(Website.YAHOO)
        force_proxy_for_website(Website.BLOOMBERG)
    """
    _proxy_config.force_proxy_for_website(website)


def disable_proxy_for_website(website: Union[str, Website]) -> None:
    """
    禁用某个网站的代理(便捷函数)
    
    :param website: 网站标识
    :type website: str or Website
    
    Example::
    
        from akshare.utils.proxy import disable_proxy_for_website, Website
        
        # 国内网站不需要代理
        disable_proxy_for_website(Website.EASTMONEY)
        disable_proxy_for_website(Website.SINA)
    """
    _proxy_config.disable_proxy_for_website(website)


def enable_proxy() -> None:
    """启用代理系统(便捷函数)"""
    _proxy_config.enable()


def disable_proxy() -> None:
    """禁用代理系统(便捷函数)"""
    _proxy_config.disable()


def clear_proxy_config() -> None:
    """清除所有代理配置(便捷函数)"""
    _proxy_config.clear()


def get_proxy_config_info() -> Dict:
    """
    获取当前代理配置信息(便捷函数)
    
    :return: 配置信息字典
    :rtype: dict
    """
    return _proxy_config.get_config_info()


# 导出
__all__ = [
    'ProxyType',
    'Website',
    'ProxyConfig',
    'get_proxy',
    'set_global_proxy',
    'set_website_proxy',
    'set_proxy_pool',
    'force_proxy_for_website',
    'disable_proxy_for_website',
    'enable_proxy',
    'disable_proxy',
    'clear_proxy_config',
    'get_proxy_config_info',
]

