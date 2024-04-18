from django.urls import path

from movies.views import MovieDetailView, MovieListView


app_name = 'movies'


urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('genres/<slug:slug>/', MovieListView.as_view(), name='movie_list_cats'),
    path('years/<int:int>/', MovieListView.as_view(), name='movie_list_year'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
]

