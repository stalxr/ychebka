from dataclasses import dataclass
from typing import Optional, Iterable, Callable
from functools import wraps

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Роли пользователей
ROLE_ADMIN = "Администратор"
ROLE_MANAGER = "Менеджер"
ROLE_CLIENT = "Авторизованный клиент"
ROLE_GUEST = "Гость"

# Данные пользователя в сессии
@dataclass(frozen=True)
class SessionUser:
    id: Optional[int]
    role: str
    full_name: str
    login: str

# Получение пользователя из сессии
def get_session_user(request: HttpRequest) -> SessionUser:
    user_id = request.session.get("user_id")
    role = request.session.get("user_role") or ROLE_GUEST
    full_name = request.session.get("user_full_name") or ""
    login = request.session.get("user_login") or ""
    return SessionUser(id=user_id, role=role, full_name=full_name, login=login)

# Вход в систему
def login_user(request: HttpRequest, user) -> None:
    request.session["user_id"] = int(user.id)
    request.session["user_role"] = user.user_role
    request.session["user_full_name"] = user.user_full_name
    request.session["user_login"] = user.login

# Выход из системы
def logout_user(request: HttpRequest) -> None:
    for k in ("user_id", "user_role", "user_full_name", "user_login"):
        if k in request.session:
            del request.session[k]
    request.session.flush()

# Проверка прав доступа
def require_role(roles: Iterable[str]):
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            role = request.session.get("user_role") or ROLE_GUEST
            if role not in set(roles):
                if not request.session.get("user_id"):
                    return redirect(reverse("login"))
                return redirect(reverse("products_list"))
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
