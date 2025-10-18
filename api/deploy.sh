#!/bin/bash
# AKShare API 服务部署脚本 (Docker)

set -e

echo "======================================"
echo "   AKShare API Docker 部署脚本"
echo "======================================"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "✗ 错误: Docker 未安装,请先安装 Docker"
    exit 1
fi
echo "✓ Docker 已安装"

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "✗ 错误: Docker Compose 未安装,请先安装 Docker Compose"
    exit 1
fi
echo "✓ Docker Compose 已安装"

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠ 警告: .env 文件不存在"
    if [ -f "env.example" ]; then
        echo "? 是否使用 env.example 创建 .env 文件? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            cp env.example .env
            echo "✓ 已创建 .env 文件"
            echo "⚠ 请编辑 .env 文件,修改 API_TOKENS 等配置"
            echo "? 是否立即编辑? (y/n)"
            read -r edit_response
            if [[ "$edit_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                ${EDITOR:-nano} .env
            else
                echo "⚠ 请手动编辑 .env 文件后再继续"
                exit 0
            fi
        else
            echo "✗ 部署取消"
            exit 1
        fi
    fi
fi

echo ""
echo "======================================"
echo "   构建 Docker 镜像"
echo "======================================"
echo ""

# 构建镜像
docker-compose build

echo ""
echo "======================================"
echo "   启动服务"
echo "======================================"
echo ""

# 停止旧容器
docker-compose down

# 启动新容器
docker-compose up -d

echo ""
echo "======================================"
echo "   部署完成"
echo "======================================"
echo ""

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo "✓ 服务已成功启动"
    echo ""
    echo "服务信息:"
    docker-compose ps
    echo ""
    echo "访问地址:"
    echo "  - API 服务: http://localhost:8000"
    echo "  - 健康检查: http://localhost:8000/health"
    echo "  - API 文档: http://localhost:8000/docs (开发环境)"
    echo ""
    echo "查看日志:"
    echo "  docker-compose logs -f"
    echo ""
    echo "停止服务:"
    echo "  docker-compose down"
else
    echo "✗ 服务启动失败,请查看日志:"
    docker-compose logs
    exit 1
fi

