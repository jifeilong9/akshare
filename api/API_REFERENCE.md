# AKShare API 接口参考

快速查找所有可用的 API 接口。

## 🔑 认证

所有接口都需要在请求头中添加:

```
X-API-Token: your-api-token
```

## 📊 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": [...],
  "total": 100
}
```

## 🏷️ 接口列表

### 股票数据 `/api/stock`

#### 1. A股历史行情
**接口**: `GET /api/stock/zh_a_hist`

**参数**:
- `symbol` (必填): 股票代码,如 `000001`
- `period` (可选): 周期 `daily`/`weekly`/`monthly`, 默认 `daily`
- `start_date` (可选): 开始日期 `YYYYMMDD`, 默认 `19700101`
- `end_date` (可选): 结束日期 `YYYYMMDD`, 默认 `20500101`
- `adjust` (可选): 复权类型 `qfq`/`hfq`/``, 默认 `` (不复权)
- `limit` (可选): 返回行数限制

**示例**:
```bash
curl "http://localhost:8000/api/stock/zh_a_hist?symbol=000001&period=daily&start_date=20240101" \
  -H "X-API-Token: your-token"
```

#### 2. A股实时行情
**接口**: `GET /api/stock/zh_a_spot_em`

**参数**:
- `limit` (可选): 返回行数限制

**示例**:
```bash
curl "http://localhost:8000/api/stock/zh_a_spot_em?limit=10" \
  -H "X-API-Token: your-token"
```

#### 3. 上交所股票信息
**接口**: `GET /api/stock/info_sh`

**参数**:
- `symbol` (可选): 市场类型, 默认 `主板A股`
- `limit` (可选): 返回行数限制

#### 4. 个股详细信息
**接口**: `GET /api/stock/individual_info_em`

**参数**:
- `symbol` (必填): 股票代码

#### 5. 股票主营介绍
**接口**: `GET /api/stock/zyjs_ths`

**参数**:
- `symbol` (必填): 股票代码

---

### 基金数据 `/api/fund`

#### 1. 开放式基金信息
**接口**: `GET /api/fund/open_fund_info_em`

**参数**:
- `symbol` (必填): 基金代码
- `indicator` (可选): 指标名称, 默认 `单位净值走势`

**示例**:
```bash
curl "http://localhost:8000/api/fund/open_fund_info_em?symbol=000001&indicator=单位净值走势" \
  -H "X-API-Token: your-token"
```

#### 2. ETF基金信息
**接口**: `GET /api/fund/etf_fund_info_em`

**参数**:
- `symbol` (必填): ETF代码
- `start_date` (可选): 开始日期, 默认 `20200101`
- `end_date` (可选): 结束日期, 默认 `20250101`

#### 3. 基金持仓
**接口**: `GET /api/fund/fund_portfolio_hold_em`

**参数**:
- `symbol` (必填): 基金代码
- `date` (必填): 查询日期 `YYYY-MM-DD`
- `limit` (可选): 返回行数限制

#### 4. 基金列表
**接口**: `GET /api/fund/fund_name_em`

**参数**:
- `limit` (可选): 返回行数限制

---

### 期货数据 `/api/futures`

#### 1. 期货主力合约实时行情
**接口**: `GET /api/futures/futures_main_sina`

**参数**:
- `symbol` (必填): 期货品种代码,如 `CU`
- `limit` (可选): 返回行数限制

**示例**:
```bash
curl "http://localhost:8000/api/futures/futures_main_sina?symbol=CU" \
  -H "X-API-Token: your-token"
```

#### 2. 期货实时行情
**接口**: `GET /api/futures/futures_zh_spot`

**参数**:
- `symbol` (必填): 期货合约代码,如 `al2503`
- `market` (必填): 交易所代码 `CFFEX`/`DCE`/`CZCE`/`SHFE`/`INE`/`GFEX`

#### 3. 期货品种信息
**接口**: `GET /api/futures/futures_comm_info`

**参数**:
- `symbol` (可选): 期货品种名称, 默认 `玻璃`
- `limit` (可选): 返回行数限制

---

### 债券数据 `/api/bond`

#### 1. 可转债实时行情
**接口**: `GET /api/bond/zh_cov_spot`

**参数**:
- `limit` (可选): 返回行数限制

**示例**:
```bash
curl "http://localhost:8000/api/bond/zh_cov_spot?limit=10" \
  -H "X-API-Token: your-token"
```

#### 2. 现券市场成交行情
**接口**: `GET /api/bond/china_bond_spot`

**参数**:
- `limit` (可选): 返回行数限制

#### 3. 可转债价值分析
**接口**: `GET /api/bond/zh_cov_value_analysis`

**参数**:
- `symbol` (必填): 可转债代码,如 `113050`

---

### 指数数据 `/api/index`

#### 1. 指数历史行情
**接口**: `GET /api/index/zh_a_hist`

**参数**:
- `symbol` (必填): 指数代码,如 `000001` (上证指数)
- `period` (可选): 周期 `daily`/`weekly`/`monthly`, 默认 `daily`
- `start_date` (可选): 开始日期, 默认 `19700101`
- `end_date` (可选): 结束日期, 默认 `20500101`
- `limit` (可选): 返回行数限制

**示例**:
```bash
curl "http://localhost:8000/api/index/zh_a_hist?symbol=000001&period=daily" \
  -H "X-API-Token: your-token"
```

#### 2. 全球指数行情
**接口**: `GET /api/index/investing_global`

**参数**:
- `country` (可选): 国家名称, 默认 `中国`
- `limit` (可选): 返回行数限制

---

### 外汇数据 `/api/forex`

#### 1. 外汇实时行情
**接口**: `GET /api/forex/spot_quote`

**参数**:
- `symbol` (可选): 外汇代码, 默认 `USDCNY`
- `limit` (可选): 返回行数限制

**示例**:
```bash
curl "http://localhost:8000/api/forex/spot_quote?symbol=USDCNY" \
  -H "X-API-Token: your-token"
```

#### 2. 外汇货币对历史数据
**接口**: `GET /api/forex/pair_quote_hist`

**参数**:
- `symbol` (可选): 货币对代码, 默认 `USDCNY`
- `period` (可选): 周期 `daily`/`weekly`/`monthly`, 默认 `daily`
- `start_date` (可选): 开始日期, 默认 `19700101`
- `end_date` (可选): 结束日期, 默认 `20500101`
- `limit` (可选): 返回行数限制

---

## 🏥 系统接口

### 健康检查
**接口**: `GET /health`

**响应**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "AKShare API"
}
```

### 根路径
**接口**: `GET /`

**响应**:
```json
{
  "service": "AKShare API Service",
  "version": "1.0.0",
  "docs": "/docs",
  "message": "AKShare 财经数据 API 服务运行中"
}
```

---

## 📋 错误码说明

| 状态码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权(Token 无效或缺失) |
| 422 | 请求参数验证失败 |
| 429 | 请求过于频繁(速率限制) |
| 500 | 服务器内部错误 |

## 🚦 速率限制

- **响应头**: 
  - `X-RateLimit-Limit`: 速率限制总数
  - `X-RateLimit-Remaining`: 剩余请求次数
  - `X-RateLimit-Reset`: 重置时间戳

- **默认配置**: 60秒内最多 100 次请求

## 💡 使用建议

1. **分页查询**: 使用 `limit` 参数控制返回数据量
2. **日期范围**: 合理设置 `start_date` 和 `end_date`
3. **错误处理**: 捕获并处理各种 HTTP 错误码
4. **Token 管理**: 妥善保管 API Token
5. **速率控制**: 注意请求频率,避免触发限流

## 🔗 相关链接

- **API 文档**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **AKShare 官方文档**: https://akshare.akfamily.xyz/
- **项目文档**: [README.md](README.md)

---

**更新时间**: 2025年10月18日

