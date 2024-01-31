from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    times_cooked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField()
