from django.shortcuts import HttpResponseRedirect
from django.utils.encoding import force_text

class NoLoginRequiredMixin(object):
    redirect_url=None

    def get_redirect_url(self):
        """
        Override this method to override the redirect attribute.
        """
        redirect_url = self.redirect_url or '/'
        return force_text(redirect_url)
    
    def handle_no_permission(self):
        """Redirects to the redirect url.
        
        Returns:
            HttpResponseRedirect -- The redirect response
        """
        
        return HttpResponseRedirect(self.get_redirect_url())

    """
    CBV mixin which verifies that the current user is not authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super(NoLoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    

