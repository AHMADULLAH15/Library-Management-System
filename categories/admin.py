from django.contrib import admin
from categories.models import Category

# Register your models here.
class CategoryName_Admin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name','slug']
admin.site.register(Category,CategoryName_Admin)