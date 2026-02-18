#!/bin/bash

# Скрипт развертывания OOO Shoes
echo "🚀 Начинаем развертывание OOO Shoes..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -r requirements_prod.txt

# Настройка переменных окружения
if [ ! -f .env ]; then
    echo "⚙️ Создание файла .env..."
    cp .env.example .env
    echo "✏️ Отредактируйте .env файл с вашими настройками"
fi

# Сборка статики
echo "🎨 Сборка статических файлов..."
python manage.py collectstatic --noinput --settings oooshoes.settings_prod

# Миграции
echo "🗄️ Применение миграций..."
python manage.py migrate --settings oooshoes.settings_prod

# Создание суперпользователя (опционально)
read -p "👤 Создать суперпользователя? (y/n): " create_user
if [ "$create_user" = "y" ]; then
    python manage.py createsuperuser --settings oooshoes.settings_prod
fi

echo "✅ Развертывание завершено!"
echo "🌐 Запустите сервер: gunicorn --bind 0.0.0.0:8000 oooshoes.wsgi:application --settings oooshoes.settings_prod"
