from django.contrib import admin
from .models import Project, Category
from django.utils.translation import gettext_lazy as _

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory',  'manufacturer')
    list_filter = ('category', 'subcategory')
    readonly_fields=('created', 'updated')

    fieldsets = (
        (None, {'fields': ('name', 'user', 'visibility')}),
        (_('attributes'), {'fields': ('category', 'subcategory', 'manufacturer', 'typ',)}),
        (_('Important dates'), {'fields': ('created', 'updated')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
