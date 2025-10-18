#!/bin/bash
# AKShare 本地容器部署脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}AKShare 本地容器部署${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: 未检测到 Docker，请先安装 Docker${NC}"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}错误: 未检测到 Docker Compose，请先安装 Docker Compose${NC}"
    exit 1
fi

# 创建必要的目录
echo -e "${YELLOW}创建必要的目录...${NC}"
mkdir -p api/logs

# 停止并删除旧容器
echo -e "${YELLOW}停止旧容器...${NC}"
docker-compose down 2>/dev/null || true

# 构建镜像
echo -e "${YELLOW}构建 Docker 镜像...${NC}"
docker-compose build --no-cache

# 启动容器
echo -e "${YELLOW}启动容器...${NC}"
docker-compose up -d

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 5

# 检查容器状态
echo -e "${YELLOW}检查容器状态...${NC}"
docker-compose ps

# 检查健康状态
echo -e "${YELLOW}检查 API 健康状态...${NC}"
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API 服务已就绪!${NC}"
        break
    fi
    attempt=$((attempt + 1))
    echo -e "${YELLOW}等待中... ($attempt/$max_attempts)${NC}"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}警告: API 服务可能未正常启动，请检查日志${NC}"
    echo -e "${YELLOW}查看日志命令: docker-compose logs -f${NC}"
else
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}部署成功!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}API 地址: http://localhost:8000${NC}"
    echo -e "${GREEN}API 文档: http://localhost:8000/docs${NC}"
    echo -e "${GREEN}健康检查: http://localhost:8000/health${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}提示:${NC}"
    echo -e "  - 查看日志: ${YELLOW}docker-compose logs -f${NC}"
    echo -e "  - 停止服务: ${YELLOW}docker-compose down${NC}"
    echo -e "  - 重启服务: ${YELLOW}docker-compose restart${NC}"
    echo -e "  - 进入容器: ${YELLOW}docker-compose exec akshare-api bash${NC}"
    echo -e "${GREEN}========================================${NC}"
    
    # 测试 API
    echo -e "${YELLOW}测试 API 连接...${NC}"
    curl -s http://localhost:8000/health | python -m json.tool || echo ""
fi


