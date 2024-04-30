import django_filters

from movies.models import Movie, Genre, Country, Collections


class MovieFilter(django_filters.FilterSet):
    year = django_filters.MultipleChoiceFilter(
        choices=[
            (year, year) for year in Movie.objects.values_list(
                'year', flat=True).distinct().order_by('year')
        ],
        method='filter_by_year',
        label = 'Год'
    )

    genre = django_filters.ModelMultipleChoiceFilter(
        field_name = 'genre__name',
        lookup_expr = 'icontains',
        queryset = Genre.objects.all(),
        label = 'Жанр'
    )

    country = django_filters.ModelMultipleChoiceFilter(
        field_name = 'country__name',
        lookup_expr = 'icontains',
        queryset = Country.objects.all().order_by('name'),
        label = 'Страна'
    )

    collection = django_filters.ModelMultipleChoiceFilter(
        field_name = 'collections',
        queryset = Collections.objects.all(),
        label = 'Подборки'
    )

    class Meta:
        model = Movie
        fields = []

    def filter_by_year(self, queryset, name, value):
        return queryset.filter(**{f'{name}__in': value})
