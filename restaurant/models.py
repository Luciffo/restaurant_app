from django.db import models

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.PositiveIntegerField()  # Вес в граммах
    image = models.ImageField(upload_to='dishes/')

    def __str__(self):
        return self.name