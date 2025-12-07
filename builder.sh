#!/bin/bash
set -e

# Переходимо у директорію, де лежить скрипт
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Поточна директорія: $(pwd)"
echo "Файли в директорії:"
ls -la

# Встановлюємо залежності Python
if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Запуск бота
python bot.py
