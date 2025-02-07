from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def home(request):
    paid_products = Product.objects.filter(category__name="Платные занятия")
    free_products = Product.objects.filter(category__name="Бесплатные занятия")
    return render(request, "catalog/home.html", {'paid_products': paid_products, 'free_products': free_products})


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
