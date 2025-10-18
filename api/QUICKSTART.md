# AKShare API 快速开始

5分钟快速启动 AKShare API 服务!

## 📦 一键启动 (开发环境)

### 方式 1: 使用启动脚本 (Linux/Mac)

```bash
cd api
./start.sh
```

脚本会自动:
- 创建虚拟环境
- 安装依赖
- 创建配置文件
- 启动服务

### 方式 2: 手动启动

```bash
# 1. 进入目录
cd api

# 2. 安装依赖
pip install -r requirements.txt

# 3. 创建配置文件
cp env.example .env

# 4. 启动服务
python main.py
```

## 🐳 Docker 一键部署

```bash
cd api
docker-compose up -d
```

## ✅ 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 预期输出:
# {"status":"healthy","version":"1.0.0","service":"AKShare API"}
```

## 🔑 获取 Token

开发环境会自动生成 Token 并在启动时打印:

```
==================================================
开发环境 API Tokens:
  1. dev-token-12345678
  2. [自动生成的安全token]
==================================================
```

## 📖 查看 API 文档

启动服务后,在浏览器中打开:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 第一个 API 请求

### 使用 curl

```bash
curl -X GET "http://localhost:8000/api/stock/zh_a_hist?symbol=000001&period=daily&start_date=20240101&end_date=20241231" \
  -H "X-API-Token: dev-token-12345678"
```

### 使用 Python

```python
import requests

url = "http://localhost:8000/api/stock/zh_a_hist"
headers = {"X-API-Token": "dev-token-12345678"}
params = {
    "symbol": "000001",
    "period": "daily",
    "start_date": "20240101",
    "end_date": "20241231"
}

response = requests.get(url, headers=headers, params=params)
print(response.json())
```

### 使用客户端库

```python
# 使用提供的客户端示例
from examples.client_example import AKShareAPIClient

client = AKShareAPIClient(
    base_url="http://localhost:8000",
    api_token="dev-token-12345678"
)

# 获取股票历史数据
df = client.get_stock_hist(symbol="000001", start_date="20240101")
print(df.head())
```

## 📚 常用接口示例

### 1. 获取实时行情

```bash
curl "http://localhost:8000/api/stock/zh_a_spot_em?limit=10" \
  -H "X-API-Token: dev-token-12345678"
```

### 2. 获取基金信息

```bash
curl "http://localhost:8000/api/fund/open_fund_info_em?symbol=000001&indicator=单位净值走势" \
  -H "X-API-Token: dev-token-12345678"
```

### 3. 获取可转债行情

```bash
curl "http://localhost:8000/api/bond/zh_cov_spot?limit=5" \
  -H "X-API-Token: dev-token-12345678"
```

### 4. 获取指数行情

```bash
curl "http://localhost:8000/api/index/zh_a_hist?symbol=000001&start_date=20240101" \
  -H "X-API-Token: dev-token-12345678"
```

## ⚙️ 修改配置

编辑 `.env` 文件:

```bash
nano .env  # 或使用其他编辑器
```

常用配置:

```ini
# 修改端口
PORT=8080

# 修改 Token
API_TOKENS=your-custom-token

# 调整速率限制
RATE_LIMIT_TIMES=200
RATE_LIMIT_SECONDS=60
```

修改后重启服务即可生效。

## 🛑 停止服务

### 开发环境

按 `Ctrl+C` 停止服务

### Docker 环境

```bash
docker-compose down
```

## 📖 下一步

- 📚 查看完整文档: [README.md](README.md)
- 🚀 生产环境部署: [DEPLOY.md](DEPLOY.md)
- 💡 查看更多示例: [examples/](examples/)

## ❓ 常见问题

### Q: 服务启动失败?

**A**: 检查端口是否被占用:
```bash
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

### Q: Token 认证失败?

**A**: 确保:
1. 请求头名称为 `X-API-Token`
2. Token 值与配置文件中的一致
3. Token 前后没有多余空格

### Q: 获取数据失败?

**A**: 可能是:
1. 网络问题,无法访问数据源
2. 数据源接口变更
3. 参数错误

查看详细错误信息:
```bash
docker-compose logs -f  # Docker
# 或查看控制台输出
```

## 🆘 获取帮助

- 📋 查看完整文档: [README.md](README.md)
- 🐛 报告问题: GitHub Issues
- 📚 AKShare 文档: https://akshare.akfamily.xyz/

---

**祝你使用愉快!** 🎉

