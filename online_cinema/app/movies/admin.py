from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1
    autocomplete_fields = ('film_work','genre',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('film_work', 'genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1
    autocomplete_fields = ('film_work','person',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('film_work', 'person',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating')
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')




@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('id', 'full_name')
