from django.urls import path

from movies.views import MovieDetailView, MovieListView


app_name = 'movies'


urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('find', MovieListView.as_view(), name='movie_list_find'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
]
