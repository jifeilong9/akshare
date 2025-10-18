# AKShare 项目代码结构详细文档

> **版本**: 基于当前代码结构生成  
> **更新日期**: 2025-10-17  
> **项目地址**: https://github.com/akfamily/akshare

---

## 📋 目录

- [项目概述](#项目概述)
- [核心入口](#核心入口)
- [目录结构总览](#目录结构总览)
- [核心模块详解](#核心模块详解)
  - [股票模块 (stock)](#股票模块-stock)
  - [基金模块 (fund)](#基金模块-fund)
  - [债券模块 (bond)](#债券模块-bond)
  - [期货模块 (futures)](#期货模块-futures)
  - [期权模块 (option)](#期权模块-option)
  - [指数模块 (index)](#指数模块-index)
  - [宏观经济模块 (economic)](#宏观经济模块-economic)
  - [外汇模块 (forex)](#外汇模块-forex)
  - [加密货币模块 (crypto)](#加密货币模块-crypto)
- [辅助模块](#辅助模块)
- [工具模块 (utils)](#工具模块-utils)
- [数据文件 (data)](#数据文件-data)
- [模块依赖关系](#模块依赖关系)

---

## 项目概述

**AKShare** 是一个开源财经数据接口库,提供股票、期货、期权、基金、债券、外汇、加密货币等金融产品数据。

**核心特点**:
- 📦 **模块化设计**: 按资产类型组织,职责清晰
- 🔌 **统一接口**: 所有函数返回 pandas.DataFrame
- 🌐 **多数据源**: 东方财富、新浪财经、同花顺等
- 🔧 **易于扩展**: 标准化的开发模式

---

## 核心入口

### `akshare/__init__.py`

**作用**: 项目主入口文件,导出所有公共 API 接口

**主要功能**:
1. **版本管理**: 定义 `__version__` 变量
2. **接口导出**: 从各子模块导入函数并通过 `__all__` 导出
3. **版本历史**: 包含详细的版本更新记录

**代码结构**:
```python
# 版本号
__version__ = "X.Y.Z"

# 从各模块导入
from akshare.stock.stock_zh_a_sina import stock_zh_a_hist
from akshare.fund.fund_em import fund_em_open_fund_daily
# ... 更多导入

# 导出列表
__all__ = [
    "stock_zh_a_hist",
    "fund_em_open_fund_daily",
    # ... 所有公共接口
]
```

**使用方式**:
```python
import akshare as ak

# 调用任意接口
df = ak.stock_zh_a_hist(symbol="000001")
```

---

## 目录结构总览

```
akshare/
├── 📄 __init__.py              # ⭐ 主入口,导出所有公共接口
├── 📄 datasets.py              # 数据集示例和辅助函数
├── 📄 request.py               # HTTP 请求封装
├── 📄 exceptions.py            # 自定义异常类
│
├── 📁 stock/                   # 📈 股票数据 (59 文件)
├── 📁 fund/                    # 💰 基金数据 (18 文件)
├── 📁 bond/                    # 📊 债券数据 (15 文件)
├── 📁 futures/                 # 🌾 期货数据 (29 文件)
├── 📁 option/                  # 📉 期权数据 (18 文件)
├── 📁 index/                   # 📊 指数数据 (27 文件)
├── 📁 economic/                # 🌍 宏观经济数据 (17 文件)
├── 📁 forex/                   # 💱 外汇数据 (3 文件)
├── 📁 crypto/                  # 🪙 加密货币数据 (3 文件)
│
├── 📁 stock_feature/           # 📈 股票特征因子 (69 文件)
├── 📁 stock_fundamental/       # 📊 股票基本面 (20 文件)
├── 📁 stock_a/                 # 📈 A股特定数据 (4 文件)
│
├── 📁 futures_derivative/      # 🌾 期货衍生品 (12 文件)
├── 📁 interest_rate/           # 💹 利率数据 (2 文件)
├── 📁 reits/                   # 🏢 REITs数据 (2 文件)
│
├── 📁 bank/                    # 🏦 银行数据 (3 文件)
├── 📁 energy/                  # ⚡ 能源数据 (3 文件)
├── 📁 spot/                    # 📦 现货数据 (4 文件)
├── 📁 currency/                # 💴 货币数据 (4 文件)
│
├── 📁 fortune/                 # 💎 财富榜单 (6 文件)
├── 📁 news/                    # 📰 新闻数据 (4 文件)
├── 📁 movie/                   # 🎬 电影票房 (5 文件)
├── 📁 event/                   # 🚗 事件数据 (3 文件)
├── 📁 air/                     # 🌫️ 空气质量 (7 文件)
├── 📁 cost/                    # 💵 生活成本 (2 文件)
│
├── 📁 article/                 # 📚 学术数据 (6 文件)
├── 📁 hf/                      # 📊 对冲基金 (2 文件)
├── 📁 nlp/                     # 🤖 自然语言处理 (2 文件)
├── 📁 cal/                     # 📅 日历计算 (2 文件)
│
├── 📁 qhkc/                    # 奇货可查 (2 文件)
├── 📁 qhkc_web/                # 奇货可查网页版 (4 文件)
├── 📁 qdii/                    # QDII 基金 (2 文件)
├── 📁 fx/                      # 外汇增强 (6 文件)
├── 📁 pro/                     # 专业版接口 (4 文件)
├── 📁 rate/                    # 利率数据 (2 文件)
├── 📁 other/                   # 其他数据 (3 文件)
├── 📁 tool/                    # 工具函数 (2 文件)
│
├── 📁 utils/                   # 🔧 工具模块 (8 文件)
├── 📁 data/                    # 📦 数据文件和 JS 脚本
└── 📁 file_fold/               # 📂 文件资源 (配置文件)
```

**统计**:
- **总模块数**: 40+ 个功能模块
- **总文件数**: 400+ 个 Python 文件
- **代码行数**: 10万+ 行
- **接口数量**: 3000+ 个数据接口

---

## 核心模块详解

### 股票模块 (stock/)

**目录**: `akshare/stock/` (59 个文件)

**作用**: 提供股票市场相关数据,包括 A股、港股、美股等

#### 文件清单及功能

| 文件名 | 主要功能 | 数据源 |
|--------|---------|--------|
| `__init__.py` | 模块初始化,导出接口 | - |
| `cons.py` | 股票相关常量定义 | - |
| **A股数据** |||
| `stock_zh_a_sina.py` | A股历史行情数据 | 新浪财经 |
| `stock_zh_a_special.py` | A股特殊数据(停复牌等) | 多源 |
| `stock_zh_a_tick_tx.py` | A股分笔数据 | 腾讯财经 |
| `stock_zh_b_sina.py` | B股历史行情数据 | 新浪财经 |
| `stock_zh_ah_tx.py` | AH股比价数据 | 腾讯财经 |
| `stock_zh_comparison_em.py` | A股对比分析 | 东方财富 |
| `stock_zh_kcb_sina.py` | 科创板数据 | 新浪财经 |
| `stock_zh_kcb_report.py` | 科创板报告 | 多源 |
| **港股数据** |||
| `stock_hk_sina.py` | 港股历史行情 | 新浪财经 |
| `stock_hk_famous.py` | 港股知名公司数据 | 多源 |
| `stock_hk_fhpx_ths.py` | 港股分红排行 | 同花顺 |
| `stock_hk_hot_rank_em.py` | 港股热度排行 | 东方财富 |
| `stock_hk_comparison_em.py` | 港股对比分析 | 东方财富 |
| **美股数据** |||
| `stock_us_sina.py` | 美股历史行情 | 新浪财经 |
| `stock_us_famous.py` | 美股知名公司 | 多源 |
| `stock_us_js.py` | 美股 JavaScript 接口 | 多源 |
| `stock_us_pink.py` | 美股粉单市场 | 多源 |
| **实时行情** |||
| `stock_intraday_em.py` | 盘中分时数据 | 东方财富 |
| `stock_intraday_sina.py` | 盘中实时数据 | 新浪财经 |
| `stock_ask_bid_em.py` | 买卖盘口数据 | 东方财富 |
| **行情统计** |||
| `stock_info_em.py` | 股票基本信息 | 东方财富 |
| `stock_info.py` | 股票信息汇总 | 多源 |
| `stock_summary.py` | 市场概况统计 | 多源 |
| **板块数据** |||
| `stock_board_concept_em.py` | 概念板块数据 | 东方财富 |
| `stock_board_industry_em.py` | 行业板块数据 | 东方财富 |
| `stock_industry_cninfo.py` | 行业分类 | 巨潮资讯 |
| `stock_industry_pe_cninfo.py` | 行业市盈率 | 巨潮资讯 |
| `stock_industry_sw.py` | 申万行业分类 | 申万 |
| `stock_industry.py` | 行业数据汇总 | 多源 |
| **热度排名** |||
| `stock_hot_rank_em.py` | 股票热度排行 | 东方财富 |
| `stock_hot_search_baidu.py` | 百度搜索热度 | 百度 |
| `stock_hot_up_em.py` | 热门涨停股 | 东方财富 |
| **资金流向** |||
| `stock_fund_em.py` | 资金流向数据 | 东方财富 |
| `stock_fund_hold.py` | 基金持仓数据 | 多源 |
| `stock_hsgt_em.py` | 沪深港通资金 | 东方财富 |
| `stock_dzjy_em.py` | 大宗交易数据 | 东方财富 |
| **股东持股** |||
| `stock_hold_control_cninfo.py` | 控股情况 | 巨潮资讯 |
| `stock_hold_control_em.py` | 控股变动 | 东方财富 |
| `stock_hold_num_cninfo.py` | 股东人数 | 巨潮资讯 |
| `stock_share_hold.py` | 股东持股明细 | 多源 |
| `stock_share_changes_cninfo.py` | 股本变动 | 巨潮资讯 |
| **公司行为** |||
| `stock_dividend_cninfo.py` | 分红送股 | 巨潮资讯 |
| `stock_allotment_cninfo.py` | 配股数据 | 巨潮资讯 |
| `stock_repurchase_em.py` | 股票回购 | 东方财富 |
| `stock_ipo_summary_cninfo.py` | IPO 汇总 | 巨潮资讯 |
| `stock_new_cninfo.py` | 新股数据 | 巨潮资讯 |
| **公司治理** |||
| `stock_cg_equity_mortgage.py` | 股权质押 | 多源 |
| `stock_cg_guarantee.py` | 对外担保 | 多源 |
| `stock_cg_lawsuit.py` | 诉讼仲裁 | 多源 |
| **公司信息** |||
| `stock_profile_cninfo.py` | 公司简介 | 巨潮资讯 |
| `stock_profile_em.py` | 公司概况 | 东方财富 |
| **新闻舆情** |||
| `stock_news_cx.py` | 财新新闻 | 财新网 |
| `stock_weibo_nlp.py` | 微博舆情分析 | 微博 |
| `stock_xq.py` | 雪球数据 | 雪球 |
| `stock_gsrl_em.py` | 股市日历 | 东方财富 |
| **其他** |||
| `stock_stop.py` | 停复牌信息 | 多源 |
| `stock_rank_forecast.py` | 业绩预告排名 | 多源 |

#### 典型函数示例

```python
# 获取A股历史数据
def stock_zh_a_hist(
    symbol: str = "000001",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "20500101",
    adjust: str = ""
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日行情
    """
```

---

### 基金模块 (fund/)

**目录**: `akshare/fund/` (18 个文件)

**作用**: 提供公募基金、私募基金、ETF 等数据

#### 文件清单及功能

| 文件名 | 主要功能 | 数据源 |
|--------|---------|--------|
| `__init__.py` | 模块初始化 | - |
| **开放式基金** |||
| `fund_em.py` | 东财基金数据(核心) | 东方财富 |
| `fund_overview_em.py` | 基金概览数据 | 东方财富 |
| `fund_rank_em.py` | 基金排行榜 | 东方财富 |
| `fund_rating.py` | 基金评级数据 | 多源 |
| `fund_scale_em.py` | 基金规模数据 | 东方财富 |
| `fund_scale_sina.py` | 基金规模(新浪) | 新浪财经 |
| `fund_aum_em.py` | 资产管理规模 | 东方财富 |
| **ETF 基金** |||
| `fund_etf_em.py` | ETF 数据(东财) | 东方财富 |
| `fund_etf_sina.py` | ETF 数据(新浪) | 新浪财经 |
| `fund_etf_ths.py` | ETF 数据(同花顺) | 同花顺 |
| **LOF 基金** |||
| `fund_lof_em.py` | LOF 基金数据 | 东方财富 |
| **基金经理** |||
| `fund_manager.py` | 基金经理数据 | 多源 |
| **基金持仓** |||
| `fund_portfolio_em.py` | 基金持仓明细 | 东方财富 |
| `fund_position_lg.py` | 基金仓位数据 | 理杏仁 |
| **私募基金** |||
| `fund_amac.py` | 私募基金(协会) | 中基协 |
| **其他** |||
| `fund_fee_em.py` | 基金费率 | 东方财富 |
| `fund_fhsp_em.py` | 基金分红送配 | 东方财富 |
| `fund_init_em.py` | 基金初始数据 | 东方财富 |
| `fund_announcement_em.py` | 基金公告 | 东方财富 |
| `fund_report_cninfo.py` | 基金报告 | 巨潮资讯 |
| `fund_xq.py` | 雪球基金数据 | 雪球 |

#### 典型函数示例

```python
# 获取开放式基金净值
def fund_open_fund_info_em(
    symbol: str = "000001",
    indicator: str = "单位净值走势"
) -> pd.DataFrame:
    """
    天天基金网-基金数据
    """
```

---

### 债券模块 (bond/)

**目录**: `akshare/bond/` (15 个文件)

**作用**: 提供国债、企业债、可转债等债券数据

#### 文件清单及功能

| 文件名 | 主要功能 | 数据源 |
|--------|---------|--------|
| `__init__.py` | 模块初始化 | - |
| `cons.py` | 债券常量定义 | - |
| **国债数据** |||
| `bond_em.py` | 中美国债收益率 | 东方财富 |
| `bond_china.py` | 中国国债数据 | 多源 |
| `bond_china_money.py` | 银行间债券市场 | 中国货币网 |
| **可转债** |||
| `bond_cb_sina.py` | 可转债数据(新浪) | 新浪财经 |
| `bond_cb_ths.py` | 可转债数据(同花顺) | 同花顺 |
| `bond_convert.py` | 可转债转股数据 | 多源 |
| `bond_zh_cov.py` | 可转债汇总 | 多源 |
| **企业债** |||
| `bond_cbond.py` | 企业债数据 | 中国债券信息网 |
| `bond_nafmii.py` | 交易商协会债券 | 交易商协会 |
| **其他债券** |||
| `bond_buy_back_em.py` | 债券回购 | 东方财富 |
| `bond_zh_sina.py` | 债券行情(新浪) | 新浪财经 |
| `bond_summary.py` | 债券市场概况 | 多源 |
| `bond_info_cm.py` | 债券信息 | 中国货币网 |
| `bond_issue_cninfo.py` | 债券发行 | 巨潮资讯 |

---

### 期货模块 (futures/)

**目录**: `akshare/futures/` (29 个文件)

**作用**: 提供商品期货、金融期货等数据

#### 文件清单及功能

| 文件名 | 主要功能 | 数据源 |
|--------|---------|--------|
| `__init__.py` | 模块初始化 | - |
| `cons.py` | 期货常量定义 | - |
| **期货行情** |||
| `futures_zh_sina.py` | 期货行情(新浪) | 新浪财经 |
| `futures_hq_sina.py` | 期货实时行情 | 新浪财经 |
| `futures_hist_em.py` | 期货历史数据 | 东方财富 |
| `futures_daily_bar.py` | 期货日K线 | 多源 |
| `futures_hf_em.py` | 期货高频数据 | 东方财富 |
| **期货基础** |||
| `futures_comm_qihuo.py` | 期货品种信息 | 期货网 |
| `futures_comm_ctp.py` | CTP 期货合约 | CTP |
| `futures_contract_detail.py` | 合约详情 | 多源 |
| `symbol_var.py` | 品种变量映射 | - |
| **期货分析** |||
| `futures_basis.py` | 期货基差数据 | 多源 |
| `futures_roll_yield.py` | 展期收益率 | 多源 |
| `futures_to_spot.py` | 期现价差 | 多源 |
| `futures_spot_stock_em.py` | 现货库存 | 东方财富 |
| **持仓数据** |||
| `cot.py` | 持仓报告(COT) | CFTC |
| **库存数据** |||
| `futures_inventory_99.py` | 99期货库存 | 99期货 |
| `futures_inventory_em.py` | 东财库存数据 | 东方财富 |
| `receipt.py` | 仓单数据 | 交易所 |
| `futures_warehouse_receipt.py` | 仓单统计 | 交易所 |
| **外盘期货** |||
| `futures_foreign.py` | 外盘期货数据 | 多源 |
| `futures_comex_em.py` | COMEX 期货 | 东方财富 |
| `futures_settlement_price_sgx.py` | 新加坡结算价 | SGX |
| **期货指数** |||
| `futures_index_ccidx.py` | 期货指数 | CCIDX |
| **其他** |||
| `futures_rule.py` | 交易规则 | 交易所 |
| `futures_rule_em.py` | 交易规则(东财) | 东方财富 |
| `futures_news_shmet.py` | 期货资讯 | 上海金属网 |
| `futures_stock_js.py` | 期货持仓JS | 多源 |
| `requests_fun.py` | 请求封装 | - |

---

### 期权模块 (option/)

**目录**: `akshare/option/` (18 个文件)

**作用**: 提供股票期权、商品期权数据

#### 主要文件

- `option_dce_*.py` - 大连商品交易所期权
- `option_czce_*.py` - 郑州商品交易所期权  
- `option_shfe_*.py` - 上海期货交易所期权
- `option_cffex_*.py` - 中国金融期货交易所期权
- `option_sse_*.py` - 上海证券交易所股票期权
- `option_szse_*.py` - 深圳证券交易所股票期权

---

### 指数模块 (index/)

**目录**: `akshare/index/` (27 个文件)

**作用**: 提供各类指数数据

#### 文件清单及功能

| 文件名 | 主要功能 | 数据源 |
|--------|---------|--------|
| `__init__.py` | 模块初始化 | - |
| `cons.py` | 指数常量定义 | - |
| **A股指数** |||
| `index_zh_em.py` | A股指数(东财) | 东方财富 |
| `index_stock_zh.py` | 股票指数汇总 | 多源 |
| `index_stock_zh_csindex.py` | 中证指数 | 中证指数公司 |
| `index_sw.py` | 申万指数 | 申万 |
| `index_zh_a_scope.py` | A股指数成分 | 多源 |
| **港股指数** |||
| `index_stock_hk.py` | 港股指数 | 多源 |
| **美股指数** |||
| `index_stock_us_sina.py` | 美股指数 | 新浪财经 |
| **全球指数** |||
| `index_global_em.py` | 全球指数(东财) | 东方财富 |
| `index_global_sina.py` | 全球指数(新浪) | 新浪财经 |
| **行业指数** |||
| `index_cni.py` | 国证指数 | 国证指数公司 |
| `index_csindex.py` | 中证指数详情 | 中证指数 |
| **商品指数** |||
| `index_spot.py` | 现货指数 | 多源 |
| `index_sugar.py` | 糖业指数 | 多源 |
| `index_hog.py` | 生猪指数 | 多源 |
| `index_yw.py` | 义乌小商品指数 | 义乌指数 |
| **研究指数** |||
| `index_research_sw.py` | 申万研究指数 | 申万 |
| `index_research_fund_sw.py` | 申万基金指数 | 申万 |
| **其他指数** |||
| `index_cx.py` | 财新指数 | 财新 |
| `index_drewry.py` | Drewry 航运指数 | Drewry |
| `index_cflp.py` | 物流指数 | 中物联 |
| `index_eri.py` | ERI 指数 | - |
| `index_option_qvix.py` | 期权波动率指数 | 交易所 |
| `index_kq_fz.py` | 快期期指 | 快期 |
| `index_kq_ss.py` | 快期闪送 | 快期 |
| `index_cons.py` | 指数常量 | - |

---

### 宏观经济模块 (economic/)

**目录**: `akshare/economic/` (17 个文件)

**作用**: 提供全球宏观经济数据

#### 文件清单及功能

| 文件名 | 主要功能 | 覆盖指标 |
|--------|---------|---------|
| `__init__.py` | 模块初始化 | - |
| `cons.py` | 经济数据常量 | - |
| **中国** |||
| `macro_china.py` | 中国宏观数据(核心) | CPI、PPI、PMI、GDP等 |
| `macro_china_nbs.py` | 国家统计局数据 | 官方统计数据 |
| `macro_china_hk.py` | 香港宏观数据 | 香港经济指标 |
| `marco_cnbs.py` | 国家统计局 | 全面统计数据 |
| **美国** |||
| `macro_usa.py` | 美国宏观数据 | 非农、失业率、CPI、GDP |
| **欧洲** |||
| `macro_euro.py` | 欧元区宏观数据 | 欧洲央行数据 |
| `macro_uk.py` | 英国宏观数据 | 英国经济指标 |
| `macro_germany.py` | 德国宏观数据 | 德国经济指标 |
| **亚太** |||
| `macro_japan.py` | 日本宏观数据 | 日本经济指标 |
| `macro_australia.py` | 澳大利亚宏观数据 | 澳洲经济指标 |
| **其他** |||
| `macro_canada.py` | 加拿大宏观数据 | 加拿大指标 |
| `macro_swiss.py` | 瑞士宏观数据 | 瑞士指标 |
| **金融** |||
| `macro_bank.py` | 银行数据 | 银行业指标 |
| `macro_finance_ths.py` | 金融数据(同花顺) | 金融市场数据 |
| **综合** |||
| `macro_constitute.py` | 宏观数据构成 | 综合指标 |
| `macro_other.py` | 其他宏观数据 | 其他国家 |
| `macro_info_ws.py` | 宏观信息 | Wind 数据 |

---

### 外汇模块 (forex/)

**目录**: `akshare/forex/` (3 个文件)

**作用**: 提供外汇汇率、外汇行情数据

#### 文件清单

| 文件名 | 主要功能 |
|--------|---------|
| `__init__.py` | 模块初始化 |
| `cons.py` | 外汇常量 |
| `forex_em.py` | 外汇行情数据(东财) |

---

### 加密货币模块 (crypto/)

**目录**: `akshare/crypto/` (3 个文件)

**作用**: 提供比特币、以太坊等加密货币数据

#### 文件清单

| 文件名 | 主要功能 |
|--------|---------|
| `__init__.py` | 模块初始化 |
| `crypto_bitcoin_cme.py` | CME 比特币期货 |
| `crypto_hold.py` | 加密货币持仓 |

---

## 辅助模块

### 股票特征因子 (stock_feature/)

**文件数**: 69 个

**作用**: 提供股票技术指标、因子数据、量化特征

**主要内容**:
- 技术指标计算
- 因子数据获取
- 量化特征提取
- 回测数据支持

### 股票基本面 (stock_fundamental/)

**文件数**: 20 个

**作用**: 提供财务报表、业绩数据等基本面信息

**主要内容**:
- 资产负债表
- 利润表
- 现金流量表
- 财务指标
- 业绩预告

### 期货衍生品 (futures_derivative/)

**文件数**: 12 个

**作用**: 期货合约信息、持仓分析

**主要文件**:
- `futures_contract_info_*.py` - 各交易所合约信息
- `futures_cot_sina.py` - 持仓报告
- `futures_index_sina.py` - 期货指数
- `futures_hog.py` - 生猪期货
- `futures_spot_sys.py` - 期现系统

### 其他专项模块

| 模块 | 文件数 | 主要功能 |
|------|--------|---------|
| `bank/` | 3 | 银行业监管数据 |
| `energy/` | 3 | 能源数据(碳排放、石油) |
| `spot/` | 4 | 现货市场数据 |
| `currency/` | 4 | 货币数据、汇率 |
| `fortune/` | 6 | 财富榜单(福布斯、胡润等) |
| `news/` | 4 | 财经新闻 |
| `movie/` | 5 | 电影票房数据 |
| `event/` | 3 | 事件数据(疫情迁徙等) |
| `air/` | 7 | 空气质量数据 |
| `cost/` | 2 | 生活成本指数 |
| `article/` | 6 | 学术数据(Fama-French因子等) |
| `hf/` | 2 | 对冲基金数据 |
| `nlp/` | 2 | 自然语言处理接口 |
| `cal/` | 2 | 日历计算(交易日等) |
| `interest_rate/` | 2 | 利率数据 |
| `reits/` | 2 | REITs 数据 |
| `qdii/` | 2 | QDII 基金 |
| `qhkc/` | 2 | 奇货可查数据 |
| `qhkc_web/` | 4 | 奇货可查网页版 |
| `fx/` | 6 | 外汇增强功能 |
| `pro/` | 4 | 专业版接口 |
| `rate/` | 2 | 利率相关 |
| `other/` | 3 | 其他数据 |
| `tool/` | 2 | 工具函数 |

---

## 工具模块 (utils/)

**目录**: `akshare/utils/` (8 个文件)

**作用**: 提供通用工具函数和辅助功能

### 文件清单及功能

| 文件名 | 主要功能 | 用途 |
|--------|---------|------|
| `__init__.py` | 工具模块初始化 | 导出工具函数 |
| `cons.py` | 常量定义 | HTTP headers等常量 |
| `context.py` | 上下文管理 | 环境配置管理 |
| `demjson.py` | JSON 解析 | 解析非标准JSON |
| `func.py` | 通用函数 | 数据处理辅助函数 |
| `multi_decrypt.py` | 解密工具 | 数据解密功能 |
| `token_process.py` | Token 处理 | API token 管理 |
| `tqdm.py` | 进度条封装 | 统一的进度条接口 |

### 重要工具说明

#### `cons.py` - 常量定义
```python
# HTTP 请求头
headers = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "application/json",
}

# 其他常量
MAX_RETRY = 3
TIMEOUT = 10
```

#### `tqdm.py` - 进度条工具
```python
from akshare.utils.tqdm import get_tqdm

tqdm = get_tqdm()
for item in tqdm(items, leave=False):
    # 处理逻辑
    pass
```

#### `demjson.py` - JSON 解析
用于解析网页中的非标准 JSON 数据(如 JavaScript 变量)

---

## 数据文件 (data/)

**目录**: `akshare/data/`

**作用**: 存放配置文件、JavaScript 脚本等静态资源

### 文件清单

| 文件名 | 类型 | 用途 |
|--------|------|------|
| `__init__.py` | Python | 模块初始化 |
| `cninfo.js` | JavaScript | 巨潮资讯数据解密 |
| `ths.js` | JavaScript | 同花顺数据处理 |
| `crypto_info.zip` | 压缩包 | 加密货币信息 |

### JavaScript 脚本说明

项目中使用 `py-mini-racer` 执行 JavaScript 代码,主要用于:
- 数据解密
- 加密参数生成
- 特殊格式数据解析

---

## 核心文件说明

### `request.py` - HTTP 请求封装

**作用**: 封装统一的 HTTP 请求接口

**主要功能**:
- 请求重试机制
- 超时控制
- 错误处理
- 代理支持

### `exceptions.py` - 自定义异常

**作用**: 定义项目特定的异常类

**异常类型**:
- 网络请求异常
- 数据解析异常
- 参数验证异常

### `datasets.py` - 数据集工具

**作用**: 提供示例数据集和辅助函数

**主要功能**:
- 加载示例数据
- 数据集描述
- 快速测试接口

---

## 模块依赖关系

```
┌─────────────────────────────────────────────┐
│          akshare/__init__.py                │
│          (主入口,导出所有接口)               │
└─────────────────┬───────────────────────────┘
                  │
                  ├─→ 核心数据模块
                  │   ├─→ stock/         (股票)
                  │   ├─→ fund/          (基金)
                  │   ├─→ bond/          (债券)
                  │   ├─→ futures/       (期货)
                  │   ├─→ option/        (期权)
                  │   ├─→ index/         (指数)
                  │   ├─→ economic/      (宏观)
                  │   ├─→ forex/         (外汇)
                  │   └─→ crypto/        (加密货币)
                  │
                  ├─→ 扩展数据模块
                  │   ├─→ stock_feature/    (股票因子)
                  │   ├─→ stock_fundamental/ (基本面)
                  │   ├─→ futures_derivative/ (期货衍生)
                  │   └─→ ...
                  │
                  ├─→ 辅助模块
                  │   ├─→ utils/         (工具函数)
                  │   ├─→ data/          (数据文件)
                  │   └─→ file_fold/     (配置文件)
                  │
                  └─→ 基础设施
                      ├─→ request.py     (HTTP请求)
                      ├─→ exceptions.py  (异常定义)
                      └─→ datasets.py    (数据集)
```

### 依赖层次

1. **底层**: `utils/`, `request.py`, `exceptions.py`
2. **中层**: 各数据模块 (`stock/`, `fund/` 等)
3. **顶层**: `__init__.py` (统一导出)

### 模块间调用

```python
# 典型的模块内部结构
akshare/stock/stock_zh_a_sina.py
├─ import pandas as pd            # 外部依赖
├─ import requests                # 外部依赖
├─ from akshare.utils import ...  # 内部工具
└─ def stock_zh_a_hist(...) -> pd.DataFrame
```

---

## 开发模式

### 标准接口模式

所有数据接口遵循统一的开发模式:

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: YYYY/MM/DD HH:MM
Desc: 数据来源描述
数据源链接
"""

import pandas as pd
import requests
from akshare.utils.tqdm import get_tqdm


def interface_name(
    symbol: str = "default",
    start_date: str = "20200101",
    end_date: str = "20231231"
) -> pd.DataFrame:
    """
    接口功能描述
    数据来源链接
    :param symbol: 参数说明
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 返回数据说明
    :rtype: pandas.DataFrame
    """
    # 1. 构建请求
    url = "https://api.example.com/data"
    params = {"symbol": symbol}
    
    # 2. 发送请求
    r = requests.get(url, params=params)
    data_json = r.json()
    
    # 3. 数据处理
    temp_df = pd.DataFrame(data_json["data"])
    
    # 4. 列名转换
    temp_df.rename(columns={"old": "新名称"}, inplace=True)
    
    # 5. 类型转换
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["价格"] = pd.to_numeric(temp_df["价格"], errors="coerce")
    
    return temp_df


# 测试代码
if __name__ == "__main__":
    result_df = interface_name()
    print(result_df)
```

---

## 使用示例

### 基本使用

```python
import akshare as ak

# 股票数据
stock_df = ak.stock_zh_a_hist(symbol="000001")

# 基金数据
fund_df = ak.fund_open_fund_info_em(symbol="000001")

# 期货数据
futures_df = ak.futures_main_sina(symbol="RB0")

# 宏观数据
macro_df = ak.macro_china_cpi()
```

### 高级使用

```python
import akshare as ak
import pandas as pd

# 批量获取多只股票
symbols = ["000001", "000002", "600000"]
dfs = []
for symbol in symbols:
    df = ak.stock_zh_a_hist(symbol=symbol)
    df["symbol"] = symbol
    dfs.append(df)

result = pd.concat(dfs, ignore_index=True)
```

---

## 附录

### A. 数据源统计

| 数据源 | 使用频率 | 主要模块 |
|--------|---------|---------|
| 东方财富 (eastmoney) | ⭐⭐⭐⭐⭐ | stock, fund, bond |
| 新浪财经 (sina) | ⭐⭐⭐⭐ | stock, futures, index |
| 同花顺 (ths) | ⭐⭐⭐ | stock, fund |
| 巨潮资讯 (cninfo) | ⭐⭐⭐ | stock |
| 腾讯财经 (tencent) | ⭐⭐ | stock |
| 中国货币网 | ⭐⭐ | bond |
| 各大交易所 | ⭐⭐⭐⭐ | futures, option |

### B. 文件命名规范

- **格式**: `{资产类型}_{细分类别}_{数据源}.py`
- **示例**:
  - `stock_zh_a_sina.py` - 新浪A股数据
  - `fund_etf_em.py` - 东财ETF数据
  - `bond_cb_ths.py` - 同花顺可转债数据

### C. 函数命名规范

- **格式**: `{资产类型}_{地区}_{细分}_{数据源}`
- **示例**:
  - `stock_zh_a_hist()` - 中国A股历史数据
  - `fund_em_open_fund()` - 东财开放式基金
  - `futures_main_sina()` - 新浪主力合约

---

## 总结

**AKShare 项目特点**:

✅ **模块化设计**: 40+ 个功能模块,职责清晰  
✅ **统一接口**: 所有函数返回 pandas.DataFrame  
✅ **多数据源**: 整合 20+ 个数据源  
✅ **易于扩展**: 标准化的开发模式  
✅ **文档完善**: 每个函数都有详细文档  
✅ **开源免费**: MIT 许可证,社区活跃

**核心价值**:
- 🎯 一站式财经数据解决方案
- 🚀 简洁易用的 API 设计
- 📊 覆盖全面的金融数据
- 🔧 持续维护和更新

---

**文档版本**: v1.0  
**生成日期**: 2025-10-17  
**维护**: AKShare 开发团队  
**项目地址**: https://github.com/akfamily/akshare  
**官方文档**: https://akshare.akfamily.xyz/

