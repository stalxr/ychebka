#!/usr/bin/env python3
"""
Простой тест для проверки настроек Django
"""
import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Импортируем настройки
    from oooshoes.settings import DATABASES, INSTALLED_APPS, STATIC_URL, MEDIA_URL
    
    print("✅ Настройки Django успешно импортированы")
    print(f"📊 База данных: {DATABASES['default']['ENGINE']}")
    print(f"🎨 Установленные приложения: {', '.join(INSTALLED_APPS)}")
    print(f"📁 Статические файлы: {STATIC_URL}")
    print(f"🖼️ Медиа файлы: {MEDIA_URL}")
    
    # Проверяем модели
    try:
        from store.models import AppUser, Product, Order
        print("✅ Модели успешно импортированы")
        print(f"👤 Пользователи: {AppUser._meta.db_table}")
        print(f"📦 Товары: {Product._meta.db_table}")
        print(f"🛒 Заказы: {Order._meta.db_table}")
    except Exception as e:
        print(f"❌ Ошибка импорта моделей: {e}")
        
    # Проверяем URL
    try:
        from oooshoes.urls import urlpatterns
        print(f"✅ URL конфигурация загружена ({len(urlpatterns)} маршрутов)")
    except Exception as e:
        print(f"❌ Ошибка импорта URL: {e}")
        
    print("\n🎉 Базовая проверка прошла успешно!")
    print("💡 Для запуска сервера используйте: python manage.py runserver")
    
except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    sys.exit(1)
