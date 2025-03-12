from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import ProductForm
from .models import Contact, Product


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


class ProductDetailView(LoginRequiredMixin, DetailView):
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        product = self.get_object()
        if self.request.user != product.owner:
            return HttpResponseForbidden("У вас нет прав на редактирование продукта.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if not (request.user == product.owner or request.user.has_perm("catalog.can_unpublish_product")):
            return HttpResponseForbidden("У вас нет прав на удаление продукта.")
        product.delete()
        return redirect("catalog:product_list")


class ProductPublicationView(PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect("catalog:product_detail", pk=product.pk)
