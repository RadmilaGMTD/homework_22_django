from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Контент")
    image = models.ImageField(upload_to="blog/image", null=True, blank=True, verbose_name="Изображение")
    created_at = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    is_publication = models.BooleanField(default=False, verbose_name="Признак публикации")
    views = models.IntegerField(verbose_name="Количество просмотров", default=0)

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ['-is_publication', '-created_at']

    def __str__(self):
        return f"{self.title}"
