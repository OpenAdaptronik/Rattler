from django.contrib import admin

from apps.user.models import User
from apps.user.admin import UserAdmin as apps_UserAdmin

from .models import Profile

admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    """ Profile inline admin model.
    The 
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'




@admin.register(User)
class UserAdmin(apps_UserAdmin):
    inlines = (ProfileInline, )
