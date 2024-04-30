from django import template
from django.db.models import Prefetch

from movies.models import Genre, Movie, Comment
from users.models import User


register = template.Library()


@register.inclusion_tag('movies/inclusions_tags/comments.html')
def show_comments(movie):
    user_fields = ('username', 'avatar')
    comments = Comment.objects.filter(
        to_movie=movie.pk).prefetch_related(
            Prefetch('user', queryset=User.objects.only(*user_fields))
        )
    return {'comments': comments}


@register.inclusion_tag('movies/inclusions_tags/genres.html')
def show_genres():
    genres = Genre.objects.all()
    return {'genres': genres}


@register.inclusion_tag('movies/inclusions_tags/years.html')
def show_years():
    years = Movie.objects.values_list('year', flat=True).order_by('year')
    return {'years': years}
