from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.db.models.functions import Round
from django.db.models import Avg, Count, F
from django.shortcuts import get_object_or_404, redirect

from movies.models import *
from movies.forms import RatingForm, CommentForm
from movies.filters import MovieFilter

# Агрегация для вычисления среднего рейтинга и количества голосов
def annotate_rating_movie(instance):
    return instance.annotate(
            rate=Round(Avg('movie__rate'), precision=1),
            vote_count=Count('movie__id'),
        )


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie.html'
    context_object_name = 'movie'

    def post(self, request, **kwargs):
        form_rating = RatingForm(request.POST)
        form_comment = CommentForm(request.POST)
        print(request.POST)
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
                defaults={'rate_id': int(request.POST.get("rate"))}                )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

    def get_object(self):
        queryset = Movie.objects.prefetch_related(
            'country', 'director', 'actors', 'genre'
        )
        queryset = annotate_rating_movie(queryset)
        return get_object_or_404(queryset, slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated:
            user_rating = Rating.objects.get(
                user=self.request.user,
                movie=kwargs['object']
                ).rate
            if user_rating:
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

        if all([field_from_get, value_from_get]):
            if field_from_get == 'year':
                queryset = queryset.filter(year=value_from_get)
            else:      
                fields = ['country', 'director', 'actors', 'genre']

                if field_from_get in fields:
                    key = f'{field_from_get}__name__icontains'
                    filter_movie = {key: value_from_get}
                    queryset = queryset.filter(**filter_movie)

        queryset = annotate_rating_movie(queryset)       
        queryset = queryset.prefetch_related(
            'movie', 'country', 'genre', 'director', 'actors'
        )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_filter'] = MovieFilter()
        return context
