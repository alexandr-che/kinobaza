from django.views.generic import DetailView, ListView

from movies.models import *


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'
    

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'
