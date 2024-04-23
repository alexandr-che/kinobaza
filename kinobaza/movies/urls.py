from django.urls import path

from django_filters.views import FilterView

from movies.views import MovieDetailView, MovieListView
from movies.models import Movie


app_name = 'movies'


urlpatterns = [
    path('', MovieListView.as_view(model=Movie), name='movie_list'),
    path('find', MovieListView.as_view(), name='movie_list_find'),
    path('filter/', FilterView.as_view(model=Movie), name='movie_filter'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
]
