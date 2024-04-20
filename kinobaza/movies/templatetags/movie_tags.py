from django import template

from movies.models import Comment, Genre, Movie


register = template.Library()


@register.inclusion_tag('movies/inclusions_tags/comments.html')
def show_comments(movie):
    comments = movie.to_movie.filter(to_movie=movie.pk)
    return {'comments': comments}


@register.inclusion_tag('movies/inclusions_tags/genres.html')
def show_genres():
    genres = Genre.objects.all()
    return {'genres': genres}


@register.inclusion_tag('movies/inclusions_tags/years.html')
def show_years():
    years = sorted([year[0] for year in Movie.objects.values_list('year')])
    return {'years': years}
