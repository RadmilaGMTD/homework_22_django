from django import forms
from django.core.exceptions import ValidationError

from .mixins import FormControlMixin
from .models import Product


class ProductForm(FormControlMixin, forms.ModelForm):
    FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "category"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in name.split():
            if word.lower() in self.FORBIDDEN_WORDS:
                raise ValidationError(f"{word} - запрещенное слово!")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in description.split():
            if word.lower() in self.FORBIDDEN_WORDS:
                raise ValidationError(f"{word} - запрещенное слово!")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной!")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        image_name = image.name
        if image:
            if image.size > 5 * 1024 * 1025:
                raise ValidationError("Файл больше 5МБ")
            if not (image_name.endswith(".jpg") or image_name.endswith(".jpeg") or image_name.endswith(".png")):
                raise ValidationError("Файл недопустимого формата")
        return image
