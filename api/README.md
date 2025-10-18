# AKShare FastAPI 服务

基于 FastAPI 构建的 AKShare 财经数据 HTTP API 服务,提供股票、基金、期货、债券、指数、外汇等金融数据接口。

## ✨ 特性

- 🔐 **Token 认证**: 基于请求头的 Token 认证机制
- 🚦 **速率限制**: 防止接口被滥用,可配置的请求频率限制
- 📊 **统一响应**: 标准化的 JSON 响应格式
- 🔄 **自动文档**: FastAPI 自动生成的交互式 API 文档
- 🐳 **Docker 支持**: 开箱即用的 Docker 部署方案
- ⚡ **高性能**: 基于 Uvicorn ASGI 服务器,支持异步处理
- 🛡️ **错误处理**: 完善的异常处理和友好的错误提示
- 📦 **模块化设计**: 清晰的代码结构,易于维护和扩展

## 📋 系统要求

- Python >= 3.9
- 推荐使用 Python 3.12

## 🚀 快速开始

### 1. 安装依赖

```bash
cd api
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量示例文件并修改配置:

```bash
cp env.example .env
```

编辑 `.env` 文件,至少需要配置:

```ini
# 设置你的 API Token
API_TOKENS=your-secret-token-here

# 其他配置根据需要调整
ENVIRONMENT=development
PORT=8000
```

### 3. 启动服务

```bash
# 开发模式(自动重载)
python main.py

# 或使用 uvicorn 直接启动
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问 API 文档

服务启动后,访问以下地址查看交互式文档:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 API 使用示例

### 认证方式

所有 API 请求都需要在请求头中携带 Token:

```bash
X-API-Token: your-secret-token-here
```

### 示例 1: 获取 A股历史行情

```bash
curl -X GET "http://localhost:8000/api/stock/zh_a_hist?symbol=000001&period=daily&start_date=20240101&end_date=20241231" \
  -H "X-API-Token: your-secret-token-here"
```

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "日期": "2024-01-02",
      "开盘": 10.50,
      "收盘": 10.60,
      "最高": 10.70,
      "最低": 10.45,
      "成交量": 1000000
    }
  ],
  "total": 1
}
```

### 示例 2: 获取实时行情

```bash
curl -X GET "http://localhost:8000/api/stock/zh_a_spot_em?limit=10" \
  -H "X-API-Token: your-secret-token-here"
```

### 示例 3: 获取基金信息

```bash
curl -X GET "http://localhost:8000/api/fund/open_fund_info_em?symbol=000001&indicator=单位净值走势" \
  -H "X-API-Token: your-secret-token-here"
```

### Python 客户端示例

```python
import requests

# 配置
BASE_URL = "http://localhost:8000"
API_TOKEN = "your-secret-token-here"
headers = {"X-API-Token": API_TOKEN}

# 获取股票历史数据
response = requests.get(
    f"{BASE_URL}/api/stock/zh_a_hist",
    headers=headers,
    params={
        "symbol": "000001",
        "period": "daily",
        "start_date": "20240101",
        "end_date": "20241231"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"获取到 {data['total']} 条数据")
    print(data['data'][:5])  # 打印前5条
else:
    print(f"请求失败: {response.status_code}")
    print(response.json())
```

## 📚 API 接口列表

### 股票数据 (`/api/stock`)

| 接口路径 | 说明 | 主要参数 |
|---------|------|---------|
| `/zh_a_hist` | A股历史行情 | symbol, period, start_date, end_date, adjust |
| `/zh_a_spot_em` | A股实时行情 | limit |
| `/info_sh` | 上交所股票信息 | symbol |
| `/individual_info_em` | 个股详细信息 | symbol |
| `/zyjs_ths` | 股票主营介绍 | symbol |

### 基金数据 (`/api/fund`)

| 接口路径 | 说明 | 主要参数 |
|---------|------|---------|
| `/open_fund_info_em` | 开放式基金信息 | symbol, indicator |
| `/etf_fund_info_em` | ETF基金信息 | symbol, start_date, end_date |
| `/fund_portfolio_hold_em` | 基金持仓 | symbol, date |
| `/fund_name_em` | 基金列表 | limit |

### 期货数据 (`/api/futures`)

| 接口路径 | 说明 | 主要参数 |
|---------|------|---------|
| `/futures_main_sina` | 期货主力合约实时行情 | symbol |
| `/futures_zh_spot` | 期货实时行情 | symbol, market |
| `/futures_comm_info` | 期货品种信息 | symbol |

### 债券数据 (`/api/bond`)

| 接口路径 | 说明 | 主要参数 |
|---------|------|---------|
| `/zh_cov_spot` | 可转债实时行情 | limit |
| `/china_bond_spot` | 现券市场成交行情 | limit |
| `/zh_cov_value_analysis` | 可转债价值分析 | symbol |

### 指数数据 (`/api/index`)

| 接口路径 | 说明 | 主要参数 |
|---------|------|---------|
| `/zh_a_hist` | 指数历史行情 | symbol, period, start_date, end_date |
| `/investing_global` | 全球指数行情 | country |

### 外汇数据 (`/api/forex`)

| 接口路径 | 说明 | 主要参数 |
|---------|------|---------|
| `/spot_quote` | 外汇实时行情 | symbol |
| `/pair_quote_hist` | 外汇货币对历史数据 | symbol, period, start_date, end_date |

## ⚙️ 配置说明

### 环境变量配置

在 `.env` 文件中可以配置以下参数:

| 配置项 | 说明 | 默认值 |
|-------|------|--------|
| `ENVIRONMENT` | 运行环境 (development/production) | development |
| `HOST` | 服务监听地址 | 0.0.0.0 |
| `PORT` | 服务监听端口 | 8000 |
| `WORKERS` | 生产环境 Worker 数量 | 4 |
| `API_TOKENS` | 有效的 API Token 列表(逗号分隔) | - |
| `TOKEN_HEADER_NAME` | Token 请求头名称 | X-API-Token |
| `CORS_ORIGINS` | 允许的跨域来源 | * |
| `RATE_LIMIT_ENABLED` | 是否启用速率限制 | true |
| `RATE_LIMIT_TIMES` | 速率限制: 请求次数 | 100 |
| `RATE_LIMIT_SECONDS` | 速率限制: 时间窗口(秒) | 60 |
| `MAX_ROWS` | 单次请求最大返回行数 | 10000 |

### 速率限制

默认配置为 **60秒内最多100次请求**。可以通过环境变量调整:

```ini
RATE_LIMIT_TIMES=200
RATE_LIMIT_SECONDS=60
```

关闭速率限制:

```ini
RATE_LIMIT_ENABLED=false
```

## 🐳 Docker 部署

### 使用 Docker Compose (推荐)

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用 Docker

```bash
# 构建镜像
docker build -t akshare-api:latest .

# 运行容器
docker run -d \
  --name akshare-api \
  -p 8000:8000 \
  -e API_TOKENS="your-secret-token" \
  akshare-api:latest
```

## 🔒 安全建议

1. **生产环境配置**:
   - 修改默认 Token 为强密码
   - 设置 `ENVIRONMENT=production`
   - 配置 `ALLOWED_HOSTS` 为具体域名
   - 配置 `CORS_ORIGINS` 为具体域名

2. **使用 HTTPS**:
   - 生产环境建议使用 Nginx 反向代理并配置 SSL 证书

3. **定期更新 Token**:
   - 定期更换 API Token
   - 为不同客户端分配不同的 Token

4. **监控和日志**:
   - 配置日志文件路径
   - 监控 API 调用频率和异常

## 📁 项目结构

```
api/
├── main.py                 # 应用主入口
├── config.py              # 配置管理
├── dependencies.py        # 依赖注入
├── schemas.py             # 数据模型
├── requirements.txt       # 项目依赖
├── env.example           # 环境变量示例
├── README.md             # 项目文档
├── Dockerfile            # Docker 构建文件
├── docker-compose.yml    # Docker Compose 配置
├── middleware/           # 中间件
│   ├── __init__.py
│   └── rate_limit.py    # 速率限制中间件
└── routers/             # API 路由
    ├── __init__.py
    ├── stock.py         # 股票接口
    ├── fund.py          # 基金接口
    ├── futures.py       # 期货接口
    ├── bond.py          # 债券接口
    ├── index.py         # 指数接口
    └── forex.py         # 外汇接口
```

## 🔧 开发指南

### 添加新接口

1. 在对应的路由文件中添加新的端点函数
2. 使用 `@router.get()` 装饰器定义路由
3. 添加适当的参数验证和文档说明
4. 处理异常并返回统一格式的响应

示例:

```python
@router.get("/new_endpoint", response_model=DataResponse, summary="新接口")
async def get_new_data(
    symbol: str = Query(..., description="参数说明"),
) -> DataResponse:
    """
    接口功能说明
    
    数据来源: XXX
    接口: xxx
    """
    try:
        df = ak.some_function(symbol=symbol)
        return DataResponse(
            code=200,
            message="success",
            data=df.to_dict(orient="records"),
            total=len(df),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据失败: {str(e)}",
        )
```

### 代码规范

项目遵循 AKShare 的代码规范,使用 Ruff 进行代码检查和格式化:

```bash
# 检查代码
ruff check api/

# 格式化代码
ruff format api/
```

## 📝 常见问题

### Q: 如何生成安全的 Token?

A: 可以使用 Python 生成:

```python
import secrets
token = secrets.token_urlsafe(32)
print(token)
```

### Q: 如何处理大量数据返回?

A: 使用 `limit` 参数限制返回数据量,默认最大 10000 条,可通过 `MAX_ROWS` 配置调整。

### Q: 速率限制返回 429 错误怎么办?

A: 请求过于频繁,需要等待一段时间后再试,或者调整 `RATE_LIMIT_TIMES` 配置。

### Q: 生产环境如何部署?

A: 推荐使用 Docker Compose 部署,并配合 Nginx 反向代理。

## 📄 许可证

MIT License - 继承自 AKShare 项目

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📞 联系方式

- AKShare 项目: https://github.com/akfamily/akshare
- AKShare 文档: https://akshare.akfamily.xyz/

