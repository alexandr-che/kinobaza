from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.db.models.functions import Round
from django.db.models import Avg, Count, Case, When, BooleanField, Value
from django.shortcuts import get_object_or_404, redirect

from movies.models import *
from movies.forms import RatingForm, CommentForm, FavoriteForm
from movies.filters import MovieFilter

# Аннотация среднего рейтинга, количества голосов, есть ли фильм в избранном
def annotate_rating_movie(self, qs):
    fav_movie_user = FavoriteMovie.objects.filter(user=self.request.user)
    fav_movie_user = [movie_in_fav.movie.pk for movie_in_fav in fav_movie_user]
    return qs.annotate(
            rate=Round(Avg('movie__rate'), precision=1),
            vote_count=Count('movie__id'),
            is_favorite=Case(
                When(pk__in=fav_movie_user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'
    context_object_name = 'movie'

    def post(self, request, **kwargs):
        form_rating = RatingForm(request.POST)
        form_comment = CommentForm(request.POST)
        form_favorite = FavoriteForm(request.POST)

        if 'comment' in request.POST:
            if form_comment.is_valid():
                Comment.objects.update_or_create(
                    to_movie_id = int(request.POST.get('id_movie')),
                    user = request.user,
                    comment = request.POST.get('comment')
                )               
                return redirect('movies:movie_detail', slug=self.kwargs['slug'])
            else:
                return HttpResponse(status=400)
 
        if form_rating.is_valid():
            Rating.objects.update_or_create(
            movie_id=int(request.POST.get("movie")),
                user=self.request.user,
                defaults={'rate_id': int(request.POST.get("rate"))}
                )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

    def get_object(self):
        queryset = Movie.objects.prefetch_related(
            'country', 'director', 'actors', 'genre'
        )
        queryset = annotate_rating_movie(self, queryset)
        return get_object_or_404(queryset, slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated:
            try:
                user_rating = Rating.objects.get(
                    user=self.request.user,
                    movie=kwargs['object']
                    ).rate
            except:
                user_rating = 0
        
            context['user_rating'] = int(str(user_rating))

        return context
    

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
        search_from_get = self.request.GET.get('search')

        if search_from_get:
            queryset = Movie.objects.filter(
                title__icontains=search_from_get.capitalize()
            )

        if all([field_from_get, value_from_get]):
            if field_from_get == 'year':
                queryset = queryset.filter(year=value_from_get)
            else:      
                fields = ['country', 'director', 'actors', 'genre']

                if field_from_get in fields:
                    key = f'{field_from_get}__name__icontains'
                    filter_movie = {key: value_from_get}
                    queryset = queryset.filter(**filter_movie)

        queryset = annotate_rating_movie(self, queryset)      
        queryset = queryset.prefetch_related(
            'movie', 'country', 'genre', 'director', 'actors',
        )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_filter'] = MovieFilter()
        return context
