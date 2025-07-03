from django.db import models
from django.contrib.auth.models import User
import string
import random


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_short_code(self):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=6))

    def generate_unique_code(self):
        code = self.generate_short_code()
        while Link.objects.filter(short_code=code).exists():
            code = self.generate_short_code()
        return code

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.original_url} → {self.short_code}'
    


class ShortLink(models.Model):
    original = models.URLField(max_length=250)
    short = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.short} -> {self.original}'