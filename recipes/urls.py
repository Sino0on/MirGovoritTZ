from django.urls import path
from recipes.views import show_recipes_without_product, cook_recipe, add_product_to_recipe


urlpatterns = [
    path('cook_recipe/', cook_recipe),
    path('add_product_to_recipe/', add_product_to_recipe),
    path('show_recipes_without_product/', show_recipes_without_product,
         name='show_recipes_without_product'),
]
