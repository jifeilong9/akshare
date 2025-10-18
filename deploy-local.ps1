# AKShare 本地容器部署脚本 (Windows PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "AKShare 本地容器部署" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 检查 Docker 是否安装
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未检测到 Docker，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 检查 Docker Compose 是否可用
$dockerComposeCmd = $null
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    $dockerComposeCmd = "docker-compose"
} elseif (docker compose version 2>$null) {
    $dockerComposeCmd = "docker compose"
} else {
    Write-Host "错误: 未检测到 Docker Compose" -ForegroundColor Red
    exit 1
}

# 创建必要的目录
Write-Host "创建必要的目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "api\logs" | Out-Null

# 停止并删除旧容器
Write-Host "停止旧容器..." -ForegroundColor Yellow
if ($dockerComposeCmd -eq "docker-compose") {
    docker-compose down 2>$null
} else {
    docker compose down 2>$null
}

# 构建镜像
Write-Host "构建 Docker 镜像..." -ForegroundColor Yellow
if ($dockerComposeCmd -eq "docker-compose") {
    docker-compose build --no-cache
} else {
    docker compose build --no-cache
}

# 启动容器
Write-Host "启动容器..." -ForegroundColor Yellow
if ($dockerComposeCmd -eq "docker-compose") {
    docker-compose up -d
} else {
    docker compose up -d
}

# 等待服务启动
Write-Host "等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查容器状态
Write-Host "检查容器状态..." -ForegroundColor Yellow
if ($dockerComposeCmd -eq "docker-compose") {
    docker-compose ps
} else {
    docker compose ps
}

# 检查健康状态
Write-Host "检查 API 健康状态..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$healthy = $false

while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ API 服务已就绪!" -ForegroundColor Green
            $healthy = $true
            break
        }
    } catch {
        # 继续等待
    }
    $attempt++
    Write-Host "等待中... ($attempt/$maxAttempts)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
}

if (!$healthy) {
    Write-Host "警告: API 服务可能未正常启动，请检查日志" -ForegroundColor Red
    Write-Host "查看日志命令: docker-compose logs -f" -ForegroundColor Yellow
} else {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "部署成功!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "API 地址: http://localhost:8000" -ForegroundColor Green
    Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Green
    Write-Host "健康检查: http://localhost:8000/health" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "提示:" -ForegroundColor Yellow
    Write-Host "  - 查看日志: " -NoNewline
    Write-Host "$dockerComposeCmd logs -f" -ForegroundColor Yellow
    Write-Host "  - 停止服务: " -NoNewline
    Write-Host "$dockerComposeCmd down" -ForegroundColor Yellow
    Write-Host "  - 重启服务: " -NoNewline
    Write-Host "$dockerComposeCmd restart" -ForegroundColor Yellow
    Write-Host "  - 进入容器: " -NoNewline
    Write-Host "$dockerComposeCmd exec akshare-api bash" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Green
    
    # 测试 API
    Write-Host "测试 API 连接..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health"
        Write-Host ($response | ConvertTo-Json)
    } catch {
        Write-Host "无法获取 API 响应" -ForegroundColor Yellow
    }
}


