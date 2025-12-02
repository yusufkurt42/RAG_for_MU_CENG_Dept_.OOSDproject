# Run all tests with coverage

Write-Host "Running tests..." -ForegroundColor Green
pytest python/tests/ -v --cov=python/rag --cov-report=html --cov-report=term

Write-Host ""
Write-Host "Coverage report generated in htmlcov/index.html" -ForegroundColor Cyan
