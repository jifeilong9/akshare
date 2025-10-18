# AKShare 代理配置指南

## 📋 目录

- [简介](#简介)
- [快速开始](#快速开始)
- [代理配置方式](#代理配置方式)
- [高级用法](#高级用法)
- [接口开发指南](#接口开发指南)
- [常见场景](#常见场景)
- [FAQ](#faq)

---

## 简介

AKShare 提供了灵活的代理管理系统,允许:

✅ **全局代理** - 为所有请求设置统一代理  
✅ **网站特定代理** - 为不同数据源配置不同代理  
✅ **代理池** - 支持多个代理轮询使用  
✅ **灵活控制** - 每个接口自主决定是否使用代理  
✅ **强制/禁用** - 可强制某些网站使用或禁用代理

---

## 快速开始

### 基本使用

```python
import akshare as ak
from akshare.utils.proxy import set_global_proxy

# 1. 设置全局代理
set_global_proxy(
    http="http://127.0.0.1:7890",
    https="http://127.0.0.1:7890"
)

# 2. 使用接口(自动应用代理)
df = ak.stock_individual_info_em(symbol="000001")
print(df)
```

### 使用字典方式

```python
from akshare.utils.proxy import set_global_proxy

# 使用字典配置
set_global_proxy(proxies={
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
})
```

---

## 代理配置方式

### 1. 全局代理配置

为所有请求设置统一代理:

```python
from akshare.utils.proxy import set_global_proxy

# 设置 HTTP 和 HTTPS 代理
set_global_proxy(
    http="http://proxy.example.com:8080",
    https="https://proxy.example.com:8080"
)
```

### 2. 网站特定代理

为不同数据源配置不同代理:

```python
from akshare.utils.proxy import set_website_proxy, Website

# 为东方财富设置专用代理
set_website_proxy(
    Website.EASTMONEY,
    http="http://proxy1.com:8080",
    https="http://proxy1.com:8080"
)

# 为雅虎财经设置另一个代理
set_website_proxy(
    Website.YAHOO,
    http="http://proxy2.com:1080",
    https="http://proxy2.com:1080"
)

# 为新浪财经设置代理
set_website_proxy(
    Website.SINA,
    proxies={
        "http": "http://proxy3.com:3128",
        "https": "http://proxy3.com:3128"
    }
)
```

### 3. 代理池配置

配置多个代理,自动轮询或随机选择:

```python
from akshare.utils.proxy import set_proxy_pool, Website

# 准备代理列表
proxies_list = [
    {"http": "http://proxy1:8080", "https": "http://proxy1:8080"},
    {"http": "http://proxy2:8080", "https": "http://proxy2:8080"},
    {"http": "http://proxy3:8080", "https": "http://proxy3:8080"},
]

# 随机选择策略
set_proxy_pool(
    Website.EASTMONEY,
    proxies_list,
    strategy="random"  # 每次随机选择一个代理
)

# 轮询选择策略
set_proxy_pool(
    Website.SINA,
    proxies_list,
    strategy="round_robin"  # 依次轮询使用代理
)
```

---

## 高级用法

### 强制使用代理

某些国际网站必须使用代理才能访问:

```python
from akshare.utils.proxy import (
    force_proxy_for_website,
    set_global_proxy,
    Website
)

# 设置全局代理
set_global_proxy(
    http="http://127.0.0.1:7890",
    https="http://127.0.0.1:7890"
)

# 强制国际网站使用代理
force_proxy_for_website(Website.YAHOO)
force_proxy_for_website(Website.BLOOMBERG)
force_proxy_for_website(Website.INVESTING)

# 如果没有配置代理,访问这些网站会抛出异常
```

### 禁用特定网站代理

某些网站不需要或不支持代理:

```python
from akshare.utils.proxy import disable_proxy_for_website, Website

# 国内网站通常不需要代理
disable_proxy_for_website(Website.EASTMONEY)
disable_proxy_for_website(Website.SINA)
disable_proxy_for_website(Website.CNINFO)

# 即使设置了全局代理,这些网站也不会使用
```

### 启用/禁用代理系统

临时禁用所有代理:

```python
from akshare.utils.proxy import enable_proxy, disable_proxy

# 禁用代理系统
disable_proxy()

# ... 进行一些不需要代理的操作 ...

# 重新启用代理系统
enable_proxy()
```

### 查看代理配置

查看当前代理配置状态:

```python
from akshare.utils.proxy import get_proxy_config_info

# 获取配置信息
config_info = get_proxy_config_info()
print(config_info)

# 输出示例:
# {
#     "enabled": True,
#     "global_proxy": {"http": "...", "https": "..."},
#     "website_proxies": ["eastmoney", "yahoo"],
#     "proxy_pools": {"sina": 3},  # sina 有3个代理
#     "force_proxy_websites": ["yahoo", "bloomberg"],
#     "disabled_proxy_websites": ["cninfo"]
# }
```

### 清除所有配置

```python
from akshare.utils.proxy import clear_proxy_config

# 清除所有代理配置,恢复默认状态
clear_proxy_config()
```

---

## 接口开发指南

### 在新接口中集成代理支持

开发新接口时,按以下方式集成代理:

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 23:00
Desc: 示例接口 - 演示如何集成代理支持
"""

import pandas as pd
import requests

from akshare.utils.proxy import get_proxy, Website


def example_data_interface(symbol: str = "000001") -> pd.DataFrame:
    """
    示例数据接口
    :param symbol: 股票代码
    :type symbol: str
    :return: 数据
    :rtype: pandas.DataFrame
    """
    url = "https://data.eastmoney.com/api/data"
    params = {"symbol": symbol}
    
    # 关键步骤: 获取该网站的代理配置
    proxies = get_proxy(Website.EASTMONEY)
    
    # 在请求中使用代理
    r = requests.get(url, params=params, proxies=proxies)
    data_json = r.json()
    
    # 数据处理...
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df
```

### 支持的网站标识

使用 `Website` 枚举类选择合适的网站标识:

```python
from akshare.utils.proxy import Website

# 财经数据源
Website.EASTMONEY      # 东方财富
Website.SINA           # 新浪财经
Website.TENCENT        # 腾讯财经
Website.TONGHUASHUN    # 同花顺
Website.CNINFO         # 巨潮资讯

# 交易所
Website.SSE            # 上海证券交易所
Website.SZSE           # 深圳证券交易所
Website.BSE            # 北京证券交易所
Website.HKEX           # 香港交易所

Website.SHFE           # 上海期货交易所
Website.DCE            # 大连商品交易所
Website.CZCE           # 郑州商品交易所
Website.CFFEX          # 中国金融期货交易所
Website.INE            # 上海国际能源交易中心
Website.GFEX           # 广州期货交易所

# 监管机构
Website.CSRC           # 证监会
Website.CBIRC          # 银保监会
Website.PBOC           # 人民银行
Website.CHINAMONEY     # 中国货币网

# 国际数据源
Website.YAHOO          # 雅虎财经
Website.GOOGLE         # 谷歌财经
Website.INVESTING      # 英为财情
Website.BLOOMBERG      # 彭博

# 其他
Website.XUEQIU         # 雪球
Website.CAIXIN         # 财新
Website.BAIDU          # 百度
Website.DEFAULT        # 默认(使用全局代理)
```

### 使用字符串标识

也可以使用字符串作为网站标识:

```python
from akshare.utils.proxy import get_proxy

# 使用字符串
proxies = get_proxy("eastmoney")
proxies = get_proxy("sina")

# 或使用枚举(推荐)
from akshare.utils.proxy import Website
proxies = get_proxy(Website.EASTMONEY)
```

---

## 常见场景

### 场景1: 国内用户访问国内网站

```python
import akshare as ak

# 不需要配置代理,直接使用
df = ak.stock_individual_info_em(symbol="000001")
```

### 场景2: 国内用户访问国际网站

```python
from akshare.utils.proxy import set_global_proxy, force_proxy_for_website, Website

# 设置代理
set_global_proxy(
    http="http://127.0.0.1:7890",
    https="http://127.0.0.1:7890"
)

# 强制国际网站使用代理
force_proxy_for_website(Website.YAHOO)
force_proxy_for_website(Website.BLOOMBERG)

# 使用国际数据接口
df = ak.stock_us_daily(symbol="AAPL")
```

### 场景3: 海外用户访问国内网站

```python
from akshare.utils.proxy import set_global_proxy

# 使用国内代理服务器
set_global_proxy(
    http="http://china-proxy.com:8080",
    https="http://china-proxy.com:8080"
)

# 访问国内数据
df = ak.stock_zh_a_hist(symbol="000001")
```

### 场景4: 企业环境(需要经过公司代理)

```python
from akshare.utils.proxy import set_global_proxy

# 配置公司代理
set_global_proxy(
    http="http://proxy.company.com:8080",
    https="http://proxy.company.com:8080"
)

# 所有请求都会通过公司代理
df = ak.stock_individual_info_em(symbol="000001")
```

### 场景5: 混合场景(部分网站需要代理)

```python
from akshare.utils.proxy import (
    set_website_proxy,
    disable_proxy_for_website,
    Website
)

# 仅为国际网站配置代理
set_website_proxy(
    Website.YAHOO,
    http="http://127.0.0.1:7890",
    https="http://127.0.0.1:7890"
)

set_website_proxy(
    Website.BLOOMBERG,
    http="http://127.0.0.1:7890",
    https="http://127.0.0.1:7890"
)

# 国内网站明确禁用代理
disable_proxy_for_website(Website.EASTMONEY)
disable_proxy_for_website(Website.SINA)

# 使用时自动判断
df1 = ak.stock_individual_info_em(symbol="000001")  # 不使用代理
df2 = ak.stock_us_daily(symbol="AAPL")  # 使用代理
```

### 场景6: 使用代理池(防止单个代理被封)

```python
from akshare.utils.proxy import set_proxy_pool, Website

# 准备多个代理
proxy_list = [
    {"http": "http://proxy1:8080", "https": "http://proxy1:8080"},
    {"http": "http://proxy2:8080", "https": "http://proxy2:8080"},
    {"http": "http://proxy3:8080", "https": "http://proxy3:8080"},
]

# 为东方财富设置代理池
set_proxy_pool(Website.EASTMONEY, proxy_list, strategy="random")

# 每次请求会随机选择一个代理
for i in range(10):
    df = ak.stock_individual_info_em(symbol=f"00000{i}")
    # 每次使用不同的代理
```

---

## FAQ

### Q1: 如何知道我的代理是否生效?

```python
from akshare.utils.proxy import get_proxy, Website

# 查看特定网站的代理配置
proxies = get_proxy(Website.EASTMONEY)
print(f"东方财富代理配置: {proxies}")

# 查看所有配置
from akshare.utils.proxy import get_proxy_config_info
print(get_proxy_config_info())
```

### Q2: 代理配置优先级是什么?

优先级从高到低:
1. 代理池 (网站特定)
2. 网站特定代理
3. 全局代理
4. 无代理

### Q3: 如何为新的数据源添加网站标识?

编辑 `akshare/utils/proxy.py`,在 `Website` 枚举中添加:

```python
class Website(Enum):
    # ... 现有网站 ...
    NEW_WEBSITE = "new_website"  # 新增
```

### Q4: SOCKS5 代理怎么配置?

```python
from akshare.utils.proxy import set_global_proxy

# SOCKS5 代理
set_global_proxy(proxies={
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
})

# 注意: 需要安装 requests[socks]
# pip install requests[socks]
```

### Q5: 代理需要认证怎么办?

```python
from akshare.utils.proxy import set_global_proxy

# 带认证的代理
set_global_proxy(proxies={
    "http": "http://username:password@proxy.com:8080",
    "https": "http://username:password@proxy.com:8080"
})
```

### Q6: 如何临时不使用代理?

```python
from akshare.utils.proxy import disable_proxy, enable_proxy

# 方法1: 临时禁用
disable_proxy()
df = ak.stock_individual_info_em(symbol="000001")
enable_proxy()

# 方法2: 使用上下文管理器
from akshare.utils.context import ProxyContext

with ProxyContext(None):  # None 表示不使用代理
    df = ak.stock_individual_info_em(symbol="000001")
```

### Q7: 遇到代理错误怎么办?

```python
import akshare as ak
from requests.exceptions import ProxyError

try:
    df = ak.stock_individual_info_em(symbol="000001")
except ProxyError as e:
    print(f"代理错误: {e}")
    print("请检查:")
    print("1. 代理服务器是否正常运行")
    print("2. 代理地址和端口是否正确")
    print("3. 网络是否可达代理服务器")
```

### Q8: 如何测试代理是否可用?

```python
import requests

def test_proxy(proxy_url):
    """测试代理是否可用"""
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        r = requests.get(
            "http://httpbin.org/ip",
            proxies=proxies,
            timeout=10
        )
        print(f"代理可用! IP: {r.json()['origin']}")
        return True
    except Exception as e:
        print(f"代理不可用: {e}")
        return False

# 测试
test_proxy("http://127.0.0.1:7890")
```

---

## 最佳实践

### 1. 合理配置

```python
# ✅ 好的做法: 按需配置
from akshare.utils.proxy import set_website_proxy, Website

# 仅为需要的网站配置代理
set_website_proxy(Website.YAHOO, proxies={"http": "...", "https": "..."})

# ❌ 不好的做法: 全部使用代理(可能影响性能)
set_global_proxy(proxies={"http": "...", "https": "..."})
```

### 2. 使用枚举

```python
# ✅ 好的做法: 使用枚举
from akshare.utils.proxy import get_proxy, Website
proxies = get_proxy(Website.EASTMONEY)

# ❌ 不好的做法: 使用字符串(容易拼写错误)
proxies = get_proxy("eastmoney")  # 可能拼错
```

### 3. 异常处理

```python
# ✅ 好的做法: 处理代理异常
from requests.exceptions import ProxyError, ConnectTimeout

try:
    df = ak.stock_individual_info_em(symbol="000001")
except (ProxyError, ConnectTimeout) as e:
    print(f"代理相关错误: {e}")
    # 尝试不使用代理重试
    from akshare.utils.proxy import disable_proxy
    disable_proxy()
    df = ak.stock_individual_info_em(symbol="000001")
```

---

## 相关资源

- **项目文档**: https://akshare.akfamily.xyz/
- **GitHub**: https://github.com/akfamily/akshare
- **代理服务推荐**:
  - Clash: https://github.com/Dreamacro/clash
  - V2Ray: https://www.v2ray.com/
  - Shadowsocks: https://shadowsocks.org/

---

**更新日期**: 2025-10-17  
**维护**: AKShare 开发团队

