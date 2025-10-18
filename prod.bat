@echo off
REM Production Database Management Script
REM Usage: prod <command>

if "%1"=="" (
    echo Production Database Commands:
    echo   prod info          - Database information
    echo   prod stats         - Quick statistics
    echo   prod products      - List products
    echo   prod shell         - Django shell
    echo   prod migrate       - Run migrations
    echo   prod backup        - Create backup
    echo   prod update-images - Update product images to URLs
    echo   prod load-samples  - Load sample products
    goto :eof
)

if "%1"=="stats" (
    python prod_local.py stats
) else if "%1"=="products" (
    python prod_local.py products
) else if "%1"=="shell" (
    python prod_local.py shell
) else (
    python prod_manage_local.py %*
)