from django.urls import path, include
from store import views as store_views

urlpatterns = [
    path("", store_views.login_view, name="login"),
    path("logout/", store_views.logout_view, name="logout"),
    path("", include("store.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)