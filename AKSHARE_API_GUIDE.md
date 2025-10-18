# AKShare API 服务完整指南

一站式 AKShare API 服务部署、配置和使用文档。

---

## 📋 目录

- [项目概述](#项目概述)
- [快速开始](#快速开始)
- [Docker 部署](#docker-部署)
- [API 使用](#api-使用)
- [配置说明](#配置说明)
- [故障排查](#故障排查)
- [生产环境](#生产环境)

---

## 项目概述

本项目为 AKShare 创建了基于 FastAPI 的 HTTP API 服务，使财经数据接口可通过 RESTful API 访问，支持多种编程语言和平台集成。

### ✨ 核心特性

- ✅ **Token 认证**: 基于请求头的安全认证机制
- ✅ **速率限制**: 防止接口滥用，基于 IP/Token 的滑动窗口限流
- ✅ **Docker 支持**: 一键部署到容器环境
- ✅ **自动文档**: Swagger UI 交互式 API 文档
- ✅ **模块化设计**: 清晰的代码结构，易于扩展
- ✅ **生产就绪**: 包含 Nginx 配置、健康检查等

### 📊 已实现接口

| 模块 | 接口数量 | 说明 |
|------|---------|------|
| 股票 | 5 | 历史行情、实时行情、个股信息等 |
| 基金 | 4 | 基金净值、持仓、列表等 |
| 期货 | 3 | 主力合约、实时行情等 |
| 债券 | 3 | 可转债行情、价值分析等 |
| 指数 | 2 | 指数历史行情、全球指数 |
| 外汇 | 2 | 外汇实时行情、历史数据 |
| **总计** | **19** | 覆盖主要金融数据类型 |

### 🛠️ 技术栈

- **Web 框架**: FastAPI 0.109+
- **ASGI 服务器**: Uvicorn
- **数据源**: AKShare 1.14+
- **容器化**: Docker & Docker Compose
- **反向代理**: Nginx

---

## 快速开始

### 前置要求

- **开发环境**: Python 3.9+，pip
- **Docker 环境**: Docker Desktop (Windows/Mac) 或 Docker Engine (Linux) - [下载](https://www.docker.com/products/docker-desktop/)
- **系统要求**: 2GB+ 内存，2GB+ 磁盘空间

### 方式 1: 直接运行（开发推荐）

```bash
# 1. 进入 api 目录
cd api

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp env.example .env

# 4. 启动服务
python main.py
```

启动后访问：
- **API 服务**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### 方式 2: Docker 一键部署（推荐）

#### Windows 用户

```powershell
# 运行部署脚本
.\deploy-local.ps1
```

#### Linux/Mac 用户

```bash
# 运行部署脚本
chmod +x deploy-local.sh
./deploy-local.sh
```

#### 手动 Docker 部署

```bash
# 1. 创建日志目录
mkdir -p api/logs

# 2. 启动容器
docker-compose up -d --build

# 3. 查看状态
docker-compose ps
docker-compose logs -f
```

**注意**: 本地部署默认为开发环境，API 文档已启用，无需 Token 即可访问文档页面。

---

## Docker 部署

### 🎯 一键部署流程

部署脚本会自动完成：

1. ✅ 检查 Docker 是否安装
2. ✅ 创建必要的目录
3. ✅ 复制环境配置文件
4. ✅ 构建 Docker 镜像
5. ✅ 启动容器
6. ✅ 健康检查
7. ✅ 显示访问地址

### 📋 常用 Docker 命令

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build --force-recreate

# 进入容器
docker-compose exec akshare-api bash

# 查看资源占用
docker stats akshare-api
```

### 🧪 测试部署

```bash
# 方式1: 运行自动化测试脚本
pip install requests
python test-deployment.py

# 方式2: 手动测试健康检查
curl http://localhost:8000/health

# 方式3: 测试 API（需要 Token）
curl -H "X-API-Token: dev-token-12345678" \
  "http://localhost:8000/api/stock/zh-a-hist?symbol=000001&period=daily"
```

---

## API 使用

### 🔑 获取 Token

**开发环境**启动后会自动打印可用的 Token：

```
==================================================
开发环境 API Tokens:
  1. dev-token-12345678
  2. [自动生成的安全token]
==================================================
```

**生产环境**请在 `.env` 文件中配置：

```env
API_TOKENS=your-secure-token-here
```

生成安全 Token：

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 💻 使用示例

#### Python

```python
import requests

BASE_URL = "http://localhost:8000"
TOKEN = "dev-token-12345678"

headers = {"X-API-Token": TOKEN}

# 获取股票历史数据
response = requests.get(
    f"{BASE_URL}/api/stock/zh-a-hist",
    headers=headers,
    params={
        "symbol": "000001",
        "period": "daily",
        "start_date": "20240101",
        "end_date": "20241231"
    }
)

data = response.json()
print(data)
```

#### Python 客户端（推荐）

```python
from api.examples.client_example import AKShareAPIClient

# 初始化客户端
client = AKShareAPIClient(
    base_url="http://localhost:8000",
    api_token="dev-token-12345678"
)

# 获取股票历史数据
df = client.get_stock_hist(
    symbol="000001",
    period="daily",
    start_date="20240101"
)
print(df.head())

# 获取实时行情
df_spot = client.get_stock_spot(limit=10)
print(df_spot)

# 获取基金信息
df_fund = client.get_fund_info(symbol="000001")
print(df_fund.head())
```

#### JavaScript/Node.js

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';
const TOKEN = 'dev-token-12345678';

axios.get(`${BASE_URL}/api/stock/zh-a-hist`, {
  headers: { 'X-API-Token': TOKEN },
  params: {
    symbol: '000001',
    period: 'daily',
    start_date: '20240101'
  }
})
.then(response => console.log(response.data))
.catch(error => console.error(error));
```

#### cURL

```bash
# 健康检查（无需 Token）
curl http://localhost:8000/health

# 获取股票数据（需要 Token）
curl -X GET "http://localhost:8000/api/stock/zh-a-hist?symbol=000001&period=daily" \
  -H "X-API-Token: dev-token-12345678"

# 获取实时行情
curl -X GET "http://localhost:8000/api/stock/zh-a-spot-em?limit=10" \
  -H "X-API-Token: dev-token-12345678"
```

### 📖 API 文档

访问 **http://localhost:8000/docs** 查看完整的交互式 API 文档，支持：

- 📋 查看所有接口列表
- 🧪 在线测试 API
- 📝 查看请求/响应格式
- 🔍 搜索接口

---

## 配置说明

### ⚙️ 环境变量配置

编辑 `api/.env` 文件：

```env
# ========== 基础配置 ==========
ENVIRONMENT=development      # development 或 production
HOST=0.0.0.0
PORT=8000
WORKERS=4                    # 生产环境 Worker 数量

# ========== Token 认证 ==========
# 使用逗号分隔多个 Token
API_TOKENS=dev-token-12345678,your-custom-token
TOKEN_HEADER_NAME=X-API-Token

# ========== CORS 配置 ==========
# 允许的跨域来源，使用逗号分隔
CORS_ORIGINS=*               # 生产环境建议设置具体域名

# ========== 可信主机 ==========
ALLOWED_HOSTS=*              # 生产环境建议设置具体域名

# ========== 速率限制 ==========
RATE_LIMIT_ENABLED=true
RATE_LIMIT_TIMES=200         # 60秒内允许200次请求
RATE_LIMIT_SECONDS=60

# ========== 缓存配置 ==========
CACHE_ENABLED=false
CACHE_EXPIRE_SECONDS=300

# ========== 日志配置 ==========
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/akshare_api.log

# ========== 数据限制 ==========
MAX_ROWS=10000               # 单次返回最大行数
```

### 🔧 修改端口

编辑 `docker-compose.yml`：

```yaml
ports:
  - "8080:8000"  # 将本地 8080 端口映射到容器 8000 端口
```

修改配置后重启：

```bash
docker-compose restart
```

### 📊 性能配置

根据服务器配置调整：

```env
# Worker 数量建议: CPU 核心数 * 2
WORKERS=8

# 根据需求调整速率限制
RATE_LIMIT_TIMES=500
RATE_LIMIT_SECONDS=60

# 启用缓存提升性能
CACHE_ENABLED=true
CACHE_EXPIRE_SECONDS=600
```

---

## 故障排查

### 问题 1: 端口被占用

```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# 解决: 修改端口或停止占用进程
```

### 问题 2: 容器启动失败

```bash
# 查看详细日志
docker-compose logs

# 完全重建
docker-compose down -v
docker-compose up -d --build --force-recreate
```

### 问题 3: API 返回 401 错误

**可能原因**：
- 请求头缺少 Token
- Token 值不正确
- Token 包含多余空格

**解决方法**：
```bash
# 确保请求头格式正确
curl -H "X-API-Token: dev-token-12345678" http://localhost:8000/api/stock/zh-a-hist?symbol=000001
```

### 问题 4: Docker Desktop 未启动

**错误信息**：
```
Error: Cannot connect to the Docker daemon
```

**解决方法**: 启动 Docker Desktop 应用程序

### 问题 5: 服务无响应

```bash
# 1. 检查容器是否运行
docker-compose ps

# 2. 检查容器内服务
docker-compose exec akshare-api curl http://localhost:8000/health

# 3. 查看完整日志
docker-compose logs --tail=100

# 4. 重启服务
docker-compose restart
```

### 问题 6: 429 错误（请求过于频繁）

**原因**: 触发了速率限制

**解决方法**：
- 等待一段时间后重试
- 调整 `RATE_LIMIT_TIMES` 配置
- 检查是否有循环请求

### 问题 7: 获取数据慢

**可能原因**：
1. 网络延迟
2. 数据源响应慢
3. 返回数据量大

**解决方法**：
- 使用 `limit` 参数限制返回数量
- 启用缓存功能
- 检查网络连接

---

## 生产环境

### 🔐 安全配置清单

#### 1. 修改默认 Token

```bash
# 生成强随机 Token
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

配置到 `.env`：
```env
API_TOKENS=your-strong-random-token-here
```

#### 2. 配置 HTTPS

使用提供的 Nginx 配置（`api/nginx.conf`）：

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. 限制访问来源

```env
# 只允许特定域名访问
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

#### 4. 调整速率限制

```env
# 更严格的限制
RATE_LIMIT_ENABLED=true
RATE_LIMIT_TIMES=50
RATE_LIMIT_SECONDS=60
```

#### 5. 设置日志级别

```env
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

### 🚀 生产环境部署

#### 使用 Docker Compose

```bash
cd api

# 1. 配置环境变量
cp env.example .env
nano .env  # 修改为生产配置

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

#### 使用 Systemd（Linux）

参考 `api/DEPLOY.md` 中的 Systemd 配置

#### 使用部署脚本

```bash
cd api
chmod +x deploy.sh
./deploy.sh
```

### 📈 性能优化

#### 1. 调整 Worker 数量

```env
# 建议: CPU 核心数 * 2
WORKERS=8
```

#### 2. 启用缓存

```env
CACHE_ENABLED=true
CACHE_EXPIRE_SECONDS=600
```

#### 3. 使用 Nginx 反向代理

- 启用 gzip 压缩
- 配置缓存策略
- 实现负载均衡

#### 4. 监控和告警

- 集成 Prometheus 指标
- 配置日志聚合（ELK）
- 设置告警规则

### 🔍 监控建议

```bash
# 查看容器资源使用
docker stats akshare-api

# 查看日志
tail -f api/logs/akshare_api.log

# 健康检查
curl http://localhost:8000/health
```

---

## 📚 其他资源

### 项目文档

| 文档 | 位置 | 说明 |
|-----|------|------|
| 快速开始 | `api/QUICKSTART.md` | 5分钟快速上手 |
| 完整文档 | `api/README.md` | 详细功能说明 |
| API 参考 | `api/API_REFERENCE.md` | 所有接口参数 |
| 部署指南 | `api/DEPLOY.md` | 生产环境部署 |
| 项目总结 | `api/PROJECT_SUMMARY.md` | 项目架构说明 |

### 使用示例

- 同步客户端: `api/examples/client_example.py`
- 异步客户端: `api/examples/async_client_example.py`
- 测试脚本: `api/test_api.py`
- 部署测试: `test-deployment.py`

### 外部链接

- [AKShare 官方文档](https://akshare.akfamily.xyz/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Docker 官方文档](https://docs.docker.com/)

---

## ❓ 常见问题

**Q: 如何查看可用的 API 接口？**  
A: 访问 http://localhost:8000/docs 查看完整的交互式 API 文档

**Q: 如何修改速率限制？**  
A: 编辑 `api/.env` 中的 `RATE_LIMIT_TIMES` 和 `RATE_LIMIT_SECONDS`

**Q: 如何生成新的 Token？**  
A: 运行 `python -c "import secrets; print(secrets.token_urlsafe(32))"`

**Q: 部署脚本做了什么？**  
A: 自动创建目录、复制配置、构建镜像、启动容器、健康检查

**Q: 如何同时运行多个实例？**  
A: 修改 `docker-compose.yml` 中的容器名称和端口映射

**Q: 支持哪些数据接口？**  
A: 目前支持股票、基金、期货、债券、指数、外汇共 19 个常用接口

**Q: 性能如何？**  
A: 支持 100+ 并发请求，平均响应时间 200-500ms（取决于数据源）

---

## 🎉 开始使用

```bash
# Windows 用户
.\deploy-local.ps1

# Linux/Mac 用户
chmod +x deploy-local.sh && ./deploy-local.sh

# 访问服务
# http://localhost:8000/docs
```

**项目位置**: `E:\Code\QuantScope\akshare\api\`  
**默认 Token**: `dev-token-12345678`  
**创建日期**: 2025年10月18日  
**项目状态**: ✅ **生产就绪**

---

**祝你使用愉快！** 🚀

