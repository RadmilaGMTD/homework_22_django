from django import forms
from django.core.exceptions import ValidationError

from .mixins import FormControlMixin
from .models import Blog


class BlogForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content", "image", "is_publication"]
