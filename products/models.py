from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

