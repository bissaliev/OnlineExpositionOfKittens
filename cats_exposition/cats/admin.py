from django.contrib import admin

from .models import Breed, Cat, Rating

admin.site.register(Cat)
admin.site.register(Breed)
admin.site.register(Rating)
