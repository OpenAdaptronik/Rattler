def defer_html(request):
    def get_defer_html():
        if not hasattr(request, 'defer_html'):
            request.defer_html = []
        return request.defer_html

    def append_defer_html(html):
        if not hasattr(request, 'defer_html'):
            request.defer_html = []
        request.defer_html.append(html)

    def get_defer_head():
        if not hasattr(request, 'defer_head'):
            request.defer_head = []
        return request.defer_head

    def append_defer_head(html):
        if not hasattr(request, 'defer_head'):
            request.defer_head = []
        request.defer_head.append(html)

    return {
        'get_defer_html': get_defer_html,
        'append_defer_html': append_defer_html,
        'get_defer_head': get_defer_head,
        'append_defer_head': append_defer_head,
    }
    