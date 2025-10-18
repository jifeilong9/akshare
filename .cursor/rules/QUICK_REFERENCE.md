# AKShare 快速参考卡片

## 🚀 常用命令

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 代码格式化检查
ruff check .

# 自动修复格式问题
ruff check --fix .

# 格式化代码
ruff format .

# 运行特定模块测试
python -m akshare.bond.bond_em

# 安装本地开发版本
pip install -e .
```

## 📝 代码模板

### 新建数据接口

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/17 12:00
Desc: 数据来源描述
https://data.source.com/
"""

import pandas as pd
import requests
from akshare.utils.tqdm import get_tqdm


def data_interface_name(
    symbol: str = "000001",
    start_date: str = "20200101",
) -> pd.DataFrame:
    """
    接口功能描述
    https://data.source.com/
    :param symbol: 标的代码
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :return: 数据说明
    :rtype: pandas.DataFrame
    """
    url = "https://api.example.com/data"
    params = {"symbol": symbol, "startDate": start_date}
    
    r = requests.get(url, params=params)
    data_json = r.json()
    
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.rename(columns={"old": "新列名"}, inplace=True)
    
    # 类型转换
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["价格"] = pd.to_numeric(temp_df["价格"], errors="coerce")
    
    return temp_df


if __name__ == "__main__":
    result_df = data_interface_name()
    print(result_df)
```

## 🔧 常用代码片段

### HTTP 请求

```python
import requests

url = "https://api.example.com/data"
params = {"key": "value"}
r = requests.get(url, params=params, timeout=10)
data_json = r.json()
```

### 分页获取

```python
from akshare.utils.tqdm import get_tqdm

big_df = pd.DataFrame()
tqdm = get_tqdm()

for page in tqdm(range(1, total_pages + 1), leave=False):
    temp_df = fetch_page(page)
    big_df = pd.concat([big_df, temp_df], ignore_index=True)
```

### 数据类型转换

```python
# 数值
df["价格"] = pd.to_numeric(df["价格"], errors="coerce")

# 日期
df["日期"] = pd.to_datetime(df["日期"]).dt.date

# 百分比
df["涨跌幅"] = df["涨跌幅"].str.strip("%")
df["涨跌幅"] = pd.to_numeric(df["涨跌幅"], errors="coerce")
```

### 列重命名

```python
df.rename(
    columns={
        "old_name1": "新名称1",
        "old_name2": "新名称2",
    },
    inplace=True,
)
```

## 📋 Git 工作流

```bash
# 1. 创建新分支
git checkout -b feature/your-feature

# 2. 进行开发...

# 3. 格式化代码
ruff format .

# 4. 提交代码
git add .
git commit -m "feat: 添加 xxx 接口"

# 5. 推送分支
git push origin feature/your-feature

# 6. 在 GitHub 创建 PR
```

## 📊 提交信息规范

| 前缀 | 说明 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: 添加股票行情接口` |
| `fix:` | Bug修复 | `fix: 修复日期解析错误` |
| `docs:` | 文档更新 | `docs: 更新安装说明` |
| `style:` | 代码格式 | `style: 格式化代码` |
| `refactor:` | 代码重构 | `refactor: 优化请求逻辑` |
| `test:` | 测试相关 | `test: 添加单元测试` |
| `chore:` | 构建/工具 | `chore: 更新依赖版本` |

## 🐛 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| 中文乱码 | `r.encoding = "utf-8"` |
| JSON解析失败 | 检查响应内容,可能需要 `demjson` |
| SSL错误 | `verify=False` (不推荐) |
| 数值转换失败 | `pd.to_numeric(..., errors="coerce")` |
| 日期格式问题 | `pd.to_datetime(..., errors="coerce")` |
| 进度条不显示 | 使用 `from akshare.utils.tqdm import get_tqdm` |

## 📦 主要依赖

| 库 | 用途 | 导入 |
|----|------|------|
| pandas | 数据处理 | `import pandas as pd` |
| requests | HTTP请求 | `import requests` |
| beautifulsoup4 | HTML解析 | `from bs4 import BeautifulSoup` |
| lxml | XML解析 | `from lxml import etree` |
| py-mini-racer | JS执行 | `import py_mini_racer` |
| tqdm | 进度条 | `from akshare.utils.tqdm import get_tqdm` |

## 🎯 函数命名规范

格式: `{资产类型}_{地区}_{细分}_{数据源}`

示例:
- `stock_zh_a_hist` - 中国A股历史数据
- `bond_zh_us_rate` - 中美国债收益率
- `fund_em_open_fund` - 东财开放式基金
- `futures_main_sina` - 新浪期货主力

## 📂 项目结构

```
akshare/
├── stock/          # 股票数据
├── fund/           # 基金数据
├── bond/           # 债券数据
├── futures/        # 期货数据
├── option/         # 期权数据
├── forex/          # 外汇数据
├── crypto/         # 加密货币
├── economic/       # 宏观经济
├── index/          # 指数数据
├── utils/          # 工具函数
└── data/           # 数据文件
```

## 🔗 重要链接

- 📖 官方文档: https://akshare.akfamily.xyz/
- 💻 GitHub: https://github.com/akfamily/akshare
- 🐛 问题反馈: https://github.com/akfamily/akshare/issues
- 📧 联系邮箱: albertandking@gmail.com

## 💡 开发小贴士

1. ✅ 使用虚拟环境开发
2. ✅ 提交前运行 `ruff format .`
3. ✅ 函数必须包含完整文档字符串
4. ✅ 使用中文列名
5. ✅ 处理异常和边界情况
6. ✅ 在 `if __name__ == "__main__"` 添加测试
7. ✅ 注明数据来源链接
8. ✅ 数据仅供学术研究使用

## 🎨 代码风格

- 行长度: 最大 88 字符
- 缩进: 4 个空格
- 引号: 双引号 `"`
- 编码: UTF-8
- 工具: Ruff

---

**快速上手**: 阅读 [00-project-overview.mdc](00-project-overview.mdc)

**详细规范**: 查看 [README.md](README.md)

