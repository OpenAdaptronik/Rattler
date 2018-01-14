from django.contrib import admin
from django.utils import html
from apps.user.models import User
from apps.user.admin import UserAdmin as apps_UserAdmin
from django.utils.encoding import force_text
from django.urls import reverse

from .models import Profile,ProfileImage

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    def get_profile_image(instance):
        if not instance.profileimage.path:
            return
        return html.format_html("""<img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />""",
                                src='/' + instance.profileimage.path.url,
                                title=instance.user.username,
                                )

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
              'get_edit_link',get_profile_image
              )
    readonly_fields = ('created','updated','get_edit_link',get_profile_image)

    def get_edit_link(self, instance):
        if not instance.profileimage.path:
            return

        url = reverse('admin:%s_%s_change' % (instance.profileimage._meta.app_label, instance.profileimage._meta.model_name),
                      args=[force_text(instance.profileimage.id)])

        return html.format_html("""<a href="{url}">{text}</a>""".format(
                url=url,
                text="Ändere Bild %s auf Seperaten Seite" % instance.profileimage._meta.verbose_name,
        ))


@admin.register(User)
class UserAdmin(apps_UserAdmin):
    inlines = (ProfileInline,)

@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):

    def get_profile_image(instance):
        if not instance.path:
            return
        return html.format_html("""<img src="{src}" style="max-width: 200px; max-height: 200px;" />""",
                                src='/' + instance.path.url,
                                )

    save_on_top = True
    fields = ('path','created','updated', get_profile_image)
    readonly_fields = ('created', 'updated', get_profile_image)