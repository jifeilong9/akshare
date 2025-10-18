# AKShare API 部署指南

本文档介绍如何在不同环境下部署 AKShare FastAPI 服务。

## 目录

- [本地开发部署](#本地开发部署)
- [Docker 部署](#docker-部署)
- [生产环境部署](#生产环境部署)
- [Nginx 反向代理](#nginx-反向代理)
- [性能优化](#性能优化)
- [监控和维护](#监控和维护)

## 本地开发部署

### 1. 环境准备

```bash
# 确保 Python 版本 >= 3.9
python --version

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. 安装依赖

```bash
cd api
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置文件
cp env.example .env

# 编辑配置文件,修改 API_TOKENS
nano .env  # 或使用其他编辑器
```

### 4. 启动服务

```bash
# 方式 1: 使用启动脚本 (Linux/Mac)
./start.sh

# 方式 2: 直接运行
python main.py

# 方式 3: 使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 测试服务

```bash
# 健康检查
curl http://localhost:8000/health

# 访问 API 文档
# 浏览器打开: http://localhost:8000/docs
```

## Docker 部署

### 1. 使用 Docker Compose (推荐)

```bash
cd api

# 复制并编辑配置
cp env.example .env
nano .env  # 修改配置

# 使用部署脚本 (Linux/Mac)
./deploy.sh

# 或手动执行
docker-compose build
docker-compose up -d
```

### 2. 使用 Docker 命令

```bash
# 构建镜像
docker build -t akshare-api:latest .

# 运行容器
docker run -d \
  --name akshare-api \
  -p 8000:8000 \
  -e API_TOKENS="your-secret-token" \
  -e ENVIRONMENT="production" \
  -e WORKERS=4 \
  -v $(pwd)/logs:/app/logs \
  akshare-api:latest
```

### 3. 查看日志

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f akshare-api
```

### 4. 停止服务

```bash
# Docker Compose
docker-compose down

# Docker
docker stop akshare-api
docker rm akshare-api
```

## 生产环境部署

### 1. 系统要求

- **操作系统**: Linux (推荐 Ubuntu 20.04+ / CentOS 7+)
- **CPU**: 2核或更多
- **内存**: 至少 2GB
- **磁盘**: 至少 10GB 可用空间
- **Python**: 3.9+ (推荐 3.12)

### 2. 安全配置

编辑 `.env` 文件:

```ini
# 设置生产环境
ENVIRONMENT=production

# 使用强密码 Token
API_TOKENS=<使用 secrets.token_urlsafe(32) 生成>

# 限制 CORS 来源
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# 设置可信主机
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# 调整速率限制
RATE_LIMIT_TIMES=100
RATE_LIMIT_SECONDS=60
```

### 3. 使用 Systemd 管理服务

创建服务文件 `/etc/systemd/system/akshare-api.service`:

```ini
[Unit]
Description=AKShare FastAPI Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/akshare-api
Environment="PATH=/opt/akshare-api/venv/bin"
ExecStart=/opt/akshare-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务:

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start akshare-api

# 开机自启
sudo systemctl enable akshare-api

# 查看状态
sudo systemctl status akshare-api

# 查看日志
sudo journalctl -u akshare-api -f
```

### 4. 使用 Supervisor 管理服务

安装 Supervisor:

```bash
sudo apt-get install supervisor  # Ubuntu/Debian
# 或
sudo yum install supervisor      # CentOS
```

创建配置文件 `/etc/supervisor/conf.d/akshare-api.conf`:

```ini
[program:akshare-api]
directory=/opt/akshare-api
command=/opt/akshare-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/akshare-api/access.log
stderr_logfile=/var/log/akshare-api/error.log
```

启动服务:

```bash
# 更新配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start akshare-api

# 查看状态
sudo supervisorctl status akshare-api
```

## Nginx 反向代理

### 1. 安装 Nginx

```bash
# Ubuntu/Debian
sudo apt-get install nginx

# CentOS
sudo yum install nginx
```

### 2. 配置 Nginx

复制提供的 `nginx.conf` 到 Nginx 配置目录:

```bash
# 复制配置文件
sudo cp nginx.conf /etc/nginx/sites-available/akshare-api

# 创建软链接
sudo ln -s /etc/nginx/sites-available/akshare-api /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 3. 配置 SSL 证书 (Let's Encrypt)

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d api.yourdomain.com

# 自动续期 (添加到 crontab)
sudo crontab -e
# 添加: 0 0 * * * certbot renew --quiet
```

## 性能优化

### 1. Worker 数量配置

根据 CPU 核心数调整 Worker 数量:

```bash
# 推荐公式: workers = (2 * CPU核心数) + 1
# 例如 4核 CPU:
WORKERS=9
```

### 2. 启用缓存 (可选)

如果数据更新不频繁,可以启用缓存:

```ini
CACHE_ENABLED=true
CACHE_EXPIRE_SECONDS=300  # 5分钟
```

### 3. 数据库连接池 (如果使用数据库)

添加连接池配置优化数据库访问性能。

### 4. 启用 gzip 压缩 (Nginx)

在 Nginx 配置中添加:

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

## 监控和维护

### 1. 健康检查

```bash
# 定期检查服务状态
curl http://localhost:8000/health
```

### 2. 日志管理

```bash
# 创建日志轮转配置 /etc/logrotate.d/akshare-api
/opt/akshare-api/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    missingok
    create 644 www-data www-data
}
```

### 3. 性能监控

推荐使用以下工具:

- **Prometheus**: 指标收集
- **Grafana**: 可视化监控
- **Sentry**: 错误追踪
- **ELK Stack**: 日志分析

### 4. 备份策略

定期备份:
- 配置文件 (`.env`)
- 日志文件
- 数据库 (如果使用)

### 5. 更新和维护

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重启服务
sudo systemctl restart akshare-api
```

## 故障排查

### 服务无法启动

1. 检查日志: `journalctl -u akshare-api -n 50`
2. 检查端口占用: `netstat -tlnp | grep 8000`
3. 检查配置文件: 确保 `.env` 文件存在且配置正确

### API 返回 401 错误

检查 Token 配置是否正确,确保请求头包含有效的 Token。

### 性能问题

1. 增加 Worker 数量
2. 检查网络延迟
3. 查看 AKShare 数据源是否正常

### 内存占用过高

1. 减少 Worker 数量
2. 优化查询参数,减少返回数据量
3. 启用数据缓存

## 安全加固

1. **防火墙配置**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **限制访问**:
   - 仅允许特定 IP 访问
   - 使用 VPN 或内网访问

3. **定期更新**:
   - 及时更新系统和依赖包
   - 关注安全公告

4. **备份和恢复**:
   - 定期备份配置和数据
   - 测试恢复流程

## 联系支持

如有问题,请:
- 查看项目文档: [README.md](README.md)
- 提交 Issue: GitHub Issues
- 查看 AKShare 官方文档: https://akshare.akfamily.xyz/

