from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.db import transaction

from .models import Recipe, Product, RecipeProduct


@transaction.atomic
def add_product_to_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    try:
        recipe_product = RecipeProduct.objects.get(recipe=recipe, product=product)
        recipe_product.weight += int(weight)
        recipe_product.save()
    except RecipeProduct.DoesNotExist:
        RecipeProduct.objects.create(recipe=recipe, product=product, weight=weight)

    return HttpResponse("Product added/updated successfully.")


@transaction.atomic
def cook_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    try:
        recipe = Recipe.objects.select_for_update().get(pk=recipe_id)

        for recipe_product in recipe.recipeproduct_set.all():
            product = recipe_product.product
            product.times_cooked += 1
            product.save()

        return HttpResponse("Рецепт успешно приготовлен.")
    except Recipe.DoesNotExist:
        return HttpResponse("Рецепт не найден.", status=404)


def show_recipes_without_product(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    recipes_without_product = Recipe.objects.exclude(recipeproduct__product=product)
    recipes_with_less_than_10g = Recipe.objects.filter(recipeproduct__product=product, recipeproduct__weight__lt=10)
    context = {
        'product': product,
        'recipes_without_product': recipes_without_product,
        'recipes_with_less_than_10g': recipes_with_less_than_10g,
    }
    return render(request, 'recipes_without_product.html', context)
