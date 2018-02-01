from django.contrib import admin
from django.urls import reverse
from django.utils import html
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _

from apps.user.admin import UserAdmin as apps_UserAdmin
from apps.user.models import User

from .models import Profile,ProfileImage

admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    """ The Profile admin Inline.
    get Profile Image and shows it
    """
    def get_profile_image(instance):
        if not instance.profileimage.path:
            return
        return html.format_html("""<img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />""",
                                src='/' + instance.profileimage.path.url,
                                title=instance.user.username,
                                )

    get_profile_image.short_description = _('profil image')

    """ The Profile admin Inline.
     Attributes:
         fk_name: ForeignKey name
         fields: The field to show in the admin.
         list_display: The data to show in the list.
         readonly_fields:
     """
    model = Profile
    can_delete = False
    verbose_name = _('profile')
    verbose_name_plural = _('profile')
    fk_name = 'user'
    fields = ('company',
              'info',
              'expert',
              'visibility_mail',
              'visibility_company',
              'visibility_info',
              'visibility_first_name',
              'visibility_last_name',
              'max_projects',
              'max_datarows',
              'created',
              'updated',
              'get_edit_link',
              get_profile_image
              )
    readonly_fields = ('created','updated','get_edit_link',get_profile_image)

    """ The Profile admin model.
        Link to Change Profile Image to AdminProfileImage 
    """
    def get_edit_link(self, instance):
        if not instance.profileimage.path:
            return

        url = reverse('admin:%s_%s_change' % (instance.profileimage._meta.app_label, instance.profileimage._meta.model_name),
                      args=[force_text(instance.profileimage.id)])

        return html.format_html("""<a href="{url}">{text}</a>""".format(
                url=url,
                text="Ändere Bild %s auf Seperaten Seite" % instance.profileimage._meta.verbose_name,
        ))

    get_edit_link.short_description = _('profile image link')

    """ The User admin.
        User get Attributes from Profile via inlines
    """

@admin.register(User)
class UserAdmin(apps_UserAdmin):
    inlines = (ProfileInline,)

    """ search_fields: Filter Searchfield.
        list_filter: Filter Checkbox visibility 
    """
    search_fields = ['username',
                     'email',
                     'first_name',
                     'last_name',
                     'profile__company',
                     'profile__info',
                     ]
    list_filter = ('is_active',
                   'is_superuser',
                   'is_staff',
                   'profile__expert',
                   'profile__visibility_mail',
                   'profile__visibility_company',
                   'profile__visibility_info',
                   'profile__visibility_first_name',
                   'profile__visibility_last_name',
    )

@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):

    """ The ProfileImage admin.
        change or delete ProfileImage
    """

    def get_profile_image(instance):
        if not instance.path:
            return
        return html.format_html("""<img src="{src}" style="max-width: 200px; max-height: 200px;" />""",
                                src='/' + instance.path.url,
                                )

    get_profile_image.short_description = _('profil image')
    save_on_top = True
    fields = ('path',
              'created',
              'updated',
              get_profile_image)

    readonly_fields = ('created',
                       'updated',
                       get_profile_image)
