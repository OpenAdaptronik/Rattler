from django.contrib import admin
from .models import Project, Category

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory',  'manufacturer')
    list_filter = ('category', 'subcategory')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
