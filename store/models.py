from django.db import models

# Пользователи системы
class AppUser(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    user_role = models.CharField(max_length=255, db_column="UserRole")
    user_full_name = models.CharField(max_length=255, db_column="UserFullName")
    login = models.CharField(max_length=255, db_column="Login")
    password = models.CharField(max_length=255, db_column="Password")

    class Meta:
        managed = False
        db_table = "Users"

    def __str__(self) -> str:
        return f"{self.user_full_name} ({self.user_role})"

# Товары
class Product(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    article = models.CharField(max_length=255, db_column="Article")
    products_name = models.CharField(max_length=255, db_column="ProductsName")
    unit = models.CharField(max_length=255, db_column="Unit")
    price = models.IntegerField(db_column="Price")
    supplier = models.CharField(max_length=255, db_column="Supplier")
    manufacturer = models.CharField(max_length=255, db_column="Manufacturer")
    category = models.CharField(max_length=255, db_column="Category")
    sale = models.IntegerField(null=True, blank=True, db_column="Sale")
    count = models.IntegerField(db_column="Count")
    discription = models.TextField(null=True, blank=True, db_column="Discription")
    image = models.CharField(max_length=255, null=True, blank=True, db_column="Image")

    class Meta:
        managed = False
        db_table = "Products"

    def __str__(self) -> str:
        return f"{self.article} - {self.products_name}"

# Заказы
class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    article = models.CharField(max_length=1024, db_column="Article")
    order_date = models.CharField(max_length=255, db_column="OrderDate")
    delivery_date = models.CharField(max_length=255, db_column="DeliveryDate")
    adress_pvz_id = models.IntegerField(db_column="AdressPVZ_ID")
    client_name = models.CharField(max_length=255, db_column="ClientName")
    verefication_code = models.IntegerField(db_column="VereficationCode")
    order_status = models.CharField(max_length=255, db_column="OrderStatus")

    class Meta:
        managed = False
        db_table = "Orders"

    def __str__(self) -> str:
        return f"Заказ #{self.id} ({self.client_name})"
