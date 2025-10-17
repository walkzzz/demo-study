# 启动 Web 界面服务

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  日常办公超级智能体 - Web 界面启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 环境
Write-Host "[1/4] 检查 Python 环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python 未安装或不在 PATH 中" -ForegroundColor Red
    exit 1
}

# 检查依赖
Write-Host ""
Write-Host "[2/4] 检查依赖包..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "langchain", "pyyaml")
$missingPackages = @()

foreach ($package in $packages) {
    $result = python -c "import $package" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package 已安装" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $package 未安装" -ForegroundColor Red
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "缺少依赖包，正在安装..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# 检查 Ollama 服务
Write-Host ""
Write-Host "[3/4] 检查 Ollama 服务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method GET -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  ✓ Ollama 服务正在运行" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Ollama 服务未启动或无法访问" -ForegroundColor Yellow
    Write-Host "  提示: 请确保 Ollama 服务正在运行 (http://localhost:11434)" -ForegroundColor Yellow
}

# 检查 Web 文件
Write-Host ""
Write-Host "[4/4] 检查 Web 文件..." -ForegroundColor Yellow
$webFiles = @("web\index.html", "web\styles.css", "web\app.js")
$allFilesExist = $true

foreach ($file in $webFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file 存在" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file 缺失" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "错误: Web 文件缺失，请检查 web/ 目录" -ForegroundColor Red
    exit 1
}

# 启动服务
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 API 服务..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "服务地址:" -ForegroundColor Green
Write-Host "  🌐 Web 界面: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  📖 API 文档: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  🔧 健康检查: http://127.0.0.1:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
python src\api\main.py
