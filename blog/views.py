from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Blog
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings


class BlogListView(ListView):
    model = Blog
    def get_queryset(self):
        return Blog.objects.filter(is_publication=True)


class BlogDetailView(DetailView):
    model = Blog
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])

        if obj.views == 100:
            send_mail(
                'Поздравляем!',
                f'Ваша статья "{obj.title}" достигла 100 просмотров!',
                settings.DEFAULT_FROM_EMAIL,
                ['rmiftyaeva@mail.ru'],
                fail_silently=False,
            )
        return obj


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_publication']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_publication']
    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
