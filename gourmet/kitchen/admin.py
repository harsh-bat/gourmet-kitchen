from django.contrib import admin
from . models import Everyone, Recipe, Ingredient,Rating
# Register your models here.
admin.site.register(Everyone)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Rating)
