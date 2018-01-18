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

    """ The Profile admin model.
    Attributes:
        See django.contrib.auth.models.AbstractUser.
        fieldsets: The fieldset to show in the admin.
        list_display: The data to show in the list.
        search_fields: To filter
    """
    list_display = ('name',
                    'category',
                    'subcategory',
                    'manufacturer',
                    'visibility')

    readonly_fields = ('created',
                       'updated',
                       get_project_image)

    """ search_fields: Filter Searchfield.
        list_filter: Filter Checkbox visibility 
    """
    search_fields = ['category__name',
                     'subcategory__name',
                     'manufacturer',
                     'name',
                     'user__username',
                     'description',
                     'typ',
                     'experiment__name',
                     'experiment__description',
                     ]

    list_filter = ('visibility',)

    fieldsets = (
        (None, {'fields': ('name', 'user', 'visibility')}),
        (_('attributes'), {'fields': ('category', 'subcategory', 'manufacturer', 'typ','description',)}),
        (_('Important dates'), {'fields': ('created', 'updated')}),
        (_('Images'), {'fields': ('created', 'updated', get_project_image)}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ['name',
                     'parent'
                     ]
