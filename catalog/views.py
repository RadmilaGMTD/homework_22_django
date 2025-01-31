from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def home(requests):
    products = Product.objects.all()
    print(products)
    return render(requests, "catalog/home.html", {'products': products})


def contacts(requests):
    if requests.method == "POST":
        name = requests.POST.get("name")
        phone = requests.POST.get("phone")
        message = requests.POST.get("message")
        print(name, phone, message)
        return HttpResponse(f"Спасибо, {name}! Ваш номер телефона и сообщение получено.")
    return render(requests, "catalog/contacts.html")
