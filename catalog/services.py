from django.core.cache import cache

from config.settings import CACHE_ENABLE

from .models import Product


class ProductService:
    @staticmethod
    def product_in_category(category_id):
        product = Product.objects.filter(category_id=category_id)
        if not product.exists():
            return []
        return product

    @staticmethod
    def get_products_from_cache():
        if not CACHE_ENABLE:
            return Product.objects.all()
        key = "product_list"
        products = cache.get(key)
        if products is not None:
            return products
        products = Product.objects.all()
        cache.set(key, products)
        return products
