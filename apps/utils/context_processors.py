def defer_html(request):
    def get():
        if not hasattr(request, 'defer_html'):
            request.defer_html = []
        return request.defer_html

    def append(html):
        if not hasattr(request, 'defer_html'):
            request.defer_html = []
        request.defer_html.append(html)

    return {
        'get_defer_html': get,
        'append_defer_html': append
    }
    