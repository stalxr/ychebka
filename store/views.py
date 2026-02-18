from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import AppUser, Product, Order
from .forms import LoginForm, ProductForm, OrderForm
from .auth import (
    get_session_user, login_user, logout_user,
    require_role,
    ROLE_ADMIN, ROLE_MANAGER, ROLE_CLIENT, ROLE_GUEST,
)

# Авторизация
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.session.get("user_id"):
        return redirect(reverse("products_list"))

    form = LoginForm(request.POST or None)
    error = None

    if request.method == "POST" and form.is_valid():
        login = form.cleaned_data["login"].strip()
        password = form.cleaned_data["password"]
        
        try:
            user = AppUser.objects.get(login=login, password=password)
        except AppUser.DoesNotExist:
            user = None

        if user is None:
            error = "Неверный логин или пароль."
        else:
            login_user(request, user)
            return redirect(reverse("products_list"))

    return render(request, "login.html", {
        "form": form,
        "error": error,
        "session_user": get_session_user(request),
    })

def logout_view(request):
    logout_user(request)
    return redirect(reverse("login"))

# Список товаров
@require_http_methods(["GET"])
def products_list(request):
    session_user = get_session_user(request)
    qs = Product.objects.all()

    # Права на фильтрацию
    can_filter = session_user.role in (ROLE_MANAGER, ROLE_ADMIN)

    # Параметры фильтрации
    q = (request.GET.get("q") or "").strip()
    category = (request.GET.get("category") or "").strip()
    manufacturer = (request.GET.get("manufacturer") or "").strip()
    supplier = (request.GET.get("supplier") or "").strip()
    sort = (request.GET.get("sort") or "").strip()

    if can_filter:
        # Поиск
        if q:
            qs = qs.filter(
                Q(article__icontains=q) |
                Q(products_name__icontains=q) |
                Q(category__icontains=q) |
                Q(manufacturer__icontains=q) |
                Q(supplier__icontains=q) |
                Q(discription__icontains=q)
            )
        
        # Фильтры
        if category:
            qs = qs.filter(category=category)
        if manufacturer:
            qs = qs.filter(manufacturer=manufacturer)
        if supplier:
            qs = qs.filter(supplier=supplier)

        # Сортировка
        sort_map = {
            "price_asc": "price",
            "price_desc": "-price",
            "name_asc": "products_name",
            "name_desc": "-products_name",
            "count_asc": "count",
            "count_desc": "-count",
            "category_asc": "category",
            "category_desc": "-category",
        }
        if sort in sort_map:
            qs = qs.order_by(sort_map[sort])
    else:
        # Для гостей и клиентов отключаем фильтры
        q = category = manufacturer = supplier = sort = ""

    # Получаем уникальные значения для фильтров
    categories = manufacturers = suppliers = []
    if can_filter:
        categories = list(Product.objects.values_list("category", flat=True).distinct().order_by("category"))
        manufacturers = list(Product.objects.values_list("manufacturer", flat=True).distinct().order_by("manufacturer"))
        suppliers = list(Product.objects.values_list("supplier", flat=True).distinct().order_by("supplier"))

    return render(request, "products_list.html", {
        "products": qs,
        "session_user": session_user,
        "can_filter": can_filter,
        "q": q,
        "category": category,
        "manufacturer": manufacturer,
        "supplier": supplier,
        "sort": sort,
        "categories": categories,
        "manufacturers": manufacturers,
        "suppliers": suppliers,
    })

@require_role([ROLE_ADMIN])
@require_http_methods(["GET", "POST"])
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("products_list"))
    return render(request, "product_form.html", {"form": form, "mode": "create", "session_user": get_session_user(request)})

@require_role([ROLE_ADMIN])
@require_http_methods(["GET", "POST"])
def product_edit(request, pk: int):
    obj = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("products_list"))
    return render(request, "product_form.html", {"form": form, "mode": "edit", "session_user": get_session_user(request), "object": obj})

@require_role([ROLE_ADMIN])
@require_http_methods(["GET", "POST"])
def product_delete(request, pk: int):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(reverse("products_list"))
    return render(request, "confirm_delete.html", {
        "title": "Удаление товара",
        "message": f"Удалить товар: {obj.products_name} ({obj.article})?",
        "session_user": get_session_user(request),
    })

@require_http_methods(["GET"])
def orders_list(request):
    session_user = get_session_user(request)

    if session_user.role == ROLE_GUEST:
        return redirect(reverse("login"))

    if session_user.role == ROLE_CLIENT:
        qs = Order.objects.filter(client_name=session_user.full_name).order_by("-id")
    else:
        qs = Order.objects.all().order_by("-id")

    can_manage = session_user.role == ROLE_ADMIN

    return render(request, "orders_list.html", {
        "orders": qs,
        "session_user": session_user,
        "can_manage": can_manage,
        "is_client": session_user.role == ROLE_CLIENT,
    })

@require_role([ROLE_ADMIN])
@require_http_methods(["GET", "POST"])
def order_create(request):
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("orders_list"))
    return render(request, "order_form.html", {"form": form, "mode": "create", "session_user": get_session_user(request)})

@require_role([ROLE_ADMIN])
@require_http_methods(["GET", "POST"])
def order_edit(request, pk: int):
    obj = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("orders_list"))
    return render(request, "order_form.html", {"form": form, "mode": "edit", "session_user": get_session_user(request), "object": obj})

@require_role([ROLE_ADMIN])
@require_http_methods(["GET", "POST"])
def order_delete(request, pk: int):
    obj = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(reverse("orders_list"))
    return render(request, "confirm_delete.html", {
        "title": "Удаление заказа",
        "message": f"Удалить заказ #{obj.id} клиента: {obj.client_name}?",
        "session_user": get_session_user(request),
    })
