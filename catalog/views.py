from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact
from django.core.paginator import Paginator


def home(request):

    paid_products = Product.objects.filter(category__is_paid=True)
    free_products = Product.objects.filter(category__is_paid=False)

    paid_paginator = Paginator(paid_products, 10)
    paid_page_number = request.GET.get('paid_page')
    paid_page_obj = paid_paginator.get_page(paid_page_number)

    free_paginator = Paginator(free_products, 10)
    free_page_number = request.GET.get('free_page')
    free_page_obj = free_paginator.get_page(free_page_number)

    return render(request, "catalog/home.html", {
        'paid_products': paid_page_obj,
        'free_products': free_page_obj,
    })


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваш номер телефона и сообщение получено.")
    contact = Contact.objects.first()
    return render(request, "catalog/contacts.html", {"contacts": contact})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


def user_products(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')
        product = Product(
            name=name,
            description=description,
            price=price,
            image=image,
            category_id=category_id
        )
        product.save()
        return HttpResponse(f"Спасибо, Ваш продукт получен!")

    return render(request, 'catalog/user_products.html')
