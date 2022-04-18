import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# Класс для описания полей created и modified
class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
    )

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


# Класс для описания поля id
class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


# Класс для описания таблицы genre
class Genre(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.name

    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
    )

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content"."genre'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


# Класс для описания представления таблицы person
class Person(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.full_name

    full_name = models.CharField(
        _("Full name"),
        max_length=255,
    )

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        indexes = [
            models.Index(
                fields=["full_name"],
                name="person_full_name_idx",
            ),
        ]


# Класс для описания представления таблицы film_work
class Filmwork(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.title

    class FilmWorkType(models.TextChoices):
        MOVIE = "movie", _("Movie")
        TV_SHOW = "tv_show", _("TV Show")

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
    )
    creation_date = models.DateField(
        _("Creation date"),
        null=True,
        blank=True,
    )
    rating = models.FloatField(
        _("Rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("Type"),
        max_length=10,
        choices=FilmWorkType.choices,
        default=FilmWorkType.MOVIE,
    )

    file_path = models.FileField(
        _("file"),
        blank=True,
        null=True,
        upload_to="movies/",
    )

    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmwork",
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmWork",
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film work")
        verbose_name_plural = _("Film works")
        indexes = [
            models.Index(
                fields=["title"],
                name="film_work_title_idx",
            ),
            models.Index(
                fields=["creation_date", "rating"],
                name="film_work_creation_rating_idx",
            ),
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        verbose_name=_("Film work"),
    )
    genre = models.ForeignKey(
        "Genre",
        on_delete=models.CASCADE,
        verbose_name=_("Genre"),
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("Filmworks gengre")
        verbose_name_plural = _("Filmworks gengres")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="genre_filmwork_unique",
            ),
        ]
        indexes = [
            models.Index(
                fields=["film_work", "genre"],
                name="genre_film_work_idx",
            ),
        ]


class PersonFilmWork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = "actor", _("Actor")
        DIRECTOR = "director", _("Director")
        WRITER = "writer", _("Writer")

    film_work = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        verbose_name=_("Film work"),
    )
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        verbose_name=_("Person"),
    )
    role = models.TextField(
        _("Role"),
        choices=RoleType.choices,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("Filmworks person")
        verbose_name_plural = _("Filmworks persons")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="person_filmwork_unique",
            ),
        ]
        indexes = [
            models.Index(
                fields=["film_work", "person", "role"],
                name="film_work_person_idx",
            ),
        ]
