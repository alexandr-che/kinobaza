from django.views.generic import DetailView, ListView
from django.db.models.functions import Round
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from django_filters.views import FilterMixin

from movies.models import *
from movies.filters import MovieFilter


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'

    def get_object(self):
        queryset = Movie.objects.prefetch_related(
            'country', 'director', 'actors', 'genre'
        ).annotate(
            rate=Round(Avg('movie__rate'), precision=1),
            vote_count=Count('movie')            
        )
        return get_object_or_404(queryset, slug=self.kwargs.get('slug'))
    

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):        
        queryset = super().get_queryset()

        # Применяем django_filter на queryset
        queryset = MovieFilter(self.request.GET, queryset=queryset).qs

        # Фильтрация фильмов по параметрам из GET запроса
        field_from_get = self.request.GET.get('f')
        value_from_get = self.request.GET.get('v')

        if all([field_from_get, value_from_get]):
            if field_from_get == 'year':
                queryset = queryset.filter(year=value_from_get)
            else:      
                key = f'{field_from_get}__name__icontains'
                filter_movie = {key: value_from_get}
                
                fields = ['country', 'director', 'actors', 'genre']

                if field_from_get in fields:
                    queryset = queryset.filter(**filter_movie)

        # Агрегация для вычисления среднего рейтинга и количества голосов
        queryset = queryset.annotate(
            rate=Round(Avg('movie__rate'), precision=1),
            vote_count=Count('movie__id'),
        )
        
        queryset = queryset.prefetch_related(
            'movie', 'country', 'genre', 'director', 'actors'
        )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_filter'] = MovieFilter()
        return context
