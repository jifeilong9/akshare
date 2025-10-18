#!/bin/bash
# AKShare API 服务启动脚本

set -e

echo "======================================"
echo "   AKShare FastAPI Service Starter"
echo "======================================"
echo ""

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "⚠ 虚拟环境不存在,正在创建..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "✓ 激活虚拟环境..."
source venv/bin/activate

# 安装/更新依赖
echo "✓ 安装依赖包..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠ .env 文件不存在,复制示例文件..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✓ 已创建 .env 文件,请修改其中的配置"
        echo "⚠ 特别注意: 请修改 API_TOKENS 为安全的 token"
    else
        echo "✗ 找不到 env.example 文件"
        exit 1
    fi
fi

# 创建日志目录
mkdir -p logs
echo "✓ 日志目录已创建"

echo ""
echo "======================================"
echo "   启动服务"
echo "======================================"
echo ""

# 读取配置
export $(grep -v '^#' .env | xargs)

# 启动服务
if [ "${ENVIRONMENT}" = "production" ]; then
    echo "✓ 生产环境模式"
    uvicorn main:app \
        --host ${HOST:-0.0.0.0} \
        --port ${PORT:-8000} \
        --workers ${WORKERS:-4} \
        --log-level info
else
    echo "✓ 开发环境模式 (自动重载)"
    uvicorn main:app \
        --host ${HOST:-0.0.0.0} \
        --port ${PORT:-8000} \
        --reload \
        --log-level debug
fi

