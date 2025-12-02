# CodeWhisper FFmpeg 自动安装脚本 (Windows)
# 使用方法: powershell -ExecutionPolicy Bypass -File install_ffmpeg_windows.ps1

Write-Host "`n" -ForegroundColor Green
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║        CodeWhisper FFmpeg 自动安装脚本 (Windows)              ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  本脚本需要管理员权限运行。正在重新启动..." -ForegroundColor Yellow
    Write-Host "请在弹出的 UAC 对话框中选择『是』允许权限。`n" -ForegroundColor Yellow
    Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

# 检查是否已安装 FFmpeg
Write-Host "🔍 检查 FFmpeg 是否已安装..." -ForegroundColor Cyan
$ffmpegCheck = $null
try {
    $ffmpegCheck = ffmpeg -version 2>$null
}
catch {
    $ffmpegCheck = $null
}

if ($ffmpegCheck) {
    Write-Host "✅ FFmpeg 已安装！`n" -ForegroundColor Green
    ffmpeg -version | Select-Object -First 1
    exit 0
}

# 检查是否安装了 Chocolatey
Write-Host "`n📦 检查 Chocolatey 包管理器..." -ForegroundColor Cyan
$chocoCheck = $null
try {
    $chocoCheck = choco --version 2>$null
}
catch {
    $chocoCheck = $null
}

if (-not $chocoCheck) {
    Write-Host "⚙️  Chocolatey 未安装，正在安装 Chocolatey..." -ForegroundColor Yellow
    Write-Host "这可能需要几分钟...`n" -ForegroundColor Gray

    # 安装 Chocolatey
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    $installChocolatey = {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }

    try {
        Invoke-Command -ScriptBlock $installChocolatey
        Write-Host "✅ Chocolatey 安装成功！`n" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Chocolatey 安装失败: $_`n" -ForegroundColor Red
        Write-Host "请手动安装 Chocolatey: https://chocolatey.org/install`n" -ForegroundColor Yellow
        Write-Host "或使用其他方式安装 FFmpeg:`n" -ForegroundColor Yellow
        Write-Host "  • 访问 https://ffmpeg.org/download.html`n" -ForegroundColor Gray
        Write-Host "  • 或使用 winget install ffmpeg`n" -ForegroundColor Gray
        exit 1
    }
}

# 安装 FFmpeg
Write-Host "📥 使用 Chocolatey 安装 FFmpeg..." -ForegroundColor Cyan
Write-Host "这可能需要几分钟...`n" -ForegroundColor Gray

try {
    choco install ffmpeg -y
    Write-Host "`n✅ FFmpeg 安装成功！`n" -ForegroundColor Green

    # 验证安装
    Write-Host "✓ 验证 FFmpeg 安装..." -ForegroundColor Cyan
    ffmpeg -version | Select-Object -First 1
    Write-Host "`n🎉 FFmpeg 已准备就绪，现在可以运行 CodeWhisper 了！`n" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ FFmpeg 安装失败: $_`n" -ForegroundColor Red
    Write-Host "请手动安装 FFmpeg，访问: https://ffmpeg.org/download.html`n" -ForegroundColor Yellow
    exit 1
}

exit 0
