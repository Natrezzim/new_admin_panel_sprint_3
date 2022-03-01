import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Role(models.TextChoices):
    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('title'), max_length=50)

    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"

        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('person name'), max_length=50)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        indexes = [
            models.Index(fields=['id', 'full_name'], name='person_idx'),
        ]

        verbose_name = _('person')
        verbose_name_plural = _('person')


class Filmwork(UUIDMixin, TimeStampedMixin):
    
    title = models.TextField(_('title'), max_length=200)

    description = models.TextField(_('description'), blank=True, max_length=3000, null=True)

    creation_date = models.DateField(_('release date'), null=True)

    rating = models.FloatField(_('rating'), null=True, blank=True,
                               validators=[MinValueValidator(0.0),
                                           MaxValueValidator(10.0)]
                               )

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Type(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    type = models.TextField(
        _('type'),
        max_length=50,
        choices=Type.choices,
        default=Type.MOVIE
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"

        indexes = [
            models.Index(fields=['id', 'title', 'creation_date'], name='film_work_idx'),
        ]

        verbose_name = _('film work')
        verbose_name_plural = _('film works')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', verbose_name=_('film_work'), on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='genre_film_work_idx'),
        ]

        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', verbose_name=_('film_work'), on_delete=models.CASCADE)
    person = models.ForeignKey('Person', verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''

    role = models.TextField(
        _('role'),
        max_length=50,
        choices=Role.choices,
        default=Role.ACTOR
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'person_id'], name='person_film_work_idx'),
                   ]

        verbose_name = _('role')
        verbose_name_plural = _('roles')
