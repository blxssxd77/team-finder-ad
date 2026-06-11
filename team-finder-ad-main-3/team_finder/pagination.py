from django.core.paginator import Paginator

from team_finder.constants import PAGE_SIZE


def get_page(queryset, request, per_page=PAGE_SIZE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))
