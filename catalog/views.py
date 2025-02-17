from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Contact
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        # Вызов метода get_context_data() базового класса с помощью super
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        paid_products = Product.objects.filter(category__is_paid=True)
        free_products = Product.objects.filter(category__is_paid=False)

        paid_paginator = Paginator(paid_products, 10)
        paid_page_number = self.request.GET.get("paid_page")
        context["paid_products"] = paid_paginator.get_page(paid_page_number)

        free_paginator = Paginator(free_products, 10)
        free_page_number = self.request.GET.get("free_page")
        context["free_products"] = free_paginator.get_page(free_page_number)
        return context


class ProductDetailView(DetailView):
    model = Product


class ContactView(View):
    def get(self, request, *args, **kwargs):
        contact = Contact.objects.first()
        return render(request, "catalog/contacts.html", {"contacts": contact})

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponseRedirect(reverse_lazy("catalog:contacts"))


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "price", "image", "category"]
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "price", "image", "category"]

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
