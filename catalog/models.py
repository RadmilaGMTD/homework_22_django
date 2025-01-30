from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return {self.name}

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование продукта")
    description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(upload_to="catalog/image", null=True, blank=True, verbose_name="Изображение продукта")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория продукта", null=True, blank=True)
    price = models.CharField(max_length=50, verbose_name="Цена за покупку")
    created_at = models.DateField(verbose_name="Дата создания")
    updated_at = models.DateField(verbose_name="Дата последнего изменения")

    def __str__(self):
        return f"{self.name} {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]

