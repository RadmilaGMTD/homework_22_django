from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def home(request):
    products = Product.objects.order_by("created_at")[:5]
    print(products)
    return render(request, "catalog/home.html", {'products': products})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(name, phone, message)
        return HttpResponse(f"Спасибо, {name}! Ваш номер телефона и сообщение получено.")
    contact = Contact.objects.first()
    print(contact)
    return render(request, "catalog/contacts.html", {"contacts": contact})
