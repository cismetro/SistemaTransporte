# SistemaTransporte.ps1
# Script para criar a estrutura de diretórios e arquivos do projeto SistemaTransporte

# Definir a pasta raiz
$root = "SistemaTransporte"

# Criar diretórios
$dirs = @(
    "$root/models",
    "$root/routes",
    "$root/templates/patients",
    "$root/templates/drivers",
    "$root/templates/vehicles",
    "$root/templates/transports",
    "$root/static/css",
    "$root/static/js",
    "$root/static/img",
    "$root/data"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory | Out-Null
        Write-Host "Criado diretório: $dir"
    }
}

# Criar arquivos principais na raiz
$filesRoot = @(
    "app.py",
    "auth.py",
    "createdb.py",
    "config.py",
    "requirements.txt"
)

foreach ($file in $filesRoot) {
    $path = Join-Path $root $file
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType File | Out-Null
        Write-Host "Criado arquivo: $path"
    }
}

# Criar arquivos dentro de models
$filesModels = @(
    "__init__.py",
    "user.py",
    "patient.py",
    "driver.py",
    "vehicle.py",
    "transport.py"
)

foreach ($file in $filesModels) {
    $path = Join-Path "$root/models" $file
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType File | Out-Null
        Write-Host "Criado arquivo: $path"
    }
}

# Criar arquivos dentro de routes
$filesRoutes = @(
    "__init__.py",
    "main.py",
    "patients.py",
    "drivers.py",
    "vehicles.py",
    "transports.py"
)

foreach ($file in $filesRoutes) {
    $path = Join-Path "$root/routes" $file
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType File | Out-Null
        Write-Host "Criado arquivo: $path"
    }
}

# Criar templates principais
$filesTemplates = @(
    "base.html",
    "login.html",
    "dashboard.html"
)

foreach ($file in $filesTemplates) {
    $path = Join-Path "$root/templates" $file
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType File | Out-Null
        Write-Host "Criado arquivo: $path"
    }
}

# Criar arquivos em static
$filesCss = @("style.css")
foreach ($file in $filesCss) {
    $path = Join-Path "$root/static/css" $file
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType File | Out-Null
        Write-Host "Criado arquivo: $path"
    }
}

$filesJs = @("main.js")
foreach ($file in $filesJs) {
    $path = Join-Path "$root/static/js" $file
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType File | Out-Null
        Write-Host "Criado arquivo: $path"
    }
}

# Criar banco de dados vazio
$databasePath = "$root/data/database.db"
if (-not (Test-Path $databasePath)) {
    New-Item -Path $databasePath -ItemType File | Out-Null
    Write-Host "Criado banco de dados: $databasePath"
}

Write-Host "`nEstrutura do projeto SistemaTransporte criada com sucesso!"
