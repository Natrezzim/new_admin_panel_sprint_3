import logging

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import BaseListView

from ...models import Filmwork, Role

logger = logging.getLogger("Paginator Logger")
logger.setLevel(logging.DEBUG)


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def _aggregate_person(role):
        return ArrayAgg('persons__full_name', filter=Q(personfilmwork__role=role), distinct=True)

    @staticmethod
    def get_queryset():
        context = Filmwork.objects.order_by('title').values('id', 'title', 'description', 'creation_date',
                                                            'rating', 'type', ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=MoviesApiMixin._aggregate_person(Role.ACTOR),
            directors=MoviesApiMixin._aggregate_person(Role.DIRECTOR),
            writers=MoviesApiMixin._aggregate_person(Role.WRITER))
        return context

    @staticmethod
    def render_to_response(context):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, DetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return kwargs['object']
