#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oooshoes.settings')
django.setup()

from store.models import AppUser, Product, Order

def create_demo_data():
    # Создаем пользователей
    users = [
        AppUser(
            user_role='Администратор',
            user_full_name='Иванов Иван',
            login='admin',
            password='admin'
        ),
        AppUser(
            user_role='Менеджер',
            user_full_name='Петров Петр',
            login='manager',
            password='manager'
        ),
        AppUser(
            user_role='Авторизованный клиент',
            user_full_name='Сидоров Сидор',
            login='client',
            password='client'
        )
    ]
    
    for user in users:
        user.save()
    
    # Создаем товары
    products = [
        Product(
            article='BOOT001',
            products_name='Классические ботинки',
            unit='пара',
            price=5999,
            supplier='ОбувьПром',
            manufacturer='Италия',
            category='Ботинки',
            sale=20,
            count=45,
            discription='Классические мужские ботинки из натуральной кожи',
            image='boots1.jpg'
        ),
        Product(
            article='SNEAK001',
            products_name='Спортивные кроссовки',
            unit='пара',
            price=3999,
            supplier='СпортМастер',
            manufacturer='Китай',
            category='Кроссовки',
            sale=15,
            count=120,
            discription='Удобные кроссовки для бега',
            image='sneakers1.jpg'
        ),
        Product(
            article='HEEL001',
            products_name='Женские туфли на каблуке',
            unit='пара',
            price=8999,
            supplier='Элегант',
            manufacturer='Испания',
            category='Туфли',
            sale=None,
            count=25,
            discription='Элегантные туфли на высоком каблуке',
            image='heels1.jpg'
        )
    ]
    
    for product in products:
        product.save()
    
    # Создаем заказы
    orders = [
        Order(
            article='BOOT001',
            order_date='2024-01-15',
            delivery_date='2024-01-20',
            adress_pvz_id=1,
            client_name='Сидоров Сидор',
            verefication_code=1234,
            order_status='Доставлен'
        ),
        Order(
            article='SNEAK001',
            order_date='2024-01-18',
            delivery_date='2024-01-25',
            adress_pvz_id=2,
            client_name='Сидоров Сидор',
            verefication_code=5678,
            order_status='В обработке'
        )
    ]
    
    for order in orders:
        order.save()
    
    print("✅ Демонстрационные данные созданы")
    print("👤 Пользователи: admin/admin, manager/manager, client/client")
    print("📦 Товары: 3 шт.")
    print("🛒 Заказы: 2 шт.")

if __name__ == '__main__':
    create_demo_data()
