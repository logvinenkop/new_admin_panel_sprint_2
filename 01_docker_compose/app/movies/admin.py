from pyexpat import model
from django.contrib import admin
from .models import Genre
from .models import Filmwork
from .models import GenreFilmwork
from .models import Person
from .models import PersonFilmWork
from django.utils.translation import gettext_lazy as _


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ["person"]


# Фильтр по диапазонам значений рейтинга кинопроизведения
class RatingDateListFilter(admin.SimpleListFilter):
    title = _("rating")

    parameter_name = "rating_range"

    def lookups(self, request, model_admin):
        return (
            ("0_10", _("from 0 to 10")),
            ("10_20", _("from 10 to 20")),
            ("20_30", _("from 20 to 30")),
            ("30_40", _("from 30 to 40")),
            ("40_50", _("from 40 to 50")),
            ("50_60", _("from 50 to 60")),
            ("60_70", _("from 60 to 70")),
            ("70_80", _("from 70 to 80")),
            ("80_90", _("from 80 to 90")),
            ("90_100", _("from 90 to 100")),
        )

    def queryset(self, request, queryset):
        if self.value() == "0_10":
            return queryset.filter(
                rating__gte=0.0,
                rating__lte=10.0,
            )
        if self.value() == "10_20":
            return queryset.filter(
                rating__gte=10.0,
                rating__lte=20.0,
            )
        if self.value() == "20_30":
            return queryset.filter(
                rating__gte=20.0,
                rating__lte=30.0,
            )
        if self.value() == "30_40":
            return queryset.filter(
                rating__gte=30.0,
                rating__lte=40.0,
            )
        if self.value() == "40_50":
            return queryset.filter(
                rating__gte=40.0,
                rating__lte=50.0,
            )
        if self.value() == "50_60":
            return queryset.filter(
                rating__gte=50.0,
                rating__lte=60.0,
            )
        if self.value() == "60_70":
            return queryset.filter(
                rating__gte=60.0,
                rating__lte=70.0,
            )
        if self.value() == "70_80":
            return queryset.filter(
                rating__gte=70.0,
                rating__lte=80.0,
            )
        if self.value() == "80_90":
            return queryset.filter(
                rating__gte=80.0,
                rating__lte=90.0,
            )
        if self.value() == "90_100":
            return queryset.filter(
                rating__gte=90.0,
                rating__lte=100.0,
            )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created",
        "modified",
    )

    # Поиск по полям
    search_fields = (
        "name",
        "description",
        "id",
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "created",
        "modified",
    )

    # Поиск по полям
    search_fields = (
        "full_name",
        "id",
    )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmWorkInline)

    # Отображение полей в списке
    list_display = (
        "title",
        "type",
        "get_genres",
        "creation_date",
        "rating",
        "created",
        "modified",
    )

    list_prefetch_related = ("genres", "persons")

    # Переопределение метода get_queryset для минимизации количества запросов к БД
    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = "Жанры фильма"

    # Фильтрация в списке
    list_filter = (
        "type",
        RatingDateListFilter,
    )

    # Поиск по полям
    search_fields = (
        "title",
        "description",
        "id",
    )
