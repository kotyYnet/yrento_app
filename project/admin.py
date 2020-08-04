from django.contrib import admin

# Register your models here.
from .models import Items, Categories, Dormitories

admin.site.register(Items)
admin.site.register(Categories)
admin.site.register(Dormitories)
