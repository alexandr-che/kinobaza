from django.views.generic import DetailView, ListView
from django.db.models import Count, F

from movies.models import *


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'
    

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        field_from_get = self.request.GET.get('f')
        value = self.request.GET.get('v')

        if field_from_get == 'year':
            return Movie.objects.filter(
                year=value
            ).prefetch_related('genre', 'actors', 'director', 'country')            

        key = f'{field_from_get}__name__icontains'
        filter_movie = {key: value}
        
        fields = ['country', 'director', 'actors', 'genre']

        if field_from_get in fields:
            return Movie.objects.filter(**filter_movie).prefetch_related(
                'genre', 'actors', 'director', 'country')

        return Movie.objects.all().prefetch_related('genre', 'actors', 'director', 'country')
