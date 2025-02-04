from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование продукта")
    description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(upload_to="catalog/image", null=True, blank=True, verbose_name="Изображение продукта")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name="Категория продукта", null=True, blank=True
    )
    price = models.DecimalField(verbose_name="Цена за покупку", max_digits=10, decimal_places=2)
    created_at = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Дата последнего изменения", auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]

    def __str__(self):
        return f"{self.name} {self.price}"


class Contact(models.Model):
    address = models.CharField(max_length=255, verbose_name="Адрес", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Электронная почта", null=True, blank=True)

    class Meta:
        verbose_name = "Контакт магазина"
        verbose_name_plural = "Контакты магазина"

    def __str__(self):
        return f"{self.address} {self.phone}"
