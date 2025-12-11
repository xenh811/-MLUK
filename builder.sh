#!/bin/bash
set -e


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Поточна директорія: $(pwd)"
echo "Файли в директорії:"
ls -la


if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Запуск бота
python bot.py
