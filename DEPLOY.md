# Деплой OOO Shoes

## Подготовка сервера

### 1. Установка зависимостей
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server

# CentOS/RHEL
sudo yum install python3 python3-pip python3-venv mysql-server
```

### 2. Настройка MySQL
```bash
# Создание базы данных
sudo mysql -u root -p
CREATE DATABASE ooo_shoes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ooo_shoes.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Деплой приложения
```bash
# Клонирование репозитория
git clone <your-repo-url>
cd Practis

# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements_prod.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env с вашими настройками
```

### 4. Настройка .env файла
```bash
DJANGO_SECRET_KEY=your-very-secret-key-here
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

MYSQL_HOST=localhost
MYSQL_USER=django_user
MYSQL_PASSWORD=your_password
MYSQL_DB=ooo_shoes
MYSQL_PORT=3306
```

### 5. Сборка статики и миграции
```bash
# Сборка статических файлов
python manage.py collectstatic --noinput

# Применение миграций
python manage.py migrate
```

### 6. Настройка Gunicorn
Создать файл systemd сервиса:
```bash
sudo nano /etc/systemd/system/ooo-shoes.service
```

Содержимое файла:
```ini
[Unit]
Description=OOO Shoes Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Practis
Environment="PATH=/path/to/Practis/.venv/bin"
ExecStart=/path/to/Practis/.venv/bin/gunicorn --workers 3 --bind unix:/run/ooo-shoes.sock oooshoes.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 7. Настройка Nginx
```bash
sudo nano /etc/nginx/sites-available/ooo-shoes
```

Содержимое файла:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/Practis;
    }
    
    location /media/ {
        root /path/to/Practis;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/ooo-shoes.sock;
    }
}
```

Активация сайта:
```bash
sudo ln -s /etc/nginx/sites-available/ooo-shoes /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Запуск сервисов
```bash
sudo systemctl daemon-reload
sudo systemctl start ooo-shoes
sudo systemctl enable ooo-shoes
sudo systemctl status ooo-shoes
```

## SSL сертификаты (рекомендуется)

### С помощью Certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Мониторинг

### Проверка статуса
```bash
sudo systemctl status ooo-shoes
sudo journalctl -u ooo-shoes -f
```

### Перезапуск после изменений
```bash
sudo systemctl restart ooo-shoes
```

## Резервное копирование

### База данных
```bash
mysqldump -u django_user -p ooo_shoes > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Файлы
```bash
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

## Обновление

```bash
cd /path/to/Practis
git pull origin main
source .venv/bin/activate
pip install -r requirements_prod.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart ooo-shoes
```

## Troubleshooting

### Ошибки подключения к БД
- Проверьте учетные данные в .env
- Убедитесь что MySQL сервер запущен
- Проверьте права доступа пользователя

### Ошибки статики
- Выполните `python manage.py collectstatic --noinput`
- Проверьте права доступа к папкам static/ и media/

### Ошибки Gunicorn
- Проверьте логи: `sudo journalctl -u ooo-shoes -f`
- Убедитесь что виртуальное окружение активировано
- Проверьте права доступа к сокет файлу
