from django.contrib import admin
from rango.models import Category, Title

admin.site.register(Category)
# admin.site.register(Title)


@admin.register(Title)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")

