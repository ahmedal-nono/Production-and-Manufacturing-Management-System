from rest_framework.pagination import PageNumberPagination


class OptInPagination(PageNumberPagination):
    """Pagination that only activates when the client asks for it.

    The existing frontend reads many endpoints as a plain JSON array, so
    paginating them by default would change their response shape. Clients may
    send ``?page=`` or ``?page_size=`` to opt in and receive the standard
    ``{"count", "next", "previous", "results"}`` envelope instead.
    """

    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500

    def paginate_queryset(self, queryset, request, view=None):
        if (
            self.page_query_param not in request.query_params
            and self.page_size_query_param not in request.query_params
        ):
            return None
        # Keep page boundaries stable when the view does not define ordering.
        if getattr(queryset, 'ordered', True) is False:
            queryset = queryset.order_by('pk')
        return super().paginate_queryset(queryset, request, view)
