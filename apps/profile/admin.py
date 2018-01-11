from django.contrib import admin
from django.utils import html
from apps.user.models import User
from apps.user.admin import UserAdmin as apps_UserAdmin
from django.utils.encoding import force_text
from django.urls import reverse

from .models import Profile

admin.site.unregister(User)


def get_profile_image(instance):
    if not instance.profileimage.path:
        return
    return html.format_html("""<img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />""",
                            src='/' + instance.profileimage.path.url,
                            title=instance.user.username,
                            )

class ProfileInline(admin.StackedInline):
    """ Profile inline admin model.
    The
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('company','info','expert','visibility_mail','visibility_company',
              'visibility_info','visibility_first_name','visibility_last_name',
              'max_projects','max_datarows','created','updated',
              get_profile_image
              )
    readonly_fields = ('created','updated',get_profile_image)



@admin.register(User)
class UserAdmin(apps_UserAdmin):
    inlines = (ProfileInline,)