@echo off
REM Скрипт развертывания OOO Shoes для Windows
echo 🚀 Начинаем развертывание OOO Shoes...

REM Создание виртуального окружения
echo 📦 Создание виртуального окружения...
python -m venv .venv
call .venv\Scripts\activate.bat

REM Установка зависимостей
echo 📥 Установка зависимостей...
pip install -r requirements_prod.txt

REM Настройка переменных окружения
if not exist .env (
    echo ⚙️ Создание файла .env...
    copy .env.example .env
    echo ✏️ Отредактируйте .env файл с вашими настройками
)

REM Сборка статики
echo 🎨 Сборка статических файлов...
python manage.py collectstatic --noinput --settings oooshoes.settings_prod

REM Миграции
echo 🗄️ Применение миграций...
python manage.py migrate --settings oooshoes.settings_prod

REM Создание суперпользователя
set /p create_user="👤 Создать суперпользователя? (y/n): "
if /i "%create_user%"=="y" (
    python manage.py createsuperuser --settings oooshoes.settings_prod
)

echo ✅ Развертывание завершено!
echo 🌐 Запустите сервер: gunicorn --bind 0.0.0.0:8000 oooshoes.wsgi:application --settings oooshoes.settings_prod
pause
