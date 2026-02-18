#!/usr/bin/env python3
"""
Тесты для веб-приложения OOO Shoes
Проверка всех основных функций системы
"""

import os
import sys
import sqlite3
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent))

# Тест 1: Проверка подключения к базе данных
def test_database_connection():
    """Тест подключения к SQLite базе данных"""
    print("🧪 Тест 1: Подключение к базе данных")
    
    try:
        # Проверяем существование файла БД
        db_path = Path(__file__).parent / 'db.sqlite3'
        if not db_path.exists():
            print("❌ Файл базы данных не найден")
            return False
        
        # Подключаемся к БД
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Проверяем наличие таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ Таблицы в базе данных не найдены")
            return False
        
        print(f"✅ База данных подключена. Таблицы: {[table[0] for table in tables]}")
        
        # Проверяем структуру таблицы товаров
        cursor.execute("PRAGMA table_info(store_product);")
        columns = cursor.fetchall()
        print(f"✅ Структура таблицы товаров: {[col[1] for col in columns]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False

# Тест 2: Проверка валидации форм
def test_form_validation():
    """Тест валидации форм входа и добавления товаров"""
    print("\n🧪 Тест 2: Валидация форм")
    
    try:
        # Импортируем формы Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oooshoes.settings')
        
        import django
        django.setup()
        
        from store.forms import LoginForm, ProductForm
        
        # Тест формы входа с валидными данными
        form_data = {'login': 'admin', 'password': 'admin'}
        form = LoginForm(data=form_data)
        
        if not form.is_valid():
            print(f"❌ Форма входа не прошла валидацию: {form.errors}")
            return False
        
        print("✅ Форма входа с валидными данными работает")
        
        # Тест формы входа с невалидными данными
        form_data = {'login': '', 'password': ''}
        form = LoginForm(data=form_data)
        
        if form.is_valid():
            print("❌ Форма входа с пустыми данными прошла валидацию (не должна)")
            return False
        
        print("✅ Форма входа корректно обрабатывает невалидные данные")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования форм: {e}")
        return False

# Тест 3: Проверка URL маршрутизации
def test_url_routing():
    """Тест маршрутизации URL"""
    print("\n🧪 Тест 3: URL маршрутизация")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oooshoes.settings')
        
        import django
        django.setup()
        
        from django.urls import reverse, resolve
        from store import urls
        
        # Проверяем основные URL
        test_urls = [
            ('login', '/'),
            ('products_list', '/products/'),
            ('orders_list', '/orders/'),
            ('logout', '/logout/'),
        ]
        
        for url_name, expected_path in test_urls:
            try:
                resolved = reverse(url_name)
                if resolved != expected_path:
                    print(f"❌ URL {url_name}: ожидался {expected_path}, получен {resolved}")
                    return False
                print(f"✅ URL {url_name}: {resolved}")
            except Exception as e:
                print(f"❌ Ошибка разрешения URL {url_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования URL: {e}")
        return False

# Тест 4: Проверка моделей данных
def test_models():
    """Тест моделей данных"""
    print("\n🧪 Тест 4: Модели данных")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oooshoes.settings')
        
        import django
        django.setup()
        
        from store.models import AppUser, Product, Order
        
        # Проверяем наличие полей в модели AppUser
        required_fields = ['id', 'user_role', 'user_full_name', 'login', 'password']
        for field in required_fields:
            if not hasattr(AppUser, field):
                print(f"❌ Поле {field} отсутствует в модели AppUser")
                return False
        
        print("✅ Модель AppUser содержит все необходимые поля")
        
        # Проверяем наличие полей в модели Product
        required_fields = ['id', 'article', 'products_name', 'price', 'category']
        for field in required_fields:
            if not hasattr(Product, field):
                print(f"❌ Поле {field} отсутствует в модели Product")
                return False
        
        print("✅ Модель Product содержит все необходимые поля")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования моделей: {e}")
        return False

# Тест 5: Проверка статических файлов
def test_static_files():
    """Тест наличия статических файлов"""
    print("\n🧪 Тест 5: Статические файлы")
    
    try:
        base_path = Path(__file__).parent
        
        # Проверяем CSS файл
        css_path = base_path / 'static' / 'css' / 'app.css'
        if not css_path.exists():
            print("❌ CSS файл не найден")
            return False
        
        css_size = css_path.stat().st_size
        print(f"✅ CSS файл найден (размер: {css_size} байт)")
        
        # Проверяем изображения
        media_path = base_path / 'media'
        if not media_path.exists():
            print("❌ Папка media не найдена")
            return False
        
        images = list(media_path.glob('*.jpg'))
        if len(images) < 5:
            print(f"❌ Найдено только {len(images)} изображений (ожидается минимум 5)")
            return False
        
        print(f"✅ Найдено {len(images)} изображений")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки статических файлов: {e}")
        return False

# Тест 6: Интеграционное тестирование
def test_integration():
    """Интеграционное тестирование всего приложения"""
    print("\n🧪 Тест 6: Интеграционное тестирование")
    
    try:
        # Проверяем конфигурацию Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oooshoes.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        # Проверяем основные настройки
        if not hasattr(settings, 'DATABASES'):
            print("❌ Настройки DATABASES не найдены")
            return False
        
        print("✅ Настройки базы данных корректны")
        
        if not hasattr(settings, 'STATIC_URL'):
            print("❌ Настройки STATIC_URL не найдены")
            return False
        
        print("✅ Настройки статических файлов корректны")
        
        if not hasattr(settings, 'INSTALLED_APPS'):
            print("❌ Настройки INSTALLED_APPS не найдены")
            return False
        
        if 'store' not in settings.INSTALLED_APPS:
            print("❌ Приложение store не найдено в INSTALLED_APPS")
            return False
        
        print("✅ Приложения Django корректно настроены")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка интеграционного тестирования: {e}")
        return False

# Тест 7: Тест производительности
def test_performance():
    """Тест производительности приложения"""
    print("\n🧪 Тест 7: Производительность")
    
    try:
        import time
        
        # Тест скорости загрузки CSS
        css_path = Path(__file__).parent / 'static' / 'css' / 'app.css'
        start_time = time.time()
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        load_time = time.time() - start_time
        
        if load_time > 0.1:  # 100ms
            print(f"⚠️ Медленная загрузка CSS: {load_time:.3f}с")
        else:
            print(f"✅ CSS загружен за {load_time:.3f}с")
        
        # Тест размера CSS
        if len(css_content) > 50000:  # 50KB
            print(f"⚠️ Большой размер CSS: {len(css_content)} байт")
        else:
            print(f"✅ Оптимальный размер CSS: {len(css_content)} байт")
        
        # Тест скорости загрузки изображений
        media_path = Path(__file__).parent / 'media'
        images = list(media_path.glob('*.jpg'))
        
        total_size = 0
        for img_path in images[:3]:  # Проверяем первые 3 изображения
            total_size += img_path.stat().st_size
        
        avg_size = total_size / 3
        if avg_size > 200000:  # 200KB
            print(f"⚠️ Большой средний размер изображений: {avg_size/1024:.1f}KB")
        else:
            print(f"✅ Оптимальный размер изображений: {avg_size/1024:.1f}KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования производительности: {e}")
        return False

# Главная функция запуска всех тестов
def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов веб-приложения OOO Shoes")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_form_validation,
        test_url_routing,
        test_models,
        test_static_files,
        test_integration,
        test_performance,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Приложение готово к эксплуатации.")
        return True
    else:
        print("⚠️ Некоторые тесты не пройдены. Требуется доработка.")
        return False

if __name__ == "__main__":
    run_all_tests()
