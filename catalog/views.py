from django.shortcuts import render
from django.http import HttpResponse


def home(requests):
    return render(requests, "catalog/home.html")


def contacts(requests):
    if requests.method == "POST":
        name = requests.POST.get("name")
        phone = requests.POST.get("phone")
        message = requests.POST.get("message")
        print(name, phone, message)
        return HttpResponse(f"Спасибо, {name}! Ваш номер телефона и сообщение получено.")
    return render(requests, "catalog/contacts.html")
