#!/bin/bash
echo "=== SECURITY CHECK ==="
ERRORS=0

echo "1. Перевірка секретів у коді..."
if grep -rn "password\s*=" app/ --include="*.py" | grep -v password_hash | grep -v "# " | grep -v "Field(" | grep -v "def " | grep -v getenv; then
    echo "  ПОПЕРЕДЖЕННЯ: можливі захардкоджені паролі"
    ERRORS=$((ERRORS + 1))
else
    echo "  OK: Секрети не знайдені у коді"
fi

echo "2. Перевірка .gitignore..."
if grep -q "\.env" .gitignore 2>/dev/null; then
    echo "  OK: .env додано до .gitignore"
else
    echo "  ПОМИЛКА: .env НЕ в .gitignore!"
    ERRORS=$((ERRORS + 1))
fi

echo "3. Перевірка Dockerfile..."
if grep -q "^USER" Dockerfile; then
    echo "  OK: Non-root user налаштований"
else
    echo "  ПОМИЛКА: Контейнер працює від root!"
    ERRORS=$((ERRORS + 1))
fi

if grep -q "HEALTHCHECK" Dockerfile; then
    echo "  OK: HEALTHCHECK налаштований"
else
    echo "  ПОПЕРЕДЖЕННЯ: HEALTHCHECK відсутній"
fi

echo "=========================="
if [ $ERRORS -eq 0 ]; then
    echo "SECURITY CHECK PASSED"
else
    echo "SECURITY CHECK FAILED ($ERRORS проблем)"
fi
exit $ERRORS