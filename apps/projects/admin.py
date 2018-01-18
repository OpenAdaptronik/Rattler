from django.contrib import admin
from .models import Project, Category,ProjectImage
from django.utils import html
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_text
from django.urls import reverse

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def get_project_image(instance):
        if not instance.projectimage.path:
            return
        return html.format_html("""<img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />""",
                                src='/' + instance.projectimage.path.url,
                                title=instance.name,
                                )

    list_display = ('name', 'category', 'subcategory', 'manufacturer', 'visibility')
    list_filter = ('category', 'subcategory')
    readonly_fields = ('created', 'updated',
                        get_project_image)

    fieldsets = (
        (None, {'fields': ('name', 'user', 'visibility')}),
        (_('attributes'), {'fields': ('category', 'subcategory', 'manufacturer', 'typ','description',)}),
        (_('Important dates'), {'fields': ('created', 'updated')}),
        (_('Images'), {'fields': ('created', 'updated', get_project_image)}),
    )





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
