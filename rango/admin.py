from django.contrib import admin

from rango.models import Category, Page, UserProfile


# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)


@admin.register(Page)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")
