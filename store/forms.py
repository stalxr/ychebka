from django import forms
from .models import Product, Order

# Форма входа
class LoginForm(forms.Form):
    login = forms.CharField(
        label="Логин", 
        max_length=255, 
        widget=forms.TextInput(attrs={"autocomplete": "username"})
    )
    password = forms.CharField(
        label="Пароль", 
        max_length=255, 
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )

# Форма товара
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "article", "products_name", "unit", "price",
            "supplier", "manufacturer", "category",
            "sale", "count", "discription", "image",
        ]
        widgets = {
            "discription": forms.Textarea(attrs={"rows": 4})
        }

# Форма заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "article", "order_date", "delivery_date",
            "adress_pvz_id", "client_name",
            "verefication_code", "order_status",
        ]
