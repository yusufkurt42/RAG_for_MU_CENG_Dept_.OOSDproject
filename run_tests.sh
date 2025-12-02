#!/bin/bash
# Run all tests with coverage

echo "Running tests..."
pytest python/tests/ -v --cov=python/rag --cov-report=html --cov-report=term

echo ""
echo "Coverage report generated in htmlcov/index.html"
